# Sprocket-first service wall (#25 redirect): 5 iterations
This replaces the resident tool wall (the old iterations stay in `design/assets/tool_wall/` and git history). Built with `python3 assets/src/service_wall_generator.py`.
Each wall is 3.0 W × 2.0 H m and at most 0.5 m deep. Only the floor pad projects, to about 0.82 m from the wall. The back is on the wall, the front at +Z and the pivot bottom-center. Every part is a closed mesh and every iteration is under 6,000 tris.
**Every option has:**
- **Human kit:** a small latched human kit 0.56 m wide (slate panel, a latched driver, wrench and pliers, and a white latched fuse/first-aid box with a green cross).
- **Sprocket** (0.78 × 1.03 × 0.77 m):
  - an auto-reach parts dispenser at 0.2–1.1 m
  - a charge coupler with an amber port at 0.45 m
  - a diagnostic port with a green light at 0.45 m
  - a latched battery or tool-head swap bay
- **Group-3 items folded in:** the *floor pad* is built in (bolted pad with an amber induction ring and two clamps). The *coupler arm* is stowed flat on the plate (alloy arm, white head, amber latch) above the coupler and swings out to Sprocket's 0.45 m port. A separate pad or arm asset is only needed where there is no service wall.
**Common logic:**
- **Mounting:** the same bolted gunmetal plate, alloy rails, hook clamps and violet strip as the wardrobe and closet.
- **Spin-down:** every bin, drawer, pack, tool and gate is latched.
- **Manufacture:** flat plate, extruded rails, moulded white housings and identical bins or packs, all printable and swappable in-cylinder.

## iter_01: Rotary Carousel (3,080 tris)
A white moulded housing with a vertical-axis gunmetal drum carrying four rings of bins behind a slate window, with an amber pick gate at 0.45 m. A sealed rotating store can't spill in spin-down, and Sprocket only ever reaches one gate at its own port height.

## iter_02: Vertical Lift Dispenser (3,200 tris)
Alloy lift columns with stacked white bins (each gated) and a gunmetal carriage that brings any bin down to an alloy delivery tray at 0.45–0.56 m. It has the densest storage in a 0.5 m width, and the tall store uses wall height that Sprocket can't reach.

## iter_03: Linear Rail Shuttle (3,008 tris)
Two alloy rails at 0.72–1.02 m carry six latched white bins and a gunmetal shuttle carriage (violet light) that drops parts to a tray above the coupler. Everything is at Sprocket height along the wall, it is simple to extend by adding rail length, and it has the fewest moving parts.

## iter_04: Drawer-Matrix Auto-Feed (3,072 tris)
A white frame with a 5 × 5 matrix of gunmetal micro-drawers (amber and green latch lights) at 0.14–0.94 m, which push parts into an alloy side chute and feed tray. It is the best for many small spares, every drawer is individually latched, and a failed drawer swaps out on its own.

## iter_05: Compact Alcove Pod (3,152 tris)
Sprocket parks inside a white moulded alcove (1.04 m clear, 1.32 m high, violet edge). Gated side-wall dispensers, an overhead swap shelf with four latched packs, the coupler, the diagnostic port, the pad and the stowed arm are all inside. The kit and latched spare bins sit beside it. It is the tidiest: Sprocket is "housed", the rest of the wall stays clear, and the sheet's overview Iso shows Sprocket docked (render only).

**Recommendation:** iter_05, the Compact Alcove Pod. It reads clearly as Sprocket's home, keeps every Sprocket function within reach without moving parts across the wall, and the human kit stays small and separate. Take iter_03 if a simpler, extendable mechanism is preferred.
