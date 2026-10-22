# CE Standards — Cosmo Engineering deliverable & drawing conventions / Chuẩn hồ sơ & bản vẽ CE

Applies to EVERY Cosmo Engineering (CE) project handled by the plugin's skills and agents.
Áp dụng cho MỌI dự án CE do skill/agent của plugin xử lý. QA/QC Auditor audits against this file.

## 1. Language / Ngôn ngữ

- Client-facing documents are **bilingual, English first, Vietnamese second** (EN / VI), section by section
  or label by label: `Title / Tiêu đề`. Internal blocks (`--- INTERNAL / NỘI BỘ ---`) may be VI only.
- Tài liệu gửi khách luôn song ngữ, **EN trước, VI sau**. Khối nội bộ được phép chỉ tiếng Việt.
- Drawings: notes, title block, revision table in EN; add VI in parentheses only where a shop operator
  needs it (e.g. heat-treat instruction). Bản vẽ: chú thích tiếng Anh, thêm tiếng Việt trong ngoặc ở chỗ thợ cần.
- Numbers: SI units (mm, kg, N·m, MPa). Decimal point `.` in EN tables; keep one convention per document.

## 2. Drawings / Bản vẽ — always on the CE template

- Template: `templates/CE-TEMPLATE.dxf` in this plugin (exported from the AutoCAD Mechanical 2023
  `TEMPLATE.dwg`, standard **AM_ISO**, units **mm**, title block "Title Blocks COSMO").
  If only the `.dwg` exists, ask the user to export a DXF 2018 once; DWG cannot be read by the toolchain.
- Every drawing produced or specified by the Design Engineer MUST use that template, via
  `scripts/fill_titleblock.py` (fills the title block attributes, inserts geometry on the right layers),
  or, if no code tools are available, the drawing spec MUST list every title-block field below with its value
  so the CAD operator fills the same template.
- Standards: ISO 128 (views), ISO 129-1 (dimensioning), **ISO 2768-mK** general tolerances unless stated,
  ISO 286 fits (write `Ø60 h6`, `Ø80 H7`), ISO 1302 surface roughness (Ra), ISO 2553 weld symbols,
  weld quality per ISO 5817 class stated in "Max. weld class".
- Sheet sizes: A4 / A3 / A2 / A1 from the template layouts; scale from the ISO series (1:1, 1:2, 1:5, 2:1 …).

### 2.1 Title block fields (from the CE template) / Trường trong khung tên

| Field (EN) | Trường (VI) | Rule |
|---|---|---|
| Title | Tên chi tiết / cụm | EN, UPPERCASE, ≤ 40 chars; VI in second line if space |
| Part Number | Mã chi tiết | per §2.2 |
| Project | Dự án | project code + short name, e.g. `FFM – FORMING FLANGE MACHINE` |
| Customer / Vendor | Khách hàng / NCC | client name as on PO |
| Material where not indicated | Vật liệu (mặc định) | grade + standard, e.g. `SCM440 (JIS G4105)`; alternative materials 1–3 if allowed |
| Max. weld class | Cấp mối hàn tối đa | ISO 5817 class (B / C / D) or `N/A` |
| Weight | Khối lượng | kg, 2 decimals, from CAD or calculated |
| Scale | Tỷ lệ | ISO series |
| Format | Khổ giấy | A4/A3/A2/A1 |
| Sheet / Nr. of sheet | Tờ / Tổng số tờ | `1 / 3` |
| Designed by, Date | Thiết kế, ngày | name + `DD/MM/YYYY` |
| Checked by, Date | Kiểm tra, ngày | QA/QC (never the same person as Designed by) |
| Approved by, Date | Duyệt, ngày | Kiet / Eng. Approved / Mfg. Approved |
| Status | Trạng thái | `Concept` → `WorkInProgress` → `ISSUED`. **ISSUED only after QA VERDICT: PASS** |
| Revision table Rev.01–04 | Bảng sửa đổi | Rev, description, date, by — never overwrite, append |
| COSMO shop number | Số lệnh xưởng | from the quotation / PO, blank at concept stage |
| Estimated cost / Cost center | Dự toán / mã chi phí | internal only; blank on client copies |

### 2.2 Part numbering / Mã chi tiết

Pattern seen in the template: `8.010-FFM-00_001`

```
<group>.<seq>-<PROJECT>-<assembly>_<part>
 8.010   -  FFM   -   00    _  001
```

