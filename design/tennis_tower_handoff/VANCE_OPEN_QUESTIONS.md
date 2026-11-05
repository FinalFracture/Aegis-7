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
