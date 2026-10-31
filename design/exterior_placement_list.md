# Residential exterior — promoted asset placement list (Rook, Oct 31 2026)
World axes: X axial (fore -X / aft +X), +Z spinward, -Z antispinward (promenade/canal side). y up. Paving top y 0.05, platform top y 0.30. All paths under `godot/assets/models/`. "Rot" = yaw about Y. **TBD = not decided anywhere in the docs; not invented here.**

| # | Asset | File | Transform | Count / repeat | TBD |
|---|---|---|---|---|---|
| 15 | Tram (maglev) shelter, 05 Glass Pavilion | `ext_tram_shelter.glb` | y 0.297; footprint X 12..18, Z -16.9..-15.6 (centre X 15.0, Z -16.25) | 1 | rot (facing) TBD |
| 16 | Platform kerb, 02 Cyan Tactile | `ext_tram_platform_kerb.glb` | rot 180°, origin Z -17.55, y 0; front face Z -18.5 | 6 on platform X 9..21 | per-kerb X origins TBD (2.0 m modules suggest X 10,12..20, unconfirmed) |
| 17 | Maglev guideway, 01 T-Beam | `ext_maglev_guideway.glb` | rot 0, origin Z -20.077, y 0; track centre Z -19.90; 10 m X pitch | modules along the run | run start/end X and module count TBD |
| 19 | Maglev car body, 01 Civic Pearl Classic | `ext_maglev_car_body.glb` | car 1: (Xc-0.069, 0.06, -19.90) rot 0; car 2: rot 180 at Xc2 = Xc-12.306, body (Xc2+0.069, 0.06, -19.90) | 2 cars (set 24.31 m) | Xc (where the car stands) TBD |
| 19 | Maglev magnet module | `ext_maglev_magnet_module.glb` | car 1: (Xc-0.30, 0.06, -19.90) rot 0; car 2: (Xc2+0.30, 0.06, -19.90) rot 180 | 1 per car | Xc TBD (as above) |
| 41 | Curb segment, 01 Chamfer Slate | `ext_curb_segment.glb` | y 0 on paving base; 3 mm joints | edging for planter beds + guideway corridor (Atlas PM) | all positions/runs TBD |
| 41 | Curb corner | `ext_curb_corner.glb` | as segment | at bed corners | positions TBD |
| 44 | Paving promenade, 04 Tactile Guidance | `ext_paving_promenade.glb` | y 0 (top 0.05), tiled | promenade X -47..47, Z -18.5..-9 | tile grid origin/pitch TBD |
| 44 | Paving plaza, 04 Tactile Guidance | `ext_paving_plaza.glb` | y 0 (top 0.05), tiled | plaza | plaza extents + tile grid TBD |
| — | Platform infill | `ext_platform_infill.glb` | origin (15.0, 0, -16.048), rot 0 | 1 | — |
| 45 | Kerb ramp, 02 Railed | `ext_kerb_ramp.glb` | origin (9.75, 0, -13.996), rot 0 | 1 | — |
| 46 | Canal edge, 05 Lit Coping | `ext_canal_edge.glb` | rot 180°, origin Z -25.8, y 0; 2.0 m X pitch | 47 (asset list) | run start/end X TBD |
| 47 | Desire-path decal, 05 Worn Tactile | `ext_desire_path_decal.glb` | y 0.053; 1.2 x 4.0 m segments chained along local Z (4.0 m pitch) | 2 (asset list) | diagonal end points (platform -> exit ramp at X ±1.8), yaw and segment count TBD |
| 49 | TS-4 wear decal, 02 Mismatched Pearl | `ext_ts4_wear_decal.glb` | identical transform to the TS-4 it dresses | 1 | which TS-4 gets the overlay TBD (dead one assumed, unconfirmed) |
| 49 | TS-4 dead foliage | `ext_ts4_dead_foliage.glb` | replaces the middle west-sidewalk TS-4: X -16.6, Z -2 (Atlas PM); same transform as that TS-4 (row 25: 4 m along Z, back to Spin St W kerb) | 1 | TS-4 yaw value TBD (not recorded) |
| 50 | Litter drift W1 | `ext_litter_drift_01.glb` | (-17.4, 0.05, -7.0), rot 0 | proposal | street X centre TBD (see note) |
| 50 | Litter drift W2 | `ext_litter_drift_03.glb` | (-17.4, 0.05, -3.5), rot 0 | proposal | " |
| 50 | Litter drift W3 | `ext_litter_drift_05.glb` | (-17.4, 0.05, +2.0), rot 0 | proposal | " |
| 50 | Litter drift E1 | `ext_litter_drift_02.glb` | (+17.4, 0.05, -7.0), rot 0 | proposal | " |
| 50 | Litter drift E2 | `ext_litter_drift_04.glb` | (+17.4, 0.05, -3.5), rot 0 | proposal | " |
| 50 | Litter drift E3 | `ext_litter_drift_03.glb` | (+17.4, 0.05, +2.0), rot 0 | proposal | " |
| 51 | Track scuff — guideway, 03 Boarding Wear | `ext_track_scuff_guideway.glb` | identical transform to each guideway module (rot 0, Z -20.077) | per module (or stop modules only) | every module vs stop-only TBD |
| 51 | Track scuff — kerb | `ext_track_scuff_kerb.glb` | identical transform to each platform kerb (rot 180°, Z -17.55) | per stop kerb | kerb X origins TBD (as #16) |

Notes
- #50: Atlas gave X ±17.4; the Spin St E bollards span X 17.9..22.1, so the walkway centre may be nearer ±20. Confirm before placing. Patches clear the bollards (Z -9.4) by ≥0.8 m and the nook (Z ≤ -9.6).
- Sprocket wheel-track decals (apron X 1..5.6, Z 9..11.65 + service door jamb at X 3.2) are kept, not in this list (no file yet; Sloane).
- Detailed per-asset notes: `design/assets/<asset>/NOTES.md`; layout script `residential_exterior_plan_v1.py` still needs road zones removed and these placements added (not edited).
