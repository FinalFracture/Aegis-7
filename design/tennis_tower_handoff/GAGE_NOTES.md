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

## Entrance bay (#74)
- tt_entrance_bay.glb (4.0 m) / tt_entrance_bay_half.glb (2.0 m): tile along local X, pivot bottom centre, glass line local z 0, +Z = terrace. 42 m run = 10 full + 1 half (position of the half bay TBD, Vance).
- Doors are modelled closed. If they should open (auto-sliding or swing), split the Glass_Door_* / Door_Stiles leaves and script them. Colliders still need adding (doors, canopy blade, bollards, kerb).
- Door glass is BLEND for now. If Vance switches it to alpha-scissor (§3.11.9), change the material to dithered scissor with an opaque frit edge.
- The canopy (2.6 m) and the kerb/hedge (to z 1.82) project onto the terrace, so keep the navmesh / egress clear.

## Façade bay (#75)
- tt_facade_bay.glb (4.0 m) / tt_facade_bay_half.glb (2.0 m): tile along local X, pivot bottom centre but bbox-centred in Z (façade line (raw z 0) at local z -0.181 from the pivot, recessed pane at -0.226; check in Godot before aligning with tt_curtain_wall_panel at +12.2). Colliders are included: Wall-colonly, Plinth-colonly, Trunk-convcolonly.

## Plinth skirt (#76)
- tt_plinth_skirt.glb (4.0 m) / tt_plinth_skirt_half.glb (2.0 m): place under tt_facade_bay(_half) with the same X and the façade line aligned (the skirt pivot is bbox-centred in Z, depth 2.2 m incl. the base mat, so align face lines, not pivots). The façade bay sits on the cap at +4.0.
- Courses are separate nodes (Course0..3_Facets) for trimming where p(Z) < 4.0. Holds sit on specific courses, so a course-trim script should also drop the holds above the trimmed height. Colliders: Skirt-colonly, Mat-colonly.

## Terrace kit (#77)
- Place tt_terrace_deck / tt_terrace_edge at y=+3.70 (deck top = +4.00). Under terrace edges use tt_plinth_skirt_terrace(_half) (top +3.70), NOT tt_plinth_skirt (top +4.00, for façade-only runs). Same footprint/pivot, same 4/2 m tiling.
- Ramp tiles chain at 4 m X / -0.20 m Y; aprons 4 m wide, 1:12. Deck tiles have a medallion each; rotate/alternate if repetition reads.

## Secondary entrances (#78)
- Three face assets: tt_secondary_entrance_s.glb / _n.glb / _e.glb (not a single face-param GLB). Same 8.0 × 6.1 m module, pivot bottom centre, +Z out, BLEND glass. Pick the face that matches the wall; do not mirror to change the letter (mirroring would reverse the glyph).
- Place S/N at grade on tt_terrace_apron; place E on the East Plaza terrace (module y = +3.70 with deck/edge). Flank with tt_facade_bay (4 m) — 1 m of each façade bay overlaps the 10 m lift gap as filler.
- Skirt under E (and any terrace secondary): use tt_plinth_skirt_terrace as **2 + 4 + 2 m** centred on the door (half at x=−3, full at x=0, half at x=+3) so no skirt seam falls on the door centreline. Seams land at ±3 m.
- Doors modelled closed. Clear opening per leaf pair ≈ 1.72 × 2.34 m. Script open/slide if needed; colliders: Wall / Jamb / DoorClear / Canopy / Scoreboard.

## Foyer ticketing kit (#79)
- Assets: tt_foyer_desk.glb (8 m, guest +Z), tt_foyer_kiosk.glb, tt_foyer_stanchion.glb (belt segment toward local +X; place on 1.2 m centres), tt_foyer_backdrop.glb (4 m). Pivot bottom centre. Place desk with +Z facing the W doors; backdrop on the staff side (−Z of the desk).
- Heights: standard top 1.05 m; centred accessible bay 1.0 m wide at 0.86 m with knee clear under the guest face.
- **Baked ticket hardware (no live devices):** guest RFID reader pads + ticket slot mouths on the top; staff-side ticket printer boxes with mouth + LED under each monitor. If printers / RFID should animate or print, replace or script over these meshes — do not add a second set.
- Stanchion belt is a fixed 1.07 m segment from the cassette toward +X; tip is a separate alloy end. Chain by spacing posts 1.2 m on X.
