# Washer/dryer stack (#37): 5 iterations
Built with `python3 assets/src/washer_dryer_generator.py`. There are 4 needed (laundry). Each stack is 0.8 W × 0.8 D × 1.9 H m with the front at +Z and the pivot bottom-center. Every part is a closed mesh, every iteration is under 6,000 tris, and all are empty (no clothes).
**Common logic:**
- **Anchoring:** four bolted gunmetal floor plates with clamps, topped by slate elastomer isolation pads. The drum's vibration goes into the pads, not the floor or wall.
- **Spin-down:** amber door, drawer and cassette latches hold the doors and drawers shut (and keep the drum in place) during spin-down.
- **Lint and water:** front lint and water or reclaim drawers. In spin gravity water drains "down" (radially outward) like on Earth, so normal sumps work.
- **Sprocket:** a service port at 0.45 m on the +X side.
- **Manufacture:** white moulded composite shells, alloy rings and frames, and gunmetal plinths, all bolt-together modules built in-cylinder.

## iter_01: Moulded Tower Stack (1,744 tris)
Two white moulded shells, with the washer below and the dryer above, joined by a violet band. Both have front portholes (alloy ring, slate glass, amber latch), gunmetal control strips with green and amber status lights, front lint and water drawers, and a gunmetal plinth on the clamps and pads. It is the cleanest family match and the cheapest to mould.

## iter_02: Alloy Frame + Cassettes (2,112 tris)
A brushed-alloy frame bolted to a gunmetal wall plate with alloy rails. A white washer cassette and a gunmetal dryer cassette slide in on visible gunmetal dampers and lock with twin amber latches. It is the best for repair: a failed unit slides out as one cassette. The open frame shows the vibration isolation clearly.

## iter_03: Floor Washer + Wall-Hung Dryer (1,744 tris)
The washer stands on a gunmetal isolation plinth and clamps. A shallower dryer hangs from alloy wall rails, hook clamps and brackets on a bolted gunmetal plate, with a gap between them. The washer's vibration never loads the dryer, and the dryer's weight goes into the wall. It uses the same rail language as the wardrobe and closet.

## iter_04: Drawer-Drum Stack (1,608 tris)
Two latched pull-out drawer drums with a vertical axis. The drum axis is aligned with spin gravity, so the load sits evenly and doesn't creep with Coriolis forces. The washer is shown pulled out on alloy slides, showing the gunmetal tub and alloy drum rim. Loading from the top is ergonomic, but the drawers need about 0.45 m of pull space (the glb is exported with the drawer open, so its depth reads 1.3 m).

## iter_05: Combo Drum + Reclaim Tower (1,672 tris)
A single washer-dryer combo drum at an ergonomic 1.0 m centre. Below it, a gunmetal reclaim base holds a latched white detergent-cartridge drawer and a service hatch. Above it, a gunmetal condensate and water-recycler module has alloy vents, a green status light and a lint drawer. It is the most integrated with the habitat's water loop, and there is no need to lift a wet load between machines.

**Recommendation:** iter_01, the Moulded Tower Stack. It is the clearest and most cohesive with the white-shell family and very cheap. Pick iter_02 if fast cassette swap-out is the priority.
