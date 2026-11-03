# Strip 5 "The Green" — Multi-Sport Tower (ex Spin Court Tennis Tower) — Structure & Floor Plans

**Status:** DRAFT **Rev 2.1**, 2026-11-02 (Vance). Physical structure and floor plans only: no props, no builds, no code.
**Labels:** *(doc)* = value from a cited repo doc; *(physics)* = derived from doc values; *(real-world ref)* = outside sports/building practice, not a project constraint; **Vance proposal** = my design call, not a constraint.
Plan PNGs (not committed, renders rule): `/workspace/renders/tennis_tower/F1.png, F2.png, F3.png, section.png, roof_candidates.png, site_plan.png`.

## 0. Revision log
- **Rev 2.1 (Jared, 2026-11-02):**
  - **Box lacrosse accepted** on F2.
  - **Clear heights accepted as they are.** "The point of the game isn't to play sports. It's telling a story": sports are decoration, so rule-driven caveats leave the critical list and stay as notes (§2.4).
  - **F3 roof: not necessarily a dome.** It must cover the court (to contain balls); covering the stands too is welcome. Five roof candidates in §3.5; **Vance proposal: R4 Diagrid Lens**, which also lets the **short-side F3 stands come back** (F3 seats 2,620 → 4,704, §3.3).
  - **Spine Walk leads directly to and around the complex** (§3.8): West Arrival Plaza at the main entrance, loop arms N and S, East Plaza rejoin.
  - Main entrance lobby added in the W band; the pool shifts to Z 11..32 to make room (§3.7).
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
| F3 roof edge (≈18.3–20.5 m) | 0.909–0.898 g | |
| R4 lens crown (29.3 m) | 0.853 g | |
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
| F3 | Basketball | 28 × 15 m (+2 m runoff) | **≈8.3 m at the lens edge, 17.1 m under the crown** (R4) | The F3 roof solves the height on this floor only |

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
- Strip fit: 79 m across z fits the program area (z −40..50, 90 m) → **place at strip x 306..446, z −40..39** (Vance proposal), next to the x 300 S4|5 stop *(doc)*. Building local → strip: x = 306 + X, z = −40 + Z. **Rev 2.1: the Spine Walk is rerouted to arrive at and loop the complex (§3.8).**
- Curve sag across 79 m: 79²/(8·200) = **3.9 m** *(physics)*, so the plinth steps up to ~3.9 m at the long faces (was 2.1 m).

### 3.3 Stands per floor in 20 ft storeys (critical check 2)
- Clear height in the stand zone ≈ 5.0 m (short-span band structure, 1.1 m floor zone).
- Spectators must see over people walking on the concourse in front, so the **front row is raised +0.9 m** behind a glass balustrade (Vance proposal). Risers 0.40 m, treads 0.85 m, top-row headroom ≥ 2.5 m:
  - rows at +0.9, 1.3, 1.7, 2.1, 2.5 → **5 rows within the storey**; the top row has 2.5 m headroom. Depth 5 × 0.85 + 1.2 m rear aisle ≈ 5.5 m.
  - A 6th row would need 2.1 m headroom (too low). **No double-height zones on F1/F2** (they would eat the band floors above); F3's stands rise under the roof instead.
- **F3 (Rev 2.1, under the R4 lens):** **12 rows on all 4 sides** (0.45 m risers, 0.85 m treads, top row +5.4 m above F3 = +17.6 m), starting at the concourse edge. Long sides Z 9.1..20.5 / 58.5..69.9 (66 m of seating after the 6 m lift gap); short sides X 24.1..35.5 / 107.5..118.9 (32 m after the lift gap). The roof edge sits at ≥ +20.5 m, so ≥ 2.9 m headroom over the top row.
  - Seats: long 2 × 12 × 132 = 3,168; short 2 × 12 × 64 = 1,536; **F3 = 4,704** (Rev 2.0 dome: 2,620).
  - The short-side stands overhang the W/E band roofs by 5.9 m (X 24.1..30 and 113..118.9), carried on the band's columns.

### 3.4 Long spans
- **F2 must be column-free** over the 64 × 30 m rink, so the F3 floor spans 30 m across Z between columns at the play-area edge (in the concourse, padded).
  - Steel trusses (span/12 ≈ 2.4 m zone) → F2 clear 3.7 m (too low).
  - **Post-tensioned concrete band beams (~1.5 m zone, services run in the band, not over the rink) → F2 clear ≈ 4.6 m (recommended, Vance proposal).**
  - F2's low ceiling is the biggest sporting compromise in the building (§6).
