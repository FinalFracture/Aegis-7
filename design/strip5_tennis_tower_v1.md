# Strip 5 "The Green" — Multi-Sport Tower — Structure & Floor Plans

**Status:** DRAFT **Rev 2.4**, 2026-11-03 (Vance). Physical structure and floor plans only: no props, no builds, no code.
**Labels:** *(doc)* = value from a cited repo doc; *(physics)* = derived from doc values; *(real-world ref)* = outside practice (IBC 2021, FINA, etc.), not a project constraint; **Vance proposal** = my design call.
**Plan PNGs** (not committed, renders rule): `/workspace/renders/tennis_tower/F1.png, F2.png, F3.png, section.png, site_plan.png`.
**Coordinates:** building local X (axial, along strip x) and Z (across, along strip z), origin at the SW corner; **strip x = 60 + X, z = −40 + Z** (Rev 2.4; was 318 + X). Heights in the building are **above F1 (F1 = 0)**; site heights are **HD = above the hull floor at the strip centreline (z 0)**. **F1 = +4.0 HD** (§3.3).

## 0. Revision log
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

### 3.3 Plinth and grade (DQ-06, M3)
- The hull floor rises toward the strip edges: height above the centreline **h(z) = z²/(2R) = z²/400** *(physics, R 200 doc)*. The building floor is flat, so the plinth under F1 is **p = F1 − h**.
- F1 must clear the highest hull point under the footprint, the S face (z −40, h 4.00), so **F1 = +4.0 HD** and **p(Z) = 4.0 − (Z − 40)²/400** (Z = building local).
  - Rev 2.2's p(Z) = 3.9 − (Z − 39.5)²/400 and QA-04's 3.9 − (39.5 − Z)²/400 are **the same function** (the square makes the sign irrelevant); both centre on the building, not the strip, and are ~0.1 m low. The correct reading: **the plinth is deepest (4.0 m) at the centreline, Z 40, and zero at the long S/N faces**, because the floor curves *up* to meet the building there. Rev 2.2 had this backwards ("deepest at the long faces").
  - Values: Z 0 → 0.00; Z 10 → 1.75; Z 22 → 3.19; Z 34 → 3.91; Z 40 → 4.00; Z 79 → 0.20.
- **Consequence:** the S and N faces are **at grade** (Rim Promenade z −45 is +5.1 HD, N arm z 45 is +5.1: 1:12 aprons over ~1 m). The **W and E faces are 4.0 m above the centreline plazas**: QA-04's level problem is real but it sits on the W/E faces, not S/N.
- **Fix (Vance proposal, Jared OK Rev 2.4):** the West Arrival terrace and East Plaza are **raised terraces at +4.0 HD** (structural deck on fill over the hull, 1.4–4.0 m), so the W and E entrances are level. Rev 2.4: the W terrace is fed directly by the Fore cap portal (§3.8), so there is no W ramp; the Spine leaves the East Plaza on a **1:20 ramp** (80 m, x 230..310). The Fore Hub Station Walk descends from the stop tower foot (z −56, +7.8 HD) to the terrace (+4.0) by steps + a 1:12 switchback ramp inside its 12 m width.
- **Main entrance = W face** (level terrace, 42 m of doors, §5.3); secondary entrances S (x 100 Station Walk side, at grade), N (at grade) and E (terrace).
- Plinth drawn in `section.png`.

### 3.4 Long spans and columns (DQ-09, DQ-21)
- **F2 rink column-free:** the F3 floor spans 30 m across Z on **post-tensioned band beams, 1.5 m zone** → F2 clear ≈ 4.6 m. **PT columns 0.9 × 0.9 m** at 8 m centres on the play-area edge lines Z 24.5 / 54.5 (X 39.5..103.5, 9 per side), padded, inside the concourse (clear width 3.1 m past them).
- **F1:** columns also in the runoff between the 4 court boxes (14 × 26 m grid, 1.1 m floor zone) → F1 clear ≈ 5.0 m.
- **Bands (S/N/E):** one-way 15 m (S/N) and 27 m (E, with a line at X 126.5) slabs between façade columns (9 m centres) and the stand-back line; **no columns in the bowling lanes** (X 30..57 spans Z 0..15 in one).
- **W band (aquatic), Rev 2.3:**
  - Column lines **X −12 (façade), X 0 (foyer/water edge) and X 30 (stand back)**, at **Z 3.5, 12.5, 21.5, 30.5, 39.5, 48.5, 57.5, 66.5, 75.5** (9 m). No column stands in water: every water body lies in X 1..29.
  - **9 transfer trusses**, one per Z line, span **30 m (X 0..30)** over the aquatic hall, **2.5 m deep**, top chord at F3 (+12.2), **soffit +9.7**. They carry the F3 W terrace, the W stand overhang (X 24.1..30) and the 2 W tree columns.
  - **Coffer over the diving well (DQ-10):** between the Z 21.5 and Z 30.5 trusses the F3 slab drops to a 0.4 m coffered plate, **soffit +11.8**, giving 9.8 m above the diving deck (+2.0).
  - Foyer bay X −12..0 spans 12 m on a 0.6 m slab (the F2 gallery floor) at +6.1.

