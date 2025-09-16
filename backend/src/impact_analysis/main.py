from fastapi import FastAPI
from .api.routes_ingest import router as ingest_router
from .api.routes_chunks import router as chunks_router
from .api.routes_analyze import router as analyze_router
from .api.routes_ask import router as ask_router
from .api.routes_graph import router as graph_router

app = FastAPI(title="Impact Analysis Tool (Public Repos Only)")
app.include_router(ingest_router)
app.include_router(chunks_router)
app.include_router(analyze_router)
app.include_router(ask_router)
app.include_router(graph_router)

# Root health
@app.get("/")
async def root():
    return {"status": "ok"}