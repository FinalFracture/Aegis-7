# Tennis Tower (Strip 5): cylinder drop (Rook r7, Wed Nov 11 2026)
Not sent. Kept as a file for Gage, as with GAGE_NOTES.md. Rook did not edit any preface/cylinder scene or script.

## What to instance
- Scene: `res://scenes/tennis_tower/tennis_tower.tscn`. It has one `Node3D` root, `TennisTower_Strip5`, with the script `res://scripts/tennis_tower/tennis_tower_loader.gd`.
- On `_ready` the loader builds the whole tower from `res://assets/models/tt_tower_manifest.json`:
  - 2,671 placements, 226 unique GLBs.
  - Owners: Rook 1,022 · Arrival 42 · Aquatics 66 · Leisure 236 · Courts 352 · Active 549 · Rooftop 404.
  - Loading uses the same runtime `GLTFDocument` path as `preface_playable_area.gd` (`_load_glb_scene`), so no `.import` files are needed.
  - Each GLB is loaded once as a template and duplicated per placement.
  - Children are grouped under `Tag_f1 / f2 / f3 / roof / env / facade / plant / site / cols / struct`, which makes cutaways and culling easy.
- Colliders: every `*-colonly` mesh node becomes a hidden-mesh `StaticBody3D` with a `ConcavePolygonShape3D`, backface collision on, layer/mask 1. `*-convcolonly` nodes get a `ConvexPolygonShape3D` instead.
- Exports:
  - `build_on_ready`, `build_colliders`, `manifest_path`.
  - `apply_drop_transform` (off by default; when on, the root poses itself in the drum).
  - `axial_offset`.
  - The `tower_built(stats)` signal.
- The manifest is generated, so don't hand-edit it. To regenerate: `python3 assets/src/tennis_tower/structure/tower_drop.py`. It uses the same list as `assemble_complex.assemble()`, minus the box-only `preview_hull`.
- Services: `temp-Services_placements.json` is still untracked or unverified, so it is **not** in the manifest. Rook's 4 plant-stack shells and the restroom placeholder shells are in it.
- Water: Aquatics' existing solid placeholder (GLB material). Jared said a solid placeholder is fine; a simulated water scope comes later. The `temp-Aquatics_water.gdshader` bind in `temp-Aquatics_rooms.tscn` is not used here. If you want the shader look, bind it to the water nodes after `tower_built`.
- Plinth: new `tt_struct_plinth_fill.glb` (Rook, `structure/plinth_fill.py`, 2,840 tris, colliders):
  - It is a cast fill from the F1 slab underside (−0.403) and the W/E terrace undersides (−0.313) down to the **true R 200 hull − 0.15 m**.
  - It has its own region under the diving pit (top −2.903).
  - The 0.15 m embed covers the drum's 1° facet chord (≤ 7.6 mm) and the gap between the parabola and the circle.
  - The existing `tt_plinth_skirt` (14) and `tt_plinth_skirt_terrace` (62) still dress the faces, unchanged. Their buried bottoms sit below the hull by design.

## Building frame
- Building local axes: X runs along the drum axis, Z runs across the strip, Y is up. The origin is the SW corner, with the F1 floor top at y = 0.
- Strip 5 local coordinates: x = 60 + X, z = −40 + Z.
- Footprint: X −12..140, Z 0..79. With terraces it spans X −62.5..170.5, Z 13.5..66.5.

## Drop transform (from `preface_playable_area.gd`, read-only)
Constants used:
- `DRUM_FLOOR_R` 200, `DRUM_AXIS_Y` = `EXT_GROUND_TOP_Y` 0.12 + 200 = 200.12, `DRUM_AXIS_Z` −1.25.
- Strip k is centred at alpha = (k − 4)·36°, so strip 5 is at **alpha = +36°**.
- `_drum_outward(a)` = (0, −cos a, sin a). `_drum_tangent(a)` = (0, sin a, cos a), which points toward increasing alpha.

**Parent the scene root directly under the hab world root (world frame, not under `CylinderHab7_DrumAxisPivot`). Use this transform:**
```
basis  x = (1, 0, 0)            # building X = drum axis (+X world)
       y = (0, 0.809017, -0.587785)   # drum "up" at the Strip 5 centreline (-outward(36°))
       z = (0, 0.587785,  0.809017)   # toward increasing alpha (S5|6 side)
       = rotation_degrees (-36, 0, 0)
origin = (-40.0, 18.0743, 81.5712)  # with axial_offset -100 (see below)
```
In GDScript: `TennisTowerLoader.drop_transform()` (static; `class_name` resolves once the editor has scanned, otherwise `preload("res://scripts/tennis_tower/tennis_tower_loader.gd").drop_transform()`), or set `apply_drop_transform = true`.

- The origin is the strip centreline floor point plus tangent·(−40) plus up·F1_HD. Its distance from the axis is 199.9999 m, so the S threshold sits on the floor.
- **F1_HD = 4.0408, not 4.0.** On the real circle the hull at z = −40 is R − √(R² − 40²) = 4.0408 above the centreline. The spec parabola p(Z) = 4.0 − (Z − 40)²/400 is 40.8 mm low at the S face, which would leave the S doors under the floor. With 4.0408:
  - The S threshold (Z 0) is flush.
  - The N face (Z 79) is at −0.202, matching Vance's 0.20 m 1:12 apron.
  - The centreline plinth depth is 4.04 m.
  - Vance's spec text still says 4.0. This is a drop-only correction with no change to the building.
