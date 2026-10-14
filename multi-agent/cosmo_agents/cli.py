"""CLI: python -m cosmo_agents run --brief brief.md --project-dir ./ho-so --out ./pipeline/du-an-x"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

from .config import PipelineConfig
from .pipeline import run_pipeline
from .prompts import build_system_prompt, list_agents


def _slug(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return s[:40] or "project"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="cosmo-agents", description="Cosmo Engineering multi-agent pipeline")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="Chạy pipeline PM → Design → Cost → QA → tổng hợp")
    r.add_argument("--brief", required=True, help="File brief/RFQ (markdown hoặc text), hoặc '-' để đọc stdin")
    r.add_argument("--project-dir", help="Thư mục hồ sơ dự án (bản vẽ, spec, bảng giá NCC, dự án cũ...)")
    r.add_argument("--out", help="Thư mục đầu ra (mặc định: pipeline/<ngày>-<tên-brief>)")
    r.add_argument("--max-revisions", type=int, default=2)
    r.add_argument("--model", help="Ghi đè model cho mọi agent (mặc định claude-opus-5-5)")
    r.add_argument("--plugin-dir", help="Thư mục plugin cosmo-engineering (mặc định: ../plugins/cosmo-engineering)")
    r.add_argument("--quiet", action="store_true")

    s = sub.add_parser("show-prompt", help="In system prompt đã ghép của một agent (để kiểm tra)")
    s.add_argument("agent", nargs="?", help="project-manager | design-engineer | cost-analyst | qa-auditor")
    s.add_argument("--plugin-dir")

    a = p.parse_args(argv)
    cfg = PipelineConfig()
    if getattr(a, "plugin_dir", None):
        cfg.plugin_dir = Path(a.plugin_dir)

    if a.cmd == "show-prompt":
        if not a.agent:
            print("\n".join(list_agents(cfg)))
            return 0
        print(build_system_prompt(cfg, a.agent))
        return 0

    brief = sys.stdin.read() if a.brief == "-" else Path(a.brief).read_text(encoding="utf-8")
    if not brief.strip():
        print("Brief rỗng.", file=sys.stderr)
        return 2
    cfg.max_revisions = a.max_revisions
    cfg.with_model(a.model)
    out = Path(a.out) if a.out else Path("pipeline") / f"{date.today():%Y%m%d}-{_slug(Path(a.brief).stem if a.brief != '-' else brief[:30])}"
    log = (lambda s: None) if a.quiet else (lambda s: print(s, file=sys.stderr, flush=True))

    res = run_pipeline(brief, Path(a.project_dir) if a.project_dir else None, out, cfg=cfg, log=log)

    u = res.usage
    print(f"\nKẾT QUẢ: QA {res.verdict.verdict} sau {res.revisions} vòng sửa → {res.final_path}")
    print(f"Token: in={u.input_tokens:,} (cache đọc {u.cache_read_input_tokens:,}) out={u.output_tokens:,} | {u.calls} lượt gọi")
    if not res.passed:
        print("CẢNH BÁO: QA chưa PASS. Xem finding còn mở trong 04-qa-r*.md và khối NỘI BỘ của 05-final.md.")
    return 0 if res.passed else 1
