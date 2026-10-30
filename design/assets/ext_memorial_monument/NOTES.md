# ext_memorial_monument_01..05 (Rook, Oct 30, from Jared's 12:41 PM CT brief)
Monumental #29 candidates. The old ext_memorial_tag_rack_01..05 files are kept. Not promoted and not in VOTE_LOG.

## Ledges for #30 violet field lamp and #31 offering set (model space, +Z = front)
- 1 plinth front ledge 3.8 x 0.6 m at y 0.30 (z -0.10..+0.50; lowest tags end ~y 0.92): lamp at x +1.5, offering at x -0.6
- 2 tier-1 side ledges y 0.32, 0.45 x 1.6 m each (x +-1.35..1.8; pylons only at the back corners z < -0.55): lamp on the left ledge at x -1.57, z +0.3; offering on the right ledge turned 90 deg at x +1.57, z +0.15 (front strips are only 0.2 m deep)
- 3 base plinth 3.2 x 1.2 at y 0.20, clear front strips z +0.25..+0.6 either side of the cradle: lamp at x +1.2, offering at x -1.1
- 4 open floor plate 3.8 x 1.2 at y 0.06; outer cables stop at y ~2.6 so the plate ends are clear: lamp at x -1.4, offering at x +1.2 (z +0.3)
- 5 plinth top 2.44 x 1.0 at y 0.96 either side of the bowl (x +-0.35..1.2): lamp at x +0.9, offering at x -0.85; floor in front (z > 0.62) also clear

## SE corner nook clearance (checked against design/residential_exterior_plan_v1.py data)
- The current nook is X 15.0..16.6, Z -11.8..-10.2 (1.6 x 1.6 m). Every candidate is 3.6-3.9 m wide and 1.0-1.6 m deep, so **the nook bounds need to grow**.
- **In place** (centred X 15.8, back at Z -9.2, facing -Z toward the promenade): the plan QC finds no object or clear-zone overlaps (candidate 2's 1.2 m apron touches the nook bench). However:
  - the footprint X ~13.9..17.7 sits right across the mouth of the E sidewalk (X 14..17), where it meets the promenade at Z -9;
  - it is 0.2 m from the building corner (X 14, Z -9).
  - A 4 m wall there blocks the sidewalk-to-promenade walk line.
- **Recommended:** shift east to X 17.4..21.6, Z -12.4..-9.6 (4.2 x 2.8 m: monument back at Z -9.7, 0.2 m south of the Spin St E end bollards at Z -9.5..-9.3, plus a 1.2-1.5 m visitor apron).
  - QC is clean for all 5 candidates: no object, clear-zone or off-walk hits.
  - The promenade through-walk (Z -15.4..-12.5) stays clear.
  - Move the nook bench and bin onto the apron's south edge (for example bench X 18.6..20.4, Z -12.4..-11.9).
- Placement: rotate 180 deg (model +Z front -> world -Z) so the monument faces the promenade and canal.

## ext_memorial_aegis_01..05 (Rook, Oct 30, 12:58 PM CT round): memorial with a scaled Aegis-7 habitat
Reference: PROJECT.md line 4 (800 m long x 400 m dia, 2:1) and design/cylinder_interior_overhaul_spec.md S3/S4 (520 m spin drum R 200 with forward hemispherical endcap/docking bowl; 45-deg chamfered gunmetal aft baffle; counter-rotating 280 m aft starport + 5-coil fusion drive, collar R 45..75; three 120-deg valleys alternating with solarium strips). Generator: assets/src/ext_memorial_aegis_generator.py. Ship length 2.4–3.2 m (1:333 to 1:250).
| # | Concept | Tris | W x D x H (m) | Clip | Lamp / offering ledge |
|---|---|---|---|---|---|
| 01 | Held aloft on a titanium stele | 888 | 3.20 x 1.26 x 4.26 | PASS | plinth top y 0.35: lamp x +1.2 z +0.3, offering x -1.0 z +0.3 |
| 02 | Halo ring cradle, RFID tags under the ship | 2,192 | 3.70 x 1.40 x 4.00 | PASS | base y 0.30, front strip outside the ring: lamp x +1.3, offering x -1.25 |
| 03 | Tiered plinth, violet light seams | 904 | 3.60 x 1.50 x 2.69 | PASS | tier-1 side ledges y 0.30: lamp x -1.62 z +0.3, offering x +1.62 (turned 90 deg) |
| 04 | Cutaway (open front-upper quarter: valleys, axial sun spine) | 1,080 | 3.40 x 1.50 x 2.47 | PASS | plinth top y 0.70: lamp x +1.45, offering x -1.2 z +0.45 |
| 05 | On a beam over a violet/titanium tag curtain | 5,064 | 3.80 x 1.26 x 4.28 | PASS | floor plate y 0.06: lamp x -1.45, offering x +1.2 z +0.3 |
Nook fit (plan v1.3: X 17.4..21.6, Z -12.7..-9.6, centred X 19.5, back Z -9.7, rot 180): widest 05 spans X 17.6..21.4; deepest (03/04, 1.5 m) front at Z -11.2, so 1.0 m to the nook bench (Z -12.2), which is >= 0.9; all <= 4.3 m high. Cutaway 04 drum parts are separate nodes (Drum_*, Valley_*, Axial_Sun_Spine) so Godot can spin them about the X axis at y 1.70.

### ext_memorial_aegis_04b (Jared's pick of 04, 1:15 PM CT, + tags inside; awaiting approval, not promoted)
200 RFID tags (about 35% violet, the rest titanium) hang on 8 titanium wires strung between the bulkhead discs at r 0.22 m around the axial sun spine. Each tag hangs radially outward, the drum's spin-gravity "down", and is visible through the open cut. Node tree: Drum_Spin (translation 0, 1.70, 0 = drum axis) → 11 children (drum hull/glass, valleys, spine, bulkheads, Tag_Wires, Tags_Violet, Tags_Ti). Rotate Drum_Spin about its local X axis. Starport_Spin is on the same axis for the counter-rotating starport. 4,472 tris, 3.40 W × 1.50 D × 2.47 H, clip PASS (worst overlap 0.008). Same footprint as 04, so the v1.3 nook fit is unchanged. Generator: assets/src/ext_memorial_aegis_04b_generator.py.
