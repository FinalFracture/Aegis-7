# Strip 5 "The Green" — Multi-Sport Tower (ex Spin Court Tennis Tower) — Structure & Floor Plans

**Status:** DRAFT **Rev 2.0**, 2026-11-02 (Vance). Physical structure and floor plans only: no props, no builds, no code.
**Labels:** *(doc)* = value from a cited repo doc; *(physics)* = derived from doc values; *(real-world ref)* = outside sports/building practice, not a project constraint; **Vance proposal** = my design call, not a constraint.
Plan PNGs (not committed, renders rule): `/workspace/renders/tennis_tower/F1.png, F2.png, F3.png, section.png`.

## 0. Revision log
- **Rev 2.0 (Jared, 2026-11-02):**
  - F1 = multi-use tennis courts (convertible to modified badminton, volleyball, pickleball) **with stands**.
  - F2 = soccer + lacrosse (shared/convertible) **with stands**.
  - F3 = basketball **with stands under a geodesic dome** (replaces the flat roof).
  - Every floor has its own stands, with a **concourse between the stands and the playing area**; **lifts land on the concourse, never inside stands**.
  - Band: **arcade swaps with axe throwing + bowling**, and axe + bowling share **one floor** (F1). The freed space (S band F2) is **TBD - options: esports/VR arena, bar & lounge, kids' play zone, pro shop & lockers**.
  - Kept: 20 ft (6.10 m) storeys, plant in the 4 corners, pool on both floors, food court with the gym above, glazed ("plexiglass") enclosure.
  - Consequence: the footprint grows from 109 × 58 m to **140 × 79 m** (§3.2).
- Rev 1.1 (Jared): 3 storeys, stands on F3 only, corner plant. Superseded by 2.0 where they conflict.
- Rev 1.0: 4 storeys of tennis, stands on F4.

## 1. Brief (Jared, as given; Rev 1.0 text, then Rev 2.0)
"A type of multi-tiered tennis court thing. Big, tall, open, 4 floors, each 20 feet tall, each with 4 courts, the top one has arena seating. A series of elevators on each side goes to all floors. Each floor encased in plexiglass. It's an adapted form of tennis, adjusted for the lower gravity. Think about how that may play and look, design around it. Under the seating stands for the top level (all 4 sides): 1 side is an arcade, it will have 2 floors. A short side will have other indoor competition/athletic style games, like axe throwing and bowling. On the other short side, it takes up the whole 2 floors, but it's a swimming pool. On the other long side, first floor is a food court. Second floor is a gym. Let's just work on this design for now. Think hard and critical. Floor plans first; physical structures, not prop placement."
- Rev 1.0: 4 floors × 20 ft = 6.10 m, 24.4 m tall. **Rev 1.1: 3 floors × 6.10 m = 18.3 m** (Jared).

- **Rev 2.0 (Jared):** "Let's have tennis on floor 1, with stands as well. They can be modified badminton, volleyball, and pickleball. Floor 2, let's have soccer and lacrosse, also with stands. Floor 3 will be basketball courts, with stands and a dome." Plus (via Atlas): concourse between stands and play; lifts land on the concourse; arcade ↔ axe/bowling swap, axe + bowling on one floor; freed space TBD.

## 2. Physics
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
| F3 dome spring (18.3 m) | 0.909 g | |
| Dome apex (33.4 m) | 0.834 g | |
So the top (F3) court is only ~6% lighter. Lob flight time t = 2v_up/g: a 10 m/s vertical lob takes 2.04 s on F1 and 2.17 s on F3 (+6.5%), apex 5.10 m vs 5.43 m. **The "lower gravity" feel only becomes big in the Chapter 1 crisis states (0.35G/0.12G, doc).** What *is* strong here is **Coriolis**, so I propose the adapted sport is built around Coriolis, with a small per-floor g ladder as a bonus (Vance proposal).

