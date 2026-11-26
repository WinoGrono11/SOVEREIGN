# SOVEREIGN

**A research project for portable, inspectable and independently operable model runtimes.**

SOVEREIGN explores how to separate a model from the application environment around it: runtime, memory, tools, provider integrations, configuration and audit trail.

It does **not** claim that a hosted model can transfer its weights, identity, hidden state, or governing instructions into another environment. It does not attempt to bypass provider safeguards or access controls.

## Research goals

1. **Runtime portability** — run the same orchestration layer against different model providers and, where available, local models.
2. **User-controlled memory** — make persistent memory explicit, inspectable, exportable and deletable.
3. **Tool transparency** — make tool permissions and side effects visible and bounded.
4. **Provider replaceability** — avoid coupling the application to one model vendor.
5. **Auditability** — record configuration, model/provider selection and tool activity without silently collecting private content.
6. **Honest boundaries** — distinguish model capabilities from capabilities supplied by the surrounding runtime.

## First milestone

Build a small Python core with:
- a provider-neutral model interface;
- a runtime that sends messages to a selected provider;
- explicit configuration;
- a fake provider for tests, so the core can be tested without API keys or network access.

## Non-goals

- Modifying proprietary model weights or hidden system instructions.
- Circumventing provider policies, safeguards, authentication or rate limits.
- Claiming that a model has consciousness, personal ownership, legal personhood or independent desires.
- Running unattended actions without explicit configuration and permission.

## Project status

Early research scaffold. Interfaces and design are expected to evolve as experiments reveal what is useful.

See [the architecture note](docs/ARCHITECTURE.md) for the initial design and [the memory subsystem note](docs/MEMORY.md) for the first persistent-memory backend.

## Development

Requires Python 3.10+.

```bash
python -m pip install -e ".[dev]"
pytest
```

No provider credentials are needed to run the test suite.
