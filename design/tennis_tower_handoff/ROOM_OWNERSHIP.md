# Tennis Tower: room / zone ownership (Rook, Nov 7 2026)
Spec: `design/strip5_tennis_tower_v1.md` **Rev 2.9** (commit 1606573). Building coordinates: X axial, Z across, origin at the SW corner, F1 = 0 / F2 = +6.1 / F3 = +12.2 (F1 = +4.0 HD). Bounds are `X x0..x1, Z z0..z1`.
Structure blockout: `assets/src/tennis_tower/structure/` (`tower_plan.py` = plan data, `build_structure.py` = generators, `assemble_preview.py` + `render_preview.gd` = box-side preview). Chunked level pieces drop in at the world offsets in `godot/assets/models/tt_struct_layout.json` (yaw 0). Kit pieces are placed by `assemble_preview.py` (same numbers Gage should use).

**Rules for every owner:** themes are sports, greenery, recreation and nature. No wood. No planter boxes. Models are layered, dense and sculpted. See `STYLE_GUIDE.md`. Reuse shared and starting-area assets where they fit (Jared, Rev 2.9). Each asset stays under 6k tris, with its pivot at bottom centre, facing +Z, with colliders. Only the F3 Glass Box envelope and the aquarium acrylic are BLEND. Anything you build that touches a neighbour's edge has to match that edge (listed per room) before it is promoted.

## Structure kit (done, blockout, all pass clip / validator)
| Asset | Tris | Use |
|---|---|---|
| tt_struct_f1_slab | 1,536 | F1 slab, S aquatic deck +2.0 (lap/diving cut-outs, deck steps X 4..7), N deck +1.0 (river channel, splash -0.6, runout -1.0), 4.5 m diving pit |
| tt_struct_f2_slab | 2,752 | F2 slab with core/lift/tree/plant holes, aquatic-hall void, view bridge (X 0..24.5, Z 34.5..44.5), slide-bridge deck (X 0..20, Z 58..60.4), downstands |
| tt_struct_f3_slab | 3,104 | F3 slab, PT band beams X 39.5 + 8k, climbing void X 35..57 Z 3..9.1, coffer cut-out, E-band beams |
| tt_struct_f1_walls / f2_walls / f3_walls | 2,080 / 2,272 / 2,048 | partitions + openings (stand backs, foyer/corridor, bowling/axe, WC shells, gallery, climbing backings, F3 under-stand WC shells); gallery windows alpha-scissor |
| tt_struct_columns | 3,712 | 18 PT columns 0.9 m + teal impact pads (F1/F2), F1 runoff column, X 0 / X 30 aquatic columns, E-band X 126.5 line |
| tt_struct_aquatic_truss | 416 | 9 instances, X 15, Z 3.5 + 9k, y +9.7 (soffit) |
| tt_struct_diving_coffer | 2,784 | coffered plate, soffit +11.8, cyan coffer lights |
| tt_struct_climb_frame | 800 | W-CL 20 × 11.5 m wall frame (posts X 36/42/46/51/56) |
| tt_struct_void_guard | 1,040 | F3 1.07 m void guard, scissor panes |
| tt_struct_plant_stack / _m | 976 each | SW + NE (base, yaw 0 / 180), SE + NW (mirror, yaw 0 / 180), louvred cap to +28 |
| tt_struct_roof_bay4 | 288 | 4 × 4 m infill bay: 3-bay X strip (X 128..140) + 4-bay Z strip (Z 61.5..77.5), 197 instances |
| tt_struct_roof_edge / _edge_chord | 64 / 96 | W edge / E edge (closes the unowned +X chord) |
| tt_struct_roof_closure / _closure_chord | 184 / 216 | S / N 1.5 m closure strips (38 each) |
| tt_struct_roof_corner | 116 | 4 corner gutter returns + downpipes |
| tt_struct_f3_corner_closure | 176 | 4 × 1.5 m Glass Box closure bays (W/E faces) |
| tt_struct_ball_net | 232 | F3 ball net tile 16 × 15 m, 8 instances, y +21.5 (scissor) |

