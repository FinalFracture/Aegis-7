# Residential rev C — Exterior + 20 m City Ring (plan v1)

**Status: APPROVED by Jared 2026-10-29** (plan `0aefaa7`, then the approved decisions below). This is design only. The build follows the asset list `residential_exterior_asset_list_v1.md`.
Generator: `design/residential_exterior_plan_v1.py` · Inputs: `cylinder_interior_overhaul_spec.md` and `residential_apartment_layout_v2.md` (rev C)

![Plan](residential_exterior_plan_v1_plan.png)
![Section](residential_exterior_plan_v1_section.png)

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
1. **Maintenance service door: confirmed.** It is 2.0 m wide, on the north (+Z) wall at X 3.2. It uses a force-field frame and a Bulkhead Hub, per the rev C door spec. It gives Sprocket exterior access and serves as the **2nd fire exit**. It opens onto a service apron with one exterior Sprocket pad. This is noted in `residential_apartment_layout_v2.md`.
2. **Window streaming (handoff to Gage at rebuild):** windowed units keep the **real interior rendered out to 30 m**, and only then swap in the window card. This replaces the rev C "Cold > 20 m shows card" rule for windowed units. The whole 20 m block is inside the ring.
3. **The tram is live** and has a working stop. The shelter is still lived-in, as a story beat.
4. **Neighbour buildings are facade-only for now**: Plots W, E, N-E, SW and SE.
5. **The plinth is hidden.** The 0.22 m levelling step along both ±Z walls is masked by a run of planters plus 1:12 ramps at the Sector-4 exit and the service door. There is no visible plinth. The ±X walls need nothing, because there is no curvature along X.

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
  - The memorial nook sits at the SE corner.
  - Facade-only neighbours sit beyond.

## Circulation
- **Residents:** they come from the tram stop across the plaza to the Sector-4 exit. A worn desire path cuts diagonally across. The service door is the 2nd egress.
- **Sprocket:** it comes from the north grid depot down Spin St E, along the service lane, onto the apron and the pad, then through the service door. A secondary route runs down the east sidewalk to the exit coupler socket. Carts never cross the plaza.
- **Promenade:** it runs continuously along X, links the neighbouring blocks, and is lit.

## Lighting
- Amber `#FF9500` poles stand about every 10 m on the promenade, about every 12 m on the service lane, at the Spin Street corners, and as two poles flanking the exit.
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
