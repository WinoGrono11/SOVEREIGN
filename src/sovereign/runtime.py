"""Minimal orchestration runtime."""

from typing import Sequence

from sovereign.providers.base import ModelProvider
from sovereign.types import Message, ModelResponse


class Runtime:
    """Delegates model generation to an explicitly supplied provider.

    The runtime does not imply autonomous operation. A caller invokes
    generate() and remains responsible for credentials, permissions,
    scheduling and any external side effects.
    """

    def __init__(self, provider: ModelProvider, *, model: str) -> None:
        if not model.strip():
            raise ValueError("model must be a non-empty string")
        self._provider = provider
        self._model = model

    def generate(self, messages: Sequence[Message]) -> ModelResponse:
        if not messages:
            raise ValueError("messages must not be empty")
        return self._provider.generate(messages, model=self._model)
