# Tool wall panel (#25, pegboard + cable variant): 5 iterations
Built with `python3 assets/src/tool_wall_generator.py`. Asset list row 25: 3 needed (101, 201, Maintenance), 2.5–3.5 × 0.5 × 2.0 m. The default is 3.0 W × 2.0 H with a maximum depth of 0.5 m including shelves or benches. The back is on the wall, the front at +Z and the pivot bottom-center. **Modular:** 0.6 m panels (5 × 0.6 = 3.0; 4 or 6 panels plus 0.05 m end trims give 2.5 / 3.5). Every part is a closed mesh and every iteration is under 6,000 tris.
**Common logic:**
- **Mounting:** the same bolted gunmetal wall plate, alloy rails, hook clamps and violet strip as the wardrobe and closet.
- **Spin-down:** every tool silhouette (wrench, driver, hammer, pliers) sits under an amber spring-gate latch with gunmetal pins, so nothing can float off in spin-down. Bins, drawers and cassettes are latched.
- **Manufacture:** flat plate, extruded rail and printed or moulded cassettes, so a single panel can be swapped in-cylinder.
- **Sprocket:** a dock and service bay at 0.45 m in iter_05.

## iter_01: Pegboard Panels (2,752 tris)
Five slate pegboard insets with alloy peg-strip grids on the rails, latched tool silhouettes and a lipped full-length gunmetal shelf. It is the classic pegboard read for the asset list, and tools re-arrange freely on the peg strips.

## iter_02: Cable Management Wall (1,840 tris)
The cable variant. Alloy vertical cable trays with slate backs and amber cable gates, latched gunmetal cable spools, and a junction box with a green status light. Cable runs stay captured through spin-down, and it suits the Maintenance room.

## iter_03: Rail Tool Cassettes (2,224 tris)
Ten white moulded tool cassettes hung on three alloy rails, latched with alloy pulls, with a violet band below. One is shown open with latched tools inside, and its lid rises to about 2.3 m when open. It is the tidiest and best for unit interiors (101 / 201), and each cassette lifts off for service.

## iter_04: Magnetic Strip Wall (2,416 tris)
Three gunmetal magnetic strips with violet "mag on" lights and a green status light, plus ten latched tools and a lipped shelf of latched white bins. Magnetic hold plus gates is the fastest to grab from. It is the most "workshop" in character.

## iter_05: Sprocket Service Wall (3,536 tris)
A pegboard over three latched white drawer stacks with a lipped slate worktop (0.84 m) on the left. On the right, a 1.2 m Sprocket bay has a floor pad with an amber ring, a wall coupler and port at 0.45 m, a green status light, a latched fold-up service shelf and tools above. Sprocket can self-service and charge at the wall, which makes it the best fit for Maintenance.

**Recommendation:** iter_01 (Pegboard) for 101 and 201, plus iter_05 (Sprocket Service Wall) for Maintenance. If one design must cover all 3, iter_05, since its tool panel is the pegboard and it adds Sprocket access.
