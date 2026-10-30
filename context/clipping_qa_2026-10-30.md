# Part-Clipping QA — 2026-10-30 (Patch)

Requested by Jared via Atlas. Ran entirely **read-only on the box** (trimesh 4/5.2 + matplotlib, throwaway scripts in /tmp/clipqa, nothing committed). No Godot run, **no Windows CLI usage**. Assets and scenes were not changed. Baseline is HEAD `daff501`, which includes Gage's `dcdc365`.

## Method
- **(a) Inside each GLB:** world-baked every node, merged vertices, and split it into connected bodies. For each pair of watertight bodies from *different* nodes whose AABBs overlap, depth = the max distance that one body's vertices sit inside the other (contains + signed distance). Reported when depth > 3 mm.
- **(b) In the scenes:** the `.tscn` files are empty shells. All props are placed by `scripts/preface_playable_area.gd` (`ANIMATED_PROP_SPECS`, pickup specs) into `preface_residential_sector.glb` at the origin. I rebuilt those transforms (pos + yaw about +Y, pivot as authored) and probed: penetration into sector nodes (closest point + normal side), a downward ray for floor height, and a ray along the prop's back (−Z local) for wall distance.
- **Note:** `assets/glb/winners/` does not exist. The only "winners" path is `res://assets/models/winners/char_crew_winner_01_aegis7_commander.glb`, which the script references but which is **missing on disk** (it falls back to `char_crew_r1_02.glb`). Scope (a) therefore covered the 48 prop/arch GLBs in `godot/assets/models/`.

## Findings — placed props (scope b)
Floor top in the laundry/maintenance hall is **y = 0.235** (Residential_Hallway_Atrium). The north wall face is at **z ≈ 8.76**.

| Scene / prop | Clipping | Approx depth (m) | Severity |
|---|---|---|---|
| #38 Prop38_FoldingCounter (-1.1,0,8.6) yaw180 | Base below floor; static back + brackets into north wall (z 8.76–8.90) | floor 0.235, wall 0.14 | **Critical** |
| #43 Prop43_SparesDispenser (5.1,0,8.65) yaw180 | Base below floor; back into north wall | floor 0.235, wall 0.14 | **Critical** |
| #42 Prop42_Substation (5.7,0,2.2) yaw-90 | Below floor; West_Storage partition (z≈2.85) cuts through it; Open_Portal_1B 0.023. No wall behind it (nearest 7.7 m along the back axis). The back actually faces −X, not the east wall the comment claims | floor 0.235, partition 0.087 | **Critical** |
| #39 Prop39_FlipSeat (-2.9,0,6.8) yaw180 | Below floor; wall-mount bench is free-standing, 1.76 m from any wall | floor 0.235 (gap 1.76) | **High** |
| Pickups (Alcove2C/Apt202 batteries, Room1A spool, Room1B battery) + Apt201 terminal | No clipping. Floating 0.66–0.75 m above the floor (terminal 1.11 m), which is plausible only if they sit on furniture; not verified | 0 | Low |

