---
name: mechanical-project-concept
description: Turn a mechanical project inquiry into a client-ready DESIGN CONCEPT proposal — deep requirement analysis, concept options, recommended concept, BOM outline, phased project plan, timeline, and cost estimate — meant to be sent to the customer FIRST, before detailed design. Use this WHENEVER the user describes a new machine/equipment/automation project, a custom fabrication job beyond a single part, or says "làm dự án", "thiết kế", "design concept", "proposal", "đề xuất kỹ thuật", "lên plan/kế hoạch", "estimate", "timeline", or forwards a customer requirement for a system (jig/fixture, mechanism, tooling, equipment, line). Trigger even when the user just describes a problem to solve mechanically and wants something to send the client. Produces a bilingual (VI/EN) concept-first proposal with analysis, options, BOM, plan, timeline, and cost. Default handler for Cosmo Engineering project proposals.
---

# Mechanical Project Concept (Dự án cơ khí — Design Concept)

Produce a proposal that wins the job on engineering credibility: it shows the client you understood the problem, offers a clear recommended concept with alternatives, and gives a realistic plan, timeline, and cost — all at the concept stage, before committing to detailed design. This is a **concept-first** deliverable, not a detailed drawing package.

## Principles

- **Concept before detail.** Don't over-specify. Lock the requirement, present 2–3 concept options, recommend one, and estimate at concept-level accuracy (state the ±% confidence). Detailed design is a later, quoted phase.
- **Phased.** Structure the work in phases (Concept → Detailed design → Fabrication → Assembly/Test → Commissioning). Each phase has a deliverable and a go/no-go, so the client commits incrementally.
- **Build to what Cosmo can make.** Respect shop capability (3 manual lathe, 1 manual mill, 1 Haas VF-4 CNC, 1 wire EDM; outsource HT/coating/grinding/profiling). If a concept needs capability Cosmo lacks, plan it as outsourced and price it that way.
- **Bilingual & client-facing.** Match the client's language; default to VI with EN key terms, or full EN for export/FDI clients. Keep tone confident and specific.

## Workflow

### 1. Requirement analysis (Phân tích yêu cầu)
Extract functional requirements, constraints, and success criteria. Nail down: what the equipment must do, throughput/capacity, loads, cycle time, duty, environment, interfaces (power, air, mounting, upstream/downstream), regulatory/market requirements (e.g. US market compliance for export equipment), and any hard constraints (footprint, budget signal, deadline). List explicit assumptions where the client was silent.

### 2. Concept generation (Phương án)
Develop 2–3 distinct concepts. For each: working principle, key subsystems, materials, how it meets the requirement, pros/cons, rough cost/complexity, and risk. Favor **simplicity and low part count** — prefer one robust SKU over an over-engineered adjustable mechanism unless the requirement truly needs it. Show why the discarded options lose.

### 3. Recommended concept (Phương án đề xuất)
Pick one. Describe it concretely enough to cost and plan: main mechanism, structural approach, drive/actuation, key materials, critical tolerances, and a simple concept sketch description (or offer to generate a diagram). Note the critical-to-function features and how they'll be verified.

### 4. BOM outline (Sơ bộ BOM)
List major assemblies and bought-out items at concept level: structural members, drives/motors/actuators, bearings, fasteners class, purchased components (with likely brand/spec), and material specs for machined parts. Mark make vs. buy vs. outsource. This drives the cost estimate.

### 5. Project plan & phases (Kế hoạch & giai đoạn)
Break into phases with deliverables and go/no-go gates:
- Phase 0 — Concept (this document) → client approval
- Phase 1 — Detailed design (drawings, calculations, final BOM)
- Phase 2 — Procurement & fabrication (machining route per part, material RFQ)
- Phase 3 — Assembly & test
- Phase 4 — Delivery / commissioning / (validation IQ/OQ/PQ if regulated)
Assign responsibility (RACI-lite: who's Responsible/Accountable per phase) where a team is involved.

### 6. Timeline (Tiến độ)
Give a phase-by-phase schedule in working weeks/days from PO, with dependencies (long-lead items, outsourcing turnarounds, HT/coating). Present as a simple milestone list or offer a Gantt-style diagram. State the critical path and what could shift it.

### 7. Cost estimate (Dự toán)
Concept-level estimate with stated confidence (e.g. ±20–30% at concept stage, tightening after detailed design). Structure:
- Design/engineering effort
- Materials (from BOM outline)
- Machining/fabrication (per shop routing; use the machining-quotation rate card if available)
- Bought-out components
- Outsourcing (HT, coating, grinding, profiling)
- Assembly, test, commissioning
- Contingency + margin
Show a **total investment** figure and, if useful, a per-unit price for multi-unit orders (e.g. "20 sets" style). Keep an internal cost view separate from the client-facing price.

### 8. Assumptions, risks, next steps
State assumptions the estimate rests on, key technical/commercial risks with mitigation, and a clear next step (approve concept → proceed to Phase 1 detailed design, with that phase quoted).

## Output template

```
ĐỀ XUẤT THIẾT KẾ / DESIGN CONCEPT PROPOSAL
Dự án (Project): ___   |   Khách hàng (Client): ___   |   Ngày (Date): ___   |   Rev: ___
Cosmo Engineering Ltd. Co.

1. PHÂN TÍCH YÊU CẦU / REQUIREMENT ANALYSIS
2. PHƯƠNG ÁN THIẾT KẾ / CONCEPT OPTIONS  (Option A / B / C — pros, cons, risk)
3. PHƯƠNG ÁN ĐỀ XUẤT / RECOMMENDED CONCEPT  (mô tả + đặc điểm then chốt)
4. BOM SƠ BỘ / PRELIMINARY BOM  (make / buy / outsource)
5. KẾ HOẠCH & GIAI ĐOẠN / PROJECT PLAN (phases + gates + RACI-lite)
6. TIẾN ĐỘ / TIMELINE  (milestones, critical path)
7. DỰ TOÁN / COST ESTIMATE  (± confidence, total investment, per-unit if applicable)
8. GIẢ ĐỊNH – RỦI RO – BƯỚC TIẾP THEO / ASSUMPTIONS, RISKS, NEXT STEPS

--- NỘI BỘ / INTERNAL ---
Giá vốn chi tiết, biên lợi nhuận, điểm thương lượng (negotiation levers), cost-optimization ý tưởng.
```

## Judgment rules
- Keep the client document at concept fidelity; put detailed cost breakdown, margin, and negotiation levers in the INTERNAL block only.
- Always state estimate confidence and what tightens it.
- Prefer the simplest concept that meets the requirement; justify any complexity by a real requirement.
- Every long-lead or outsourced item must appear in both the timeline (as a dependency) and the cost.
- Offer to generate supporting visuals (concept sketch, block diagram, timeline Gantt) and, on approval, to hand detailed line-item pricing to the machining-quotation skill and the final document to the docx/xlsx skill.
- If the project is export/regulated (e.g. US agricultural market, pharma), fold compliance/validation (and IQ/OQ/PQ where relevant) into scope, plan, and cost.
