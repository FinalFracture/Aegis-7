# Residential rev C: Asset List (Vance, Oct 29 2026)
Source: approved rev C floor plans and room layouts (`residential_roomlayout_rev_c_L1/L2.png`). Checked against `godot/assets/models/` (15 glb files; re-checked rev C.2 Oct 29: 43 glb files) and `scripts/preface_playable_area.gd`.
~~Struck through~~ = already modeled as a glb (path cited). "Level blockout" = exists only as primitives built in the level script, so it still needs a glb.
Sizes are rough W × D × H in meters.

## A. Doors and building fixtures
| # | Item | Units | Qty | Size |
|---|---|---|---|---|
| 1 | ~~Force-field door frame~~ `godot/assets/models/rfid_forcefield_door.glb` | all 10 units + Sector-4 exit | 11 | 1.4 × 0.2 × 2.3 (Maint 2.0, exit 2.6) |
| 2 | ~~Bulkhead Hub~~ `godot/assets/models/door_hub_bulkhead.glb` | all doors | 11 | 0.40 × 0.20 × 0.80 |
| 3 | ~~Switchback stair set: flight 1 16 R + flight 2 10 R (26 × 0.1615, T 0.28), south mid-landing Y 2.585, L1 bottom landing 2.4, L2 landing 4.1 (approved, `residential_stair_core_v1.md`)~~ `godot/assets/models/stair_set_switchback.glb` | stair core L1–L2 | 1 | 3.8 × 8.1 clear, 4.2 rise |
| 4 | ~~Stair glass guards (laminated, clamped + latch pins) + handrails both sides (own colliders)~~ `godot/assets/models/stair_guard_handrail.glb` | stair core | 1 set | ~15.5 m handrail at 0.9 H, ~11 m guard at 1.1 H |
| 5 | ~~Skylight strip, over the stair void only (v1.1)~~ `godot/assets/models/stair_skylight.glb` | stair core roof, Z -8.9..-4.88 | 1 | 3.8 × 4.0 |
| 6 | Lit window interior card | 8 apartments | 8 | 3.0 × 1.5 quad |
| 7 | ~~Riser shaft + sealed wall chase (re-aligned v1.1: X 0.6..1.6, Z 2.4..3.4 on both levels)~~ `godot/assets/models/riser_shaft.glb` | Maintenance, 202 | 1 | 1.0 × 1.0 × 8.8 |
| 51 | ~~Sprocket bot lift (v1.1, pending review): 1.2 × 1.2 × 1.4 car, 1.6 × 1.6 shaft, 2 shaft doors 1.0 × 1.3, 2 call panels in Bulkhead Hub style (reuses the `door_hub_bulkhead.glb` mesh with a lift glyph), controller cabinet~~ `godot/assets/models/sprocket_lift.glb` | Maintenance SW / 202 SW, opens to corridor L1 + L2 | 1 set | shaft 1.6 × 1.6 × 6.6 |


## B. Bath and hygiene
| # | Item | Units | Qty | Size |
|---|---|---|---|---|
| 8 | ~~Bath pod (shower, WC, sink module)~~ `godot/assets/models/bath_pod_capsule.glb` | 101–104, 201–204 | 8 | 2.2 × 2.2 × 2.4 |


## C. Kitchen and dining
| # | Item | Units | Qty | Size |
|---|---|---|---|---|
| 9 | ~~Kitchen counter + hob (modular run)~~ `godot/assets/models/kitchen_counter_wallpods.glb` | 101–104, 201–204 | 8 | 3.5 × 0.6 × 0.9 |
| 10 | ~~Small dining table~~ `godot/assets/models/table_pedestal_small.glb` | 101, 104, 201, 204 | 4 | 1.2 × 0.8 × 0.75 |
| 11 | ~~Dining table for 4~~ `godot/assets/models/table_pedestal_dining4.glb` | 103, 202 | 2 | 1.6 × 0.9 × 0.75 |
| 12 | ~~Tea table (low)~~ `godot/assets/models/table_pedestal_tea.glb` | 102, 203 | 2 | 1.2 × 0.8 × 0.45 |
| 13 | ~~Dining chair/stool~~ `godot/assets/models/dining_chair_swivel.glb` | tables above | 20 | 0.45 × 0.45 × 0.9 |
| 14 | ~~Tea set (pot + cups)~~ `godot/assets/models/tea_set_rail_caddy.glb` | 102, 203 | 2 | 0.4 × 0.3 × 0.2 |


## D. Living
| # | Item | Units | Qty | Size |
|---|---|---|---|---|
| 15 | ~~Sofa~~ `godot/assets/models/sofa_lowlounge_plinth.glb` | 101, 103, 201, 202, 203, 204 | 6 | 2.5 × 0.9 × 0.85 |
| 16 | ~~Armchair / reading chair~~ `godot/assets/models/armchair_swivel_pedestal.glb` | 102, 203, 201 (C.2 reading chair by the W window), 204 (C.2) | 4 | 1.0 × 1.0 × 1.0 |
| 17 | ~~Lab bench~~ MOVED TO LAB/WORKSHOP BUILDING (Jared, Oct 29): removed from 104; not modeled now, waits for that building | ~~104~~ lab/workshop building | — | 2.5 × 0.9 × 0.9 |
| 18 | Window reading nook bench | 203 | 1 | 4.0 × 0.4 × 0.5 |


