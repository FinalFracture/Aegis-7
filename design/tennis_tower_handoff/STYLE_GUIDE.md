# Tennis Tower: style guide (Rook, Nov 7 2026)
This applies to every room owner and to every temp agent. Spec: `design/strip5_tennis_tower_v1.md` Rev 2.9. Room list: `ROOM_OWNERSHIP.md`.

## 1. Theme
- **Sports, greenery, recreation and nature**, inside a hard-sci-fi drum. The look is court lines, tennis-ball yellow, leaf crests, moss, river stone and kelp, set against gunmetal and slate.
- **Every room carries at least one sport cue and one nature cue.** Sport cues include court-line inlays, ball finials and net patterns. Nature cues include leaf crests, moss mounds, river-stone pebbles, branch forms and kelp.
- **No wood**, anywhere. That covers decks, benches, cladding, handles and "timber-look" textures. Use slate, alloy, gunmetal, white composite, poured rubber or HDPE instead.
- **No planter boxes.** Greenery is **integrated**:
  - moss-capped mounds and boulders;
  - green walls on structure;
  - vines on fins and columns;
  - leaf-crest ornaments;
  - branch / tree columns.
  It is never a trough or pot.
- **Layered, dense, sculpted.** Use bevels, reveals, secondary and tertiary detail (inlays, fasteners, LED reveals, moss tufts), and render from angles that show depth. Flat single-box props are blockout only.
- **Sport is decoration** (Rev 2.1). Detail should read at play distance, but it never blocks clear widths, egress zones or sightlines.

## 2. Palette and materials (names from the promoted GLBs; textures from Sloane)
| Material | Use | Notes |
|---|---|---|
| TT_Gunmetal `#1A1E24` | primary structure, frames, nodes, fins | textured (facade_titanium_gunmetal_hull) |
| TT_CarbonSlate `#282E38` | walls, spandrels, floors, signage blades | textured |
| TT_StairSlate / TT_StairGunmetal | stair and lift cores, secondary trims | Rev C stair PBR |
| TT_BrushedSteel / TT_BrushedAlloy | rails, posts, cables, fixtures | textured |
| TT_WhiteComposite `#D8DEE6` | cores, fin caps, panels, benches | keep albedo ≤ 0.9 |
| TT_CyanLED `#00E5FF` (emissive) | wayfinding, roof grid lines, coffer lights, floor-line reveals | the main accent |
| TT_AmberLED `#FF9500` (emissive) | hazard bands, court-line accents, plant caps | the secondary accent; sparing |
| TT_BallYellow | tennis-ball finials and holds | one sport cue per room |
| TT_Leaf / TT_LeafLight / TT_Soil | foliage, crests, moss, vines, berms | never in a box |
| TT_PaverStone | terraces, ramps, aprons | site only |
| TT_PlayRubber_* / TT_PlayPanel_HDPE_* / TT_PlaySand | playground and soft surfaces | playground, toddler areas, gym floors |
| TT_RinkRubber_Slate `#2B383D` | rink surface panels (`tt_rink_surface_*`) | dark slate rubber; albedo (0.17, 0.22, 0.26), metallic 0, roughness 0.85. Distinct from TT_PlayRubber_* (playground EPDM). Untextured is fine for first pass. |
| TT_MirrorOpaque | gym and restroom wall mirrors | opaque reflective only, no BLEND; albedo (0.93, 0.95, 0.96), metallic 1, roughness 0.03. The 0.9 dielectric albedo cap does not apply. Official TT_ name for legacy `Mirror`. |
| TT_CabanaCanvas_White / TT_Upholstery_FabricSlate / TT_Cushion_Button | soft goods | cabanas, lounges, stools |
| TT_StatusGreen / TT_AccentViolet (emissive) | status lights, accessible-route markers | small accents only |
| TT_StructConcrete (new, blockout) | slabs, beams, coffer plate | Sloane: concrete/terrazzo albedo needed |
| TT_PadTeal (new) | column impact pads | Sloane: padded vinyl |
| TT_GlassScissor (new, MASK) | all F1/F2 glass, guards, gallery windows, court glass | 30% ordered-dither alpha + opaque frit edge (embedded) |
| TT_NetScissor (new, MASK) | ball nets, court nets | 0.1 m cord mesh alpha (embedded) |
| Glass (BLEND) | **only** the F3 Glass Box envelope / roof and the aquarium acrylic | §3.12.6 |

Legacy names `Gunmetal`, `WhiteComposite` and `StatusGreen` (restroom pods) should be renamed to the TT_ set when those assets are next touched. Legacy `Mirror` renames to `TT_MirrorOpaque`.

## 3. Transparency rule (§3.12.6)
- **At most one BLEND layer in any line of sight.** BLEND is used only for the F3 Glass Box envelope / roof (tt_curtain_wall_panel, tt_roof_bay, tt_struct_roof_bay4 / closure, tt_struct_f3_corner_closure) and the aquarium acrylic (tt_aquarium_tank `Glass_Acrylic`).
- **Everything else is alpha-scissor** (TT_GlassScissor / TT_NetScissor): doors, storefront, ribbon windows, the gallery window, court glass, the F3 ball guard, nets and stand guards. Water is opaque (animated normal + depth tint), not BLEND.
- **Still to switch from BLEND to scissor:** 14 promoted GLBs use `Glass` BLEND today and should not:
  - court_partition(_door);
  - entrance_bay(_half);
  - secondary_entrance_s / n / e;
  - facade_bay(_half);
  - stand_module(_f3) guards;
  - stair_core_a / b;
  - slide_tower.
  Keep BLEND only on curtain_wall_panel, roof_bay and aquarium_tank (plus the tt_struct_ envelope pieces).
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
  If a variant is needed, add a parameter to the generator and promote it as a sibling GLB (`_half`, `_terrace`, `_m`).

## 5. Technical conventions
- **Geometry:** metres, Y up, **+Z = front**, pivot at bottom centre, under 6k tris per GLB (chunk larger pieces), colliders as `-colonly` / `-convcolonly` nodes.
- **Pipeline:** build with `assets/src/tennis_tower/modlib.py` (`run()` for 5 variants, `export_chunk()` / `pack()` in `structure/struct_lib.py` for level pieces). Then run:
  - the clipping check (A1–A5);
  - `validate_models`;
  - `tools/first_pass_check.py --no-godot`.
- **Naming:** only glass parts contain "glass", and they use the BLEND `Glass` material. Scissor parts are named `*_Scissor` and use TT_GlassScissor or TT_NetScissor.
- **Edges:** match the neighbour interfaces in `ROOM_OWNERSHIP.md`, which are glass lines, slab tops (F1 0, F2 +6.1, F3 +12.2, S deck +2.0, N deck +1.0) and wall faces. Never coplanar: embed by 4 mm.
- **Clearances:** 6 m main-door egress zone; 6 m foyer passage X −12..−6; 8 m aquarium corridor (≥ 6 m clear); 3.1 m concourse past the columns; 1.5 m playground path; track 1.8 m clear.
- **Coriolis:** slides, swings, runouts and throwing lanes run along X (axial). Nothing spins.
