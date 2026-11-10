# temp-Aquatics — Tennis Tower room-additions kit

## Source of truth and ownership
- Read ROOM_OWNERSHIP.md, STYLE_GUIDE.md, GAGE_NOTES.md and the full tower spec.
- **Spec Rev 3.2 addendum** (cc7fd9a), with aquatic coordinates/decisions from Rev 3.0 (2a0d7c3); header correction 7bb043c is present. Rev 3.1/3.2 addenda were checked during the build and do not move these aquatic rooms. Rev 3.2 explicitly confirms Y-up.
- Structural blockout d7a72f2 is reused, never modified. No changes to
  `tt_struct_layout.json`, `assemble_preview.py`, shared materials, shared generators,
  other owners' files, or the game entry scene.
- Canonical repository convention is **Y up / +Z front**, not Z up. All new
  GLBs have bottom-centre pivots; placement JSON restores building coordinates.
- Sports + nature; no wood and no planter boxes. Locally corrected non-metal
  slate and white albedo; shared files are unchanged.

## Reproduce
```sh
python3 assets/src/tennis_tower/rooms/temp-Aquatics/build_aquatics.py
python3 assets/src/tennis_tower/rooms/temp-Aquatics/audit_rooms.py
python3 assets/src/tennis_tower/rooms/temp-Aquatics/assemble_rooms.py
python3 tools/first_pass_check.py godot/assets/models/rooms/temp-Aquatics_rooms.tscn --no-godot
```
`modlib.py` and `structure/struct_lib.py` provide all house primitives, export,
A1–A5 clipping and `validate_models`. The room audit additionally reloads actual
GLBs, checks **across chunk boundaries**, and tests their final world transforms
against the current structural wall/column meshes. It never changes thresholds.
Every solid has `-colonly` collision; decorative floats/foliage and water do not.
Every new GLB is below 6,000 triangles including its collision mesh.

## Outputs / integration
- `godot/assets/models/tt_pool_*.glb`, `tt_leisure_*.glb`, `tt_gallery_*.glb`,
  `tt_bridges_*.glb`, `tt_corridor_*.glb`.
- `godot/assets/models/rooms/temp-Aquatics_placements.json`: authoritative new
  room additions + reused aquarium placements. **Do not also instance the old
  aquarium placements** when using this scene or manifest.
- `godot/assets/models/rooms/temp-Aquatics_rooms.tscn`: room additions only;
  instance once alongside Rook's structure, not instead of it.
- The scene shares one opaque animated-normal water shader via
  `temp-Aquatics_water_bind.gd`; water never writes ALPHA. All new guard panes
  use embedded alpha-scissor, not BLEND. Only the reused aquarium acrylic blends.
- Previews and all QA logs/reports stay outside Git at
  `/workspace/renders/tennis_tower/rooms/temp-Aquatics/`.
- Preview project is private scratch `/tmp/tt_rooms_temp_Aquatics/`; runtime GLB
  loading avoids generating .import or extracted-texture junk in the repository.
- Actual Godot capsule traversal/swimming, door animation, accessibility approval,
  and draw-call optimisation in the assembled shipping level remain Gage/QA work.

