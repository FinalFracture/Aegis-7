# Residential Exterior + 20 m Ring: Asset List v1 (Vance, Oct 29 2026)
Source: the approved `residential_exterior_plan_v1.md` and the **v1.1 QC plan** `residential_exterior_plan_v1_1_plan.png` (counts updated for v1.1: poles 23→30, platform kerb 7→6). Checked against `godot/assets/models/` (24 glb files).
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
| 15 | Tram stop shelter (lived-in) | promenade, X 10..16 | 1 | 6.0 × 1.3 × 2.8 | 6,000 |
| 16 | Tram platform kerb module | stop platform, X 9..21 | 6 | 2.0 × 1.9 × 0.3 | 300 |
| 17 | Tram rail module (twin track, axial) | Z -19..-22 | 10 | 10 × 3.5 | 400 |
| 18 | Catenary mast + wire span | along tram line | 5 | 0.3 × 3.5 × 6.0 | 900 |
| 19 | Tram vehicle (live, 2-car) | tram line | 1 | 24 × 2.6 × 3.4 | 18,000 |
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
| 25 | **APPROVED (Jared, Oct 29, for now):** sidewalk hydro planter = Tiered Steps TS-4, 4 m length along Z, back to the Spin St W kerb (X -16.8..-16.39), 1 patched liner | west sidewalk, z0 -7, -2, 3 | 3 TS-4 | 0.41 × 4.0 × 0.70 | 2,784 |

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
| 49 | Patch tape + mismatched liner decals | hydro beds, planters | 1 | set | 100 |
| 50 | Litter / spill drift decals (Coriolis, antispinward) | Spin Sts | 1 | set | 200 |
| 51 | Sprocket wheel-track + coupler-scuff decals | apron, door jamb | 1 | set | 100 |
| 52 | Pictogram notice board (wordless) | stop | 1 | 1.0 × 0.1 × 1.4 | 400 |

## L. Characters (placed, already modeled)
| # | Item | Where | Qty | Size | Tris (each) |
|---|---|---|---|---|---|
| 53 | ~~Sprocket~~ `godot/assets/models/char_bot_r2_05_livery_01_sprocket.glb` | service route | 1 | 0.78 × 0.77 × 1.03 | — |
| 54 | ~~Citizen commuter~~ `godot/assets/models/char_citizen_commuter.glb` | tram stop, promenade | 4 | human | — |
| 55 | ~~Clover (agri bot)~~ `godot/assets/models/char_bot_r2_05_livery_04_clover.glb` | hydro co-op | 1 | same as Sprocket | — |

## Counts
- **Total items: 55.** Already modeled as glb: **5** (#1, 2, 53, 54, 55), plus the Tiered Steps TS-4 module that #23, #25 and #26 now use. Still to model: **50**; for #23, #25 and #26 this is only the TS-2 cut-down variant and the patched liner.
- **Tiered Steps tri impact (Oct 29):** planters + beds rise from about 16.4k to about 77k tris (23 TS-4 × 2,784 + 9 TS-2 × ~1,500), so the ring goes from **~209k to ~270k** LOD0. The approved lower-detail version (#23b, ~900 tris) beyond 20 m keeps the ≤ 60k on-screen target. Fit QC: `residential_exterior_tiered_steps_fit.py`.
- The ring totals about **209k** tris (LOD0, all placed instances). The tram vehicle is 18k of that, and the 5 neighbour facades are 20.5k together. With instancing plus LOD1 beyond 20 m, the on-screen target is ≤ 60k.

## Suggested modeling order (most reused first)
1. Curb segment (68), Residential facade panel (60), Canal edge module (47), Curved road segment (34), Street light pole (30), Exterior window unit (24), Flat road / lane segment (20), Tiered Steps TS-2 variant (9; TS-4 done), Bollard (12), Tram rail module (10), Bench (8), Accessible kerb ramp (8)
2. Mid-reuse kit: catenary mast (5), bins (6), plaza bollard lights (6), tram platform kerb (6), wayfinding totems and street blades (4 each)
3. Hero pieces: tram stop shelter, tram vehicle, the 5 neighbour facades, roof parapet, door canopies
4. Hydro co-op and planters: Tiered Steps TS-2 variant (#23a) + lower-detail version (#23b) + patched liner (TS-4 done), grow racks, pump cabinet
5. Story singles: memorial nook set, shelter sleeper set, notice board, hand cart, exterior Sprocket pad/apron, decal sets
