"""Test logic orchestrator với LLM giả (không gọi mạng, không cần API key).

Chạy:  python -m unittest discover -s multi-agent/tests   (từ gốc repo)
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from cosmo_agents.config import PipelineConfig  # noqa: E402
from cosmo_agents.llm import Usage  # noqa: E402
from cosmo_agents.pipeline import Pipeline  # noqa: E402
from cosmo_agents.prompts import build_system_prompt, strip_frontmatter  # noqa: E402
from cosmo_agents.schemas import QAFinding, QAVerdict  # noqa: E402


class FakeLLM:
    """QA trả REVISE (1 finding design + 1 cost) ở vòng 0, PASS từ vòng 1."""

    def __init__(self, revise_rounds: int = 1):
        self.usage = Usage()
        self.calls: list[tuple[str, str]] = []
        self.qa_calls = 0
        self.revise_rounds = revise_rounds

    def complete(self, *, agent, system, user, settings):
        self.calls.append((agent, user))
        assert "Cosmo Engineering" in system, "system prompt phải nạp từ agents/*.md"
        return f"<{agent} output #{len(self.calls)}>"

    def complete_structured(self, *, agent, system, user, settings, schema):
        self.calls.append((agent, user))
        self.qa_calls += 1
        if self.qa_calls <= self.revise_rounds:
            return QAVerdict(
                verdict="REVISE",
                summary="Còn lỗi.",
                findings=[
                    QAFinding(severity="blocker", target="design", issue="Thiếu giờ máy P-01", basis="AC2", required_fix="Bổ sung"),
                    QAFinding(severity="major", target="cost", issue="Margin sai tầng", basis="rate card §5", required_fix="Dùng tầng direct"),
                ],
                verified_ok=["Vật liệu đúng"],
            )
        return QAVerdict(verdict="PASS", summary="Đạt.", findings=[], verified_ok=["Tất cả AC"])


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.cfg = PipelineConfig(max_revisions=2)
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name) / "out"
        self.proj = Path(self.tmp.name) / "proj"
        self.proj.mkdir()
        (self.proj / "gia-ncc.csv").write_text("item,price\nSCM440,45000\n", encoding="utf-8")
        (self.proj / "ban-ve.pdf").write_bytes(b"%PDF-1.4 fake")

    def tearDown(self):
        self.tmp.cleanup()

    def test_prompts_load_from_plugin(self):
        for agent in ("project-manager", "design-engineer", "cost-analyst", "qa-auditor"):
            sp = build_system_prompt(self.cfg, agent)
            self.assertNotIn("\n---\nname:", sp[:10])
            self.assertFalse(sp.startswith("---"), "frontmatter phải bị bỏ")
            self.assertIn("Cosmo Engineering", sp)
        self.assertIn("Rate Card", build_system_prompt(self.cfg, "cost-analyst"))  # skill knowledge attached
        self.assertEqual(strip_frontmatter("---\nname: x\n---\nbody"), "body")

    def test_revise_then_pass(self):
        llm = FakeLLM(revise_rounds=1)
        res = Pipeline(llm, self.cfg).run("Gia công 10 trục SCM440", self.proj, self.out)
        self.assertTrue(res.passed)
        self.assertEqual(res.revisions, 1)
        agents = [a for a, _ in llm.calls]
        self.assertEqual(
            agents,
            ["project-manager", "design-engineer", "cost-analyst", "qa-auditor",
             "design-engineer", "cost-analyst", "qa-auditor", "project-manager"],
        )
        # Finding được gửi đúng người: design nhận finding design, không nhận finding cost
        design_r1 = llm.calls[4][1]
        self.assertIn("Thiếu giờ máy P-01", design_r1)
        self.assertNotIn("Margin sai tầng", design_r1)
        cost_r1 = llm.calls[5][1]
        self.assertIn("Margin sai tầng", cost_r1)
        self.assertIn("ĐÃ thay đổi", cost_r1)
        # Cost nhận rate card, hồ sơ CSV được nạp, PDF chỉ liệt kê tên
        self.assertIn("Rate Card", llm.calls[2][1])
        self.assertIn("SCM440,45000", llm.calls[2][1])
        self.assertIn("ban-ve.pdf", llm.calls[2][1])
        # QA vòng 1 thấy kết luận vòng trước
        self.assertIn("KẾT LUẬN QA VÒNG TRƯỚC", llm.calls[6][1])
        # Files
        names = sorted(p.name for p in self.out.iterdir())
        self.assertEqual(
            names,
            ["00-brief.md", "01-plan.md", "02-design-r0.md", "02-design-r1.md", "03-cost-r0.md",
             "03-cost-r1.md", "04-qa-r0.md", "04-qa-r1.md", "05-final.md", "run.json"],
        )
        run = json.loads((self.out / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(run["history"], [{"rev": 0, "verdict": "REVISE", "findings": 2}, {"rev": 1, "verdict": "PASS", "findings": 0}])
        self.assertTrue((self.out / "04-qa-r0.md").read_text(encoding="utf-8").startswith("VERDICT: REVISE"))

    def test_gives_up_after_max_revisions(self):
        llm = FakeLLM(revise_rounds=99)
        res = Pipeline(llm, self.cfg).run("brief", None, self.out)
        self.assertFalse(res.passed)
        self.assertEqual(res.revisions, 2)
        self.assertEqual(llm.qa_calls, 3)
        self.assertIn("DỰ THẢO", llm.calls[-1][1])  # PM được báo QA chưa PASS

    def test_pass_first_time_skips_loop(self):
        llm = FakeLLM(revise_rounds=0)
        res = Pipeline(llm, self.cfg).run("brief", None, self.out)
        self.assertTrue(res.passed)
        self.assertEqual([a for a, _ in llm.calls], ["project-manager", "design-engineer", "cost-analyst", "qa-auditor", "project-manager"])


if __name__ == "__main__":
    unittest.main()
