# Strip 5 "The Green" — Spin Court Tennis Tower — Structure & Floor Plans v1

**Status:** DRAFT v1, 2026-11-02 (Vance). Physical structure and floor plans only: no prop placement, no builds, no code.
**Labels:** *(doc)* = value from a cited repo doc; *(physics)* = derived from doc values; *(real-world ref)* = outside sports/building practice, not a project constraint; **Vance proposal** = my design call, not a constraint.
Plan PNGs (not committed, renders rule): `/workspace/renders/tennis_tower/F1.png … F4.png, section.png`.

## 1. Brief (Jared, as given)
"A type of multi-tiered tennis court thing. Big, tall, open, 4 floors, each 20 feet tall, each with 4 courts, the top one has arena seating. A series of elevators on each side goes to all floors. Each floor encased in plexiglass. It's an adapted form of tennis, adjusted for the lower gravity. Think about how that may play and look, design around it. Under the seating stands for the top level (all 4 sides): 1 side is an arcade, it will have 2 floors. A short side will have other indoor competition/athletic style games, like axe throwing and bowling. On the other short side, it takes up the whole 2 floors, but it's a swimming pool. On the other long side, first floor is a food court. Second floor is a gym. Let's just work on this design for now. Think hard and critical. Floor plans first; physical structures, not prop placement."
- 4 floors × 20 ft = **6.10 m**, building **24.4 m** tall.

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
| F4 (18.3 m) | 0.909 g | |
| Roof (24.4 m) | 0.878 g | |
So the top court is only ~9% lighter. Lob flight time t = 2v_up/g: a 10 m/s vertical lob takes 2.04 s on F1 and 2.24 s on F4 (+10%), apex 5.10 m vs 5.61 m. **The "lower gravity" feel only becomes big in the Chapter 1 crisis states (0.35G/0.12G, doc).** What *is* strong here is **Coriolis**, so I propose the adapted sport is built around Coriolis, with a small per-floor g ladder as a bonus (Vance proposal).

### 2.3 Coriolis (a = −2ω×v, ω along the drum axis)
- **Motion parallel to the axis (strip x): zero Coriolis.**
- **Spinward/antispinward motion (strip z):** radial force 2ωv. At 30 m/s that is 13.3 m/s², bigger than g: a spinward drive "falls" ~2.4× faster than an antispinward one. **Unplayable/unfair for a z-oriented court.**
- **Vertical motion (toward/away from axis):** sideways push, spinward when rising. A lob with v_up drifts sideways by Δ = (4/3)·ω·v_up³/g² (physics):
  - v_up 10 m/s on F1: **3.07 m** drift; on F4: 3.72 m.
  - 4 m-rise lob (fits a 5 m clear ceiling): 2.13 m on F1, 2.24 m on F4.
- Crosscourt component: 5 m/s across the court gives 2.2 m/s² (~0.23 g) radial change; spinward crosscourts dip, antispinward ones float.
- Lifts: a 2.5 m/s lift sees 2ωv = 1.1 m/s² (0.11 g) sideways; at 1.0 m/s it is 0.045 g (Vance proposal: cap lift speed at 1.0–1.6 m/s and use stiff guide rails).

### 2.4 "Spin Court" — the adapted sport (all Vance proposal)
| Item | Proposal | Why |
|---|---|---|
| Orientation | **Play axis along strip x (axial)** | Main ball velocity has zero Coriolis; only lobs and crosscourt shots curve, which becomes the skill |
| Fairness | Both players' lobs drift spinward, which is one player's forehand side and the other's backhand; change ends every odd game (as tennis does) and play sets in pairs | Mirror symmetry is restored over a match |
| Court | Padel-derived 10 × 20 m glass box (*real-world ref*: padel 10 × 20 m) inside a 14 × 26 m module (2 m side, 3 m end runoff) | Fits 4 per floor and a short ceiling |
| Walls | Back walls and side returns playable (padel/squash style); laminated tempered glass 12 mm, 4 m high at the back, 3 m sides; perimeter "plexiglass" enclosure separate | Rebounds keep rallies low; glass, not acrylic, for a playable wall (acrylic scratches and flexes) |
| Net | 0.88 m centre / 0.92 m posts (*real-world ref*: padel) | Low ball path |
| Ball | Pressureless, low-rebound ball (Vance proposal: ~15% less rebound than tennis) | Keeps bounces under the ceiling |
| Ceiling | **Ball touching the ceiling = point lost** ("ceiling out" rule) | The clear height can't allow tennis lobs (§2.5) |
| Signature | Coriolis lob curl 2–2.5 m sideways; F4 "light court" (0.91 g) used for finals | The look: visibly curving lobs seen through glass |

