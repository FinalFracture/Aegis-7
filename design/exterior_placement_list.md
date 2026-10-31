# Residential exterior — promoted asset placement list (Rook, Oct 31 2026)
World axes: X axial (fore -X / aft +X), +Z spinward, -Z antispinward (promenade/canal side). y up. Paving top y 0.05, platform top y 0.30. All paths under `godot/assets/models/`. "Rot" = yaw about Y. Numbers are the placements in `residential_exterior_plan_v1.py`.

| # | Asset | File | Transform | Count / repeat | Resolved |
|---|---|---|---|---|---|
| 15 | Tram (maglev) shelter, 05 Glass Pavilion | `ext_tram_shelter.glb` | (15, 0.297, -16.25), rot 180; open side (local +Z) faces the guideway. Footprint X 12..18, Z -16.9..-15.6 (centre X 15.0, Z -16.25) | 1 | rot 180, open side to the guideway |
| 16 | Platform kerb, 02 Cyan Tactile | `ext_tram_platform_kerb.glb` | rot 180, y 0, origin Z -17.55; front face Z -18.5; X 10, 12, 14, 16, 18, 20 | 6 on platform X 9..21 | X 10..20 step 2 |
| 17 | Maglev guideway, 01 T-Beam | `ext_maglev_guideway.glb` | rot 0, y 0, origin Z -20.077; track centre Z -19.90; X -45..45 step 10 | 10 | X -45, -35, -25, -15, -5, 5, 15, 25, 35, 45 |
| 19 | Maglev car body, 01 Civic Pearl Classic | `ext_maglev_car_body.glb` | pair centred on shelter X 15. Xc=21.153, Xc2=8.847. Car 1 (21.153, 0.06, -19.90) rot 0; car 2 (8.847, 0.06, -19.90) rot 180 | 2 cars (set 24.31 m) | centred on shelter X 15 at the stop |
| 19 | Maglev magnet module | `ext_maglev_magnet_module.glb` | car 1 (20.922, 0.06, -19.90) rot 0; car 2 (9.078, 0.06, -19.90) rot 180 | 1 per car | offset from the body, shifted with it |
| 41 | Curb segment, 01 Chamfer Slate | `ext_curb_segment.glb` | y 0; pitch 1.997 m (segment 1.994 m, 3 mm joints); centreline 0.152 m outside the bed edge; rot 0 along X, rot 90 along Z | 168 placed (de-duped Oct 31, was 270) | runs listed below; segments fit inside each edge (no overhang) |
| 41 | Curb corner | `ext_curb_corner.glb` | y 0, rot 0, at each merged bed's four outside corners (offset 0.152 m out on both axes) | 40 (was 100) | same beds as the segment runs |
| 44 | Paving promenade, 04 Tactile Guidance | `ext_paving_promenade.glb` | y 0 (top 0.05); 2 m grid, origin corner (9, -18.5) | other walkways | promenade on the other walkway cells of that grid |
| 44 | Paving plaza, 04 Tactile Guidance | `ext_paving_plaza.glb` | y 0 (top 0.05); same 2 m grid; centres inside X 9..18, Z -25.6..-12.5, skipping guideway, platform, shelter, kerb ramp, and platform infill | 14 | grid origin (9, -18.5); plaza X 9..18, Z -25.6..-12.5 |
| — | Platform infill | `ext_platform_infill.glb` | origin (15.0, 0, -16.048), rot 0 | 1 | — |
| 45 | Kerb ramp, 02 Railed | `ext_kerb_ramp.glb` | origin (9.75, 0, -13.996), rot 0 | 1 | — |
| 46 | Canal edge, 05 Lit Coping | `ext_canal_edge.glb` | rot 180, y 0, origin Z -25.8; X -46..46 step 2 | 47 | X -46..46 step 2 |
| 47 | Desire-path decal, 05 Worn Tactile | `ext_desire_path_decal.glb` | y 0.053; from kerb-ramp foot (9.75, -13.996) to Sector-4 exit ramp foot (0, -11.65); length 10.028 m; yaw -76.4710° (local +Z along the line). Centres (7.8055, -13.5281), (3.9165, -12.5924), (0.0275, -11.6566) | 3 × 4 m | yaw along the line |
| 49 | TS-4 wear decal, 02 Mismatched Pearl | `ext_ts4_wear_decal.glb` | (-16.6, 0, 0), rot 90; same transform as the dead foliage | 1 | dresses the dead middle-west TS-4 |
| 49 | TS-4 dead foliage | `ext_ts4_dead_foliage.glb` | (-16.6, 0, 0), rot 90; replaces the middle west TS-4 (hydro planter W, Z -2..2; 4 m along Z, back local -Z to Spin St W kerb X -16.8) | 1 | rot 90 at (-16.6, 0, 0) |
| 50 | Litter drift W 01 | `ext_litter_drift_01.glb` | (-20, 0.05, -7), rot 0 | 1 | Spin St W centre X -20 |
| 50 | Litter drift W 03 | `ext_litter_drift_03.glb` | (-20, 0.05, -3.5), rot 0 | 1 | Spin St W centre X -20 |
| 50 | Litter drift W 05 | `ext_litter_drift_05.glb` | (-20, 0.05, 2), rot 0 | 1 | Spin St W centre X -20 |
| 50 | Litter drift E 02 | `ext_litter_drift_02.glb` | (20, 0.05, -7), rot 0 | 1 | Spin St E centre X 20 |
| 50 | Litter drift E 04 | `ext_litter_drift_04.glb` | (20, 0.05, -3.5), rot 0 | 1 | Spin St E centre X 20 |
| 50 | Litter drift E 03 | `ext_litter_drift_03.glb` | (20, 0.05, 2), rot 0 | 1 | Spin St E centre X 20 |
| 51 | Track scuff — guideway, 03 Boarding Wear | `ext_track_scuff_guideway.glb` | identical transform to guideway modules at X 5, 15, 25 (rot 0, y 0, Z -20.077) | 3 | stop at shelter X 15, plus one module either side |
| 51 | Track scuff — kerb | `ext_track_scuff_kerb.glb` | not placed | 0 | no kerb scuffs |

