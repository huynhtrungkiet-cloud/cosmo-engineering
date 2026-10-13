"""Cấu hình pipeline. Mọi giá trị có thể ghi đè bằng biến môi trường hoặc tham số CLI."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

# Thư mục plugin chứa agents/ và skills/ (nguồn duy nhất của prompt vai trò).
_DEFAULT_PLUGIN_DIR = Path(__file__).resolve().parents[2] / "plugins" / "cosmo-engineering"

# Mỗi vai có thể chạy model/effort khác nhau. QA chạy effort cao vì phản biện là nơi cần suy nghĩ kỹ nhất.
DEFAULT_MODEL = "claude-opus-5-5"


@dataclass
class AgentSettings:
    model: str = DEFAULT_MODEL
    effort: str = "high"  # low | medium | high | xhigh | max
    max_tokens: int = 32000


@dataclass
class PipelineConfig:
    plugin_dir: Path = field(default_factory=lambda: Path(os.environ.get("COSMO_PLUGIN_DIR", _DEFAULT_PLUGIN_DIR)))
    max_revisions: int = 2
    # Giới hạn ký tự đưa vào context từ hồ sơ dự án (tránh phình prompt khi folder có hàng trăm file).
    max_context_chars: int = 400_000
    max_chars_per_file: int = 60_000
    agents: dict[str, AgentSettings] = field(
        default_factory=lambda: {
            "project-manager": AgentSettings(effort="medium"),
            "design-engineer": AgentSettings(effort="high"),
            "cost-analyst": AgentSettings(effort="high"),
            "qa-auditor": AgentSettings(effort="xhigh", max_tokens=16000),
        }
    )

    def with_model(self, model: str | None) -> "PipelineConfig":
        if model:
            for s in self.agents.values():
                s.model = model
        return self

    @property
    def rate_card_path(self) -> Path:
        return self.plugin_dir / "skills" / "machining-quotation" / "references" / "rate-card.md"

    @property
    def agents_dir(self) -> Path:
        return self.plugin_dir / "agents"

    @property
    def skills_dir(self) -> Path:
        return self.plugin_dir / "skills"