## E. Sleeping and storage
| # | Item | Units | Qty | Size |
|---|---|---|---|---|
| 19 | ~~Double bed~~ `godot/assets/models/double_bed_moulded_clamped.glb` | 101, 102, 103, 104, 201, 202, 203, 204 | 8 | 2.0 × 1.6 × 0.6 |
| 20 | ~~Kids' bunk~~ `godot/assets/models/kids_bunk_wall_clamped.glb` | 103, 202 | 2 | 0.9 × 1.9 × 1.7 |
| 21 | ~~Wardrobe~~ `godot/assets/models/wardrobe_openbays_rails.glb` | 101, 103, 104, 201, 202, 203, 204 | 7 | 0.5 × 2.5–3.0 × 2.1 |
| 22 | ~~Coat and storage closet~~ `godot/assets/models/coat_closet_mudroom.glb` | 103, 104, 203, 204 | 4 | 3.7 × 0.5 × 2.1 |
| 23 | Suit hook + storage with pressure suit | 102 | 1 | 0.5 × 2.5 × 2.1 |
| 24 | ~~Resident lockers~~ REMOVED FROM APARTMENT BUILDING (Jared, Oct 29): option 5 Bench Niche kept as a standalone locker run for another building (TBD), not tied to laundry; `godot/assets/models/locker_run_bench_niche.glb` | ~~Laundry~~ other building TBD | — | 4.8 × 0.5 × 2.0 |