Notes
- Resolved 2026-10-31 (Gage). Former open items are the numbers `design/residential_exterior_plan_v1.py` writes. Rule 12: #51 scuffs only on guideway X 5, 15, 25.
- #41 curb runs, de-duped 2026-10-31 (Rook) — one curb per edge, none where the platform kerb is. Y unchanged (all 0; Gage snaps at spawn). Verified by `design/verify_curb_overlaps.py`: 0 curb-curb, 0 curb-kerb.
  - Planter S: the two rows of 5 planters (0.2 m gaps) are each ONE bed outline: X -13.8..-3.0 and 3.0..13.8, Z -10.0..-9.1. South 5 + north 5 segments + 4 corners each.
  - Planter N: X -13.8..-0.8 (6 + 6 segments) and X 8.0..14.0 (3 + 3), Z 9.1..10.0, + 4 corners each.
  - Hydro planter W ×3 (1 m gaps, kept separate): X -16.8..-15.4; Z -7..-3, -2..2, 3..7. West 2 + east 2 + 4 corners each.
  - Hydro bed ×3: X -13..-3; Z 19.5..20.4, 21.5..22.4, 23.5..24.4. South 5 + north 5 + 4 corners each.
  - Short ends (0.9 m bed ends, 1.4 m hydro-planter ends) carry corners only: a 1.994 m segment can't fit between the corners. Runs are centred, leaving < 1 pitch split between the two ends.
  - Guideway north X -47..9 at Z -18.352: 28 segments. Guideway north X 21..47: 13. Guideway south X -47..47 at Z -21.802: 47. None in the kerb span X 9..21.
  - Placed: 168 segments, 40 corners (was 270 + 100).
- #19: Xc = 15 + 12.306/2 = 21.153, Xc2 = Xc - 12.306 = 8.847, so the two-car set is centred on the shelter at X 15. Body x is Xc and Xc2. Magnets keep their offset from the bodies (20.922 and 9.078).
- #44: grid corners sit on (9, -18.5) with a 2 m pitch. Plaza is that grid inside X 9..18, Z -25.6..-12.5 (14 tiles after the skips above). Promenade is the other walkway cells on the same grid (walk, and not building, plot, green, water, guideway, or a solid object).
- #47: three 4 m segments cover the 10.028 m line. Centres are 2 m, 6 m, and 10 m from (9.75, -13.996). The Sector-4 entrance at Z -9 is up the exit ramp from (0, -11.65).
- #49: the middle west TS-4 is the hydro planter whose box is Z -2..2. Dead foliage replaces it at the box centre (-16.6, 0, 0), rot 90. The wear decal uses that same transform.
- #50: Spin St W is X -23..-17, centre -20 (W 01 / 03 / 05). Spin St E is X 17..23, centre +20 (E 02 / 04 / 03). Z -7 / -3.5 / +2, y 0.05, rot 0. Patches clear the bollards (Z -9.4) by ≥0.8 m and the nook (Z ≤ -9.6).
- Sprocket wheel-track decals (apron X 1..5.6, Z 9..11.65 + service door jamb at X 3.2) are kept, not in this list (no file yet; Sloane).
- Detailed per-asset notes: `design/assets/<asset>/NOTES.md`. Placements come from `design/residential_exterior_plan_v1.py`.