- **F1** can keep columns in the runoff between its 4 court boxes (14 × 26 m grid, 1.1 m floor zone) → F1 clear ≈ 5.0 m. These columns carry the F2 floor.
- **F3** is spanned by the R4 lens (§3.5); its floor is the PT slab above.

### 3.5 F3 roof candidates (Rev 2.1; replaces the Rev 2.0 geodesic dome)
**Cover zone:** hall 64 × 30 m + concourse + 12-row stands on 4 sides = **X 23.5..119.5, Z 8.5..70.5 (96 × 62 m)**. Top stand row +17.6 m → roof edge ≥ +20.5 m. No wind, snow or rain in the drum (Vance assumption), so roofs carry self-weight, services and ball-impact only; netting under glazing contains balls.
| # | Candidate | Span / plan | Rise / height | Structure | Skyline read | Pros | Cons | Story flavor |
|---|---|---|---|---|---|---|---|---|
| R1 | **Hypar Saddle Shell** | 96 × 62, one hyperbolic paraboloid | high points over the short ends **+34 m**, low points over the long-side midpoints **+22 m** | steel gridshell (2 m grid) of straight members (hypar = ruled surface), edge ring beam, 4 corner thrust blocks on the plant-corner lines | a giant saddle; the curves echo the drum's curvature from across the cylinder | iconic, straight members, thrust to 4 points only | corner thrust blocks are large; ~7 m variable headroom over the long stands | "Poured by the first crews from sintered lunar regolith; the saddle is on every Hab-7 sports patch." |
| R2 | **Cable-Net Canopy on Masts** | 96 × 62 net, 4 raked masts outside the corners | masts **+45 m** (0.775 g at tip), membrane +21..+38 m | steel masts, pre-tensioned cable net, translucent ETFE/PTFE membrane, ball net below | 4 spikes reaching toward the axis; a tent | lightest, cheapest, no snow/wind so membranes thrive | mast backstays land in the walks/plaza; reads more festival than hard sci-fi | "Rigged by EVA crews with spare tether cable; Kade still tunes the cables before every final." |
| R3 | **Ribbed Barrel Vault with Glazed Lanterns** | vault spans **62 m across Z**, 96 m long along X | spring +20.5 m, crown **+38.5 m** (rise 18 m) | 13 steel box ribs at 8 m, tie rods at spring, 3 glazed lantern strips along the crown | a drydock hangar laid along the drum axis; the vault arc crosses the drum's own arc | very buildable, regular, reuses shipyard (bldg_16) language | tallest bulk; tie rods cross over the stands; least unique | "Built from a decommissioned cargo-hangar kit; the rib numbers are still stencilled on." |
| **R4** | **Diagrid Lens (recommended)** | elliptical lens **100 × 66 m** over the 96 × 62 cover zone | edge **+20.5 m**, crown **+29.3 m** (rise 8.8 m, 0.853 g at crown) | 2-layer steel diagrid space truss, **3.0 m deep** (≈ span/21 on the 62 m short span), on **8 V-columns** at the stand backs; ETFE cushions + BLEND glass oculus over the courts; no horizontal thrust | a floating disc/lens, an "eye" looking up at the Sun-core from across the drum | covers court + all 4 stands, thrust-free (simple supports on the band), lowest bulk, short-side stands return | 3 m deep truss is heavy for a span; double-curved diagrid nodes are complex | "Ground like a telescope lens; at dusk-cycle the oculus focuses the Sun-core onto centre court." |
| R5 | **Iris / Petal Roof** | elliptical ring 96 × 62 m, 12 steel petals | ring +20.5 m, petal tips meet at **+26 m** closed | fixed perimeter ring truss (covers the stands) + 12 motorised petals on rail bogies (cover the courts); ball nets under the opening | an aperture that opens to the drum sky, like a camera iris | the most theatrical; opens for events | moving roof = drives, seals and maintenance; ball containment when open needs a net | "Opens only for the Remembrance Match, so the players are seen from every strip." |

