# Residential rev C — Exterior + 20 m City Ring (plan v1)

**Status: APPROVED v1.2 by Jared 2026-10-29.** The v1 design decisions are approved, and Jared thumbs-upped v1.1. This is design only. The v1 and v1.1 plan PNGs are kept for comparison. The build follows the asset list `residential_exterior_asset_list_v1.md`.
Generator: `design/residential_exterior_plan_v1.py` · Inputs: `cylinder_interior_overhaul_spec.md` and `residential_apartment_layout_v2.md` (rev C)

![Plan v1.2](residential_exterior_plan_v1_2_plan.png)
(For comparison: v1.1 `residential_exterior_plan_v1_1_plan.png`, v1 `residential_exterior_plan_v1_plan.png`)
![Section](residential_exterior_plan_v1_section.png)

## QC v1.2: street furniture (same object table and asserted checks; PNG checked with Read)
**Furniture placed:**
- **8 benches** (1.8 × 0.5 m):
  - 2 at the tram platform ends, beside the shelter.
  - 4 along the track-side edge of the promenade, facing the canal.
  - 1 at the west edge of the plaza.
  - 1 at the memorial nook.
- **6 bins**: 2 at the tram stop and one beside each of 4 benches (2 promenade, plaza, nook).
- **12 bollards**:
  - 4 across the end of each Spin Street at Z -9.4, which protects the promenade and plaza.
  - 2 + 2 along the lane-side edge of the north sidewalk, either side of the service ramp, separating lane from sidewalk.
- These match the asset list, so no counts changed.

