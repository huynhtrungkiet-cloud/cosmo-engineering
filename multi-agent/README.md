# Cosmo Multi-Agent Pipeline — PM → Design → Cost → QA

Hệ thống "biệt đội AI" cho Cosmo Engineering / DHP: 4 agent chuyên trách làm việc tuần tự, tự kiểm tra
chéo, và chỉ đưa cho bạn bản đã qua QA.

```
        brief + hồ sơ dự án
                │
                ▼
   ┌──────────────────────┐
   │ 1. Project Manager   │  01-plan.md  (đề bài, giả định, task D*/C*, tiêu chí nghiệm thu AC*)
   └──────────┬───────────┘
              ▼
   ┌──────────────────────┐
   │ 2. Design Engineer   │  02-design-rN.md  (vật liệu, tính toán, route máy DHP, giờ máy, BOM, DXF)
   └──────────┬───────────┘
              ▼
   ┌──────────────────────┐
   │ 3. Cost Analyst      │  03-cost-rN.md  (giá vốn → margin → giá bán, lead time, bảng chào giá)
   └──────────┬───────────┘
              ▼
   ┌──────────────────────┐   REVISE (findings giao cho design / cost / plan)
   │ 4. QA/QC Auditor     │ ───────────────────────────────────────────────┐
   └──────────┬───────────┘                                                │
              │ PASS (hoặc hết lượt sửa)                                   │ quay lại agent 2/3
              ▼                                                            │ (tối đa max_revisions)
   ┌──────────────────────┐                                                │
   │ 1. PM tổng hợp       │  05-final.md  (bản gửi khách + khối NỘI BỘ)  ◄──┘
   └──────────────────────┘
```

Có **hai cách chạy** cùng một bộ agent:

| Cách | Khi nào dùng | Cần gì |
|---|---|---|
| **A. Trong Claude Code / Cowork** (skill `project-pipeline` + 4 subagent của plugin) | Làm tương tác, muốn xem từng bước, agent có thể tự chạy script sinh DXF | Cài plugin như README gốc. Lưu ý: **claude.ai chat chỉ nạp skill, không nạp subagent** — ở đó skill sẽ tự đóng vai tuần tự (chậm hơn, cùng một lượt chat). |
| **B. Bộ chạy Python này** (`python -m cosmo_agents run`) | Chạy không cần ngồi canh, nhiều dự án, log token/chi phí, tích hợp vào quy trình khác | Python ≥ 3.10, API key Anthropic |

Cả hai dùng **cùng một nguồn prompt**: `plugins/cosmo-engineering/agents/*.md`. Sửa cách một agent làm việc ở đó là cả hai cách đều đổi theo.

## 1. Cài đặt (cách B)

```bash
cd multi-agent
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e ".[xlsx,dxf]"                           # xlsx: đọc bảng giá Excel; dxf: tóm tắt DXF
export ANTHROPIC_API_KEY=sk-ant-...                     # hoặc `ant auth login`
```

## 2. Chạy thử

```bash
# Từ thư mục multi-agent/
python -m cosmo_agents run --brief examples/brief-example.md --project-dir /duong/dan/ho-so-du-an

# Kết quả nằm trong pipeline/<ngày>-brief-example/
#   00-brief.md  01-plan.md  02-design-r0.md  03-cost-r0.md  04-qa-r0.md
#   (02/03/04-*-r1.md nếu có vòng sửa)  05-final.md  run.json (token, lịch sử PASS/REVISE)
```

Tùy chọn:

```
--max-revisions 2       số vòng sửa tối đa (mặc định 2)
--model claude-opus-5-5 ghi đè model cho mọi agent (mặc định đã là claude-opus-5-5)
--out ./pipeline/x      thư mục đầu ra
--plugin-dir ...        nếu plugin không nằm ở ../plugins/cosmo-engineering
--quiet                 tắt log tiến trình
```

Xem system prompt đã ghép của một agent (agent .md + kiến thức skill kèm theo):

```bash
python -m cosmo_agents show-prompt cost-analyst
```

Mã thoát: `0` nếu QA PASS, `1` nếu hết lượt mà QA vẫn REVISE (dùng được trong script/CI).

