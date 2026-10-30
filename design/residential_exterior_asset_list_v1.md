# Residential Exterior + 20 m Ring: Asset List v1 (Vance, Oct 29 2026; finalized 2026-10-30)
**Status: FINAL (2026-10-30, Vance). Exterior sprint approved by Jared (relayed by Atlas); build order for Rook is in "Prioritized modeling order" at the end.** History: DRAFT v1 Oct 29. Readiness pass Oct 29: rows were checked against `godot/assets/models/` (46 glb files), and counts were checked against the v1.2 plan and the Tiered Steps swap.
Source: the approved `residential_exterior_plan_v1.md` and the **v1.1 QC plan** `residential_exterior_plan_v1_1_plan.png` (counts updated for v1.1: poles 23→30, platform kerb 7→6). (Final reconciliation 2026-10-30 against the APPROVED v1.2 plan; see "Final reconciliation".)
~~Struck through~~ means already modeled as a glb (path cited). Sizes are rough W × D × H in meters. Tris are per instance (LOD0); already-modeled items are not counted. Instanced kits are batched with MultiMesh.

## A. Doors, building fixtures and service
| # | Item | Where | Qty | Size | Tris (each) |
|---|---|---|---|---|---|
| 1 | ~~Force-field door frame (2.0 m variant)~~ `godot/assets/models/rfid_forcefield_door.glb` | Maintenance north service door | 1 | 2.0 × 0.2 × 2.3 | — |
| 2 | ~~Bulkhead Hub~~ `godot/assets/models/door_hub_bulkhead.glb` | service door | 1 | 0.40 × 0.20 × 0.80 | — |
| 3 | Exterior Sprocket floor pad + coupler arm (same mesh as rev C pad) | north sidewalk at X 6.4..7.6, beside the service ramp | 1 | 1.2 × 1.2 | 900 |
| 4 | Service ramp coping + scuff/track decal (ramp is the apron, v1.1) | north wall, X 1..5.6 | 1 | 4.6 × 2.65 | 300 |
| 5 | Door canopy hood | Sector-4 exit, service door | 2 | 3.2 × 1.2 × 0.3 | 600 |

## B. Facade kits
| # | Item | Where | Qty | Size | Tris (each) |
|---|---|---|---|---|---|
| 6 | Residential facade panel (pearl cladding, graphite spandrel) | Residential, 4 walls × 2 floors | 60 | 3.0 × 0.2 × 4.4 | 400 |
| 7 | Exterior window unit (frame + glass; real interior ≤30 m, then card) | Residential outer walls | 24 | ~2.4 × 1.5 | 500 |
| 8 | L2 promenade window frame | stair landing, Z -9 | 1 | 2.4 × 2.0 | 600 |
| 9 | Roof parapet + plant cap | Residential roof | 1 | 28 × 18 edge | 3,000 |
| 10 | Neighbour facade (facade-only): R-6 residential | Plot W | 1 | 30 × 12 face | 5,000 |
| 11 | Neighbour facade: clinic / market hall | Plot E | 1 | 30 × 10 face | 5,000 |
| 12 | Neighbour facade: workshop row (roller shutters) | Plot N-E | 1 | 14 × 9 face | 4,000 |
| 13 | Neighbour facade: kiosk row | Plot SW | 1 | 17 × 4 face | 3,000 |
| 14 | Neighbour facade: tram depot edge | Plot SE | 1 | 20 × 7 face | 3,500 |

## C. Tram (live)
| # | Item | Where | Qty | Size | Tris (each) |
|---|---|---|---|---|---|
| 15 | Tram stop shelter (lived-in) | platform, X 12..18, Z -16.9..-15.6 (v1.2 plan) | 1 | 6.0 × 1.3 × 2.8 | 5,800 |
| 16 | Tram platform kerb module | stop platform, X 9..21 | 6 | 2.0 × 1.9 × 0.3 | 300 |
| 17 | Tram rail module (twin track, axial) | Z -19..-22 | 10 | 10 × 3.5 | 400 |
| 18 | Catenary mast + wire span | along tram line | 5 | 0.3 × 3.5 × 6.0 | 900 |
| 19 | Tram vehicle (live, 2-car), split for the <6,000 cap: **19a** car body w/ cab (one mesh, mirrored for car 2) 5,800; **19b** bogie + coupler 1,500 (×4); **19c** pantograph 800 (×1) | tram line | 1 set | 24 × 2.6 × 3.4 overall (car 12 × 2.6 × 3.4) | ~18,400 set |
| 20 | Stop totem / timetable panel | stop | 1 | 0.5 × 0.3 × 2.4 | 500 |