| # | Check | Result | Note |
|---|---|---|---|
| 1 | Nothing in a road, lane or tram band | PASS | All 86 objects are on walk or green zones. There are 0 object-object overlaps and 0 off-map. |
| 2 | Walkways keep ≥ 0.9 m clear | FIXED | The bollards narrow the north sidewalk clear width from 1.5 to 1.1 m. Other widths: W 1.4, E 2.6, platform front 1.6 (now X 9..21), new promenade through-walk 2.9. |
| 3 | Exit approach, ramps and service door clear | PASS | The 2.6 m approach has no objects. The ramp-plus-apron box (X 0.5..6.0) is clear at 2.8 m deep. Furniture stays off both ramps. |
| 4 | Bollard gaps between 0.9 and 1.5 m (people pass, carts and vehicles don't) | PASS | Spin Street ends: 1.13 between bollards and 0.9 to the kerbs. Apron rows: 1.2. The 5.5 m ramp opening is the intended service access. |
| 5 | Sprocket (0.78 m) reaches the apron | PASS | The 5.5 m opening is well over 0.78, and the route lane → ramp → door is clear at a 0.9 m check width. |
| 6 | Walking routes | PASS | The desire path (platform → exit) and the promenade → exit route are both unobstructed. |
| 7 | Label collisions | FIXED | The plaza label moved off the plaza-edge bench, and the tram stop label moved into the tram band, off the poles and benches. The legend has 11 entries in the margin band. |
| 8 | Asset counts | PASS | Benches 8, bins 6, bollards 12, as in the asset list. Only the Where column was updated. |

## QC v1.1 checklist (geometry checked in the `.py`, which asserts every check; PNG checked with Read)
| # | Check | Result | Note |
|---|---|---|---|
| 1 | 30 m window-card ring is a true offset | PASS | It was already straight sides plus R 30 quarter arcs. The code confirms the offset error is 0.000 m. The 20 m box corner (34, 29) is 28.28 m from the footprint corner, so it is **inside** the ring. The plot extent covers the whole ring. |
| 2 | Hydro beds clear of Spin St W | FIXED | v1 beds ran to X -21, over the roadway. They now sit at X -14..-2 in a co-op yard that starts at X -17. No zones overlap. |
| 3 | Light poles never in a roadway | FIXED | v1 had poles in Spin St W and E (X ±17.4), the canal and the lane corner. All 30 v1.1 poles fall on walk surfaces, and the code finds 0 in road, lane or tram zones. |
| 4 | Label collisions and legend | FIXED | The memorial nook moved off the building edge into a promenade pocket. The legend, scale bar and compass now sit in a margin band below the map. The tram stop and desire-path labels were moved apart as well. |
| 5 | Plot edges match their labels | FIXED | W edge X -26, E edge +26, N-E edge Z +18, SW and SE Z -9..-3. These come from one zone table that drives both the geometry and the labels. Plots W/E start at Z -2, leaving a 1 m alley to SW/SE. Scale bar 10 m. |
| 6 | Tram shelter off the track | FIXED | The shelter is X 12..18, Z -16.9..-15.6, on the X 9..21 platform, with 1.6 m clearance to the track band. |
| 7 | Sensible walking routes | FIXED | Two routes reach the exit ramp: platform → diagonal desire path, and promenade (west) → plaza. Both are checked unobstructed at a 0.9 m width. The 2.6 m exit approach corridor is kept object-free. |
| 8 | Widths, connections, nothing blocking the exit | FIXED | Clear widths: W sidewalk 1.4, E 2.6, N 1.5, platform front 1.6, hydro aisles 1.1, kerb walk 2.9 (all ≥ 0.9). v1 ramps were only 0.9 m long (1:4), and v1.1 makes them 2.65 m (1:12). The exit ramp meets the plaza, the service ramp meets the lane, and the pad meets the sidewalk. The planters leave both ramps clear. |
| 9 | Orientation labels agree | PASS | +Z spinward, -Z antispinward, X axial with fore -X and aft +X. The plan compass now reads FORE -X / AFT +X, which matches the section and this doc. |
| 10 | Extra: Spin Streets crossed the pedestrian promenade and tram band | FIXED | The streets now end at the promenade (Z -9). Carts stay out of the plaza. |
| 11 | Extra: Plot SW/SE sat on the promenade, and contour ticks overlapped Plot W | FIXED | SW/SE are now at Z -9..-3, behind the promenade. The floor-rise ticks moved into the left margin. |
| 12 | Extra: Sprocket secondary route on the east sidewalk was redundant and crossed the nook | FIXED | Removed, because the exit hub is on the corridor side. The service route runs lane → ramp → door and is checked clear. |
| 13 | Extra: rectangle overlap audit | PASS | All ground zones (with only declared parent/child nesting) and all 60 objects (planters, ramps, pad, shelter, nook, beds, poles) were checked pairwise: 0 overlaps, 0 objects off a walk or green zone, 0 off-map. |
| 14 | Extra: asset counts | FIXED | Light poles 23 → 30 and platform kerb 7 → 6. The service apron is now the ramp. The tri total is about 209k. See the asset list. |
| 15 | Section PNG | PASS | Curvature numbers and labels are unchanged. It was regenerated from the same script. |


## Axis mapping and constants
- **The walking floor is at R = 185.5 m** (`R_HULL_FLOOR`). R 200 m is the hull/interior shell. The drum is 520 m long along world X, and the spin axis sits at Y 200, Z 0.
- **X is axial**: fore is -X, aft is +X. The floor is flat along X.
- **Z is circumferential**: spinward is +Z, antispinward is -Z. The floor curves only along Z.
- **Up** points toward the axis. **Down** points radially outward.
- The **Sector-4 promenade is on -Z** and faces the Valley A canal. The service side is on +Z.

## Curvature (rise = R(1 − cos(s/R)), tilt = s/R)
| Point (arc distance from building centre along Z) | Floor rise | Local "up" tilt |
|---|---|---|
| 9 m (building wall) | 0.22 m | 2.78° |
| 29 m (wall + 20 m, study edge) | **2.26 m** | **8.96°** |
| 39 m (30 m window-card ring) | 4.08 m | 12.05° |
| 20 m from the wall's own tangent | **1.08 m** | 6.18° |
| 1.7 m eye line meets floor at | **25.1 m** away | — |
| Axial (X) | 0 | 0° |

What this means on the ground:
- Neighbour buildings lean about 9° toward the player at the study edge.
- Past roughly 25 m along Z, the ground sits above eye level, so the horizon climbs overhead. The far side is 371 m straight up.
- Streets along X look flat. The Spin Streets, which run along Z, bowl upward.

## Approved decisions (Jared, 2026-10-29)
1. **Maintenance service door: confirmed.** It is 2.0 m wide, on the north (+Z) wall at X 3.2. It uses a force-field frame and a Bulkhead Hub, per the rev C door spec. It gives Sprocket exterior access and serves as the **2nd fire exit**. It opens onto a 1:12 service ramp, which doubles as the apron (X 1..5.6, Z 9..11.65). The exterior Sprocket pad sits flat beside it on the north sidewalk. This is noted in `residential_apartment_layout_v2.md`.
2. **Window streaming (handoff to Gage at rebuild):** windowed units keep the **real interior rendered out to 30 m**, and only then swap in the window card. This replaces the rev C "Cold > 20 m shows card" rule for windowed units. The whole 20 m block is inside the ring.
3. **The tram is live** and has a working stop. The shelter is still lived-in, as a story beat.
4. **Neighbour buildings are facade-only for now**: Plots W, E, N-E, SW and SE.
5. **The plinth is hidden.** The 0.22 m levelling step along both ±Z walls is masked by a run of planters plus 1:12 ramps at the Sector-4 exit and the service door. Each ramp is 2.65 m long for the 0.22 m rise, and the planters stop clear of both ramps. There is no visible plinth. The ±X walls need nothing, because there is no curvature along X.

## Zoning
- **South (-Z): the public face.**
  - The Sector-4 plaza (16 × 9.5 m) sits in front of the 2.6 m exit, with the L2 landing window above it.
  - A 9.5 m promenade runs along X, then the live tram (axial line, catenary), then the canal esplanade.
- **North (+Z): the service side.**
  - A 4 m service lane runs along X.
  - The apron and service door sit off the lane.
  - The hydro co-op beds and the workshop row are beyond the lane.
- **East and west (±X): the Spin Streets.** These are 3 m sidewalks plus 6 m Spin Streets running along Z, the curving direction.
  - The west sidewalk carries hydro planters.
  - The memorial nook sits in a promenade pocket at the SE corner (X 15.8, Z -11).
  - Facade-only neighbours sit beyond.

## Circulation
- **Residents:** they come from the tram platform diagonally across the plaza to the exit ramp, or along the promenade from the west to the same ramp. A worn desire path cuts diagonally across. The service door is the 2nd egress.
- **Sprocket:** it comes from the north grid depot down Spin St E, along the service lane, up the service ramp to the service door. It reaches the Sector-4 exit's Bulkhead Hub from inside, since that hub is on the corridor side. There is no exterior route to it. Carts never cross the plaza.
- **Promenade:** it runs continuously along X, links the neighbouring blocks, and is lit.

## Lighting
- There are 30 amber `#FF9500` poles, all on walk surfaces and never in a roadway, the lane or the tram band. They stand about every 10 m on the promenade's track-side edge, at the edges of the three building sidewalks, on the far side of the lane, on the outer sidewalks of the Spin Streets and on the canal kerb walk, plus two in the plaza at X ±6, clear of the 2.6 m exit approach.
- The dark gaps between poles let the lit windows read.
- The far-side city overhead provides the ambient light.

## Story and setting (wordless)
- **Aegis lived-in:** residents keep the block running.
  - The hydro beds are patched with amber tape and mismatched liners.
  - One west planter is dead.
- **Tram shelter:** the trams run, yet someone sleeps behind the timetable panel, with a bedroll and a hot plate.
- **Memorial nook:** wrist-RFID tags hang on a wire rack beside a violet field lamp and dried hydro flowers.
- **Wear:** the desire line across the plaza paving, scuffed kerbs at the stop, and Sprocket wheel tracks plus coupler scuffs on the apron and the service door jamb.
- **Coriolis tell:** litter and spills drift antispinward along the Spin Streets.

## Handoffs
- **Gage:** at rebuild time, change window streaming so windowed units keep real interiors to 30 m, then show the card (decision 2). Also add the service door as a navmesh link for Sprocket and as an egress.
- **Rook:** build to `residential_exterior_asset_list_v1.md`.
