# Technology Stack

## Backend
- Python 3.x
- FastAPI (API framework)
- Uvicorn (ASGI server)
- Pydantic v2
- pydantic-settings
- GitPython (repository cloning)
- httpx, orjson, tenacity
- python-multipart

## Code Analysis (planned/partial)
- tree-sitter (core)
- tree-sitter-python
- tree-sitter-javascript
- tree-sitter-typescript
- tree-sitter-java
- tree-sitter-go
- tree-sitter-rust
- tree-sitter-cpp

## Databases
- Neo4j (graph database)
- Qdrant (vector database)

## Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- Cytoscape.js (graph visualization)
- cytoscape-fcose (layout)
- cytoscape-cola (layout)
- clsx, tailwind-merge
- lucide-react (icons)

## AI/Embedding (extensible)
- OpenAI (client)
- tiktoken (tokenization)

## Dev & Tooling
- Node.js & npm
- ESLint (+ @typescript-eslint)
- Docker & Docker Compose
- cURL, Git

## Runtime Ports (defaults)
- Frontend (Vite): 3000 (dev), may auto-switch to 3001/3002
- Backend: 8001 (local dev), 8000 (Docker Compose)
- Neo4j: 7474 (HTTP), 7687 (Bolt)
- Qdrant: 6333 (HTTP), 6334 (gRPC)
