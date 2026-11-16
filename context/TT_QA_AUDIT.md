# Tennis Tower QA audit (TTQA)

Audit only. Build: FinalFracture/Aegis-7 `main` bfe716e (code = 3795a90). Audit clone `/workspace/aegis-tt-qa`; probes are untracked in `godot/_ttqa/` (never committed). Date: Sun 15 Nov 2026 (America/Chicago).

Coordinates: `q` = tower-local building coords (X axial, Y up, Z across; F1 y 0, F2 y 6.1, F3 y 12.2). `w` = world under CylinderHab7_FullScale_World: w = (-40,18.0743,81.5712) + X(1,0,0) + Y(0,0.809017,-0.587785) + Z(0,0.587785,0.809017).

## Summary

**48 findings: 11 blocker, 19 major, 18 minor.**

| Owner | Blocker | Major | Minor | Total |
|---|---:|---:|---:|---:|
| Gage | 0 | 3 | 0 | 3 |
| Rook | 4 | 11 | 15 | 30 |
| Vance | 7 | 5 | 3 | 15 |

### Why "you can't even get into the complex"
The main W entrance (11 `tt_entrance_bay`, X -13.07) and the E entrance (`tt_secondary_entrance_e`, X 140.98) sit on the W terrace / E plaza at building y 0.00, but the drum floor beside the plinth is 2.34–4.04 m lower (y -2.34 at Z14/66, -3.04 at Z20/60, -3.80 at Z30/50, -4.04 at Z39.5). `tt_plinth_skirt_terrace` is a sheer wall with a collider; no ramp or stair exists in layout or manifest (only two `tt_terrace_apron` at N). Player step is 0.32 m, jump ~1.18 m. Every real-player route from the drum to the W bays and E door is BLOCKED; started on the terrace, all 22 W bay halves and the E door ENTER. The existing `--qa-tower-walk` passes because it teleports onto the terrace. The only drum-level ways in are the single 8 m S door (X72, Z -0.98) and N door (X72, Z 79.98) mid-face on 152 m facades, whose glass leaves look like curtain wall until you are within 4 m.

### Why so many objects are walk-through
The loader builds collision only from GLB nodes named `*-colonly` (trimesh) or `*-convcolonly` (convex). Batching (`MultiMesh`) skips StaticBody3D and only hides MeshInstances, and tower bodies stay on layer 1 (extra QA bit 1<<18) with player mask 1, so batching and layers are NOT the cause. The cause is Rook's GLBs: 430 of 2,659 instances have zero colliders and 13,016 of 52,215 visual probe points (25%) have no collider within 0.12 m. Worst: `tt_lift_core` (no colliders), `tt_restroom` (none), `tt_stair_core_*` walls/guards, `tt_court_partition` glass panes, `tt_arc_vr_pod`, `tt_struct_f3_corner_closure`. Real-player walks verified through lift walls, stair-core walls, court glass, restroom partitions and VR pods.

### Method
Real `PlayerBody` (CharacterBody3D capsule, floor_max 50°, snap 0.35, step 0.32) driven through PPA's `_qa_tower_walk_leg` in the full main scene (drum gravity) for entry and verification; standalone tower probes for mesh-vs-collider sampling (1,612 instances, 0.5 m ray grid, 3 plan slices at 1.0/7.1/13.2 m), 0.5 m walkability grid (168,140 nodes, 25,188 m² main component), drop/guard clusters (7,556 edges ≥0.5 m in 175 clusters), stair/ramp profiles at 0.02 m, AABB clash/support checks, and regulation dimension checks. Maps and screenshots in `/workspace/tt_qa_shots/`.

## Findings

