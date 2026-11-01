# Cylinder Hab-7: Master Bug List
Owner: Patch (QA lead). Created 2026-11-01. Base: main 7b46c85 (QA sources audited main 39eba42; Patch passes up to 1a349a3).
Sources: QA-02 geometry (cd17628), QA-03 visuals (404cdd7), QA-04 layout/props (b5b551a), QA-05 stability/input (7b46c85), and the open items in context/playtest_bug_report.md.
Master IDs: `M-xx`, in priority order. "Source IDs" keeps the original IDs. QA-04's LAY-xx are shown as L4-xx because they collide with the old fixed LAY-01/02.
Status values: Open, Open-blocked (waiting on a decision or approval), Deferred (accepted interim), Downgraded, Task (QA/tooling work).

## Critical / High
| Master | Sev | Owner | Location / file | Summary | Source IDs | Status |
|---|---|---|---|---|---|---|
| M-01 | High | Gage (Rook if a collision mesh is needed) | preface_playable_area.gd ANIMATED_PROP_SPECS; Prop38/39/42/43 nodes | Interactive props 38/39/42/43 have no CollisionObject3D. The player walks through them. | GEO-01 | Open |
| M-02 | High | Gage | preface_playable_area.gd:1830 (Prop43 still at (-8.00,0.235,8.50) yaw 180) | Prop43 clashes with the wall / built-ins and is not at the Rev 3 spot (-5.16,0.235,5.20) yaw -90. Causes 3 placement_assert failures (clearance, mesh_clearance, front_zone). | L4-01 (QA-04 LAY-01), Prop43 clash (1a349a3 pass) | Open-blocked (placement decision) |
| M-03 | High | Gage | preface_playable_area.gd (no refs) | The 8 interim props from strip4_preface_layout_v1 #5-#12 are not placed (suit storage, lost+found, tea set, clutter kit, telescope, lab crates 104/204, cycler lightbox). | L4-02 | Open |
| M-04 | High | Gage | preface_playable_area.gd:2289 (`directional_shadow_max_distance = 45.0`), _process sun orbit | The sun lights the interior through the opaque drum hull outside the 45 m shadow range. Only the 36 degree window should admit sunlight. | VIS-02 | Open |

