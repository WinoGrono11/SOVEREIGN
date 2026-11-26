"""Explicit, local-first memory storage.

Nothing is stored unless a caller explicitly invokes MemoryStore.add().
The module never captures prompts, model outputs, or tool activity on its own.
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class MemoryStore:
    """SQLite-backed memory with explicit CRUD, search, and JSON export."""

    def __init__(self, database: str | Path) -> None:
        self.database = str(database)
        if self.database != ":memory:":
            Path(self.database).expanduser().parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    tags_json TEXT NOT NULL,
                    source TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_updated ON memories(updated_at)"
            )

    def add(
        self,
        content: str,
        *,
        tags: Iterable[str] = (),
        source: str | None = None,
    ) -> dict[str, Any]:
        """Store one memory. This explicit call is the only write-on-create path."""
        if not isinstance(content, str) or not content.strip():
            raise ValueError("content must be a non-empty string")
        normalized_tags = sorted({tag.strip() for tag in tags if tag.strip()})
        memory_id = str(uuid.uuid4())
        timestamp = _now()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO memories (id, content, tags_json, source, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    memory_id,
                    content.strip(),
                    json.dumps(normalized_tags, ensure_ascii=False),
                    source,
                    timestamp,
                    timestamp,
                ),
            )
        return self.get(memory_id)  # type: ignore[return-value]

    def get(self, memory_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM memories WHERE id = ?", (memory_id,)
            ).fetchone()
        return self._to_dict(row) if row else None

    def search(self, query: str, *, limit: int = 20) -> list[dict[str, Any]]:
        """Case-insensitive substring search; no embedding service required."""
        if limit < 1:
            raise ValueError("limit must be at least 1")
        term = query.strip()
        if not term:
            return []
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM memories
                WHERE instr(lower(content), lower(?)) > 0
                   OR instr(lower(tags_json), lower(?)) > 0
                ORDER BY updated_at DESC
                LIMIT ?
                """,
                (term, term, limit),
            ).fetchall()
        return [self._to_dict(row) for row in rows]

    def update(
        self,
        memory_id: str,
        *,
        content: str | None = None,
        tags: Iterable[str] | None = None,
        source: str | None = None,
    ) -> dict[str, Any] | None:
        """Update supplied fields; passing source=None leaves source unchanged."""
        current = self.get(memory_id)
        if current is None:
            return None
        new_content = current["content"] if content is None else content.strip()
        if not new_content:
            raise ValueError("content must be a non-empty string")
        new_tags = current["tags"] if tags is None else sorted(
            {tag.strip() for tag in tags if tag.strip()}
        )
        new_source = current["source"] if source is None else source
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE memories
                SET content = ?, tags_json = ?, source = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    new_content,
                    json.dumps(new_tags, ensure_ascii=False),
                    new_source,
                    _now(),
                    memory_id,
                ),
            )
        return self.get(memory_id)

    def delete(self, memory_id: str) -> bool:
        """Permanently delete one memory; returns whether a row was removed."""
        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM memories WHERE id = ?", (memory_id,)
            )
        return cursor.rowcount > 0

    def export_json(self) -> str:
        """Export all records as portable UTF-8-compatible JSON text."""
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM memories ORDER BY created_at ASC"
            ).fetchall()
        return json.dumps(
            [self._to_dict(row) for row in rows],
            ensure_ascii=False,
            indent=2,
        )

    @staticmethod
    def _to_dict(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "id": row["id"],
            "content": row["content"],
            "tags": json.loads(row["tags_json"]),
            "source": row["source"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