### 2.5 Is 6.1 m enough? **No, for tennis; marginal even for padel.**
- Tennis lobs peak ~8–12 m; ITF indoor guidance wants ~9 m+ over the baseline (*real-world ref*). Padel federation minimum is ~6 m clear (*real-world ref*).
- Clear height = 6.10 m − floor/structure zone. With long spans (§3.3) the clear is **3.7–5.5 m**.
- **Fix options (Vance proposal):** (a) the "ceiling out" rule plus the low-rebound ball with ~5.0 m clear (V2, recommended); (b) raise floor-to-floor to 7.6 m (25 ft) → 30.4 m tall building, ~6.5 m clear; (c) make each court double-height (2 courts per floor-pair), which breaks "4 courts per floor".

## 3. Structural concept
### 3.1 Court layout: **2 × 2, play axis along x** (chosen)
- 1 × 4 in a row along x: 104 × 14 m core, very long and thin, poor spectator bowl, 4 lift banks too far apart.
- 1 × 4 side by side across z: 56 m core across the curve and courts aimed axially, OK, but the core gets wide where the floor curves most.
- **2 × 2:** core **52 × 28 m** (2 modules along x, 2 across z). Compact bowl, stands see all 4 F4 courts, short spans, one column line in the runoff between courts.

### 3.2 Footprint (building local X along strip x, Z along strip z)
| Part | X | Z | Size | Area |
|---|---|---|---|---|
| Pool band (W short side) | 0..30 | 0..58 | 30 × 58 | 1,740 m² |
| Court core | 30..82 | 15..43 | 52 × 28 | 1,456 m² |
| Arcade band (S long side) | 30..82 | 0..15 | 52 × 15 | 780 m²/floor |
| Food court / gym band (N long side) | 30..82 | 43..58 | 52 × 15 | 780 m²/floor |
| Bowling / axe band (E short side) | 82..109 | 0..58 | 27 × 58 | 1,566 m²/floor |
| **Overall** | **0..109** | **0..58** | **109 × 58 m, 24.4 m high** | 6,322 m² |
- Short-side depths are set by the pool (25 m + decks) and bowling (19.16 m foul line to head pin, *real-world ref*, + 4.6 m approach + ~3 m pin deck/machines = ~27 m).

### 3.3 How the band relates to the tower (geometry reading, chosen: "Reading A")
- **Reading A (chosen, most buildable):** the core is the full 4-court tower F1–F4. The 2-floor program band **rings the base at F1–F2** (0–12.2 m). Above the band, **F3 (12.2–18.3 m) is the under-stand concourse and plant**, and the **F4 stands rake outward and up from the F4 court deck (18.3 m)** over the band. So the band is "under the stands" in plan, with one concourse floor between.
- Reading B: the band at F3–F4 directly under the rake; but F4 is the court floor itself, so the band would be beside, not under, the stands, and the base of the building would be courts only. Rejected.
- Reading C: a bowl raked from F2 up to F4 with the band under its lower rows. Taller, bigger structure; rejected for v1.
- **Open question Q1.**

### 3.4 Column grid and long-span floors — 3 variants (genuinely uncertain)
| Variant | Grid | Floor zone | Clear height in core | Notes |
|---|---|---|---|---|
| V1 column-free core | Columns only on the core perimeter; 28 m trusses across Z | ~2.4 m (span/12) | **3.7 m** | Fails padel; truss depth could host viewing/plant mezzanine |
| **V2 one column line in runoff (recommended)** | Core columns at X 30/56/82, Z 15/29/43 → 26 × 14 m bays; 0.6 m padded columns in the 4 m gap between court modules | ~1.1 m (beams + slab + services) | **≈5.0 m** | Columns sit in runoff, not play area; works with the "ceiling out" rule |
| V3 hung floors | Roof mega-trusses (~4 m deep, above F4) carry hangers; floors thin | ~0.6 m | ≈5.5 m | Best clear height; heaviest roof, F4 roof zone grows, complex |
- Band: 9 m grid on long sides (Z 0/7.5/15 lines), 30 m transfer trusses over the pool at F3 (≈2.5 m deep, inside the F3 storey).

