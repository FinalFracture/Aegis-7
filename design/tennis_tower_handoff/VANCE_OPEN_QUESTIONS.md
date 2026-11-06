# Tennis Tower: open spec questions for Vance (Rook, Nov 4 2026)
Not sent. Kept as a file per Jared. Source: context/VOTE_LOG.md #52-#73.

## Slide tower (#59 tt_slide_tower.glb)
- Island datum: confirm the ground level the towers stand on (model base y 0).
- Bridge width conflict: the spec bridge is 2.4 m wide but the tower's bridge opening is 1.1 m (-X face, local z +1.2..+2.3). Which one wins?
- The bridge reaches T2 only. Confirm how T1 is reached, or whether T1 needs its own bridge or opening.

## Stand seats (#54 tt_stand_module / _f3)
- Confirm the bay count and run lengths (7.5 m tiling along X, front +Z = concourse) for F1/F2 (5 rows) and F3 (12 rows).
- Confirm the seat finish and colour (the V6 hybrid uses court rail with branch posts and leaf shades).

## Court glass / partitions (#56 tt_court_partition, net, door)
- Confirm the glass line offset: local z +0.2275 (panel/net) and -0.230 (door).
- Confirm the door positions (2 per box) and the parked-open 90° leaf.

## Climbing wall (#60 tt_climbing_panel, boulder, trim)
- Confirm the Stand-Back Wall layout (16 x 5 panels = 20 x 11.5 m) and the 19 m wall (15 panels + trim).
- Confirm where the boulder overhang goes. Its top kicks +0.73 m toward +Z, so check clearance.

## Kids' wall (#60 tt_climbing_panel_kids)
- Confirm the Z 15 face placement and count (12 panels, 1.25 x 5.0 m), and the fall-zone matting.

## Cabana (#61 tt_cabana)
- Confirm the 8 instances along X -11..-7, Z 18..62, with +Z rotated to face the W glass (-X).

## Bar (#62 tt_bar + 20 stools)
- Confirm the bar position and the staff opening (-Z) relative to the back-of-house route.

