# Memory subsystem: first implementation

## Scope

The first memory backend is local SQLite. It is intentionally simple and does not require embeddings, a hosted service, or provider-specific features.

## Privacy and control

- No memory is created automatically.
- The application must call `MemoryStore.add()` explicitly.
- Records can be inspected with `get()` and `search()`.
- Records can be edited with `update()` or permanently removed with `delete()`.
- The full store can be exported with `export_json()`.
- Prompts, completions, credentials and tool traces are not captured by this module.

## Example

```python
from sovereign.memory import MemoryStore

memory = MemoryStore("./data/sovereign-memory.sqlite3")
record = memory.add(
    "The user prefers concise technical explanations.",
    tags=["preference", "communication"],
    source="explicit-user-approved-note",
)

matches = memory.search("technical")
print(matches)
```

## Current limitations

Search is case-insensitive substring matching, not semantic retrieval. There is no encryption, multi-user access control, import/restore workflow, retention scheduler, or automatic relevance ranking yet. The database file should be protected using normal operating-system permissions, and secrets should not be stored in it.

## Design decision

Memory is an explicit subsystem outside the model provider. Replacing the model does not require replacing the memory store. Conversely, this store does not recreate a model's weights, hidden state, or personal identity.