- **Axial datum, needs Gage to confirm:** world x = strip x − 100. That puts the preface building (strip 4, x 100 per `strip4_plan.md` §3) at world x ≈ 0. The tower then spans world x −52..+100 (−102..+120 with terraces), inside the current drum span x −232..488. If the preface's real axial origin differs, change only `axial_offset`.
- Scale: 1:1 metres. Do **not** parent under `CylinderHab7_DrumAxisPivot`: its YZ scale (`_drum_radial_scale`) is fitted to the visual hull, and the walkable facet floor uses the unscaled `DRUM_FLOOR_R`. The tower is built against the walkable floor.
- Gravity / up: building +Y equals `_drum_up_at()` at the Strip 5 centreline. At the E/W terrace ends it is 0°; at the S/N faces it is about 11.5° off the local radial (rule P3 says buildings are levelled at their own centre, and this one is centred on the centreline). If player gravity blends radially, stairs and ramps near the S/N faces will feel about 11° tilted. `DRUM_BLEND_IN/OUT` "world-down inside the footprint" would need the tower footprint added, or a gravity box (`_gravity_boxes`) with building −Y down.
- Coriolis: all play axes run along building X, the drum axis, as specified.

## Headless check (box, Godot 4.7.2, copy of `godot/`)
`godot --headless --path godot -s res://scripts/tennis_tower/tennis_tower_check.gd` printed:
`placed=2671 glbs=226 missing=0 surfaces=24303 tris=3,074,638 colliders=3259 build 1.5–2.0 s`, drop origin (−40.0, 18.0743, 81.5712) at r 200.0000 from the axis and **PASS**.

Floor ray probes (all within ±0.02):

| Probe | Floor y |
|---|---|
| F1 foyer | 0.000 |
| F2 W gallery | 6.112 |
| F2 E | 6.100 |
| F3 | 12.200 |
| Pool ramp top landing | 2.0116 |
| Pool deck past exit | 2.012 |
| Leisure ramp top | 1.0078 |
| Leisure deck past exit | 1.012 |
| W terrace | 0.000 |

No script errors, no leaks at exit.

## Performance (whole tower, everything visible)
- Visible triangles: **3.07 M**.
- Mesh surfaces: **24,303**, the upper bound on opaque draw calls before culling. This is the first thing to reduce.
- Collision shapes: **3,259**. All are trimesh except the trunk convex shapes.
- Largest repeat sets, which are the first MultiMesh / merge candidates:

| Asset | Count |
|---|---|
| tt_terrace_deck | 228 |
| tt_struct_roof_bay4 | 182 |
| tt_gym_floor_tile | 130 |
| tt_court_net | 120 |
| tt_curtain_wall_panel | 114 |
| tt_food_table4 | 114 |
| tt_court_partition | 112 |
| tt_facade_bay | 97 |
| tt_arc_video | 80 |
| tt_climbing_panel | 80 |
| tt_cab_dress_mound | 69 |
| tt_rink_board_2m | 64 |

- Suggested: at far-strip distance, hide `Tag_f1/f2/f3` (interiors) and keep `env/facade/roof/site/struct`. Visibility ranges (`visibility_range_end`) per tag node would cut most of the draw calls from across the drum.

## Known open items
- The axial datum (`axial_offset`) and the gravity blend over the footprint are Gage's calls (see above).
- Services placements are not included until they are committed.
- Mesh clash r3: 228 instance pairs (was 231). The remaining items per owner are in `/workspace/renders/tennis_tower/cylinder_drop_r1/` (box only) and in Rook's report.
- `tt_gallery_lockers_b` reads as "floating" by AABB. It is a door chunk on `_a` (Aquatics), so this is intended. The 12 `tt_lift_core` pits read as "sunk", also intended.

## r7b (Nov 11, 08:3x CT): Rooftop 358edb5 / Courts cc9a204 fixes
- `tt_curtain_wall_panel`: `Sill_Track` now reaches 0.15 m inboard of the glass line. It was 0.65 m and swallowed the F3 E fences, the swing and dome pads, and the W view rails. The room-side sill faces are now at Z 0.135 (S), 78.865 (N), X 139.85 (E) and −11.85 (W).
  - Each trunk fin gets a 0.12 m gunmetal shoe down to the deck.
  - `Head_Track` is unchanged, so the bbox and pivot are unchanged.
  - New `Curtain-colonly` 0.1 m wall at the glass line (the panel had no collider before).
- `tt_lift_core` is now the spec 4.0 m wide: shafts 2 × 1.75, walls 0.15/0.2/0.15, car 1.5 × 2.4 internal, landing doors 1.0 m. It was 4.6 m.
- New `tt_stair_core_b_cap` for the ST+S1 / ST+S2 F2 cores, whose tops sit under the F3 stand rake. Well guards, handrails and the top court stripe are cut at F3. Below F3 everything is unchanged; above F3 the stand's solid rake closes the well.
- Headless check after the fixes: placed 2,659, 228 GLBs, missing 0, surfaces 24,279, tris 3,075,770, colliders 3,361, PASS.

## r7c (Aquatics 667f3cc)
- S facade bays X 2..26 (Z -0.21, yaw 180) now use `tt_facade_bay_pool.glb`: plinth ledge upper box and edge fin trimmed to world Z <= 0.496 (hidden behind lap-tank wall at Z 0.504). Header kept, so bbox/pivot identical to tt_facade_bay. Colliders unchanged (Plinth-colonly reaches Z 0.071, Wall-colonly at glass line).
- Focused clash tt_pool_* vs tt_facade_bay_pool: 0 pairs. tt_pool_deck_finish_c confirmed at [24.0225, 1.92, 17.237].