### 3.5 F3 Glass Box (Jared Rev 2.2; dimensions and structure Vance proposal)
**Structure (Vance proposal):**
- **Roof:** two-way **square-on-square steel space frame**, 3.0 × 3.0 m grid, 3.0 m deep, CHS members with bolted ball nodes. **Column-free over 96 × 62 m** (the hall, concourse and all 4 stands, X 23.5..119.5, Z 8.5..70.5): depth 3.0 m on the 62 m short span = span/21 ✓ for a two-way frame with light glazing loads (no wind, rain or snow in the drum, Vance assumption).
- **Supports (Rev 2.3, DQ-02/DQ-17):** 12 tree columns at the stand backs (coordinates §4.6) carry the inner 96 × 62 field. Outside it the frame is **continuous to perimeter façade columns at 9 m centres on all four faces plus the 4 plant-stack corners** (concrete shafts take the box corners), so there are **no cantilevers**: the largest bay outside the field is 9 × 12 m (W terrace) on a 3.0 m two-way frame.
- **Walls:** steel fin mullions, **600 mm deep, at 3.0 m centres** (matching the roof grid), horizontal transoms at 3.325 m (4 panes over 13.3 m); fins double as façade columns every 9 m (heavier fins).
- **Glazing module:** 3.0 × 3.325 m wall panes, 3.0 × 3.0 m roof panes (one per grid bay).
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
| **W foyer (main entrance hall)** | −12..0 | 10..69 | 12 × 59 | — | F1; doors along the W face Z 18.5..60.5 (**42 m**); ticketing, F2 gallery above |
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
| Front desk / gear rental | 58..66.5 | 9..15 | 51 m² | beside ST+S1 |
| Entry lobby | 66.5..76.5 | 0..9.5 | — | from lift S / LS |
| Kids' wall + auto-belays (5 m walls) | 77..85.5 | 0..15 | 128 m² | |
| Training (spray / hang boards) | 85..94 | 9..15 | 54 m² | behind ST+S2 |
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
- **Spine at the Fore cap (Vance proposal, needs a Fore Cap map tie):** the cap portal (x 0, z −6..6) lands **level at +4.0 HD** on the terrace. If the Fore Cap map fixes the portal at grade (0 HD), the fallback is grand steps + 2 lifts + a 1:12 switchback ramp (48 m in 4 legs) inside the terrace's W 12 m; an 80 m 1:20 ramp does not fit between the cap and the building.
- **Follow-up (not in this commit):** `recreation_slice_36deg_layout_v1.md` §8 C5 still shows the tower in the middle third. The parks + Dome move from the Fore third to x 310..568; the Aft River (x 530 inlet) is unaffected.

### 3.9 F3 open areas (Jared Rev 2.4; layout Vance proposal)
| Element | X | Z | Size | Note |
|---|---|---|---|---|
| **Running track** | loop X 0.7..127.6, Z 0.7..78.4 | — | **1.8 m wide (2 lanes), ≈400 m centreline lap** | 0.7 m off the glass (clears the 600 mm fins); inboard of the 4 plant corners; painted crossings at every stair landing. S/N straights are axial (zero Coriolis); on the W/E straights a 4 m/s runner gets ±0.18 g (spinward "heavy leg", antispinward "light leg"), story beat |
| **Dining terrace (tables)** | 3.5..23 | 4..33 and 46..75 | 2 × 565 m², ≈230 seats each | over the aquatic transfers; served from the F1 food court via lift W |
| **Cabanas** | −11..−7 | 18..62 | **8 cabanas, 4 × 4 m**, 1.5 m apart | along the W glass, looking out at the Fore cap |
| Lounge / view walk | −7..−0.7 | 16..63 | 6.3 m wide | between cabanas and track |
| **Small bar** | 8..20 | 35..44 | 12 × 9 = 108 m², ~14 m counter, ~20 stools | opposite the LW / lift W landing |
| **Kids' playground** | 128.3..140 | 17..62 | **12 × 45 = 530 m²**, fenced 1.2 m | **fits**, on the E terrace outside the track between ARS and ARN; 3 gates (S end → ARS, N end → ARN, gated track crossing → ST+E); swings and slides axial (no Coriolis twist) |
| Climbing void + glass rail | 35..57 | 3..8 | 110 m² | view down to F2 (§3.7.1) |
| S / N rear concourse lounges | 3..125 | 2.5..9.1 / 69.9..76.5 | ≈650 / 730 m² net | |
| Restrooms under the stands | §3.10 | | | |

