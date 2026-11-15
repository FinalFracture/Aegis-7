# Strip 5 "The Green" — Multi-Sport Tower — Structure & Floor Plans

**Status:** DRAFT **Rev 3.8**, 2026-11-15 (Vance). Physical structure and floor plans only: no props, no builds, no code.
**Labels:** *(doc)* = value from a cited repo doc; *(physics)* = derived from doc values; *(real-world ref)* = outside practice (IBC 2021, FINA, etc.), not a project constraint; **Vance proposal** = my design call.
**Plan PNGs** (not committed, renders rule): `/workspace/renders/tennis_tower/F1.png, F2.png, F3.png, section.png, site_plan.png`.
**Coordinates:** building local X (axial, along strip x) and Z (across, along strip z), origin at the SW corner; **strip x = 60 + X, z = −40 + Z** (Rev 2.4; was 318 + X). Heights in the building are **above F1 (F1 = 0)**; site heights are **HD = above the hull floor at the strip centreline (z 0)**. **F1 = +4.0 HD** (§3.3).

## 0. Revision log
- **Rev 2.8 (2026-11-06, Vance answers to Rook's base-kit questions, `design/tennis_tower_handoff/VANCE_OPEN_QUESTIONS.md`):**
  - New **§3.12**: aquarium corridor, foyer ticketing, F1/F2 façade, entrances, terrace edges, playground plan.
  - W doors realigned to the grid: **Z 17.5..61.5 = 44 m** (11 × 4 m).
  - S/N apron level resolved; transparency rule restated; kids' wall face corrected to X 84.5.
  - Toddler zone = Meadow Hills; soft-play not sunken; stand bays 12 seats; ridge ornament to +26.4.
- **Rev 2.7 (2026-11-03, Rook stair finding; Vance decision):**
  - Stair cores enlarged for code landings: **Type A 5.5 × 10.2 m, Type B 6.0 × 10.6 m**; flight widths unchanged.
  - All 17 cores re-fitted (§4.6). Zone trims:
    - corner stairs take 4.7 m of each S/N stand segment (≈ −580 seats);
    - ST-AQS/AQN moved to the foyer's inner side (X −6..0) to keep the 42 m of doors;
    - F2 desk moved into the entry lobby; F2 training moved onto the bouldering W wall;
    - F3 playground Z 20.6..58.4 (454 m²); F3 lounge Z 20.6..58.4;
    - F3 restroom blocks re-split, with W/E under-stand blocks added.
  - Egress re-checked (§5).
- **Rev 2.6 (2026-11-03, Jared approved all four column-clash fixes, §3.11.11):**
  - ST+E moved to Z 50..56.
  - The kids' wall E face is on X 84.5, with TC-S3 as a climbable pillar.
  - The front desk front is at Z 9.5, with TC-S2 free-standing and clad.
  - TC-S1 is wrapped in the thickened ST+S1 W wall (core outer face X 57.0); W-CL ends at X 56.
  - Egress re-checked (§5.2).
- **Rev 2.5 (2026-11-03, Rook modeling feedback):**
  - New **§3.11 Modeling spec**. It covers:
    - the 4.0 m curtain-wall / roof module, with 1.5 m closure bays on the 79 m faces;
    - space-frame members and the tree column detail;
    - the stand treads;
    - court boxes 10 × 20 m on a 2 × 2 grid of 14 × 26 m modules, glass **3.0 m + net**;
    - cabanas, climbing panels, the playground piece list, the restroom grid and the lift car;
    - stair cores standardized to 2 types (egress width unchanged at 44.3 m).
  - The roof grid changes from 3.0 m to **4.0 m**, and the façade columns from 9 m to **8 m** centres.
  - Rook's tri-budget plan is accepted, and the BLEND stacking fix is set (§3.11.9).
  - Rook's roof, net and glass questions are answered (§3.11.10).
  - Coordinate fixes:
    - kids wall now X 77..85 (it overlapped training by 0.5 m);
    - track offsets restated against all four glass lines;
    - LW / LE trimmed to 5.5 m and ST+S/N to 6.0 m (core types);
    - §3.5 / §4.6 W tree columns reconciled;
    - stale C5 notes removed.
  - **Column clashes:** TC-E2 / ST+E, TC-S3, TC-S2 and TC-S1 are written up as **Vance proposal — pending Jared** (§3.11.11). They are not applied.
- **Rev 2.4 (2026-11-03, Jared decisions on Rev 2.3 §7):**
  - **Relocated to the Fore cap:** footprint now **x 48..200** (W face **48 m** from the Fore cap at x 0). The West Arrival terrace sits between the Fore Hub and the main entrance. The W Spine ramp is gone; the E ramp and loop moved with the building. Station Walks are re-routed to the **Fore Hub (x 0), x 100 and x 200** stops (§3.8).
  - **F2 S band = climbing & bouldering gym**, with a double-height **20 × 11.5 m wall** through an F3 slab void (§3.7.1).
  - **F3 open areas:** ~400 m **running track** around the perimeter, **dining with tables + 8 cabanas**, a **small bar**, and a **kids' playground** (it fits, on the E terrace) (§3.9).
  - **Restrooms on every floor**, sized to IBC 2021 Table 2902.1 (§3.10).
  - Egress re-run with the new F3 uses: **F3 ≈ 7,120 occupants, 36.3 m needed vs 44.3 m (22% margin) ✓** (§5).
  - Confirmed by Jared: 3 m + 1 m diving boards; the seat count is not a constraint; raised terraces + ramps OK.
- **Rev 2.3 (2026-11-02, QA-04 review DQ-01..21 merged with Vance self-review B1–B3, M1–M7, m1–m7; resolution table in §8):**
  - Aquatic center re-planned (§3.6): W foyer under the F2 gallery with **42 m of main-entrance doors**; diving well moved to the deep central plinth (Z 22..34); slides and runouts axial, inside the north island, no lobby crossing; W-band column grid + transfer trusses defined, no columns in water.
  - Lift gaps in the stands widened to **10 m** (lift + stair side by side); radial aisles every 7.5 m; **seats 6,776** (was 8,624).
  - Egress recomputed to IBC 2021 (sprinklered) including band programs and F3 terraces; **17 stairs, 44.3 m** (§5); full stair/lift/column/transfer coordinate table (§4.6).
  - Plinth curve corrected and reconciled (§3.3); W/E plazas become raised terraces at F1 level with 1:20 Spine ramps; **x 400 Station Walk restored** (§3.8).
  - Stale text removed; superseded content moved to **Appendix A**; sections renumbered.
- Rev 2.2: F3 Glass Box; aquatic center; C5 Arena deferred (Jared will revisit). Rev 2.1: box lacrosse accepted; clear heights accepted; sports are decoration; Spine loop. Rev 2.0: F1 multi-use courts, F2 rink, F3 basketball, stands + concourse every floor, axe + bowling swap with arcade. Rev 1.1: 3 storeys. Rev 1.0: 4 storeys of tennis. Details in Appendix A.

## 1. Brief (Jared, as given)
"A type of multi-tiered tennis court thing. Big, tall, open, 4 floors, each 20 feet tall, each with 4 courts, the top one has arena seating. A series of elevators on each side goes to all floors. Each floor encased in plexiglass. It's an adapted form of tennis, adjusted for the lower gravity. Think about how that may play and look, design around it. Under the seating stands for the top level (all 4 sides): 1 side is an arcade, it will have 2 floors. A short side will have other indoor competition/athletic style games, like axe throwing and bowling. On the other short side, it takes up the whole 2 floors, but it's a swimming pool. On the other long side, first floor is a food court. Second floor is a gym. Let's just work on this design for now. Think hard and critical. Floor plans first; physical structures, not prop placement."
Later decisions (Jared): 3 storeys × 6.10 m (Rev 1.1); "tennis on floor 1, with stands… modified badminton, volleyball, and pickleball. Floor 2… soccer and lacrosse, also with stands. Floor 3… basketball courts, with stands" (Rev 2.0); box lacrosse accepted, sports are story decoration (Rev 2.1); F3 in a giant glass box; "the pool can be bigger or gain amenities"; Arena deferred (Rev 2.2).

## 2. Physics (F1 = 0 m; unchanged since Rev 2.2)
### 2.1 Doc values
| Value | Source |
|---|---|
| R = 200 m floor (Jared Q1) | `design/strip4_plan.md` §1.1; `design/cylinder_master_plan.md` §1 |
| Nominal 1.00G at 1.98–2.09 RPM; flare states 0.35G / 0.12G; aftermath 0.85G at 1.92 RPM | `design/vance_chapter1_solar_flare_environmental_states.md` §State matrix |
| g scales linearly with radius (g_eff ∝ r) | `design/quinn_market_research_and_gameplay_mechanics_spec.md` l.126 (written for R 185.5, retired) |
| Climbing toward the axis gives ~0.02 g Coriolis side push | `design/residential_stair_core_v1.md` |

**Doc inconsistency (flag):** 1.00G at R 200 needs ω = √(9.81/200) = **0.2215 rad/s = 2.115 RPM**. 2.09 RPM gives 0.977 g and 1.98 RPM gives 0.876 g at R 200. The doc RPMs were set for the retired R 185.5. I use **ω = 0.2215 rad/s, 1.00 g at the floor** below.

### 2.2 The key finding: this is not low gravity
At the floor Strip 5 is **1.00 g** (State 1). Spin gravity g(h) = ω²(R − h):
| Level (base height) | g | |
|---|---|---|
| F1 (0 m) | 1.000 g | 9.81 m/s² |
| F2 (6.1 m) | 0.970 g | |
| F3 (12.2 m) | 0.939 g | |
| F3 roof edge (≈18.3–20.5 m) | 0.909–0.898 g | |
| Glass Box roof top (25.5 m above F1) | 0.873 g | |
So the top (F3) court is only ~6% lighter. Lob flight time t = 2v_up/g: a 10 m/s vertical lob takes 2.04 s on F1 and 2.17 s on F3 (+6.5%), apex 5.10 m vs 5.43 m. **The "lower gravity" feel only becomes big in the Chapter 1 crisis states (0.35G/0.12G, doc).** What *is* strong here is **Coriolis**, so I propose the adapted sport is built around Coriolis, with a small per-floor g ladder as a bonus (Vance proposal).

### 2.3 Coriolis (a = −2ω×v, ω along the drum axis)
- **Motion parallel to the axis (strip x): zero Coriolis.**
- **Spinward/antispinward motion (strip z):** radial force 2ωv. At 30 m/s that is 13.3 m/s², bigger than g: a spinward drive "falls" ~2.4× faster than an antispinward one. **Unplayable/unfair for a z-oriented court.**
- **Vertical motion (toward/away from axis):** sideways push, spinward when rising. A lob with v_up drifts sideways by Δ = (4/3)·ω·v_up³/g² (physics):
  - v_up 10 m/s on F1: **3.07 m** drift; on F3: 3.48 m.
  - 4 m-rise lob (fits a 5 m clear ceiling): 2.13 m on F1, 2.20 m on F3.
- Crosscourt component: 5 m/s across the court gives 2.2 m/s² (~0.23 g) radial change; spinward crosscourts dip, antispinward ones float.
- Lifts: a 2.5 m/s lift sees 2ωv = 1.1 m/s² (0.11 g) sideways; at 1.0 m/s it is 0.045 g (Vance proposal: cap lift speed at 1.0–1.6 m/s and use stiff guide rails).

### 2.4 Sport-by-sport notes (Vance proposal unless marked)
**Rev 2.1:** Jared: sports are set dressing for the story, so the clear-height and rules items below are **notes, not critical issues**.
**All play axes run along strip x (axial)**, so the main ball velocity has zero Coriolis; lobs and shots curl spinward on the way up (§2.3). Teams/players change ends at each half or odd game for fairness.

| Floor | Sport | Size *(real-world ref)* | Clear height here | Consequence |
|---|---|---|---|---|
| F1 | Spin Court tennis (padel-derived glass box) | 10 × 20 m, module 14 × 26 m | ≈5.0 m | "Ceiling out" rule, low-rebound ball (Rev 1.0) |
| F1 | Modified badminton | 13.4 × 6.1 m inside the 10 × 20 box | ≈5.0 m (real play wants 7–9 m+) | **Modified:** heavier shuttle, flat-drive game, ceiling out |
| F1 | Modified volleyball | 18 × 9 m inside the box (free zone cut to 0.5 m) | ≈5.0 m (real min ~7 m) | **Modified:** lowered net 2.0 m, no high sets above 4.5 m, side glass in play |
| F1 | Pickleball | 13.41 × 6.10 m, 1 per box | ≈5.0 m | Fits well; low game anyway |
| F2 | **Box lacrosse / arena soccer (recommended)** | rink ~61 × 26 m with boards + glass | ≈4.6 m (§3.4) | Low, fast shots suit it; lofted balls hit the ceiling → ceiling out / ceiling in play (arena-soccer style) |
| F2 | Futsal | 40 × 20 m inside the rink | ≈4.6 m | Convertible lines on the same floor |
| F2 | Field lacrosse | 110 × 55 m | — | **Rejected** (§6, issue 1) |
| F3 | Basketball | 28 × 15 m (+2 m runoff) | **10.3 m under the Glass Box soffit** (Rev 2.2) | The F3 box solves the height on this floor only |

**Basketball Coriolis (physics, g = 0.939 on F3):** drift Δ = (4/3)ωv_up³/g². A free throw (v_up ≈ 5 m/s, flight ≈ 1.1 s) drifts **0.44 m** spinward, about one rim diameter (0.457 m *real-world ref*); a 3-pointer (v_up ≈ 6 m/s) drifts **0.75 m**. Players must aim off; both baskets sit on the axial line, so the drift is mirrored for the two teams and fair over two halves. This is the signature look of the floor.
**Axe throwing Coriolis:** a horizontal 8 m/s throw across the spin gets 2ωv = 3.5 m/s² (0.36 g) radial push, so **all axe lanes throw axially** (along x).
**Bowling:** lanes axial, so the rolling ball has no Coriolis hook (Rev 1.0).


## 3. Structural concept
### 3.1 Zones (all floors)
| Element | X | Z | Size |
|---|---|---|---|
| Play area | 39.5..103.5 | 24.5..54.5 | 64 × 30 |
| Concourse ring (4.0 m; **3.1 m clear** past the 0.9 m PT columns, DQ-21) | 35.5..107.5 | 20.5..58.5 | 72 × 38 outer |
| F1/F2 stands ring (5 rows, 5.5 m) | 30..113 | 15..64 | 83 × 49 outer |
| W band: aquatic center (F1–F2) | −12..30 | 0..79 | 42 × 79 |
| E band: arcade (F1–F2) | 113..140 | 0..79 | 27 × 79 |
| S band: F1 bowling + axe; F2 **climbing & bouldering** | 30..113 | 0..15 | 83 × 15 |
| N band: F1 food court; F2 gym | 30..113 | 64..79 | 83 × 15 |
| Plant stacks F1–F3 (SW, NW, SE, NE) | −12..0 / 128..140 | 0..10 / 69..79 | 4 × 12 × 10 |
| **Footprint** | −12..140 | 0..79 | **152 × 79 m** = 12,008 m² per floor |
| **Strip position (Rev 2.4)** | **x 48..200** | z −40..39 | W face 48 m from the Fore cap; next to the Fore Hub (x 0), x 100 and x 200 S4|5 stops *(doc stops every 100 m)* |

Field lacrosse (110 × 55 m) needs a 186 × 104 m building, wider than the ~101 m usable strip; box lacrosse (accepted) sets the 64 × 30 play area (Appendix A.2).

### 3.2 Stands and seats (DQ-03, DQ-13, DQ-16, M1)
- **Lift gaps 10 m** at each side midpoint (S/N X 66.5..76.5, W/E Z 34.5..44.5) on every floor: lift (4 m) + stair (5.5 m) + 0.5 m wall, so no stair sits in a stand.
- **Radial aisles 1.2 m wide every ≤ 7.5 m** (≤ 12 seats, ≤ 6 m to an aisle), plus the front (concourse) and rear aisles; seat width 0.5 m (Vance proposal).
- Segments: long sides 2 × 31 m each (4 internal aisles → **52 seats/row**); short sides 2 × 14 m each (1 aisle → **25 seats/row**).
- F1/F2: 5 rows, front row +0.9 m behind a glass balustrade, risers 0.40, treads 0.85, top-row headroom 2.5 m (Appendix A.2 derivation). **1,540 per floor.**
- F3: 12 rows on all 4 sides (risers 0.45, top row +5.4 m above F3 = +17.6), long sides Z 9.1..20.5 / 58.5..69.9, short sides X 24.1..35.5 / 107.5..118.9. Long 12 × 208 = 2,496; short 12 × 100 = **1,200** (the Rev 2.2 "+2,084" was wrong; Rev 2.2's true short-side figure was 1,536, DQ-13). **F3 = 3,696.**
- **Total 6,776 seats** (1,540 + 1,540 + 3,696).
- **Rev 2.7:** the enlarged corner stairs take the first 4.7 m of each S/N stand segment: −180 seats on F1 and on F2 (1,360 each), and about −216 on F3 (≈3,480). **Total ≈6,200** (Jared: the seat count doesn't matter).

### 3.3 Plinth and grade (DQ-06, M3)
- The hull floor rises toward the strip edges: height above the centreline **h(z) = z²/(2R) = z²/400** *(physics, R 200 doc)*. The building floor is flat, so the plinth under F1 is **p = F1 − h**.
- F1 must clear the highest hull point under the footprint, the S face (z −40, h 4.00), so **F1 = +4.0 HD** and **p(Z) = 4.0 − (Z − 40)²/400** (Z = building local).
  - Rev 2.2's p(Z) = 3.9 − (Z − 39.5)²/400 and QA-04's 3.9 − (39.5 − Z)²/400 are **the same function** (the square makes the sign irrelevant); both centre on the building, not the strip, and are ~0.1 m low. The correct reading: **the plinth is deepest (4.0 m) at the centreline, Z 40, and zero at the long S/N faces**, because the floor curves *up* to meet the building there. Rev 2.2 had this backwards ("deepest at the long faces").
  - Values: Z 0 → 0.00; Z 10 → 1.75; Z 22 → 3.19; Z 34 → 3.91; Z 40 → 4.00; Z 79 → 0.20.
- **Consequence:** the S and N faces are **at grade** (Rev 2.8: the +5.1 HD of the Rim Promenade / N arm centrelines is just the hull curve, which is the walking surface. **S face: hull +4.00 = F1, flush threshold. N face: hull +3.80, so a 1:12 apron rises 0.20 m over 2.4 m to F1, falling away from the building**). The **W and E faces are 4.0 m above the centreline plazas**: QA-04's level problem is real but it sits on the W/E faces, not S/N.
- **Fix (Vance proposal, Jared OK Rev 2.4):** the West Arrival terrace and East Plaza are **raised terraces at +4.0 HD** (structural deck on fill over the hull, 1.4–4.0 m), so the W and E entrances are level. Rev 2.4: the W terrace is fed directly by the Fore cap portal (§3.8), so there is no W ramp; the Spine leaves the East Plaza on a **1:20 ramp** (80 m, x 230..310). The Fore Hub Station Walk descends from the stop tower foot (z −56, +7.8 HD) to the terrace (+4.0) by steps + a 1:12 switchback ramp inside its 12 m width.
- **Main entrance = W face** (level terrace, 42 m of doors, §5.3); secondary entrances S (x 100 Station Walk side, at grade), N (at grade) and E (terrace).
- Plinth drawn in `section.png`.

### 3.4 Long spans and columns (DQ-09, DQ-21)
- **F2 rink column-free:** the F3 floor spans 30 m across Z on **post-tensioned band beams, 1.5 m zone** → F2 clear ≈ 4.6 m. **PT columns 0.9 × 0.9 m** at 8 m centres on the play-area edge lines Z 24.5 / 54.5 (X 39.5..103.5, 9 per side), padded, inside the concourse (clear width 3.1 m past them).
- **F1:** columns also in the runoff between the 4 court boxes (14 × 26 m grid, 1.1 m floor zone) → F1 clear ≈ 5.0 m.
- **Bands (S/N/E):** one-way 15 m (S/N) and 27 m (E, with a line at X 126.5) slabs between façade columns (8 m centres, Rev 2.5) and the stand-back line; **no columns in the bowling lanes** (X 30..57 spans Z 0..15 in one).
- **W band (aquatic), Rev 2.3:**
  - Column lines **X −12 (façade), X 0 (foyer/water edge) and X 30 (stand back)**, at **Z 3.5, 12.5, 21.5, 30.5, 39.5, 48.5, 57.5, 66.5, 75.5** (9 m). No column stands in water: every water body lies in X 1..29.
  - **9 transfer trusses**, one per Z line, span **30 m (X 0..30)** over the aquatic hall, **2.5 m deep**, top chord at F3 (+12.2), **soffit +9.7**. They carry the F3 W terrace, the W stand overhang (X 24.1..30) and the 2 W tree columns.
  - **Coffer over the diving well (DQ-10):** between the Z 21.5 and Z 30.5 trusses the F3 slab drops to a 0.4 m coffered plate, **soffit +11.8**, giving 9.8 m above the diving deck (+2.0).
  - Foyer bay X −12..0 spans 12 m on a 0.6 m slab (the F2 gallery floor) at +6.1.

### 3.5 F3 Glass Box (Jared Rev 2.2; dimensions and structure Vance proposal)
**Structure (Vance proposal):**
- **Roof:** two-way **square-on-square steel space frame**, **4.0 × 4.0 m grid** (Rev 2.5; was 3.0), 3.0 m deep, CHS members with bolted ball nodes. **Column-free over 96 × 62 m** (the hall, concourse and all 4 stands, X 23.5..119.5, Z 8.5..70.5): depth 3.0 m on the 62 m short span = span/21 ✓ for a two-way frame with light glazing loads (no wind, rain or snow in the drum, Vance assumption).
- **Supports (Rev 2.3, DQ-02/DQ-17; reconciled Rev 2.5):** 12 tree columns carry the inner 96 × 62 field (coordinates §4.6). **10 run grade to roof** (TC-S1..S4, TC-N1..N4 at the S/N stand backs, TC-E1/E2 at the E stand back). **TC-W1/W2 run F3 to roof only**: they stand on transfer trusses T-W4/T-W6 behind the W stand, not on grade. Outside the field the frame is **continuous to perimeter façade columns at 8 m centres** (Rev 2.5; module §3.11.1) plus the 4 plant-stack corners, so there are **no cantilevers**.
- **Walls (Rev 2.5):** steel fin mullions, **600 mm deep, at 2.0 m centres**, with a heavier fin every 4.0 m on the roof grid lines; horizontal transoms at 3.325 m (4 panes over 13.3 m); a façade column every 8 m. Details in §3.11.1.
- **Glazing module:** 2.0 × 3.325 m wall panes; roof panes 2.0 × 4.0 m (2 per 4 m grid bay, split by a glazing bar).
- **Build-up:**
  - **Wall:** laminated low-iron glass 2 × 10 mm heat-strengthened + 1.52 mm SGP interlayer, plus an inner **10 mm polycarbonate ("plexiglass") ball-guard** from +12.2 to +16.2 behind the concourse (the brief's plexiglass).
  - **Roof:** laminated 2 × 8 mm heat-strengthened + 1.52 SGP (overhead safety), 40% ceramic frit dot pattern for glare from the Sun-core and the far-wall city; a **tensioned ball net** under the space frame over the play area.
  - In-engine: alphaMode **BLEND** glass with specular (Aegis-7 Standard, `PROJECT.md`, `context/vance-handoff-v3.md` §2).
- **Drainage / condensation (habitat atmosphere):** there is no rain, so the 2% fall serves **cleaning water and condensate** only, into 300 mm perimeter gutters piped down the corner plant stacks. The box is a conditioned volume inside the drum's shared air (not a pressure boundary). Condensation risk is where chilled supply air meets glass and on the inside of the roof when the drum's lighting cycle drops; control it with dehumidification (NE plant), warm-air curtains at the façade base and a dew-point alarm. Pool humidity is sealed below the F3 slab.
- **Hard-sci-fi look:** gunmetal `#1A1E24` space-frame nodes and fins, matte white `#D8DEE6` fin caps, recessed cyan `#00E5FF` LED strips along every roof grid line (so the box reads as a lit grid from across the drum, 400 m overhead), amber `#FF9500` hazard bands at the plant caps (PROJECT.md palette). From the far side of the drum it reads as a glowing glass slab with the courts visible inside.
- **Smoke:** the 12,008 m² box with a 10–14 m smoke reservoir; NE plant smoke exhaust plus roof vents in the frit zone (Vance proposal).

| Item | Value |
|---|---|
| Plan | 152 × 79 m = 12,008 m², X −12..140, Z 0..79 (full footprint, Jared: "the whole upper level") |
| F3 floor / top stand row | +12.2 / +17.6 |
| Roof space-frame soffit / depth | **+22.5** at the perimeter / 3.0 m |
| Roof top | +25.5 perimeter, **+26.3 crown** (2% fall to gutters) |
| Glazed wall | +12.2 → +25.5 (13.3 m) |
| Headroom over the top row | 4.9 m ✓ |
| Clear over the courts | 10.3 m edge, ≈11.1 m at the crown |
| Gravity at roof top | 0.873 g (physics) |

### 3.6 Aquatic center (W band X −12..30, F1–F2; Vance proposal)
| Element | X | Z | Size | Water depth | Deck / note |
|---|---|---|---|---|---|
| **W foyer (main entrance hall)** | −12..0 | 10..69 | 12 × 59 | — | F1; doors along the W face **Z 17.5..61.5 (44 m, Rev 2.8; was 18.5..60.5 / 42 m)**; ticketing, F2 gallery above |
| Lobby / aquarium corridor | 0..30 | 34.5..44.5 | 30 × 10 | — | foyer → W lift + stair → F1 concourse; **no slide tube crosses it** |
| **Lap pool** | 2.5..27.5 | 0.5..21.5 | 25 × 21 (8 lanes) | 2.0 | tank on the F1 slab, deck +2.0 |
| **Diving well** | 15..28 | 22..34 | 13 × 12 | **4.5** | **3 m + 1 m boards confirmed (Jared, Rev 2.4)**; 2.5 m pit in the plinth (p ≥ 3.19 here) + 2.0 m deck; boards face +X (axial): 3 m board at Z 25 (under the +11.8 coffer), 1 m boards at Z 28.5 and 31.5 |
| Diving / lap deck | 0..30 | 0..34.5 | rest | — | column line X 0 at the deck edge |
| **Lazy river** | outer 1..29, inner 4..26 | outer 47..75, inner 50..72 | 3 m channel, ~100 m loop | 1.0 | river outer edge 1 m from the X 0 columns |
| Island: **kiddie/splash pool** | 5..17 | 51..62 | 12 × 11 | 0.3–0.6 | spray deck |
| Island: **slide towers T1 / T2** | 20..25 | 51..56 / 57..62 | 5 × 5 each | — | **1 m clear of the river's inner edge (X 26)** (DQ-08); stair to a start deck at **+7.0**; tower roof +9.4 under the +9.7 truss soffit |
| Island: **slide runout pool** | 5..23 | 64..71 | 18 × 7, 2 lanes | 1.0 | runouts run **−X (axial)** (M5) |
| Slide bridge (F2) | 0..20 | 58..60.4 | 2.4 m wide | — | gallery (+6.1) → towers, over the river; 3.6 m under the soffit |
| **F2 gallery** | −12..0 | 10..69 | 12 × 59 | — | changing, lockers, viewing; over the foyer, **not over water** (M6); stairs ST-AQS / ST-AQN at both ends (DQ-07) |

- **Slides (DQ-18, M5):** enclosed tubes spiral down inside the island footprint from +7.0. **"+X m" on a tube means its invert (inside bottom).** The highest tube crown is ≤ +9.0, 0.7 m under the +9.7 transfer soffit; no tube crosses a walkway, so no invert-over-walk clearance applies. Straight finishes and runouts run axially (zero Coriolis).
- **Loads (DQ-20, physics, γw 9.81 kN/m³, concrete 24 kN/m³):**
| Body | Water | Tank slab 0.5 m | Total | Bears on |
|---|---|---|---|---|
| Lap pool 2.0 m | 19.6 kPa | 12.0 | **31.6 kPa** | F1 slab on plinth |
| Diving well 4.5 m | 44.1 | 12.0 | **56.1 kPa** | plinth pit (1.0 m below F1) |
| Lazy river / runout 1.0 m | 9.8 | 12.0 | 21.8 | F1 slab |
| Splash 0.6 m | 5.9 | 12.0 | 17.9 | F1 slab |
- **Coriolis (physics):** slides moving spinward/antispinward at 8 m/s feel ±3.5 m/s² (±36% g), hence enclosed tubes and axial runouts. A diver drifts antispinward by ωgt³/3: 0.07 m from 1 m, 0.35 m from 3 m; ≥ 2.5 m side clearance at each board.
- Pools on grade/plinth still assume no hull excavation (unverified).

### 3.7 Bowling, axe throwing, S/N bands, plant
- **Bowling (F1, S band):** 8 lanes along X, X 30..57 (19.16 m to the head pin + 4.6 m approach + 3 m pin deck), Z 0.6..15; 1 m acoustic wall X 57..58.
- **Free bay X 58..66.5:** ST+S1 stair (§4.6) and S-band service.
- **S entrance + lift lobby X 66.5..76.5:** vestibule Z 0..9.5, lift S + stair LS behind it.
- **Axe (F1, S band):** 2 rows × 4 bays (3.7 × 7 m), throwing **+X axially**: row 1 X 77..84 into an isolated target wall X 84..85; row 2 X 94..101 into X 101..102; free bay X 85..94 holds ST+S2. Target walls are 2-leaf isolated concrete on resilient bearings, plus a 1 m acoustic wall toward the stands.
- **F2 S band: climbing & bouldering gym (Jared, Rev 2.4), see §3.7.1.**
- **Restroom cores** in the S/N bands, see §3.10.

#### 3.7.1 F2 climbing & bouldering gym (S band X 30..113, Z 0..15; layout Vance proposal)
| Zone | X | Z | Size | Note |
|---|---|---|---|---|
| **Lead / top-rope hall** (belay floor) | 30..57 | 0..8 | 27 × 8 = 216 m² | over the bowling lanes; double-height over Z 3..8 |
| **Double-height "Stand-Back Wall"** | 36..56 (face at Z 8) | 8..9.1 | **20 m wide × 11.5 m tall** (+6.1 → +17.6 above F1) | through an **F3 slab void X 35..57, Z 3..8** (110 m²); built against the back of the F3 S stand (top row +17.6); ~6 rope lanes at 3.3 m |
| Changing / lockers / WC | 30..57 | 10.5..15 | 27 × 4.5 | behind the wall |
| Front desk / gear rental | **67..76** (Rev 2.7; moved into the entry lobby) | **6.5..9.5** | 27 m² | ST+S1 now fills X 57..64 to Z 13.2; TC-S2 stays free-standing, clad, between the stair and the desk |
| Entry lobby | 66.5..76.5 | 0..9.5 | — | from lift S / LS |
| Kids' wall + auto-belays (5 m walls) | **77..84.5** (E face on X 84.5, Rev 2.6) | 0..15 | 113 m² | TC-S3 built into the E face as a climbable pillar |
| Training (spray / hang boards) | — | — | — | **Rev 2.7: moved onto the W wall of the bouldering hall (X 94)**; ST+S2 now fills X 86..92 to Z 13.2 |
| **Bouldering hall** | 94..113 | 0..15 | 19 × 15 = 285 m² | 4.5 m walls, 300 mm mats (band clear ≈ 5.4 m); tree column TC-S4 (X 101.5) clad as a free-standing "tree boulder" |
- **Is the double-height wall feasible? Yes (Vance proposal, engineer to confirm).** The F3 S-band slab spans one way Z 0..15; the void needs **trimmer beams along Z 3 and Z 8** (X 35..57, 22 m), carried by the façade grid at X 33/42/51/60 on Z 3 and by the wall's own steel frame (posts at X 36, 42, 46, 51, 56) on Z 8. No tree column is hit (TC-S1 is at X 57.5, Z 8.5, just outside). The F3 track runs past the void's S edge behind a glass rail, so runners and the S concourse look down on the climbers.
- **Physics:** g at the top hold (+17.6) is 0.912 g. Climbing is slow (≈0.5 m/s → 0.02 g sideways, same as the stair doc), but a lowering climber at 1.5 m/s feels 2ωv ≈ 0.07 g sideways, so auto-belays and lowers swing gently spinward; lanes 3.3 m apart, story beat "you never come down where you went up".
- **N band:** F1 food court, F2 gym (stairs ST+N1/N2 and the N lift stack pass through).
- **Arcade (E band):** ~1,730 m² net per floor; ST+E and façade stairs ST-ARS / ST-ARN pass through.
- **Plant:** 4 corner stacks (SW/NW pool, SE substation + bowling machines, NE AHUs/chillers/smoke exhaust), rising through the Glass Box to louvred caps (~+28).

### 3.8 Site: Spine Walk arrival and loop (strip coordinates, Vance proposal)
| Element | x | z | Width | Level / note |
|---|---|---|---|---|
| Fore cap portal (Spine) | 0 | −6..6 | 12 m | lands on the terrace at +4.0 HD (§3.8 note) |
| **West Arrival Terrace** | 0..48 | −24..24 | 48 × 48 | deck **+4.0 HD**; main entrance on the W face (doors z −21.5..20.5) |
| **Fore Hub Station Walk** | 0..12 | −56..−24 | 12 m | from the Fore Hub stop tower (+7.8) down to the terrace SW corner: steps + 1:12 switchback |
| **x 100 Station Walk** | 94..106 | −62.8..−40 | 12 m | x 100 stop → S arm → **S entrance at x 126.5..136.5** (20 m east) |
| **x 200 Station Walk** | 194..206 | −62.8..−40 | 12 m | x 200 stop → S arm at the SE corner → SE corner link → East Plaza |
| Loop S arm (= Rim Promenade) | 48..200 | −50..−40 | 9.5 m + 0.5 m paved apron | S face at grade |
| Loop N arm | 48..200 | 39..50 | **11 m** (absorbs the old 2 m gap, m7) | N face at grade; N entrance x 126.5..136.5 |
| Corner links | 36..48 / 200..212 | ±24..±41 | 12 m | terrace (+4.0) to arms (+4.0..4.2): level |
| **East Plaza (terrace)** | 200..230 | −24..24 | 30 × 48 | +4.0 HD; E entrance |
| **East Spine ramp** | 230..310 | −6..6 | 12 m | 1:20 down to grade |
| Spine Walk (to Aft) | 310..800 | −6..6 | 12 m | at grade |
| Cross walks x 50 / 150 | 50 / 150 | −62.8..−50, 50..62.8 | 6 m | end at the loop arms |
- **Area (m², Rev 2.4):** terraces 3,744 + E ramp 960 + N arm 1,672 + corner links 816 + Station Walks 942 ≈ **8,130 m² (0.81 ha)** excluding the existing Rim Promenade (the W ramp is gone).
- C5 Arena block: **deferred, Jared will revisit**.
- **Spine at the Fore cap (Vance proposal, needs a Fore Cap map tie):** the cap portal (x 0, z −6..6) lands **level at +4.0 HD** on the terrace. **Rev 2.9 decision: build to +4.0 HD; the Fore Cap map must set the portal floor at +4.0 HD. The fallback below is not built.** If the Fore Cap map fixes the portal at grade (0 HD), the fallback is grand steps + 2 lifts + a 1:12 switchback ramp (48 m in 4 legs) inside the terrace's W 12 m; an 80 m 1:20 ramp does not fit between the cap and the building.
- **Recreation layout:** `recreation_slice_36deg_layout_v1.md` §8 C5 was updated in 2bef23c. Tower complex x 0..310; parks + Dome x 310..520; River x 530..740 unchanged.

### 3.9 F3 open areas (Jared Rev 2.4; layout Vance proposal)
| Element | X | Z | Size | Note |
|---|---|---|---|---|
| **Running track** | loop X 0.7..127.6, Z 0.7..78.4 | — | **1.8 m wide (2 lanes), ≈400 m centreline lap** | Offsets (Rev 2.5): **S and N straights 0.7 m** off the Z 0 / Z 79 glass (clears the 600 mm fins). **W straight 12.7 m** in from the X −12 glass and **E straight 12.4 m** in from the X 140 glass: both run inboard of the 4 plant corners (12 m deep), so the cabanas sit on the W side and the playground on the E side, outside the loop; painted crossings at every stair landing. S/N straights are axial (zero Coriolis); on the W/E straights a 4 m/s runner gets ±0.18 g (spinward "heavy leg", antispinward "light leg"), story beat |
| **Dining terrace (tables)** | 3.5..23 | 4..33 and 46..75 | 2 × 565 m², ≈230 seats each | over the aquatic transfers; served from the F1 food court via lift W |
| **Cabanas** | −11..−7 | 18..62 | **8 cabanas, 4 × 4 m**, 1.5 m apart | along the W glass, looking out at the Fore cap |
| Lounge / view walk | −7..−0.7 | **20.6..58.4** (Rev 2.7) | 6.3 m wide | between cabanas and track; ST-AQS/AQN at its ends |
| **Small bar** | 8..20 | 35..44 | 12 × 9 = 108 m², ~14 m counter, ~20 stools | opposite the LW / lift W landing |
| **Kids' playground** | 128.3..140 | **20.6..58.4** (Rev 2.7) | **12 × 37.8 = 454 m²**, fenced 1.2 m | **fits**, on the E terrace outside the track between ARS and ARN; 3 gates (S end → ARS, N end → ARN, gated track crossing → ST+E); swings and slides axial (no Coriolis twist) |
| Climbing void + glass rail | 35..57 | 3..8 | 110 m² | view down to F2 (§3.7.1) |
| S / N rear concourse lounges | 3..125 | 2.5..9.1 / 69.9..76.5 | ≈650 / 730 m² net | |
| Restrooms under the stands | §3.10 | | | |

### 3.10 Restrooms (Jared Rev 2.4: every floor; IBC 2021 Table 2902.1 A-4, *real-world ref*; layout Vance proposal)
Rule: occupants 50/50; WC male 1/75 for the first 1,500 then 1/120, female 1/40 for the first 1,520 then 1/60; lavatories male 1/200, female 1/150; drinking fountains 1/1,000; up to 67% of male WCs may be urinals. Plus **2 all-gender accessible/family rooms per floor**. Space allowance 5.5 m² per WC (incl. lavs and circulation). Aquatic changing rooms (F2 gallery) are extra.
| Floor | Occupants (§5.1) | WC M (≤ 67% urinals) | WC F | Lav M / F | Fountains | Need | Blocks (X, Z) | Provided |
|---|---|---|---|---|---|---|---|---|
| F1 | 5,120 | 29 | 56 | 13 / 18 | 6 | ≈470 m² | **R1-S** 102..113, 0..15 (165); **R1-NW** 30..44, 64..79 (210); **R1-NE** 102..113, 64..79 (165) | 540 m² ✓ |
| F2 | 4,138 | 25 | 48 | 11 / 14 | 5 | ≈400 m² | **R2-NW** 30..44, 64..79 (210); **R2-NE** 102..113, 64..79 (165); climbing changing WC 30..57, 10.5..15 (~60) | 435 m² ✓ |
| F3 | 7,120 (conservative; Rev 2.7 ≈ 6,830) | 38 | 72 | 18 / 24 | 8 | ≈605 m² | Rev 2.7, under the stands (headroom 2.6–5.4 m): **S** X 36..57, 76.5..86, 92..107 (Z 9.1..15); **N** X 36..58, 76.5..86, 92..107 (Z 64..69.9); **W** X 24.1..30, Z 21..34; **E** X 113..118.9, Z 21..34 | 696 m² ✓ |
| **Total** | | **92** | **176** | **42 / 56** | **19** | | **268 WCs** | |
- Wet stacks line up at X 36..44 and X 102..107 (N) through all three floors; R1-S stands alone over the SE substation side.
- The R1-S block takes the free S-band bay X 102..113 behind the AXE 2 target wall; R1/R2-NW and NE take the ends of the food court and gym.

### 3.11 Modeling spec (Rev 2.5, for Rook; Vance proposal unless marked)
#### 3.11.1 Curtain-wall and roof module
- **Module 4.0 m**, origin at the SW corner (X −12, Z 0).
  - **X faces (S/N, 152 m): 38 bays × 4.0 m**, which divides exactly.
  - **Z faces (W/E, 79 m): 1.5 m closure bay + 19 × 4.0 m + 1.5 m closure bay.** The closure bays sit at the corners, behind the plant shafts.
- **Mullion fins:** every 2.0 m (light fin, 600 × 25 mm plate). Every 4.0 m a heavy fin (600 × 50 mm) lands on a roof grid line. **Façade columns** (600 × 300 mm box) at 8.0 m: 19 bays on the X faces; on the Z faces at Z 1.5 + 8k (k = 0..9), then the last bay of 4.0 m to Z 77.5.
- **Transoms** at +3.325 / 6.65 / 9.975 above F3 (box 150 × 100 mm). **Wall pane 2.0 × 3.325 m.**
- **Roof grid:** 4.0 × 4.0 m on the same origin (X −12 + 4i; Z 1.5 + 4j inside the 1.5 m closure strips). Roof pane 2.0 × 4.0 m.
- **Tree trunks keep their §4.6 positions** (they are not on grid lines). Their branches land on the nearest 4 bottom-chord nodes (§3.11.3).
#### 3.11.2 Space frame
| Member | Size | Note |
|---|---|---|
| Top / bottom chords | CHS **219 mm** (CHS 273 in the 2 bays around each tree) | 4.0 m long |
| Diagonals | CHS **168 mm** | top-to-bottom, half-offset (square-on-square) |
| Ball nodes | **Ø 350 mm**; Ø 450 mm at tree branch heads and façade columns | bolted |
| Depth | 3.0 m centre to centre | soffit +22.5, top +25.5 (flat, §3.11.10) |
| Instancing | **5 × 5 bay tile = 20 × 20 m** (Rook) | along X: 7 full tiles + a 3-bay strip; along Z: 3 full tiles + a 4-bay strip + the 1.5 m closure strips |
#### 3.11.3 Tree columns (12)
- **Trunk:** CHS **Ø 914 mm**, from the base to the branch point at **+19.0** (1.4 m above the top F3 stand row).
- **Branches:** **4 per tree**, CHS Ø 406 mm, cast-steel crown node at +19.0. They land on **4 bottom-chord nodes at +22.5** forming an 8 × 8 m square around the trunk. Each tree's square snaps to the nearest grid nodes, so branch lengths vary ±0.7 m; model 2 variants.
- **Base:** 10 trees run grade to roof on a pinned cast-steel shoe on a 2.0 × 2.0 × 0.6 m concrete pedestal on the F1 slab; the trunk is clad 1.2 m square through the bands. TC-W1/W2 sit on a shoe on the top chord of T-W4 / T-W6 at +12.2 (F3 floor).
- Colours: gunmetal `#1A1E24`, with a cyan LED ring at the crown node.
#### 3.11.4 Stands
- **F3:** 12 rows, riser 0.45 m, **tread 0.95 m** (11.4 m deep / 12), seat 0.5 m wide.
- **F1/F2:** 5 rows, riser 0.40 m, tread 0.85 m (Rev 2.3).
- Instance unit: a **7.5 m stand bay** (Rook), i.e. 15 seats between radial aisles. Odd lengths use one cut bay per segment end.
#### 3.11.5 F1 court boxes (reconciles the 14 × 26 m grid with 4 boxes in 64 × 30)
- **Glass court box: 10 × 20 m** (Z × X), play along X. The modified volleyball court (18 × 9 m) and pickleball fit inside it.
- **Module 14 × 26 m** (2 m runoff around each box on the sides, 3 m at the ends). 2 × 2 modules = **28 × 52 m**, centred in the 64 × 30 play area at **X 45.5..97.5, Z 25.5..53.5** (1 m clear to the PT lines at Z 24.5 / 54.5).
- **Boxes:** X **48.5..68.5 and 74.5..94.5** × Z **27.5..37.5 and 41.5..51.5**. The F1 runoff columns stand on X 71.5 at Z 39.5 (the middle of the 2 × 2 grid).
- **Glass (Rev 2.5): panels 2.0 m wide × 3.0 m tall** (12 mm toughened, in steel posts at 2.0 m). Each box takes 2 × 10 long-side + 2 × 5 end panels = **30 panels**, minus 2 door panels. Above the glass a **ball net runs from 3.0 m to the ceiling** (≈5.0 m).
#### 3.11.6 F3 amenities
- **Cabanas (8):** 4 × 4 m. Post-and-beam frame 3.0 m to the eave, fabric hip roof with its **peak at 3.4 m**, 3 sides with roll-down fabric, open toward the glass.
- **Climbing panels:** module **1.25 m wide**.
  - Lead wall: 20 m = 16 panels, 11.5 m tall in 2.3 m courses (5 courses).
  - Kids' wall: on the **X 84.5 face** (15 m along Z), 12 panels × 5.0 m (Rev 2.8 clarification).
  - Bouldering: 15 m wall = 12 panels; the 19 m wall = 15 panels + a 0.25 m trim; 4.5 m tall, with 1.5 m faceted overhang segments.
- **Playground (E terrace, 12 × 45 m):**
  1. combo tower (2 decks at 1.2 / 2.0 m, 2 slides running axially), 8 × 6 m;
  2. 2-bay swing set (4 seats, swinging along X), 7 × 3 m;
  3. climbing dome Ø 4 m;
  4. 2 see-saws (rocking across, along Z);
  5. **Meadow Hills** toddler zone, 8 × 8 m (hills, tunnel, mini slide, pods, balance path; Rev 2.8);
  6. 3 balance beams;
  7. soft-play 4 × 4 m, **not sunken** (0.35 m raised rim on the overlay; Rev 2.8);
  8. 6 benches;
  9. 1.2 m fence with 3 gates; poured-rubber surface in 3 colours (decals).
  - No spinning pieces (Coriolis).
#### 3.11.7 Restrooms
- **Grid 0.9 m.** WC stalls 0.9 × 1.5 m; accessible stall 1.8 × 1.6 m (1 per block); partitions 1.8 m tall, 0.15 m off the floor.
- Urinals at 0.75 m centres with 0.45 m screens. Vanities at 0.75 m centres, 0.6 m deep counters, mirror band 1.0 m.
- Blocks are built from a 7.2 m (8 × 0.9) row unit: 8 stalls facing 8 stalls across a 1.8 m aisle (7.2 × 4.8 m).
- Counts per floor: §3.10.
#### 3.11.8 Lifts and stairs
- **Lift car:** 1.6 × 2.4 × 2.5 m internal, 1,600 kg / 21 persons (stretcher-capable), centre-opening doors 1.1 × 2.1 m. 2 cars per stack in the 4 × 4 m shaft zone (2 × 2.0 × 2.8 m shafts). Speed 1.0–1.6 m/s (§2.3).
- **Stair cores, 2 types only:**
  - **Rev 2.7 (Rook: two flights per 6.1 m storey need code landings):** 36 risers per storey at **0.1694 m**, 18 per flight (3.05 m rise, under the 3.66 m IBC flight limit); **treads 0.28 m**, 17 per flight = **4.76 m run**; **landing depth = flight width**; walls 0.2 m; 0.1 m well.
  - **Type A: core 5.5 × 10.2 m** (5.5 = 2 × 2.5 + 0.1 + 2 × 0.2; 10.16 = 4.76 + 2 × 2.5 + 2 × 0.2). 2.5 m flights. 8 cores: C-SW/SE/NW/NE, LS, LN, LW, LE.
  - **Type B: core 6.0 × 10.6 m** (6.0 = 2 × 2.7 + 0.2 + 2 × 0.2; 10.56 = 4.76 + 2 × 2.7 + 2 × 0.2). 2.7 m flights. 9 cores: ST+S1/S2/N1/N2, ST+E, ST-AQS/AQN, ST-ARS/ARN.
  - Long-axis orientation per core is in §4.6.
  - **Egress re-check:** 8 × 2.5 + 9 × 2.7 = **44.3 m, unchanged**. F3 needs 36.3 m ✓, F2 21.1 m ✓ (§5.1).
#### 3.11.9 Tri budget and transparency (Rook)
- **Accepted (Rook's plan):**
  - an instanced 5 × 5 space-frame tile (§3.11.2);
  - a 7.5 m stand bay;
  - a track kit of 4 straights + 4 corners;
  - decals for court lines, track lanes, wayfinding and playground surfacing.
- **Stacked BLEND glass fix (Vance proposal):**
  - **only the Glass Box envelope is BLEND** (one layer from any viewpoint, plus the roof);
  - **F1 court glass drops to 3.0 m** and uses **alpha-scissor** (dithered 30% tint + opaque frame/frit edge band);
  - the F3 polycarbonate ball guard and **all ball nets are alpha-scissor**;
  - roof frit is baked into the roof BLEND texture (no extra layer);
  - the pool hall glass on the lobby / view bridge is opaque-frit scissor.
  - So no view looks through more than one BLEND layer.
#### 3.11.10 Rook's questions, answered
1. **Roof crown: faceted.** Two flat planes meeting at a ridge along X at Z 39.5, not a curved surface.
2. **2% fall:** **model the roof flat** at top +25.5 for instancing. The crown is shown only as a **ridge cap** (one bay each side of Z 39.5, peak +26.3; Rev 2.8: leaf ornament may reach +26.4, eaves 0.2 m reveal OK). The physical fall stays a design note.
3. **Ball net: a separate asset** (alpha-scissor, hung 1.0 m under the space-frame soffit over the F3 play area, plus the F1 court nets).
4. **Court glass lower: yes**, 3.0 m + net (§3.11.5).
#### 3.11.11 Column clashes — **DECIDED (Jared, 2026-11-03), applied in Rev 2.6**
| Clash | Problem | Proposed fix |
|---|---|---|
| **TC-E2** (119.5, 48.5) vs **ST+E** (119.5..125.5, Z 46..52) | trunk on the stair's W edge line | move ST+E north to **Z 50..56** (same X), so the trunk is 1.5 m clear; still outside the E stand and the track (E straight X 125.8) |
| **TC-S3** (84.5, 8.5) vs kids' wall (X 77..85) | trunk inside the kids' wall zone near its E edge | set the kids' wall's E face on **X 84.5** and build the trunk into the wall (clad as a climbable pillar); no zone change |
| **TC-S2** (65.5, 8.5) vs front desk (X 58..66.5, Z 9..15) | trunk 0.5 m in front of the desk | move the desk front back to **Z 9.5** and leave the trunk free-standing in the lobby as a clad feature column |
| **TC-S1** (57.5, 8.5) vs ST+S1 (X 58..64, Z 2.6..8.6) and W-CL end (X 56) | trunk 0.5 m from the stair corner, 1.5 m from the wall end | wrap the trunk in a thickened W wall of ST+S1 (core outer face to X 57.0); W-CL stays ending at X 56 |

### 3.12 Base-kit decisions (Rev 2.8; Vance proposal unless marked; full Q&A in `tennis_tower_handoff/VANCE_OPEN_QUESTIONS.md`)
#### 3.12.1 Lobby / aquarium corridor (X 0..30, Z 34.5..44.5)
- **Tank:** X 1..23, Z 42.5..44.5, water 2.8 m deep, top +3.2. **Acrylic line on Z 42.5**, 4 × 5.5 m panels, 0.2 m thick. Opaque reef backdrop behind; service catwalk at +3.4 via a hatch from the F2 view bridge. Load ≈ 39.5 kPa ✓.
- **Corridor:** clear width 8.0 m (Z 34.5..42.5), walk X 0..24.5. The X 0 / Z 39.5 column is clad as a portal pier.
- **Finish and props:** slate terrazzo floor, a cyan inlay at Z 41.5, a lean rail at Z 41.9, 4 benches, 2 info plinths, 3 caustic projectors.
- **Wayfinding:** blades at X 1 and X 24; AQUATICS signs at the deck doorways.
- **Transparency:** the acrylic is the **single BLEND layer** in its view (allowed).
#### 3.12.2 F1/F2 façade (all faces; 4.0 m bays, 8 m columns)
- **F1:** 4.0 m storefront (2 × 2.0 m panes) + a 2.1 m slate spandrel.
  - **Opaque slate bays:** bowling (X 30..57 S), axe (X 77..102 S), WC R1-S/NW/NE, stair cores on the façade (ARS/ARN), and the 1.5 m corner closure panels in front of the plant.
- **F2:** slate with a 2.4 m ribbon window (+1.2..+3.6) and a cyan LED reveal at each floor line; opaque at WC R2 and the climbing changing rooms.
  - **Above the W doors:** slate + 0.6 m clerestory, with a **10 m glazed viewing window at Z 34.5..44.5**.
  - **Above the S/N/E entrances:** a 1.2 m illuminated glyph band.
- **Façade bay asset:** used on all S/N/E runs and on the W face outside the doors. Tree pedestals may stand 0.12 m into the Rim Promenade (≥ 9.38 m clear).
#### 3.12.3 Entrances
- **W main:** doors **Z 17.5..61.5 = 44 m** (11 × 4.0 m bays on grid lines; the 8 m columns sit on bay joints). Canopy 2.6 m. A **6 m egress zone in front of the doors stays clear** (no kerb or hedge; bollards at ≥ 1.5 m spacing).
- **Secondary:** one 8.0 m module (2 double pairs, 3.6 m clear), mirrored S/N at **X 68..76**, rotated for **E at Z 33.5..41.5**. Canopy 2.2 m; 3 m clear in front. The E threshold is flush on the terrace deck (+4.0). Glyph = a parameter on one asset.
#### 3.12.4 Foyer ticketing
- **Desks:** two 8 m desks against X 0 at **Z 22..30 and 49..57**, desk front X −2.5. Each has 1 accessible bay (0.86 m) + 4 stations (1.05 m): **10 stations** in all.
- **Queues and kiosks:** 3-lane serpentine queues in X −6..−2.5; **8 kiosks** (Rev 2.9) against the X 0 wall, X −1.0..0, faces −X: Rev 3.4 explicit **centres** (0.6 m wide, footprint X −0.699..0): **Z 31.175, 32.05, 32.925, 33.8** (S group), **Z 42.875, 43.75, 44.625** (between the aquarium mouth and the N-deck door), **Z 47.675** (N of the door), between the desks and clear of the aquarium corridor mouth (Z 34.5..42.5). Use zone X −2.5..−1.0; nothing in the 6 m passage.
- **Clearances:** a 6 m clear passage (X −12..−6) runs the full foyer length.
- Model +Z faces −X. Screens are opaque emissive; printers and RFID are baked mesh (any live behaviour is a later Gage item).
#### 3.12.5 Terraces, ramps, plinth (project rule)
- **Guards:** 1.07 m, < 100 mm openings, wherever the drop is > 0.76 m. That covers terrace edges, corner-link outer edges, and the East Spine ramp sides from x 230 to ≈ 295 (a 0.15 m kerb below that). No handrails on the 1:20 ramp or the aprons; no ramp landings.
- **Skirt:** exposed only on terrace / ramp / corner-link edges and a 0.2 m course on the N face.
  - Stepped 1.0 m course trim is OK.
  - A 3.7 m variant goes under the 0.30 m deck tiles.
  - Stepped V1/V2 variants only off circulation.
- Corner links reuse the deck + skirt. The Fore Hub Station Walk steps get a later small kit.
#### 3.12.6 Other
- **Transparency rule (supersedes §3.11.9 wording):** **at most one BLEND layer in any line of sight.** BLEND = the F3 Glass Box envelope/roof and the aquarium acrylic only. Alpha-scissor = all F1/F2 glass (doors, storefront, ribbon, gallery window), court glass, the F3 ball guard and nets. Signage and screens are opaque emissive.
- **Stands:** 7.5 m bay = **12 seats + a 1.2 m aisle**. Long runs 26.3 m = 3 bays + a 3.8 m cut bay (corner-stair end); short runs 14.0 m = 1 bay + a 6.5 m cut bay (lift-gap end). V6 hybrid finish.
- **Slides:** island datum F1 + 1.0. The 2.4 m bridge necks to a 1.1 m gate at T2; a 1.0 m link deck at +7.0 joins T2 to T1.
- **Cabanas:** 8 at X −11..−7, centres at Z 20 + 5.5k, open to −X. **Bar:** staff opening at the +X end (toward lift W); 1.5 m accessible section (0.86 m) at the W end of the S face.
- **Climbing:** the 19 m bouldering wall is on Z 15 (overhang kick toward −Z); the 15 m walls are on X 113 and X 94 (training). The kids' wall is on the X 84.5 face, with a 2.0 m mat zone.
- **Playground plan** (zone X 128.3..140, Z 20.6..58.4; flat accessible path X 128.3..129.8):

  | Piece | X | Z |
  |---|---|---|
  | Toddler Meadow Hills | 130..138 | 21.5..29.5 |
  | Soft-play | 130..134 | 30.5..34.5 |
  | See-saws (Rev 2.9: 2 boards, rocking along **Z**, 3.6 m long × 0.4 m, at X 135.8 and 137.2) | 135..138 | 31.2..34.8 (+0.7 m fall zone each end) |
  | Swing set (swings along X) | 130..134.45 | 37..44 |
  | Balance beams | 134.8..139.8 | 36.5..44.5 |
  | Climbing dome, Ø 7 m pad | centre 134 | centre 48.4 |
  | Combo tower 8 × 6 m | 130..138 | 52.4..58.4 |

  - Benches (Rev 2.9): 4 benches, 1.8 × 0.5 m, long axis along Z, **outside the W fence** at X 127.2..127.7 facing +X, centres Z 25, 33, 41, 46 (W gate Z 50..51.5 kept clear). The 1.5 m path stays fully clear.
  - Fence: 0.6 m kick-plate + 80 mm pickets.
  - Gates: S (Z 20.6, X 128.5..130), N (Z 58.4, X 128.5..130), W (X 128.3, Z 50..51.5).
  - Surface: rubber overlay at +0.038, with the humps kept off the path.

## 4. Floor-by-floor plans
### 4.1 Summary
| Floor | Height | g | Play area | Stands | S band | N band | W band | E band |
|---|---|---|---|---|---|---|---|---|
| F1 | 0–6.1 | 1.000 | 4 Spin Court boxes (convertible: modified badminton / volleyball / pickleball) | 5 rows, **1,540** | bowling 8 + axe 8 + S entrance | food court | foyer, lap, diving, lazy river, splash, slides | arcade L1 |
| F2 | 6.1–12.2 | 0.970 | 1 box-lacrosse / arena-soccer rink 61 × 26 (futsal 40 × 20) | 5 rows, **1,540** | **climbing & bouldering** | gym | gallery + aquatic hall void | arcade L2 |
| F3 | 12.2–26.3 | 0.939 | 2 basketball courts 28 × 15 end-to-end along X | 12 rows, **3,696** | lounge, climbing void, track | lounge, track | dining, cabanas, bar, track | kids' playground, track |
Court counts: **F1 4, F2 1 rink, F3 2.**

### 4.2 F1
```
Z79 +-PLANT NW-+------------- FOOD COURT -------N+----------------+-PLANT NE-+
    |FOYER|LAZY RIVER+island(splash,T1,T2,runout)|==STANDS 5r==L==|  ARCADE  |
Z44 |doors|========= LOBBY ====L=W=| CONCOURSE / 4 COURTS 2x2 |L=E  ARCADE  |
Z34 |42 m |DIVING 15..28 | LAP POOL|==STANDS 5r====L====|      ST-ARS   |
Z0  +-PLANT SW-+--BOWLING X30-57|ST+S1|S ENT/LIFT|AXE1|ST+S2|AXE2|WC-+-PLANT SE-+
    X-12  X0          X30                                    X113    X140
```
### 4.3 F2
Gallery X −12..0 (stairs ST-AQS/ST-AQN at its ends, bridge to the slide towers), aquatic hall void, rink, S band climbing & bouldering (§3.7.1), gym with WC blocks at both ends, arcade L2. Same stair and lift stacks as F1. F1 WC blocks: §3.10.
### 4.4 F3
Glass Box over the full footprint; 12-row stands on 4 sides with 10 m lift gaps; perimeter track; W terrace dining, cabanas, bar; E terrace playground; climbing void; WC under the S/N stands; 12 tree columns (§3.9).
### 4.5 Section (`section.png`, cut at X 50, looking +X; Rev 2.4)
Hull curve, plinth (0 → 4.0 → 0.2 m), F1/F2/F3 slabs, S/N stands, climbing void + 11.5 m wall, WC under the F3 stands, track, Glass Box; ST+S1/ST+N1 shown dashed (beyond, at X 58).

### 4.6 Coordinate table: stairs, lifts, tree columns, transfers (DQ-02, DQ-14, B3)
| ID | Type | X | Z | Floors | Width | Lands in (F1 / F2) |
|---|---|---|---|---|---|---|
| C-SW / C-SE / C-NW / C-NE | stair (ring corner), **Type A 5.5 × 10.2**, long axis X | **30..40.2 / 102.8..113** | 15..20.5 / 58.5..64 | F1–F3 | 2.5 | ring corner + first 4.7 m of the S/N stand segment (Rev 2.7) |
| LS | stair beside S lift, Type A, long axis Z | 71..76.5 | **9.5..19.7** | F1–F3 | 2.5 | S lift gap (4.5 m passage kept at X 66.5..71) |
| LN | stair beside N lift, Type A, long axis Z | 71..76.5 | **59.3..69.5** | F1–F3 | 2.5 | N lift gap (4.5 m passage kept) |
| LW | stair beside W lift, Type A, long axis X | **24.5..34.7** | 39..44.5 | F1–F3 | 2.5 | lobby end + W lift gap (passage Z 34.5..39 kept) |
| LE | stair beside E lift, Type A, long axis X | **108.3..118.5** | 39..44.5 | F1–F3 | 2.5 | E lift gap + arcade |
| ST+S1 / ST+S2 | stair (S rear), **Type B 6.0 × 10.6**, long axis Z (ST+S1 W wall thickened to X 57.0, wraps TC-S1) | **57..64 / 86..92** | **2.6..13.2** | F1–F3 | 2.7 | F1 free bays; F2 climbing; F3 S concourse, under the stand rake (≥3.4 m) |
| ST+N1 / ST+N2 | stair (N rear), Type B, long axis Z | 58..64 / 86..92 | **65.8..76.4** | F1–F3 | 2.7 | food court / gym / F3 N concourse |
| ST+E | stair (E terrace), Type B, long axis Z | 119.5..125.5 | **50..60.6** | F1–F3 | 2.7 | arcade / E terrace (TC-E2 1.5 m clear) |
| ST-AQS / ST-AQN | stair (W foyer, inner side), Type B, long axis Z | **−6..0** | **10..20.6 / 58.4..69** | F1–F3 | 2.7 | foyer / gallery ends; moved off the façade so the 42 m of W doors stay |
| ST-ARS / ST-ARN | stair (E façade), Type B, long axis Z | 134..140 | **10..20.6 / 58.4..69** | F1–F3 | 2.7 | arcade, by the SE/NE plant |
| Lift S / N | 2 cars | 66.5..70.5 | 11..15 / 64..68 | F1–F3 | — | concourse via 10 m gap |
| Lift W / E | 2 cars | 26..30 / 113..117 | 34.5..38.5 | F1–F3 | — | concourse via 10 m gap |
| TC-S1..S4 | tree column | 57.5, 65.5, 84.5, 101.5 | 8.5 | grade–roof | — | S1 inside the ST+S1 W wall; S2 free-standing clad in the F2 climbing lobby (F1: free bay); S3 climbable pillar in the F2 kids' wall E face (F1: axe target wall); S4 tree boulder / axe target wall |
| TC-N1..N4 | tree column | 57.5, 65.5, 84.5, 101.5 | 70.5 | grade–roof | — | food court / gym |
| TC-W1 / W2 | tree column | 23.5 | 30.5 / 48.5 | F3–roof | — | **on transfer trusses T-W4 / T-W6** |
| TC-E1 / E2 | tree column | 119.5 | 30.5 / 48.5 | grade–roof | — | arcade |
| T-W1..T-W9 | transfer truss 2.5 m | 0..30 | 3.5, 12.5 … 75.5 | F2/F3 | — | over aquatic hall; bear on X 0 and X 30 columns |
| Façade columns | perimeter | X −12, 140 / Z 0, 79 | **8 m c/c** (Rev 2.5; §3.11.1) | grade–roof | — | Glass Box edges, no cantilevers |
| PT columns | 0.9 × 0.9 | 39.5..103.5 @ 8 | 24.5 / 54.5 | F1–F3 | — | concourse inner edge |
| **Rev 2.4 additions** | | | | | | |
| V-CL | F3 slab void (climbing) | 35..57 | 3..8 | F2–F3 | — | trimmers on Z 3 / Z 8 (§3.7.1) |
| W-CL | climbing wall | 36..56 | 8..9.1 | +6.1 → +17.6 | 20 m | F2 belay floor |
| R1-S / R1-NW / R1-NE | WC block | 102..113 / 30..44 / 102..113 | 0..15 / 64..79 / 64..79 | F1 | — | §3.10 |
| R2-NW / R2-NE | WC block | 30..44 / 102..113 | 64..79 | F2 | — | §3.10 |
| R3-S1/S2/N1/N2 | WC under stand | 36..66.5 / 76.5..107 | 9.1..15 / 64..69.9 | F3 | — | §3.10 |
| TRK | track loop 1.8 m | 0.7..127.6 | 0.7..78.4 | F3 | 1.8 | §3.9 |
| BAR / PLAY / CAB | F3 | 8..20 / 128.3..140 / −11..−7 | 35..44 / 17..62 / 18..62 | F3 | — | §3.9 |

**Strip coordinates (Rev 2.4):** add 60 to any X above (x = 60 + X); Z → z = −40 + Z is unchanged, so the plinth (§3.3) is unchanged.

## 5. Circulation and egress (IBC 2021, sprinklered, *real-world ref*; Vance proposal)
### 5.1 Occupant load
Factors (IBC Table 1004.5): fixed seats as counted; unconcentrated assembly (food court, arcade, F3 dining/cabanas/lounges/playground) 1.39 m² net; standing at the bar and the climbing rail 0.46 m²; climbing gym and the F3 track 4.65 m² gross (exercise); exercise (gym), pool water, locker rooms 4.65 m² gross; pool decks 1.39 m²; standing (F2 viewing bridge) 0.46 m²; bowling 5 per lane; participants ~50–60 per floor. Inner concourse rings are seat circulation (not loaded).
| Floor | Seats | Band / terrace occupants | **Total** | Stair needed (5.1 mm/p) | Provided |
|---|---|---|---|---|---|
| F3 | 3,696 | track 720 m² → 155; cabanas/lounge 531 → 382; dining 1,130 → 835 (≈460 table seats fit); bar 121; playground 540 → 389; S/N lounges 1,380 → 993; other terrace 450 → 331 + 119; climbing rail 39; players 60 | **≈ 7,120** | **36.3 m** | **44.3 m ✓** (17 stairs, 22% margin) |
| F2 | 1,540 | gym 240, **climbing 1,245 m² gross → 268**, arcade 1,250, gallery 140, bridge 650, players 50 | **≈ 4,140** | 21.1 m | 44.3 m ✓ |
| F1 | 1,540 | food court 810, arcade 1,250, aquatic 1,130, foyer 510, bowling/axe 100, players 50 | **≈ 5,120** | doors 19.5 m (3.8 mm/p) | > 80 m ✓ |
- QA-04's F3 ~8,700 / F2 ~4,600 estimates agree within ~10% (the difference is the 10 m lift gaps and aisles, which remove 928 F3 seats).
- **Stairs: 17 full-height, 8 × 2.5 + 9 × 2.7 = 44.3 m.** Rev 2.4 margin **22% on F3** (was 12%): the track, dining tables and playground are lighter loads than open terrace. If the F3 open areas are ever cleared for standing events (0.46 m²), cap them at ~4,000 by signage (unchanged rule).
### 5.2 Distances (DQ-15)
- Travel (IBC A, sprinklered, 76 m; Vance 60 m to an axial route): Rev 2.4 worst F3 points: cabana at X −11, Z 40 → ST-AQS ≈ **25 m**; playground X 140, Z 40 → ST+E (gated crossing, Rev 2.6 at Z 50..56) ≈ 25 m, → ARS ≈ 24 m; climbing belay floor X 30, Z 5 → C-SW ≈ 17 m; bouldering X 113, Z 0 → ST+S2 ≈ 21 m; W terrace X 10, Z 26 → ST-AQS/LW ≈ 24 m; S rear concourse X 45 → C-SW ≈ 20 m; F1 lap deck → foyer doors ≈ 25 m. QA-04's 48–52 m terrace figure was against the Rev 2.2 14-stair set; all now ≤ 30 m ✓.
- **Rev 2.7 re-fit:** width unchanged at 44.3 m. Loads drop with the seats: F3 ≈ 6,830 → 34.8 m needed (27% margin); F2 ≈ 3,960 → 20.2 m; F1 ≈ 4,940. Travel: playground X 140, Z 40 → ARS (now ends Z 20.6) ≈ 20 m, → ARN ≈ 19 m; cabana X −11, Z 40 → ST-AQS (X −6..0, ends Z 20.6) ≈ 24 m; F2 bouldering X 113, Z 0 → ST+S2 ≈ 21 m; F1 lap deck → foyer doors ≈ 25 m. All ≤ 30 m ✓ (limit 76 m). The corner stairs now open onto the concourse directly at the stand ends. Common paths unchanged (≤ 15 m).
- Rev 2.6 ST+E move: E terrace worst point (X 120, Z 30) → LE ≈ 10 m, → ST+E ≈ 20 m; arcade (F1/F2) X 125, Z 40 → ST+E ≈ 10 m; all ≤ 30 m ✓; stair width unchanged (44.3 m).
- Common path (A: 23 m): the playground has 3 gates, worst common path ≈ 12 m ✓; the climbing belay floor opens at both ends (C-SW side and the S lobby), ≈ 14 m ✓. F2 gallery now has stairs at both ends (ST-AQS/ST-AQN, 47 m apart, plus the W lift/LW via the bridge), so the worst common path ≈ 15 m ✓ (DQ-07).
- Doc rule 2 exits per building (`strip4_plan.md` §6): exits on all 4 faces.
### 5.3 Main exit (DQ-05)
IBC §1030.2: the main exit must take ≥ ½ the building load. Rev 2.7: ½ × (4,940 + 3,960 + 6,830) × 3.8 mm = **29.9 m** ≤ 44 m ✓ (Rev 2.8 door run). Rev 2.4: ½ × 16,380 (F1 5,120 + F2 4,140 + F3 7,120) × 3.8 mm = **31.1 m**. W face doors **Z 18.5..60.5 = 42 m ✓** onto the +4.0 HD West Arrival terrace (a public way via the Fore cap portal, the Fore Hub Station Walk and the corner links to both loop arms).
### 5.4 Circulation
Lift → concourse → stands (front/radial/rear aisles); bands open off the rear aisles and outside; lift speed cap 1.0–1.6 m/s (Coriolis, §2.3).

## 6. Critical issues (Rev 2.4)
1. **Raised W/E terraces** (+4.0 HD) and the E Spine ramp (Jared OK). New: the W terrace depends on the **Fore cap portal level** (+4.0 HD wanted; fallback steps/lifts/switchback, §3.8).
1a. **Climbing void** in the F3 S-band slab needs trimmer beams (§3.7.1).
1b. Column clashes resolved in Rev 2.6 (§3.11.11).
2. **Glass Box:** 3.0 m deep space frame (4.0 m grid) column-free over 96 × 62 m; glare/heat gain, condensation control, cleaning gantry.
3. **W-band transfer trusses** (9 × 30 m span, 2.5 m deep) carry the F3 W terrace, stand overhang and 2 tree columns over the aquatic hall.
4. **Diving pit** 1.0 m below F1 in the deepest plinth zone (3.2–3.9 m of plinth): waterproof tank in fill; assumes no hull excavation (unverified).
5. **Egress margin 22% on F3** with the Rev 2.4 uses; a standing-event conversion must be capped (§5.1).
6. Corner-plant ducts run ~60 m to the far side of the hall.
7. Doc RPM values don't match R 200 (§2.1).
**Notes (not critical, per Jared):** F1/F2 clear heights (≈5.0/4.6 m), modified badminton/volleyball, shot drift, "not low gravity".

## 7. Open questions for Jared
Rev 2.3 questions answered (Rev 2.4): seats don't matter; terraces + ramps OK; F3 = lounge/dining/track/playground; F2 S band = climbing; 3 m + 1 m boards.
1. Fore cap portal: can the Fore Cap map put the Spine portal at +4.0 HD (level onto the terrace), or keep it at grade (steps + lifts + switchback)?
2. C5 Arena: deferred (Jared will revisit).

## 8. QA-04 + self-review resolution (Rev 2.3)
| Finding | Resolution | § |
|---|---|---|
| DQ-01 / B1 diving pit below hull | Plinth curve corrected (deepest at centre); well moved to Z 22..34 where p = 3.2–3.9 m; 1.0 m pit | 3.3, 3.6 |
| DQ-02 / B3 / M2 stairs + tree columns in programs | ST+S/N in free bays X 58..64.4 / 86..92.4; tree columns on walls/free bays; W trees on transfers; full table | 4.6 |
| DQ-03 / M1 lift stairs in stands | gaps 10 m, lift + stair side by side; seats recounted | 3.2 |
| DQ-04 / M4 occupant load | IBC 2021 sprinklered, bands + terraces; 17 stairs 44.3 m vs 39.7 m | 5.1 |
| DQ-05 main exit | 42 m of W doors ≥ 33.5 m; slide tube no longer crosses the lobby | 5.3, 3.6 |
| DQ-06 / M3 entrances above grade | curve reconciled (same function; deepest at centre); S/N at grade; W/E raised terraces + 1:20 ramps; plinth in section | 3.3, 3.8 |
| DQ-07 F2 gallery dead end | stairs ST-AQS/AQN at both ends + slide bridge | 3.6, 5.2 |
| DQ-08 slide tower in river | towers X 20..25, 1 m clear of the river | 3.6 |
| DQ-09 / B2 W-band grid | lines X −12/0/30 × 9 Z lines; 9 transfer trusses, soffit +9.7; no columns in water | 3.4 |
| DQ-10 coffer soffit | +11.8 | 3.4 |
| DQ-11 / m4 section | cut at X 60, plinth drawn, tags current | 4.5 |
| DQ-12 / M7 stale text | full rewrite; history to Appendix A | all |
| DQ-13 short-side seats | stated correctly (1,536 in Rev 2.2; 1,200 now) | 3.2 |
| DQ-14 ST+ coordinates | in table | 4.6 |
| DQ-15 travel incl. terraces | ≤ 30 m with façade stairs | 5.2 |
| DQ-16 radial aisles | 1.2 m every ≤ 7.5 m | 3.2 |
| DQ-17 corner cantilevers | perimeter façade columns 9 m + plant-stack corners, no cantilevers | 3.5 |
| DQ-18 slide "+4 m" | heights are inverts; no tube crosses a walk; crown ≤ +9.0 | 3.6 |
| DQ-19 x 400 Station Walk | restored to the S entrance | 3.8 |
| DQ-20 pool loads | table incl. tank slab (31.6 / 56.1 / 21.8 / 17.9 kPa) | 3.6 |
| DQ-21 concourse / PT column | 4.0 m, 3.1 m clear; 0.9 × 0.9 m at 8 m | 3.1, 3.4 |
| M5 slides along Z | runouts axial, tubes in island | 3.6 |
| M6 gallery over water | gallery over the foyer; water starts at X 1 | 3.6 |
| m1 stair margin | 12% after recount | 5.1 |
| m2 area | measured 0.93 ha | 3.8 |
| m3 entrance markers | S/N at the lift gaps (x 384.5..394.5), W centred | 3.8 |
| m5 F1/F2 missing trees/link | all columns, stairs and the bridge drawn on every PNG | PNGs |
| m6 recreation doc outdated | `recreation_slice_36deg_layout_v1.md` §8 C5 updated | — |
| m7 gap strips | N arm widened to 11 m; 0.5 m S apron paved | 3.8 |

## Appendix A. Superseded content (for the record)
### A.1 Revision history detail
- Rev 2.2: aquatic center with the diving well at Z 1..15 (wrongly assumed the plinth was deepest at the long faces), slide tube crossing the lobby at +4 m, F2 gallery over water, 6 m lift gaps with stairs in the F3 stands, 14 stairs / 36.2 m against a seats-only load (7.6 mm/p), 8,624 seats, x 400 Station Walk dropped.
- Rev 2.1: R4 Diagrid Lens roof (A.3). Rev 2.0: geodesic dome; 140 × 79 m footprint. Rev 1.1: 3 storeys, stands on F3. Rev 1.0: 4 storeys, 109 × 58 m.
### A.2 Footprint and stand derivations (Rev 2.0)
- Field lacrosse 110 × 55 → 186 × 104 m building > ~101 m usable strip width; rejected; box lacrosse sets 64 × 30.
- F1/F2 stands: rows at +0.9/1.3/1.7/2.1/2.5 → 5 rows in a 5.0 m clear storey with 2.5 m headroom; a 6th row would leave 2.1 m.
### A.3 F3 roof candidates (Rev 2.1, superseded by the Glass Box)
**Cover zone:** hall 64 × 30 m + concourse + 12-row stands on 4 sides = **X 23.5..119.5, Z 8.5..70.5 (96 × 62 m)**. Top stand row +17.6 m → roof edge ≥ +20.5 m. No wind, snow or rain in the drum (Vance assumption), so roofs carry self-weight, services and ball-impact only; netting under glazing contains balls.
| # | Candidate | Span / plan | Rise / height | Structure | Skyline read | Pros | Cons | Story flavor |
|---|---|---|---|---|---|---|---|---|
| R1 | **Hypar Saddle Shell** | 96 × 62, one hyperbolic paraboloid | high points over the short ends **+34 m**, low points over the long-side midpoints **+22 m** | steel gridshell (2 m grid) of straight members (hypar = ruled surface), edge ring beam, 4 corner thrust blocks on the plant-corner lines | a giant saddle; the curves echo the drum's curvature from across the cylinder | iconic, straight members, thrust to 4 points only | corner thrust blocks are large; ~7 m variable headroom over the long stands | "Poured by the first crews from sintered lunar regolith; the saddle is on every Hab-7 sports patch." |
| R2 | **Cable-Net Canopy on Masts** | 96 × 62 net, 4 raked masts outside the corners | masts **+45 m** (0.775 g at tip), membrane +21..+38 m | steel masts, pre-tensioned cable net, translucent ETFE/PTFE membrane, ball net below | 4 spikes reaching toward the axis; a tent | lightest, cheapest, no snow/wind so membranes thrive | mast backstays land in the walks/plaza; reads more festival than hard sci-fi | "Rigged by EVA crews with spare tether cable; Kade still tunes the cables before every final." |
| R3 | **Ribbed Barrel Vault with Glazed Lanterns** | vault spans **62 m across Z**, 96 m long along X | spring +20.5 m, crown **+38.5 m** (rise 18 m) | 13 steel box ribs at 8 m, tie rods at spring, 3 glazed lantern strips along the crown | a drydock hangar laid along the drum axis; the vault arc crosses the drum's own arc | very buildable, regular, reuses shipyard (bldg_16) language | tallest bulk; tie rods cross over the stands; least unique | "Built from a decommissioned cargo-hangar kit; the rib numbers are still stencilled on." |
| **R4** | **Diagrid Lens (recommended)** | elliptical lens **100 × 66 m** over the 96 × 62 cover zone | edge **+20.5 m**, crown **+29.3 m** (rise 8.8 m, 0.853 g at crown) | 2-layer steel diagrid space truss, **3.0 m deep** (≈ span/21 on the 62 m short span), on **8 V-columns** at the stand backs; ETFE cushions + BLEND glass oculus over the courts; no horizontal thrust | a floating disc/lens, an "eye" looking up at the Sun-core from across the drum | covers court + all 4 stands, thrust-free (simple supports on the band), lowest bulk, short-side stands return | 3 m deep truss is heavy for a span; double-curved diagrid nodes are complex | "Ground like a telescope lens; at dusk-cycle the oculus focuses the Sun-core onto centre court." |
| R5 | **Iris / Petal Roof** | elliptical ring 96 × 62 m, 12 steel petals | ring +20.5 m, petal tips meet at **+26 m** closed | fixed perimeter ring truss (covers the stands) + 12 motorised petals on rail bogies (cover the courts); ball nets under the opening | an aperture that opens to the drum sky, like a camera iris | the most theatrical; opens for events | moving roof = drives, seals and maintenance; ball containment when open needs a net | "Opens only for the Remembrance Match, so the players are seen from every strip." |

**(Superseded) Rev 2.1 recommendation: R4 Diagrid Lens.** It covers the court and all four stands, has no thrust into the 2-floor band, brings the short-side stands back (+2,084 seats), sits lowest in the skyline (crown +29.3 m), and its oculus gives the building a single story beat. R5 Iris is the story alternative if Jared wants an opening roof.
- Gravity notes: crown heights give 0.853 g (R4) to 0.775 g (R2 mast tips). Coriolis: a ball or tool dropped from the R4 crown (17.1 m above the court) lands ~0.3 m spinward of plumb (physics, (2/3)ω√(2h³/g)), so hang scoreboards on the lens centre line.


**Rev 2.9 (Jared via Rook):** programme furnishings (gym, arcade, bowling, etc.) reuse existing shared game assets where they fit; bespoke otherwise. Kiosks moved to X 0 wall, see-saws turned to rock along Z, benches moved outside the W fence, Fore cap portal fixed at +4.0 HD.

**Rev 3.0 (blockout d7a72f2 conflicts, Vance calls):**
1. Playground benches move inside the W fence as 4 fence-mounted perch seats (1.8 × 0.3 m, X 128.3..128.6, centres Z 25/33/41/46). The accessible path becomes X 128.6..129.8 (1.2 m clear, ≥ 0.915 m min). Nothing goes into the track's outer lane.
2. The slide bridge lands at the gallery door Z 56..58.4, as in the blockout. Bridge neck centred on the door; ST-AQN is untouched.
3. Confirmed: omit the 3 pool-hall columns at X30/Z39.5, X0/Z12.5 and X0/Z66.5. Core walls carry the load; truss T-W5 bears on a 0.6 m pilaster thickening in the LW wall.
4. Bowling acoustic wall: no separate wall where it overlaps ST+S1. The acoustic lining (50 mm panels) is applied to the core's W face; the free-standing wall runs only where there's no core.
5. Accepted: the F3 slab is cut back to Z 9.1, with a 1.07 m guard on the new slab edge.
6. Accepted: cutouts in the 4 corner roof tiles for the plant stacks (to +28), each with a 0.3 m flashing collar.
7. New asset: `tt_roof_ridge_12`, a 12 m ridge cap for the X 128–140 strip, using the same profile as the main ridge.

**Rev 3.1 (climbing band edges, raised by temp-Active):**
1. **ST+S1 (X 57..64) and ST+S2 (X 86..92), both at Z 2.6..13.2, stay where they are.** They split the F2 band into zones: lead hall X 30..57, entry lobby + kids' wall X 64..86, and bouldering hall X 94..113. A **1.8 m clear spine at Z 13.2..15** runs X 30..94 behind both cores and links the zones. No climbing wall, mat or prop goes on a core face or in the spine. Climbing faces stay on X 30..56, the X 84.5 kids' face, and the bouldering hall.
2. **Bouldering hall (X 94..113, Z 0..15):** the 19 m wall is the hall's **N wall, on Z 15, X 94..113**. It is 4.5 m high, its overhang reaches down to Z 13.5, and the mats run Z 9..15 under it. The X 94 training wall is cut to **13 m, Z 0..13** (10 panels + 0.25 m trim). That leaves a **2 m hall entry at X 94, Z 13..15** at the spine's E end. The spine stops at X 94; inside the hall, Z 9..15 is mats only. The X 113 wall stays 15 m. TC-S4 at X 101.5 stays a free-standing tree boulder, with its own 2 m mat ring.

**Rev 3.2 (F1 leisure rooms, raised by temp-Leisure; Vance proposal unless noted):**
1. **Axes:** Godot Y-up. Building X = Godot +X (axial), building Z = Godot +Z (across), heights = +Y above F1. Each asset's "front" is as stated in its own spec line (e.g. the §3.12.4 desks face −X).
2. **Axe throwing:** bays are **3.4 m wide** (across Z), not 3.7 m. Four bays take Z 0.3..13.9 including 0.1 m partitions, with a 0.3 m frame zone at Z 0..0.3 and a **1.1 m spectator/aisle strip at Z 13.9..15**. The acoustic lining goes on the target walls and partitions. Throw length (7 m along X) is unchanged.
3. **Food court (N band, Z 64..79):**
   - **Vendors:** 6 stalls, each 6 × 5 m including its kitchen, against the N façade at Z 74..79: 4 at X 30..54 and 2 at X 66..78. ST+N1 (X 58..64) and ST+N2 (X 86..92) stay clear.
   - **Seating:** about 300 seats on the open floor at Z 64..74 and X 78..113, between the cores. At least 5% of seats are accessible, with 0.9 m clear routes between tables.
   - **Accessible counters:** every stall has a counter section at least 0.9 m long and 0.86 m high.
   - **Waste:** out through a service door in the N façade at X 54..57, onto the N arm at grade.
   - **F3 dining service:** carts go up lift W.
4. **Arcade (E band, L1 + L2):**
   - **Cabinet mix per floor:** about 40% video cabinets, 20% redemption games, 10% claw/prize machines, 10% sit-down racers, 6 air-hockey tables, a 4-machine pinball row and 4 VR pods.
   - **Prize counter:** on L1, beside ST+E.
   - **Feature stair:** an open 2.5 m-wide stair from L1 to L2 at X 126..139, Z 38..40.5, with a mid landing. It is decorative and not counted for egress.
5. **Bowling (X 30..57):** keep 8 lanes across Z 0.6..15 (4 pairs at 3.6 m = 14.4 m). Because the sports are story decoration (Jared), lanes run 17 m to the head pin. In X that gives a 2.4 m settee and scoring zone at X 30..32.4, the 4.6 m approach at X 32.4..37, the lane to the head pin at X 54, and the pin deck at X 54..57. The pinsetters' machinery is in the SE plant stack.


**Rev 3.3 (temp-Arrival):** the N kiosk group is split 2 + 2 around the existing N-deck doorway on the X 0 wall (Z 45..47, `build_structure.py:63`). The kiosks are at Z 42.65..44.4 and 47.15..48.9, X −0.7..0. The doorway and the aquarium corridor mouth stay clear. Door leaves must not swing into the foyer within Z 47..47.15.

**Rev 3.4 (supersedes the Rev 3.3 kiosk ranges):** all 8 kiosks are given as Z centres; see §3.12.4. Rule: kiosk footprints (±0.3 m) stay ≥ 0.075 m off the X 0 piers (AQ_Z ± 0.3: Z 30.2..30.8, 48.2..48.8), the aquarium mouth (Z 34.5..42.5), the N-deck door (Z 45..47) and its 0.15 m no-swing strip (Z 47..47.15). The piers stay as built, with no notching. Footprints: 30.875..34.1, 42.575..44.925, 47.375..47.975.

**Rev 3.5 (accessible routes; Vance proposal, approved by Jared 2026-11-10, raised by Rook from Patch QA at 10deb61):**
1. **Rule:** every public floor or deck is reached step-free by a ramp of 1:12 or flatter (each run rises 0.76 m at most and is 9 m long at most, with 1.5 m level landings at the top, bottom and turns, 1.2 m clear between handrails, handrails on both sides, and a 1.07 m guard wherever the drop is over 0.76 m) or by a lift stop. Slide towers and the slide start decks (+7.0) are stairs only, because slide platforms are exempt. The 1:20 Spine ramp and terrace rules (§3.12.5) still apply outside.
2. **Datums (measured in the build):** F1 is 0. The pool deck is **+2.0** (+1.92 is the diving-tank water surface, not a floor). The leisure hall deck is **+1.0** (X 0.32..29.68, Z 44.8..78.68). The F2 gallery, slide bridge and T2 −X gate are **level at +6.1**. +6.75 is the underside of the T1–T2 link deck, not a walking surface, so there is no gallery step.
3. **Pool deck switchback (F1 to +2.0):**
   - Cut the deck fill in an L shape: X 4..10.5 at Z 22..31, plus a passage at X 4..6.25, Z 31..34.5.
   - Make a 1.5 m opening in the Z 34.5 lobby wall at X 4.5..6. A level F1 passage runs from it to the bottom landing at X 4.25..5.75, Z 29.5..31.
   - Four legs run along Z, each 6 m long and 1.5 m wide, rising 0.5 m at 1:12:
     - L1 at X 4.25..5.75, from Z 29.5 (0) to Z 23.5 (+0.5).
     - L2 at X 5.75..7.25, from Z 23.5 back to Z 29.5 (+1.0).
     - L3 at X 7.25..8.75, from Z 29.5 to Z 23.5 (+1.5).
     - L4 at X 8.75..10.25, from Z 23.5 to Z 29.5 (+2.0).
   - Turning landings: at Z 22..23.5 (+0.5 for L1→L2, +1.5 for L3→L4) and at Z 29.5..31 (+1.0 for L2→L3, beside the F1 bottom landing, with a guard between them).
   - The top landing is at X 8.75..10.5, Z 29.5..31 (+2.0). It exits +X onto the deck at X 10.5..15, which is clear of the diving well (X 15..28, Z 22..34).
   - A 1.07 m guard runs on the deck edge around the whole cut. The lap pool tank (Z ≤ 21.5) keeps a 0.5 m wall to the cut.
4. **Leisure hall ramp (F1 to +1.0), on the S strip:**
   - The N-deck door (X 0 wall, Z 45..47) opens onto an F1 bottom landing at X 0.3..1.8, Z 44.8..47.0, covering the full door width. It is guarded where it meets the +1.0 deck and the river wall.
   - The ramp runs +X at Z 44.8..46.3 (1.2 m clear): a 6 m leg at X 1.8..7.8 (to +0.5), a 1.5 m landing at X 7.8..9.3, then a 6 m leg at X 9.3..15.3 (to +1.0). It joins the deck at X 15.3.
   - A 1.07 m guard runs on the +Z side along the drop.
   - The +1.0 deck fill and the `tt_leisure_deck` finish are cut at X 0.3..15.3, Z 44.8..47.0 under the landing and Z 44.8..46.3 under the legs.
   - The aquarium tank bays (to Z 44.5) stay 0.3 m clear, and the Rev 3.4 kiosk (Z 44.325..44.925, foyer side) is unaffected.
5. **Island footbridges:** the river water drops to **+0.85** (0.85 m deep). Both footbridges become **flush at +1.0** with a 0.1 m deck (underside +0.9, 0.05 m over the water), so there is no step at either end. The N bridge stays at X 8..10, Z 71.85..75.15. The **S bridge moves to X 18..20** (Z about 46.85..50.15), clear of the S-strip ramp.
6. **Owners:**
   - Rook builds the cuts, ramps, landings, guards and the Z 34.5 wall opening.
   - temp-Aquatics does the river level, the footbridges, and the `tt_leisure_deck` / `tt_pool_deck_finish` trims.
   - Columns on the S strip are checked during the build.

**Rev 3.6 (supersedes Rev 3.5 item 3 and the footbridge spans in item 5; raised by temp-Aquatics at d76e318).** The Rev 3.5 cut swallowed the 3 m board stair (X 7.56..12.6, Z 24.5..25.5), so the switchback is turned to run along X, north of the board. The boards stay as specified in §3.6.
1. **Cut:** X 1.0..10.0, Z 26.0..32.0, plus a passage at X 8.5..10.0, Z 32.0..34.5. It stays ≥ 0.5 m clear of the 3 m board stair. The 1 m board stairs at Z 28.5 / 31.5 must stay at X ≥ 10.05; temp-Aquatics to confirm.
2. **Entry:** a 1.5 m opening in the Z 34.5 lobby wall at X 8.5..10.0. A level F1 passage runs from it to the bottom landing at X 8.5..10.0, Z 30.5..32.0.
3. **Legs:** each is 6 m long along X (X 2.5..8.5), 1.5 m wide and rises 0.5 m at 1:12:
   - L1 at Z 30.5..32.0 runs −X to +0.5.
   - L2 at Z 29.0..30.5 runs +X to +1.0.
   - L3 at Z 27.5..29.0 runs −X to +1.5.
   - L4 at Z 26.0..27.5 runs +X to +2.0.
4. **Landings:** turning landings at X 1.0..2.5, Z 29.0..32.0 (+0.5) and Z 26.0..29.0 (+1.5), and at X 8.5..10.0, Z 27.5..30.5 (+1.0, guarded from the F1 bottom landing next to it). The top landing is at X 8.5..10.0, Z 26.0..27.5 (+2.0). It exits +X onto the deck along Z 26.0..27.5, 0.5 m north of the 3 m board stair.
5. **Guards:** 1.07 m on the deck edge around the whole cut and between landings at different levels.
6. **Footbridges:** each spans only the channel, S at Z 47.0..50.0 and N at Z 72.0..75.0. They bear flush on the +1.0 deck edges, so no recesses are cut. The S bridge is at X 18..20 and the N bridge at X 8..10. The other Rev 3.5 terms are unchanged.

**Rev 3.7: QA access, gates and guards (TTQA)** (2026-11-15, Vance; answers `context/TT_QA_AUDIT.md`, TTQA-001/002/007/008/009/010/011/021/022/023/024/029/031/035/048). All layout calls here are **Vance proposal** under the Rev 3.5 access rules: ramps ≤ 1:12, each run ≤ 0.76 m rise and ≤ 9 m long, 1.5 m landings, 1.8 m clear on exterior ramps, 1.07 m guards with < 100 mm openings wherever the drop is > 0.76 m, stairs riser ≤ 0.18 and tread ≥ 0.28. Sports stay decoration (Jared). Reuse shared assets (edge/skirt opening variants, `tt_stand_module_6p5`, `tt_struct_void_guard`, rink board modules).
- **Ownership:** Rook builds every new piece in the GLBs with `*-colonly` (trimesh) / `*-convcolonly` (convex) colliders that match the visuals, and adds the manifest rows (`tower_drop.py`). Room-owned assets (temp-Active, Leisure, temp-Aquatics, Courts, temp-Arrival) are swapped by their owners at the coordinates given. Gage owns runtime: drum gravity, water volumes and swim, ladder climb areas, and door behaviour.
- **Drum floor:** level along X, `y(Z) = 195.9592 − √(40000 − (Z − 40)²)` (building frame; −2.34 at Z 14, −4.04 at Z 39.5). Probe values vary by about ±0.12 m, so Rook ray-probes every foot and landing and sets each one on the probed top within ±0.005. All terrace ramps run along X, so their slope lines up with drum gravity; the cross-fall where they meet the drum (Z 8.3..12.5) is 7.5–9°. Gage's gravity volume must cover every ramp and stair footprint below.
- **Clash rules applied to every footprint** (3d-part-clipping-check, game-first-pass-check): overlap ≤ 0.010 m, ≥ 0.02 m clear for free-standing parts, drops > 0.5 m guarded, 2.1 m headroom, ≥ 0.9 m clear aisles. Each item says which existing pieces it touches. Anything not listed was box-checked against the audit placements and is clear.

1. **W terrace (TTQA-001/002): two switchback ramps plus a grand stair.**
   - **SW ramp** sits outside the S skirt and runs along X with solid fill underneath. It has handrails both sides and 1.07 m guards on every open side.
     - Lanes: N cheek/guard Z 12.3..12.5 (0.10 m off the skirt base at Z 12.6); lane A clear Z 10.5..12.3; median guard Z 10.25..10.5; lane B clear Z 8.45..10.25; S guard Z 8.3..8.45.
     - Total rise 1.678 m (drum −1.537..−1.816 under lane B), split into 3 runs of 0.559 m over 6.71 m (1:12).
     - Top landing **X −27.0..−25.0, Z 10.25..13.5, y 0.00.** The terrace edge module 793 (X −28..−24) becomes the opening variant, clear X −27..−25 through Z 13.5..16.01, and skirt 795 is notched for the landing.
     - Run 1 descends −X in lane A from X −27.0 to −33.71 (to −0.56). Intermediate landing X −33.71..−35.21 (−0.56). Run 2 continues from X −35.21 to −41.92 (to −1.12).
     - Turn landing X −41.92..−43.42, Z 8.3..12.5 (−1.12), spanning both lanes.
     - Run 3 climbs back +X in lane B from X −41.92 to −35.21 (to −1.68). Foot landing X −35.21..−33.71 on the drum, exiting +X onto the drum. Its last 1.0 m is warped to the drum cross-fall (±0.14 m).
     - The median guard runs the full length X −43.42..−25.0, because lane B and the drum sit up to 2.4 m below lane A. The S guard runs X −43.42..−35.21; handrails extend 0.3 m past the foot.
     - **Footprint X −43.42..−25.0, Z 8.3..13.5.** It touches only skirts 779–795 (the lanes stay at Z ≤ 12.5, 0.10 m clear) and module 793/795 at the landing (opening variants). It is 4.56 m clear of the Fore Hub Station Walk (X ≤ −48) and 1.0 m clear of the SW corner link (X ≥ −24).
   - **NW ramp:** the SW ramp mirrored about Z 40, at the same X values and levels.
     - Lanes: cheek Z 67.5..67.7; lane A Z 67.7..69.5; median Z 69.5..69.75; lane B Z 69.75..71.55; guard Z 71.55..71.7.
     - Top landing X −27..−25, Z 66.5..69.75. Edge module 794 gets the opening variant (clear X −27..−25) and skirt 796 is notched.
     - Footprint X −43.42..−25.0, Z 66.5..71.7. Same clearances as SW (NW corner link X ≥ −24).
   - **W grand stair** on the axis:
     - 6.0 m clear at Z 36.5..42.5. Cheek/guard walls at Z 36.3..36.5 and 42.5..42.7, plus a centre handrail on Z 39.5.
     - Rise 4.03 m (drum −4.010..−4.040) in 23 risers of 0.1752 on 0.30 treads.
     - Top landing X −63.5..−60.0 at y 0, through openings in edge modules 747/749 (Z 36.5..42.5) and notches in skirts 748/750.
     - Flight 1: 12 risers, X −63.5 → −66.8 (to −2.10). Landing X −66.8..−68.8. Flight 2: 11 risers, X −68.8 → −71.8 (to −4.03).
     - Foot clear zone X −71.8..−73.8. Solid fill under, closed sides.
     - **Clash:** the stair sits inside the §3.8 Fore cap portal reservation (X −60, Z 34..46). It is valid only while the drop leaves drum floor west of X −62.5 (69.5 m today). If the portal is built, the stair is redesigned with it.

2. **E plaza (TTQA-001/002): one switchback ramp plus one stair.**
   - **E ramp:** same lanes, Z values and levels as the SW ramp, mirrored in X.
     - Top landing **X 153.0..155.0, Z 10.25..13.5.** Edge module 929 (X 152..156) gets the opening variant (clear X 153..155) and skirt 931 is notched.
     - Run 1 goes +X from 155.0 to 161.71. Landing 161.71..163.21. Run 2 goes from 163.21 to 169.92. Turn landing 169.92..171.42.
     - Run 3 comes back −X from 169.92 to 163.21. Foot landing 163.21..161.71, exiting −X onto the drum.
     - **Footprint X 153.0..171.42, Z 8.3..13.5.** It is 1.0 m clear of the SE corner link (X ≤ 152) and clear of the x 200 Station Walk (X 134..146, Z < 0).
     - **Open check:** the plaza corner X 168..171.4, Z 12.6..16 has no skirt piece (cf. TTQA-043). The ramp, at Z ≤ 12.5, clears it, but Rook should close that gap.
   - **E stair** to the E door (X 140.98, Z 37.5):
     - Clear Z 36.5..39.5, through an opening in edge module 903 and a notch in skirt 904. Cheeks at Z 36.3..36.5 and 39.5..39.7.
     - Top landing X 168.0..171.5. Flight 1: 12 risers, X 171.5 → 174.8. Landing 174.8..176.3. Flight 2: 11 risers, X 176.3 → 179.3. Foot zone X 179.3..181.3.
     - 23 × 0.1752 risers on 0.30 treads.
     - **Clash:** it overlaps the unbuilt East Spine ramp reservation (X 170..250, Z 34..46). Revisit if the Spine is built.
   - **Interim match (Gage):** Gage's interim runtime ramps go at exactly the item 1–2 footprints and levels (SW, NW and E ramps), so the final GLB pieces replace them one for one. Stairs are not needed in the interim.

3. **Rink (TTQA-007).** The boards are temp-Active placements: S Z 26.18..26.58, N Z 52.42..52.82, ends X 41.18..41.58 / 102.42..102.82.
   - **Players' gates:**
     - Replace `tt_rink_board_gate` 1739 (X 65.5..67.5) with a 2.0 m module that has 1.2 m clear at **X 65.9..67.1** and 0.4 m fixed panels. Its leaf is parked open at 180° against the concourse face of the next board panel, projecting ≤ 0.1 m.
     - Vance proposal: do the same at 1751 for the second bench (clear **X 76.9..78.1**).
     - Both open onto the N concourse (Z 52.82..59.25) between the PT columns at X 63.5 / 71.5 / 79.5 (Z 54.05..54.95), facing the N lift gap X 66.5..76.5 (lift 985, stair LN a_958). The existing leaves carry a static closed collider (0.976 m), which goes away.
   - **Zamboni gate:**
     - Replace boards 1777 + 1779 (X 102.42..102.82, Z 34.5..38.5) with one 4.0 m double-leaf module, opening **Z 34.85..37.85** (2 × 1.5 m leaves parked flat against boards 1775/1781).
     - Service route: E concourse X 102.82..108.25 → the gap between the E stands (Z 34.48..44.51) → corridor Z 34.5..39.0 between stand 1649 and stair a_962 (4.5 m) → lift E 991 (X 113.38..116.63, Z 34.5..38.5).
     - **Clash:** goal 1846 (X 98.35..99.49, Z 37.9..41.1) is 0.05 m N of the opening line. Leave it as is; the story says goals are lifted off for resurfacing.

4. **Axe throwing (TTQA-008).** The bays are Leisure assets; the walls are Rook's `walls_f1`.
   - **Deviation from the brief:** the spectator rails 1146/1154 (Z 13.85..14.75) back onto the dead Z 15 wall (Z 14.7..15.0) and only touch the N bay, so a gate in them would lead nowhere. They stay closed.
   - **Clash (Rook/Leisure):** the rail overlaps the wall by 0.05 m. Trim the rail to Z ≤ 14.68.
   - **Row 1** (X 77.2..84.0; throw lines X 79.25 / 80.52, target face X 84.0):
     - 1.0 m gates in the X 77 wall (X 76.85..77.15) at **Z 4.9..5.9** (bay 1140) and **Z 8.3..9.3** (bay 1141), entered from the S lobby. Stair core a_955 starts at Z 9.5, X 71..76.5, so the approach stays clear.
     - Bay 1142 gets a 1.0 m gate in partition 1145 at **X 77.4..78.4**, 0.85 m behind the far throw line.
     - The existing bay 1139 opening (Z 2..4.5) stays.
   - **Row 2** (X 94.2..101):
     - 1.0 m gates in the X 93.85 wall (X 93.7..94.0) at **Z 4.9..5.9, 8.3..9.3 and 11.7..12.7** (bays 1148/1149/1150), entered from the corridor strip X 92.0..93.7 beside core b_965. Each gate is ≥ 0.9 m from the partitions and 2.4 m behind the throw lines (X 96.25 / 97.52).
     - The existing bay 1147 opening (Z 0.6..2.5) stays.
   - **F1 concourse door:**
     - Courts replaces stands 1616 (X 84.01..91.48) and 1618 (X 91.51..98.98) with `tt_stand_module_6p5` at **X 84.01..90.48 and X 92.51..98.98**. That leaves a gap of X 90.48..92.51 with end-cheek guards, 1.83 m clear.
     - Rook puts a 1.8 m pair door at **X 90.6..92.4** in the existing Z 15 opening (X 90..93) and infills the rest.
     - The PT columns at X 87.5 / 95.5 (Z 24.05..24.95) are clear.
   - **F2 climbing pocket:** Vance proposal, replacing a second stand cut. Restore the Rev 3.1 spine.
     - Rook cuts the X 84.5 kids'-wall backing wall at **Z 13.2..14.7 (1.5 m clear, 2.2 m high)**. The kids' panels end at Z 12.95 and the mats at Z 13.1, so the cut clears both.
     - That links the S entry lobby (reached through the N lift gap / S cores) along Z 13.2..14.7 behind b_cap_966 to the bouldering entry at X 94.
     - The dead F2 Z 15 opening X 86.3..89 (behind stand 1640) is infilled.

5. **Pools (TTQA-009/010).** temp-Aquatics handles the deck-finish trims and placements. Gage handles water volumes, swim, and a climb Area3D on every ladder; the stairs are the guaranteed walk-out without swim.
   - **Lap tank** (X 2.5..27.5, Z 0.5..21.5; floor +0.04; deck +2.0):
     - **Deviations:** the S long side has no deck (Z 0.32..0.5 to the façade), so it gets no ladder. The W end has start blocks across Z 1.87..20.13, so the stair goes at the E end.
     - Recessed stair in an E-deck alcove at **X 27.5..29.6, Z 0.5..3.8**, rising +Z: bottom at Z 0.5..1.0 on the tank floor, then 11 risers of 0.178 and 10 treads of 0.28 over Z 1.0..3.8, exiting onto the E deck. Handrails on both sides.
     - The alcove trims deck finishes b/c/d. Column X 30, Z 3.5 (X 29.7..30.3) is 0.1 m clear, and the façade bays end at Z 0.62.
     - Ladders:
       - N side at **X 12.5, Z 21.5**, exiting onto the N deck (3 m board edge at Z 24.49);
       - W end at **X 2.5, Z 20.8** (N of the blocks);
       - E end at **X 27.5, Z 19.5** (lifeguard chair Z 11.5..12.66).
     - Every water point is within 21 m of an exit (limit 23 m).
   - **Diving well** (X 15..28, Z 22..34; pit −2.5):
     - **Deviation:** the boards are on the W side, and the N (0.2 m deck) and S (0.5 m strip) sides are unusable. The stair goes against the E wall.
     - In-tank stair **X 26.6..28.0**:
       - flight 1 from Z 33.7 rising −Z: 13 risers × 0.18 to Z 30.34 (y −0.16);
       - landing Z 30.34..29.14;
       - flight 2: 12 risers to Z 26.06 (+2.0);
       - top landing Z 26.06..24.56, exiting +X onto the E deck (X 28..29.68).
       - The stair is ≥ 9 m from the board tips.
     - Ladders at **Z 23.0** on the E wall (X 28.0) and on the W wall (X 15.0), the W one exiting onto the deck at X 13.5..15, 1.5 m from the 3 m board edge.
   - **Lazy river** (floor 0.0, water +0.85, deck +1.0):
     - **Deviation:** 4 steps would need a 0.19 m riser, over the 0.18 limit. Each entry is 6 risers × 0.16 and 5 treads × 0.28 (1.4 m projection), 1.2 m clear plus rails, perpendicular to the bank.
     - Positions:
       - S outer **X 21.0..22.4, Z 47.0→48.4**;
       - S island **X 15.6..17.0, Z 50.0→48.6**;
       - N outer **X 10.6..12.0, Z 75.0→73.6**;
       - N island **X 6.0..7.4, Z 72.0→73.4**.
     - Each pair straddles its footbridge (S X 18..20, N X 8..10) and leaves ≥ 1.6 m of channel open. They clear the S-strip ramp (X ≤ 15.6), T1 (X ≥ 19.9) and the mounds (Z ≥ 76.17).
   - **Runout exit** (Vance proposal, TTQA-010): stair along the W end wall at **X 5.0..6.4**, rising +Z with 6 × 0.16 risers over Z 69.6..70.99, onto the island strip Z 71..72.
   - **Splash pad:** zero-depth. Raise the basin floor from +0.40 to **+0.98**, remove the splash hole from the +1.0 deck, and raise the sprays by 0.58 (temp-Aquatics). Gage: no water volume, spray VFX only.

6. **F3 track guards (TTQA-011/048).** The track runs at track_sn Z 0.7..2.5.
   - **Deviation from the brief:** the b_cap top landing is at the N end (Z 10.26..13.0), under the F3 stand, whose back is at Z 9.07, not on the track side. So the track side is fully guarded and the painted crossing is dropped.
   - **ST+S1 hole (X 57..64, Z 2.6..10.26):**
     - 1.07 m glass guard on **Z 2.50..2.58, X 57.06..64.0**, joining the existing `tt_struct_void_guard` (X 34.94..57.06);
     - E guard **X 64.0..64.1, Z 2.58..9.0**;
     - the W side is the thickened core wall around TC-S1 (X 57.05..57.95, Z 8.05..8.95, inside the hole);
     - N side: the stand back. Rook confirms it is solid to the floor; otherwise add a guard on Z 9.0.
     - Raise Well_Guard_F2 to 1.07 m over the flight-1 well at the top landing, with a cross guard along Z 10.26 over X 57.0..61.0 and open at the flight-2 arrival X 61.1..63.8.
   - **ST+S2 hole (X 86..92):**
     - S guard **Z 2.50..2.58, X 85.9..92.1**;
     - W guard **X 85.9..86.0** and E guard **X 92.0..92.1**, both Z 2.58..9.0;
     - well cross guard Z 10.26, X 86.2..88.9, with the arrival open at X 89.1..91.8;
     - TC-S3 is 0.95 m clear.

7. **Slab openings (TTQA-011).**
   - F2 core openings are closed by the core walls (TTQA-004 colliders). Lift openings are closed by the shaft walls and landing doors (TTQA-003).
   - Each F3 core top gets a 1.07 m guard ring on the wall heads, plus a cross guard over flight 1 that is open at the arrival:
     - **LS a_956:** S Z 9.5..9.7; W X 71.0..71.2 and E X 76.3..76.5 (Z 9.5..16.97); cross Z 16.97 over X 71.2..73.7; arrival X 73.8..76.3.
     - **LN a_958:** S Z 59.3..59.5; W/E as LS over Z 59.3..66.77; cross Z 66.77 over X 71.2..73.7; arrival X 73.8..76.3.
     - **LW a_960 (yaw 90):** W X 24.5..24.7; S Z 39.0..39.2 and N Z 44.3..44.5 (X 24.5..31.97); cross along X 31.97 over Z 41.8..44.3; arrival Z 39.2..41.7.
     - **ST-ARN b_m_980:** top landing Z 58.6..61.34; W guard X 134.0..134.2, Z 61.34..69.01; cross Z 61.34 over X 134.2..136.9; arrival X 137.1..139.8; the E side is closed by the façade.
   - F2-ARC and F3-PLAY are this ARN core plus the NE plant stack, which item 10 closes.

8. **Gallery edge (TTQA-024):**
   - 1.07 m glass guard (< 100 mm openings) at **Z 68.70..68.80, X −11.80..−6.10**, on the `tt_gallery_floor` N edge.
   - It has a 1.2 m gap at **X −8.7..−7.5**, where the 0.22 m gap to the plant-stack face is infilled at Z 68.80..69.02 for the item 10 staff door.
   - The showers end at Z 66.88, so the guard is clear. It touches façade bay 577 (X ≤ −11.38) at its W end.
   - **Also found:** a 0.2 m slot under the non-colliding partition at X −6.1..−5.9. Rook adds a wall collider there. The ST-AQN edge at Z 58.4 is TTQA-004.

9. **Plinth fill (TTQA-021):**
   - Fill top **−0.403** under X −12..140, Z 0..79 (the F1 slab underside); **−0.313** under the terraces.
   - Diving pit: the fill top drops to **−2.903** under the pit slab, with liner walls at **X 14.7..28.3, Z 21.7..34.3**.
   - Lift pits: recess the F1 slab top by 0.15 m, keeping 0.25 m of slab beneath, instead of letting the cores overlap the slab. Locations: S X 66.5..70.5, Z 11..15; N X 66.5..70.5, Z 64..68; W X 26..30, Z 34.5..38.5; E X 113..117, Z 34.5..38.5.
   - **Open:** check the fill outside the terraces separately.

10. **Plant stacks (TTQA-022):**
    - Close all four shells with convcolonly walls and lids: SW X −11.44..−0.02, Z 0.56..9.97; NW Z 69.02..78.43; SE / NE X 128.02..139.44.
    - Each stack gets one locked, static 1.0 m staff door per floor (F1 0, F2 6.1, F3 12.2):
      - **SW** at X −8.6..−7.6 on the Z 9.97 face. The F2 sill meets the gallery floor through a 0.23 m infill at Z 9.97..10.2, and the door is 0.6 m clear of changing (X ≤ −9.2).
      - **NW** at X −8.6..−7.6 on the Z 69.02 face.
      - **SE** at X 131.5..132.5 on the Z 9.97 face.
      - **NE** at X 131.5..132.5 on the Z 69.02 face, clear of arcade redemption 1185 (X ≤ 131.01) and 1279/1280 (X ≤ 128.16).

11. **Court size (TTQA-029):** won't fix. The courts stay 10 × 20 m and keep their name (decoration, Jared).

12. **W entrance bays (TTQA-031):**
    - **Deviation:** 4 leaves of 1.0 m don't fit the 3.864 m stile span, and 2 sliders per bay give only 22 m, under the §5.3 need of 29.9 m.
    - Each of the 11 bays gets **3 leaves × 1.0 m clear** at Zc −1.6..−0.6, −0.5..+0.5 and +0.6..+1.6 (0.10 m mullions), which gives **33.0 m ≥ 29.9 m ✓**.
    - Bollards: split the single colonly box (X −13.63..−13.47, Zc ± 1.08, 0.96 m high) into individual posts, Ø ≤ 0.15 at Zc ± 0.55, with ≥ 0.915 m clear between them.
    - Owners: Rook / temp-Arrival for the pieces, Gage for the proximity doors.

13. **Under-flight pockets (TTQA-035):**
    - The low-headroom nodes sit under the solid-cast flight-1 / mid-landing visuals, which have no colliders. Add convcolonly hulls matching the casts. Where a pocket is genuinely open, put a 0.9 m planter colonly at the 2.1 m headroom line.
    - Instances:
      - F1: a_947/949/951/953/955/957/959/961, b_963/965/967/969/971/973/977, b_m_975/979;
      - F2: a_948..962 (even), b_cap_964/966, b_968/970/972/974/978, b_m_976/980.
    - Flagged for Rook: 1,247 other F1 nodes under stands and decks have < 2.1 m headroom. Close each one with the stand or deck colliders.

14. **TTQA-048:** info only, covered by item 6.

15. **Slide bridges (TTQA-023, Vance proposal; missing from the decision list, added under the Rev 3.5 rule):** 1.07 m colonly guards with < 100 mm openings on every open edge of the F2 slide bridges and decks (X 20.5..24.5, Z 51.5..61.5, at +6.1 / +7.0). The only openings are the slide tube mouths.

### Rev 3.7.1, 2026-11-15 (Vance): build answers for Rev 3.7 (Rook's questions)
1. **SW/NW ramp median:** ends at X −41.92 so the turn landing (X −43.42..−41.92) stays full width. Accepted.
2. **Rink gate leaves (Vance proposal):** park the leaves opened 90° *into the rink*, perpendicular to the boards, on a floor stop beside the jamb. Don't lay them flat on the next board panel. Both the 1.2 m players' gates and the 4.0 m Zamboni pair work this way, and each leaf gets its own convcolonly.
3. **Axe gate X 77.4..78.4:** move bay 1142's rack +X until there is ≥1.0 m clear in front of the gate. If the rack can't move without entering the throw zone, shift the gate −X along partition 1145 to get the same clearance.
4. **Axe throw-line datum:** measure from the **target face at X 83.2** (row 2 likewise from its target face), not from the wall at X 84. Rook's measured lines are correct.
5. **Ramp feet:** replace the 1 m warp with a **level 1.5 m foot landing** set at the mean probed drum height. Blend the drum into its open sides with a terrain fillet no steeper than 1:20 (colonly), so no edge is steeper than 1:20 and no lip exceeds 13 mm.
6. **Confirmed:** the added guard at X 57.03, the gallery guard starting at X −11.36, and the ST+S1 cross guard starting at X 59.36.
7. **Plaza corner X 168..171.4, Z 12.6..16:** don't add an overlapping piece. Trim the existing E/S terrace skirts to a mitred meet, with no overlap and no slit, and close the joint with a 0.2 m corner post (convcolonly). The same detail fixes TTQA-043.
8. **Still to build:** the 0.15 m lift-pit recesses (#9), the pool stairs and ladders (#5), the W bay leaves and bollards (#12), and the slide-bridge guards (#15). The F3 stand-back guards on Z 9.0 are accepted.

### Rev 3.8, 2026-11-15 (Vance): r2 QA items (`context/TT_QA_AUDIT_r2.md`)
All layout calls below are **Vance proposal** under the Rev 3.5 rules (1.8 m clear links, 1.07 m guards with < 100 mm openings, 2.1 m headroom). Every footprint was box-checked against the r2 placements (audit clone at `03de15a`) plus the Rook commits since (pools, ramps, skirts, rink leaves, court doors, grand-stair colliders), none of which touch these footprints. Clash rule: overlap ≤ 0.010 m, ≥ 0.02 m free-standing clearance. The only hits listed below are the pieces this revision removes or swaps. Owners follow Rev 3.7: Rook builds GLB pieces with `*-colonly` / `*-convcolonly` plus manifest rows, room owners swap their own assets, and Gage owns runtime (doors, step-up).

1. **TTQA-050, bowling entrances (blocker).**
   - **Why the lanes change:** the hall X 30..57, Z 0.3..14.7 is filled edge to edge by 4 lane pairs, X 32.4..56.9 (8 lanes). The only non-lane floor is the settee strip at X 30..32.4, and core a_961 sits right behind it (X 29.99..40.2, Z 15..20.5). A door anywhere on the Z 15 wall therefore lands on a lane bed (the foul line is at X 37.02).
   - **Fix (Vance proposal, Leisure):** remove lane pair **1150** (Z 11.05..14.65) and settee **1151**, leaving **6 lanes**. That frees an entry aisle at **X 30.0..56.9, Z 11.16..14.70** (3.54 m), which opens at its W end onto the bowlers' area and approaches (X 30..37), behind the foul line.
   - **Divider:** Rook adds a 1.07 m colonly divider rail at **Z 11.06..11.16, X 37.0..56.9**, 0.01 m off lane pair 1148 and meeting the acoustic wall 1152. It keeps players off the lanes past the foul line.
   - **Main door:**
     - Courts removes stand **3p8_1620** (X 40.22..43.99), giving gap A at X 40.20..44.01. Courts also swaps stand **1622** for `tt_stand_module_6p5` at X 44.01..50.48.
     - Rook adds a stand-end cheek guard at X 43.91..44.01 (1.07 m over the rake) and cuts a new **1.8 m pair-door opening in Walls_F1 line Z 15 (Z 14.70..15.00) at X 40.35..42.15**, 2.4 m high.
     - The door is 0.15 m clear of the a_961 E wall (X 40.20). It opens from the S concourse (Z ≥ 19.76) through gap A into the aisle.
   - **Second exit:**
     - Courts swaps stand **1624** for `tt_stand_module_6p5` at X 52.51..58.98, giving gap B at X 50.48..52.51. Rook adds cheeks at X 50.48..50.58 and 52.41..52.51 (1.83 m clear).
     - The existing **Walls_F1 Z 15 opening X 50..53 becomes a 1.8 m pair-door opening at X 50.6..52.4**, 2.4 m high, with infill at X 50.0..50.6 and 52.4..53.0.
   - **Doors:** both are built like the Rev 3.7 #4 door (frame, no leaf collider; Gage may add proximity leaves). They are 10.25 m apart, which meets the 1/3-diagonal rule (30.6 m / 3 = 10.2 m, *real-world ref*).
   - **Clearances:** both doors are clear of b977 (X ≥ 58) and of the pin-end masking (X ≥ ~54.6 on the remaining pairs). The PT column at X 39.5, Z 24.5 is outside gap A. Headroom is to the F2 slab underside at 5.70.
   - **Open (Jared):** this takes the house from 8 lanes to 6. No layout keeps 8 lanes without moving core a_961 or the X 30 wall.

2. **TTQA-051, F2 slot beside b977 (blocker): infill (Vance proposal, Rook).**
   - **Cause:** the F2 `CORE_HOLES` entry for ST+S1 is the nominal X 57..64. The as-built core b977 is X 58.00..64.00, Z 2.60..13.21; the Rev 2.6 thickened W wall was never built.
   - **Fix:** make the F2 hole for ST+S1 **X 58.00..64.00, Z 2.60..13.21**, which infills **X 57.00..58.00, Z 2.60..13.21** at y 5.70..6.10 (butting the core W wall face, overlap ≤ 0.005).
   - **TC-S1 tree hole:** trim it (now X 56.8..58.2, Z 7.8..9.2) to **0.02 m off the trunk faces** (trunk about X 57.05..57.95, Z 8.05..8.95; Rook probes the as-built faces at y 5.7..6.1). That closes the 0.25 m ring the probe dropped through at X 56.5, Z 7.5..9.0.
   - **Checks:**
     - The acoustic wall 1152 (X 56.90..57.00, top 5.54) is 0.16 m below the infill underside.
     - The acoustic stubs (X 57..58, Z 0.3..2.6 / 13.2..14.7, top 5.71) touch only the infill ends (≤ 0.01).
     - F2 climbing pieces are ≥ 0.75 m away (lead routes to X 56.0, frame to X 56.15, lockers to X 56.3).
   - **F3:** no change. The F3 slot stays guarded at X 57.03 (Rev 3.7.1 #6).
   - A guard isn't needed because the drop is removed.

3. **TTQA-053, zone links (major).** Two F1 links and two F2 links between the S-door zone and the W/N/E zone, each at a point where the r2 grid has the two zones ≤ 1.5 m apart across one wall.
   - **L1-N, F1 concourse ↔ food court:**
     - Courts swaps stands **1631 / 1633** for `tt_stand_module_6p5` at **X 84.01..90.48 and X 92.51..98.98**, giving gap X 90.48..92.51. Rook adds cheeks (1.83 m clear).
     - The **Walls_F1 Z 64 opening X 90..93 becomes a 1.8 m pair-door opening at X 90.6..92.4**, 2.4 m high, with infill on the rest.
     - On the food side the door meets the strip Z 64.3..65.79 (b983 at X 86..92 is 1.49 m N) and the passage **X 92.0..94.0** to stall 1174 (2.0 m).
     - Optional: Leisure moves bin 1186 (X 86..87.2), which pinches the W strip to 0.63 m.
     - This mirrors the Rev 3.7 #4 axe door.
   - **L2-N, F2 concourse ↔ gym:**
     - Courts swaps stands **1655 / 1657** the same way (X 84.01..90.48 / 92.51..98.98). Rook converts the **Walls_F2 Z 64 opening X 90..93 to a pair-door opening at X 90.6..92.4** (F2 + 2.4).
     - temp-Active moves treadmills **2116–2119 +0.9 m in X** (to X 94.0..98.4, Z 65.05..67.16; the floor there is clear) to open the passage **X 92.0..94.0**.
   - **L1-E, F1 concourse ↔ arcade:**
     - Courts swaps **6p5_1639** (Z 28.01..34.48) for `tt_stand_module_3p8` at **Z 28.01..31.78** (X 108.25..112.56, yaw −90). Rook adds a cheek at Z 31.78..31.88 over X 108.25..113.0, which also closes the dead pocket behind the stand.
     - The gap Z 31.88..34.48 joins the lift-E corridor. Rook cuts a new **1.8 m pair-door opening in Walls_F1 line X 113 (X 113.0..113.3) at Z 32.4..34.2**, 2.4 m high.
     - It is 0.30 m S of lift E (X 113.38..116.63, Z 34.5..38.5) and 4.8 m from the TC-E1 trunk.
   - **L2-E, F2 concourse ↔ arcade L2:** the same detail with **6p5_1663 → 3p8 at Z 28.01..31.78** and a **Walls_F2 X 113 opening at Z 32.4..34.2** (F2 + 2.4). Arcade video 1324 (to Z 31.96, X ≥ 116.22) is clear.
   - **Rejected:**
     - W side: the aquarium corridor's E end is fully closed by lift W and LW at every floor.
     - F2 X 113 at Z 0..15: the bouldering mats fill the approach, and only a 1.0 m strip is free.
     - Z 64 X 50..53: food stalls 1172/1173 stand in front of it.

4. **TTQA-011 remainder, NE plant opening F2-ARC / F3-PLAY (blocker): guards (Vance proposal, Rook).**
   - The r2 drop edges run on the slab edge of the NE `PLANT_HOLES` cut (X 128..140, Z 69..79) along its W side (X 128.0) and S side (Z 69.0), so the stack shell collides only at its door module.
   - At **F2 (+6.1) and F3 (+12.2)**, 1.07 m colonly guards with < 100 mm openings, on the slab and 0.02 m off the stack faces (X 128.02 / Z 69.02):
     - **W guard X 127.90..128.00, Z 69.00..78.38**, ending on the façade-bay inner face;
     - **S guard Z 68.90..69.00, X 127.90..134.00**, ending on core b_m 993/994 (F2) and the Rev 3.7 #7 ARN ring guard X 134.0..134.2 (F3).
   - **Gap:** one gap at **X 131.25..133.24** in front of the staff-door module (Z 69.19..69.39). The slab is infilled at Z 69.00..69.19 under that span, so the locked door is reachable and no slot is left.
   - **Stair side:** no public stair lands in this opening. The ST-ARN portals and arrival face Z 58.4 / Z 61.34 and stay open as built, so nothing else is left open.
   - **Clearances:** F3 track (X ≤ 127.60, corner Z 75.34..78.34) 0.30 m; F2 redemption 1293/1294 (Z ≤ 67.75) 1.15 m.
   - **Also for Rook:** the NE stack's W and S shell faces should get the same convcolonly as SW/SE (Rev 3.7 #10). The guards stay either way.

5. **TTQA-052, grand-stair snags (major, Rook): smooth ramp colliders.**
   - The stepped tread collider is replaced by straight colonly ramps whose top passes through the nosing line (≤ 0.01 m), full clear width, meeting the cheek walls. The landings are flat and the visual treads are unchanged, the same scheme as the cores' `Flight*_Ramp`. Slope 2.102 / 3.60 = **30.3°**.
   - **W stair** (Z 36.5..42.5):
     - ramp 1 X −63.50 (y 0) → −67.10 (−2.102);
     - landing X −67.10..−68.80 (−2.102);
     - ramp 2 X −68.80 → −72.10 (−4.030), onto the pad X −71.80..−73.80.
   - **E stair** (Z 36.5..39.5):
     - ramp 1 X 171.50 → 175.10;
     - landing X 175.10..176.30;
     - ramp 2 X 176.30 → 179.60, onto the pad X 179.30..181.30.
   - Centre-rail posts (W) keep their own colliders.
   - **Status:** built in `921ef1b`. Gage confirms the player's `floor_max_angle` is ≥ 35° and that step-up doesn't fight the ramp. r3 re-walks lanes Z 37–42 (W) and Z 38.5 / 39.0 (E).

6. **Already answered:**
   - **TTQA-055:** rink gate leaves, Rev 3.7.1 #2 (parked 90° into the rink on floor stops, own convcolonly). Built in `f216e2f`, after r2.
   - **TTQA-009:** pool exits, Rev 3.7 #5. Built in `a7e7d35`, after the r2 snapshot (`03de15a`), so r2 couldn't see them. Gage still owns the ladder climb areas and swim. Both go to r3 for verification.

### Rev 3.8.1, 2026-11-15 (Vance): Rook build confirmations
- **Accepted as built:**
  - The TTQA-011 infill stops at Z 69.148, where the plant grating starts at 69.15.
  - The existing shell on the NE stack already closes its W face (X 128.34) and S face (Z 69.14).
  - Per-core guard exceptions where the F3 stands overhang the X 61/89 cores to Z 67.05, and where the aisle plate of stand 1704 laps core 984 to X 91.75.
  - The TC-S1 trunk probe extent is X 56.90..58.10, Z 7.90..9.10.
  - Stand swaps were placed by coordinates, not by manifest index.
- **TTQA-026, climbing hook rails (Vance proposal):** don't add a partition at Z 13.2, because the spine must stay clear. Move the 7 hook rails onto the solid wall faces of the locker bays and snap them to the face, with the rail at about 1.4 m above F2.
- **TTQA-039, gallery relief (Vance proposal):** don't mount it in open space. Move it to the nearest solid gallery wall face. If no wall is within 3 m, stand it on a freestanding 0.3 m-deep plinth wall (convcolonly), parallel to the gallery edge and leaving at least 1.8 m clear walkway.
- **TTQA-050, bowling:** held for Jared's call (6 lanes or keep 8).