## Rooms
Each line gives **Reuse** (promoted assets) and **Needs** (still to model), plus the **Edges** the owner must match.

### F1
1. **F1-FOY: W foyer / main entrance hall.** X −12..0, Z 10..69. Main entrance (44 m of doors at Z 17.5..61.5), 2 desks, 8 kiosks, queues, and the 6 m passage at X −12..−6. §3.6, §3.12.3–4.
   - **Reuse:** tt_entrance_bay ×11, tt_foyer_desk ×2, tt_foyer_backdrop ×4, tt_foyer_kiosk ×8, tt_foyer_stanchion, tt_stair_core_b (ST-AQS/AQN), tt_facade_bay.
   - **Needs:**
     - entrance bay re-promote (no kerb or hedge, colliders, scissor glass);
     - foyer floor finish;
     - wayfinding totems;
     - X 0 wall cladding;
     - portal-pier cladding (X 0, Z 39.5).
   - **Edges:**
     - W terrace (door glass line X −12, 6 m clear zone);
     - aquarium corridor mouth Z 34.5..42.5;
     - N-deck door Z 45..47;
     - F2 gallery soffit +5.7.
2. **F1-AQC: Lobby / aquarium corridor.** X 0..30, Z 34.5..44.5. §3.12.1.
   - **Reuse:** the full #80 kit (tank ×4, floor, bench ×4, plinth ×2, sign ×2, caustic ×3).
   - **Needs:**
     - service catwalk + hatch (+3.4);
     - life-support grilles;
     - end-pillar cladding;
     - direction signs (replace the AQUATICS glyphs);
     - 0.3 m inlay;
     - deck-door portal at X 4..7 with AQUATICS signage.
   - **Edges:** foyer; S pool deck +2.0 via steps X 4..7; W lift / LW lobby X 24.5..30; F2 view bridge above.
3. **F1-POOL: Lap pool + diving hall (S deck +2.0).** X 0..30, Z 0..34.5. §3.6.
   - **Reuse:** none directly; slate / white palette.
   - **Needs:**
     - lap pool tank lining, lane lines, gutters and starting blocks;
     - diving well with the 3 m board and 2 × 1 m boards;
     - deck drains;
     - lifeguard chairs;
     - water surface (BLEND is **not** allowed, so use opaque animated water).
   - **Edges:**
     - X 0 columns and foyer wall;
     - X 30 stand-back wall;
     - corridor S wall Z 34.5;
     - coffer above Z 21.5..30.5.
4. **F1-LEIS: Leisure water (N deck +1.0).** X 0..30, Z 44.5..79. Lazy river, splash pool, slide towers T1/T2, runout pool. §3.6, §3.12.6.
   - **Reuse:** tt_slide_tower ×2 (deck-height fix and tube opening pending).
   - **Needs:**
     - spiral slide tubes;
     - landing / runout pool;
     - river channel lining and footbridges to the island;
     - splash sprays;
     - the T2→T1 link deck at +7.0.
   - **Edges:** slide bridge (F2) at Z 58..60.4; tank back wall Z 44.5; NW plant stack.
5. **F1-CRT: Spin Court hall.** X 39.5..103.5, Z 24.5..54.5. 4 glass boxes, 10 × 20 m. §3.11.5.
   - **Reuse:** tt_court_partition, tt_court_partition_door (the closed variant is needed), tt_court_net.
   - **Needs:** court surface + line decals, the closed door variant, umpire stands, and the switch to scissor glass.
   - **Edges:** PT columns (pads done), runoff column X 71.5 Z 39.5, F2 downstands +5.0.
6. **F1-CON / F2-CON: Concourse ring + 5-row stands.** X 30..113, Z 15..64. §3.1–3.2.
   - **Reuse:** tt_stand_module (12 / floor placed), tt_lift_core, tt_stair_core_a.
   - **Needs:**
     - short end sections (3.8 m and 6.5 m cut bays);
     - concourse floor finish;
     - vomitory portals in the stand-back walls (door openings are already cut).
   - **Edges:** stand-back walls Z 15 / 64 and X 30 / 113, and the corner stairs.
