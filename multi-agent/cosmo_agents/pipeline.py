"""Orchestrator: PM -> Design -> Cost -> QA -> (vòng sửa) -> PM tổng hợp.

Mỗi giai đoạn ghi ra file trong thư mục đầu ra, giống skill `project-pipeline`:
  00-brief.md, 01-plan.md, 02-design-rN.md, 03-cost-rN.md, 04-qa-rN.md, 05-final.md, run.json
Logic vòng sửa là code thường (không để model quyết "đã đủ tốt chưa"): QA phải trả PASS, hoặc hết lượt.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .config import PipelineConfig
from .context import ProjectContext, gather_project_context
from .llm import LLM, Usage
from .prompts import build_system_prompt
from .schemas import QAVerdict

Logger = Callable[[str], None]
PORTFOLIO_MARKER = "<<<PORTFOLIO>>>"


@dataclass
class PipelineResult:
    out_dir: Path
    verdict: QAVerdict
    revisions: int
    passed: bool
    final_path: Path
    usage: Usage
    history: list[dict] = field(default_factory=list)


def _fmt_findings(verdict: QAVerdict, target: str) -> str:
    items = verdict.findings_for(target)
    if not items:
        return "(không có finding riêng cho bạn ở vòng này)"
    return "\n".join(
        f"- [{f.severity}] {f.issue}\n  Căn cứ: {f.basis}\n  Yêu cầu sửa: {f.required_fix}" for f in items
    )


class Pipeline:
    def __init__(self, llm: LLM, cfg: PipelineConfig, log: Logger | None = None):
        self.llm = llm
        self.cfg = cfg
        self.log = log or (lambda s: None)
        self._systems: dict[str, str] = {}

    # ---------- helpers ----------
    def _system(self, agent: str) -> str:
        if agent not in self._systems:
            self._systems[agent] = build_system_prompt(self.cfg, agent)
        return self._systems[agent]

    def _call(self, agent: str, user: str) -> str:
        t0 = time.time()
        self.log(f"▶ {agent} ...")
        out = self.llm.complete(agent=agent, system=self._system(agent), user=user, settings=self.cfg.agents[agent])
        self.log(f"✔ {agent} ({time.time() - t0:.0f}s, {len(out)} ký tự)")
        return out

    def _call_qa(self, user: str) -> QAVerdict:
        t0 = time.time()
        self.log("▶ qa-auditor ...")
        verdict = self.llm.complete_structured(
            agent="qa-auditor",
            system=self._system("qa-auditor"),
            user=user,
            settings=self.cfg.agents["qa-auditor"],
            schema=QAVerdict,
        )
        self.log(f"✔ qa-auditor → {verdict.verdict} ({len(verdict.findings)} findings, {time.time() - t0:.0f}s)")
        return verdict

    @staticmethod
    def _write(path: Path, text: str) -> Path:
        path.write_text(text, encoding="utf-8")
        return path

    @staticmethod
    def _shared_context(brief: str, ctx: ProjectContext, rate_card: str | None = None) -> str:
        parts = [f"# BRIEF CỦA KHÁCH / ĐỀ BÀI\n\n{brief}", ctx.text]
        if rate_card is not None:
            parts.append(f"# RATE CARD NỘI BỘ (skills/machining-quotation/references/rate-card.md)\n\n{rate_card}")
        return "\n\n".join(parts)

    # ---------- stages ----------
    def run(self, brief: str, project_dir: Path | None, out_dir: Path) -> PipelineResult:
        cfg = self.cfg
        out_dir.mkdir(parents=True, exist_ok=True)
        ctx = gather_project_context(project_dir, cfg.max_context_chars, cfg.max_chars_per_file)
        if ctx.truncated:
            self.log(f"⚠ Hồ sơ vượt giới hạn context; {len(ctx.files_listed_only)} file chỉ liệt kê tên.")
        rate_card = cfg.rate_card_path.read_text(encoding="utf-8") if cfg.rate_card_path.exists() else "(không tìm thấy rate card)"
        shared = self._shared_context(brief, ctx)
        shared_cost = self._shared_context(brief, ctx, rate_card)
        history: list[dict] = []

        self._write(out_dir / "00-brief.md", brief)

        # 1. PM lập kế hoạch
        plan = self._call(
            "project-manager",
            f"{shared}\n\n# YÊU CẦU\nChế độ 1 — LẬP KẾ HOẠCH. Viết kế hoạch theo đúng cấu trúc trong hướng dẫn của bạn.",
        )
        self._write(out_dir / "01-plan.md", plan)

        # 2–3. Design, Cost (vòng 0)
        rev = 0
        design = self._call(
            "design-engineer",
            f"{shared}\n\n# KẾ HOẠCH CỦA PM\n\n{plan}\n\n# YÊU CẦU\nThực hiện các task D* theo kế hoạch. Rev 0.",
        )
        self._write(out_dir / f"02-design-r{rev}.md", design)
        cost = self._call(
            "cost-analyst",
            f"{shared_cost}\n\n# KẾ HOẠCH CỦA PM\n\n{plan}\n\n# THIẾT KẾ (Design Engineer, Rev {rev})\n\n{design}\n\n"
            "# YÊU CẦU\nThực hiện các task C* theo kế hoạch. Rev 0.",
        )
        self._write(out_dir / f"03-cost-r{rev}.md", cost)

        # 4–5. QA + vòng sửa
        verdict = self._audit(out_dir, shared, plan, design, cost, rev, previous=None)
        history.append({"rev": rev, "verdict": verdict.verdict, "findings": len(verdict.findings)})

        while verdict.verdict == "REVISE" and rev < cfg.max_revisions:
            rev += 1
            self.log(f"↻ Vòng sửa {rev}/{cfg.max_revisions}")
            plan_findings = verdict.findings_for("plan")
            if plan_findings:
                plan = self._call(
                    "project-manager",
                    f"{shared}\n\n# KẾ HOẠCH TRƯỚC\n\n{plan}\n\n# FINDING CỦA QA GIAO CHO PLAN\n{_fmt_findings(verdict, 'plan')}\n\n"
                    "# YÊU CẦU\nChế độ 1 — cập nhật kế hoạch, xử lý từng finding (Đã sửa / Không đồng ý vì).",
                )
                self._write(out_dir / f"01-plan-r{rev}.md", plan)

            design_changed = False
            if verdict.findings_for("design") or plan_findings:
                design = self._call(
                    "design-engineer",
                    f"{shared}\n\n# KẾ HOẠCH CỦA PM\n\n{plan}\n\n# BẢN THIẾT KẾ TRƯỚC (Rev {rev - 1})\n\n{design}\n\n"
                    f"# FINDING CỦA QA GIAO CHO DESIGN\n{_fmt_findings(verdict, 'design')}\n\n"
                    f"# YÊU CẦU\nXuất bản Rev {rev} đầy đủ (không chỉ phần sửa). Xử lý từng finding ở mục 9: Đã sửa / Không đồng ý vì.",
                )
                self._write(out_dir / f"02-design-r{rev}.md", design)
                design_changed = True

            # Cost chạy lại nếu có finding riêng, hoặc thiết kế đổi (giờ máy/BOM có thể đổi theo).
            if verdict.findings_for("cost") or design_changed:
                cost = self._call(
                    "cost-analyst",
                    f"{shared_cost}\n\n# KẾ HOẠCH CỦA PM\n\n{plan}\n\n# THIẾT KẾ (Design Engineer, Rev {rev})\n\n{design}\n\n"
                    f"# BẢN DỰ TOÁN TRƯỚC (Rev {rev - 1})\n\n{cost}\n\n# FINDING CỦA QA GIAO CHO COST\n{_fmt_findings(verdict, 'cost')}\n\n"
                    f"# YÊU CẦU\nXuất bản Rev {rev} đầy đủ. Thiết kế {'ĐÃ thay đổi – cập nhật mọi số phụ thuộc' if design_changed else 'không đổi'}. "
                    "Xử lý từng finding ở mục 8: Đã sửa / Không đồng ý vì.",
                )
                self._write(out_dir / f"03-cost-r{rev}.md", cost)

            verdict = self._audit(out_dir, shared, plan, design, cost, rev, previous=verdict)
            history.append({"rev": rev, "verdict": verdict.verdict, "findings": len(verdict.findings)})

        passed = verdict.verdict == "PASS"
        if not passed:
            self.log(f"⚠ Hết {cfg.max_revisions} vòng sửa mà QA vẫn REVISE – bản giao sẽ ghi rõ finding còn mở.")

        # 6. PM tổng hợp
        final = self._call(
            "project-manager",
            f"{shared}\n\n# KẾ HOẠCH\n\n{plan}\n\n# THIẾT KẾ ĐÃ DUYỆT (Rev {rev})\n\n{design}\n\n# DỰ TOÁN ĐÃ DUYỆT (Rev {rev})\n\n{cost}\n\n"
            f"# KẾT LUẬN QA (Rev {rev})\n\n{verdict.to_markdown()}\n\n"
            "# YÊU CẦU\nChế độ 2 — TỔNG HỢP BÀN GIAO (EN/VI, EN trước). Sau tài liệu gửi khách, viết trang portfolio mở đầu bằng dòng `<<<PORTFOLIO>>>`. "
            + ("" if passed else "QA chưa PASS: liệt kê rõ các finding còn mở ở đầu khối NỘI BỘ và đánh dấu tài liệu là DỰ THẢO."),
        )
        # PM mode 2 appends the portfolio one-pager after a marker line (ce-standards §4).
        final_doc, sep, portfolio = final.partition(PORTFOLIO_MARKER)
        final_path = self._write(out_dir / "05-final.md", final_doc.rstrip() + "\n")
        if sep:
            self._write(out_dir / "06-portfolio.md", portfolio.lstrip())
        else:
            self.log("⚠ PM không trả về khối <<<PORTFOLIO>>>; không có 06-portfolio.md.")

        result = PipelineResult(out_dir, verdict, rev, passed, final_path, self.llm.usage, history)
        self._write(
            out_dir / "run.json",
            json.dumps(
                {
                    "passed": passed,
                    "revisions": rev,
                    "history": history,
                    "files_included": ctx.files_included,
                    "files_listed_only": ctx.files_listed_only,
                    "usage": self.llm.usage.__dict__,
                    "models": {k: v.__dict__ for k, v in cfg.agents.items()},
                },
                ensure_ascii=False,
                indent=2,
            ),
        )
        return result

    def _audit(self, out_dir: Path, shared: str, plan: str, design: str, cost: str, rev: int, previous: QAVerdict | None) -> QAVerdict:
        prev_block = ""
        if previous is not None:
            prev_block = f"\n\n# KẾT LUẬN QA VÒNG TRƯỚC (để kiểm tra đã xử lý thật chưa)\n\n{previous.to_markdown()}"
        verdict = self._call_qa(
            f"{shared}\n\n# KẾ HOẠCH CỦA PM\n\n{plan}\n\n# THIẾT KẾ (Rev {rev})\n\n{design}\n\n# DỰ TOÁN (Rev {rev})\n\n{cost}{prev_block}\n\n"
            "# YÊU CẦU\nSoát xét theo checklist. Trả về đúng schema: verdict, summary, findings[], verified_ok[]."
        )
        self._write(out_dir / f"04-qa-r{rev}.md", verdict.to_markdown())
        return verdict


def run_pipeline(
    brief: str,
    project_dir: Path | None,
    out_dir: Path,
    cfg: PipelineConfig | None = None,
    llm: LLM | None = None,
    log: Logger | None = None,
) -> PipelineResult:
    cfg = cfg or PipelineConfig()
    if llm is None:
        from .llm import ClaudeLLM

        llm = ClaudeLLM(log=log)
    return Pipeline(llm, cfg, log).run(brief, project_dir, out_dir)
