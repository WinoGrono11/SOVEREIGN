from typing import Sequence

import pytest

from sovereign.runtime import Runtime
from sovereign.types import Message, ModelResponse


class FakeProvider:
    name = "fake"

    def __init__(self) -> None:
        self.received = None

    def generate(
        self,
        messages: Sequence[Message],
        *,
        model: str,
    ) -> ModelResponse:
        self.received = (list(messages), model)
        return ModelResponse(
            content="deterministic test response",
            provider=self.name,
            model=model,
        )


def test_runtime_delegates_to_provider() -> None:
    provider = FakeProvider()
    runtime = Runtime(provider, model="test-model")
    messages = [Message(role="user", content="Hello")]

    result = runtime.generate(messages)

    assert result.content == "deterministic test response"
    assert result.provider == "fake"
    assert result.model == "test-model"
    assert provider.received == (messages, "test-model")


def test_runtime_rejects_empty_conversation() -> None:
    runtime = Runtime(FakeProvider(), model="test-model")

    with pytest.raises(ValueError, match="messages must not be empty"):
        runtime.generate([])


def test_runtime_rejects_empty_model_name() -> None:
    with pytest.raises(ValueError, match="model must be a non-empty string"):
        Runtime(FakeProvider(), model=" ")
