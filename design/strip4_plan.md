# Strip 4 — "Spin Street Residential" (Valley A) — Plan v1
**Status:** DRAFT v1, 2026-10-31 (Vance). Markdown only: no assets, no code.
**Sources:** `cylinder_master_plan.md` @124a1bb, `residential_exterior_plan_v1.md` (v1.3), `preface_test_environment_and_wrist_spec.md`, and Rook's curvature numbers (Oct 31).

## 1. Frame and coordinates
- Strip 4 is centred at θ = 144° and spans 126°–162°. It is bounded by seam **S3|4** (126°, toward Civic / strip 3) and seam **S4|5** (162°, toward The Green / strip 5).
- Local map space follows master plan §6:
  - **x = axial length**, 0 m at the Fore Ring up to 800 m at the Aft Ring.
  - **z = arc distance** from the strip centreline. z = −62.83 is S3|4 and z = +62.83 is S4|5. The strip is 125.66 m wide.
  - Down is local −y.
- Rings sit at x = 0 / 200 / 400 / 600 / 800 (the Fore Ring, Ring 25, the Mid Ring, Ring 75 and the Aft Ring).
- **No roads.** Every surface is a walkway, plaza, stair, green or canal. The Spin Streets and the service lane in the v1.3 exterior plan become walkways (see §4).

