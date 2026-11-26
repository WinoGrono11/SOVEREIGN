"""Small provider-neutral data types."""

from dataclasses import dataclass
from typing import Literal


Role = Literal["system", "user", "assistant"]


@dataclass(frozen=True)
class Message:
    role: Role
    content: str


@dataclass(frozen=True)
class ModelResponse:
    content: str
    provider: str
    model: str