## Room status
| Room | Existing partial build | This pass | Still outstanding |
|---|---|---|---|
| Lap / diving hall | Raised +2 deck, pool/pit cutouts, trusses/coffer | 8 axial lap lanes, opaque animated water, linings, flush gutters, 8 moulded start blocks, 3m + 2x1m diving boards with real stairs, lifeguard chair, sport/leaf relief; placed in blockout | Shipping-level swim volumes, player walk/physics QA; final lighting/material approval |
| Leisure water | +1 island/deck and cutouts; legacy slide-tower asset | Continuous open river lining/water (no corner dams), splash/runout, 2 guarded island footbridges, ball-crown sprays, sculpted moss/stone crests | Enclosed T1/T2 slide tubes + NE helices built (`slides.py`, `tt_leisure_slide_tubes_a..d`) but **not placed** until Rook's island-relative `tt_slide_tower` lands; +7.0 T1–T2 link deck not emitted yet |
| Aquatic gallery | Partition and viewing panes + stair cores | 40 lockers with actual ventilation apertures, 5 composite benches, 4 changing cabins, 4 shower bays, floor finish, sculpted relief, frames reusing existing scissor panes | Shower drains/wet-floor details, accessible changing fitout, exterior F2 facade closure by envelope owner, player/door QA |
| Slide / view bridges | Structural slab decks and gallery landing | Scissor view-deck and main slide-span guards, keeping existing slab dogleg; T2 1.1 m queue gate (Z 58.65..59.75), leaf canopy, dogleg landing guards (`bridges_finish.py`) placed | +6.1 to +7 transition at the tower; gallery landing Z56..58.4 / +2.0 deck ramp (Rook/Vance) |
| Aquarium corridor | `aquarium_corridor.py` + `aquarium_corridor_final.py`: full promoted #80 Kelp Forest kit | Reused tank visuals via `tt_corridor_tank_bay` (Tank-colonly carved for walk prism); life-support grilles/end cladding; FOYER/COURTS blades; AQUATICS sign; **service catwalk placed** (headroom 2.10 m, width 0.67 m, hatch X11..14 north bypass; F2 hatch still on hold) | Genuine F2 hatch cut (Rook/Vance); widen aisle if wall moves; player traversal QA |

## Neighbour / Vance / Rook questions
1. Rev 3.0 moves the **gallery landing to Z56..58.4**, leaves ST-AQN untouched.
   The existing blockout has a 2m landing/dogleg joining the original main
   Z58..60.4 span. This pass preserves it; confirm whether the whole span or
   only its gallery neck is intended to move before finishing the gate/canopy.
2. The 3 omitted columns (X30/Z39.5, X0/Z12.5, X0/Z66.5) and 0.6m LW pilaster
   are accepted per Rev 3.0. No duplicate columns or bearing changes were made.
3. The legacy `tt_slide_tower` generator uses +6.1/+7/+9.4 **relative to its
   base**, then old placement adds the +1 island datum, producing +7.1/+8/+10.4
   in building coordinates; its roof exceeds the +9.7 truss soffit. It also
   still uses BLEND and some variants use planter boxes. Do not instance it
   unchanged. A shared-generator parameter variant, not a copied/forked tower,
   is needed before tube routing and the T2 gate can be finalised.
4. Aquarium service catwalk is now placed at walk Y 3.55..3.60 (headroom 2.10 m to
   soffit +5.7). `tt_corridor_tank_bay` keeps Tank-colonly but carves the walk prism
   (local Y>=3.55, Z -1.60..-0.80). Clear width is 0.67 m (tank back wall at Z 44.5).
   F2 hatch remains on hold; path uses the north bypass around X 11..14.
   Gallery 0.0246 m worst overlap is the Changing_HardwareHinge embed (r=0.022 into
   door; hardware exception ≤0.030 m).
5. Gallery external F2 wall behind the west lockers is not present in Rook's
   structural preview. Envelope owner should close it before final room lighting.
6. Need Gage's swim-volume/contact policy before adding invisible pool barriers;
   this pass supplies geometry/colliders but never pretends to implement swimming.

## QA iteration record
Rope/water contact and springboard rail joints failed two early geometry passes;
whole-room checking then caught lane-T/stripe coplanarity, exact floor/foot contact,
and a leaf panel over an aquatic column. Fixed the geometry (raised float seating,
shortened/butted rail joints, separated stripe strokes, 4mm floor embeds, moved
panel off the column). No validator, threshold or shared QA file was changed.
All inserted grilles/locker vents have real cuts in their host finish skin.

The first-pass checker reports repository-wide shared-tree hygiene/import/duplicate
warnings and emissive-cyan albedo warnings; do not stash, reset or clean another
owner's work to silence them. Runtime engine checks are not claimed by a static
`--no-godot` check; the box-side PNG previews are not a playable-level signoff.

## Final static QA snapshot
- 37 live GLBs (pool 15 / gallery 8 / bridges 2 / corridor 5 / leisure 7),
  plus one held-back catwalk candidate outside Git; maximum 5,600 triangles.