### 1.1 Floor radius: decision
- **Decision (proposed): the walking floor is R = 200 m** for all strip maps. The master plan derives the 125.66 m arc and the 400 m diameter from it, and Rook's sag numbers use it.
- Preface assets were authored to R_HULL_FLOOR = 185.5 m. The difference is small:
  - A 5 m curved walkway segment (#42) sags 16.8 mm at R 185.5 and 15.6 mm at R 200, a 1.2 mm mismatch.
  - Across the 18 m building depth the rise is 0.22 m at R 185.5 and 0.20 m at R 200.
  - The existing preface pieces therefore fit at R 200 with no remodel. Only the bend parameter of the curved segment kit changes.
- **Open question for Jared (Q1):** confirm R 200, so that 185.5 is retired, or keep 185.5 with a 14.5 m sub-floor (the strip arc at R 185.5 is 116.6 m).

## 2. Curvature, plinths and piers (chord-sag math)
- For a flat chord of width c on a floor of radius R, the sag is s = R(1 − cos(c/2R)) ≈ c² / 8R.
- At R = 200 (Rook's numbers, checked):

| Flat width c across the curve (z) | Sag s | Use |
|---|---|---|
| 10 m | 0.063 m | Guideway module bow on ring lines (§5) |
| **12.6 m** | **0.099 m** | **Maximum single flat plinth with a gap of 10 cm or less** (edge shimmed by kerb trim) |
| 20 m | 0.25 m | Needs 2 steps |
| 30 m | 0.56 m | Needs 3 steps |
| 40 m | 1.00 m | Needs 4 steps |

- **Rule P1:** a building footprint wider than 12.6 m in z sits on **stepped plinth bays of 12.6 m or less**. Each bay is flat, and successive bays step down toward the strip edges, following the tangent. The step is 0.1–0.25 m, hidden by planters or ramps, as in the v1.3 plinth masking.
  - The alternative is **piers**: a flat deck on columns whose height grows with the sag.
- **Rule P2:** along the axis (x) the floor is straight, so footprints can be any length in x with no stepping.
- **Rule P3: tilt.** A building whose centre is at arc distance z leans by z/R rad relative to the strip centreline. At the edge buildings (|z| = 55 m) that is 15.8°. Each building is rotated to its own local up and is never authored "level" to the centreline.

## 3. Placing the preface area (fit and elevated-tram conversion)
- **Axial position:** the preface building (28 × 18 m, footprint X −14..14, Z −9..9) is centred at **x = 100, z = +36.0**. That puts it beside the **x = 100 local stop on S4|5**, one stop from the **Fore Hub** (Fore Ring × S4|5, the passenger dock nearest the preface and the Green), which is the master plan's anchor.
- **Mapping from exterior-plan coordinates to strip coordinates:** x = 100 + X and z = 36.0 − Z. The exterior plan's −Z public face (promenade, tram, canal) turns toward +z, which is toward S4|5 and the Green, so the canal flows toward the river.

| Exterior v1.3 element (X, Z) | Strip 4 position (x, z) | Change |
|---|---|---|
| Building (−14..14, −9..9) | x 86..114, z 27..45 | Unchanged. Ground floor plinth bays 2 × 9 m (sag 0.05 m each) |
| Sector-4 plaza and promenade (Z −9..−18.5) | z 45..54.5 | Unchanged |
| Ground tram band and rails (Z −18.5..−22.5) | z 54.5..58.5 | **Removed.** It becomes the station forecourt walkway (4 m) |
| Ground tram shelter (X 12..18, Z −16.9..−15.6) | x 112..118, z 51.6..52.9 | **Removed as a stop.** The lived-in shelter stays as a story prop (rain shelter / sleeper, #48) |
| Platform kerb, stop totem, cyan tactile kerb | — | Move up to the elevated platform edge (Gage TODO per master plan §4) |
| Canal edge (Z −26) | z 62.0 | The canal moves to z 58.5..61.0 (§7) |
| Memorial nook v1.3 (X 17.4..21.6, Z −12.7..−9.6) | x 117.4..121.6, z 45.6..48.7 | Unchanged. It faces +z toward the station and canal (the v1.3 180° rotation is still correct) |
| Spin St W/E (roads) | x 77..83 / 117..123 | Become **6 m walkways (Spin Walk W/E)** with planter islands. The cart bollards stay at the promenade end |
| Service lane (Z 11.8..15.8) | z 20.2..24.2 | Becomes a 4 m **service walkway** for Sprocket and carts |

- **Elevated stop x = 100 on S4|5:**
  - The platform runs x 85..115 on the strip-4 side of the guideway (z 59.3..62.3).
  - The deck is +5.4 m above the floor; the rail top sits about 5.0 m up, inside the 4.6–6.1 m band.
- **Access from grade:** two stair and lift towers (§5.2):
  - **West tower** at x 86..92, z 54.5..58.5, on the forecourt and clear of the plaza approach.
  - **East tower** at x 108..114, z 54.5..58.5, 3.4 m west of the memorial and clear of its 1.4 m east walk.
- The old resident desire path (platform → exit ramp) now runs from the stair foot to the exit, which is shorter.

## 4. Zoning blocks (axial boulevard)
- **Spine Walk:** a 12 m walkway at z −6..6 for the full 0..800 m. It is the main pedestrian axis and is lit by amber poles every 10 m.
- **Edge Promenades:**
  - **Canal Promenade:** 9.5 m at z 45..54.5 on the S4|5 side.
  - **Civic Promenade:** 9.5 m at z −54.5..−45 on the S3|4 side.
- **Cross Walks:**
  - 6 m walkways along z at every 50 m in x.
  - The ring cross-walks (x 0/200/400/600/800) are 12 m wide, under the ring guideway.
- **Blocks:** each block is 44 m (x) between cross walks and is subdivided into the plots below.

| Block | x range | z range | Use |
|---|---|---|---|
| B-Fore (Fore Ring terrace edge) | 0..50 | −62.8..62.8 | Fore Hub forecourt, end-cap stairs |
| B1 Preface (existing) | 50..150 | 6..62.8 | Preface building, plaza, memorial, x 100 station |
| B2 Housing Row A | 50..200 | −62.8..−6 | Mid-rise housing, galley courts |
| B3 Courtyard Homes | 150..200 | 6..62.8 | Low-rise courtyard blocks, hydro co-op 2 |
| B4 Ring 25 Commons | 200..250 | −62.8..62.8 | Market plaza at the ring crossing |
| B5 Housing Rows B/C | 250..400 | both sides | Mid-rise housing, schools/clinic (Civic side) |
| B6 Mid Ring Civic Gate | 400..450 | −62.8..62.8 | Commons Central forecourt (S3|4) |
| B7 Housing Rows D/E | 450..600 | both sides | Housing, the Headwater Basin on the S4|5 side |
| B8 Ring 75 Commons | 600..650 | −62.8..62.8 | Rec yard, depot |
| B9 Aft Housing | 650..800 | both sides | Housing, aft end-cap stairs |

## 5. Maglev, stations, piers
- **Seam lines S3|4 and S4|5** are axial and straight (along x), on the seam ribs at z = ±62.83. Each guideway is shared with the neighbour strip.
- **Local stops** are at x = 100, 300, 500 and 700 on each line, 8 in strip 4.
- **Transfer stations** are where each line meets the 5 rings, 10 shared with strips 3 and 5:
  - Notable ones: **Fore Hub** (x 0, S4|5) and **Commons Central** (x 400, S3|4).

### 5.1 Guideway and piers
- **T-beam guideway:** the rail top is +5.0 m (inside the 4.6–6.1 band) and the beam is 1.2 m deep.
- **Modules** are 10 m precast spans.
- **Piers:**
  - Every **20 m** on open track (2 modules per span).
  - Every **10 m** under station platforms.
  - Each pier stands on the seam rib (2–3 m raised hull frame), so no walkway is blocked.
- **Clear height under the beam** is 5.0 − 1.2 = 3.8 m for walkways crossing under (2.5 m minimum is required).

### 5.2 Stations
- **Platform:** 30 m long, so a 2-car 24 m train fits with 3 m at each end.
  - Width: 3.5 m local, 5 m at transfers.
  - Deck +5.4 m. The car floor is about +5.4 m, the gap is 75 mm or less, and the cyan tactile kerb runs along the edge.
- **Canopy:** steel and BLEND glass, 3.0 m clear above the deck.
- **Access tower** (6 × 4 m): a 2-flight stair (2 × 2.7 m rise, 1.2 m wide, ≤ 180 mm risers, half landing) plus a 1.6 × 1.6 m lift. Local stops have 2 towers per platform and transfers have 4. All doors are force-field.

### 5.3 Straight seam lines vs curved ring lines
- **Seam (axial) lines are straight.** Platforms are straight, with no curvature issue.
- **Ring lines follow the circumference.**
  - On the floor-radius arc, a 10 m module turns 10/200 rad = **2.865°** and bows (sagitta) 10² / (8 × 200) = **62 mm**.
  - At the guideway height the radius is about 195 m, so a module turns 2.94° and bows 64 mm.
- **Proposal:**
  - **Open ring track:** straight 10 m modules with **angled joints of 2.87° at each pier**. The 62 mm bow is hidden by the beam fascia, and no curved mesh is needed.
  - **Ring-line station platforms** (where a station has a ring face): 3 × 10 m **curved platform-edge modules** (R ≈ 195 m), so the gap between a straight 12 m car and the platform stays under 75 mm. A 12 m car on R 195 has a mid-ordinate of about 92 mm, which straight edges would exceed.
  - **Seam-line platforms stay straight.**
- **Crossings:** where a ring crosses a seam line, both are elevated, so they must be grade-separated:
  - Proposed: the seam line stays at +5.0 m and the ring line rises to a **+10.5 m upper level** within ±70 m of each crossing (4% max grade).
  - This is outside the 4.6–6.1 m band, so it is Q3 below.

## 6. Buildings (footprints and heights)
Coordinates are x (length, m) by z (arc, m). Heights are above the local floor. "Bays" are plinth bays per rule P1.

| ID | Building | x range | z range | Footprint | Floors / height | Plinth |
|---|---|---|---|---|---|---|
| P-1 | **Preface residential (rev C, existing)** | 86..114 | 27..45 | 28 × 18 | 2 / 8.8 m + parapet | 2 bays × 9 m |
| H-A1..A6 | Housing Row A mid-rise ×6 | 55..195 (20 m each, 4 m gaps) | −42..−24 | 20 × 18 | 4 / 17.6 m | 2 bays × 9 m |
| C-1..C4 | Courtyard homes ×4 | 155..195 | 10..40 | 18 × 30 (U-shape) | 2 / 8.8 m | 3 bays × 10 m |
| M-1 | Ring 25 market hall | 210..240 | −20..20 | 30 × 40 | 1 / 9 m | 4 bays × 10 m (step 0.06–0.25 m) |
| H-B/C | Housing Rows B, C ×12 | 255..395 | ±(24..42) | 20 × 18 | 4 / 17.6 m | 2 bays |
| K-1 | Clinic + school (Civic) | 300..340 | −58..−46 | 40 × 12 | 3 / 13.2 m | 1 bay (12 m) |
| G-1 | Civic Gate / Commons Central concourse (at grade under the station) | 395..425 | −62..−48 | 30 × 14 | 2 / 9 m | 2 bays × 7 m |
| H-D/E | Housing Rows D, E ×12 | 455..595 | ±(24..42) | 20 × 18 | 4 / 17.6 m | 2 bays |
| R-1 | Ring 75 rec yard + depot | 610..640 | −40..−20 | 30 × 20 | 1 / 6 m | 2 bays × 10 m |
| H-F | Aft Housing ×12 | 655..795 | ±(24..42) | 20 × 18 | 4–5 / ≤ 22 m | 2 bays |

- All doors are force-field (rev C door spec, Bulkhead Hub). Every building has 2 exits, one onto a promenade or the Spine and one onto a service walkway.
- Heights are capped at 22 m. The far side of the drum is 400 m overhead, and at |z| = 42 m rule P3 tilts buildings 12°.

## 7. Canal and river headwater link
- The **Canal Promenade canal** runs axially at z 58.5..61.0 (2.5 m wide, 1.2 m deep, railing and coping #46 on the strip side) from x 40 to x 560.
- **Headwater Basin** (landmark): at x 500..540, z 48..61, a 40 × 13 m pool with a weir.
- **Link to strip 5:** at x 540 the water passes under the S4|5 seam rib in a culvert (one of the 2–4 rib crossings, with a gated walkway above). It feeds **the River** in strip 5, per master plan §3: the canal outflow to the Green recirculates to strip 2.
- **Supply:** the master plan's Cascade aqueduct along the 3–4 border delivers water at x 40 (Fore end) via a cross-strip channel. That channel runs under the Spine Walk on a 2.5 m culvert bridge at x 40.
- The canal is flat along x (P2), so the gradient is pumped or wire-weired, not built into the floor.

## 8. Landmarks
1. **Preface building and its x = 100 station** (Chapter 1 start, the D-204 hatch, the first tram ride).
2. **The Memorial (#29 monument)** at x 117.4..121.6, z 45.6..48.7, facing +z. It is the first landmark seen from the platform.
3. **The Canal Promenade and Headwater Basin** (x 500..540).
4. **Fore Hub** (x 0, S4|5): passenger dock interchange, with the end-cap terrace stairs.
5. **Commons Central** (x 400, S3|4): Civic ↔ Spin Street, Chapter 1's first trip.
6. **Ring 25 Market Hall** (M-1).

## 9. Walkway grid (widths)
| Walkway | Width | Notes |
|---|---|---|
| Spine Walk (axial, z 0) | 12 m | Main axis; amber poles every 10 m |
| Canal / Civic Promenades | 9.5 m | Through-walk of at least 2.7 m kept clear (v1.3 QC) |
| Ring cross-walks (x 0/200/400/600/800) | 12 m | Under the ring guideway, clear height ≥ 3.8 m |
| Cross Walks (every 50 m) | 6 m | Run along z, so they rise with the curve: 1:12 ramps or steps at each plinth step |
| Spin Walk W/E (preface) | 6 m | The former Spin Streets |
| Service walkways | 4 m | Sprocket and carts; bollard gaps 0.9–1.5 m at junctions |
| Station forecourts | 4 m | Stair and lift foot |
| Minimum anywhere | 0.9 m clear | Same as the exterior plan QC |

## 10. Open questions for Jared
1. **Q1 Floor radius:** use R 200 everywhere (proposed; preface assets fit within 1–2 mm), or keep 185.5?
2. **Q2 Preface axial slot:** is x = 100 (one stop from the Fore Hub) right, or should it sit next to Commons Central (x 400)?
3. **Q3 Ring × seam crossings:** both lines are elevated. Is a +10.5 m ring upper level at crossings (outside 4.6–6.1 m) OK, or should the seam line dip instead?
4. **Q4 The old ground tram shelter:** keep it as a lived-in story prop (proposed) or remove it?
5. **Q5 Canal length:** x 40..560 with the headwater at 540 (proposed), or the full 800 m?
6. **Q6 Housing height cap:** 22 m (proposed)?

## 11. Handoffs
- **Gage (at rebuild, via the CLI):**
  - Raise the preface tram and stop per §3; the platform goes to x 85..115.
  - Retarget the backdrop roll to 144°.
  - Convert the Spin Streets and service lane to walkways.
  - Re-run the navmesh and HAND/NAV QA.
- **Rook:** review the points listed in the commit report (stepped plinths, guideway joints, station platform-edge modules).
