"""Gom hồ sơ dự án (folder) thành văn bản để nạp vào context của các agent.

Hỗ trợ: .md .txt .csv .json .yaml .yml (đọc thẳng), .xlsx/.xlsm (openpyxl, nếu cài), .dxf (ezdxf nếu cài,
hoặc thống kê thô). PDF/ảnh/STEP bị bỏ qua nhưng vẫn được liệt kê tên để agent biết chúng tồn tại.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

TEXT_EXT = {".md", ".txt", ".csv", ".json", ".yaml", ".yml", ".tsv"}
XLSX_EXT = {".xlsx", ".xlsm"}
DXF_EXT = {".dxf"}
LISTED_ONLY_EXT = {".pdf", ".png", ".jpg", ".jpeg", ".step", ".stp", ".iges", ".igs", ".dwg", ".docx", ".sldprt", ".sldasm"}


@dataclass
class ProjectContext:
    text: str
    files_included: list[str]
    files_listed_only: list[str]
    truncated: bool


def _read_xlsx(path: Path, max_rows: int = 200) -> str:
    try:
        import openpyxl  # type: ignore
    except ImportError:
        return "(file Excel – cài `pip install openpyxl` để đọc nội dung)"
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out: list[str] = []
    for ws in wb.worksheets:
        out.append(f"#### Sheet: {ws.title}")
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i >= max_rows:
                out.append(f"... (cắt sau {max_rows} dòng)")
                break
            cells = ["" if v is None else str(v) for v in row]
            if any(cells):
                out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def _read_dxf(path: Path) -> str:
    try:
        import ezdxf  # type: ignore
    except ImportError:
        raw = path.read_text(encoding="utf-8", errors="ignore")
        n_lines = raw.count("\n")
        return f"(DXF {n_lines} dòng – cài `pip install ezdxf` để tóm tắt entity; không nạp nội dung thô)"
    doc = ezdxf.readfile(str(path))
    msp = doc.modelspace()
    counts: dict[str, int] = {}
    for e in msp:
        counts[e.dxftype()] = counts.get(e.dxftype(), 0) + 1
    layers = ", ".join(sorted(l.dxf.name for l in doc.layers))
    ext = doc.header.get("$EXTMIN"), doc.header.get("$EXTMAX")
    texts = [e.dxf.text for e in msp.query("TEXT MTEXT")[:50] if hasattr(e.dxf, "text")]
    return (
        f"Entities: {counts}\nLayers: {layers}\nExtents: {ext}\n"
        + ("Text/annotations: " + " | ".join(texts) if texts else "")
    )


def _read_file(path: Path) -> str | None:
    ext = path.suffix.lower()
    if ext in TEXT_EXT:
        return path.read_text(encoding="utf-8", errors="replace")
    if ext in XLSX_EXT:
        return _read_xlsx(path)
    if ext in DXF_EXT:
        return _read_dxf(path)
    return None


def gather_project_context(project_dir: Path | None, max_total: int, max_per_file: int) -> ProjectContext:
    if project_dir is None:
        return ProjectContext("(không có hồ sơ dự án)", [], [], False)
    project_dir = Path(project_dir)
    if not project_dir.is_dir():
        raise NotADirectoryError(project_dir)

    included: list[str] = []
    listed: list[str] = []
    chunks: list[str] = []
    total = 0
    truncated = False
    for path in sorted(p for p in project_dir.rglob("*") if p.is_file() and not p.name.startswith(".")):
        rel = path.relative_to(project_dir).as_posix()
        content = _read_file(path)
        if content is None:
            listed.append(rel)
            continue
        if len(content) > max_per_file:
            content = content[:max_per_file] + f"\n... (cắt, file dài {len(content)} ký tự)"
        block = f"\n\n--- FILE: {rel} ---\n{content}"
        if total + len(block) > max_total:
            truncated = True
            listed.append(rel + " (không nạp: vượt giới hạn context)")
            continue
        chunks.append(block)
        included.append(rel)
        total += len(block)

    header = f"# HỒ SƠ DỰ ÁN: {project_dir.name}\nFile đã nạp nội dung: {len(included)}. File chỉ liệt kê tên: {len(listed)}."
    if listed:
        header += "\nChỉ liệt kê tên (không đọc được/không nạp): " + ", ".join(listed)
    return ProjectContext(header + "".join(chunks), included, listed, truncated)
