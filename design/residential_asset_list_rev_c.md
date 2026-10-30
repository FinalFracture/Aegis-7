# Residential rev C: Asset List (Vance, Oct 29 2026)
Source: approved rev C floor plans and room layouts (`residential_roomlayout_rev_c_L1/L2.png`). Checked against `godot/assets/models/` (15 glb files) and `scripts/preface_playable_area.gd`.
~~Struck through~~ = already modeled as a glb (path cited). "Level blockout" = exists only as primitives built in the level script, so it still needs a glb.
Sizes are rough W × D × H in meters.

## A. Doors and building fixtures
| # | Item | Units | Qty | Size |
|---|---|---|---|---|
| 1 | ~~Force-field door frame~~ `godot/assets/models/rfid_forcefield_door.glb` | all 10 units + Sector-4 exit | 11 | 1.4 × 0.2 × 2.3 (Maint 2.0, exit 2.6) |
| 2 | ~~Bulkhead Hub~~ `godot/assets/models/door_hub_bulkhead.glb` | all doors | 11 | 0.40 × 0.20 × 0.80 |
| 3 | Switchback stair set: flight 1 16 R + flight 2 10 R (26 × 0.1615, T 0.28), south mid-landing Y 2.585, L1 bottom landing 2.4, L2 landing 4.1 (approved, `residential_stair_core_v1.md`) | stair core L1–L2 | 1 | 3.8 × 8.1 clear, 4.2 rise |
| 4 | Stair glass guards (laminated, clamped + latch pins) + handrails both sides (own colliders) | stair core | 1 set | ~15.5 m handrail at 0.9 H, ~11 m guard at 1.1 H |
| 5 | Skylight strip, over the stair void only (v1.1) | stair core roof, Z -8.9..-4.88 | 1 | 3.8 × 4.0 |
| 6 | Lit window interior card | 8 apartments | 8 | 3.0 × 1.5 quad |
| 7 | Riser shaft + sealed wall chase (re-aligned v1.1: X 0.6..1.6, Z 2.4..3.4 on both levels) | Maintenance, 202 | 1 | 1.0 × 1.0 × 8.8 |
| 51 | Sprocket bot lift (v1.1, pending review): 1.2 × 1.2 × 1.4 car, 1.6 × 1.6 shaft, 2 shaft doors 1.0 × 1.3, 2 call panels in Bulkhead Hub style (reuses the `door_hub_bulkhead.glb` mesh with a lift glyph), controller cabinet | Maintenance SW / 202 SW, opens to corridor L1 + L2 | 1 set | shaft 1.6 × 1.6 × 6.6 |


## B. Bath and hygiene
| # | Item | Units | Qty | Size |
|---|---|---|---|---|
| 8 | Bath pod (shower, WC, sink module) | 101–104, 201–204 | 8 | 2.2 × 2.2 × 2.4 |


## C. Kitchen and dining
| # | Item | Units | Qty | Size |
|---|---|---|---|---|
| 9 | Kitchen counter + hob (modular run) | 101–104, 201–204 | 8 | 3.5 × 0.6 × 0.9 |
| 10 | Small dining table | 101, 104, 201, 204 | 4 | 1.2 × 0.8 × 0.75 |
| 11 | Dining table for 4 | 103, 202 | 2 | 1.6 × 0.9 × 0.75 |
| 12 | Tea table (low) | 102, 203 | 2 | 1.2 × 0.8 × 0.45 |
| 13 | Dining chair/stool | tables above | 20 | 0.45 × 0.45 × 0.9 |
| 14 | Tea set (pot + cups) | 102, 203 | 2 | 0.4 × 0.3 × 0.2 |


## D. Living
| # | Item | Units | Qty | Size |
|---|---|---|---|---|
| 15 | Sofa | 101, 103, 201, 202, 203, 204 | 6 | 2.5 × 0.9 × 0.85 |
| 16 | Armchair / reading chair | 102, 203 | 2 | 1.0 × 1.0 × 1.0 |
| 17 | Lab bench | 104 | 1 | 2.5 × 0.9 × 0.9 |
| 18 | Window reading nook bench | 203 | 1 | 4.0 × 0.4 × 0.5 |