**Recommendation (Vance proposal): R4 Diagrid Lens.** It covers the court and all four stands, has no thrust into the 2-floor band, brings the short-side stands back (+2,084 seats), sits lowest in the skyline (crown +29.3 m), and its oculus gives the building a single story beat. R5 Iris is the story alternative if Jared wants an opening roof.
- Gravity notes: crown heights give 0.853 g (R4) to 0.775 g (R2 mast tips). Coriolis: a ball or tool dropped from the R4 crown (17.1 m above the court) lands ~0.3 m spinward of plumb (physics, (2/3)ω√(2h³/g)), so hang scoreboards on the lens centre line.

### 3.8 Spine Walk arrival and loop (Rev 2.1, Jared: "leads directly to and around our sports complex")
Strip-5 coordinates (x axial, z arc; `recreation_slice_36deg_layout_v1.md` §3). All Vance proposal.
| Element | x | z | Width | Notes |
|---|---|---|---|---|
| Spine Walk (from Fore) | 0..258 | −6..6 | 12 m | unchanged, then opens into the plaza |
| **West Arrival Plaza** | 258..306 | −24..24 | 48 × 48 m | **main entrance** at the building W face (lobby z −5.5..4.5); the **x 300 Station Walk (12 m, x 294..306)** runs through its east edge, so the x 300 stop towers (z ≈ −56) are 32 m from the plaza |
| **Loop South arm** | 306..446 | −50..−40.5 | 9.5 m | **shared with the Rim Promenade**, the S face entrance (bowling/axe side) opens onto it |
| **Loop North arm** | 306..446 | 41..50 | 9 m | new walk along the N face (food court entrance), abutting the Rim Trail at z 50 |
| West/East corner links | 300..306 / 446..452 | ±24..±41 | 12 m | join the plaza to both arms |
| **East Plaza (rejoin)** | 446..476 | −24..24 | 30 × 48 m | E face entrance (arcade); the **x 450 cross walk** crosses it; Spine Walk resumes east at z −6..6 |
| Spine Walk (to Aft) | 476..800 | −6..6 | 12 m | unchanged |
| Cross walks x 350 / 400 | 350 / 400 | −62.8..−50 and 50..62.8 | 6 m | **end at the loop arms** (S: Rim Promenade, N: north arm) instead of crossing the building |
- Rev 2.0's "divert around the N face" is dropped: the loop gives both sides and makes the building the Spine's destination.
- The C5 Arena block (x 480..520) sits 4 m beyond the East Plaza; its west edge becomes the plaza's frontage (open question: keep bldg_17 there, or drop it because the complex is now the arena).

### 3.6 Lifts, stairs and egress (critical check 4)
- **4 lift banks, one per side** (brief), 2 cars each = 8 cars, at the side midpoints: S X 69.5..73.5 / Z 11..15, N X 69.5..73.5 / Z 64..68, W X 26..30 / Z 37.5..41.5, E X 113..117 / Z 37.5..41.5. Each opens through a **6 m gap in the stands straight onto the concourse** (lifts never surface inside stands). Lift speed cap 1.0–1.6 m/s (Coriolis, Rev 1.0).
- **8 stairs, full height, 2.5 m each = 20 m**: 4 in the stand-free ring corners (X 30..35.5 / 107.5..113, Z 15..20.5 / 58.5..64; outside the dome circle on F3) + 4 beside the lift banks.
- Load (real-world ref ~7.6 mm of stair per person, sized on the worst floor): F1/F2 1,960 → 14.9 m ✓. **Rev 2.1 F3 4,704 seats → 35.8 m needed.** Vance proposal: add **6 F3 stairs 2.7 m wide** (16.2 m) at the backs of the 4 stands (2 each long side at X ~45 / ~98, 1 each short side), dropping through the band to grade beside the lift banks → **14 stairs, 36.2 m ✓**.
- Doc rule: 2 exits per building (`strip4_plan.md` §6). Worst travel from a seat to a stair ≈ 35 m, within the 60 m Vance proposal (`recreation_slice_36deg_layout_v1.md` §5). Ground exits on all 4 faces.

