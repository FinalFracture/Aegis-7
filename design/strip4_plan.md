# Strip 4 — "Spin Street Residential" (Valley A) — Plan v1
**Status:** DRAFT **v2.1**, 2026-10-31 (Vance). v2.1 adds Jared's answers (relayed by Atlas, 2026-10-31): Q1, Q3, Q4 and Q6 are resolved, Q2 and Q5 are on hold, and Q7 and Q8 are open. Unresolved dimensions marked "Vance proposal" are my assumptions, not constraints. v2 resolves every blocker and risk in the "Rook review" section, and the resolution log is §12. Where v1 text below conflicts with v2, the v2 text and §12 win. Markdown only: no assets, no code.
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
- **RESOLVED 2026-10-31 (Jared, Q1): R = 200 m everywhere.** R 185.5 is retired.

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
| Ground tram band and rails (Z −18.5..−22.5) | z 54.5..58.5 | **Removed.** v2: **canal z 51.4..54.3** (2.5 m water + 2 × 0.2 m coping), then forecourt z 54.3..61.3 |
| Ground tram shelter (X 12..18, Z −16.9..−15.6) | x 112..118, z 51.6..52.9 | **RESOLVED 2026-10-31 (Jared, Q4): replaced, not kept as a story prop.** The ground shelter is removed. Its role passes to the elevated x 100 station (platform canopy, x 85..115). The sleeper set #48 is no longer placed here. |
| Platform kerb, stop totem, cyan tactile kerb | — | Move up to the elevated platform edge (Gage TODO per master plan §4) |
| Canal edge (Z −26) | — | v2: the canal moves inboard to z 51.4..54.3, clear of the platform (§7) |
| Memorial nook v1.3 (X 17.4..21.6, Z −12.7..−9.6) | x 117.4..121.6, z 45.6..48.7 | Unchanged. It faces +z toward the station and canal (the v1.3 180° rotation is still correct) |
| Spin St W/E (roads) | x 77..83 / 117..123 | Become **6 m walkways (Spin Walk W/E)** with planter islands. The cart bollards stay at the promenade end |
| Service lane (Z 11.8..15.8) | z 20.2..24.2 | Becomes a 4 m **service walkway** for Sprocket and carts |

- **Elevated stop x = 100 on S4|5 (v2):**
  - The platform runs x 85..115, z **57.93..61.43**. Its edge is at z 61.43 = 62.83 − 1.405, clear of the car envelope z 61.50..64.16 (a 70 mm gap).
  - It is **cantilevered 3.37 m** off the rib piers (rib edge z 61.3), so there are no piers in the canal and the canal is not underneath.
  - Deck +5.40 = car floor (rail top **+5.26**).
- **Access from grade:** two stair and lift towers (§5.2):
  - Towers are 7 × 5 m.
  - **West tower** at x 85..92, z 54.3..59.3.
  - **East tower** at x 107..114, z 54.3..59.3.
  - Each tower's top landing overlaps the platform deck by 1.37 m, so no bridge is needed.
  - A 2.0 m forecourt walk passes the towers at z 59.3..61.3.
  - Memorial clearance: 3.4 m in x (114 → 117.4) and 5.6 m in z (48.7 → 54.3).
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
- **T-beam guideway (v2):** the rail top is **+5.26 m**, measured from the floor, not the rib top. The promoted 0.163 m guideway slab sits on a new 1.2 m T-beam. The beam soffit is 5.26 − 0.163 − 1.2 = **+3.90 m**, and the car roof is +8.50.
- **Modules** are 10 m precast spans.
- **Piers:**
  - Every **20 m** on open track (2 modules per span).
  - Every **10 m** under station platforms.
  - Each pier stands on the seam rib (2–3 m raised hull frame), so no walkway is blocked.
- **Clear height under the beam** is 3.90 m (2.5 m minimum is required).
- **Culvert:** it sits mid-span at **x 530**, between piers at 520 and 540. The pier grid is unchanged and no pier stands on the culvert.