## Medium
| Master | Sev | Owner | Location / file | Summary | Source IDs | Status |
|---|---|---|---|---|---|---|
| M-05 | Med | Gage | preface_playable_area.gd:3175 (`_sun.basis = ...`) | The orbiting sun lights the deck from below / through floors for about half of each 4-minute cycle. There is no occlusion fade. | VIS-03, LIT-01 | Downgraded High->Med (Patch measured only +15% luminance at +180 degrees, 797fc94) |
| M-06 | Med | Gage | preface_playable_area.gd `_cut_observation_window` (code-generated cut) | Jagged sawtooth shell fragments along the 36 degree window-slice edges. The cut is generated in code, so this is Gage's, not a Rook mesh. | WIN-01 | Open |
| M-07 | Med | Gage | renders / perf | 2,617 draw calls (paving and curbs drawn as separate meshes). Needs MultiMesh or merging, and a GPU fps run. No GPU numbers yet (QA-05). | PERF-01, QA-05 perf note | Open; needs GPU run (T-02) |
| M-08 | Med | Gage | pickups at y 0.98 / 5.02 / 5.10 (see QA-02) | 7 pickups are sunk 0.07-0.095 m into shelves and desks. | GEO-02 | Open |
| M-09 | Med | Gage | (-13.30,5.02,-4.95), (-12.85,5.02,-4.95) | The Apt 201 tool-wall spool and BCI headband float 0.675 m (past the shelf collider edge at x -12.74). | GEO-03 | Open |
| M-10 | Med | Gage | Ext_47 decal 1002/1003, about (2.0,0.18,-12.1) | Overlapping desire-path decals z-fight. | GEO-04 | Open |
| M-11 | Med | Gage | sprocket_lift.glb | The sprocket lift (9 clips) is not placed or wired. Rev C scope. | L4-03 | Downgraded High->Med; Open-blocked (Rev C build approval) |
| M-12 | Med | Gage | service_wall_rail_shuttle.glb | The service wall / pads / coupler arms are not placed or wired. Rev C scope. | L4-04 | Downgraded High->Med; Open-blocked (Rev C build approval) |
| M-13 | Med | Gage | folding_counter_fold_leaf_3p5.glb | The 3.5 m folding counter run is not placed. | L4-08 | Open |
| M-14 | Med | Gage + Jared | — | No spot for the 4.0 m reading bench. Needs Jared: rebuild, 3.0 m variant, or plaza. | L4-09 | Open-blocked (Jared) |
| M-15 | Med | Sloane | preface_playable_area.gd:1411 (`dup.emission = albedo*0.22`) | Blanket 22% self-emission on drum materials flattens lighting, ignores textures, and survives emergency lighting. | VIS-04 | Open |
| M-16 | Med | Sloane | `_set_emergency_lighting` ~L2367 | The emergency toggle restores wrong values (fill 0.34 vs authored 0.28, ambient 0.36 vs 0.42) and doesn't dim the luminaires, spots, or emission. | VIS-05 | Open |
| M-17 | Med | Sloane | Mat_ObservationWindowGlass ~L1417 | The window glass is invisible (alpha 0.06, metallic 0.85). No tint, Fresnel, or mullions. | VIS-06 | Open |
| M-18 | Med | Sloane | ObservationWindowGlass mesh ~L1430 | The strip and both cap discs are one double-sided alpha mesh, causing sorting errors against fields and starfield. | VIS-07 | Open |
| M-19 | Med | Sloane | .tscn Environment (reflected_light_source Sky) vs black BG; ReflectionProbe UPDATE_ONCE | Metals reflect a blue-grey sky that doesn't exist. The probe bakes before the interiors stream in. | VIS-08 | Open |
| M-20 | Med | Rook | Side_Room_East_Lounge / West_Storage vs *_SeamFix (x -4.75/-12.25/0.75/8.25) | SeamFix boxes are coplanar with the room shells (about 19 m2 each). Z-fight risk. Confirm visually. | GEO-05 | Open |
| M-21 | Med | Rook | DoorHubBulkhead DockPad_InductionRing vs DockPad_Chevrons, all 6 hubs | Coplanar dock-pad meshes z-fight. | GEO-06 | Open |

