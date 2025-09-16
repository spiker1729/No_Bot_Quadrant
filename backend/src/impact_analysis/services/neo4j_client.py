from __future__ import annotations
import os
from neo4j import GraphDatabase
from typing import Iterable

_NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
_NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
_NEO4J_PASS = os.getenv("NEO4J_PASS", "neo4jpass")

class Neo4jDriver:
    def __init__(self):
        self.driver = GraphDatabase.driver(_NEO4J_URI, auth=(_NEO4J_USER, _NEO4J_PASS))
        self._ensure_indexes()

    def _ensure_indexes(self):
        cypher = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (f:File) REQUIRE f.path IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Code) REQUIRE c.id IS UNIQUE",
        ]
        with self.driver.session() as s:
            for stmt in cypher:
                s.run(stmt)

    def upsert_code_node(self, chunk_id: str, path: str, symbol: str, kind: str):
        with self.driver.session() as s:
            s.run(
                "MERGE (f:File {path:$path})"
                "MERGE (n:Code {id:$id}) SET n.symbol=$symbol, n.kind=$kind"
                "MERGE (f)-[:CONTAINS]->(n)",
                path=path, id=chunk_id, symbol=symbol, kind=kind
            )

__all__ = ["Neo4jDriver"]