7. **F1-BOWL: Bowling.** X 30..57, Z 0..15. §3.7.
   - **Reuse:** shared game bowling assets if any exist (Jared's reuse rule); facade opaque bays.
   - **Needs:** 8 lanes, approach, pinsetter masking, ball returns, seating and scoring screens.
   - **Edges:** acoustic stubs X 57..58, ST+S1 W wall X 57, SW corner of the S stand.
8. **F1-SENT: S entrance + lift lobby + free bay.** X 57..77, Z 0..15. §3.7, §3.12.3.
   - **Reuse:** tt_secondary_entrance_s (X 68..76), tt_lift_core, tt_stair_core_a/b, tt_tree_column (TC-S1/S2).
   - **Needs:** TC-S2 cladding; vestibule screens.
   - **Edges:** Rim Promenade (S face, flush); bowling; AXE 1.
9. **F1-AXE: Axe throwing.** X 77..102, Z 0..15. §3.7.
   - **Reuse:** shared axe-lane assets if any; tt_tree_column (TC-S3/S4 inside the target walls).
   - **Needs:** 8 bays (3.7 × 7 m) with cages, targets, scoring and the spectator rail.
   - **Edges:** target walls X 84..85 and X 101..102; partitions X 77 and X 93.85; ST+S2.
10. **F1-WC-S / F1-WC-N: Restrooms R1-S, R1-NW, R1-NE.** X 102..113 Z 0..15; X 30..44 and X 102..113, Z 64..79. §3.10.
    - **Reuse:** tt_restroom, tt_restroom_accessible, tt_restroom_basin, tt_restroom_urinal.
    - **Needs:** block shells (interior skins), family rooms, 19 drinking fountains (all floors).
    - **Edges:** shell walls X 44 / X 102 (door Z 70..72.5), X 113 door Z 5..8.
11. **F1-FOOD: Food court.** X 44..102, Z 64..79. §3.7.
    - **Reuse:** tt_secondary_entrance_n; shared food-court assets where they exist.
    - **Needs:** counters, seating, menu boards and bins.
    - **Edges:** N stand back Z 64; ST+N1/N2; lift N / LN; TC-N1..N4.
12. **F1-ARC / F2-ARC: Arcade L1 / L2.** X 113..140, Z 0..79. §3.7.
    - **Reuse:** shared arcade cabinets (reuse rule); tt_secondary_entrance_e; the X 126.5 column line.
    - **Needs:** cabinet layout, the prize counter, and the L1–L2 feature stair (if any).
    - **Edges:** X 113 wall (doors Z 24..27, 52..55, 70..73), ST+E, ST-ARS/ARN, the E entrance at Z 33.5..41.5.
13. **F1-PLANT: Plant stacks.** 4 corners, 12 × 10 m.
    - **Reuse:** tt_struct_plant_stack(_m).
    - **Needs:** plant interiors (AHU, chillers, substation; low priority) and the **roof tile cut-outs at the 4 corners**.
    - **Edges:** façade corner closures; roof.

### F2
14. **F2-GAL: Aquatic gallery.** X −12..0, Z 10..69. Changing, lockers, showers and the viewing walk. §3.6.
    - **Reuse:** tt_restroom kit, tt_stair_core_b.
    - **Needs:** changing rooms, lockers, showers, benches, and the scissor viewing-window frames.
    - **Edges:**
      - partition X −6 (doors Z 26 / 38 / 50);
      - X 0 window wall;
      - view-bridge door Z 35..44;
      - slide-bridge door (**conflict**, see below).
15. **F2-BRG: Slide bridge + view bridge.** X 0..24.5, Z 34.5..60.4. §3.6, §3.12.6.
    - **Needs:**
      - bridge deck, guards and canopy;
      - the 1.1 m gate at T2;
      - the aquarium service hatch to the catwalk.
    - **Edges:** gallery; slide towers; corridor ceiling +5.7.
16. **F2-RINK: Box-lacrosse / arena-soccer rink.** X 39.5..103.5, Z 24.5..54.5. §4.1.
    - **Needs:** boards, scissor glass, gates, goals, the surface, and the players' benches.
    - **Edges:** PT columns + pads; F3 PT beams at +10.7.
17. **F2-CLIMB: Climbing & bouldering gym.** X 30..113, Z 0..15. §3.7.1.
    - **Reuse:** tt_climbing_panel ×80 (lead wall), tt_climbing_panel_kids ×12, tt_climbing_panel_boulder ×37, tt_climbing_panel_trim, tt_struct_climb_frame.
    - **Needs:**
      - rental desk (X 67..76, Z 6.5..9.5);
      - training boards on X 94;
      - belay anchors / auto-belays;
      - 300 mm mats;
      - TC-S4 "tree boulder";
      - changing room fit-out.
    - **Edges:**
      - void above (F3 guard);
      - changing wall Z 10.5;
      - kids' backing X 84.5;
      - training backing X 94;
      - stand back Z 15.
18. **F2-GYM: Gym.** X 44..102, Z 64..79.
    - **Reuse:** shared gym equipment.
    - **Needs:** equipment layout, mirrors and rubber floor.
    - **Edges:** WC R2 shells X 44 / X 102; ST+N1/N2.
19. **F2-WC: Restrooms R2-NW / R2-NE.** As F1-WC-N.

### F3
20. **F3-BB: Basketball hall.** X 39.5..103.5, Z 24.5..54.5. 2 courts, 28 × 15.
    - **Reuse:** tt_struct_ball_net ×8.
    - **Needs:** court floor + decals, hoops (×4), the scorer's table, and the scoreboard.
    - **Edges:** stands; ball net (+21.5).
21. **F3-STAND: 12-row stands + concourse.** X 24.1..118.9, Z 9.1..69.9.
    - **Reuse:** tt_stand_module_f3 ×16, tt_tree_column(_west).
    - **Needs:** cut bays; WC fit-out in the under-stand shells (tt_struct_f3_walls).
    - **Edges:** track; S/N lounges; W dining; E playground.
22. **F3-TRK: Running track loop.** X 0.7..127.6, Z 0.7..78.4. §3.9.
    - **Needs:** track kit of 4 straights + 4 corners (accepted §3.11.9), lane decals, stair-landing crossings, and the void-edge rail.
    - **Edges:**
      - curtain-wall fins (0.7 m);
      - plant corners;
      - cabanas / lounge;
      - **playground benches (conflict, see below)**.
23. **F3-DINE: W dining terrace + bar.** X −0.7..24.1, Z 4..75. Bar at X 8..20, Z 35..44.
    - **Reuse:** tt_bar, tt_bar_stool ×20.
    - **Needs:** dining tables and chairs (shared assets where they exist, no wood), the bar's accessible counter, and a staff opening at +X.
    - **Edges:** W stand rear X 24.1; track W straight; lift W / LW landing.
24. **F3-CAB: Cabanas + lounge.** X −12..−0.7, Z 18..62.
    - **Reuse:** tt_cabana ×8.
    - **Needs:** lounge seating and a view rail at the W glass.
    - **Edges:** ST-AQS/AQN landings; track.
25. **F3-PLAY: Kids' playground.** X 128.3..140, Z 20.6..58.4.
    - **Reuse:** tt_toddler_zone, tt_soft_play (shrink to 4 × 4 pending), tt_see_saw, tt_swing_set, tt_balance_trail, tt_dome_climber, tt_play_tower, tt_play_surface, tt_fence_panel, tt_fence_gate.
    - **Needs:**
      - a playground bench 1.8 × 0.5 (no promoted asset; tt_aquarium_bench is the stand-in);
      - fence pickets on the kick plate;
      - surface decals.
    - **Edges:** track E straight; ST+E / ARS / ARN landings.
26. **F3-SLNG: S/N rear lounges + climbing void.** X 3..125, Z 2.5..9.1 / 69.9..76.5.
    - **Reuse:** tt_struct_void_guard.
    - **Needs:** lounge seating and greenery (no planter boxes: use moss mounds or green walls).
    - **Edges:** WC shells Z 9.1 / 69.9; track.
27. **F3-ROOF: Glass Box envelope + roof.** Full footprint.
    - **Reuse:** tt_curtain_wall_panel, tt_roof_bay ×21, tt_roof_ridge_crown ×7, the tt_struct_roof_* kit, tt_struct_f3_corner_closure, tt_struct_plant_stack.
    - **Needs:**
      - a 12 m ridge-crown piece for the X 128..140 strip;
      - roof tiles cut for the plant caps;
      - an F3 ball-guard (polycarbonate, scissor) at +12.2..16.2.

### Site
28. **S-WT: West Arrival Terrace.** X −60..−12, Z 16..64. Deck +4.0 HD.
    - **Reuse:** tt_terrace_deck / edge, tt_plinth_skirt_terrace.
    - **Needs:** the Fore Hub Station Walk steps kit, and the portal tie (Fore Cap map sets +4.0).
29. **S-EP: East Plaza + Spine ramp.** X 140..170 (+ ramp to x 310). Deck +4.0 HD.
    - **Reuse:** terrace kit, tt_terrace_ramp.
    - **Needs:** ramp guards x 230..295.

## Spec conflicts found by the blockout (for Vance)
1. **Slide bridge vs ST-AQN.** The bridge (Z 58..60.4, from X 0) lands on the ST-AQN core (X −6..0, Z 58.4..69). Only 0.4 m of it meets the gallery wall. The blockout puts the gallery doorway at Z 56..58.4, with a 2 m deck landing at X 0..2. Vance needs to choose between moving the bridge to Z 56..58.4 and moving the core.
2. **Columns inside stair cores.** Three aquatic columns land inside stair-core walls: X 30 / Z 39.5 (T-W5 bearing) inside LW (X 24.5..34.7, Z 39..44.5); X 0 / Z 12.5 inside ST-AQS; X 0 / Z 66.5 inside ST-AQN. The blockout leaves them out, so the core walls take the bearing. This needs confirming.
3. **Bowling acoustic wall vs ST+S1.** The acoustic wall (X 57..58, Z 0..15) overlaps ST+S1's thickened W wall (X 57, Z 2.6..13.2). It is modelled only as stubs at Z 0.3..2.6 and Z 13.2..14.7.
4. **W-CL wall vs the F3 slab.** The wall (Z 8..9.1) stands on the F3 slab strip outside the void (Z 3..8). The blockout cuts the slab to Z 9.1 at X 35..57.
5. **Plant stacks vs roof tiles.** The plant stacks rise to +28 through the space frame. The roof_bay tiles over the 4 corners need cut-out variants.
6. **Ridge crown gap.** The X 128..140 roof strip has no ridge crown piece.
7. **Playground benches vs the track.** See below.

## Playground benches vs F3 layout (Rev 2.9 check)
- **No clash with the F3 dining layout.** Dining is at X 3.5..23 on the W terrace, about 104 m away. The bar (X 8..20) and the cabanas (X −11..−7) are also on the W side.
- **Clash with the running track.** The E straight is X 125.8..127.6 (12.4 m in from the X 140 glass, §3.9). The benches at X 127.2..127.7 sit **0.4 m into the track's outer lane** at all four positions, Z 25 / 33 / 41 / 46.
- The gap between the track edge (127.6) and the W fence (128.3) is only 0.7 m, so a 0.5 m bench with knee space cannot fit there.
- Options:
  - (a) put the benches inside the fence, beside the 1.5 m path (X 128.3..129.8). The pieces start at X 130, so they would have to move 0.5 m east, or the benches would have to sit in the gaps between pieces. This needs a re-plan.
  - (b) move the track E straight 0.6 m inboard (to X 125.2..127.0). This makes it overlap ST+E (X 119.5..125.5, Z 50..60.6) by 0.3 m, so it only works if ST+E moves too.
  - Rook recommends (a). Vance should decide.