### 3.7 Pool, bowling, axe throwing, plant
- **Rev 2.1 main entrance lobby (W band, F1):** X 0..30, Z 34.5..44.5 (10 m), straight from the West Arrival Plaza to the W lift bank and the F1 concourse; F2 above it is a pool viewing gallery.
- **Pool (W band, F1–F2):** Rev 2.1 at X 2.5..27.5, **Z 11..32** (clear of the SW plant corner Z 0..10 and the lobby); changing rooms Z 47..69. 25 × 21 m, 2.0 m deep, tank on grade, deck +2.0 m (no-excavation assumption, unverified), load ≈ 32 kPa. The SW/NW plant corners serve it.
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
Z15 |  LOBBY>+==== STANDS (5 rows) ============+         |
    |PLANT SW| S band: F1 BOWLING+AXE / F2 TBD |PLANT SE |
Z0  +--------+---------------------------------+---------+
    X0      X30                               X113      X140
 # = stair in ring corner; L = lift bank (S/N at X 69.5..73.5) opening onto the concourse.
 F3: R4 Diagrid Lens 100 x 66 m over hall + 4 stands (12 rows); band roof elsewhere.
```
| Floor | Height (m) | g | Play area (64 × 30) | Concourse | Stands | S band | N band | W band | E band |
|---|---|---|---|---|---|---|---|---|---|
| F1 | 0–6.1 | 1.000 | **4 Spin Court boxes** (2 × 2), each convertible to 1 modified badminton / 1 modified volleyball / 1 pickleball | 4 m ring | 5 rows, 4 sides, **1,960** | Bowling 8 lanes + axe 8 bays | Food court | Pool (deck +2.0) | Arcade L1 |
| F2 | 6.1–12.2 | 0.970 | **1 box-lacrosse / arena-soccer rink** (61 × 26, boards + glass); converts to 1 futsal 40 × 20 | 4 m ring | 5 rows, 4 sides, **1,960** | **TBD** | Gym | Pool void | Arcade L2 |
| F3 | 12.2–18.3 + R4 lens to 29.3 | 0.939 | **2 basketball courts** 28 × 15 end-to-end along X (or 4 cross half-courts for practice) | 4 m ring | 12 rows, **all 4 sides, 4,704** | band roof: rear concourse / terrace | same | flat roof over pool | flat roof over arcade |
- **Total seats ≈ 8,624** (1,960 + 1,960 + 4,704).
- Court counts: **F1 4, F2 1 rink, F3 2.**

## 5. Circulation and egress
- Ground entries on all 4 faces (S faces the x 300 stop across the Rim Promenade).
- Each floor: lift → concourse ring → stands via the front aisle (seats face inward over the concourse) and the rear aisle. Players reach the play area from the concourse through gates in the glass.
- Band programs on F1–F2 open off the stands' rear aisle and from outside.
- 8 stairs × 2.5 m serve every floor; worst travel ≈ 35 m.

## 6. Critical issues (Rev 2.1; sports-rule items moved to notes per Jared)
1. **F3 egress:** 4,704 seats need ~36 m of stair; 14 stairs (8 × 2.5 + 6 × 2.7 m) proposed.
2. **Footprint 140 × 79 m** and a 3.9 m plinth sag across Z; the loop walk and plazas use ~1.1 ha of the C5 Long Field third.
3. **R4 lens:** 3.0 m deep diagrid over 62 m on 8 V-columns standing on the band; the band's columns must take the roof plus the overhanging short-side stands.
4. **Pool moved** to Z 11..32 for the lobby; pool on grade still assumes no hull excavation (unverified).
5. **Corner-plant ducts** run ~60 m to the far side of the hall.
6. Doc RPM values don't match R 200 (carried from Rev 1.0).
**Notes (not critical, per Jared):** F1/F2 clear heights (≈5.0/4.6 m), modified badminton/volleyball, Coriolis shot drift, "not low gravity". Kept in §2 for story/visual use.

## 7. Open questions for Jared
1. **Roof: R4 Diagrid Lens (recommended), or R1 Saddle / R2 Cable-Net / R3 Barrel Vault / R5 Iris?**
2. Bring back the short-side F3 stands (+2,084 seats, +6 stairs)?
3. Spine loop: West Arrival Plaza as the main entrance (with the x 300 stop alongside) and the East Plaza rejoin: OK?
4. C5 Arena (bldg_17) next to the East Plaza: keep, move, or drop since this complex is now the arena?
5. **S band F2 freed space: TBD - options: esports/VR arena, bar & lounge, kids' play zone, pro shop & lockers.**
6. Pool on the W side behind the main lobby, arcade on the E side: OK?
