# Tennis Tower: style guide (Rook, Nov 7 2026)
This applies to every room owner and to every temp agent. Spec: `design/strip5_tennis_tower_v1.md` (header Rev 3.0, with the Rev 3.1 and Rev 3.2 addenda). Transparency: **§3.12.6**, which supersedes the §3.11.9 wording. Room list: `ROOM_OWNERSHIP.md`.

temp-Style consistency pass: sport and nature cues are per room. Scissor and allowed BLEND are told apart by scope and by the established material names. This pass does not rename assets and does not approve a second scissor recipe.

## 1. Theme
- **Sports, greenery, recreation and nature**, inside a hard-sci-fi drum. The look is court lines, tennis-ball yellow, leaf crests, moss, river stone and kelp, set against gunmetal and slate.
- **Every room carries at least one sport cue and at least one nature cue.** That is a minimum for the room, not a cap, and not a rule for every prop. Sport cues include court-line inlays, ball finials and net patterns. Nature cues include leaf crests, moss mounds, river-stone pebbles, branch forms and kelp. A room may carry more than one of each.
- **No wood**, anywhere. That covers decks, benches, cladding, handles and "timber-look" textures. Use slate, alloy, gunmetal, white composite, poured rubber or HDPE instead.
- **No planter boxes.** Greenery is **integrated** into the room:
  - moss-capped mounds and boulders;
  - green walls on structure;
  - vines on fins and columns;
  - leaf-crest ornaments;
  - branch / tree columns.
  It is never a trough or pot.
- **Layered, dense, sculpted.** Use bevels, reveals, secondary and tertiary detail (inlays, fasteners, LED reveals, moss tufts), and render from angles that show depth. Flat single-box props are blockout only.
- **Sport is decoration** (Rev 2.1). Detail should read at play distance, but it never blocks clear widths, egress zones or sightlines.
- **Wayfinding is one cyan-led system** (`TT_CyanLED`): blades, inlay lines, roof grid lines and floor-line reveals read as the same accent. Amber is sparing. It does not lead wayfinding.

## 2. Palette and materials (names from the promoted GLBs; textures from Sloane)
| Material | Use | Notes |
|---|---|---|
| TT_Gunmetal `#1A1E24` | primary structure, frames, nodes, fins | textured (facade_titanium_gunmetal_hull) |
| TT_CarbonSlate `#282E38` | walls, spandrels, floors, signage blades | textured |
| TT_StairSlate / TT_StairGunmetal | stair and lift cores, secondary trims | Rev C stair PBR |
| TT_BrushedSteel / TT_BrushedAlloy | rails, posts, cables, fixtures | textured |
| TT_WhiteComposite `#D8DEE6` | cores, fin caps, panels, benches | keep albedo ≤ 0.9 |
| TT_CyanLED `#00E5FF` (emissive) | wayfinding, roof grid lines, coffer lights, floor-line reveals | the leading accent; keep wayfinding cyan-coherent |
| TT_AmberLED `#FF9500` (emissive) | hazard bands, court-line accents, plant caps | secondary; sparing; not the wayfinding colour |
| TT_BallYellow | tennis-ball finials and holds | one sport cue among others; not a per-room maximum |
| TT_Leaf / TT_LeafLight / TT_Soil | foliage, crests, moss, vines, berms | never in a box |
| TT_PaverStone | terraces, ramps, aprons | site only |
| TT_PlayRubber_* / TT_PlayPanel_HDPE_* / TT_PlaySand | playground and soft surfaces | playground, toddler areas, gym floors |
| TT_CabanaCanvas_White / TT_Upholstery_FabricSlate / TT_Cushion_Button | soft goods | cabanas, lounges, stools |
| TT_StatusGreen / TT_AccentViolet (emissive) | status lights, accessible-route markers | small accents only |
| TT_StructConcrete (blockout) | slabs, beams, coffer plate | Sloane: concrete/terrazzo albedo needed |
| TT_PadTeal | column impact pads | Sloane: padded vinyl |
| TT_OpaquePoolWater | pool, river, splash and runout surfaces | opaque; not BLEND |
| TT_GlassScissor (MASK) | shared scissor glazing | one material, from `assets/src/tennis_tower/structure/struct_lib.py`. See §3. Do not publish a second texture under this name |
| TT_NetScissor (MASK) | shared alpha-card nets | the helper's cord texture. `tt_struct_ball_net.glb` uses it. `tt_court_net.glb` is separate: opaque `TT_CarbonSlate` cords (`Ball_Net_Cord`), not this card and not BLEND |
| Glass (BLEND) | F3 Glass Box envelope / roof, and the aquarium acrylic | established name. Do not add `TT_GlassBlend`. Do not rename the acrylic |

