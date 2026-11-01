# QA-02 Geometry & Collision Audit — 2026-11-01

- Build: origin/main @ 39eba42 (Godot 4.7.2 headless, main scene `res://scenes/preface/preface_playable_area.tscn`, run with `--qa-placement` so interiors stay loaded)
- Method: headless SceneTree scripts (kept outside the repo) that (1) dump the global AABB of all 3,790 visible MeshInstance3D nodes and all 3,266 CollisionShape3D nodes, (2) look for coplanar overlapping faces (<=0.001 m apart, >1 cm2 overlap), (3) cast physics rays down/sideways from each prop to measure floor contact and wall gap. Thresholds from the 3d-part-clipping-check skill (floor +/-0.005 m, wall back gap 0-0.015 m, overlap <=0.010 m).
- No game code or assets were changed. Text log only, no renders.
- Clean checks: 0 CollisionShape3D with NULL shape, 0 disabled shapes. Props 38/39/42/43 sit on the floor (dy 0.000) with 0.010 m back gap to the atrium wall (pass).
- Limits: AABB-level coplanar test on big merged meshes (CylinderHab7 drum) gives false positives and was skipped. A point-query wall-leak grid could not read concave trimesh colliders, so no walk-through gaps in walls were proven. A follow-up should use a capsule sweep along every wall line.

## Summary
| Severity | Count |
|---|---|
| Critical | 0 |
| High | 1 |
| Medium | 5 |
| Low | 3 |

## Bugs

### GEO-01 — Interactive props 38/39/42/43 have no collision (player walks through them)
- Severity: High
- Nodes: `InteractivePropsAndPickups/Prop38_FoldingCounter/Counter_Static`, `Prop39_FlipSeat/Bench_Static`, `Prop42_Substation/Substation_Static`, `Prop43_SparesDispenser/Spares_Static` (and all child meshes)
- World AABB: P38 (-3.35,0.235,8.33)-(-0.35,1.135,8.75); P39 (-4.70,0.235,8.63)-(-3.50,1.035,8.75); P42 (9.43,0.235,7.95)-(11.93,2.435,8.75); P43 (-8.95,0.235,8.25)-(-7.05,2.035,8.75)
- Evidence: no CollisionObject3D on the node, its ancestors, or its children. Down/side rays pass through all four props and hit `Residential_Hallway_Atrium_col` behind them.
- Repro: F5, walk to the north atrium wall at z~8.5 (for example x=10.7 for the 2.2 m substation) and walk forward. The player passes through the prop.

### GEO-02 — Pickups sunk 7–9.5 cm into the surface below them
- Severity: Medium
- Nodes / bottom y vs collider top below:
  - `Room1A_Laundry_SuperWire_Spool` (-6.15, 0.980, 7.25): surface 1.075 (`Side_Room_East_Lounge_col`), sunk 0.095
  - `Room1B_Substation_Battery_Cell` (7.20, 0.980, 7.10): surface 1.065 (`Side_Room_West_Storage_col`), sunk 0.085
  - `Apt202_Desk_Battery_Cell` (10.70, 5.100, 7.20): surface 5.195 (`Room_2B_Neighbor_Balcony_Suite_col`), sunk 0.095
  - `Apt201_ToolWall_Thermal_Jelly` (-12.40, 5.020, -4.95): surface 5.090, sunk 0.070
  - `Apt201_ToolWall_Battery_Cell` (-11.95, 5.020, -4.95), `Alcove2C_SuperWire_Expansion` (-11.55, 5.020, -4.95), `Alcove2C_Battery_Expansion` (-10.75, 5.020, -4.95): surface 5.110 (`Alcove_2C_Upper_Vent_Chase_col`), sunk 0.090
- Evidence: a ray cast down from 0.5 m above each pickup's AABB minimum hits the collider top shown. The tolerance is +/-0.005 m.
- Repro: F5, go to each listed location. The lower part of the pickup is hidden inside the shelf or desk.

