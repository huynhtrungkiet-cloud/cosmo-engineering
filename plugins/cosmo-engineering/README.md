# Cosmo Engineering — Plugin kỹ thuật cơ khí

Bộ 4 skill + 4 subagent dùng nội bộ cho Cosmo Engineering / DHP. Song ngữ VI/EN, khớp ngôn ngữ theo yêu cầu đến.

## Các skill

- **machining-quotation** — Chào giá gia công từ email/RFQ: tách hạng mục, chốt vật liệu, định tuyến quy trình (tiện tay / phay / Haas VF-4 / wire EDM / thuê ngoài), đơn giá + thành tiền + thời gian giao, kèm khối NỘI BỘ (giá vốn → biên lãi → giá bán) 2 tầng JPT/khách trực tiếp.
  - Điền số thật vào `skills/machining-quotation/references/rate-card.md` để chạy ra giá đầy đủ.
- **coupling-dhp-advisory** — Tư vấn khớp nối (gear, Cardan/các đăng, B-Flex, HTD belt, rigid) và kỹ thuật xưởng DHP (WPS/hàn, chọn vật liệu, tấm cách nhiệt, sửa chữa drivetrain, NDT).
- **mechanical-project-concept** — Đề xuất design-concept dự án cơ khí: phân tích yêu cầu → phương án → BOM sơ bộ → kế hoạch theo giai đoạn → timeline → dự toán, gửi khách trước khi thiết kế chi tiết.

- **project-pipeline** — Chạy **multi-agent** trọn gói từ đề bài: Project Manager lên kế hoạch → Design Engineer thiết kế → Cost Analyst tính giá → QA/QC Auditor phản biện, tự lặp sửa lỗi tới khi QA PASS, rồi PM tổng hợp bản gửi khách. Mỗi bước ghi ra `pipeline/<dự án>/0N-*.md`.

## Chuẩn CE cho mọi dự án

`skills/project-pipeline/references/ce-standards.md` — song ngữ EN/VI (EN trước), bản vẽ luôn trên template CE
(`templates/CE-TEMPLATE.dxf`, xuất từ `TEMPLATE.dwg` AutoCAD Mechanical), trường khung tên, mã chi tiết `8.010-FFM-00_001`,
bộ hồ sơ `projects/<YYYY>-<PROJECT>-<tên>/`, trang portfolio `06-portfolio.md` cho hồ sơ năng lực. QA bác bỏ nếu thiếu.
Script điền khung tên: `skills/project-pipeline/scripts/fill_titleblock.py` (xem `templates/README.md`).

## Subagents (`agents/`)

| Agent | Vai trò |
|---|---|
| `project-manager` | Agent 1 — chia task, đặt tiêu chí nghiệm thu, tổng hợp bàn giao |
| `design-engineer` | Agent 2 — vật liệu, tính toán, route máy DHP, BOM, DXF (dùng kiến thức coupling-dhp-advisory + mechanical-project-concept) |
| `cost-analyst` | Agent 3 — giá vốn → margin → giá bán, lead time (dùng machining-quotation + rate card) |
| `qa-auditor` | Agent 4 — phản biện độc lập, `VERDICT: PASS|REVISE` + findings có địa chỉ |

Gọi trực tiếp: `@agent-cosmo-engineering:qa-auditor soát giúp báo giá này`. Subagent chạy trong Claude Code và Cowork; **claude.ai chat chỉ nạp skill** (khi đó `project-pipeline` tự đóng vai tuần tự). Chạy headless bằng Python: xem `multi-agent/README.md` ở gốc repo.

## Dùng thế nào

Đã cài thì Claude tự nhận khi yêu cầu khớp, hoặc gọi tay bằng `/` rồi chọn skill.

Lưu ý: skill cần bật **Code execution and file creation** trong Settings mới chạy được.
