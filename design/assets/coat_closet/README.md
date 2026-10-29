# Coat & storage closet (#22): 5 iterations
Built with `python3 assets/src/coat_closet_generator.py`. There are 4 needed (103, 104, 203, 204). Each closet is 3.7 W × 0.5 D × 2.1 H m with the front at +Z, the back on the wall and the pivot bottom-center. Every part is a closed mesh and every iteration is under 6,000 tris. **Empty by design:** no clothes, coats or garments, only bars, hooks, trays and shelves.
**Shared with the approved open-bay wardrobe** (`wardrobe_openbays_rails.glb`): the same bolted gunmetal wall plate, alloy rails at 0.30 / 2.06 m with a violet strip, gunmetal brackets with two bolts and hook clamps at every joint, alloy uprights, gunmetal shelves, slate straps with amber buckles and the same palette. They can share a wall, and `overview.png` shows each one beside the wardrobe. **Modules:** 0.05 slim end cheeks plus bays 0.9 / 0.6 / 0.6 / 0.6 / 0.9 = 3.7 m.
**Common logic:**
- **Spin gravity:** the bays hang on the rails and the floor stays clear (0.15 m).
- **Spin-down anchoring:** bolted wall plate and hook clamps, latched doors, drawers and lids, and strapped shelves.
- **In-cylinder manufacture:** extruded alloy uprights and rails, gunmetal plate shelves, and moulded white doors or lids that bolt on or off per bay.
- **Sprocket:** service via clear floor bays or ports at 0.45 m.

## iter_01: Open Hook + Shelf Bays (3,408 tris)
The closest twin of the wardrobe. Two 0.9 m hook bays (two rows of alloy coat hooks plus a lipped boot tray) frame three 0.6 m strapped shelf bays. It is the calmest pairing with the wardrobe, but everything is on show and it has no Sprocket feature.

## iter_02: Hung Doors on Rails (2,864 tris)
The same rail system closed with five moulded white doors (wall-pod language), with alloy pulls and amber latches. The first is shown open to the hook bay. Doors stop loose items drifting in spin-down and hide clutter, and the doors swap individually. It swings 0.87 m into the room.

## iter_03: Mudroom Bench + Sprocket Dock (2,912 tris)
A gunmetal bench across four bays with latched white lift-lid storage, a 12-hook rail above and strapped cubbies on top. The 0.9 m end bay is open to the floor as a Sprocket dock, with a floor pad, an amber induction ring, a rear port at 0.45 m and a green status light. The dock bay is 0.84 m clear, so Sprocket (0.78 W × 1.03 H) fits under the 1.2 m shelf but sticks about 0.3 m out past the 0.5 m depth. This is the most functional option for an entry space.

## iter_04: Sliding Panels + Suit Locker (2,880 tris)
Two gunmetal panels slide on an alloy top track over the hook and shelf bays (no swing). A latched white suit or hardware locker with a green status light takes the right bay. It is a good middle ground between open and closed.

## iter_05: Utility Mix + Service Hatch (3,248 tris)
A tall latched white tool or vacuum locker, two latched four-drawer stacks with strapped shelves above, a Sprocket service hatch (amber port at 0.45 m) under a laundry chute (green status), and an open hook bay with a boot tray. It has the most varied storage and ties into the laundry and Sprocket loop like the wardrobe iter_05 idea.

**Recommendation:** iter_03, the Mudroom Bench + Sprocket Dock. It gives the coat closet a real job (seating, boot storage, and Sprocket's home dock) while matching the wardrobe's rails. Pick iter_01 if it must read as a pure twin of the wardrobe.
