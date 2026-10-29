# Wardrobe (#21): 5 iterations
Built with `python3 assets/src/wardrobe_generator.py`, reusing the shared rasterizer, glb writer, emissive tone-mapping and white exposure lift. There are 7 needed (101, 103, 104, 201–204).
The default is 2.7 W × 0.5 D × 2.1 H m, with the front at +Z, the back against the wall at -Z and the pivot bottom-center. **Modular:** end panels 0.15 m (or 0.05 m slim) plus bays of 0.6 / 0.9 m: 2.7 = 0.15+0.9+0.6+0.9+0.15; 2.5 = 0.05+0.9+0.6+0.9+0.05; 3.0 = 0.15+0.9+0.9+0.9+0.15. Every hanging bay has an alloy garment bar plus a gunmetal retaining top bar so hangers can't lift off in spin-down. Every part is a closed mesh. Iso views show a door or tambour partly open.

## iter_01: Moulded Slab + Sliding Doors (1,840 tris)
A flush white moulded carcass on a recessed gunmetal base, with three latched sliding doors (amber latches) in an alloy top track and a violet header band. Sliding doors need no swing clearance in tight units, and the latches hold them closed when spin-down tries to roll them. The doors and carcass panels are simple moulded flats that are easy to swap.

## iter_02: Alloy Rail + Open Bays (2,032 tris)
An open brushed-alloy upright system bolted to a gunmetal wall back plate, with floor feet, gunmetal shelves, slate elastic retaining straps across the shelves and hanging bays, and latched strap buckles. It is the lightest and most repairable kit (extruded uprights and flat shelves), but it is visually busy and relies on straps rather than doors.

## iter_03: Wall Pods on Rails (1,344 tris)
Three rounded white pods hang clear of the floor on two alloy rails over a bolted gunmetal strongback, with cleats at each bay joint, hook clamps and a violet under-band, matching the wall-pod kitchen. The middle pod is shown open with shelves. The floor stays clear for cleaning and Sprocket, and each pod lifts off the rail for repair. It is the cheapest option.

## iter_04: Tambour Roll-Door Unit (2,560 tris)
A white moulded carcass with three vertical-track roll doors (two alloy, one gunmetal) shown at different heights, plus amber latched pulls and a violet header band. Tambours never swing into the room and lock at any height. The slats are identical printed or extruded parts that are cheap to replace, but it is the most expensive in tris.

## iter_05: Mixed: Drawers + Hanging + Niche (1,776 tris)
A white carcass with a latched three-drawer stack and a cupboard (left), a lit display niche with a retaining lip above a Sprocket-reachable laundry chute hatch with an amber port at 0.45 m (middle), and a hinged hanging bay (right, shown open). Open end shelves sit at the sides, with tucked bolted floor clamps and amber clamp lights from the bed family. It has the most varied storage and ties into the laundry and Sprocket service loop.

**Recommendation:** iter_05. It is the most useful storage mix, it has the bed's clamps and the Sprocket chute, and it stays in the white-composite family. If floor space is tight, iter_01's sliding doors are the pick.

## Final: Open Bays on Wall Rails (2,544 tris)
This combines iter_02's open alloy bays with iter_03's wall-rail mounting, built with `python3 assets/src/wardrobe_generator.py final`. It is exported only to `godot/assets/models/wardrobe_openbays_rails.glb`, and the sheet is `final_openbays_rails_sheet.png`. Overall it is 2.7 W × 0.5 D × 2.1 H m, and the bays hang 0.15 m clear of the floor with no kick.
- **Layout:** two bay types: 0.9 m hanging (alloy bar plus a gunmetal retainer bar, no straps, four simple garment shapes) and 0.6 m shelves (five evenly spaced gunmetal shelves, one slate strap per compartment at the same height, with an amber buckle latch). Default 2.7 = 0.15 end + 0.9 H + 0.6 S + 0.9 H + 0.15 end. 2.5 = 0.05 slim ends + H S H. 3.0 = 0.05 slim ends + H S S H.
- **Mounting:** a full-length bolted gunmetal wall plate with two alloy rails (a thin violet strip on the top rail). Each bay joint has a chamfered alloy upright, a gunmetal bracket with two bolts and a gunmetal hook clamp on each rail, all aligned. The gunmetal end panels hang at the same height.
- **Meshes:** every part is a closed mesh. Shelves, uprights and panels are chamfered, with hard edges over 30°.