### 3.10 Restrooms (Jared Rev 2.4: every floor; IBC 2021 Table 2902.1 A-4, *real-world ref*; layout Vance proposal)
Rule: occupants 50/50; WC male 1/75 for the first 1,500 then 1/120, female 1/40 for the first 1,520 then 1/60; lavatories male 1/200, female 1/150; drinking fountains 1/1,000; up to 67% of male WCs may be urinals. Plus **2 all-gender accessible/family rooms per floor**. Space allowance 5.5 m² per WC (incl. lavs and circulation). Aquatic changing rooms (F2 gallery) are extra.
| Floor | Occupants (§5.1) | WC M (≤ 67% urinals) | WC F | Lav M / F | Fountains | Need | Blocks (X, Z) | Provided |
|---|---|---|---|---|---|---|---|---|
| F1 | 5,120 | 29 | 56 | 13 / 18 | 6 | ≈470 m² | **R1-S** 102..113, 0..15 (165); **R1-NW** 30..44, 64..79 (210); **R1-NE** 102..113, 64..79 (165) | 540 m² ✓ |
| F2 | 4,138 | 25 | 48 | 11 / 14 | 5 | ≈400 m² | **R2-NW** 30..44, 64..79 (210); **R2-NE** 102..113, 64..79 (165); climbing changing WC 30..57, 10.5..15 (~60) | 435 m² ✓ |
| F3 | 7,120 | 38 | 72 | 18 / 24 | 8 | ≈605 m² | **4 blocks under the F3 stands** X 36..66.5 / 76.5..107, Z 9.1..15 (S) and 64..69.9 (N), headroom 2.6–5.4 m | 708 m² ✓ |
| **Total** | | **92** | **176** | **42 / 56** | **19** | | **268 WCs** | |
- Wet stacks line up at X 36..44 and X 102..107 (N) through all three floors; R1-S stands alone over the SE substation side.
- The R1-S block takes the free S-band bay X 102..113 behind the AXE 2 target wall; R1/R2-NW and NE take the ends of the food court and gym.

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
| C-SW / C-SE / C-NW / C-NE | stair (ring corner) | 30..35.5 / 107.5..113 | 15..20.5 / 58.5..64 | F1–F3 | 2.5 | stand-free ring corners |
| LS | stair beside S lift | 71..76.5 | 9.5..15 | F1–F3 | 2.5 | S entrance lobby / climbing lobby |
| LN | stair beside N lift | 71..76.5 | 64..69.5 | F1–F3 | 2.5 | food court / gym |
| LW | stair beside W lift | 24..30 | 39..44.5 | F1–F3 | 2.5 | lobby corridor end |
| LE | stair beside E lift | 113..119 | 39..44.5 | F1–F3 | 2.5 | arcade |
| ST+S1 / ST+S2 | stair (S rear) | 58..64.4 / 86..92.4 | 2.6..8.6 | F1–F3 | 2.7 | **free bays** X 58..66.5 / 85..94 |
| ST+N1 / ST+N2 | stair (N rear) | 58..64.4 / 86..92.4 | 70.4..76.4 | F1–F3 | 2.7 | food court / gym |
| ST+E | stair (E terrace) | 119.5..125.5 | 46..52 | F1–F3 | 2.7 | arcade |
| ST-AQS / ST-AQN | stair (W façade) | −12..−6 | 10..16 / 63..69 | F1–F3 | 2.7 | foyer / gallery ends |
| ST-ARS / ST-ARN | stair (E façade) | 134..140 | 10..16 / 63..69 | F1–F3 | 2.7 | arcade, by the SE/NE plant |
| Lift S / N | 2 cars | 66.5..70.5 | 11..15 / 64..68 | F1–F3 | — | concourse via 10 m gap |
| Lift W / E | 2 cars | 26..30 / 113..117 | 34.5..38.5 | F1–F3 | — | concourse via 10 m gap |
| TC-S1..S4 | tree column | 57.5, 65.5, 84.5, 101.5 | 8.5 | grade–roof | — | acoustic wall, free bay, axe target walls |
| TC-N1..N4 | tree column | 57.5, 65.5, 84.5, 101.5 | 70.5 | grade–roof | — | food court / gym |
| TC-W1 / W2 | tree column | 23.5 | 30.5 / 48.5 | F3–roof | — | **on transfer trusses T-W4 / T-W6** |
| TC-E1 / E2 | tree column | 119.5 | 30.5 / 48.5 | grade–roof | — | arcade |
| T-W1..T-W9 | transfer truss 2.5 m | 0..30 | 3.5, 12.5 … 75.5 | F2/F3 | — | over aquatic hall; bear on X 0 and X 30 columns |
| Façade columns | perimeter | X −12, 140 / Z 0, 79 | 9 m c/c | grade–roof | — | Glass Box edges, no cantilevers |
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
- Travel (IBC A, sprinklered, 76 m; Vance 60 m to an axial route): Rev 2.4 worst F3 points: cabana at X −11, Z 40 → ST-AQS ≈ **25 m**; playground X 140, Z 40 → ST+E (gated crossing) ≈ 21 m, → ARS ≈ 24 m; climbing belay floor X 30, Z 5 → C-SW ≈ 17 m; bouldering X 113, Z 0 → ST+S2 ≈ 21 m; W terrace X 10, Z 26 → ST-AQS/LW ≈ 24 m; S rear concourse X 45 → C-SW ≈ 20 m; F1 lap deck → foyer doors ≈ 25 m. QA-04's 48–52 m terrace figure was against the Rev 2.2 14-stair set; all now ≤ 30 m ✓.
- Common path (A: 23 m): the playground has 3 gates, worst common path ≈ 12 m ✓; the climbing belay floor opens at both ends (C-SW side and the S lobby), ≈ 14 m ✓. F2 gallery now has stairs at both ends (ST-AQS/ST-AQN, 47 m apart, plus the W lift/LW via the bridge), so the worst common path ≈ 15 m ✓ (DQ-07).
- Doc rule 2 exits per building (`strip4_plan.md` §6): exits on all 4 faces.
### 5.3 Main exit (DQ-05)
IBC §1030.2: the main exit must take ≥ ½ the building load: Rev 2.4: ½ × 16,380 (F1 5,120 + F2 4,140 + F3 7,120) × 3.8 mm = **31.1 m**. W face doors **Z 18.5..60.5 = 42 m ✓** onto the +4.0 HD West Arrival terrace (a public way via the Fore cap portal, the Fore Hub Station Walk and the corner links to both loop arms).
### 5.4 Circulation
Lift → concourse → stands (front/radial/rear aisles); bands open off the rear aisles and outside; lift speed cap 1.0–1.6 m/s (Coriolis, §2.3).