Legacy names `Gunmetal`, `WhiteComposite`, `Mirror` and `StatusGreen` (restroom pods) should be renamed to the TT_ set when those assets are next touched. That is not a rename of `Glass` or of the aquarium node `Glass_Acrylic`.

## 3. Transparency rule (§3.12.6)
- **At most one BLEND layer in any line of sight.**
- **BLEND is only** the F3 Glass Box envelope / roof, and the aquarium acrylic.
- Promoted files that currently carry that envelope or roof glass were read from the GLB on origin/main `3218906`. Each has material `Glass`, `alphaMode` BLEND, `doubleSided`, and no `alphaCutoff`:
  - `tt_curtain_wall_panel.glb` (`Glass_Pane_*`);
  - `tt_roof_bay.glb` (`Roof_Glass_Panes`);
  - `tt_struct_roof_bay4.glb` (`Glass_Bay_Roof`);
  - `tt_struct_roof_closure.glb` and `tt_struct_roof_closure_chord.glb` (`Glass_Closure_Roof`);
  - `tt_struct_f3_corner_closure.glb` (`Glass_Closure_Pane`).
  The aquarium acrylic is the node `Glass_Acrylic` in `tt_aquarium_tank.glb`. Its material on that file is the same established `Glass` material, BLEND. Leave the node and the material name as they are.
- These filenames are the verified baseline set. A `tt_struct_*` prefix is not a BLEND permission. `tt_struct_void_guard.glb`, `tt_struct_f2_walls.glb` and `tt_struct_ball_net.glb` are already MASK. `tt_struct_roof_edge.glb`, `tt_struct_roof_edge_chord.glb`, `tt_struct_roof_corner.glb` and `tt_roof_ridge_crown.glb` have no glass material. Any other envelope file is unresolved until its own GLB shows envelope or roof glazing.
- **Everything else that is glazed is alpha-scissor** (`TT_GlassScissor` / `TT_NetScissor`): F1/F2 doors, storefront, ribbon windows, the gallery window, court glass, pool-lobby and view-bridge glazing (opaque-frit scissor, §3.11.9 detail kept by §3.12.6), nets that use the net card, stand guards, the F3 ball guard, and other F3 guards and rails that are not the glass-box envelope. Water is opaque (animated normal + depth tint), not BLEND. Promoted water materials that exist are `TT_OpaquePoolWater`, `alphaMode` OPAQUE, factor alpha 1, and no base-colour texture.
- **Shared `TT_GlassScissor` is the structure helper's material only.** Where the promoted image matches that helper, the texture is the 64×64 dither: texels are 0 or 255, `alphaCutoff` 0.5, baseColorFactor alpha 1. Five of the sixteen Bayer cells survive (31.25% of the field). A 4px border of that image is opaque in texel space; it is not a measured frame on the pane. A base-colour alpha of 0.3 is not 30% coverage. Under cutoff 0.5 it discards the fragment. Verified matches with factor alpha 1: `tt_struct_void_guard.glb`, `tt_struct_f2_walls.glb`, `tt_bridges_view_guards.glb`, `tt_bridges_slide_guards.glb`, `tt_leisure_footbridges.glb`, `tt_axe_spectator.glb`, `tt_food_stall.glb`, `tt_arc_claw.glb`, `tt_arc_feature_stair.glb`. The two room-local entrance copies use that same dither image but still carry the old `Glass` factor alpha 0.251, so cutoff 0.5 drops every texel. Filter, mipmaps and UV scale are an open consistency item. Do not fork another `TT_GlassScissor` to change them. A room-local dither, scale or frit keeps its own material name until the owners agree to change the helper.
- **Still BLEND on the promoted kit, which §3.12.6 does not allow.** Read from each GLB's `alphaMode`. This is not a claim that anyone has converted them. All fourteen use material `Glass`, BLEND, factor alpha 0.251, `doubleSided`, an embedded 256×256 image and no external URI:
  - `tt_court_partition.glb`, `tt_court_partition_door.glb`;
  - `tt_entrance_bay.glb`, `tt_entrance_bay_half.glb`;
  - `tt_secondary_entrance_s.glb`, `tt_secondary_entrance_n.glb`, `tt_secondary_entrance_e.glb`;
  - `tt_facade_bay.glb`, `tt_facade_bay_half.glb`;
  - `tt_stand_module.glb`, `tt_stand_module_f3.glb` (node `Guard_Glass`);
  - `tt_stair_core_a.glb`, `tt_stair_core_b.glb` (node `Guard_Glass`);
  - `tt_slide_tower.glb` (node `Enclosure_Glass`).
  Scope owners for the conversion, when assigned: Courts (`court_partition.py`, `stand_module.py`, and the four GLBs above that those generators own); Arrival (entrance-bay sources and `tt_entrance_bay.glb` / `tt_entrance_bay_half.glb`); Rook (`slide_tower.py`, `tt_slide_tower.glb`). Owners are unresolved for the secondary entrances, the facade bays and both stair cores. Room-local files `tt_food_entrance_n_scissor.glb` and `tt_arc_entrance_e_scissor.glb` are not the canonical entrances.
