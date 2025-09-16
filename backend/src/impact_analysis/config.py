import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database connections
    neo4j_uri: str = "bolt://neo4j:7687"
    neo4j_user: str = "neo4j"
    neo4j_pass: str = "password"
    
    qdrant_host: str = "qdrant:6333"
    qdrant_port: int = 6333
    
    # API keys
    embedding_api_key: Optional[str] = None
    github_token: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    # Application settings
    max_chunk_tokens: int = 1000
    embedding_model: str = "text-embedding-3-small"
    embedding_dimension: int = 1536
    
    # File processing
    supported_extensions: list = [".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs", ".cpp", ".c", ".h", ".hpp"]
    max_file_size_mb: int = 10
    
    # RAG settings
    top_k_chunks: int = 8
    top_k_graph_nodes: int = 10
    max_context_tokens: int = 4000
    
    # Worker settings
    max_workers: int = 4
    batch_size: int = 100
    
    # Data paths
    data_dir: str = "/app/data"
    repos_dir: str = "/app/data/repos"
    chunks_dir: str = "/app/data/chunks"
    cache_dir: str = "/app/data/cache"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
