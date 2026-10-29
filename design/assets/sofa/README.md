# Sofa (#15): 5 iterations
Built with `python3 assets/src/sofa_generator.py`, reusing the shared rasterizer, glb writer, emissive tone-map, white exposure lift and the bed's smooth cushion loft. Fabric albedo is lifted (slate 0.42/0.46/0.52, warm grey 0.64, off-white 0.86) so upholstery doesn't read dark. There are 6 needed (101, 103, 201–204).
Each sofa is about 2.5 W × 0.9 D × 0.85 H m with the seat at about 0.40–0.43 m, the front at +Z and the pivot bottom-center. Every part is a closed mesh. Files: `iter_0N.glb`, `iter_0N_sheet.png`, `overview.png`.

## iter_01: Moulded Shell + Slate Cushions (2,176 tris)
A white moulded shell (deck, back and rounded arms) on a recessed gunmetal base with a violet front band. Three slate seat and back cushions are held by gunmetal clip tabs with amber locks. It has four tucked bolted floor clamps with amber lights from the bed, and the clipped cushions can't float off in spin-down.

## iter_02: Alloy Frame + Cushion Cassettes (2,400 tris)
A brushed-alloy tube frame with bolted gunmetal foot plates and alloy arm rails. Each seat is a gunmetal cassette tray carrying a warm-grey cushion that clips in at the front (amber tabs). Worn cushions or cassettes swap out individually, which makes it the most in-cylinder-repairable.

## iter_03: Wall-Rail Floating Sofa (1,936 tris)
A white seat pod and back pod hang from two alloy rails on a bolted gunmetal wall plate, with gunmetal cantilever brackets and hook clamps like the wall-pod kitchen and wardrobe. Off-white cushions, a violet under-band, and a Sprocket charge dock with an amber port under the front edge. The floor stays clear and anchoring goes into the wall (cushions reach about 0.91 m).

## iter_04: Low Lounge + Storage Plinth (1,728 tris)
A deep single warm-grey seat cushion (seat at 0.40 m) on a heavy gunmetal storage plinth with three latched white drawers. Slate back bolsters are held by slate straps with amber buckles, like the wardrobe, plus round slate arm bolsters. The heavy low base anchors it, and it has the most storage.

## iter_05: Curved Conversation Sofa (2,880 tris)
A four-segment arc (radius 2.8 m, about 2.3 m wide and within 0.9 m deep) of white moulded shell segments with off-white seats, slate backs and clipped cushions. It has a recessed gunmetal base with two tucked floor clamps. It suits face-to-face seating in a round living space, and the segments are identical moulds, so a 3-segment chaise or loveseat variant falls out of the same parts.

**Recommendation:** iter_01 is the most cohesive with the bed and capsule family (white shell, recessed base, tucked clamps, clipped cushions). Take iter_02 if cushion-cassette repairability matters most.