## Findings — inside GLBs (scope a), worst pairs
| Asset | Parts clipping | Depth (m) | Severity |
|---|---|---|---|
| kitchen_counter_wallpods | Sink_Basin / Sink_Drain buried in Pods_Low (no cut-out); Service_Port in Pods_Low | 0.165 / 0.145 / 0.10 | High |
| potted_plants_pocket_column | Column_Bands inside Column (hidden); Foliage_Light into Column | 0.135 / 0.046 | Med |
| telescope_pier_dobsonian | Tube_Rings inside Tube; Finder, Pier_Column into Tube | 0.097 / 0.043 / 0.039 | Med |
| lab_crate_frame_204 | Emitter_alloy vs Emitter_violet coincident | 0.078 | Med (z-fight) |
| service_wall_rail_shuttle | Wall_Static sub-parts overlap; Coupler_Arm into wall | 0.075 / 0.025 | Med |
| spares_gravity_dispenser (#43) | Spares_Static stacked bodies overlap (x3) | 0.068 | Med |
| armchair_swivel_pedestal | SwivelLock_Ring in Column; Back_Cushion in Shell | 0.065 / 0.051 | Med |
| bath_pod_capsule | WC_VacUnit in WC (13 pairs) | 0.061 | Med |
| coat_closet_mudroom | Hook_Clamps into Bench_Box (34 pairs) | 0.06 | Med |
| hydro_planter_tiered_exterior | Foliage into Tiers | 0.050 | Low (organic) |
| sofa_lowlounge_plinth | Arm_Bolster into Back_Bolster (L/R) | 0.049 | Med |
| potted_plants_* (trio/rail/tray) | Foliage/Stems | 0.045–0.049 | Low |
| double_bed_moulded_clamped | Headboard vs Mattress/Shell | 0.045 | Low |
| stair_set_switchback | Guard_Sockets into landings | 0.045 | Low (intended embed) |
| riser_shaft | Clamp_Collars on pipes | 0.044 | Low |
| others (31 assets) | bolts/clamps/hinges/latches | ≤ 0.03 | Low (intentional seating) |
| lost_and_found_rail_bins, stair_skylight | none | 0 | — |

Totals: **Critical 3, High 2, Med 10, Low ~33** (Low = the many ≤30 mm hardware embeds plus the pickups).

## Renders
- `godot/renders/qa/clipping/01_prop38_folding_counter_wall_floor.png`: section X=-1.1
- `godot/renders/qa/clipping/02_prop43_spares_dispenser_wall_floor.png`: section X=5.1
- `godot/renders/qa/clipping/03_prop42_substation_plan_y1.png`: plan at Y=1.0
- `godot/renders/qa/clipping/04_kitchen_counter_wallpods_sink_vs_pods.png`: section X=0

## Root causes
1. **Placement against the wrong floor datum (all 4 Gage props):** spawned at y=0.0 while the hall floor top is 0.235. Pivots are correct (bottom-centre, min y = 0), so this is a placement bug, not a pivot bug.
2. **Placement z set to the wall line rather than wall − back depth:** #38/#43 use z=8.6/8.65 with a 0.25–0.30 m back extent, against a wall at 8.76, so they sit 0.14 m into it. Correct z ≈ 8.76 − back extent − 0.01 (≈ 8.45 for #38, ≈ 8.50 for #43).
3. **Wrong yaw/position for #42:** yaw -90 points the back at −X, and there is no wall within reach at x 5.3–6.1. It sits across the West_Storage partition.
4. **#39 footprint comment** ("X -3.5..-2.3, Z 6.6..7.0") has no wall behind it, so a wall-mount part floats.
5. **Overlapping sub-parts in GLBs:** decorative inserts (sink, bands, rings, emitters) are modelled as solid primitives pushed into a parent with no boolean cut. Mostly hidden; visible cases are the sink, the coincident emitters (z-fighting) and the sofa bolsters.
6. **Scale:** none found; all props are at authored scale 1.0.

## Proposed prevention checks (thresholds)
| Check | Threshold |
|---|---|
| Sub-part penetration (different nodes) | ≤ 0.010 m pass; 0.010–0.030 m allowed only for named hardware (bolt/clamp/hinge/latch/socket); > 0.030 m fail unless the part is listed as hidden-embed |
| Coplanar / coincident surfaces (z-fight) | no two faces within 0.001 m and parallel within 1°, overlap area > 1 cm² |
| Floor contact | prop min-y − floor-ray y within ±0.005 m (floor props); never < −0.005 |
| Wall-mounted back clearance | gap from back plane to wall 0.000–0.015 m (no penetration, no float > 15 mm) |
| Free-standing prop to wall/other prop | ≥ 0.02 m AABB clearance, 0 mesh penetration > 0.005 m |
| Pivot standard (Aegis-7) | bottom-centre at (0,0,0): |min y| ≤ 0.002, |centre x|, |centre z of footprint| ≤ 0.01; front = +Z, wall side = −Z |
| Scale | node/root scale 1.0 ± 0.001, no negative scale |
| Spec comment vs geometry | placement yaw must point local −Z at a wall within 0.05 m, or fail |

Suggested automation: a headless Godot `--script` check (through the Grok Build CLI) that, after `_spawn_animated_props()`, ray-probes floor and back wall per spec and asserts the thresholds above. Also a GLB-import CI pass that runs the same sub-part check as /tmp/clipqa/b.py.

## Not checked / limits
- Characters/bots, `env_cylinder_hab7_fullscale_map.glb`, and the sector GLB's own internals were skipped (scope and cost).
- door_hub_bulkhead, rfid_forcefield_door and the 5 pickup GLBs have **no watertight bodies**, so the sub-part depth check could not run on them; only AABB overlap was seen (door_hub CouplerArm vs HubPanel ≤ 0.03 m AABB).
- Animated states: only rest pose (frame 0) checked. Fold-up/flip/drop clips were not swept for clipping.
- Runtime mods (`_remove_all_doors_and_grates`, `_retire_apartment_workbench`, the fullscale world) were not reproduced. The checks ran against the raw sector GLB.
- No in-engine screenshots; the renders are geometric cross-sections.
- Missing asset: `assets/models/winners/char_crew_winner_01_aegis7_commander.glb`.
