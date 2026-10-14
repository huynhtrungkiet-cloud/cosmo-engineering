"""Lớp mỏng bọc Claude API cho pipeline.

- Streaming cho mọi lượt văn bản dài (tránh timeout HTTP).
- Structured outputs (Pydantic) cho phán quyết QA, để orchestrator đọc được PASS/REVISE không cần parse text.
- Prompt caching: system prompt của mỗi agent + hồ sơ dự án là phần ổn định -> đặt cache_control.
- fallbacks="default": nếu bộ lọc an toàn từ chối, API tự chạy lại trên model dự phòng (beta server-side-fallback).
- Thinking: adaptive (mặc định trên các model hiện tại); độ sâu chỉnh bằng output_config.effort.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, TypeVar

from pydantic import BaseModel

from .config import AgentSettings

T = TypeVar("T", bound=BaseModel)

FALLBACK_BETA = "server-side-fallback-2026-07-01"


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_input_tokens: int = 0
    cache_creation_input_tokens: int = 0
    calls: int = 0

    def add(self, usage) -> None:  # usage: anthropic Usage object
        self.calls += 1
        self.input_tokens += getattr(usage, "input_tokens", 0) or 0
        self.output_tokens += getattr(usage, "output_tokens", 0) or 0
        self.cache_read_input_tokens += getattr(usage, "cache_read_input_tokens", 0) or 0
        self.cache_creation_input_tokens += getattr(usage, "cache_creation_input_tokens", 0) or 0


class LLM(Protocol):
    """Giao diện để test có thể thay bằng bản giả (FakeLLM) không gọi mạng."""

    usage: Usage

    def complete(self, *, agent: str, system: str, user: str, settings: AgentSettings) -> str: ...

    def complete_structured(
        self, *, agent: str, system: str, user: str, settings: AgentSettings, schema: type[T]
    ) -> T: ...


class RefusedError(RuntimeError):
    """API trả stop_reason=refusal (cả model dự phòng cũng từ chối)."""


@dataclass
class ClaudeLLM:
    client: object = None  # anthropic.Anthropic; tạo lười để import không cần key
    usage: Usage = field(default_factory=Usage)
    log: object = None  # callable(str) hoặc None

    def _client(self):
        if self.client is None:
            import anthropic

            self.client = anthropic.Anthropic()  # đọc ANTHROPIC_API_KEY / profile `ant auth login`
        return self.client

    @staticmethod
    def _system_blocks(system: str) -> list[dict]:
        # Khối ổn định -> cache. Nội dung thay đổi theo lượt nằm ở messages, sau breakpoint này.
        return [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]

    def _check_refusal(self, message, agent: str) -> None:
        if message.stop_reason == "refusal":
            details = getattr(message, "stop_details", None)
            raise RefusedError(f"[{agent}] bị từ chối: {getattr(details, 'category', None)} – {getattr(details, 'explanation', '')}")
        if message.stop_reason == "max_tokens":
            self._say(f"[{agent}] CẢNH BÁO: chạm max_tokens, đầu ra có thể bị cắt – tăng max_tokens trong config.")

    def _say(self, text: str) -> None:
        if self.log:
            self.log(text)

    def complete(self, *, agent: str, system: str, user: str, settings: AgentSettings) -> str:
        client = self._client()
        with client.beta.messages.stream(
            model=settings.model,
            max_tokens=settings.max_tokens,
            system=self._system_blocks(system),
            messages=[{"role": "user", "content": user}],
            output_config={"effort": settings.effort},
            betas=[FALLBACK_BETA],
            fallbacks="default",
        ) as stream:
            message = stream.get_final_message()
        self.usage.add(message.usage)
        self._check_refusal(message, agent)
        return "".join(b.text for b in message.content if b.type == "text")

    def complete_structured(
        self, *, agent: str, system: str, user: str, settings: AgentSettings, schema: type[T]
    ) -> T:
        client = self._client()
        message = client.beta.messages.parse(
            model=settings.model,
            max_tokens=settings.max_tokens,
            system=self._system_blocks(system),
            messages=[{"role": "user", "content": user}],
            output_config={"effort": settings.effort},
            output_format=schema,
            betas=[FALLBACK_BETA],
            fallbacks="default",
        )
        self.usage.add(message.usage)
        self._check_refusal(message, agent)
        parsed = message.parsed_output
        if parsed is None:
            raise RuntimeError(f"[{agent}] không parse được structured output")
        return parsed
