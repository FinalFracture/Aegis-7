# Table family (#10 small dining, #11 dining for 4, #12 tea): 5 iterations
Built with `python3 assets/src/table_family_generator.py`. Each family uses one design language across three sizes: small dining 1.2×0.8×0.75, dining for 4 1.6×0.9×0.75, tea 1.2×0.8×0.45 m. Length is along X, the pivot is bottom-center and Y is up. Files: `iter_0N_{small_dining,dining4,tea}.glb`, `iter_0N_sheet.png` (3 sizes × Top/Front/Side/Iso; the dining-4 Iso shows 4 swivel chairs), `overview.png`. Every part is a closed mesh.
**Shared logic.** Spin-down anchoring uses bolted gunmetal floor plates and clamps with amber lights (iter_03 also hooks onto a wall rail), as in the bed, sofa and wardrobe. Each table has an amber Sprocket service or charge port. Every table is flat-pack parts (moulded or printed white composite, extruded alloy, gunmetal plate) that can be repaired in-cylinder.

**Chair-fit check** against `dining_chair_swivel.glb` (seat top 0.479 m, base plate 0.34 m square, foot ring r = 0.181 m). Chairs are placed with the seat front 55 mm under the table edge, two per long side (x ±0.27 small, ±0.40 dining for 4). The numbers below are measured from the meshes:
- seat-to-top = 0.271 m for all dining sizes (target 0.27–0.30).
- Thigh clearance is from the seat top to the lowest table part over the knee zone.
- Base clearance is the plan gap from the chair's plate or foot-ring zone to any table part below 0.22 m. **No clashes.**

| iter | tris (small / dining4 / tea) | thigh clear (small / d4) | chair-base clear (small / d4) |
|---|---|---|---|
| 01 Moulded Pedestal | 496 / 848 / 496 | 0.236 / 0.236 | 0.269 / 0.319 |
| 02 Alloy Frame + Apron | 576 / 576 / 576 | 0.163 / 0.206 | 0.059 / 0.126 |
| 03 Wall-Rail End + T-Leg | 592 / 592 / 592 | 0.186 / 0.186 | 0.129 / 0.135 |
| 04 Slab Ends + Stretcher | 944 / 944 / 944 | 0.226 / 0.236 | 0.051 / 0.105 |
| 05 Spine Beam + Fork Feet | 960 / 960 / 960 | 0.236 / 0.236 | 0.099 / 0.099 |

## iter_01: Moulded Pedestal
A white moulded top with a violet edge band on one (small, tea) or two (dining for 4) white pedestals. Each pedestal sits on a gunmetal base with two tucked bolted clamps and has an amber Sprocket port on the column. The legs are central, so it has the most knee room and the biggest clearance from the chair bases. The pedestal is a single moulding, and the low centre of mass helps in spin-down.

## iter_02: Alloy Frame + Apron
A slate top with an alloy edge on four alloy legs, a gunmetal apron, bolted foot plates and a violet apron accent. The Sprocket port is in the front apron. It is a classic and very cheap extruded kit, but the apron reduces thigh room (0.163 m on the small size), and the corner legs sit closest to the chair bases (59 mm).

## iter_03: Wall-Rail End + T-Leg
One short end hooks onto an alloy rail on a bolted gunmetal wall plate with brackets. A single gunmetal T-leg with a clamped alloy foot carries the other end, with the Sprocket port and a violet strip on the leg. It is the strongest spin-down anchoring and frees one end of the floor, but it must go against a wall (the wall plane is at -X) and can only seat people on the long sides.

## iter_04: Slab Ends + Stretcher
White moulded slab end legs on gunmetal feet with tucked clamps, plus a high gunmetal stretcher with a violet line and the Sprocket port on one slab. It reads like the bed and kitchen white-shell family. The slab feet sit 51 mm from the chair bases on the small size, which is tight but clear.

## iter_05: Spine Beam + Fork Feet
A slate top with an alloy inlay over a gunmetal torsion-box spine (with a green status light and the Sprocket service bay). The spine sits on two forked alloy feet with clamps. It is rigid, light and easy to print and bolt, and everything is kept on the centreline, so chairs can sit anywhere.

**Recommendation:** iter_01, the Moulded Pedestal. It has the best chair fit (no apron, central bases about 0.27–0.32 m from the chair clamps), it matches the white-shell family, and the same pedestal scales cleanly to the tea table.
