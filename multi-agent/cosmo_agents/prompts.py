"""Nạp system prompt của từng agent từ plugins/cosmo-engineering/agents/*.md.

Agent .md dùng chung cho Claude Code (subagent) và cho bộ chạy Python này, nên chỉ cần sửa một chỗ.
Phần frontmatter YAML (name/description/tools) bị bỏ; phần thân là system prompt.
Ngoài ra, mỗi agent được kèm thêm kiến thức nền từ skill tương ứng để có đúng "bộ não" như khi chạy trong Claude.
"""

from __future__ import annotations

import re
from pathlib import Path

from .config import PipelineConfig

# Skill nào được nạp kèm cho agent nào (SKILL.md + references/*.md).
SKILLS_FOR_AGENT: dict[str, list[str]] = {
    "project-manager": ["mechanical-project-concept", "machining-quotation"],
    "design-engineer": ["coupling-dhp-advisory", "mechanical-project-concept"],
    "cost-analyst": ["machining-quotation"],
    "qa-auditor": ["machining-quotation", "coupling-dhp-advisory"],
}

_FRONTMATTER = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)


def strip_frontmatter(text: str) -> str:
    return _FRONTMATTER.sub("", text, count=1).lstrip()


def load_agent_body(cfg: PipelineConfig, agent: str) -> str:
    path = cfg.agents_dir / f"{agent}.md"
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy agent prompt: {path} (đặt COSMO_PLUGIN_DIR nếu plugin ở nơi khác)")
    return strip_frontmatter(path.read_text(encoding="utf-8"))


def load_skill_knowledge(cfg: PipelineConfig, skill: str) -> str:
    skill_dir = cfg.skills_dir / skill
    parts: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        parts.append(f"### Skill: {skill}\n\n{strip_frontmatter(skill_md.read_text(encoding='utf-8'))}")
    refs = skill_dir / "references"
    if refs.is_dir():
        for ref in sorted(refs.glob("*.md")):
            parts.append(f"### {skill}/references/{ref.name}\n\n{ref.read_text(encoding='utf-8')}")
    return "\n\n".join(parts)


# Chuẩn CE (song ngữ, template bản vẽ, mã chi tiết, bộ hồ sơ) được nạp cho MỌI agent.
CE_STANDARDS = Path("project-pipeline") / "references" / "ce-standards.md"


def load_ce_standards(cfg: PipelineConfig) -> str:
    path = cfg.skills_dir / CE_STANDARDS
    if not path.exists():
        return ""
    return f"### skills/{CE_STANDARDS.as_posix()}\n\n{path.read_text(encoding='utf-8')}"


def build_system_prompt(cfg: PipelineConfig, agent: str) -> str:
    """System prompt = thân agent .md + chuẩn CE + kiến thức skill đi kèm. Ổn định giữa các lần gọi -> cache được."""
    body = load_agent_body(cfg, agent)
    knowledge = [load_ce_standards(cfg)] + [load_skill_knowledge(cfg, s) for s in SKILLS_FOR_AGENT.get(agent, [])]
    knowledge = [k for k in knowledge if k]
    if not knowledge:
        return body
    return (
        f"{body}\n\n"
        "---\n\n"
        "# Kiến thức nền từ plugin (áp dụng như skill đã nạp; đường dẫn file trong đây là tương đối trong plugin)\n\n"
        + "\n\n".join(knowledge)
    )


def list_agents(cfg: PipelineConfig) -> list[str]:
    return sorted(p.stem for p in cfg.agents_dir.glob("*.md"))