| ID | Sev | Owner | Area | Room/Floor | Node | q (tower) | w (world) | Problem (measured) | Root cause | Fix | Shot |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TTQA-001 | blocker | Vance | Entry | W terrace / main entrance (11 bays) | `tt_plinth_skirt_terrace_738 (+ all W skirt panels)` | (-62.9, -3.02, 18.7) | (-102.9, 26.62, 98.47) | Main W entrance unreachable from the drum floor. Terrace deck is at building y 0.00, drum floor beside it is y -2.34 (Z14/66), -3.04 (Z20/60), -3.80 (Z30/50), -4.04 (Z39.5): a sheer 2.34-4.04 m skirt wall. Player step 0.32 m, jump ~1.18 m. All W drum routes BLOCKED in real-player sim. | No ramp/stair from drum floor to terrace in layout or manifest (only 2 tt_terrace_apron at N, X70/74 Z79.5). ROOM_OWNERSHIP S-EP spine ramp + GAGE_NOTES #77 terrace ramp tiles never placed. | Vance: add >=2 ramps (<=1:12, 1.8 m wide, guarded) or stair+ramp from drum to terrace on W face; Rook: build ramp GLB with *-colonly + manifest rows. | S01_W_terrace_wall_from_drum.png |
| TTQA-002 | blocker | Vance | Entry | E plaza / secondary entrance E | `tt_plinth_skirt_terrace_904 / tt_secondary_entrance_e` | (170.9, -4.07, 36.3) | (130.9, 36.12, 113.33) | E entrance (X140.98 Z37.5) unreachable from drum: E plaza deck y 0 vs drum -2.34..-4.07, sheer skirt wall, no ramp. Starting ON the plaza the door works (ENTER). | Same as W: plaza built as raised plinth with no access ramp. | Vance/Rook: ramp or stairs from drum to E plaza. | S03_E_plaza_wall_from_drum.png |
| TTQA-003 | blocker | Rook | Walk-through | Lift cores F1-F3 (4 shafts x3 floors) | `tt_lift_core x12 (981-992)` | (66.5, 0.0, 11.38) | (26.5, 24.76, 90.78) | ZERO colliders: shaft walls, door wall, landing doors and car are all walk-through (94% of 1,536 visual probe hits leak). Player walked from (68.5,0,19) into the shaft and stood inside (68.50,-0.12,12.85). On F2/F3 the slab is open over the shaft: unguarded 6.1/12.2 m drop (F2 X66-76.5 Z9-20, F3 X67-76 Z9-20 & Z59-69.5, F2/F3 X24-35 Z34.5-44, F2 X108-118.5 Z34-44). Lifts also have no interaction (non-functional). VERIFIED real-player: F1 walked through shaft side wall (63.5,13)->(68.18,13); F2/F3 walk-in from Z18 -> player fell into the shaft and landed 1.74 m lower (q y 4.36 on F2, 10.51 on F3, 14 airborne frames), trapped inside. | tt_lift_core.glb has no *-colonly / *-convcolonly nodes; loader only builds colliders from those. | Rook: add Shaft_Walls/Door_Wall/Landing_Doors convcolonly; Gage: lift interaction or block landing doors. | S19_lift_shaft_fall_F2.png |
| TTQA-004 | blocker | Rook | Walk-through | All stair cores F1-F3 (34 instances) | `tt_stair_core_a x16, _b x12, _b_m x4, _b_cap x2` | (49.0, 0.0, 6.0) | (9.0, 21.6, 86.43) | Core_Walls, Front_Wall, Mid_Landing edges and Flight1_Cast have no collider (71% / 81% / 71% / 88% leak). Players walk through stair-core walls and fall off landing sides: 3-12.2 m drops with only 0.25-0.45 m effective guard (e.g. F1-CON X30.5-40.5 Z15.5-20.5; F2 X108-118.5 Z34-44 to 12.2 m; F2-ARC X134.5-139.5 Z59-68.5 & Z10.5-20 12.2 m; F2-GYM X56.5-66.5/83.5-92 Z65.5-76.5 11.7 m; F3-CAB X-11.5-0 Z58-68.5 12.2 m). VERIFIED real-player: walked through tt_stair_core_b_963 W wall (55,6)->(60.19,6) and tt_stair_core_a_955 wall (73.5,6.5)->(73.29,13.16). | Stair-core GLBs only carry colonly for treads/flight ramps; walls, guards and landing edges are visual-only. | Rook: convcolonly for Core_Walls, Front_Wall, guards (>=1.07 m) on every core variant. | slice_F1_walkthrough.png |
| TTQA-005 | blocker | Rook | Walk-through | F1 Spin Court hall (courts 1-8) | `tt_court_partition x112, tt_court_net x8` | (58.5, 0.0, 27.4) | (18.5, 34.18, 103.74) | Glass court partitions: Court_Pane_Scissor has no collider (62% leak at 0.5 m); only posts collide, so every court boundary is walk-through. Court nets Ball_Net_Scissor 58% leak. VERIFIED real-player: crossed partition at X61.5 (Z24.5->30.17) and at X74.4/Z33 (X71.5->77.17); only an 8 cm floor channel and 0.08 m posts collide. | Scissor glass mesh exported without colonly; only post boxes collide. | Rook: one thin box convcolonly per pane (full 2.06 m x 5.19 m). | S06_court_glass_walkthrough.png |
| TTQA-006 | blocker | Rook | Walk-through | Restrooms F1/F2 (10 blocks) + F3 (4) | `tt_restroom x10, tt_restroom_6 x4` | (33.4, 0.0, 68.8) | (-6.6, 58.51, 137.23) | tt_restroom has ZERO colliders (Partitions, Pilasters, Stall_Doors, WC units, Wet_Wall 100% leak); tt_restroom_6 partitions 53% leak. Player walks straight through stalls and the wet wall. VERIFIED real-player: walked into tt_restroom_1010 (37,66)->(37,69.64) through partitions. | No colonly nodes in tt_restroom.glb; partial in _6. | Rook: add convcolonly for wet wall, partitions, pilasters, doors (doors can be static closed). | slice_F1_walkthrough.png |
| TTQA-007 | blocker | Vance | Connectivity | F2 Ice rink | `tt_rink_board_2m loop (1742-1789)` | (72.0, 6.11, 39.5) | (32.0, 46.23, 109.94) | Rink surface 1,506 m^2 (X42-102 Z27-52, y 6.11) completely enclosed by continuous 2.42 m boards: no gate. Unreachable. | Board loop has no gate module in layout. | Vance/Rook: 2 gate modules (players' gate + Zamboni gate). | S09_rink_no_gate.png |
| TTQA-008 | blocker | Vance | Connectivity | F1 Axe throwing (8 bays) + F2 climbing pocket | `tt_axe_bay_s 1140-1142, E row, tt_axe_spectator 1146/1154` | (80.0, 0.0, 7.0) | (40.0, 22.19, 87.23) | Only bay 1 (tt_axe_bay_s_1139, Z2.05) is reachable. Bays 1140/1141/1142 are sealed 14-17 m^2 boxes (X77 wall + 3.46 m partitions + 2.4 m spectator rail Z13.85 + target wall X84). The whole E row + corridor X85-94 + F2 auto-belay/bouldering form an isolated 764 m^2 pocket (X85-112.5 Z0.5-16) reachable only via tt_stair_core_b (89,7.9). | Spectator rail and partitions span full bay width; no gates; pocket walls have no door. | Vance: gate in each spectator rail + door from concourse to E row/climb zone. | map_F1_reachability.png |
| TTQA-009 | blocker | Vance | Connectivity | F1 Pools (lap / diving / river / splash) | `tt_pool_lap_tank, diving tank, tt_leisure_river` | (12.0, 0.04, 58.0) | (-28.0, 52.2, 128.47) | Pools are dry traps: lap tank floor y 0.04 vs deck 2.0 (1.96 m wall), diving tank y -2.46 vs deck 2.0 (4.46 m), river 0.04 vs deck 1.0 (0.96 m, only escapable by jump). No ladders/steps/exits. Water is visual only (no swim): player walks on the tank bottom and is stuck. 1 m / 3 m diving boards drop 5.4 / 7.5 m onto tank floor. | No pool ladders/steps placed; no water volume/swim (Gage). | Rook: ladder/step GLBs with colonly at each tank; Gage: water Area3D (buoyancy/swim or exit-teleport). | S10_lap_pool_no_exit.png |
| TTQA-010 | blocker | Vance | Safety | F3 track over stair cores | `tt_stair_core_b_cap / track` | (61.0, 12.2, 6.0) | (21.0, 31.47, 79.25) | Running track passes open stairwells: X57.5-64 and X85.5-92, Z2.5-9, drop up to 12.24 m, no guard on track side. | Track routed across b_cap core openings; no guard. | Vance: reroute track or guard openings (1.07 m). | map_F3_reachability.png |
| TTQA-011 | blocker | Vance | Safety | Slab openings F2/F3 | `f2/f3 slabs at lift+stair cores` | (71.0, 6.1, 14.0) | (31.0, 31.24, 89.31) | Unguarded slab openings: F2 X66-76.5 Z9-20 (6.1 m), F2 X24-35 Z34.5-44 (6.1), F3 X24-35 Z35-44 (12.2), F3 X67-76 Z9-20 & Z59-69.5 (12.2), F2-ARC X127.5-139.5 Z58-78.5 (6.1), F3-PLAY X127.5-133.5 Z59-78.5 (12.2). | Guards missing / lift walls visual-only. | Vance: 1.07 m guards on every opening; Rook: colliders. | map_F2_reachability.png |
| TTQA-012 | major | Gage | Entry | QA harness | `preface_playable_area.gd --qa-tower-walk` | (-20.0, 0.0, 39.5) | (-60.0, 41.29, 113.53) | --qa-tower-walk passes (52 s) because it teleports the player onto the terrace (y 0) before walking in; no leg starts from the drum floor, so the 'can't get in' bug was invisible to CI. | Harness start points are on the plinth, not on the drum. | Gage: add drum-floor start legs to every entrance (W bays, E, S, N) and fail if not ENTERED. |  |
| TTQA-013 | major | Gage | Entry | S door (X72 Z-0.98) / N door (X72 Z79.98) | `tt_door S/N modules` | (72.0, 0.0, -0.98) | (32.0, 17.5, 80.78) | Only working drum-level entrances are one 8 m door module mid-face on each 152 m long S and N facade. Glass leaves look like curtain wall until the player is within 4 m (proximity open). Both halves ENTER from drum and from preface edge, incl. sprint. | Door open radius 4 m, no signage/canopy/lighting cue; entrances not discoverable. | Gage: wayfinding light/sign + open radius ~6 m; Vance: canopy/marker at S/N doors. |  |
| TTQA-014 | major | Rook | Walk-through | Facade, all floors | `tt_curtain_wall_panel x114, tt_facade_bay x90` | (30.0, 6.1, -0.6) | (-10.0, 22.66, 77.5) | Curtain wall Fin_Branch 39% leak, facade bay Frame 32% leak (fins/frames visual-only). Glazing itself collides, so no exit found, but fins are walk-through at 0.1-0.5 m depth. | Fins/frames not in colonly. | Rook: include mullion/fin volume in panel colonly. |  |
| TTQA-015 | major | Rook | Walk-through | F3 corners (4) | `tt_struct_f3_corner_closure 342-345` | (-12.03, 12.2, 0.0) | (-52.03, 27.94, 74.4) | Corner closures (glass + fins, 13.3 m tall) at the 4 F3 building corners have ZERO colliders. Potential walk-out over a 12 m drop if a corner is reachable (not proven reachable in grid; cabanas/plant stacks are adjacent). | No colonly in GLB. | Rook: convcolonly box for each closure. |  |
| TTQA-016 | major | Rook | Walk-through | F1/F2 Arcade | `tt_arc_vr_pod x8, tt_arc_racer x20, tt_arc_feature_stair guard` | (131.5, 0.0, 49.0) | (91.5, 46.88, 121.21) | VR pods 100% leak (zero colliders; VERIFIED walk-through (127,49)->(134.67,48.95)), racer seats/shells partly walk-through; feature stair Guard_Scissor no collider (4.6 m side drop, effective guard 0.22 m at X134-135.5 Z38.5-40). | Missing colonly. | Rook: convcolonly per pod/racer, guard panels. | S20_vr_pod_walkthrough.png |
| TTQA-017 | major | Rook | Walk-through | F1 Food court / F3 dining | `tt_food_table4 x114, tt_food_stall x6, tt_bar` | (70.0, 0.0, 72.0) | (30.0, 60.39, 139.82) | Chair back-posts 50% leak, stall counters and F3 bar counter (68% leak) are walk-through. | Missing colonly on chairs/counters. | Rook: counters convcolonly; chairs simple box. |  |
| TTQA-018 | major | Rook | Walk-through | F2 Gym | `tt_gym_cycle x24, tt_gym_rower x4, tt_gym_dumbbell_rack` | (75.0, 6.1, 70.0) | (35.0, 64.15, 134.62) | Bikes 41%, rowers 86%, dumbbell rack partly walk-through. | Missing colonly. | Rook: box colliders per machine. |  |
| TTQA-019 | major | Rook | Walk-through | F1 Bowling | `tt_bowl_lane_pair x4, tt_bowl_core_acoustic` | (45.0, 0.0, 8.0) | (5.0, 22.78, 88.04) | Pit curtain/masking 51% leak, Acoustic_Panels 70% leak (walk into the pin deck / masking). | Missing colonly. | Rook: masking unit + panel colliders. |  |
| TTQA-020 | major | Rook | Connectivity | F3 Stands | `tt_stand_module_f3* (rise 0.37-0.45 m)` | (72.0, 12.2, 20.0) | (32.0, 39.7, 90.58) | Stand tiers rise 0.415-0.45 m (F1/F2) and 0.37-0.45 m (F3) with no aisle steps; player STEP_HEIGHT 0.32 so tiers are unclimbable and F3 stand components are isolated. Real stands use 2 aisle steps per tier (<=0.18-0.2 m). | Stand GLBs lack aisle stair geometry/colonly. | Rook: add aisle step colonly every ~6 m. |  |
| TTQA-021 | major | Vance | Physics | Void under F1 | `tt_struct_plinth_fill (13 etc.)` | (80.0, -3.0, 40.0) | (40.0, 39.16, 115.7) | Hollow void: plinth fill top is y -2.2..-4.2 under X29-139.5 (5,682 m^2), X-11.5-14 (1,460 m^2), X15-27.5, while F1 slab underside is -0.403: a 1.8-3.8 m hidden void, contradicting CYLINDER_DROP. Any opening (lift pit at -0.15, pool tanks) risks fall-through into it. | Plinth fill height not raised to slab. | Vance/Rook: raise fill to -0.40 or seal. |  |
| TTQA-022 | major | Vance | Safety | Plant stacks SW/SE (F2/F3) | `tt_services_plant_stack_sw / _m` | (-5.5, 6.1, 5.0) | (-45.5, 25.95, 82.03) | Plant-stack interiors (X-10.5..-1 and X129..138.5, Z1.5..9.5) are enterable from F2/F3 with 6-12 m drops inside and 0.25 m headroom pockets. | Plant stack is open shell with no lid/door colliders. | Rook: close shell with colonly / Vance: access door. | map_F2_reachability.png |
| TTQA-023 | major | Vance | Safety | F2 slide tower / bridges | `tt_slide_tower_t1/t2, tt_bridges_slide_guards` | (22.5, 6.1, 56.5) | (-17.5, 56.22, 123.7) | F2-BRG X20.5-24.5 Z51.5-61.5: edges drop up to 6 m with effective guard 0.39 m. | Guard height/colliders insufficient. | Rook: 1.07 m guard colonly. |  |
| TTQA-024 | major | Vance | Safety | F2 Aquatic gallery edge | `tt_struct_f2_slab gallery edge` | (-9.0, 6.1, 30.0) | (-49.0, 40.64, 102.26) | Gallery edge X-11.5..-6.5 drops 6.11 m with no guard. | No guardrail along gallery edge. | Vance: guard. |  |
| TTQA-025 | major | Gage | Lighting | Whole tower | `tennis_tower_lighting.gd` | (72.0, 0.0, 40.0) | (32.0, 41.59, 113.93) | Only 26 omni + 3 spot (0 shadowed) + 8 soffit panels, all near W foyer (X-8..4), S lobby (X66-76 Z8-16), 6 stair cores and 6 fills at X-4..6. Courts, rink, pools, bowling, arcade, gym, food court and all of F3 are dead zones. | Lighting rig only covers arrival zones. | Gage: per-room light grid (or baked/VoxelGI) for every room. | S13_dark_court_hall_F1.png |
| TTQA-026 | major | Rook | Placement | F2 Climbing | `tt_climb_hook_rail x7` | (54.75, 7.51, 12.85) | (14.75, 31.7, 87.55) | Hook rails float 1.41 m above floor with no wall within 0.12 m (e.g. X54.75 y7.51 Z12.85). | Placement y/wall offset wrong. | Rook: snap to wall face. |  |
| TTQA-027 | major | Rook | Placement | F2/F3 Aquatic truss | `tt_struct_aquatic_truss` | (24.5, 9.68, 39.15) | (-15.5, 48.92, 107.55) | Truss passes 5.65 m through tt_stair_core_a_960 (X24.5 y9.68 Z39.15) and through stair_core_b/_b_m walls at X-0.15 Z12.15/66.15. | Truss span not trimmed to cores. | Vance/Rook: trim or reroute. |  |
| TTQA-028 | major | Rook | Placement | Services | `temp-Services_placements.json` | (70.0, 0.0, 40.0) | (30.0, 41.59, 113.93) | Services room file has 0 placements: no drinking fountains, no family/accessible rooms in the whole complex (19 stations proposed but gated). | Gated pending Vance spec + headroom review. | Vance: release spec; Rook: place. |  |
| TTQA-029 | major | Vance | Realism | F1 Spin Courts | `court boxes 10 x 20 m` | (58.5, 0.0, 32.5) | (18.5, 37.18, 107.86) | 'Tennis Tower' has no regulation tennis court: court boxes are 10 x 20 m; tennis doubles needs 23.77 x 10.97 m plus run-off (~36.6 x 18.3 m). Volleyball fits 18 x 9 but lacks 3 m free zone. | Layout sized for padel-like courts. | Vance: decide - add >=1 tennis court or rename. |  |
| TTQA-030 | major | Rook | Realism | F1 Bowling | `tt_bowl_lane_pair` | (45.5, 0.0, 4.0) | (5.5, 20.43, 84.81) | Foul line X~37.00 to head pin X~54.0 = 17.0 m; regulation 18.29 m (1.29 m short). Lane width 1.066 OK, approach 4.6 m OK. | Lane mesh length. | Rook: lengthen lane bed 1.29 m. | S16_bowling_lane_short.png |
| TTQA-031 | minor | Vance | Entry | W entrance bays | `tt_entrance_bay x11` | (-13.07, 0.0, 39.5) | (-53.07, 41.29, 113.53) | W bay door clear opening per half ~0.895 m (< 0.9 m minimum); S/N/E halves 1.713 m. | Bay module door leaf sizing. | Widen W bay leaves to >=0.9 m clear (pref 1.0). |  |
| TTQA-032 | minor | Rook | Walk-through | F3 Playground fence | `tt_play_fence_kick x44 (2304-2349)` | (128.26, 12.2, 40.6) | (88.26, 51.81, 107.25) | Pickets visual-only (33% leak) at 0.5 m; rails collide so a player is stopped, but small gaps / visual mismatch. | Pickets not in colonly. | Rook: single panel convcolonly per fence segment. |  |
| TTQA-033 | minor | Rook | Walk-through | Misc props | `tt_foyer_stanchion x30, tt_aquarium_bench x4, tt_swing_set, tt_cab_view_rail posts, tt_struct_void_guard panes, tt_axe_partition posts/vines, tt_climbing_panel holds, tt_secondary_entrance_n frame, tt_corridor_deck_portal_sign, tt_cab_dress_vine x63` | (-5.0, 0.0, 39.5) | (-45.0, 41.29, 113.53) | Aquarium benches 100% leak; swing set 75%; stanchions, view-rail posts (69%), void-guard panes (74%, top rail still collides), axe partition posts/vines, holds, signage and vines leak. | Missing colonly. | Rook: add colliders to anything >0.3 m tall a player can touch. |  |
| TTQA-034 | minor | Rook | Walk-through | Invisible colliders | `various (cabanas F3 X-11..-7, stair cores, benches)` | (-9.0, 12.2, 39.5) | (-49.0, 51.16, 106.36) | Slice maps: collider with no visual at slice height: F1 2,341 / F2 4,581 / F3 4,936 cells (0.2 m) - oversize boxes (e.g. F3 cabanas) act as invisible walls. | Colonly boxes larger than visuals. | Rook: shrink colonly to visual hull. |  |
| TTQA-035 | minor | Vance | Safety | Headroom | `stair-core entries F1/F2 (many)` | (45.0, 6.1, 18.0) | (5.0, 33.59, 92.55) | Headroom under first stair flights 1.84-1.91 m (F1 X34-136, F2 X45-112.5 at core entries) < 2.1 m; stair under-flight pockets 0.09-0.23 m (head trap). | Open under-flight space not closed off. | Rook: close under-flight with colonly; Vance: check section. |  |
| TTQA-036 | minor | Rook | Safety | Stair cores | `tt_stair_core_* flights` | (49.0, 0.0, 6.0) | (9.0, 21.6, 86.43) | Typical rise 0.171 / run 0.28 OK, but first/last risers up to 0.19 m (inconsistent risers). | Flight start/end rounding. | Rook: even risers. |  |
| TTQA-037 | minor | Rook | Safety | Slides | `tt_leisure_slide_tubes_d/e` | (24.5, 4.0, 60.0) | (-15.5, 56.58, 127.76) | Chute colliders 32-40 deg (< 50 deg floor_max): players can walk up slides; tubes_d/e colliders extend to y ~1.0-1.9 below the visual (hidden step). | Collision hull loose. | Rook: tighten slide colonly; Gage: flag slide as non-walkable. |  |
| TTQA-038 | minor | Rook | Placement | F2 Climbing | `climbing mats vs boulder/kids/train/lead panels` | (105.0, 6.1, 13.9) | (65.0, 31.18, 89.23) | 300 mm mats penetrate wall panels by 0.10-0.34 m (X84.31, X94.01, X98-111.75 Z13.9, Z7.93). | Mat footprint overlaps panel base. | Rook: offset mats 0.35 m from panels. |  |
| TTQA-039 | minor | Rook | Placement | F2 Gallery | `tt_gallery_nature_relief` | (-5.9, 6.71, 40.0) | (-45.9, 47.01, 109.99) | Relief floats 0.6 m off floor with no wall behind. | Placement. | Rook: mount on wall or add plinth. |  |
| TTQA-040 | minor | Rook | Placement | F3 Basketball | `tt_bb_scoreboard_1709` | (71.5, 19.7, 39.5) | (31.5, 57.23, 101.95) | Scoreboard at y 19.7 with no hanger/support detected. | No rigging. | Rook: add hanger cables/truss. |  |
| TTQA-041 | minor | Rook | Placement | F2 Leisure | `tt_leisure_slide_link_1112` | (56.5, 6.75, 24.1) | (16.5, 37.7, 97.1) | Slide link at y 6.75-7.0 with no support underneath. | No support. | Rook: add supports. |  |
| TTQA-042 | minor | Rook | Placement | Rooftop/roof | `tt_roof_plant_cutout` | (70.0, 25.25, 40.0) | (30.0, 62.01, 99.09) | Roof plant cutouts clip roof edge chords/corners/closures at y 25.25. | Overlap. | Rook: trim. |  |
| TTQA-043 | minor | Rook | Placement | Plinth | `tt_plinth_skirt_terrace vs tt_plinth_skirt` | (-13.1, -1.0, 13.5) | (-53.1, 25.2, 93.08) | Skirts overlap at X-13.1 Z13.5 and X140 Z65.5 (z-fight); E/W terrace skirt bottoms 0.16-0.19 m above fill at X169.2 Z40 (visible slit). | Overlap/gap. | Rook: trim/extend. |  |
| TTQA-044 | minor | Rook | Placement | F3 Playground | `tt_play_surface vs dome climber/balance trail/perch/fence` | (133.3, 12.2, 20.56) | (93.3, 40.03, 91.03) | Coplanar pads z-fight (known rooftop pads); play_perch into fence_kick (X128.32); fence_kick vs fence_gate overlap (X133.3 Z20.56/58.36); fence 3 cm sunk into swing pad. | Coplanar/overlapping placements. | Rook: 5 mm lift for pads; trim fence at gate. |  |
| TTQA-045 | minor | Rook | Placement | F1 Pools | `tt_pool_lap_tank a/d` | (12.0, 0.0, 58.0) | (-28.0, 52.17, 128.49) | Lap tanks a/d sunk 3.5 cm. | Placement y. | Rook: snap. |  |
| TTQA-046 | minor | Rook | Placement | F3 toddler zone | `tt_toddler_zone_2300` | (134.5, 12.2, 54.0) | (94.5, 59.68, 118.09) | Foliage/terrain visuals without colliders (5 leaks; known phantom). | Visual-only dressing. | Rook: ok if intentional; else colonly. |  |
| TTQA-047 | minor | Rook | Realism | F1 Axe throwing | `tt_axe_bay` | (80.0, 0.0, 2.0) | (40.0, 19.25, 83.19) | Throw lines at 3.48 m and 4.75 m from target face vs WATL 3.66 m / 4.57 m. Target centre 1.52 m OK. | Line offsets. | Rook: move lines. |  |
| TTQA-048 | minor | Vance | Realism | F3 Track | `track loop` | (72.0, 12.2, 4.0) | (32.0, 30.3, 77.64) | Single 1.8 m lane, loop ~394 m; shares deck with open stairwells (see blocker). | Layout. | Vance: info only / guard. |  |

## Recommended fix order

Blockers first. Integration (Gage) is separated from asset/layout (Rook/Vance).

### Gage – integration (preface_playable_area.gd, loader/batcher, lighting, doors, gravity)
- TTQA-012 (major): --qa-tower-walk passes (52 s) because it teleports the player onto the terrace (y 0) before walking in; no leg starts from the drum floor, s… → Gage: add drum-floor start legs to every entrance (W bays, E, S, N) and fail if not ENTERED.
- TTQA-013 (major): Only working drum-level entrances are one 8 m door module mid-face on each 152 m long S and N facade. Glass leaves look like curtain wall un… → Gage: wayfinding light/sign + open radius ~6 m; Vance: canopy/marker at S/N doors.
- TTQA-025 (major): Only 26 omni + 3 spot (0 shadowed) + 8 soffit panels, all near W foyer (X-8..4), S lobby (X66-76 Z8-16), 6 stair cores and 6 fills at X-4..6… → Gage: per-room light grid (or baked/VoxelGI) for every room.
- Also (from asset findings): water Area3D / swim or exit for pools (TTQA pool blocker), lift interaction, drum-start legs in `--qa-tower-walk`, and a CI check that fails when a tower GLB mesh >0.3 m tall has no `*-colonly` sibling.

### Vance – architecture/layout
- TTQA-001 (blocker): W terrace / main entrance (11 bays) – Vance: add >=2 ramps (<=1:12, 1.8 m wide, guarded) or stair+ramp from drum to terrace on W face; Rook: build ramp GLB with *-colonly + manifest rows.
- TTQA-002 (blocker): E plaza / secondary entrance E – Vance/Rook: ramp or stairs from drum to E plaza.
- TTQA-007 (blocker): F2 Ice rink – Vance/Rook: 2 gate modules (players' gate + Zamboni gate).
- TTQA-008 (blocker): F1 Axe throwing (8 bays) + F2 climbing pocket – Vance: gate in each spectator rail + door from concourse to E row/climb zone.
- TTQA-009 (blocker): F1 Pools (lap / diving / river / splash) – Rook: ladder/step GLBs with colonly at each tank; Gage: water Area3D (buoyancy/swim or exit-teleport).
- TTQA-010 (blocker): F3 track over stair cores – Vance: reroute track or guard openings (1.07 m).
- TTQA-011 (blocker): Slab openings F2/F3 – Vance: 1.07 m guards on every opening; Rook: colliders.
- TTQA-021 (major): Void under F1 – Vance/Rook: raise fill to -0.40 or seal.
- TTQA-022 (major): Plant stacks SW/SE (F2/F3) – Rook: close shell with colonly / Vance: access door.
- TTQA-023 (major): F2 slide tower / bridges – Rook: 1.07 m guard colonly.
- TTQA-024 (major): F2 Aquatic gallery edge – Vance: guard.
- TTQA-029 (major): F1 Spin Courts – Vance: decide - add >=1 tennis court or rename.
- TTQA-031 (minor): W entrance bays – Widen W bay leaves to >=0.9 m clear (pref 1.0).
- TTQA-035 (minor): Headroom – Rook: close under-flight with colonly; Vance: check section.
- TTQA-048 (minor): F3 Track – Vance: info only / guard.

### Rook – GLBs, manifest, placements
- TTQA-003 (blocker): Lift cores F1-F3 (4 shafts x3 floors) – Rook: add Shaft_Walls/Door_Wall/Landing_Doors convcolonly; Gage: lift interaction or block landing doors.
- TTQA-004 (blocker): All stair cores F1-F3 (34 instances) – Rook: convcolonly for Core_Walls, Front_Wall, guards (>=1.07 m) on every core variant.
- TTQA-005 (blocker): F1 Spin Court hall (courts 1-8) – Rook: one thin box convcolonly per pane (full 2.06 m x 5.19 m).
- TTQA-006 (blocker): Restrooms F1/F2 (10 blocks) + F3 (4) – Rook: add convcolonly for wet wall, partitions, pilasters, doors (doors can be static closed).
- TTQA-014 (major): Facade, all floors – Rook: include mullion/fin volume in panel colonly.
- TTQA-015 (major): F3 corners (4) – Rook: convcolonly box for each closure.
- TTQA-016 (major): F1/F2 Arcade – Rook: convcolonly per pod/racer, guard panels.
- TTQA-017 (major): F1 Food court / F3 dining – Rook: counters convcolonly; chairs simple box.
- TTQA-018 (major): F2 Gym – Rook: box colliders per machine.
- TTQA-019 (major): F1 Bowling – Rook: masking unit + panel colliders.
- TTQA-020 (major): F3 Stands – Rook: add aisle step colonly every ~6 m.
- TTQA-026 (major): F2 Climbing – Rook: snap to wall face.
- TTQA-027 (major): F2/F3 Aquatic truss – Vance/Rook: trim or reroute.
- TTQA-028 (major): Services – Vance: release spec; Rook: place.
- TTQA-030 (major): F1 Bowling – Rook: lengthen lane bed 1.29 m.
- TTQA-032 (minor): F3 Playground fence – Rook: single panel convcolonly per fence segment.
- TTQA-033 (minor): Misc props – Rook: add colliders to anything >0.3 m tall a player can touch.
- TTQA-034 (minor): Invisible colliders – Rook: shrink colonly to visual hull.
- TTQA-036 (minor): Stair cores – Rook: even risers.
- TTQA-037 (minor): Slides – Rook: tighten slide colonly; Gage: flag slide as non-walkable.
- TTQA-038 (minor): F2 Climbing – Rook: offset mats 0.35 m from panels.
- TTQA-039 (minor): F2 Gallery – Rook: mount on wall or add plinth.
- TTQA-040 (minor): F3 Basketball – Rook: add hanger cables/truss.
- TTQA-041 (minor): F2 Leisure – Rook: add supports.
- TTQA-042 (minor): Rooftop/roof – Rook: trim.
- TTQA-043 (minor): Plinth – Rook: trim/extend.
- TTQA-044 (minor): F3 Playground – Rook: 5 mm lift for pads; trim fence at gate.
- TTQA-045 (minor): F1 Pools – Rook: snap.
- TTQA-046 (minor): F3 toddler zone – Rook: ok if intentional; else colonly.
- TTQA-047 (minor): F1 Axe throwing – Rook: move lines.

## Passes (checked, OK)

- S and N doors: both halves ENTER from drum floor, preface edge (14°) and at sprint.
- Stair cores: typical rise 0.171 m / run 0.28 m (within 0.16–0.18 / ≥0.28).
- Leisure ramp and pool ramp: 1:12.5 (0.08) slope.
- Basketball court 28 × 15 m, rim 3.04 m, backboard 1.18 m from baseline.
- Bowling lane width 1.066 m, approach 4.6 m. Axe target centre 1.52 m.
- Rink 62 × 27 m (NHL-ish 61 × 26).
- No walkable column without a surface (0 grid holes) – no fall-through into the void from open floor.
- Batcher/collision layers do not drop collision.

## Artifacts

- Screenshots: `/workspace/tt_qa_shots/S*.png` (S01 W terrace wall, S02 W terrace aerial, S03 E plaza wall, S04 F1 lift lobby, S06 player inside court glass line, S09 rink boards, S10 lap pool, S13 dark court hall, S16 bowling lanes, S19 F2 lift landing after fall, S20 player inside VR pods) (S19/S20 used a QA fill light at the camera; all others, incl. S13, show the shipped lighting).
- Plan maps: `map_F{1,2,3}_reachability.png` (green reachable, red isolated, blue ×: unguarded drops), `slice_F{1,2,3}_walkthrough.png` (black visible+collider, red visible no collider, blue invisible collider).
- Raw data: `/tmp/ttqa_a_{walk,place,grid,misc}.json`, `/tmp/ttqa_dropclusters.json`, `/tmp/ttqa_entry.log`, `/tmp/ttqa_verify.log` (box only). Probes: `/workspace/aegis-tt-qa/godot/_ttqa/` (untracked).
