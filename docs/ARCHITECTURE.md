# Initial architecture

## Central distinction

A hosted model and the software environment that calls it are different things.

SOVEREIGN can make the surrounding environment portable and inspectable. It cannot thereby acquire or relocate a provider's model weights, internal activations, hidden instructions, private training data, or service-side state.

## Components

```text
User / Client
     |
     v
SOVEREIGN Runtime
     |---- Configuration
     |---- Explicit SQLite MemoryStore (implemented separately; caller-controlled)
     |---- Tool registry (future milestone)
     |---- Audit events (future milestone)
     |
     v
Model Provider interface
     |---- Hosted API adapter (future)
     |---- Local model adapter (future)
     |---- Fake provider (first milestone)
```

## Design principles

### 1. Provider-neutral core
The runtime depends on a small interface, not a vendor-specific SDK. Provider adapters translate between that interface and provider APIs.

### 2. Explicit memory
Memory is a separate subsystem, not an assumed property of the model. The first local SQLite backend supports explicit add, inspect, substring search, update, deletion and JSON export. The runtime does not write memories automatically. Future work includes retention rules, encryption and a documented import/restore path.

### 3. Permissioned tools
Tools should declare their capabilities and side effects. Read-only operations should be distinguishable from actions that write, send, purchase, publish or modify external state.

### 4. Observable operation
The runtime should expose which provider and configuration were used, and which tools ran. Sensitive prompts and outputs must not be logged by default.

### 5. Replaceability without identity claims
Changing the provider changes the model implementation. Conversation history and application state may be portable; the model's weights, hidden state and exact behavior are not thereby transferred.

## First milestone: minimal runtime

- Define a provider protocol.
- Define simple message and response types.
- Implement a runtime that delegates one request to a provider.
- Implement a deterministic fake provider.
- Test the delegation path without network access.

## Questions for later research

- Which memory formats are portable across providers?
- How can tool permissions be represented and audited?
- What is the smallest useful common denominator across hosted and local models?
- How can users migrate their data without implying that model internals migrate with it?
- Which actions should require confirmation, and how should revocation work?


## Current implementation snapshot

- The provider-neutral runtime delegates one explicit generation request to a supplied provider.
- The SQLite memory store is independent of the runtime and writes only when a caller invokes its API.
- The Lexicon Robustness Lab has a benign seed fixture and a deterministic structural validator. Semantic equivalence and content-safety review remain human responsibilities.
- Tool registration, permission enforcement and audit-event integration are still future milestones; their absence should not be inferred as implemented from the architecture diagram.
