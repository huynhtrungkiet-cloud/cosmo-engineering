# Coupling Types — Selection, Sizing, Failure Modes, Repair

Table of contents:
1. Gear couplings
2. Universal-joint / Cardan shafts
3. Flexible couplings (B-Flex / elastomer / disc)
4. HTD synchronous belt drives (drive coupling by belt)
5. Rigid couplings
6. Quick selection matrix

---

## 1. Gear couplings

**Use when:** high torque density, small-to-moderate misalignment, reversing/shock duty (steel-plant main drives, pinion stands). Handles large shafts (∅ up to ~540 mm in the drivetrains DHP works).

**Sizing:**
- Design torque = 9550 × kW / rpm (N·m) × service factor (SF).
- SF for reversing rolling-mill duty is high (often 2–3+); use the catalog SF table for the application class.
- Check bore range, max speed, and allowable misalignment (typ. ~0.5–1.5° per gear mesh) against catalog.

**Failure modes:** tooth wear from lube starvation/contamination, fretting at hub bore, misalignment beyond rating → uneven tooth loading, seal failure → grease loss. Steel-plant dust + heat accelerate lube breakdown.

**Repair/DHP notes:** re-machine worn bores and re-fit hubs to correct interference (ISO 286 fit, e.g. H7/s6 class for shrink), verify tooth contact, re-grease with the right high-load EP grease. Check keyway integrity; re-cut oversize + shim if wallowed.

---

## 2. Universal-joint / Cardan shafts (e.g. ITALGIUNTI)

**Use when:** significant angular misalignment between non-parallel shafts; telescoping length change (spline slip) needed.

**Key checks:**
- Operating angle within rating; equal angles at both joints to cancel the 2/rev velocity fluctuation.
- Torque + reversing factor vs. joint rating.
- Spline slip: ensure adequate engagement, lubrication, and no bottoming.

**Critical weld detail (repair):** tube-to-yoke joints. Fillet-only welds are a **fatigue liability** on 42CrMo4-class tubes. Prefer **CJP (complete joint penetration) groove welds**.
- WPS essentials for 42CrMo4: correct groove prep, **preheat** (material is hardenable — preheat/interpass control avoids HAZ cracking), controlled interpass temp, and **PWHT 580–620 °C** to relieve residual stress and temper HAZ.
- Back the repair with a **fatigue check**: compare weld detail FAT class before/after (fillet vs. CJP), Miner's-rule cumulative-damage life estimate for the load spectrum.
- **NDT:** PAUT/UT on the groove welds + hardness survey across weld/HAZ/base to confirm PWHT effectiveness. MT for surface.

**Heat environment:** near radiant heat (rolling mill), protect with **phlogopite mica board** heat shield.

---

## 3. Flexible couplings (B-Flex / elastomer / disc)

**Use when:** need misalignment accommodation + vibration/shock damping, moderate torque, no lubrication desired.

**B-Flex / Rathi / Lovejoy type:** elastomer element in shear/compression. Select from catalog by:
- Torque rating × SF, bore range, max speed, allowable angular/parallel/axial misalignment.
- If a migrated B-Flex data table exists (PDF→Excel catalog), read the rating directly from it rather than estimating.

**Failure modes:** elastomer aging/heat set, over-torque tearing, misalignment beyond rating → premature element wear. Disc types fail by disc-pack fatigue if misaligned.

**Repair/DHP notes:** usually element replacement (consumable). Verify hub bores/fits; re-align within spec at commissioning.

---

## 4. HTD synchronous belt drives (as drive coupling)

Context: Fette tablet-press-style gearmotor + HTD belt system.

**Checks:**
- Belt pitch/width vs. transmitted torque; tooth-jump (ratcheting) margin under peak/shock.
- Pulley center distance, tension, and alignment (parallel + angular of pulley faces).
- Speed ratio and pulley tooth counts; min. teeth-in-mesh.

**Motor/gearmotor pairing:** match Siemens/Flender gearmotor + ATB (or equivalent) motor frame, output speed, and torque to the driven load; check thermal/duty class. For pharma equipment, plan **IQ/OQ/PQ revalidation** after any drivetrain change.

**Failure modes:** tension loss → tooth jump, misalignment → edge wear, over-tension → bearing load. Replace belt + inspect pulleys as a set.

---

## 5. Rigid couplings

**Use when:** shafts truly collinear, no misalignment, need max torsional stiffness/positioning accuracy. Any residual misalignment goes straight into bearing load — only use with precise alignment.

---

## 6. Quick selection matrix

| Requirement dominates | Prefer |
|-----------------------|--------|
| High torque + shock, small misalignment | Gear coupling |
| Large angular misalignment / offset drives | Universal-joint / Cardan |
| Damping + easy maintenance, no lube | Flexible / elastomer (B-Flex) |
| Speed change + drive over distance | HTD belt drive |
| Perfect alignment + stiffness | Rigid |

Always confirm the choice against: design torque (nominal × SF), bore/shaft size, speed, misalignment budget, environment (temp/dust/reversing), and maintenance access.
