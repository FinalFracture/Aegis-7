# Tennis Tower: Godot notes for Gage (Rook, Nov 4 2026)
Not sent. Kept as a file per Jared. All GLBs are in godot/assets/models/. Colliders use -colonly / -convcolonly suffixes.

## Placement and offsets
- Ridge crown (#73): position = tt_roof_bay position + (0.075, 3.346, 0.112 + ridge_z), no rotation, tiles every 20 m in X with the roof bays. The ridge must be on a mid-bay roof line.
- Roof bay (#55): tiles every 20 m in X and Z. Each tile owns its -X/-Z edge nodes.
- Court partition (#56): glass line at local z +0.2275 (panel/net) and -0.230 (door). Place the net at y +3.0.
- Lift core (#57): pivot at the pit floor. Place it 0.15 m below the landing. Stairs stack every 6.1 m.
- Restrooms (#58): pair two half-units face to face (180° about Y). Repeat every 7.2 m. Basin/urinal runs repeat every 3.0 m.
- Climbing panels (#60): boulder/trim pivots are bbox-centred. Align the vertical faces, not the pivots, when mixing them with flat panels.
- Bar stools (#62): 20 instances from bar.py STOOLS (bar recenter shift z +0.20). Use a MultiMesh.
- Play tower (#63): orient local X along the hab axis (the slides run axially, with no Coriolis twist).

## Scripting / interaction
- Fence gate (#71): animate Gate_* about a Y hinge at local x -0.72, z 0 (0..100°), with a self-closing spring return and a child-proof latch at the top (adult reach / interact). The collider must move with the leaf. 3 instances.
- Swing set (#64): swing animation / physics on the seats (the sweep check passed in the model).
- See-saws (#66): pivoting beam animation.
- Court partition door (#56): the leaf is modelled parked open at 90°. Script it if it should close.

## Level geometry
- Soft-play (#69): if Vance picks a sunken pit, cut the floor mesh and collider under the ball pool (r 1.08 at local (-0.9, 0.3)) and drop the pool 0.3-0.4 m.
- Surface (#72): 6 m periodic tile, no rotation. Overlay top +0.038. Each piece has its own pad.
- Toddler zone (#67): the colliders include the Zone-colonly floor at y 0.