## Playground (#63-#72)
- Swing set (#64): built 7 x 4.45 m against the spec's 7 x 3 m. Check it still fits the 12 m E-terrace zone.
- Climbing dome (#65): the pad is Ø 7 m against the spec dome's Ø 4 m, because a fall zone was added.
- See-saws (#66): the spec has no footprint. Built 5 x 3 m.
- Toddler zone (#67): the spec says "4 spring riders + toddler deck in 8 x 8 m", but the winner is Meadow Hills (hills, tunnel, mini slide, pods, balance path). Please update the spec text.
- Balance beams (#68): the spec has no footprint. Built 8 x 5 m.
- Soft-play (#69): sunken pit or not? If sunken, cut the floor locally (circle r 1.08 at local (-0.9, 0.3)) and drop the pool 0.3-0.4 m.
- Benches (#70): positions for 6 instances facing the play pieces.
- Fence (#71): the solid screen blocks terrace sightlines. Keep it, or swap to 80 mm pickets or a 0.6 m kick-plate with pickets? Also, positions for the 3 gates.
- Surface (#72): floor replacement or overlay (top +0.038)? Keep the 0.10-0.12 m humps off accessible routes.
- Overall: the playground layout plan (positions of all pieces in the zone).

## Ridge crown (#73 tt_roof_ridge_crown)
- The ridge must sit on a mid-bay line of the roof grid (e.g. roof-tile local z 10). Confirm that spec Z 39.5 maps to one.
- The eaves sit ~0.2 m above the roof, not flush. Is that acceptable?
- Leaf relief reaches ~+26.36, above the +26.3 peak.

## Deferred
- Curtain wall moss + vine overlay (#52), deferred by Jared.

## Entrance bay (#74 tt_entrance_bay / _half)
- No F1/F2 façade definition: the spec only defines the F3 Glass Box wall (§3.11.1). Please define the F1/F2 elevation on all faces, including F2 (6.1..12.2) above the W doors (not built), and the S/N/E secondary entrances.
- 42 m door run = 10.5 x 4.0 m bays: the run is built as 10 x 4.0 m + 1 x 2.0 m half bay. Where does the half bay go, and how does the run align with the 8 m façade columns (not modelled as separate assets)?
- Door glass: built BLEND (envelope). §3.11.9 makes lobby / pool-hall glass opaque-frit alpha-scissor. Should the entrance doors switch to alpha-scissor (stacking with the Glass Box BLEND layer from the F3 terrace)?
- Canopy reach: the canopy projects 2.6 m over the West Arrival terrace (+3.0..+3.16, fascia to ~+3.3), and the kerb, hedge and bollards reach z 1.82 m. Neither is in the spec. Check the terrace circulation and egress width (§5.3) in front of the doors.

## Façade bay (#75 tt_facade_bay / _half)
- Which faces/runs get tt_facade_bay (S/N/E, W outside the 42 m doors)? Closure bays at the corners (1.5 m on the W/E faces per §3.11.1) have no F1/F2 module. Is a 1.5 m bay needed?
- The trunk stands 0.62 m proud of the glass on a 0.4 x 0.42 m pedestal (bay depth 1.66 m). Check the S/N aprons (1:12 over ~1 m at grade) and the Rim Promenade clear width.
- F1 glazing at the bowling, axe and WC bands: should those bays be opaque (slate) rather than glass?

## Plinth skirt (candidates, not promoted)
- Where is the plinth actually exposed? Per §3.3 the W and E faces sit on raised terraces at +4.0 HD, so the building plinth is buried there and the S/N faces are at grade. The 4.0 m skirt therefore reads only on the terrace edges (West Arrival / East Plaza perimeters, the East Spine ramp sides) unless something else is meant. Please confirm the runs and the faces.
- p(Z) varies 0..4.0 m along the W/E faces. The skirt is built as 4 x 1.0 m courses for trimming. Is a stepped trim acceptable, or is a sloped top / custom per-bay height needed?
- Stepped variants (V1/V2) project 1.6-1.85 m from the face line. Does that fit the plaza edge and the 1:12 aprons?

## Terrace decks + ramps (candidates, not promoted)
- No guard/handrail rules in the spec. The kit assumes IBC 2021: 1.07 m guards with < 100 mm openings at every terrace edge and ramp side with a drop > 0.76 m; no handrails on the 1:20 East Spine (a walking surface); no handrail on the 1:12 aprons (rise < 0.15 m). Please confirm, or give the project rule.
- S/N aprons: §3.3 says the Rim Promenade (z -45) and N arm (z 45) are +5.1 HD while F1 is +4.0, yet the aprons are "1:12 over ~1 m" (only 0.083 m of rise). These don't reconcile (1.1 m at 1:12 needs ~13 m). Which way does the apron fall, and how big is the level change?
- Deck build-up: the deck tiles are 0.30 m deep (surface at +4.0, so the tiles sit at +3.70). Where the terrace edge is over the plinth skirt, the skirt top must be at +3.70, not +4.0 (trim 0.3 m off the top course, or a 3.7 m skirt variant). Also the spec says "deck on fill 1.4-4.0 m": confirm the retaining edge is the tt_plinth_skirt language.
- The East Spine ramp: 12 m wide x 80 m at 1:20 = 20 x 4 m modules per half (mirrored halves). Do any intermediate landings or rest areas apply (not required at 1:20 under IBC)? What retains the sides of the ramp (fill + skirt, or open structure)?
- The corner links (terrace to the loop arms, "+4.0..4.2, level") and the Fore Hub Station Walk steps + 1:12 switchback (§3.8) aren't covered by this kit yet. Do they need their own modules?

## Secondary entrances S/N/E (candidates, Rook 2026-11-05)
- Spec gives S/N at grade and E on the East Plaza terrace, and a ~10 m lift-lobby gap (X 66.5..76.5 / Station Walk x 126.5..136.5), but no F1 door count, clear width, canopy reach or wayfinding for the secondary doors. Candidates are an 8.0 m module (2 × 4 m façade columns) with 1 m façade fillers each side. Confirm width (8 vs 10 m), door count (2 double pairs built) and whether S/N share one asset mirrored on X.
- Canopy projects ~2.2 m over the apron / terrace (shorter than the W main's 2.6 m). Check Rim Promenade / East Plaza clear width and egress in front of the doors.
- Face glyph (S/N/E) is a parameter on the wayfinding blade. Prefer one GLB + face param, or three promoted assets?
- E sits on tt_terrace_* at +3.70; S/N sit on tt_terrace_apron at grade. Is a level-adjusted skirt / threshold needed under E, or does the terrace deck already cover it?
- F2 above the secondary doors is not modelled (module is F1 6.1 m only, matching #74). Confirm F2 treatment.
