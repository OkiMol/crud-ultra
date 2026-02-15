from fastapi import FastAPI, Response, HTTPException
from pydantic import BaseModel, Field
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from typing import Dict
from uuid import uuid4

app = FastAPI(title="CRUD Ultra")

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

@app.middleware("http")
async def metrics_middleware(request, call_next):
    response = await call_next(request)

    # Avoid self-scrape noise
    if request.url.path != "/metrics":
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=str(response.status_code)
        ).inc()

    return response

# --- Health / Readiness / Metrics ---

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    # Later: add DB connectivity check here
    return {"status": "ready"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# --- CRUD (in-memory) ---

class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)

class Item(ItemCreate):
    id: str

_STORE: Dict[str, Item] = {}

@app.post("/items", response_model=Item, status_code=201)
def create_item(payload: ItemCreate):
    item_id = str(uuid4())
    item = Item(id=item_id, **payload.model_dump())
    _STORE[item_id] = item
    return item

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: str):
    item = _STORE.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.get("/items", response_model=list[Item])
def list_items():
    return list(_STORE.values())

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: str):
    if item_id not in _STORE:
        raise HTTPException(status_code=404, detail="Item not found")
    del _STORE[item_id]
    return Response(status_code=204)