- Repository model validator + per-model A1–A5: all pass. Reloaded whole-room
  cross-chunk check: all 5 rooms pass, no coplanar/open meshes. The gallery's
  24.6mm maximum is an intentional hinge embed (30mm hardware limit); all other
  contacts remain below the 10mm non-hardware limit.
- Final transforms: 1,427 prop components tested against 176 wall/column
  components, zero penetration failures; 99 floor-contact checks pass.
- First-pass static checker: 20 PASS / 7 WARN / 0 FAIL before commit. Warnings
  are the shared-tree/input/import/duplicate/dead-setting items and emissive
  cyan albedo; no tests or thresholds were modified.
- 15 PNGs rendered including a structure-only baseline. Preview fixed-pose pool
  draw calls: 223 structure-only, 1,010 with aquatic additions + reused aquarium.
  This is the uncullled box-side preview, not a shipping-level performance claim.
- Complete local file inventory: `/workspace/renders/tennis_tower/rooms/temp-Aquatics/owned_files.json`.
- Plain `git pull --rebase` was blocked by others' unstaged `context/STATUS.md`
  and `context/check_context.py`. No stash/autostash/reset was used. Push is
  deferred rather than touching their work.

## Git handoff blocker
The aquatics-only commit was attempted and refused because this checkout has no
Git author identity (`Author identity unknown`). No global/repository identity
was invented or changed. The exact owned files were then unstaged with
`git restore --staged -- <owned paths>` only, leaving their working files intact
and leaving other agents' index entries untouched. The 45-file inventory above
is ready for the parent to commit with the approved identity; no hash exists.

## Nov 9 evening pass (placement fix landed; room finishes held)
- `assemble_rooms.py` no longer places `tt_corridor_tank_bay` / `tt_aquarium_tank` from the
  generic layout loop. That loop had put a stray fifth tank bay (BLEND acrylic) at the origin.
  The placements now have exactly four bays (X 3.75/9.25/14.75/20.25, Z 42.9, yaw 180) and no
  `tt_aquarium_tank`; the room `.tscn` was regenerated to match.
- `tt_corridor_tank_bay` is a copy of Rook's `tt_aquarium_tank`. Its only change is a carved
  `Tank-colonly`; the aquarium-acrylic BLEND exception is unchanged.
- Held, not committed (the team weekly-usage soft cap was reached): slide tubes + NE helices,
  bridge canopy, landing guards and the T2 gate, the gallery wet floor/drains and the accessible
  cabin/shower/thresholds. They are generated and mostly validated off-repo. The gate still needs
  a 6 mm finial lift.
- Still blocked:
  - The shared tower datum (local +6.1/+7.0/+9.4 on the +1.0 island) needs Rook.
  - The T1 +Z / T2 -Z link openings and the T2 bridge-opening Z offset need Rook.
  - The +2.0 deck has no space for 1:12 ramps without a structural cut (Rook/Vance).

## Nov 10 pass (bridges finish landed; tubes built, unplaced)
- T2 gate: ball finial centre raised 6 mm (now 6 mm into the post, limit 10 mm). Gate clear
  opening already matches Rook's stated west bridge gate, world Z 58.65..59.75.
- Landed and placed: `tt_bridges_t2_gate`, `tt_bridges_canopy_a/_b`, `tt_bridges_landing_guards`.
- Landed but **unplaced**: `tt_leisure_slide_tubes_a..d` (`assemble_rooms.py` `HELD_UNPLACED`).
  Towers and tubes are placed together only after Rook's rebuilt tower (deck local 6.0 / roof 8.4,
  1.1 m ±Z link openings) is on main; then place tubes, check the +X stubs at invert +7.0 against
  the openings, and emit `slides.link_items()` (+7.0 deck, Z 56..57, 1.1 m wide).
- Tube worst overlaps 16–24 mm are `Tube_HardwareClamp`/`Tube_HardwareArms` embeds (30 mm hardware limit).
- Still held outside Git (needs Gage/QA): `gallery_wet.py`, the wet `tt_gallery_floor` and
  `tt_gallery_accessible`. The committed dry gallery floor is unchanged.