## E. Sleeping and storage
| # | Item | Units | Qty | Size |
|---|---|---|---|---|
| 19 | Double bed | 101, 102, 103, 104, 201, 202, 203, 204 | 8 | 2.0 × 1.6 × 0.6 |
| 20 | Kids' bunk | 103, 202 | 2 | 0.9 × 1.9 × 1.7 |
| 21 | Wardrobe | 101, 103, 104, 201, 202, 203, 204 | 7 | 0.5 × 2.5–3.0 × 2.1 |
| 22 | Coat and storage closet | 103, 104, 203, 204 | 4 | 3.7 × 0.5 × 2.1 |
| 23 | Suit hook + storage with pressure suit | 102 | 1 | 0.5 × 2.5 × 2.1 |
| 24 | Resident lockers | Laundry | 1 run | 4.8 × 0.5 × 2.0 |


## F. Workstations and story props
| # | Item | Units | Qty | Size |
|---|---|---|---|---|
| 25 | Tool wall panel (pegboard, cable variant) | 101, 201, Maintenance | 3 | 2.5–3.5 × 0.5 × 2.0 |
| 26 | Apartment workbench (level blockout `Apartment_Workbench`) | 201 | 1 | 3.7 × 2.5 nook |
| 27 | Task lamp (level blockout `Apt201_Workbench_TaskLight`) | 201, 104, 204 | 3 | 0.2 × 0.2 × 0.5 |
| 28 | Window desk + data slates | 104, 204 | 2 | 4.0 × 0.4 × 0.75 |
| 29 | ~~Specimen shelf~~ MOVED TO LAB BUILDING (Jared, Oct 29): removed from 104; Open Rack is a future science/lab-building asset, `godot/assets/models/specimen_rack_open_lab.glb` | ~~104~~ lab building | — | 0.9 × 0.63 × 1.9 |
| 30 | Telescope | 104 | 1 | 0.6 × 0.6 × 1.5 |
| 31 | Emitter repair bench (dismantled field emitter) | 204 | 1 | 0.9 × 1.9 × 0.9 |
| 32 | Cycler route model (wall) | 203 | 1 | 0.9 × 0.2 × 1.0 |
| 33 | ~~Hydro planter (window/balcony)~~ MOVED TO EXTERIOR (Jared, Oct 29): removed from 103/202; Tiered Steps planter now serves the hydro co-op / sidewalk planters, `godot/assets/models/hydro_planter_tiered_exterior.glb` | ~~103, 202~~ exterior | — | 4.0 × 0.4 × 0.7 |
| 34 | Potted plants set (Jared's final pick, Oct 29): `godot/assets/models/potted_plants_rail_cradles.glb` (default 102) and `godot/assets/models/potted_plants_pocket_column.glb` (default 203). SUPERSEDED, kept unplaced: `potted_plants_moulded_trio.glb`, `potted_plants_shared_tray.glb` | 102, 203 | 2 | 1.20 × 0.55 × 0.25 (wall rail) / 0.90 × 0.78 × 0.41 |
| 35 | Toy chest + rail bins + toy kit (Jared combined iter 1 + 3, Oct 29): `godot/assets/models/toy_chest_rail_bins.glb` | 103 | 1 | 1.2 × 0.6 × 0.5 chest; bins on a 0.90 m rail to 1.21 m |
| 36 | Small clutter kit (meal tray, cups, cables, photo frames as decals) | 101, 102, 104, 202 | 1 kit | small |


## G. Laundry
| # | Item | Units | Qty | Size |
|---|---|---|---|---|
| 37 | Washer/dryer stack | Laundry | 4 | 0.8 × 0.8 × 1.9 |
| 38 | Folding counter | Laundry | 1 | 0.6 × 3.5 × 0.9 |
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

## Counts
- **Total items: 51** (#51 bot lift added in stair core v1.1). Already modeled as glb: **9** (#1, 2, 44–50). Still to model: **42**, of which 4 exist only as level blockouts (#26, 27, 40, 42).

## Suggested modeling order (most reused first)
1. Dining chair (20), window cards (8), bath pod (8), kitchen counter (8), double bed (8)
2. Wardrobe (7), sofa (6), the three table variants (8 total), coat closet (4), washer/dryer stack (4)
3. Repeated small items: tool wall (3), task lamp (3), floor pad (3), coupler arm (3)
4. Building fixtures: stair set, rail, skylight, riser, bot lift (#51)
5. Pairs: kids' bunk, armchair, window desk, plants, tea set
6. Singles and story pieces: workbench, substation, lockers, laundry counter/bench, spares shelf, suit storage, lab bench, specimen shelf, telescope, emitter bench, Cycler model, toy bin, reading nook, clutter kit
