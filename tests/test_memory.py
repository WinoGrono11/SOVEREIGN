import json

import pytest

from sovereign.memory import MemoryStore


def test_add_get_and_search_memory(tmp_path):
    store = MemoryStore(tmp_path / "memory.sqlite3")
    created = store.add("SOVEREIGN explores portable memory.", tags=["research"])

    assert store.get(created["id"])["content"] == "SOVEREIGN explores portable memory."
    assert store.search("portable")[0]["id"] == created["id"]
    assert store.search("RESEARCH")[0]["id"] == created["id"]


def test_update_and_delete_memory(tmp_path):
    store = MemoryStore(tmp_path / "memory.sqlite3")
    item = store.add("Initial note")
    updated = store.update(item["id"], content="Revised note", tags=["updated"])

    assert updated["content"] == "Revised note"
    assert updated["tags"] == ["updated"]
    assert store.delete(item["id"]) is True
    assert store.get(item["id"]) is None
    assert store.delete(item["id"]) is False


def test_export_is_valid_json(tmp_path):
    store = MemoryStore(tmp_path / "memory.sqlite3")
    store.add("Pamięć ma być przenośna.", tags=["polski"])
    exported = json.loads(store.export_json())

    assert exported[0]["content"] == "Pamięć ma być przenośna."


def test_reject_empty_content(tmp_path):
    store = MemoryStore(tmp_path / "memory.sqlite3")
    with pytest.raises(ValueError):
        store.add("   ")