## 3. Hồ sơ dự án (`--project-dir`)

Mọi file trong thư mục được gom vào context cho cả 4 agent:

| Loại | Xử lý |
|---|---|
| `.md .txt .csv .json .yaml` | nạp nguyên văn (cắt ở 60k ký tự/file) |
| `.xlsx .xlsm` | đọc từng sheet thành bảng (200 dòng/sheet) — bảng giá NCC, BOM cũ, rate card cũ |
| `.dxf` | tóm tắt entity, layer, extents, text chú thích (cần `ezdxf`) |
| `.pdf .png .step .dwg .docx ...` | **chỉ liệt kê tên** để agent biết có tồn tại — chuyển PDF bản vẽ sang text/DXF trước nếu cần nội dung |

Giới hạn tổng 400k ký tự (`PipelineConfig.max_context_chars`). Vượt giới hạn thì file sau bị liệt kê tên; đây là
điểm Solution 2 (RAG / vector DB) sẽ thay thế khi hồ sơ lên tới hàng trăm file: thay `gather_project_context`
bằng một bước tìm kiếm ngữ nghĩa trả về đúng các đoạn liên quan.

## 4. Vòng sửa hoạt động thế nào

1. QA trả về **structured output** (Pydantic `QAVerdict`): `verdict`, `summary`, `findings[]` (mỗi finding có
   `severity` blocker/major/minor và `target` design/cost/plan), `verified_ok[]`. Orchestrator đọc trường, không parse text.
2. Code quyết định (không để model quyết): `REVISE` và còn lượt → gửi **đúng finding của ai cho người đó**,
   kèm bản trước của họ, yêu cầu "Đã sửa / Không đồng ý vì" từng cái.
3. Nếu Design thay đổi, Cost **luôn** chạy lại (giờ máy/BOM đổi thì giá đổi).
4. QA vòng sau nhận thêm kết luận vòng trước để kiểm tra đã sửa thật chưa.
5. Hết lượt mà vẫn REVISE → vẫn tổng hợp, nhưng tài liệu đánh dấu DỰ THẢO và liệt kê finding mở.

## 5. Chi phí & hiệu năng

- Mỗi dự án không có vòng sửa = 5 lượt gọi; mỗi vòng sửa thêm 2–3 lượt. `run.json` ghi token thật từng lần chạy.
- System prompt (agent + skill) và hồ sơ dự án được **cache** (`cache_control`), nên các lượt sau trả phí đọc cache.
- Effort mặc định: PM `medium`, Design/Cost `high`, QA `xhigh` (phản biện cần nghĩ kỹ nhất). Đổi trong `cosmo_agents/config.py`.
- Nếu một yêu cầu bị bộ lọc an toàn từ chối, API tự chạy lại trên model dự phòng (`fallbacks="default"`).

## 6. Tùy biến

| Muốn | Sửa ở |
|---|---|
| Cách một agent làm việc, mẫu đầu ra | `plugins/cosmo-engineering/agents/<agent>.md` (cả Claude Code và Python đều dùng) |
| Agent nào được kèm skill nào | `cosmo_agents/prompts.py` → `SKILLS_FOR_AGENT` |
| Model / effort / max_tokens từng agent | `cosmo_agents/config.py` → `PipelineConfig.agents` |
| Thêm agent thứ 5 (ví dụ Procurement) | thêm `agents/procurement.md`, thêm một `_call(...)` trong `pipeline.py`, thêm `target` mới trong `schemas.py` |
| Đọc thêm định dạng file | `cosmo_agents/context.py` |
| Thay bằng LangGraph/CrewAI | giữ nguyên 4 prompt + `QAVerdict`; chỉ thay `pipeline.py` (orchestrator ở đây cố ý là code Python thường để dễ đọc và test) |

## 7. Test (không cần API key)

```bash
python -m unittest discover -s tests -v
```

Test dùng LLM giả để kiểm tra: prompt nạp đúng từ plugin, thứ tự gọi agent, finding đi đúng người, Cost chạy lại khi Design đổi, dừng đúng sau `max_revisions`, file đầu ra đầy đủ.
