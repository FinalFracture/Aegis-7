# Door lab pass C: Rook hardware upgrade (Vance REALISM_SPEC §9, a84b576)

Run: `python3 assets/src/door_lab/door_lab_passC.py` builds all 15 variants, exports them, runs QA (`passC_qa.json`) and renders to `/workspace/renders/doorlab_passC/`.
V1 of each asset is also written to `godot/assets/models/door_lab/door_lab_<asset>.glb`. Variants go to `assets/glb/door_lab/<asset>/v1..v5.glb`.
Approach side = -Z for every asset. LH variants are X-mirrors: rotations about local Y/Z and translations along local X flip sign. The slider handed variants swap the _L/_R names, so `leaf_L` stays the -X leaf and no sign flips.

## Variants (visual tris, budget < 6000)
| asset | v1 (placed) | v2 | v3 | v4 | v5 |
|---|---|---|---|---|---|
| bulkhead_hatch | RH 150 coaming 5766 | LH 5766 | RH 300 coaming 5776 | LH 300 5776 | RH, 6 ribs + kick 5960 |
| biparting_slide | panel shown swung up 5808 | panel closed 5808 | no panel (service) 5568 | v1 handed 5808 | v2 handed 5808 |
| floor_hatch | RH stay, 0.45 well 4370 | LH 4370 | RH 0.75 well 4370 | LH 0.75 4370 | RH 0.30 well 4370 |

## Animated nodes (pivot on the axis, closed pose = modelled)
**bulkhead_hatch** (recenter shift z +0.0725; pass B was +0.0745)
- `leaf`: group on the hinge axis (0.65, -, 0.1585). Open = about +Y, +100°.
- `bulkhead_LockWheel`: about local Z, +90° (dogs thrown).
- `bulkhead_OverrideOrange_Handwheel`: coaxial, about local Z, 4320° (12 turns) for full throw.
- `bulkhead_Dog_01..08` / `bulkhead_Linkage_01..08`: local +X, +0.025 m.
- `bulkhead_InflatableSeal`: scale local Z ×1.385 when inflated (8 mm compression).
- `bulkhead_PushOffRam_1/2`: +Z 0.012 m.
- `bulkhead_Damper_body` (root) / `bulkhead_DamperRod` (leaf child): each aims local -Z at the other.
- `bulkhead_Gauge_needle_front/back`: about local Z, -270/110 (front) / +270/110 (back) deg per kPa.
- `bulkhead_EqualizeLever` (approach face): about local Z, -90°.

**biparting_slide**
- `leaf_L` / `leaf_R`: X -1.000 / +1.000 m.
- `slide_roller_*`: spin about local Z by travel/r (r 0.030; antilift r 0.015, opposite sign). Gage's `_tag_rollers` is unchanged.
- `slide_SolenoidBolt`: +Z 0.018 m (locked).
- `slide_HexRelease_socket`: about local Z, 90° (manual release).
- `slide_AccessPanel`: about local X; closed to open is +90°. V1 bakes the open pose, so closing from V1 is -90°.
- `slide_Keeper` rides on leaf_L.

**floor_hatch** (finished floor plane = GLB y 0.462; opening centred on GLB x/z = 0)
- `hatch_leaf`: group on the hinge axis (0, 0.446, -0.524). Open = about local +X, -105°.
- `hatch_LockWheel`: about local Y, +90°.
- `hatch_OverrideOrange_Handwheel`: about local Y, 4320°.
- `hatch_OverrideOrange_Lever`: about local Z, +70°.
- `hatch_Dog_01..04` / `hatch_Linkage_01..04`: local +X, +0.025 m.
- `hatch_InflatableSeal`: scale local Y ×1.208 (4 mm compression).
- `hatch_strut_L/R_body` (root) / `_rod` (leaf child): each aims local +Z at the other.
- `hatch_stay_arm` (root): about local X. Table at 0..105° in 15° steps: 0, -20.5, -39.25, -55.94, -70.42, -82.73, -93.11, -101.91°.

## QA (`passC_qa.json`)
- All 15 variants pass:
  - Clip check at every key pose: no bad overlaps, no coplanar faces, no open meshes.
  - Motion sweeps: worst penetration ≤ 0.1 mm.
  - Tri budget.
- Floor hatch:
  - Leaf top flush with the flange: 0.0 mm.
  - Liner clear opening measured 0.900 × 0.900 m (rays at -0.15 and -0.30 m).
  - Dog keepers sit in pockets behind the liner.
- Known spec conflict: the hinge-side counterbalance hardware sits inside the 0.90 prism. That covers the strut and stay frame clevises (up to 82 / 105 mm from the hinge-side liner, 0.12–0.18 m below the floor) and, at full open, the strut bodies and the stay arm (≤ 94 mm, up to 0.26 m above the floor). The cause is the hinge geometry: with the axis 24 mm outboard of a 1.00 m leaf, the open leaf's underside sits on the liner line, so any strut between that underside and the frame lies in front of it.