- `group.seq` — CE product/job group and job sequence (keep the company list; ask Kiet when a new group is needed).
- `PROJECT` — 2–4 letter project code, stable across all documents of the project.
- `assembly` — `00` = top assembly / general, `01…` = sub-assemblies.
- `part` — three digits, `000` = assembly drawing, `001…` = parts.
- File name = part number + revision: `8.010-FFM-00_001_R01.dxf` (and `.pdf` for issue).

### 2.3 Drawing content checklist / Checklist nội dung bản vẽ

- [ ] Views sufficient to manufacture (no implied features); section views for bores/keyways.
- [ ] All functional dimensions with tolerance; fits in ISO 286 notation; general tolerance note.
- [ ] Surface finish on bearing seats / seals / sliding faces; default Ra elsewhere.
- [ ] Material + heat treatment + hardness (e.g. `SCM440, Q&T 28–32 HRC`) + coating.
- [ ] Weld symbols (ISO 2553) and weld class; WPS reference for fatigue-critical joints; NDT note.
- [ ] Weight, scale, sheet n/N, status, revision row filled; "Checked by" ≠ "Designed by".
- [ ] For assemblies: BOM table on sheet (Item, Qty, Part Number, Title, Material, Weight, Remark) matching the Design package part table 1:1.

## 3. Project document set / Bộ hồ sơ mỗi dự án

Same structure every time so projects stack into a capability profile (hồ sơ năng lực) and a demo video
can walk through them in the same order.

```
projects/<YYYY>-<PROJECT>-<short-name>/
├── 00-brief.md                     # client request as received (+ source email / RFQ file)
├── 01-plan.md                      # PM plan: scope, assumptions, open questions, acceptance criteria
├── 02-design-rN.md                 # Design package (part table, routing, BOM, calcs, drawing list)
├── 03-cost-rN.md                   # Cost & quotation (client table + INTERNAL block)
├── 04-qa-rN.md                     # QA/QC verdicts, one per revision
├── 05-final.md                     # client deliverable, EN/VI, assembled by PM after QA PASS
├── 06-portfolio.md                 # one-page project summary EN/VI for the capability profile (§4)
├── drawings/                       # <part-number>_R<rev>.dxf / .pdf on the CE template
├── calcs/                          # spreadsheets / scripts behind the numbers
├── inputs/                         # client files: drawings, specs, supplier quotes (read-only)
└── media/                          # renders, photos, video stills, demo script
```

- Revision discipline: a new `rN` file per QA round; never edit a previous revision in place.
- Status words are the same in documents and drawings: `Concept` / `WorkInProgress` / `ISSUED`.
- Nothing is `ISSUED` without a `04-qa-rN.md` with `VERDICT: PASS` for that revision.

## 4. Portfolio one-pager (06-portfolio.md) / Trang tóm tắt năng lực

Bilingual EN / VI, max one page, written by the PM in "Mode 2" together with `05-final.md`:

```
# <PROJECT CODE> — <Project title EN> / <Tên dự án VI>
Client / Khách hàng: ___ (or "confidential")   |   Year / Năm: ___   |   Status: Concept | Delivered

**Challenge / Bài toán** — 2–3 sentences: what the client needed, constraints (load, duty, deadline, standard).
**Solution / Giải pháp** — 3–5 bullets: concept, key materials & processes (DHP machines + outsourced), standards applied.
**Key numbers / Số liệu then chốt** — torque / size / qty / tolerance class / lead time (no prices on client copies).
**Deliverables / Sản phẩm bàn giao** — drawings (count, template CE), calc note, QA report, quotation.
**Result / Kết quả** — what was delivered, acceptance, lessons learned (1 line).
**Media** — list of renders / photos / video clips in `media/`.
```

## 5. Minimum acceptance criteria the PM must always include / AC bắt buộc

The Project Manager appends these to every plan; the QA/QC Auditor fails the review if any is missing:

- AC-STD-1 Client deliverable is bilingual EN/VI, EN first, consistent terminology.
- AC-STD-2 Every drawing (file or spec) is on the CE template with all §2.1 fields filled; status rule respected.
- AC-STD-3 Part numbers follow §2.2 and match 1:1 across Design part table, drawings, BOM, and quotation lines.
- AC-STD-4 Material, tolerance, finish, heat treatment, weld class present for every manufactured part.
- AC-STD-5 Project folder follows §3; final package includes `06-portfolio.md`.
- AC-STD-6 No internal cost/margin content in client-facing files.
