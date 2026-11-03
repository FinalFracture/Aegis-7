# QA-04 r5: Wardrobe_101 trim retest (2026-11-03, 08:05 CST)
HEAD tested: **b724bdc** (fresh clone; includes e3d9a78). Report only; no game files edited.
Method: as in r4. Headless Godot 4.7 ran `preface_playable_area.tscn --qa-placement` from a scratch copy outside the repo (deleted). I measured the world AABB of every MeshInstance3D and raycast down from each mesh's bottom at the centre and 2 inset corners, ignoring the prop's own collider. I ran a shape query and prop-AABB intersections for overlaps, horizontal rays for wall and front clearance, and NavigationServer paths from Door_101. Screenshot: xvfb/GLES3 → `/workspace/qa04-shots/r5_Wardrobe_101.png` (not committed).

## Change under test
e3d9a78 adds `"scale": Vector3(0.925926, 1, 1)` to the Wardrobe_101 spec and applies `node.scale` in `_spawn_rev_c_static_props()`. This is a non-uniform squash along local X (world Z after yaw 90), not a geometry trim.

## Results
| Check | Measured | Expected | Result |
|---|---|---|---|
| Pose | pos (-13.65, 0.02, 5.75), yaw 90.00 | X -13.65, yaw 90 (r3/r4) | **PASS**, unchanged |
| Length / z extent | 2.5000 m, z 4.5000..7.0000 | 2.5 m, z 4.5..7.0 (Rev C.3) | **PASS** |
| Depth / x extent | 0.4880 m, x -13.9000..-13.4120 | x -13.9..-13.4 | PASS (12 mm short of the -13.4 rect edge, inside it) |
| Height | 0.120..2.120 (2.000 m) | ~2.1 m | Note: 2.0 m mesh, unchanged from r4 |
| Collider (PropAabbBody box) | x -13.9000..-13.4120, y 0.12..2.12, z 4.5000..7.0000 | matches mesh | **PASS**, collider follows the scale |
| Floor contact (lowest mesh) | Wall_Plate 0.1200 over the floor at 0.1200 → **0.0 mm** (3 rays) | ≤ 5 mm | **PASS** |
| Back to wall | West wall hit at x -13.9000 at z 4.60 / 5.75 / 6.90; back face -13.9000 → **0.0 mm** | flush | **PASS** |
| Overlaps | Shape query: none. Prop AABBs: none. | none | **PASS** |
| Front clearance | +X rays at z 4.60..6.90, y 0.3 / 1.0 / 1.7: first hit Prop43 at x -5.108 (8.30 m clear) for z ≤ 5.75, and the 101 east wall at x -4.600 (8.81 m) for z ≥ 6.3. The 1.2 m front zone (x -13.4..-12.2) is clear. | ≥ 1.2 m front zone; 0.9 m path at x -11.5 clear | **PASS** |
| Door / clearance | Door_101 at (-6.5, 0, 0.9) (force-field, no swing), 7.1 m in x and 3.6 m in z from the wardrobe | no conflict | **PASS** |
| Nav from Door_101 | Paths found to (-12.9, 5.75) in front (13 pts, nearest point 0.512 m from the wardrobe AABB), to (-11.5, 7.0) on the 0.9 m path (20 pts, 1.034 m), and past the end to (-12.9, 7.6) (16 pts, 0.636 m) | reachable, path not blocked | **PASS** |

### Per-mesh bottoms (gap to floor; all 3 rays agree)
Wall_Plate **0.0**; Uprights, End_Panels, Shelves_1/2/3 **50.0**; Brackets 150.0; Hook_Clamps 180.0; Wall_Rail 200.0; Straps_2 220.0; Buckle_Latches 228.0; Bracket_Bolts 488.0; Hanging bars 1,720.0; Retainer bars 1,800.0; Accent strip 1,970.0 mm. Every mesh's z extent is inside 4.5000..7.0000.

## LAY-23 (2.7 vs 2.5 m point)
**Resolved.** The extent is now z 4.5..7.0 (was 4.40..7.10), exactly the Rev C.3 rect, and the collider matches. With the floor contact verified in r4, LAY-23 stays **Closed**.

## Notes (Low, not failed)
- **Squash, not trim:** a 0.926 non-uniform scale narrows every bay, rail and bar by 7.4%. It's visually fine (screenshot), but the glb is still 2.7 m. Long term, Rook could export a 2.5 m variant. Non-uniform node scale can also skew child transforms and normals if the prop is ever rotated off-axis.
- **Stale comment** at `preface_playable_area.gd:2605-2606` still says "mesh is 2.7 m … world-Z extent 4.40..7.10". Update it to the scaled 4.50..7.00.
- **Carcass hang:** as in r4, the uprights, end panels and shelves sit 50 mm above the floor, and only the wall plate touches it. This reads as wall-hung.

Open LAY counts unchanged from r4: Critical 0 · High 0 · Medium 3 (LAY-06, 07, 18) · Low 4 (LAY-11, 19, 20, 25).