## 6. Critical issues (Rev 2.4)
1. **Raised W/E terraces** (+4.0 HD) and the E Spine ramp (Jared OK). New: the W terrace depends on the **Fore cap portal level** (+4.0 HD wanted; fallback steps/lifts/switchback, §3.8).
1a. **Climbing void** in the F3 S-band slab needs trimmer beams (§3.7.1).
1b. `recreation_slice_36deg_layout_v1.md` §8 C5 is out of date after the move.
2. **Glass Box:** 3.0 m space frame column-free over 96 × 62 m; glare/heat gain, condensation control, cleaning gantry.
3. **W-band transfer trusses** (9 × 30 m span, 2.5 m deep) carry the F3 W terrace, stand overhang and 2 tree columns over the aquatic hall.
4. **Diving pit** 1.0 m below F1 in the deepest plinth zone (3.2–3.9 m of plinth): waterproof tank in fill; assumes no hull excavation (unverified).
5. **Egress margin 22% on F3** with the Rev 2.4 uses; a standing-event conversion must be capped (§5.1).
6. Corner-plant ducts run ~60 m to the far side of the hall.
7. Doc RPM values don't match R 200 (§2.1).
**Notes (not critical, per Jared):** F1/F2 clear heights (≈5.0/4.6 m), modified badminton/volleyball, shot drift, "not low gravity".

## 7. Open questions for Jared
Rev 2.3 questions answered (Rev 2.4): seats don't matter; terraces + ramps OK; F3 = lounge/dining/track/playground; F2 S band = climbing; 3 m + 1 m boards.
1. Fore cap portal: can the Fore Cap map put the Spine portal at +4.0 HD (level onto the terrace), or keep it at grade (steps + lifts + switchback)?
2. Update the recreation doc C5 (parks + Dome move to the middle third)?
3. C5 Arena: deferred (Jared will revisit).

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