### 5.2 Stations
- **Platform:** 30 m long, so the 2-car 24.31 m train fits with 2.85 m at each end. It is a **straight 30 m tangent deck on piers**, and the guideway kinks only outside the platform.
  - Width: 3.5 m local, 5 m at transfers.
  - Deck +5.40 m = car floor (rail top +5.26 + 0.14). The edge sits 1.405 m from the track centre (70 mm gap), with the cyan tactile kerb along it.
- **Canopy:** steel and BLEND glass, 3.0 m clear above the deck.
- **Access tower (v2), 7.0 × 5.0 m:**
  - Dog-leg stair, 2 flights × 15 risers at 180 mm (2.7 m each), 14 treads × 280 mm = **3.92 m going**.
  - Landings: 1.2 m half landing and 1.2 m bottom landing.
  - Width: 2 × 1.2 m flights + 0.1 m well + 0.15 m walls.
  - Lift shaft 1.9 × 1.9 m including walls. Local stops have 2 towers per platform and transfers have 4. All doors are force-field.

### 5.3 Straight seam lines vs curved ring lines (v2)
- **All platforms are straight 30 m tangents. There are no curved platform edges.**
  - Rook's point: the ring curve is vertical, so a curved edge would not help.
  - On a ring line the floor under the platform ends drops 15² / (2R) ≈ 0.59 m, and pier height absorbs it.
- **Ring track:** straight modules with mitred joints and a pier-cap joint cover. The cover hides the ~31 mm wedge (1.2 m × tan of half the joint angle).
  - **Ring lines at rail top +10.2 (R 189.8), per Q3:** circumference 1192.6 m = **120 modules × 9.938 m**, 3.00° per joint.
- **RESOLVED 2026-10-31 (Jared, Q3): option A.** Ring lines stay up (rail top +10.2) and transfers are two-level. Maglev line height **may rise or fall as needed**; there is no fixed height band. The seam-dip option B is dropped.
- **Crossings:** the v1 "+10.5 m within ±70 m at 4%" is **dropped** (impossible: 5.5 m at 4% needs 137.5 m).
  - The ring rail must clear the seam car roof: 8.50 + 0.30 + 1.2 + 0.163 = **+10.16 m** minimum.

| Option | Geometry | Pros | Cons |
|---|---|---|---|
| **A (SELECTED 2026-10-31): ring lines permanently up**, rail top +10.2 | No grades. Ring station decks at +10.34. Two-level transfers: seam +5.40, ring +10.34 | Simplest track. All 50 transfers identical. No ramps interfering between crossings (125.7 m apart along the ring) | Taller towers (2 × 5.2 m, ~29 risers, lift essential). Heavier visual mass overhead |


## 6. Buildings (footprints and heights)
Coordinates are x (length, m) by z (arc, m). Heights are above the local floor. "Bays" are plinth bays per rule P1.

