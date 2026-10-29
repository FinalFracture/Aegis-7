# #7 Riser shaft + sealed wall chase (v1.1)
Generator: `assets/src/riser_generator.py`. glb: `godot/assets/models/riser_shaft.glb`, 1,904 tris, closed meshes, panels closed, not placed anywhere. Sheet: `final_riser_sheet.png`. Its last view is an open-panel iso, rendered only.

- **Origin:** the building plan origin, the same as #3–#5. X is axial, Y is up from the L1 finished floor, and +Z is spinward.
- **Position:** X 0.6..1.6, Z 2.4..3.4, Y 0..8.8, taken from `RISER` in `residential_stair_core_v1.py` and in `residential_floorplan_rev_c.py` (78af7a0). It is the same XZ in Maintenance (L1) and 202 (L2). The access panels stand 0.039 m proud of the east face X 1.6.
- **Lift #51 gap:** the riser's south face Z 2.4 is the shaft's north face (shaft X 0.6..2.2, Z 0.8..2.4). The gap is 0.000 m with no overlap; the plan has them touching by design ("services stack").
- **Shell:** white composite, 40 mm, sealed.
- **Fire stops:** gunmetal fire-stop plates at the L2 slab crossing (Y 3.9 and 4.2), the base and the roof soffit.
- **Services:** water and reclaim pipes, 3 power conduits, 4 data conduits (violet), and an air duct.
- **Spin-down:** gunmetal clamp rails and collars about every 1.1 m.
- **Per level:** a bolted gunmetal access panel on the east face, with an amber latch and a green status light above it. A Sprocket service port at 0.45 m above each floor (Y 0.45 and 4.65) has an amber ring.