### 3.5 Enclosure
- Each court floor is wrapped in a full-height glazed wall on the core perimeter (the brief's "plexiglass"; Vance proposal: laminated polycarbonate panels, BLEND glass in-engine per the Aegis-7 Standard, `context/vance-handoff-v3.md` §2), mullions on the 3.5 m sub-grid.
- Inside, each court has its own playable glass box (§2.4). The outer skin of the band is opaque cladding with glazed strips.

### 3.6 Lifts, stairs, egress
- **Lift banks, one per side (brief "each side"), 2 cars each = 8 cars**, all floors F1–F4 + roof terrace: N and S banks at X 52..60 in the long bands against the core; W and E banks at Z 25..33 in the short bands. Each bank has a stair beside it.
- **Stairs: 8 total, full height** (4 with the lift banks + 4 at the core corners), 2.4 m wide each (Vance proposal).
- Doc rule: **every building has 2 exits** (`strip4_plan.md` §6). Recreation plan Vance proposal: ≤ 60 m to an axial route (`recreation_slice_36deg_layout_v1.md` §5). Worst case in a 109 × 58 m building is ~30 m to a stair; ground exits on all 4 faces → passes both.
- Stand capacity drives stair width (real-world ref: ~7.6 mm of stair per person): 8 rows all round ≈ 2,560 seats → ~19.5 m of stair → 8 × 2.4 m = 19.2 m (≈OK; Vance proposal caps seats at ~2,500).

### 3.7 Pool
- 25 × 21 m (8 lanes × 2.5 m, *real-world ref*), 2.0 m deep, in a hall X 0..30 × Z 0..58, double height F1–F2.
- Load: 2.0 m water = **19.6 kPa** + 0.5 m tank slab ≈ 32 kPa. Put the tank on grade.
- **Hull floor can't be dug into (Vance assumption, unverified):** so the tank sits on the floor and the pool deck is raised **+2.0 m** (ramps 1:12 from F1 entry, 24 m long, or a lift), giving ~7.7 m clear under the F3 transfer truss.
- Spin effect on water: the free surface follows the local g, flat to the eye; slosh from Coriolis is negligible at swimming speeds.

### 3.8 Bowling & axe throwing (E band)
- **F1 bowling** on grade (heavy ball drops on grade, no slab vibration): 12 lanes along X (lane 1.07 m + gutters, pairs 3.6 m) = ~22 m wide; lanes run axially, so the rolling ball has **no Coriolis hook**, keeping it fair (physics).
- **F2 axe throwing:** 8 bays 3.7 × 7 m, targets on isolated steel frames, 150 mm floating floor on spring isolators over the bowling hall, 1 m-wide double stud walls toward the gym/arcade (Vance proposal), throw direction toward the outer wall, away from circulation.

### 3.9 Fit in Strip 5 (C5 Long Field)
- C5 Long Field / Courts block: x 280..480, z −35..40 (`recreation_slice_36deg_layout_v1.md` §8).
- **Place at strip x 306..415, z −36..22** (Vance proposal): 6 m off the x 300 Station Walk, walking 26 m from the x 300 stop towers (S4|5 at z −62.83, *doc*) across the Rim Promenade.
- **Conflict:** it covers the Spine Walk (z −6..6) and the x 350/400 cross walks. Proposal: divert the Spine around the N face at z 24..36 for x 300..420. Open question Q4.
- Curvature: 58 m across z sags 58²/(8·200) = **2.1 m** *(physics)*; the building is levelled at its centre (rule P3, `strip4_plan.md`) on a stepped plinth up to ~2.1 m at the long edges.
- No height cap *(doc, Q6)*.

## 4. Floor-by-floor plans
Building local coordinates (m), origin at the SW corner (X axial, Z toward S5|6).
```
Z58 +-------------+---------------------------+---------+
    |             | N: F1 food court / F2 gym | E band  |
Z43 |  W band     +-------------+-------------+ F1 bowl |
    |  POOL HALL  | COURT 3     | COURT 4     | F2 axe  |
Z29 |  F1-F2      +-------------+-------------+         |
    |  (deck+2.0) | COURT 1     | COURT 2     |         |
Z15 |             +-------------+-------------+         |
    |             | S: ARCADE F1-F2           |         |
Z0  +-------------+---------------------------+---------+
    X0           X30           X56           X82       X109
  Lift banks: N/S at X52-60 ; W/E at Z25-33.  Stairs: 4 corner + 4 at banks.
```
| Floor | Height (m) | Core (X30..82, Z15..43) | S band (Z0..15) | N band (Z43..58) | W band (X0..30) | E band (X82..109) |
|---|---|---|---|---|---|---|
| F1 | 0–6.1 | Courts 1–4, g 1.000 | Arcade L1 (780 m²) | Food court (780 m²) | Pool hall, deck +2.0 | Bowling, 12 lanes |
| F2 | 6.1–12.2 | Courts 5–8, g 0.970 | Arcade L2 (780 m²) | Gym (780 m²) | Pool double height (void) | Axe throwing, 8 bays |
| F3 | 12.2–18.3 | Courts 9–12, g 0.939 | Under-stand concourse, toilets, plant | Concourse, plant | Concourse + pool transfer truss | Concourse, plant |
| F4 | 18.3–24.4 | Courts 13–16, g 0.909, finals | Stands 8 rows (6.8 m deep), rear terrace | Stands 8 rows | Stands 8 rows | Stands 8 rows |
- Stands: 0.85 m treads, 0.45 m risers (Vance proposal); front row at +18.3 at the core edge, top row +21.9, 2.5 m headroom to the 24.4 m roof.
- Seats ≈ long sides 2 × 8 × 104 + short sides 2 × 8 × 56 = **2,560**.

## 5. Circulation and egress
- Ground entries on all 4 faces: S (arcade, facing the x 300 stop), N (food court, facing the diverted Spine), W (pool) and E (bowling).
- Vertical: 8 lifts in 4 banks + 8 stairs; F3 concourse is the stand distributor (vomitories up to the F4 rows).
- Court access: each floor has a 4 m perimeter corridor around the core glass (inside the band edge on F1–F2, on the concourse at F3).
- Egress: ≥ 2 exits per floor (8 available), ≤ 30 m to a stair, meets the doc 2-exit rule and the 60 m Vance proposal.

## 6. Critical issues
1. **Not low gravity:** docs set Strip 5 at 1.00 g; the top floor is 0.91 g. "Low-g tennis" only exists in the flare states, unless the brief means Coriolis tennis. Needs Jared's call (Q2).
2. **6.1 m storeys can't take tennis lobs**: 3.7–5.5 m clear after structure. Needs the "ceiling out" padel-style sport or taller storeys (Q3).
3. **Coriolis makes a spinward court unfair** (13.3 m/s² at 30 m/s): courts must play axially.
4. **RPM numbers in the docs don't match R 200** (2.115 RPM needed for 1.00 g).
5. **Site conflict:** the 109 × 58 m footprint blocks the Spine Walk and 2 cross walks in C5.
6. **Pool on a hull floor:** tank on grade with a +2.0 m raised deck, assuming no excavation (unverified).
7. **Stand egress** limits seats to ~2,500 with 8 × 2.4 m stairs.
8. **Building tilt/plinth:** 2.1 m curve sag across Z.
9. **Lift sideways Coriolis** 0.11 g at 2.5 m/s; cap lift speed.

## 7. Open questions for Jared
1. Band geometry: Reading A (band at F1–F2, concourse F3, stands on F4 over the band) OK?
2. Gravity: keep 1.00 g (Coriolis tennis, F4 at 0.91 g), or is this building meant to be low-g (e.g. a trim-bay style local gravity like Room 10, or set in a 0.35G/0.85G state)?
3. Height: keep 20 ft storeys with the padel-style "ceiling out" sport (V2, ~5.0 m clear), or go to 25 ft storeys (30.4 m tall)?
4. Site: x 306..415 / z −36..22 by the x 300 stop with the Spine diverted, or somewhere else in Strip 5?
5. Which long side is the arcade (I put it on S, facing the maglev), and which short side the pool (W, Fore)?
6. Seat count target (~2,500 proposed)?
7. Structural variant V1/V2/V3 (V2 recommended)?