### 2.3 Coriolis (a = −2ω×v, ω along the drum axis)
- **Motion parallel to the axis (strip x): zero Coriolis.**
- **Spinward/antispinward motion (strip z):** radial force 2ωv. At 30 m/s that is 13.3 m/s², bigger than g: a spinward drive "falls" ~2.4× faster than an antispinward one. **Unplayable/unfair for a z-oriented court.**
- **Vertical motion (toward/away from axis):** sideways push, spinward when rising. A lob with v_up drifts sideways by Δ = (4/3)·ω·v_up³/g² (physics):
  - v_up 10 m/s on F1: **3.07 m** drift; on F3: 3.48 m.
  - 4 m-rise lob (fits a 5 m clear ceiling): 2.13 m on F1, 2.20 m on F3.
- Crosscourt component: 5 m/s across the court gives 2.2 m/s² (~0.23 g) radial change; spinward crosscourts dip, antispinward ones float.
- Lifts: a 2.5 m/s lift sees 2ωv = 1.1 m/s² (0.11 g) sideways; at 1.0 m/s it is 0.045 g (Vance proposal: cap lift speed at 1.0–1.6 m/s and use stiff guide rails).

### 2.4 Sport-by-sport consequences (Vance proposal unless marked)
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
| F3 | Basketball | 28 × 15 m (+2 m runoff) | **11.8 m at the court ends, 21.1 m under the apex** (FIBA min ~7 m ✓) | Dome solves the height problem on this floor only |

**Basketball Coriolis (physics, g = 0.939 on F3):** drift Δ = (4/3)ωv_up³/g². A free throw (v_up ≈ 5 m/s, flight ≈ 1.1 s) drifts **0.44 m** spinward, about one rim diameter (0.457 m *real-world ref*); a 3-pointer (v_up ≈ 6 m/s) drifts **0.75 m**. Players must aim off; both baskets sit on the axial line, so the drift is mirrored for the two teams and fair over two halves. This is the signature look of the floor.
**Axe throwing Coriolis:** a horizontal 8 m/s throw across the spin gets 2ωv = 3.5 m/s² (0.36 g) radial push, so **all axe lanes throw axially** (along x).
**Bowling:** lanes axial, so the rolling ball has no Coriolis hook (Rev 1.0).

## 3. Structural concept (Rev 2.0)
### 3.1 Per-floor hall
- Each floor's core is one **play area 64 × 30 m** (sized by the F2 rink + runoff), ringed by a **4 m concourse** (lifts land here), then **stands**, then the band (F1–F2) or the band roof (F3).
- Building local coordinates (m): origin at the SW corner, X along strip x (axial), Z along strip z.
| Element | X | Z | Size |
|---|---|---|---|
| Play area | 39.5..103.5 | 24.5..54.5 | 64 × 30 |
| Concourse ring (4 m) | 35.5..107.5 | 20.5..58.5 | 72 × 38 outer |
| F1/F2 stands ring (5.5 m) | 30..113 | 15..64 | 83 × 49 outer |
| W band: pool (F1–F2) | 0..30 | 0..79 | 30 × 79 |
| E band: **arcade (F1–F2)** | 113..140 | 0..79 | 27 × 79 |
| S band: **F1 bowling + axe**, **F2 TBD** | 30..113 | 0..15 | 83 × 15 |
| N band: F1 food court, F2 gym | 30..113 | 64..79 | 83 × 15 |
| Plant corners (F1–F3 stacks) | 0..12 / 128..140 | 0..10 / 69..79 | 4 × 12 × 10 m |
| **Overall footprint** | **0..140** | **0..79** | **140 × 79 m** (was 109 × 58) |

