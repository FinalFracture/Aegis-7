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

## Nov 10 late pass (Rook tower r2 1ef96f1 on main)
- **Link deck landed and placed**: `tt_leisure_slide_link` (`slides.link_items()`), +7.0 deck X 23.60..24.70,
  Z 55.909..57.091. The measured enclosure faces are Z 55.911 (T1) and 57.089 (T2), not 56.9, so the deck
  embeds 4 mm into each tower sill; guards stop 4 mm short of the faces. Underside +6.75 keeps the
  ground-entry gap (X 20.2..21.24 west doors, Z 55.9..57.1) clear. No penetration into either tower mesh.
- **T2 gate unplaced** (`HELD_UNPLACED`): the tower's west gate is now Z 58.0..59.1 and the old gate's
  north flare panel/post would block it, leaving 0.45 m of clear width. A pure 0.65 m shift south puts
  the north post (Z 57.88..58.0) and panel (Z 57.35..57.88) over a void, because the slide span slab
  is Z 58.0..60.4 at X 19.84. The gate needs a re-cut (one side panel only, or a post inside the span).
- **Tubes still unplaced**: the start cap is normal to the 1:5 slope (tilted 11.3°) but the tower stub
  ends in a vertical face at X 25.052 (centre Y 7.40, Z 52.30/58.30, outer R 0.453, inner ~0.404).
  Centre, invert +7.0 and radius match, but the crown leaves an 86 mm open wedge (outer crown at X 25.138),
  the sole reaches 90 mm back into the stub (X 24.962), and the bore floor at the cap is 12 mm above
  the stub's (7.008 vs 6.996). This needs a tube model edit: a short horizontal lead-in before the elbow.

## Nov 10 clash-fix pass (tubes + T2 gate placed)
- **Tubes** (`slides.py`): the section now matches Rook's r2 stub (16-gon, flats on the cardinals,
  inner/outer flat apothems 0.3960/0.4460, centre +7.40). The start face is vertical and flush at X 25.052
  (elbow radius 0.478). The elbow starts level and eases linearly to the 1:5 slope. Measured at both stubs:
  bore floor +7.004 both sides (no lip), crown/side walls identical, 0.000 mm X overlap, 0.36 cm² of
  stub bevel corners outside our section. The only uncovered area is Rook's own inter-stave slits.
  The 16-sided section re-chunks the tubes into `tt_leisure_slide_tubes_a..f` (max 5,600 tris including collision).
- **T2 gate** (`bridges_finish.py`): north post Z 58.04..58.14 on the existing north guard line, south post
  Z 59.24..59.36, header Z 58.144..59.236, gate clear Z 58.14..59.24 (1.10 m), and one south flare panel
  Z 59.364..60.40. The whole footprint is on the +6.1 slab (Z 58.0..60.4). Through-clear with the tower
  opening (Z 58.0..59.1) is **0.96 m (Z 58.14..59.10)**: the existing slide-span guard at Z 58.06..58.14
  and the tower's north jamb set it. A full 1.1 m needs the tower opening to move to about Z 58.14..59.24 (Rook).
- `tt_gallery_lockers_b` at +6.168 is the locker door/handle chunk. It is fixed to `_a`'s carcass front
  (4 mm embed), above the 60 mm toe plinth, and is not floor-standing, so it is left in place.
- Pool water look: the runtime water is the scene shader (`ROUGHNESS = 0.24` in `temp-Aquatics_water.gdshader`
  via the bind script), which overrides the GLB material. A softer look needs a shader change (owner approval).

## Rev 3.5 accessibility pass (Vance 19fece7)
- River water surface +0.85 (`tt_leisure_river`); the water sits 4 mm inside the lining faces; lining tops +0.904.
- Flush footbridges (`tt_leisure_footbridges`): N X 8..10 over Z 72..75, S moved to X 18..20 over Z 47..50.
  Deck +0.9..+1.0 with a nonslip top at +1.012 (= the deck-finish top, so no step). The bridges bear 4 mm onto
  the lining tops and lap 4 mm into the deck finish. Water is 0.05 m below the underside. Guards are 1.10 m with
  rails at +2.078..2.112. The audit floor-contact datum for `RiverBridge_Deck` moved from +1.012 (old bridges sat
  on the deck) to the +0.904 lining bearing; the ±5 mm tolerance is unchanged.
- `tt_leisure_deck` finish cut at X 0.3..15.3 / Z 44.8..46.3 (ramp legs) plus X 0.3..1.8 / Z 44.8..47.0 (F1 landing).
- `tt_pool_deck_finish` L cut: X 4..10.5 / Z 22..31 plus X 4..6.25 / Z 31..34.5. This replaces the old
  X 4..7 / Z 31.1..34.5 stair hole, so X 6.25..7 at Z 31..34.5 is finished deck now. The X 10.5..15 exit band is finished.
- **Held**: `tt_pool_board_3m` is unplaced. Its stair (X 7.56..12.6, Z 24.5..25.5) stands inside the L cut over
  legs L3/L4. Spec §diving well puts the 3 m board at Z 25, so this is a spec conflict for Vance/Rook.
- Lifeguard chair feet now embed 4 mm into the finish (they were flush-coplanar) and legs start at +0.050.
- Pool gutter: the last side grate stops 4 mm short of the slot end (it was coplanar at Z 21.5).

## Rev 3.6 pool switchback pass (Vance ad89c1a; Rook ramps 8638069 / de77ddc)
- `tt_pool_deck_finish` cut is now X 1.0..10.0 / Z 26..32 plus the passage X 8.5..10 / Z 32..34.5. The Rev 3.5 L cut
  is gone. The ramp-top exit band (Z 26..27.5, X 10..14.82) is finished deck. The old X 4..7 deck stair opening is no
  longer in the spec. All finish is supported by the +2.0 deck (4 mm embed).
- `tt_pool_board_3m` is placed again at Z 25. Its stair runs X 7.56..12.60 / Z 24.5..25.5, 0.5 m clear of the cut at Z 26.
- The 1 m board stairs (unchanged) run X 10.92..12.60 at Z 28.0..29.0 and 31.0..32.0, so min X is 10.92 (≥ 10.05). They
  sit 0.92 m east of the cut edge.
- `tt_corridor_deck_portal_sign` is centred at X 9.25 (blade X 7.8..10.7, +3.08..3.66) over the Z 34.5 lobby-wall opening
  X 8.5..10.0, whose head is at +3.0, giving 80 mm clearance. It embeds 4 mm into the wall face.
- Pool gutter dark-slot ends now embed 4 mm into the deck-hole edges (their end caps were flush-coplanar), and the slot
  bottoms sit at +2 mm.
- Against Rook's ramps:
  - No penetrations between our parts and the ramps.
  - Guard kerbs bear flush on the terrazzo top.
  - Footbridges are ≥ 2.8 m from the ramp guards.
  - Open item for Rook: the ramp tops meet our finish with a lip. At the pool exit (X 10) the ramp is at +2.000 and the
    finish at +2.012, a 12.0 mm lip. At the leisure exit (X 15.3) the ramp is at +0.9988 and the finish at +1.012, a 13.2 mm lip.
- No aquatics placement sits in the cut or the passage. There are 4 tank bays at Z 42.9, none at the origin.
