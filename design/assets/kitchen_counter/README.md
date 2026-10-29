# Kitchen counter + hob (#9): 5 iterations
Built with `python3 assets/src/kitchen_counter_generator.py`, which reuses the loft, glb writer and soft-lit rasterizer from `dining_chair_generator.py` / `bath_pod_generator.py`. There are 8 runs needed (101–104, 201–204).
Default run is 3.5 × 0.6 m with the worktop at 0.9 m: 0.25 m end cap + five 0.6 m modules (Cold, Store, Sink, Hob, Store) + 0.25 m end cap. Re-ordering, adding or dropping 0.6 m modules gives any 2.4–4.2 m run. Pivot is bottom-center, the front faces +Z and Y is up. Every iteration has a back upstand and side rails plus a low front lip, amber-latched drawers (green on the cold store), a spinward (-X) sink drain, a utensil or rail clip line, induction rings with pan fences, and a recycler tie-in with an amber Sprocket service port. Files: `iter_0N.glb`, `iter_0N_sheet.png` (Top, Front, Side, Iso), `overview.png`.

## iter_01: Monolithic Moulded Run (2,708 tris)
A white moulded composite carcass and worktop with rounded edges on a gunmetal plinth, with a violet toe-kick line. It is the most cohesive with the capsule bath pod and the easiest to wipe down. Modules are still separate cassettes behind the moulded skin, but a repair means pulling off a larger shell panel.

## iter_02: Alloy Frame + Drop-in Cassettes (3,396 tris)
An exposed brushed-alloy frame on a 0.6 m pitch with gunmetal cassettes that slide in, white latched fronts and a slate worktop with alloy lips. This is the most "built and repaired in-cylinder" option: a failed module is unlatched and swapped from the printer bay without touching its neighbours.

## iter_03: Galley Rail + Wall Pods (3,268 tris)
Low and high rounded pods hang on gunmetal wall rails with a gunmetal hood pod over the hob, leaving the floor mostly clear apart from two feet and the cold store. Rail-mounted pods won't walk under spin-down, cleaning is easy, and Sprocket can reach the recycler under the sink. The trade-off is a busier wall and more parts that need anchoring to the wall structure.

## iter_04: Island + Recycler Plinth (2,788 tris)
The whole run sits on a gunmetal recycler plinth (with its service port front-centre and a violet line), with slate waterfall ends and worktop. Water recycling is a visible part of the design and the plinth gives the heavy, low anchoring mass for the run. It can also stand free as a peninsula.

## iter_05: Ribbed Industrial + Overhead Rack (3,876 tris)
A gunmetal body with ribbed white fronts and an alloy worktop, plus an overhead rack with clip hooks and a violet light bar. It has the strongest utensil anchoring and reads as a working galley. It is the most industrial and the closest to the tri budget.

**Recommendation:** iter_02 (Alloy Frame + Cassettes) is the clearest answer to modular build and repair while matching the swivel's alloy and the capsule's white.

## Final: Galley Rail + Wall Pods (3,988 tris)
This is the polished iter_03, built with `python3 assets/src/kitchen_counter_generator.py final`. It is exported only to `godot/assets/models/kitchen_counter_wallpods.glb`, and the sheet is `final_wallpods_sheet.png`. The default 3.5 m run keeps 0.25 m end caps around five 0.6 m modules (Cold, Store, Sink, Hob, Store) with the worktop at 0.9 m.
- **Wall anchoring:** a full-length gunmetal strongback sits on the wall plane (z = -0.30). Bolted gunmetal cleats at every 0.6 m module joint carry the worktop and pods. Two brushed-alloy rails run the length, with gunmetal hook clamps on every pod. The low pods hang clear of the floor (lowest point 0.16 m on the cold store) with no feet.
- **Pods and hood:** white moulded composite pods (albedo 0.92) with rounded corners and bevelled top and bottom edges. The hood pod sits directly over the hob on the 0.6 m grid, with a slim gunmetal vent slot, a warm light strip and a violet accent.
- **Sink:** a real recessed alloy basin through an opening in the slate worktop, 0.2 m deep, with a spinward (-X) drain.
- **Spin-down retention:** gunmetal back upstand, side rails and front lip. Fronts have amber latches (green on the cold store), the hob has alloy pan-fence posts and violet induction rings, and there is a utensil rail with clips. The recycler tie-in has an amber Sprocket port.
- **Meshes:** every part is a closed mesh, with smooth normals and hard edges over 30°. The sheet uses an exposure lift on the object only, so the whites read white.