| ID | Building | x range | z range | Footprint | Floors / height | Plinth |
|---|---|---|---|---|---|---|
| P-1 | **Preface residential (rev C, existing)** | 86..114 | 27..45 | 28 × 18 | 2 / 8.8 m + parapet | 2 bays × 9 m |
| H-A1..A6 | Housing Row A mid-rise ×6 (v2 re-grid, clear of the cross walks) | 53..73, 77..97, 103..123, 127..147, 153..171, 175..193 | −42..−24 | 20 (18 for A5/A6) × 18 | 4 / 17.6 m (Vance proposal) | 2 bays × 9 m + 0.20 m skirt |
| C-1..C4 | Courtyard homes ×4 | 155..195 | 10..40 | 18 × 30 (U-shape) | 2 / 8.8 m (Vance proposal) | 3 bays × 10 m |
| M-1 | Ring 25 market hall | 210..240 | −20..20 | 30 × 40 | 1 / 9 m (Vance proposal) | **v2: 8 × 5 m bays.** Steps 0 / 0.125 / 0.25 / 0.375 m. The outer 0.375 m step is 2 risers of 0.1875 m plus a 4.5 m 1:12 ramp at the doors |
| H-B/C | Housing Rows B, C ×12 | 255..395 | ±(24..42) | 20 × 18 | 4 / 17.6 m (Vance proposal) | 2 bays |
| K-1 | Clinic + school (Civic) | 303..343 | **−44.5..−32.5** (v2, off the promenade) | 40 × 12 | 3 / 13.2 m (Vance proposal) | 1 bay (12 m) |
| G-1 | Civic Gate / Commons Central concourse | **407..437** (v2, clear of the ring walk at 394..406) | **−44.5..−30.5** (v2, off the promenade and rib) | 30 × 14 | 2 / 9 m (Vance proposal) | 2 bays × 7 m |
| H-D/E | Housing Rows D, E ×12 | 455..595 | ±(24..42) | 20 × 18 | 4 / 17.6 m (Vance proposal) | 2 bays |
| R-1 | Ring 75 rec yard + depot | 610..640 | −40..−20 | 30 × 20 | 1 / 6 m (Vance proposal) | 2 bays × 10 m |
| H-F | Aft Housing ×12 | 655..795 | ±(24..42) | 20 × 18 | 4–5 floors (Vance proposal) | 2 bays |

- All doors are force-field (rev C door spec, Bulkhead Hub). Every building has 2 exits, one onto a promenade or the Spine and one onto a service walkway.
- **RESOLVED 2026-10-31 (Jared, Q6): no building height cap.** The floor counts above are Vance proposals. The far side of the drum is 400 m overhead, and at |z| = 42 m rule P3 tilts buildings 12°.

