"""Provider contract used by the SOVEREIGN runtime."""

from typing import Protocol, Sequence

from sovereign.types import Message, ModelResponse


class ModelProvider(Protocol):
    """Minimal interface implemented by hosted or local model adapters."""

    @property
    def name(self) -> str:
        """Stable provider identifier."""

    def generate(
        self,
        messages: Sequence[Message],
        *,
        model: str,
    ) -> ModelResponse:
        """Generate one response for the supplied conversation."""