## D. Lighting
| # | Item | Where | Qty | Size | Tris (each) |
|---|---|---|---|---|---|
| 21 | Street light pole (amber) | promenade, plaza, sidewalks, outer sidewalks, kerb walk (v1.1: none in roads) | 30 | 0.3 × 0.3 × 5.0 | 1,200 |
| 22 | Low bollard light | plaza | 6 | 0.2 × 0.2 × 0.9 | 200 |

## E. Plinth masking (approved: hidden)
| # | Item | Where | Qty | Size | Tris (each) |
|---|---|---|---|---|---|
| 23 | **APPROVED (Jared, Oct 29, for now):** masking planter = **Tiered Steps** (Rook, `godot/assets/models/hydro_planter_tiered_exterior.glb`, 4.0 × 0.41 × 0.70, high tier against the wall). TS-4 modeled; TS-2 is a 2.0 m cut-down variant still to model | ±Z walls: S 2 × (TS-4, TS-4, TS-2) with 0.4 gaps, X -13.8..-3.0 / 3.0..13.8; N-W 3 × TS-4 with 0.2 gaps, X -13.8..-1.4; N-E TS-4 + TS-2 butted, X 8.0..14.0; Z ±9.1..±9.51 | 8 TS-4 + 3 TS-2 | 4.0 / 2.0 × 0.41 × 0.70 | 2,784 / ~1,500 |
| 23a | Tiered Steps **TS-2** variant (APPROVED): 2.0 m cut-down of TS-4 with the same 3 troughs, levelling feet and latched lids. Used on the south wall beside the exit ramp and as bed/run ends | S wall (2), N-E (1), hydro beds (6) | 9 | 2.0 × 0.41 × 0.70 | ~1,500 |
| 23b | Tiered Steps **lower-detail version** (APPROVED): ~900 tris, foliage merged, lids and feet simplified. Used beyond 20 m for TS-4 and TS-2 | all TS instances beyond 20 m | LOD of 23/23a | same | ~900 |
| 24 | Ramp 1:12, 0.22 m rise | Sector-4 exit, service door | 2 | 3.6–4.7 × 2.7 | 250 |
| 25 | ~~**APPROVED (Jared, Oct 29, for now):** sidewalk hydro planter = Tiered Steps TS-4~~ (modeled: `godot/assets/models/hydro_planter_tiered_exterior.glb`), 4 m length along Z, back to the Spin St W kerb (X -16.8..-16.39), 1 patched liner | west sidewalk, z0 -7, -2, 3 | 3 TS-4 | 0.41 × 4.0 × 0.70 | 2,784 |

## F. Hydro co-op
| # | Item | Where | Qty | Size | Tris (each) |
|---|---|---|---|---|---|
| 26 | **APPROVED (Jared, Oct 29, for now):** hydro bed = back-to-back Tiered Steps pair (2 × 0.41 + 0.08 spine = 0.9) × (TS-4 + TS-4 + TS-2 = 10.0 m), 1 patched liner. v1 row said 14 m at X -20..-6, but the v1.2 plan has 10 m at X -13..-3; corrected | hydro co-op, X -13..-3, Z 19.5 / 21.5 / 23.5 | 3 beds = 12 TS-4 + 6 TS-2 | 10.0 × 0.9 × 0.70 | 2,784 / ~1,500 |
| 27 | Pump + water tank cabinet | hydro co-op | 1 | 1.2 × 0.8 × 1.8 | 1,200 |
| 28 | Grow-light rack (length now matches the 10 m beds) | hydro co-op | 3 | 10 × 0.2 × 2.2 | 700 |

## G. Memorial nook
| # | Item | Where | Qty | Size | Tris (each) |
|---|---|---|---|---|---|
| 29 | Wire rack with hanging RFID tags | SE corner | 1 | 1.2 × 0.3 × 1.8 | 1,500 |
| 30 | Violet field lamp (shrine) | SE corner | 1 | 0.3 × 0.3 × 1.2 | 600 |
| 31 | Dried flower / offering set | SE corner | 1 | 0.6 × 0.3 × 0.3 | 800 |