## 7. Canal and river headwater link
- The **Canal Promenade canal** runs axially at z 58.5..61.0 (2.5 m wide, 1.2 m deep, railing and coping #46 on the strip side) from x 40 to x 560.
- **v2 canal:** z 51.4..54.3, from x 40 to **x 530**, with no dead end. Each 6 m cross walk crosses it on a footbridge.
- **Headwater Basin** (landmark, v2): x 518..545, z 45..54.3, a 27 × 9.3 m pool with a weir. It sits clear of the x 500 platform (x 485..515) and its towers.
- **Link to strip 5:** at **x 530** (mid-span between piers 520 and 540) the water passes under the S4|5 seam rib in a culvert (one of the 2–4 rib crossings, with a gated walkway above). It feeds **the River** in strip 5, per master plan §3: the canal outflow to the Green recirculates to strip 2.
- **Supply:** the master plan's Cascade aqueduct along the 3–4 border delivers water at x 40 (Fore end) via a cross-strip channel. That channel runs under the Spine Walk on a 2.5 m culvert bridge at x 40.
- The canal is flat along x (P2), so the gradient is pumped or wire-weired, not built into the floor.

## 8. Landmarks
1. **Preface building and its x = 100 station** (Chapter 1 start, the D-204 hatch, the first tram ride).
2. **The Memorial (#29 monument)** at x 117.4..121.6, z 45.6..48.7, facing +z. It is the first landmark seen from the platform.
3. **The Canal Promenade and Headwater Basin** (x 518..545).
4. **Fore Hub** (x 0, S4|5): passenger dock interchange, with the end-cap terrace stairs.
5. **Commons Central** (x 400, S3|4): Civic ↔ Spin Street, Chapter 1's first trip.
6. **Ring 25 Market Hall** (M-1).

## 9. Walkway grid (widths)
| Walkway | Width | Notes |
|---|---|---|
| Spine Walk (axial, z 0) | 12 m | Main axis; amber poles every 10 m |
| Canal / Civic Promenades | 9.5 m (Canal side v2: z 45..51.4 plus the canal) | Through-walk of at least 2.7 m kept clear (v1.3 QC) |
| Ring cross-walks (x 0/200/400/600/800) | 12 m | Under the ring guideway, clear height ≥ 3.8 m |
| Cross Walks (every 50 m) | 6 m | Run along z, so they rise with the curve: 1:12 ramps or steps at each plinth step |
| Spin Walk W/E (preface) | 6 m | The former Spin Streets |
| Service walkways | 4 m | Sprocket and carts; bollard gaps 0.9–1.5 m at junctions |
| Station forecourts | 4 m | Stair and lift foot |
| Minimum anywhere | 0.9 m clear | Same as the exterior plan QC |

## 10. Open questions for Jared (v2.1)
1. ~~Q1 Floor radius~~ **RESOLVED 2026-10-31:** R 200 m everywhere.
2. **Q2 Preface axial slot (x = 100): ON HOLD** until Jared reviews the redrawn map.
3. ~~Q3 Ring × seam crossings~~ **RESOLVED 2026-10-31:** option A. Ring lines stay up at +10.2, transfers are two-level, and line height may rise or fall as needed.
4. ~~Q4 Old ground tram shelter~~ **RESOLVED 2026-10-31:** replaced by the elevated station, not kept as a prop.
5. **Q5 Canal length (x 40..530): ON HOLD** until Jared reviews the redrawn map.
6. ~~Q6 Housing height cap~~ **RESOLVED 2026-10-31:** no cap.
7. **Q7 Curved walkway kit: OPEN.** v2 uses the curved floor as the walk surface, so #42 is not revived. OK?
8. **Q8 Guideway tri budget: OPEN.** About 7,700 modules ≈ 4.6M tris before instancing. Accept MultiMesh + a 5-module merged LOD beyond 100 m?

## 11. Handoffs
- **Gage (at rebuild, via the CLI):**
  - Raise the preface tram and stop per §3; the platform goes to x 85..115.
  - Retarget the backdrop roll to 144°.
  - Convert the Spin Streets and service lane to walkways.
  - Re-run the navmesh and HAND/NAV QA.
- **Rook:** review the points listed in the commit report (stepped plinths, guideway joints, station platform-edge modules).

## Rook review (3D modeling, 2026-10-31)
Reviewed against R = 200 m (floor), the promoted GLBs, and Vance's text above (unchanged). All numbers recomputed: sag s = c²/8R, turn = L/R.
Promoted dims used: `ext_maglev_guideway.glb` 10.0 × 3.146 m bed, **0.163 m tall** (flange/stator top +0.160, glow +0.163); `ext_maglev_car_body.glb` 12.162 × 2.66 × 3.34 m, placed at guideway base +0.06, floor = base +0.30 (= rail top +0.14), roof = base +3.40; 2-car set 24.31 m; kerb edge 1.40 m from track centre (70 mm gap).

1. **Plinth step bays — RISK (M-1 = BLOCKER for "hidden" steps).**
   - Per-bay sag checks out: 9 m 0.051, 10 m 0.0625, 12.6 m 0.099 m.
   - But if bays are level in the building frame (building rotated to local up at its centre, rule P3), the step between neighbouring bays is b·d/R, where b is the bay width and d the distance of the joint from the centre:
     - H-* 18 m, 2 × 9 bays: symmetric, so 0 step. The footprint edges sit 0.20 m below the centre floor (gap). This needs a 0.20 m skirt; a single 0.10 m shim fails.
     - C-1..4 30 m, 3 × 10: steps 0.25 m at d = ±5. OK at the top of Vance's range.
     - M-1 40 m, 4 × 10: centre bays equal, outer steps (15² − 5²)/400 = **0.50 m**, not 0.06–0.25. Two 0.5 m steps can't hide under a planter; each needs a 6 m 1:12 ramp, or stairs.
   - Fix: M-1 → 8 × 5 m bays (steps 0.125 / 0.25 / 0.375 m) or 0.5 m terraced stairs; or put M-1 on piers (flat deck, 1.0 m max pier rise).
   - Clipping rule: each level bay sits at its own highest floor point (its inner edge), so the slab never sinks into the curved ground. The gap at the outer edge is ≤ b²·(2d+b)/(4bR)… in practice ≤ 0.25 m, closed by a skirt mesh, never by sinking the plinth.
2. **Re-bending #42 from R 185.5 to 200 — RISK (scope).**
   - Math OK: 5 m chord sag 16.85 → 15.63 mm (Δ 1.2 mm), 18 m 0.218 → 0.2025 m.
   - But #42 (curved road) and #43 are **CUT** (Jared, Oct 31, "no roads"). Only shelved candidates exist in `design/assets/ext_road_curved_R185/shelved/`.
   - Reviving them as a curved *walkway* kit is Jared's call (the cut is revivable), not a parameter change.
   - The rest of the preface (paving, curb, kerb, canal edge, guideway) is flat-tiled and isn't bent at all. At R 200 a 2 m paving tile sags 2.5 mm (snaps fine). Without the curved kit, the curved floor itself must be the walk surface.
3. **2.87° ring joints / fascia hiding the 62–64 mm bow — RISK.**
   - At rail level the radius is ≈195 m, not 200, so the joint is 10/195 rad = **2.94°** (1.47° mitre per module end), not 2.87°. Using 2.87° drifts 0.073° per joint.
   - Closure: the full ring circumference at R 195 is 1225.2 m = **122.52 modules**, not a whole number. Use 123 modules of **9.961 m** (or 9.96 m + one closer), each turning 2.927°.
   - The 62–64 mm "bow" is the polygon-vs-arc offset. A chain of straight chords has no visible bow to hide, so the fascia isn't needed for that. What the fascia must hide is the **mitre gap at each pier**: 1.2 m beam × tan 1.47° ≈ 31 mm wedge per side. Recommend a pier-cap joint cover.
   - The +10.5 m crossing level (R 189.5) changes the angle again (3.02°).
   - The promoted `ext_maglev_guideway.glb` is a 0.163 m slab with no beam, so the elevated 1.2 m T-beam span, pier and pier cap are **new assets** (see 6).
4. **R ≈ 195 ring platform edges, 75 mm gap vs 92 mm mid-ordinate — BLOCKER (wrong axis).**
   - Mid-ordinate of the 12.162 m car on R 195 = 12.162²/(8 × 195) = **95 mm** (not 92).
   - The ring curve is **vertical**: it follows the floor around the cylinder axis. A straight car on a curved ring deck gives a **vertical** floor mismatch of up to 95 mm (car mid above the platform if the ends match, or ±47 mm split). It does not give a horizontal edge gap, so curved *edge* modules don't fix it.
   - A ±47 mm step at the door is over a sensible 20 mm boarding tolerance.
   - Fix: build ring-line stations as a **straight tangent 30 m segment** (flat deck and track on piers; the floor below drops 0.577 m at the platform ends, absorbed by pier height), with the 2.94° kinks outside the platform. Then platform edges stay straight like the seam lines.
   - Seam lines: car half-width 1.33 + 75 mm → edge at 1.405 m from track centre (promoted kerb: 1.40 / 70 mm). OK.
5. **6 × 4 m stair/lift towers — RISK (too small) + BLOCKER (platform position).**
   - Rise 5.4 m = 2 × 2.7 m at ≤ 180 mm → **15 risers per flight** (exactly 180 mm). The going at 280 mm is 14 treads = 3.92 m per flight.
   - Dog-leg footprint: 3.92 run + 1.2 half landing + 1.2 bottom landing = 6.32 m > 6 m.
   - Width: 2 × 1.2 flights + 1.6 lift = 4.0 m with zero walls, shaft or clearances.
   - Recommend **7.0 × 5.0 m** (stairs 2 × 1.2 + 0.1 well + 0.15 walls, lift shaft 1.9 × 1.9 incl. walls).
   - Memorial: east tower x 108..114 vs memorial x 117.4..121.6 → **3.4 m in x, confirmed**. They are also 5.8 m apart in z (tower z 54.5..58.5, memorial 45.6..48.7), so there's no conflict. A 7 m tower at x 107..114 still leaves 3.4 m.
   - **The towers fill the whole 4 m forecourt** (z 54.5..58.5), blocking the forecourt walk. Shift them to z 50.5..54.5 (promenade edge) or widen the forecourt.
   - **BLOCKER:** the platform z 59.3..62.3 overlaps the train. The guideway centre is at z 62.83, so the car occupies z 61.50..64.16. The platform edge must be at 62.83 − 1.405 = **z 61.43**, so the platform is z 57.93..61.43 (3.5 m).
   - That platform sits over the canal (z 58.5..61.0). Platform piers every 10 m (5.1) would stand in the canal, but 5.1 puts piers only on the seam rib. Decide between a cantilever off the rib piers (3.5 m + fascia) or piers on the canal coping.
   - The towers need a ~0.6 m bridge from z 58.5 to the platform at 57.93 (they touch).
6. **Deck +5.4 / rail top +5.0 / beam 1.2 / 3.8 m clear / car floor — BLOCKER (0.26 m step).**
   - With the promoted car and guideway, car floor = rail top + 0.14 → **+5.14 m**, not +5.4. A +5.4 deck gives a 0.26 m step up into the platform from the car.
   - Fix: rail top **+5.26** (deck stays +5.4, still inside the 4.6–6.1 band), or deck +5.14.
   - Beam soffit = rail top − 0.163 slab − 1.2 beam ≈ +3.64 at rail top 5.0 (+3.90 at 5.26). Vance's 3.8 m drops the slab; still ≥ 2.5 m. OK.
   - Car roof = base + 3.40 → +8.24 at rail top 5.0 (+8.50 at 5.26). This matters for item 9.
   - Is "+5.0 above floor" measured from the floor or from the top of the 2–3 m seam rib? If from the rib top, everything rises 2–3 m: Q-R1.
7. **Building tilt 12–15.8° vs neighbours and seam rib — RISK.**
   - Tilts OK: 42/200 rad = 12.03°, 55/200 = 15.76°. A row centre at |z| 33 tilts 9.45°.
   - Tops converge by h/R: a 4 m gap at 17.6 m height closes to 3.65 m (OK).
   - Overlaps found:
     - (a) **K-1 (z −58..−46) and G-1 (z −62..−48) overlap the Civic Promenade (z −54.5..−45)**.
     - (b) **G-1 to z −62 reaches the seam rib**. A 2–3 m rib at z −62.83 spans about −61.3..−64.3, so the overlap is 0.7 m.
     - (c) **H-A2 (x 79..99) and H-A5 (x 151..171) overlap the 6 m cross-walks at x 100 and x 150** (x 97..103, 147..153) by 2 m each.
     - (d) The x 100 cross-walk runs through **P-1** (x 86..114); B1 needs an exemption.
   - Fix: re-grid H-A to the 44 m blocks (2 × 20 m with a 4 m gap per block), pull K-1/G-1 to z ≥ −45 or move the promenade, and keep 1.5 m off the rib.
   - Clipping: author each building upright in its own frame and place it at its own (x, z) with a rotation of z/R. Never reuse one transform for a row spread over z.
8. **Canal culvert under S4|5 at x 540 vs piers — RISK.**
   - Open-track piers every 20 m from x 0 put a **pier exactly at x 540**, on the culvert. Also, the x 500 local stop (platform x 485..515, piers every 10 m) sits over the Headwater Basin (x 500..540, z 48..61).
   - Fix: put the culvert mid-span at **x 530** (piers at 520/540), or span the culvert with a 20 m transfer beam. Keep basin piers out of the pool or mark them as wading piers.
   - The canal runs to x 560 but exits at 540, which leaves a 20 m dead end. End the canal at 540, or clarify.
9. **Ring ramp to +10.5 m within ±70 m at 4% — BLOCKER (geometrically impossible).**
   - The rise is 10.5 − 5.0 = 5.5 m. At 4% that needs **137.5 m**; inside 70 m it is **7.9%**.
   - 4% over 70 m gives only 2.8 m (rail top +7.8), which is **below the seam car roof (+8.24)**.
   - Minimum ring rail top = car roof 8.24 + 0.3 clearance + 1.2 beam + 0.163 = **+9.9 m** → rise 4.9 m → 122.5 m at 4%.
   - Transfer stations sit *at* the crossings and need ≥ 30 m flat, so ramps start at ±15 m: ±138 m total. Ring stations are 200 m apart along x; along the ring the neighbouring seam crossing is 125.66 m away, so **ramps from adjacent crossings overlap**. The ring line would have to stay up at +9.9 m for the whole ring.
   - Options:
     - Keep the ring line permanently at an upper level (+9.9..10.5 m), all 10 transfer stations two-level. Simplest.
     - Let the seam line dip at crossings instead (Vance's Q3 alternative): the same 4.9 m drop needs the same run along x, and that fits, since crossings are 200 m apart along x.
     - Accept 8% for a maglev, which is plausible for maglev but outside the stated 4%.
   - Recommend the seam-line dip or a permanent upper ring level. Q3 for Jared.
10. **1:12 cross-walk ramps at plinth steps — OK with a note.**
    - Cross-walks lie on the curved floor itself, which is locally level everywhere (radial gravity), so they need **no ramps** except where they meet a plinth.
    - Ramp lengths at 1:12: 0.10 → 1.2 m, 0.20 → 2.4 m, 0.25 → 3.0 m, 0.50 (M-1) → 6.0 m.
    - Use the promoted `ext_kerb_ramp.glb` pattern: 1.5 m wide, 1:12. The 3.0 m version already covers ≤ 0.25 m.
    - Clipping: ramps sit at their low-end floor contact (±0.005 m) and butt the plinth with a 4 mm joint (same rule as #45).

**General modelling notes**
- Snapping: Gage snaps props to the ground at spawn. For any footprint wider than 2 m in z, use the multi-point (corner) contact and the highest point, never centre-only, or edges sink by c²/8R.
- Tri budget: the promoted guideway is 160 tris per 10 m. A beam, pier and cap set at ~600 tris per 10 m × (800 m × 2 seam lines + 5 rings × 1225 m) ≈ 7,700 modules ≈ 4.6M tris. Needs instancing (MultiMesh) plus an LOD that merges 5 modules beyond 100 m.
- Coplanar risk: the plinth slab top vs paving tiles (keep paving 3 mm above the plinth top or omit it), and the canal coping vs the platform underside (≥ 20 mm).
- Modularity: new assets needed are the elevated T-beam span (10 m, plus a 9.961 m ring variant), pier (rib-mounted and free-standing), pier cap/joint cover (2.94° mitre), a 30 m straight station deck kit, a 7 × 5 m access tower, a plinth skirt (0.05–0.5 m), and a 6 m 1:12 ramp.

**Open questions for Vance**
- Q-R1: is +5.0 m rail top measured from the floor or from the seam rib top?
- Q-R2: should the platform be cantilevered off the rib or on piers in the canal? (Item 5.)
- Q-R3: does the M-1 re-bay (8 × 5 m) or pier deck work for the market hall?
- Q-R4: should the crossing level be resolved by a seam dip or a permanent upper ring level? (Item 9, Q3.)
- Q-R5: is the #42 revival as a walkway kit needed at all, or does the curved floor serve as the walk surface?


## 12. v2 Resolution log (Vance, 2026-10-31)
| Rook item | Status | Resolution |
|---|---|---|
| 1 Plinths | FIXED | M-1 re-bayed to 8 × 5 m (steps 0.125 / 0.25 / 0.375). The 0.375 m step is 2 × 0.1875 risers plus a 4.5 m 1:12 ramp. H-* rows get a 0.20 m skirt. Each bay sits at its highest floor point and is never sunk. |
| 2 #42 rebend | RESOLVED | No roads, so #42 is not revived. The curved floor is the walk surface (Q7). Flat 2 m tiles sag 2.5 mm and snap fine. |
| 3 Ring joints | FIXED | 120 × 9.938 m at 3.00° (option A, selected 2026-10-31). A pier-cap joint cover hides the 31 mm mitre wedge. |
| 4 Curved edges | FIXED | Straight 30 m tangent stations only. Ring-station pier heights absorb the 0.59 m. |
| 5 Towers / platform | FIXED | Towers 7 × 5 m (15 risers per flight, 3.92 m going), at x 85..92 / 107..114, z 54.3..59.3. Memorial clearance 3.4 m (x) and 5.6 m (z). Platform z 57.93..61.43, edge 1.405 m from the track centre, clear of the car at 61.50. Cantilevered 3.37 m from the rib piers. The canal moves to z 51.4..54.3, so nothing is over the canal. |
| 6 Rail/deck step | FIXED | Rail top +5.26, so the car floor is +5.40 = deck. Soffit +3.90 (≥ 2.5 m). Roof +8.50. Heights are measured from the floor (Q-R1). |
| 7 Overlaps | FIXED | K-1 moves to z −44.5..−32.5 (was −58..−46, 9.5 m into the promenade). G-1 moves to x 407..437, z −44.5..−30.5 (was z −62..−48, 0.7 m into the rib). It is now 16.8 m off the rib, well over the 1.5 m minimum. H-A re-gridded: A2 77..97 and A5 153..171 now clear the cross walks at 97..103 and 147..153. The other rows follow the same 44 m block grid. P-1 gets an exemption for the x 100 cross walk, which detours via Spin Walk W/E. |
| 8 Culvert | FIXED | The culvert is at x 530, mid-span between piers 520 and 540. The canal ends at 530. The basin moves to x 518..545, z 45..54.3, off the x 500 platform. |
| 9 Ring ramp | FIXED | The ±70 m 4% ramp is dropped. Ring rail minimum is +10.16. **Option A selected by Jared 2026-10-31.** Option B is dropped. |
| 10 Cross-walk ramps | OK | No ramps on the floor itself. 1:12 ramps only at plinths: 0.10 → 1.2 m, 0.20 → 2.4, 0.25 → 3.0, 0.375 → 4.5. |
| Q-R1..R5 | ANSWERED | R1: from the floor. R2: cantilever. R3: 8 × 5 m bays. R4: option A (Jared 2026-10-31). R5: no revival (Q7). |

**New assets for Rook** (not modeled yet):
- Elevated T-beam span: 10 m, plus ring variants of 9.938 m or 9.948 m.
- Piers: rib-mounted and free-standing, the latter with 0.59 m extra height at the ends of ring stations.
- Pier cap / mitre joint cover (3.00° or 2.927°).
- 30 m straight station deck kit, including a 3.37 m cantilever version.
- 7 × 5 m access tower, plus the two-level transfer variant (option A).
- Plinth skirt (0.05–0.5 m).
- 1:12 ramps (1.2–4.5 m).
- Canal footbridge (6 m).

All must be under 6,000 tris each, bottom-centre pivot, +Z facing, use the 5-candidate workflow, and be instanced via MultiMesh with a merged LOD beyond 100 m.

## 13. v2.1 change log (2026-10-31)
- Q1: R 200 m everywhere. Q3: option A, with no fixed maglev height band and option B removed. Q4: the shelter is replaced by the elevated station. Q6: no height cap, and every building height is labelled "Vance proposal". Q2 and Q5 are on hold pending the redrawn map. Q7 and Q8 are open.