## Low
| Master | Sev | Owner | Location / file | Summary | Source IDs | Status |
|---|---|---|---|---|---|---|
| M-22 | Low | Gage | project.godot:16/92; Environment SSAO/SSR | gl_compatibility is the chosen renderer (D670-07 already gates SSR to forward_plus), so missing SSAO/SSR is a design tradeoff, not a bug. Action: drop or gate the dead SSAO settings, fix config/features ("Forward Plus" label), and fake contact shadows if needed. | VIS-01 | Downgraded High->Low (design) |
| M-23 | Low | Gage | preface_playable_area.gd:2703 (`KEY_E`, `KEY_F`, toggles) | Interact, RFID pulse and the toggles are hardcoded keys, so they can't be remapped (an `interact` action exists but is unused). Movement does use actions (L2771). SYS-03 cites player_camera.gd:104-188, but no scene uses that script (dead code). INPUT-01 was only partly fixed. | SYS-03, INPUT-01 (partial) | Open |
| M-24 | Low | Gage | nav bake | 40 navmesh islands plus "8 edge errors" (overlapping edges) at load. | NAV-02, GEO-09, SYS-02 | Open |
| M-25 | Low | Gage | engine exit | RID / ObjectDB / GL leaks at exit. Exit only. | E793-01, SYS-01 (QA-05 rated Med) | Open |
| M-26 | Low | Gage | --qa-reticle-stars-doors | QA run takes 554 s and keeps getting slower. | E793-02 | Open |
| M-27 | Low | Gage | preface_playable_area.gd:417 | Headless force-quits after about 4 frames unless a QA flag is set. Needs a --soak flag for stability runs. | SYS-04 | Open (tooling) |
| M-28 | Low | Gage | `_run_qa_egress`, `_run_qa_player_exit` | Egress test hardening: add Y bands per waypoint (a fall would pass), pass doors only once the player is through, stop on first failure, use input actions. player-exit writes rotation_degrees.y directly. | egress review (1a349a3 pass) | Open (tooling) |
| M-29 | Low | Gage | Prop42 (10.68,8.35) / Prop39 (-4.10,8.55) / Prop38 (-1.85,8.45) | Interim positions differ from Rev C. Accepted for the preface; move at the Rev C rebuild. | L4-05, L4-06, L4-07 | Deferred |
| M-30 | Low | Gage | 37 Rev C GLBs | Rev C interiors are unbuilt (no references). | L4-10 | Downgraded Med->Low; Open-blocked (Rev C approval) |
| M-31 | Low | Gage | Hatch_D204_EmitterPanel (-11.20,5.45,-5.30) | Confirm the troubleshoot panel isn't standing in for the moved emitter bench #31. Also, D-204 is a panel, not a walkable hatch (HATCH-01, ee61cb6). | L4-12, HATCH-01 | Open (confirm) |
| M-32 | Low | Gage | R_HULL_FLOOR 185.5 vs plan R=200 | The bend radius isn't verified in code. | L4-13 | Open (verify) |
| M-33 | Low | Sloane | starfield end caps ~L4499 | Stars are stretched and shimmer on the end-cap discs (cap UVs, 6x3 scale). | VIS-09 | Open |
| M-34 | Low | Sloane | material import loop ~L2440-2460 | All prop glass is forced to one grey-blue, and every surface is CULL_DISABLED. | VIS-10 | Open |
| M-35 | Low | Sloane | `_add_recreation_grass_slab` ~L1562 | The grass slab is a flat untextured green placeholder. | VIS-11, grass placeholder (797fc94) | Open |
| M-36 | Low | Sloane | Seam03_Alcove2C_EastRail / Rail | The Alcove 2C rail renders as a flat untextured grey slab. | RAIL-01 | Open |
| M-37 | Low | Sloane | — | Window cards x8 and removal decals are not modeled. | L4-11 | Open |
| M-38 | Low | Rook | APT 201 (-13.65,2.65), APT 202 (13.65,2.65); side-room front corners z~2.92 | Outer front corners are 0.05 m short. Side-room SeamFix walls leave about a 0.02 m slot behind the front wall. | SEAM-04 | Open |
| M-39 | Low | Rook | DoorHubBulkhead TalkPad vs IntercomRing | Coplanar faces (about 3 cm2). | GEO-07 | Open |
| M-40 | Low | Rook | Open_Portal_Sector_Exit (z -8.76) | Portal face is coplanar with the vestibule shell (about 9.35 m2). | GEO-08 | Open |
| M-41 | Low | Gage | DOOR_APT201 open portal | Open portal / door frame gap check (DOOR-04 closed at 1a349a3, so no gap expected). Placeholder for capsule-sweep results. | — | see sweep |

## QA tasks
| Task | Owner | Summary | Status |
|---|---|---|---|
| T-01 | Patch | Capsule sweep (r=0.35) along every interior wall and corner, to find squeeze-through gaps (QA-02 limit). | In progress |
| T-02 | Patch / Jared GPU box | GPU run: --render-all for QA-03 light levels, plus fps for PERF-01 / QA-05. | Open |

## Merged duplicates
- VIS-03 = LIT-01 -> M-05
- QA-04 LAY-01 = Prop43 clash -> M-02
- VIS-11 = grass placeholder -> M-35
- GEO-09 = SYS-02 = NAV-02 edge errors -> M-24
- SYS-01 = E793-01 -> M-25
- SYS-03 = INPUT-01 remainder -> M-23
- L4-12 + HATCH-01 -> M-31
- L4-05/06/07 interim offsets -> M-29

## Reserved for QA-01
(QA-01 findings will be added here and merged into the tables above.)