## H. Street furniture
| # | Item | Where | Qty | Size | Tris (each) |
|---|---|---|---|---|---|
| 32 | Bench | tram platform 2, promenade (canal-facing) 4, plaza edge 1, memorial nook 1 (placed v1.2) | 8 | 1.8 × 0.5 × 0.45 | 800 |
| 33 | Bin / recycler | tram stop 2, beside benches 4 (placed v1.2) | 6 | 0.5 × 0.5 × 1.0 | 400 |
| 34 | Bollard (cart barrier) | Spin St ends 4 + 4, service ramp edge 2 + 2 (placed v1.2) | 12 | 0.2 × 0.2 × 0.9 | 150 |
| 35 | Utility junction cabinet | service lane | 3 | 0.8 × 0.4 × 1.4 | 400 |
| 36 | Service hand cart | apron | 1 | 1.4 × 0.7 × 1.0 | 900 |

## I. Signage and wayfinding
| # | Item | Where | Qty | Size | Tris (each) |
|---|---|---|---|---|---|
| 37 | Sector-4 lit sign | above exit | 1 | 2.6 × 0.1 × 0.5 | 300 |
| 38 | Wayfinding totem (spinward/antispinward pictograms) | corners | 4 | 0.5 × 0.3 × 2.2 | 800 |
| 39 | Street name blade | Spin St W/E, service lane | 4 | 0.8 × 0.05 × 0.2 | 100 |
| 40 | Ground decal set (spin arrows, chevrons, Sprocket lane) | streets, lane | 1 | decals | 200 |

## J. Paving, curb and canal edge
| # | Item | Where | Qty | Size | Tris (each) |
|---|---|---|---|---|---|
| 41 | Curb segment (straight 2 m + corner) | all street edges | 68 | 2.0 × 0.3 × 0.15 | 120 |
| 42 | Curved road segment (bent to R 185.5 along Z) | Spin Sts W/E | 34 | 5.0 × 6.0 | 200 |
| 43 | Flat road / lane segment (axial) | service lane, tram bed | 20 | 5.0 × 4.0 | 100 |
| 44 | Paving tile kit (pearl promenade, warm plaza) | promenade, plaza, sidewalks | 2 | tiling | 200 |
| 45 | Accessible kerb ramp | corners, crossings | 8 | 1.5 × 1.2 | 150 |
| 46 | Canal edge module (railing + coping) | esplanade edge | 47 | 2.0 × 0.4 × 1.1 | 300 |
| 47 | Desire-path wear decal | plaza, promenade | 2 | decals | 50 |

## K. Lived-in story props
| # | Item | Where | Qty | Size | Tris (each) |
|---|---|---|---|---|---|
| 48 | Bedroll + hot plate + crate (shelter sleeper) | tram shelter | 1 | set | 1,500 |
| 49 | Patch tape + mismatched liner decals + **dead-foliage material swap** for one west-sidewalk TS-4 (plan story beat) | hydro beds, planters | 1 | set | 100 |
| 50 | Litter / spill drift decals (Coriolis, antispinward) | Spin Sts | 1 | set | 200 |
| 51 | Sprocket wheel-track + coupler-scuff decals, + **kerb scuff decals at the stop** (plan wear beat) | apron, door jamb, platform kerb | 1 | set | 100 |
| 52 | Pictogram notice board (wordless) | stop | 1 | 1.0 × 0.1 × 1.4 | 400 |

## L. Characters (placed, already modeled)
| # | Item | Where | Qty | Size | Tris (each) |
|---|---|---|---|---|---|
| 53 | ~~Sprocket~~ `godot/assets/models/char_bot_r2_05_livery_01_sprocket.glb` | service route | 1 | 0.78 × 0.77 × 1.03 | — |
| 54 | ~~Citizen commuter~~ `godot/assets/models/char_citizen_commuter.glb` | tram stop, promenade | 4 | human | — |
| 55 | ~~Clover (agri bot)~~ `godot/assets/models/char_bot_r2_05_livery_04_clover.glb` | hydro co-op | 1 | same as Sprocket | — |

