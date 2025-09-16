from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import os

router = APIRouter(prefix="/api", tags=["graph"])

@router.get("/graph/{node_id:path}")
def get_graph(node_id: str):
    # Create a sample graph structure for demonstration
    nodes = [node_id]
    edges = []
    
    # Add some related nodes based on the node_id
    if node_id.endswith('.py'):
        # For Python files, create related function/class nodes
        base_name = node_id.replace('.py', '')
        related_nodes = [
            f"{base_name}_function_1",
            f"{base_name}_function_2", 
            f"{base_name}_class_A",
            f"test_{base_name}.py"
        ]
        nodes.extend(related_nodes)
        
        # Create edges showing relationships
        for related in related_nodes:
            if related.startswith('test_'):
                edges.append({"source": related, "target": node_id, "label": "tests"})
            else:
                edges.append({"source": node_id, "target": related, "label": "contains"})
    
    elif node_id.endswith(('.ts', '.tsx', '.js', '.jsx')):
        # For JavaScript/TypeScript files
        base_name = node_id.split('.')[0]
        related_nodes = [
            f"{base_name}_component",
            f"{base_name}_hook",
            f"{base_name}_utils"
        ]
        nodes.extend(related_nodes)
        
        for related in related_nodes:
            edges.append({"source": node_id, "target": related, "label": "exports"})
    
    else:
        # For functions/classes, create a small dependency graph
        related_nodes = [
            f"dependency_1",
            f"dependency_2",
            f"caller_function",
            f"imported_module"
        ]
        nodes.extend(related_nodes)
        
        edges.extend([
            {"source": "imported_module", "target": node_id, "label": "imports"},
            {"source": node_id, "target": "dependency_1", "label": "calls"},
            {"source": node_id, "target": "dependency_2", "label": "uses"},
            {"source": "caller_function", "target": node_id, "label": "calls"}
        ])
    
    return {"node_id": node_id, "nodes": nodes, "edges": edges}


class ListNodesRequest(BaseModel):
    repo_path: str


@router.post("/graph/list_nodes")
def list_nodes(body: ListNodesRequest):
    repo_path = Path(body.repo_path)
    if not repo_path.exists():
        raise HTTPException(status_code=400, detail="repo_path not found")

    # Very simple stub: return up to 200 code-like files as node ids
    exts = {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".java", ".rb"}
    nodes: list[str] = []
    for root, _dirs, files in os.walk(repo_path):
        for f in files:
            p = Path(root) / f
            if p.suffix in exts:
                # node id: path relative to repo root
                rel = str(p.relative_to(repo_path))
                nodes.append(rel)
                if len(nodes) >= 200:
                    break
        if len(nodes) >= 200:
            break

    return {"nodes": nodes}


class FullGraphRequest(BaseModel):
    repo_path: str


@router.post("/graph/full")
def full_graph(body: FullGraphRequest):
    repo_path = Path(body.repo_path)
    if not repo_path.exists():
        raise HTTPException(status_code=400, detail="repo_path not found")

    # Build a more meaningful graph: files with potential relationships
    exts = {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".java", ".rb"}
    nodes = []
    edges = []
    
    # Collect all code files
    code_files = []
    for root, _dirs, files in os.walk(repo_path):
        for f in files:
            p = Path(root) / f
            if p.suffix in exts:
                rel = str(p.relative_to(repo_path))
                code_files.append(rel)
                nodes.append({"id": rel, "label": f, "kind": "file"})
                if len(nodes) >= 100:  # Limit for performance
                    break
        if len(nodes) >= 100:
            break

    # Create relationships based on file patterns and names
    for i, file1 in enumerate(code_files):
        for file2 in code_files[i+1:]:
            # Create edges based on naming patterns
            file1_name = Path(file1).stem
            file2_name = Path(file2).stem
            
            # Test file relationships
            if file1_name.startswith('test_') and file1_name[5:] == file2_name:
                edges.append({"source": file1, "target": file2, "label": "tests"})
            elif file2_name.startswith('test_') and file2_name[5:] == file1_name:
                edges.append({"source": file2, "target": file1, "label": "tests"})
            
            # Component relationships (React/Vue)
            elif (file1.endswith(('.tsx', '.jsx')) and file2.endswith(('.ts', '.js')) and 
                  file1_name.lower() == file2_name.lower()):
                edges.append({"source": file1, "target": file2, "label": "uses"})
            
            # Utils/helpers
            elif 'util' in file1_name.lower() or 'helper' in file1_name.lower():
                edges.append({"source": file2, "target": file1, "label": "imports"})
            elif 'util' in file2_name.lower() or 'helper' in file2_name.lower():
                edges.append({"source": file1, "target": file2, "label": "imports"})
            
            # Same directory files (potential relationships)
            elif Path(file1).parent == Path(file2).parent and len(edges) < 200:
                edges.append({"source": file1, "target": file2, "label": "related"})

    return {"nodes": nodes, "edges": edges}


class RepoTreeRequest(BaseModel):
    repo_path: str
    max_nodes: int | None = 800


@router.post("/graph/repo_tree")
def repo_tree(body: RepoTreeRequest):
    repo_path = Path(body.repo_path)
    if not repo_path.exists():
        raise HTTPException(status_code=400, detail="repo_path not found")

    # Build a directory tree graph: repo -> dirs -> files
    max_nodes = body.max_nodes or 800
    nodes: dict[str, dict] = {}
    edges: list[dict] = []

    def add_node(node_id: str, label: str, kind: str):
        if node_id not in nodes:
            nodes[node_id] = {"id": node_id, "label": label, "kind": kind}

    repo_id = repo_path.name
    add_node(repo_id, repo_id, "repo")

    count = 1
    for root, _dirs, files in os.walk(repo_path):
        rel_root = Path(root).relative_to(repo_path)
        parent_id = repo_id if str(rel_root) == "." else str(rel_root).replace("\\", "/")
        if parent_id != repo_id:
            add_node(parent_id, parent_id, "dir")
            # Edge from repo to top-level dirs
            if "/" not in parent_id:
                edges.append({"source": repo_id, "target": parent_id, "label": "contains"})

        for f in files:
            p = Path(root) / f
            file_id = str(p.relative_to(repo_path)).replace("\\", "/")
            add_node(file_id, file_id, "file")
            edges.append({"source": parent_id, "target": file_id, "label": "contains"})
            count += 1
            if count >= max_nodes:
                break
        if count >= max_nodes:
            break

    return {"nodes": list(nodes.values()), "edges": edges, "root": repo_id}

__all__ = ["router"]