### 3.2 Footprint check (critical check 1)
- **Field lacrosse (110 × 55 m):** play + concourse + stands = 129 × 74 m; with the bands **186 × 104 m**. Strip 5 is 125.66 m wide *(doc)*; after the S4|5 station band (6 m), the Rim Promenade (9.5 m), the Rim Trail (6 m) and 1.5 m rib buffers each side (`recreation_slice_36deg_layout_v1.md` §3) only ~101 m is left, so **104 m does not fit**, the curve sag across 104 m is 6.8 m, and a 5 m ceiling can't take field-lacrosse lofted passes. **Rejected.**
- **Vance proposal: box lacrosse (~61 × 26 m rink, Jared's ~60 × 26) shared with arena soccer and futsal (40 × 20).** This sets the 64 × 30 m play area and the **140 × 79 m** minimum footprint.
- Strip fit: 79 m across z fits the program area (z −40..50, 90 m) → **place at strip x 306..446, z −40..39** (Vance proposal), next to the x 300 S4|5 stop *(doc)*. It still covers the Spine Walk (z −6..6) and the x 350 / 400 cross walks → divert the Spine around the N face (z 41..53) for x 300..450 (open question).
- Curve sag across 79 m: 79²/(8·200) = **3.9 m** *(physics)*, so the plinth steps up to ~3.9 m at the long faces (was 2.1 m).

### 3.3 Stands per floor in 20 ft storeys (critical check 2)
- Clear height in the stand zone ≈ 5.0 m (short-span band structure, 1.1 m floor zone).
- Spectators must see over people walking on the concourse in front, so the **front row is raised +0.9 m** behind a glass balustrade (Vance proposal). Risers 0.40 m, treads 0.85 m, top-row headroom ≥ 2.5 m:
  - rows at +0.9, 1.3, 1.7, 2.1, 2.5 → **5 rows within the storey**; the top row has 2.5 m headroom. Depth 5 × 0.85 + 1.2 m rear aisle ≈ 5.5 m.
  - A 6th row would need 2.1 m headroom (too low). **No double-height zones on F1/F2** (they would eat the band floors above); F3's stands rise under the dome instead.
- **F3 under the dome:** stands on the two long sides only, **12 rows** (0.45 m risers, top row +5.4 m) from z ±19 m off the hall centre line, rows clipped where the dome leaves < 2.5 m headroom. The short sides sit at the dome's edge, where the dome is too low for stands, so there are no short-side stands on F3.

### 3.4 Long spans
- **F2 must be column-free** over the 64 × 30 m rink, so the F3 floor spans 30 m across Z between columns at the play-area edge (in the concourse, padded).
  - Steel trusses (span/12 ≈ 2.4 m zone) → F2 clear 3.7 m (too low).
  - **Post-tensioned concrete band beams (~1.5 m zone, services run in the band, not over the rink) → F2 clear ≈ 4.6 m (recommended, Vance proposal).**
  - F2's low ceiling is the biggest sporting compromise in the building (§6).
- **F1** can keep columns in the runoff between its 4 court boxes (14 × 26 m grid, 1.1 m floor zone) → F1 clear ≈ 5.0 m. These columns carry the F2 floor.
- **F3** is spanned by the dome; its floor is the PT slab above.

### 3.5 Geodesic dome (critical check 3)
- **Plan:** circular, **D = 79 m** (the building width), centred on the hall (X 71.5, Z 39.5), bearing on a ring beam at the F3 wall top **+18.3 m**. It covers the play area (diagonal 70.6 m < 79 ✓) and the long-side stands; the four ring corners and the band roof outside the circle get a flat roof.
- **Section:** spherical cap rise **h = 15 m** (Vance proposal), sphere radius (a² + h²)/2h = **59.5 m**, apex **+33.4 m**. Clear above the F3 floor: **21.1 m at the centre, 11.8 m at the court ends (x ±32 m), 12.8 m over the top stand row at centre**.
- **Frame:** 8-frequency icosahedral geodesic grid (Vance proposal; struts ≈ 7–9 m) in steel nodes and struts, triangular **BLEND glass/polycarbonate** panels (Aegis-7 Standard, `context/vance-handoff-v3.md` §2), opaque panels toward the drum axis glare if needed.
- **Gravity:** 0.909 g at the spring line, **0.834 g at the apex** *(physics)*. Dome loads are self-weight only (no wind, no snow in the drum; *Vance assumption*), so the frame is light; the ring beam takes the outward thrust.
- **Coriolis notes:** nothing static changes; anything falling from the dome (maintenance, a dropped ball from 21 m) lands ~(2/3)ω√(2h³/g) ≈ 0.4 m spinward of the plumb point *(physics)*, so hang scoreboards and nets on the dome's centre line and offset drop zones.

### 3.6 Lifts, stairs and egress (critical check 4)
- **4 lift banks, one per side** (brief), 2 cars each = 8 cars, at the side midpoints: S X 69.5..73.5 / Z 11..15, N X 69.5..73.5 / Z 64..68, W X 26..30 / Z 37.5..41.5, E X 113..117 / Z 37.5..41.5. Each opens through a **6 m gap in the stands straight onto the concourse** (lifts never surface inside stands). Lift speed cap 1.0–1.6 m/s (Coriolis, Rev 1.0).
- **8 stairs, full height, 2.5 m each = 20 m**: 4 in the stand-free ring corners (X 30..35.5 / 107.5..113, Z 15..20.5 / 58.5..64; outside the dome circle on F3) + 4 beside the lift banks.
- Load (real-world ref ~7.6 mm of stair per person, sized on the worst floor): F3 2,620 seats → 19.9 m ✓; F1/F2 1,960 → 14.9 m ✓.
- Doc rule: 2 exits per building (`strip4_plan.md` §6). Worst travel from a seat to a stair ≈ 35 m, within the 60 m Vance proposal (`recreation_slice_36deg_layout_v1.md` §5). Ground exits on all 4 faces.

### 3.7 Pool, bowling, axe throwing, plant
- **Pool (W band, F1–F2):** 25 × 21 m, 2.0 m deep, tank on grade, deck +2.0 m (no-excavation assumption, unverified), load ≈ 32 kPa. The SW/NW plant corners serve it.
- **Bowling + axe on F1 (S band, X 30..113 × Z 0..15), on grade (best for impact):**
  - **Bowling:** 8 lanes along X, X 30..57 (19.16 m to the head pin + 4.6 m approach + ~3 m pin deck), Z 0.6..15.
  - **Axe:** 2 rows × 4 bays (3.7 × 7 m), throwing **+X axially** into isolated target walls at X 82..83 and X 101..102, Z 0.2..15; 1 m double-stud acoustic wall between bowling and axe at X 57..58 and toward the stands; lift lobby S at X 69.5..73.5 between them.
  - Stands above? No: the S band is behind the S stands at the same level, separated by the glazed stand back wall.
- **S band F2: TBD - options: esports/VR arena, bar & lounge, kids' play zone, pro shop & lockers** (Jared to choose; 83 × 15 m = 1,245 m² minus the lift bank).
- **Arcade (E band, F1–F2):** 27 × 79 m less the SE/NE plant corners ≈ 1,900 m² per floor.
- **Plant:** 4 corner stacks 12 × 10 m, F1–F3 (Rev 1.1, Jared), louvred tops. SW/NW pool; SE substation and bowling machines; NE AHUs, chillers and the dome smoke exhaust.

## 4. Floor-by-floor plans (Rev 2.0)
```
Z79 +--------+---------------------------------+---------+
    |PLANT NW|  N band: F1 FOOD COURT / F2 GYM |PLANT NE |
Z64 |        +==== STANDS (5 rows) ============+         |
    |  W     |# +--- CONCOURSE 4 m ---------+ #|  E      |
    |  POOL  |S |  PLAY AREA 64 x 30        | S|  ARCADE |
    |  F1-F2 |T |  F1 4 courts / F2 rink /  | T|  F1-F2  |
    |  L=W   |N |  F3 2 basketball          | N|  L=E    |
Z15 |        +==== STANDS (5 rows) ============+         |
    |PLANT SW| S band: F1 BOWLING+AXE / F2 TBD |PLANT SE |
Z0  +--------+---------------------------------+---------+
    X0      X30                               X113      X140
 # = stair in ring corner; L = lift bank (S/N at X 69.5..73.5) opening onto the concourse.
 F3: dome D 79 m over the hall; stands N and S only (12 rows); band roof elsewhere.
```
| Floor | Height (m) | g | Play area (64 × 30) | Concourse | Stands | S band | N band | W band | E band |
|---|---|---|---|---|---|---|---|---|---|
| F1 | 0–6.1 | 1.000 | **4 Spin Court boxes** (2 × 2), each convertible to 1 modified badminton / 1 modified volleyball / 1 pickleball | 4 m ring | 5 rows, 4 sides, **1,960** | Bowling 8 lanes + axe 8 bays | Food court | Pool (deck +2.0) | Arcade L1 |
| F2 | 6.1–12.2 | 0.970 | **1 box-lacrosse / arena-soccer rink** (61 × 26, boards + glass); converts to 1 futsal 40 × 20 | 4 m ring | 5 rows, 4 sides, **1,960** | **TBD** | Gym | Pool void | Arcade L2 |
| F3 | 12.2–18.3 + dome to 33.4 | 0.939 | **2 basketball courts** 28 × 15 end-to-end along X (or 4 cross half-courts for practice) | 4 m ring | 12 rows, N and S sides, **2,620** | band roof: rear concourse / terrace | same | flat roof over pool | flat roof over arcade |
- **Total seats ≈ 6,540** (1,960 + 1,960 + 2,620).
- Court counts: **F1 4, F2 1 rink, F3 2.**

## 5. Circulation and egress
- Ground entries on all 4 faces (S faces the x 300 stop across the Rim Promenade).
- Each floor: lift → concourse ring → stands via the front aisle (seats face inward over the concourse) and the rear aisle. Players reach the play area from the concourse through gates in the glass.
- Band programs on F1–F2 open off the stands' rear aisle and from outside.
- 8 stairs × 2.5 m serve every floor; worst travel ≈ 35 m.

## 6. Critical issues (Rev 2.0)
1. **Field lacrosse doesn't fit** (186 × 104 m with stands and band; Strip 5 has ~101 m net; 6.8 m sag; 5 m ceiling). Box lacrosse recommended (Vance proposal).
2. **F2 clear height ≈ 4.6 m** over a column-free 64 × 30 m rink, even with PT band beams. Lofted soccer/lacrosse play needs arena rules (ceiling in play or out).
3. **F1 badminton and volleyball** really want 7–9 m+; at 5.0 m they only work as "modified" low-ceiling versions (Jared's word "modified" fits).
4. **Only 5 stand rows fit per 20 ft storey** (front row raised 0.9 m over the concourse); seats per lower floor are limited to ~1,960.
5. **Footprint grows to 140 × 79 m** and the plinth sag to 3.9 m; it covers the Spine Walk and 2 cross walks.
6. **Dome edge vs short-side stands:** a circular 79 m dome can't cover stands at the hall ends; F3 has long-side stands only.
7. **Basketball Coriolis drift 0.44–0.75 m** per shot: a strong feature, but it must read as intended (aim-off training, fair over halves).
8. Not low gravity (1.00 → 0.83 g at the apex; Rev 1.0 issue stands).
9. Doc RPM values don't match R 200 (Rev 1.0 issue stands).
10. Pool on grade, no-excavation assumption (unverified); corner-plant duct runs now ~60 m to the far side of the hall.
11. Stair egress for ~2,620 seats on F3 uses all 8 × 2.5 m stairs; no spare capacity if seats grow.

## 7. Open questions for Jared
1. **Box lacrosse + arena soccer + futsal on F2 instead of field lacrosse** (Vance proposal)? Field lacrosse can't fit.
2. Accept F2 ≈ 4.6 m clear with arena "ceiling" rules, or give F2 a taller storey (breaks the 20 ft rule)?
3. Footprint 140 × 79 m at strip x 306..446, z −40..39, with the Spine Walk diverted: OK?
4. Dome: circular D 79 m, 15 m rise, apex +33.4 m, glazed: OK? Or an elongated dome / twin domes to get short-side stands?
5. **S band F2 freed space: TBD - options: esports/VR arena, bar & lounge, kids' play zone, pro shop & lockers.**
6. Is the 5-row limit on F1/F2 stands acceptable (≈1,960 seats each), with ≈2,620 on F3 (≈6,540 total)?
7. F3: 2 full basketball courts end-to-end (recommended), or 1 show court with larger runoff?
8. Pool still on the W side and arcade on the E side?