## Counts
- **Total items: 57** (55 + #23a TS-2 + #23b lower-detail version). Already modeled as glb: **6** (#1, 2, 25, 53, 54, 55). Still to model: **51**. #23 and #26 are partly done: TS-4 exists and they wait only on #23a TS-2; #25's patched liner is decal #49.
- **Counts match the v1.2 plan:** benches 8, bins 6, bollards 12, poles 30, platform kerb 6. Tiered Steps: walls 8 TS-4 + 3 TS-2, sidewalk 3 TS-4, beds 12 TS-4 + 6 TS-2, so 23 TS-4 + 9 TS-2 in all.
- **Tiered Steps tri impact (Oct 29):** planters + beds rise from about 16.4k to about 77k tris (23 TS-4 × 2,784 + 9 TS-2 × ~1,500), so the ring goes from **~209k to ~270k** LOD0. The approved lower-detail version (#23b, ~900 tris) beyond 20 m keeps the ≤ 60k on-screen target. Fit QC: `residential_exterior_tiered_steps_fit.py`.
- (Superseded by the Tiered Steps line above: ~270k LOD0.) Pre-swap the ring totalled about **209k** tris (LOD0, all placed instances). The tram vehicle is 18k of that, and the 5 neighbour facades are 20.5k together. With instancing plus LOD1 beyond 20 m, the on-screen target is ≤ 60k.

## Suggested modeling order (most reused first)
1. Curb segment (68), Residential facade panel (60), Canal edge module (47), Curved road segment (34), Street light pole (30), Exterior window unit (24), Flat road / lane segment (20), Tiered Steps TS-2 variant (9; TS-4 done), Bollard (12), Tram rail module (10), Bench (8), Accessible kerb ramp (8)
2. Mid-reuse kit: catenary mast (5), bins (6), plaza bollard lights (6), tram platform kerb (6), wayfinding totems and street blades (4 each)
3. Hero pieces: tram stop shelter, tram vehicle, the 5 neighbour facades, roof parapet, door canopies
4. Hydro co-op and planters: Tiered Steps TS-2 variant (#23a) + lower-detail version (#23b) + patched liner (TS-4 done), grow racks, pump cabinet
5. Story singles: memorial nook set, shelter sleeper set, notice board, hand cart, exterior Sprocket pad/apron, decal sets

## Final reconciliation vs plan v1.2 (2026-10-30)
- Counts re-checked: benches 8, bins 6, bollards 12, poles 30, platform kerb 6, Tiered Steps 23 TS-4 + 9 TS-2 all match the plan. No missing structural assets.
- **Fixed #15** tram shelter location X 10..16 → **X 12..18, Z -16.9..-15.6** (plan v1.1 QC #6); tris 6,000 → 5,800 (cap is <6,000).
- **Fixed #19** tram vehicle 18k single mesh broke the <6,000 cap → split into 19a car body (5,800, mirrored), 19b bogie+coupler (1,500), 19c pantograph (800).
- **Added to #49** dead-planter material swap (plan: "one west planter is dead"); **added to #51** scuffed-kerb decals at the stop (plan wear beat).
- Stale header counts (24 / 46 glb) and the 209k total marked superseded (~270k LOD0, ≤60k on-screen with #23b LOD).
- Extras kept (not in plan text but compatible): #5 door canopies, #22 plaza bollard lights, #35 junction cabinets, #36 hand cart.

## Aegis-7 build rules (all batches)
- <6,000 tris per glb (LOD0); bottom-center pivot at (0,0,0), +Z facing (front/street face toward +Z in model space); metres, real scale.
- Palette: Matte Titanium Alabaster `#D8DEE4` (~55%), Deep Structural Slate `#2A3038` (~20%), Brushed Machined Steel `#707A84` / rubber `#1E2228` (~15%); dept accents ≤10–15% (Engineering amber `#E89B2D`, Civic cyan `#38B8C8`, Science violet `#7B5CFF`, Agri emerald `#3BA868`). Street light amber `#FF9500`. Pearl cladding + graphite spandrel on facades; <1.2% micro-noise PBR.
- Glass: alphaMode **BLEND**, light tint, no opaque glass.
- **5-candidate workflow:** 5 iterations per asset (`<name>_01..05.glb`), render a comparison sheet, team votes post-render in `context/VOTE_LOG.md`, winner copied to `godot/assets/models/<name>.glb`. Kit modules (curbs, road, rails) may run 5 iterations on the first module and derive siblings from the winner.

## Prioritized modeling order for Rook (FINAL)
### Batch 1 — hero / blocking structural (defines the silhouette; 9 assets)
| Order | # | File | Size (m) | Tris | Spec / materials |
|---|---|---|---|---|---|
| 1 | 6 | `ext_facade_panel_res.glb` | 3.0 × 0.2 × 4.4 | ≤400 | Pearl alabaster cladding, graphite slate spandrel band, steel reveal; ×60 MultiMesh |
| 2 | 7 | `ext_window_unit.glb` | 2.4 × 0.15 × 1.5 | ≤500 | Slate frame, steel sill; glass pane separate surface alphaMode BLEND; ×24 |
| 3 | 9 | `ext_roof_parapet_plantcap.glb` | 28 × 18 edge × ~1.0 | ≤3,000 | Alabaster coping, slate plant-cap housings, amber hazard edge ≤10% |
| 4 | 15 | `ext_tram_shelter.glb` | 6.0 × 1.3 × 2.8 | ≤5,800 | Steel frame, BLEND glass walls, Civic cyan trim, timetable panel slot at rear (sleeper set #48 sits behind it) |
| 5 | 19a | `ext_tram_car_body.glb` | 12 × 2.6 × 3.4 | ≤5,800 | Alabaster body, slate skirt, cyan Civic livery stripe, BLEND windows; mirrored for car 2 |
| 6 | 19b | `ext_tram_bogie_coupler.glb` | 2.4 × 2.2 × 0.9 | ≤1,500 | Steel/rubber, slate; ×4 |
| 7 | 19c | `ext_tram_pantograph.glb` | 1.8 × 1.2 × 1.2 | ≤800 | Steel, amber contact shoe |
| 8 | 17 | `ext_tram_rail_module.glb` | 10 × 3.5 × 0.2 | ≤400 | Twin axial track, slate sleepers, steel rails; ×10 |
| 9 | 18 | `ext_catenary_mast_span.glb` | 0.3 × 3.5 × 6.0 | ≤900 | Slate mast, steel arm, wire span; ×5 |

### Batch 2 — ground kit (most reused; 9 assets)
#41 `ext_curb_segment.glb` (+ corner), #42 `ext_road_curved_R185.glb`, #43 `ext_road_flat.glb`, #44 `ext_paving_tile_kit.glb`, #45 `ext_kerb_ramp.glb`, #46 `ext_canal_edge_module.glb`, #16 `ext_tram_platform_kerb.glb`, #24 `ext_ramp_1to12.glb`, #4 `ext_service_ramp_coping.glb`.

### Batch 3 — neighbour facades + door fixtures (8 assets)
#10 `ext_nbr_r6_residential.glb`, #11 `ext_nbr_clinic_market.glb`, #12 `ext_nbr_workshop_row.glb`, #13 `ext_nbr_kiosk_row.glb`, #14 `ext_nbr_tram_depot.glb`, #8 `ext_l2_promenade_window.glb` (BLEND glass), #5 `ext_door_canopy.glb`, #37 `ext_sector4_sign.glb`.

### Batch 4 — lighting + street furniture + wayfinding (11 assets)
#21 `ext_street_light_pole.glb` (amber `#FF9500`), #22 `ext_bollard_light.glb`, #32 `ext_bench.glb`, #33 `ext_bin_recycler.glb`, #34 `ext_bollard.glb`, #35 `ext_junction_cabinet.glb`, #20 `ext_stop_totem.glb`, #38 `ext_wayfinding_totem.glb`, #39 `ext_street_blade.glb`, #52 `ext_notice_board.glb`, #3 `ext_sprocket_pad.glb` (reuse rev C pad mesh).

### Batch 5 — hydro co-op + Tiered Steps variants (5 assets)
#23a `hydro_planter_tiered_ts2.glb`, #23b `hydro_planter_tiered_lod.glb` (TS-4 + TS-2 LOD ~900), #27 `ext_hydro_pump_tank.glb`, #28 `ext_grow_light_rack.glb`, #36 `ext_service_hand_cart.glb`.

### Batch 6 — story singles + decals (9 assets)
#29 `ext_memorial_tag_rack.glb`, #30 `ext_violet_field_lamp.glb` (Science violet `#7B5CFF`), #31 `ext_offering_set.glb`, #48 `ext_shelter_sleeper_set.glb`, decal sets #40, #47, #49, #50, #51 (Sloane textures; Rook only places quads).

Totals: **51 to-model entries** across 6 batches: 9 / 9 / 8 / 11 / 5 / 9 (#23 and #26 are complete once TS-2 #23a lands; tram #19 split into 19a/b/c). Already done: #1, 2, 25, 53, 54, 55 and TS-4.
