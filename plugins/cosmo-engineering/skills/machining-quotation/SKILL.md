---
name: machining-quotation
description: Build a detailed machining/fabrication quotation from a customer email or request. Use this WHENEVER the user pastes or forwards a request that mentions machining a part, fabricating a component, "chào giá", "báo giá", "quotation", "RFQ", "gia công", material + quantity + drawing, or asks for unit price and delivery time for made-to-order parts. Trigger even if the user only says "làm giúp cái này" and drops in a spec, a drawing note, or a parts list. Produces a bilingual (VI/EN) quotation with per-item material, process route, unit price, total, lead time, plus a two-tier (internal cost vs. client price) breakdown and a list of items to confirm. This is the default handler for Cosmo Engineering / DHP machining quotes.
---

# Machining Quotation (Chào giá gia công)

Turn an incoming machining request into a clean, defensible quotation. The goal is a document Kiet can review in one pass and send to the client with minimal edits, plus an internal cost view so margin is always visible.

## Operating context (Cosmo Engineering / DHP)

Assume this shop capacity unless the request says otherwise:
- 3 × manual lathe, 1 × manual mill
- 1 × Haas VF-4 CNC (3-axis vertical machining center)
- 1 × wire EDM (molybdenum wire)
- Outsourced when needed: heat treatment, plating/coating, grinding, gear cutting, casting/forging blanks, laser/plasma/waterjet profiling

Currencies: default **VND** for domestic clients, **USD** for export/FDI clients. If the request is in English or names a foreign buyer, default to USD. Always state the currency and the exchange basis if converting.

Language: match the request. If the incoming email is Vietnamese → answer in Vietnamese with English terms in parentheses for key items. If English → English. If mixed or unclear → bilingual (VI first, EN under it).

## Workflow

Work through these steps in order. Do the engineering reasoning fully; only the money numbers depend on the rate card.

### 1. Parse the request into line items
Extract every distinct part/operation. For each, capture: part name, quantity, material (spec + grade), key dimensions/tolerances, surface finish, heat treatment/coating, drawing reference. If a drawing is attached, read it. Note anything the client left out — it goes in the "to confirm" list, it does not get silently assumed into a price.

### 2. Fix the material for each item
State the material spec precisely (e.g. SCM440 / 42CrMo4, SS400, SUS304, C45). If the client gave a vague material ("thép", "steel"), propose the most likely grade for the application and flag it as an assumption. Estimate blank size (stock diameter/plate size) with realistic machining allowance, and the material weight for costing.

### 3. Route the process
For each item decide the operation sequence and which machine does it. Typical routes:
- Round part, moderate tolerance → manual lathe (+ manual mill for flats/keyways)
- Complex profile / pockets / precise features / batch repeatability → Haas VF-4 CNC
- Hardened part slots, dies, precise through-profiles, no-draft → wire EDM
- Precision bore/OD after heat treat → outsource grinding
Note setups, expected cycle time per piece, and total machine hours = cycle × qty + setup.

### 4. Cost each item (use the rate card)
Read `references/rate-card.md` for machine-hour rates, material price basis, consumables, outsourcing markups, and margin tiers. If the user has given real rates in the conversation, use those instead and say so. Build, per item:
- Material cost = weight × unit price × (1 + scrap allowance)
- Machining cost = Σ (machine-hours × machine-hour rate)
- Outsourcing cost (HT, coating, grinding, blank) at cost + handling markup
- Tooling/consumables if significant (wire EDM wire, special inserts, custom fixture)
- **Internal unit cost** = sum of the above ÷ qty
- **Client unit price** = internal cost × margin tier (see rate card: standard / JPT-tier vs. direct-client-tier)

Never invent a rate as if it were fact. If the rate card still has placeholders, compute the structure symbolically and clearly mark the fields Kiet must fill (e.g. `[CNC rate: ___ VND/h]`), then flag it at the top.

### 5. Lead time
Estimate delivery from: total machine hours vs. available capacity, outsourcing turnaround (HT ~5–7 days, plating ~3–5 days, grinding ~2–4 days — confirm with vendor), material procurement lead time, and current shop load if known. Give a realistic range in working days from PO/deposit, and state the assumptions (material in stock vs. to order).

### 6. Assemble the quotation
Use the template below.

## Output template

Produce this structure (translate labels to match the request language):

```
BÁO GIÁ / QUOTATION
Khách hàng (Client): ___    |    Ngày (Date): ___    |    Số báo giá (Quote No.): ___
Đơn vị: Cosmo Engineering Ltd. Co.

BẢNG BÁO GIÁ / QUOTATION TABLE
| STT | Hạng mục (Item) | Vật liệu (Material) | Quy trình (Process route) | SL (Qty) | Đơn giá (Unit price) | Thành tiền (Amount) | Giao hàng (Lead time) |

Tổng cộng (Subtotal): ___
VAT (nếu có): ___
TỔNG (Total): ___

ĐIỀU KIỆN (Terms)
- Báo giá có hiệu lực (Validity): 30 ngày
- Thanh toán (Payment): 50% đặt cọc / 50% trước giao hàng (điều chỉnh theo thỏa thuận)
- Giao hàng (Delivery): ___ ngày làm việc kể từ khi nhận PO + đặt cọc
- Chưa gồm/đã gồm (Excl./Incl.): VAT, vận chuyển, ...

CẦN XÁC NHẬN (To confirm) — các điểm ảnh hưởng đến giá:
- ...

--- NỘI BỘ / INTERNAL (không gửi khách) ---
Bảng giá thành theo từng item: material / machining / outsourcing / consumables → giá vốn đơn vị → % lãi → giá bán.
Cảnh báo rủi ro chi phí (cost risks): ...
```

Always split the client-facing table from the INTERNAL cost breakdown clearly — the internal block is never for the client.

## Judgment rules
- Missing info that swings the price (drawing, tolerance, qty, material grade, surface finish, heat treat, coating) → list it under "To confirm", quote a conditional price, don't guess silently.
- If quantity is large enough for a fixture/CNC program amortization to matter, show the unit price dropping with qty (price breaks).
- If a job doesn't fit shop capability (e.g. needs 5-axis, gear hobbing, large casting), say so and quote it as outsourced or decline that line.
- Round prices sensibly for the currency (VND to nearest thousand; USD to nearest dollar or sensible increment).
- Keep the reasoning visible in the INTERNAL block so Kiet can defend or adjust any number fast.

If the user wants the result as a file (Word/Excel), build the markdown first, confirm, then hand off to the docx/xlsx skill.