### GEO-03 — Apt 201 tool-wall pickups float 0.675 m above the walkway
- Severity: Medium
- Nodes: `InteractivePropsAndPickups/Apt201_ToolWall_SuperWire_Spool` (-13.30, 5.020, -4.95), `Apt201_ToolWall_BCI_Headband` (-12.85, 5.020, -4.95)
- Evidence: there is no collider under them until `Upper_Mezzanine_Walkway_col` at y=4.345 (gap 0.675 m). The shelf collider `Alcove_2C_Upper_Vent_Chase_col` ends at about x=-12.74, so these two sit past its edge. Neighbouring items at x>=-12.53 rest on y~5.09–5.11.
- Repro: F5, go up to the Apt 201/Alcove 2C tool wall and look at the left end. The spool and headband hang in mid-air.

### GEO-04 — Z-fighting: overlapping desire-path decals
- Severity: Medium
- Nodes: `ExteriorPlacements_v1_3/Ext_47_ext_desire_path_decal_1002/layer0..2` and `..._1003/layer0..2`
- World: y=0.183/0.185/0.186, overlap x 1.83–2.11, z -12.71 to -11.54 (about 0.33 m2 per layer)
- Evidence: each matching layer pair is coplanar to within 0.000 m and overlaps.
- Repro: F5, exit Sector 4 and look at the ground at about (2.0, 0.18, -12.1). The decal flickers.

### GEO-05 — Z-fighting: SeamFix boxes share faces with the room shells
- Severity: Medium (confirm visually)
- Nodes: `.../Side_Room_East_Lounge` vs `Side_Room_East_Lounge_SeamFix` (planes x=-4.75 and x=-12.25, about 19 m2); `.../Side_Room_West_Storage` vs `Side_Room_West_Storage_SeamFix` (planes x=0.75 and x=8.25, about 19.7 m2)
- Evidence: the AABB faces are identical (to within 0.0005 m) across y 0.225–3.99 and z 2.935–8.765.
- Repro: F5, stand in either side room and look at the side walls from a shallow angle. Look for flicker.

### GEO-06 — Z-fighting: DockPad InductionRing and Chevrons are coplanar at all 6 door hubs
- Severity: Medium
- Nodes: `InteractivePropsAndPickups/SectorRFIDForceFieldDoors/<DOOR>/DoorHub_<DOOR>/DoorHubBulkhead/DockPad_InductionRing` and `DockPad_Chevrons` for DOOR_APT201, APT202, ALCOVE2C (y=4.357), RM1A, RM1B, SECTOR4_EXIT (y=0.247)
- Evidence: both meshes are flat on the same plane, overlapping about 196 cm2.
- Repro: F5, look down at the dock pad in front of any force-field door.

### GEO-07 — Z-fighting: TalkPad and IntercomRing coplanar
- Severity: Low
- Nodes: `.../DoorHubBulkhead/TalkPad` vs `IntercomRing` on DOOR_APT201, APT202, RM1A (z=2.669/2.76), ALCOVE2C (z=-3.382)
- Evidence: about 3 cm2 coplanar overlap.

### GEO-08 — Open_Portal_Sector_Exit face coplanar with the vestibule shell
- Severity: Low
- Node: `.../Ground_Service_Vestibule/Open_Portal_Sector_Exit`, plane z=-8.76, x -1.48 to 1.48, y 0.235–3.395 (about 9.35 m2 of shared face)
- Repro: F5, look at the Sector 4 exit portal frame face-on.

### GEO-09 — Navmesh edge-overlap errors at load
- Severity: Low
- Evidence: at load, the console prints "Navigation region synchronization had 8 edge error(s). More than 2 edges tried to occupy the same map rasterization space." This points to overlapping or duplicated geometry in the baked navigation sources.
- Repro: run the main scene headless and read the console.

## Notes (not filed)
- Pickups have no CollisionObject3D. This is treated as by design (distance-based interaction).
- Prop43 sits in the 0.9 m strip between the East Lounge collider face (z=7.86) and the atrium wall (z=8.76), not inside the lounge footprint. Confirm this matches the intended "East Lounge north wall" placement.
