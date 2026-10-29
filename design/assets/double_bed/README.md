# Double bed (#19): 5 iterations
Built with `python3 assets/src/double_bed_generator.py`, reusing the dining chair / bath pod / kitchen rasterizer, glb writer, emissive tone-mapping and the object-only exposure lift that makes whites read white. There are 8 beds needed (101–104, 201–204).
Each bed is about 1.6 W × 2.0 L m with the foot at +Z, the headboard at -Z and the pivot bottom-center. The mattress, duvet and pillows are smooth-shaded cushion lofts in matte fabric (roughness 0.9: off-white, warm grey or slate). Files: `iter_0N.glb`, `iter_0N_sheet.png` (Top, Front, Side, Iso), `overview.png`. Every part is a closed mesh.

## iter_01: Moulded Platform + Drawers (1,376 tris; headboard 0.8 m)
A white moulded-composite platform on a recessed gunmetal plinth, with a violet band at the foot, a low moulded headboard and four latched side drawers (Drawer_L1/L2/R1/R2) with amber latch lights. It is one moulded shell plus drop-in drawers, so it is easy to print and swap in-cylinder. Under spin-down, the latches hold the storage shut and the plinth bolts down.

## iter_02: Alloy Frame + Strap Restraint (1,968 tris; headboard 1.0 m)
A folded brushed-alloy frame with gunmetal slats and a padded slate headboard. Each leg stands on a bolted gunmetal foot plate (Anchor_Feet / Anchor_Bolts). Two gunmetal Restraint_Straps run across the duvet and clip to the side rails with amber buckle lights, which is the most explicit spin-down sleeper restraint. The slats and frame are flat-pack parts that are easy to repair.

## iter_03: Wall-Anchored Cantilever (1,376 tris; headboard pod 1.05 m)
The bed hangs from a gunmetal strongback on the wall with bolted brackets, and the front has no legs. The tall white headboard pod has a shelf, green reading lights and an alloy rail, matching the wall-pod kitchen. Anchoring sits inside the wall structure, and the clear floor underneath is easy to clean and gives Sprocket access. The under-deck tray is the storage.

## iter_04: Low Platform + Floor Clamps (1,376 tris; headboard 0.55 m)
A low slate platform 0.18 m high with a lift-up warm-grey deck that opens to storage, held by four gunmetal corner floor clamps with bolt heads and amber clamp lights, and a thin futon-style mattress. The low centre of mass and positive clamps make it the calmest option during spin-down. It is a simple slab-and-clamp build.

## iter_05: Capsule Bed + Canopy (1,684 tris; canopy 1.1 m)
A white moulded tub with raised slate side bolsters, latched side drawers and an arched partial canopy over the head end. The canopy has a violet band and an amber reading-light strip. The bolsters and canopy keep the sleeper centred and sheltered when gravity changes. It matches the capsule bath pod's moulded language.

**Recommendation:** iter_01 (Moulded Platform + Drawers) is the cleanest fit with the white-composite family and has the most storage. If restraint should read strongly, iter_02 is the pick.

## Final: Moulded Platform + Floor Clamps (1,904 tris)
This combines iter_01 with iter_04's clamps, built with `python3 assets/src/double_bed_generator.py final`. It is exported only to `godot/assets/models/double_bed_moulded_clamped.glb`, and the sheet is `final_moulded_clamped_sheet.png`.
- **Footprint:** the white moulded Shell (bevelled, rounded corners) is 1.6 × 2.0 m. Overall it is 1.68 × 2.08 m including the floor plates. The mattress top is at 0.54 m and the Headboard at 0.8 m.
- **Clamps:** the gunmetal Base is recessed. Four hard-edged gunmetal Clamp_* feet sit inside the plan outline under the shell corners, each on a bolted FloorPlate_* that sticks out 40 mm, with an amber clamp light.
- **Drawers:** four latched Drawer_* (L1/L2/R1/R2) with amber latches and alloy pulls sit between the clamps (z -0.57 to 0.77 vs plates from ±0.86), so they have a clear outward pull path.
- **Materials:** violet FootBand, smooth-shaded fabric Mattress/Duvet/Pillow_L/R (non-metal, roughness 0.9). Every part is a closed mesh.
