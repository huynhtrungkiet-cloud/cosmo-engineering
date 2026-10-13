"""Schema cho đầu ra có cấu trúc của QA/QC Auditor (structured outputs)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class QAFinding(BaseModel):
    severity: Literal["blocker", "major", "minor"]
    target: Literal["design", "cost", "plan"] = Field(description="Agent phải sửa finding này")
    issue: str = Field(description="Vấn đề, trích đúng chỗ: mục, mã chi tiết, con số")
    basis: str = Field(description="Vì sao sai / căn cứ (tiêu chuẩn, công thức, đối chiếu plan/brief)")
    required_fix: str = Field(description="Yêu cầu sửa cụ thể")


class QAVerdict(BaseModel):
    verdict: Literal["PASS", "REVISE"]
    summary: str = Field(description="2–4 câu: tình trạng chung, gửi khách được chưa, rủi ro lớn nhất")
    findings: list[QAFinding]
    verified_ok: list[str] = Field(description="Những điểm đã kiểm tra và đạt")

    def findings_for(self, target: str) -> list[QAFinding]:
        return [f for f in self.findings if f.target == target]

    def to_markdown(self) -> str:
        lines = [f"VERDICT: {self.verdict}", "", "## Tóm tắt", self.summary, "", "## Findings"]
        if self.findings:
            lines.append("| # | Mức độ | Giao cho | Vấn đề | Căn cứ | Yêu cầu sửa |")
            lines.append("|---|---|---|---|---|---|")
            for i, f in enumerate(self.findings, 1):
                row = [str(i), f.severity, f.target, f.issue, f.basis, f.required_fix]
                lines.append("| " + " | ".join(c.replace("|", "\\|").replace("\n", " ") for c in row) + " |")
        else:
            lines.append("(không có)")
        lines += ["", "## Đã kiểm tra & đạt"] + [f"- {v}" for v in self.verified_ok]
        return "\n".join(lines) + "\n"