- Signage and screens are **opaque emissive**.

## 4. Reuse
- **Reuse before you build** (Jared, Rev 2.9).
  - Programme furnishings (gym, arcade, bowling, axe, food court, dining) come from **shared game assets** wherever one exists and fits the palette. Re-material it to the TT_ set rather than remodelling.
  - Starting-area / preface assets (stairs, lifts, restroom pods) are already adapted. Use those.
- **Tennis Tower kits that rooms must share, not fork:**
  - facade_bay / entrance / secondary entrance;
  - the terrace kit;
  - stand_module(_f3);
  - climbing panels;
  - the restroom kit;
  - the aquarium kit;
  - the foyer kit;
  - the tt_struct_* structure.
  Sharing that structure kit is not a BLEND permission (§3).
- The promoted `godot/assets/models/tt_*.glb` file is the canonical asset. A room-local copy is not a substitute and must not be documented as the shared kit. `tt_food_entrance_n_scissor.glb` and `tt_arc_entrance_e_scissor.glb` are copies of that kind.
- If a variant is needed, add a parameter to the shared generator and promote it as a sibling GLB (`_half`, `_terrace`, `_m`).

## 5. Technical conventions
- **Geometry:** metres, Y up, **+Z = front**, pivot at bottom centre, under 6k tris per GLB (chunk larger pieces), colliders as `-colonly` / `-convcolonly` nodes.
- **Pipeline:** build with `assets/src/tennis_tower/modlib.py` (`run()` for 5 variants, `export_chunk()` / `pack()` in `structure/struct_lib.py` for level pieces). Then run:
  - the clipping check (A1–A5);
  - `validate_models`;
  - `tools/first_pass_check.py --no-godot`.
- **Naming:** scissor and allowed BLEND are different materials, not a global rename.
  - Allowed BLEND keeps the established material name `Glass` on the envelope, the roof and the aquarium acrylic. The acrylic node stays `Glass_Acrylic`. Do not add `TT_GlassBlend`. Do not rename that node or its material.
  - Scissor glazing uses `TT_GlassScissor` or `TT_NetScissor`. New scissor nodes use a `*_Scissor` name and do not use the BLEND `Glass` material.
  - A legacy node that still says `Glass` on the fourteen kit files is not permission to keep BLEND. This guide does not order a repo-wide rename. The assigned owner changes that file's material when the file is theirs to edit.
  - Non-glazing parts are not given glass material names. Hardware exemptions already in the pipeline (clamp, bracket, spigot, hinge, bolt, fixing) stay as they are.
- **Edges:** match the neighbour interfaces in `ROOM_OWNERSHIP.md`, which are glass lines, slab tops (F1 0, F2 +6.1, F3 +12.2, S deck +2.0, N deck +1.0) and wall faces. Never coplanar: embed by 4 mm.
- **Clearances:** 6 m main-door egress zone; 6 m foyer passage X −12..−6; 8 m aquarium corridor (≥ 6 m clear); 3.1 m concourse past the columns; 1.5 m playground path; track 1.8 m clear.
- **Coriolis:** slides, swings, runouts and throwing lanes run along X (axial). Nothing spins.