## F. Workstations and story props
| # | Item | Units | Qty | Size |
|---|---|---|---|---|
| 25 | ~~Tool wall panel, built as the Sprocket-first service wall redirect (`design/assets/service_wall/`)~~ `godot/assets/models/service_wall_rail_shuttle.glb` | 101, 201, Maintenance | 3 | 2.5–3.5 × 0.5 × 2.0 |
| 26 | ~~Apartment workbench~~ (level blockout `Apartment_Workbench`) MOVED TO LAB/WORKSHOP BUILDING (Jared, Oct 29): removed from 201; not modeled now, waits for that building | ~~201~~ lab/workshop building | — | 3.7 × 2.5 nook |
| 27 | ~~Task lamp (level blockout `Apt201_Workbench_TaskLight`)~~ `godot/assets/models/task_lamp_rail_slider.glb` | 104, 201, 204 | 3 (C.2: on the 104 and 204 window desks; 201 as a side-table/floor-stand lamp beside the reading chair) | 0.2 × 0.2 × 0.5 |
| 28 | ~~Window desk + data slates~~ `godot/assets/models/window_desk_cantilever_slab.glb` | 104, 204 | 2 | 4.0 × 0.4 × 0.75 |
| 29 | ~~Specimen shelf~~ MOVED TO LAB BUILDING (Jared, Oct 29): removed from 104; Open Rack is a future science/lab-building asset, `godot/assets/models/specimen_rack_open_lab.glb` | ~~104~~ lab building | — | 0.9 × 0.63 × 1.9 |
| 30 | ~~Telescope~~ `godot/assets/models/telescope_pier_dobsonian.glb` | 104 | 1 | 0.6 × 0.6 × 1.5 |
| 31 | ~~Emitter repair bench (dismantled field emitter)~~ MOVED TO LAB/WORKSHOP BUILDING (Jared, Oct 29): removed from 204; not modeled now, waits for that building | ~~204~~ lab/workshop building | — | 0.9 × 1.9 × 0.9 |
| 32 | ~~Cycler route model (wall)~~ `godot/assets/models/cycler_route_lightbox.glb` | 203 | 1 | 0.9 × 0.2 × 1.0 |
| 33 | ~~Hydro planter (window/balcony)~~ MOVED TO EXTERIOR (Jared, Oct 29): removed from 103/202; Tiered Steps planter now serves the hydro co-op / sidewalk planters, `godot/assets/models/hydro_planter_tiered_exterior.glb` | ~~103, 202~~ exterior | — | 4.0 × 0.4 × 0.7 |
| 34 | ~~Potted plants set~~ (Jared's final pick, Oct 29): `godot/assets/models/potted_plants_rail_cradles.glb` (default 102) and `godot/assets/models/potted_plants_pocket_column.glb` (default 203). SUPERSEDED, kept unplaced: `potted_plants_moulded_trio.glb`, `potted_plants_shared_tray.glb` | 102, 203 | 2 | 1.20 × 0.55 × 0.25 (wall rail) / 0.90 × 0.78 × 0.41 |
| 35 | ~~Toy chest + rail bins + toy kit~~ (Jared combined iter 1 + 3, Oct 29): `godot/assets/models/toy_chest_rail_bins.glb` | 103 | 1 | 1.2 × 0.6 × 0.5 chest; bins on a 0.90 m rail to 1.21 m |
| 52 | ~~Fold-down wall desk~~ DROPPED in C.2 (Jared: don't shape 201 around the objective; Gage re-points the objective at rebuild) | — | — | — |
| 53 | Lab crate, labelled for the future lab/workshop (violet D-03 lab glyph, wordless; 204 lid ajar showing emitter parts). Same mesh as exterior #48 crate | 104, 204 | 2 | 1.0 × 0.6 × 0.5 / 0.9 × 0.7 × 0.5 |
| 55 | Lost-and-found rail bins + wordless notice board (C.2a kitbash: #35 rail bins + the exterior #52 board mesh) | Laundry N wall X -4.3..-3.0 | 1 | 1.3 × 0.3 × 1.4 |
| 54 | Removal decal set (dust outline of the lab bench and workbench, shelf ghost + wall anchor holes, planter clamp-bolt marks + water ring) | 104, 201, 204 (emitter bench outline), 103, 202 | 1 set | decals |
| 36 | Small clutter kit (meal tray, cups, cables, photo frames as decals) | 101, 102, 104, 202 | 1 kit | small |


## G. Laundry
| # | Item | Units | Qty | Size |
|---|---|---|---|---|
| 37 | ~~Washer/dryer stack~~ `godot/assets/models/washer_dryer_alloy_reclaim.glb` | Laundry | 4 | 0.8 × 0.8 × 1.9 |
| 38 | Folding counter (C.2a: +1 run on the N wall, where the lockers were, X -2.6..0.4) | Laundry | 2 | 0.6 × 3.5 × 0.9 / 3.0 × 0.6 × 0.9 |
| 39 | Bench | Laundry | 1 | 1.2 × 0.4 × 0.45 |


## H. Maintenance
| # | Item | Units | Qty | Size |
|---|---|---|---|---|
| 40 | Sprocket floor pad (level blockout `DockPad`/`DockPad_InductionRing`) | Maintenance | 3 | 1.2 × 1.2 × 0.05 |
| 41 | Coupler arm (wall/ceiling mount) | Maintenance | 3 | 0.3 × 1.5 reach |
| 42 | Substation cabinet (level blockout `Room1B_Substation_*`) | Maintenance | 1 | 0.6 × 2.5 × 2.2 |
| 43 | Spares shelf | Maintenance | 1 | 1.9 × 0.5 × 1.8 |


## I. Characters and pickups (placed, already modeled)
| # | Item | Units | Qty | Size |
|---|---|---|---|---|
| 44 | ~~Neural tendon sleeve~~ `godot/assets/models/prop_wrist_rfid_winner_01_neural_tendon_sleeve.glb` | 201 | 1 | wrist |
| 45 | ~~BCI headband~~ `godot/assets/models/prop_bci_headband.glb` | 201 | 1 | small |
| 46 | ~~Super Wire spool~~ `godot/assets/models/prop_super_wire_spool.glb` | 201 | 1 | small |
| 47 | ~~Battery Charge pickup~~ `godot/assets/models/prop_pickup_battery_charge.glb` | 201, 203 | 2 | small |
| 48 | ~~Thermal Jelly~~ `godot/assets/models/prop_jelly_01.glb` | 201 | 1 | small |
| 49 | ~~Sprocket~~ `godot/assets/models/char_bot_r2_05_livery_01_sprocket.glb` | Maintenance | 1 | 0.78 × 0.77 × 1.03 |
| 50 | ~~Sweep (stuck)~~ `godot/assets/models/char_bot_r2_05_livery_02_sweep.glb` | 204 | 1 | same |

## Counts (rev C.2a)
- **Item numbers 1–55.**
  - Moved out (kept, not deleted): **6**. #17, #26, #31 go to the lab/workshop building, #29 to the lab building, #33 to the exterior, and #24 to a future building (TBD; Rook's Bench Niche, `locker_run_bench_niche.glb`).
  - Dropped: **1** (#52).
  - New: #53, #54, #55.
- **Active in the residential building: 48.**
- **Already modeled (struck through): 35.** #1–5, 7–16, 19–22, 25, 27, 28, 30, 32, 34, 35, 37, 44–51, each glb verified in `godot/assets/models/`.
- **Still to model: 13** (#6, 18, 23, 36, 38–43, 53, 54, 55). Of these, #40 and #42 exist as level blockouts.

## Suggested modeling order (remaining items, most reused first)
1. Window cards #6 (8; iterations and combos exist in `design/assets/window_card/`, no glb in models yet)
2. Floor pad #40 (3), coupler arm #41 (3)
3. Folding counter #38 (2), lab crate #53 (2, shared with exterior #48), removal decals #54
4. Singles: suit storage #23, laundry bench #39, lost-and-found + notice board #55 (kitbash), clutter kit #36, substation #42, spares shelf #43, reading nook #18
5. Off-building (deferred): lab bench #17, workbench #26, specimen rack #29 (glb done), emitter repair bench #31, lockers #24 (Bench Niche glb done)
