# Tennis Tower: open spec questions for Vance (Rook, Nov 4 2026)
**Answered by Vance, 2026-11-06.** Spec changes are folded into `design/strip5_tennis_tower_v1.md` **Rev 2.8** (§3.12). Sports and fittings are story decoration (Jared), so these answers favour buildable, consistent geometry over regulation detail.

## Lobby / aquarium corridor (Vance priority item, added 2026-11-06)
- **Decision: a real aquarium tank wall along the N side of the corridor** (Vance proposal), the story set-piece between the foyer and the courts.
  - **Corridor:** X 0..30, Z 34.5..44.5; clear walk X 0..24.5 (LW and lift W at the E end). The X 0 / Z 39.5 column stays: clad it as a portal pier, which splits the foyer mouth into two 4.5 m openings.
  - **Tank:** X 1..23, Z 42.5..44.5 (22 × 2.0 m), water 2.8 m deep, tank top +3.2 above F1. **Acrylic line on Z 42.5** (facing −Z into the corridor), 4 panels × 5.5 m, 0.2 m thick, F1 +0.2..+3.0 visible. **Corridor clear width 8.0 m** (Z 34.5..42.5).
  - **Back of tank:** opaque, a painted deep-blue reef backdrop on the Z 44.5 wall (nothing visible through the tank). **Service catwalk** over the tank at +3.4, through a hatch from the F2 view bridge. Load: 2.8 m water + 0.5 m tank slab ≈ 39.5 kPa on the F1 slab over 3.9 m of plinth ✓.
  - **Floor finish:** dark slate terrazzo, a 0.3 m cyan `#00E5FF` inlay strip along Z 41.5 (0.9 m off the acrylic as a lean-rail line) and a caustic-light decal pool along the tank.
  - **Props:** 4 benches facing the tank (backs to Z 35.5); 2 info plinths; 1 lean rail at Z 41.9 along the acrylic; 3 ceiling caustic projectors; 4 life-support grille panels under the tank lip; aquascape inside (rock + kelp mesh); fish deferred (a later Gage item).
  - **Wayfinding:** overhead blade at X 1, "COURTS · LIFT W · STAIR LW →"; blade at X 24, "← FOYER · EXIT"; floor arrow decals; an "AQUATICS" sign at the S edge doorways onto the lap/diving deck.
  - **Transparency rule:** **the tank acrylic is a single BLEND layer** (allowed). The rule is: **at most one BLEND layer in any line of sight.** Behind the acrylic is opaque, and nothing in front of it is BLEND (F1 glass is alpha-scissor), so it complies. The §3.11.9 alpha-scissor / opaque-frit rule covers the rest of the lobby and pool-hall glass, not the tank.
Not sent. Kept as a file per Jared. Source: context/VOTE_LOG.md #52-#73.

## Slide tower (#59 tt_slide_tower.glb)
- Island datum: confirm the ground level the towers stand on (model base y 0).
  - **Vance answer:** Island datum is **F1 + 1.0 m** (the river-tank deck level; the 1.0 m river sits in a tank on the F1 slab). Model base y 0 = F1 + 1.0. The start deck stays at +7.0 above F1, i.e. 6.0 m above the island.
- Bridge width conflict: the spec bridge is 2.4 m wide but the tower's bridge opening is 1.1 m (-X face, local z +1.2..+2.3). Which one wins?
  - **Vance answer:** **Both stand.** The bridge structure is 2.4 m wide (spec). It **necks down to a 1.1 m gate** at the T2 opening (the queue gate where riders are dispatched one at a time). Keep the tower's 1.1 m opening and add a 0.65 m solid flare panel each side at the bridge end (Vance proposal).
- The bridge reaches T2 only. Confirm how T1 is reached, or whether T1 needs its own bridge or opening.
  - **Vance answer:** T1 is reached from T2: a **1.0 m-long, 1.1 m-wide link deck at +7.0** across the 1 m gap between the towers (Z 56..57), with a matching 1.1 m opening on T1's +Z face (Vance proposal). No second bridge.

## Stand seats (#54 tt_stand_module / _f3)
- Confirm the bay count and run lengths (7.5 m tiling along X, front +Z = concourse) for F1/F2 (5 rows) and F3 (12 rows).
  - **Vance answer:** Rev 2.7 runs (corner stairs take 4.7 m of each long segment). **Long segments: X 40.2..66.5 and 76.5..102.8 = 26.3 m each = 3 × 7.5 m bays + 1 cut bay of 3.8 m** (cut bay at the corner-stair end). **Short segments: Z 20.5..34.5 and 44.5..58.5 = 14.0 m = 1 × 7.5 + 1 cut bay of 6.5 m** (cut bay at the lift-gap end). The same runs apply on F1/F2 (5 rows) and F3 (12 rows; F3 short stands sit at X 24.1..35.5 / 107.5..118.9). Front (+Z local) = concourse side on every segment; rotate per side.
- Confirm the seat finish and colour (the V6 hybrid uses court rail with branch posts and leaf shades).
  - **Vance answer:** **Accept the V6 hybrid.** Seat shells matte white `#D8DEE6`, court rail and branch posts gunmetal `#1A1E24`, leaf shades in a desaturated green with a cyan `#00E5FF` edge strip on every 4th bay.

## Court glass / partitions (#56 tt_court_partition, net, door)
- Confirm the glass line offset: local z +0.2275 (panel/net) and -0.230 (door).
  - **Vance answer:** **Confirmed:** panel/net at local z +0.2275, door at −0.230 (the door leaf sits inboard of the glass line so it swings clear of the posts).
- Confirm the door positions (2 per box) and the parked-open 90° leaf.
  - **Vance answer:** **2 doors per box, one at the middle of each long side** (X = box centre), diagonally useful for both halves. The parked-open 90° leaf is a variant; **default is closed**.

## Climbing wall (#60 tt_climbing_panel, boulder, trim)
- Confirm the Stand-Back Wall layout (16 x 5 panels = 20 x 11.5 m) and the 19 m wall (15 panels + trim).
  - **Vance answer:** **Confirmed:** Stand-Back Wall 16 × 5 panels = 20 × 11.5 m (X 36..56, face at Z 8). The **19 m bouldering wall runs along the Z 15 back wall of the hall** (X 94..113), 15 panels + 0.25 m trim; the 15 m walls are on X 113 (E, 12 panels) and X 94 (W, the training/spray wall).
- Confirm where the boulder overhang goes. Its top kicks +0.73 m toward +Z, so check clearance.
  - **Vance answer:** Overhang segments go on the **19 m Z 15 wall, mirrored so the +0.73 m kick points −Z** (into the hall). The hall is 15 m deep, so with a 2.0 m mat zone there's ≥ 12 m left. Do not put overhangs on the X 94 training wall.

## Kids' wall (#60 tt_climbing_panel_kids)
- Confirm the Z 15 face placement and count (12 panels, 1.25 x 5.0 m), and the fall-zone matting.
  - **Vance answer:** **Correction: the kids' wall is on the X 84.5 face** (the E face fixed in Rev 2.6, running Z 0..15 = 15 m), **not Z 15** (that face is only 7.5 m). 12 panels × 1.25 × 5.0 m, TC-S3 built in as the climbable pillar near Z 8.5. **Fall zone: 0.3 m mat, 2.0 m deep (X 82.5..84.5), full length.** Spec text corrected in Rev 2.8.

## Cabana (#61 tt_cabana)
- Confirm the 8 instances along X -11..-7, Z 18..62, with +Z rotated to face the W glass (-X).
  - **Vance answer:** **Confirmed:** 8 cabanas, X −11..−7, centres at Z 20 + 5.5k (Z 18..62), open side facing the W glass (−X). Rev 2.7 note: ST-AQS/AQN are at X −6..0, so the cabana row (X ≤ −7) stays clear by 1 m.

## Bar (#62 tt_bar + 20 stools)
- Confirm the bar position and the staff opening (-Z) relative to the back-of-house route.
  - **Vance answer:** Bar stays at **X 8..20, Z 35..44**. **Move the staff opening to the +X end** (facing the lift W / LW landing at X 24.5..30, the back-of-house route to the F1 food court). Guests use the N, S and W faces. **Accessible section: 1.5 m long at 0.86 m top, knee clear, at the W end of the S face** (Vance proposal).

## Playground (#63-#72)
- Swing set (#64): built 7 x 4.45 m against the spec's 7 x 3 m. Check it still fits the 12 m E-terrace zone.
  - **Vance answer:** **Fits.** Placed with the beam along Z (swinging along X, zero Coriolis): 4.45 (X) × 7 (Z) at X 130..134.45, Z 37..44. Plan in 'Overall' below.
- Climbing dome (#65): the pad is Ø 7 m against the spec dome's Ø 4 m, because a fall zone was added.
  - **Vance answer:** **Accept the Ø 7 m pad** (fall zone is right). Centre X 134, Z 48.4.
- See-saws (#66): the spec has no footprint. Built 5 x 3 m.
  - **Vance answer:** **Accept 5 × 3 m** (2 see-saws in one pad). Place it as **3 (X) × 5 (Z), with the see-saws side by side, each rocking along X** (axial, zero Coriolis), at X 135..138, Z 30.5..35.5.
- Toddler zone (#67): the spec says "4 spring riders + toddler deck in 8 x 8 m", but the winner is Meadow Hills (hills, tunnel, mini slide, pods, balance path). Please update the spec text.
  - **Vance answer:** **Accepted: Meadow Hills** (hills, tunnel, mini slide, pods, balance path) replaces the 4 spring riders + deck. 8 × 8 m at X 130..138, Z 21.5..29.5. Spec updated in Rev 2.8.
- Balance beams (#68): the spec has no footprint. Built 8 x 5 m.
  - **Vance answer:** **Accept 8 × 5 m**, placed 5 (X) × 8 (Z) at X 134.8..139.8, Z 36.5..44.5 (beams along Z are fine; walking speed is low).
- Soft-play (#69): sunken pit or not? If sunken, cut the floor locally (circle r 1.08 at local (-0.9, 0.3)) and drop the pool 0.3-0.4 m.
  - **Vance answer:** **Not sunken.** Use a raised rim (0.35 m) on the overlay surface; don't cut the F3 slab (it is the arcade ceiling below). Pad 4 × 4 m at X 130..134, Z 30.5..34.5.
- Benches (#70): positions for 6 instances facing the play pieces.
  - **Vance answer:** 6 benches on the inner accessible path (X 128.4..129.6), **facing +X toward the pieces**, at Z 23, 29, 35, 41, 47, 53.
- Fence (#71): the solid screen blocks terrace sightlines. Keep it, or swap to 80 mm pickets or a 0.6 m kick-plate with pickets? Also, positions for the 3 gates.
  - **Vance answer:** **Swap to a 0.6 m kick-plate + 80 mm pickets** (1.2 m total, openings < 100 mm), so terrace sightlines stay. **Gates (1.5 m):** S gate on the Z 20.6 edge at X 128.5..130 (to ARS); N gate on the Z 58.4 edge at X 128.5..130 (to ARN); W gate on the X 128.3 edge at Z 50..51.5 (to the track crossing and ST+E).
- Surface (#72): floor replacement or overlay (top +0.038)? Keep the 0.10-0.12 m humps off accessible routes.
  - **Vance answer:** **Overlay** (top +0.038). Keep the 0.10–0.12 m humps off the **accessible path X 128.3..129.8** (flat, full length) and out of the gate approaches.
- Overall: the playground layout plan (positions of all pieces in the zone).
  - **Vance answer:** **Playground plan (zone X 128.3..140, Z 20.6..58.4; path X 128.3..129.8):** toddler Meadow Hills X 130..138 / Z 21.5..29.5 · soft-play X 130..134 / Z 30.5..34.5 · see-saws X 135..138 / Z 30.5..35.5 · swing set X 130..134.45 / Z 37..44 · balance beams X 134.8..139.8 / Z 36.5..44.5 · climbing dome Ø 7 centre (134, 48.4) · combo tower 8 (X) × 6 (Z) at X 130..138 / Z 52.4..58.4 (slides run along X) · benches as above. Spec updated in Rev 2.8.

## Ridge crown (#73 tt_roof_ridge_crown)
- The ridge must sit on a mid-bay line of the roof grid (e.g. roof-tile local z 10). Confirm that spec Z 39.5 maps to one.
  - **Vance answer:** **Yes.** Roof grid Z lines are 1.5 + 4j, so Z 39.5 is the middle of the 37.5..41.5 bay. In tile terms (tiles start at Z 1.5, 20 m each) that's **tile row 2, local z 18**, a mid-bay line ✓.
- The eaves sit ~0.2 m above the roof, not flush. Is that acceptable?
  - **Vance answer:** **Acceptable.** A 0.2 m reveal reads as a shadow gap.
- Leaf relief reaches ~+26.36, above the +26.3 peak.
  - **Vance answer:** **Acceptable.** Spec now reads: structural crown +26.3, **ornament to +26.4**.

## Deferred
- Curtain wall moss + vine overlay (#52), deferred by Jared.
  - **Vance answer:** Noted, stays deferred (Jared).

## Entrance bay (#74 tt_entrance_bay / _half)
- No F1/F2 façade definition: the spec only defines the F3 Glass Box wall (§3.11.1). Please define the F1/F2 elevation on all faces, including F2 (6.1..12.2) above the W doors (not built), and the S/N/E secondary entrances.
  - **Vance answer:** **Defined in spec §3.12.2 (Vance proposal).** Same 4.0 m bays and 8 m columns on all faces. **F1 (0..6.1):** storefront glass 4.0 m tall (2 × 2.0 m panes per bay) + a 2.1 m slate spandrel hiding the F2 slab zone; opaque slate where §3.12.2 lists. **F2 (6.1..12.2):** slate cladding with a 2.4 m ribbon window (+1.2..+3.6 above F2) and a 50 mm cyan LED reveal at each floor line. **F2 above the W doors:** the F2 gallery (changing/lockers) is slate with only a 0.6 m clerestory ribbon at the top, **except a 10 m glazed viewing window at Z 34.5..44.5** (centred on the gallery's viewing area). **Secondary entrances:** see that section.
- 42 m door run = 10.5 x 4.0 m bays: the run is built as 10 x 4.0 m + 1 x 2.0 m half bay. Where does the half bay go, and how does the run align with the 8 m façade columns (not modelled as separate assets)?
  - **Vance answer:** **Realigned to the grid: doors Z 17.5..61.5 = 44 m = 11 full 4.0 m bays, no half bay.** Grid lines are 1.5 + 4j, so 17.5 and 61.5 are on it, and the 8 m façade columns (Z 17.5, 25.5 … 57.5) fall on bay joints, built into the mullion (no separate asset). Main exit capacity goes up (44 m vs 29.9 m needed).
- Door glass: built BLEND (envelope). §3.11.9 makes lobby / pool-hall glass opaque-frit alpha-scissor. Should the entrance doors switch to alpha-scissor (stacking with the Glass Box BLEND layer from the F3 terrace)?
  - **Vance answer:** **Switch to alpha-scissor.** Project rule (§3.11.9, restated in Rev 2.8): **at most one BLEND layer in any line of sight.** BLEND is used only for (a) the F3 Glass Box envelope and roof and (b) the aquarium acrylic (§3.12.1). **All F1/F2 glass (doors, storefront, F2 ribbon, gallery window), court glass, the F3 ball guard and all nets are alpha-scissor** (dither + frit). Signage and screens are opaque emissive.
- Canopy reach: the canopy projects 2.6 m over the West Arrival terrace (+3.0..+3.16, fascia to ~+3.3), and the kerb, hedge and bollards reach z 1.82 m. Neither is in the spec. Check the terrace circulation and egress width (§5.3) in front of the doors.
  - **Vance answer:** **Accept the 2.6 m canopy** (it's overhead, at +3.0..+3.3). **Keep a 6 m clear egress zone in front of the 44 m door run:** no kerb or hedge inside it; bollards are OK at ≥ 1.5 m spacing. Hedges only at the run ends (Z < 17.5 and > 61.5). The terrace is 48 m deep, so §5.3 is unaffected.

## Façade bay (#75 tt_facade_bay / _half)
- Which faces/runs get tt_facade_bay (S/N/E, W outside the 42 m doors)? Closure bays at the corners (1.5 m on the W/E faces per §3.11.1) have no F1/F2 module. Is a 1.5 m bay needed?
  - **Vance answer:** **All S, N and E runs, and the W face outside the door run** (Z 1.5..17.5 and 61.5..77.5), except the entrance modules. **Corner closure bays (1.5 m on the W/E faces):** these sit in front of the plant shafts; use a **1.5 m opaque slate closure panel** (F1–F2 height, no glazing), a simple scaled variant, not a new module.
- The trunk stands 0.62 m proud of the glass on a 0.4 x 0.42 m pedestal (bay depth 1.66 m). Check the S/N aprons (1:12 over ~1 m at grade) and the Rim Promenade clear width.
  - **Vance answer:** **Accepted.** At the S face it reaches 0.12 m into the Rim Promenade every 8 m; the promenade keeps ≥ 9.38 m clear. On the N arm (11 m) there's no issue. Keep the pedestals out of door modules.
- F1 glazing at the bowling, axe and WC bands: should those bays be opaque (slate) rather than glass?
  - **Vance answer:** **Yes, opaque slate** for F1 bays at bowling (X 30..57 S), axe (X 77..102 S), WC blocks (R1-S, R1-NW, R1-NE) and stair cores on the façade (ARS/ARN). Also F2 opaque at WC R2-NW/NE and the climbing changing rooms. **Keep glass** at the climbing halls (the wall is a show piece from the promenade), food court, gym and arcade.

## Plinth skirt (candidates, not promoted)
- Where is the plinth actually exposed? Per §3.3 the W and E faces sit on raised terraces at +4.0 HD, so the building plinth is buried there and the S/N faces are at grade. The 4.0 m skirt therefore reads only on the terrace edges (West Arrival / East Plaza perimeters, the East Spine ramp sides) unless something else is meant. Please confirm the runs and the faces.
  - **Vance answer:** **Confirmed:** the skirt reads only on terrace and ramp edges: West Arrival terrace N and S edges (its W edge meets the Fore cap), East Plaza N/S/E edges, East Spine ramp sides and the corner-link outer edges. On the building, only the **N face shows a 0.2 m plinth** (one trimmed course); the S face is flush.
- p(Z) varies 0..4.0 m along the W/E faces. The skirt is built as 4 x 1.0 m courses for trimming. Is a stepped trim acceptable, or is a sloped top / custom per-bay height needed?
  - **Vance answer:** **Stepped trim by 1.0 m course is fine** (Vance proposal). No sloped top: the guard rail on top hides the steps.
- Stepped variants (V1/V2) project 1.6-1.85 m from the face line. Does that fit the plaza edge and the 1:12 aprons?
  - **Vance answer:** OK on the terrace and ramp edges (outside circulation). **Not on the aprons or the Rim Promenade side.**

## Terrace decks + ramps (candidates, not promoted)
- No guard/handrail rules in the spec. The kit assumes IBC 2021: 1.07 m guards with < 100 mm openings at every terrace edge and ramp side with a drop > 0.76 m; no handrails on the 1:20 East Spine (a walking surface); no handrail on the 1:12 aprons (rise < 0.15 m). Please confirm, or give the project rule.
  - **Vance answer:** **Confirmed as the project rule:** 1.07 m guards, < 100 mm openings, on every terrace edge and ramp side with a drop > 0.76 m. No handrails on the 1:20 East Spine ramp or the aprons. The East Spine ramp sides need guards from x 230 down to about x 295 (where the drop falls below 0.76 m); below that, a 0.15 m kerb.
- S/N aprons: §3.3 says the Rim Promenade (z -45) and N arm (z 45) are +5.1 HD while F1 is +4.0, yet the aprons are "1:12 over ~1 m" (only 0.083 m of rise). These don't reconcile (1.1 m at 1:12 needs ~13 m). Which way does the apron fall, and how big is the level change?
  - **Vance answer:** **Resolved: the +5.1 is the hull height at the promenade centreline, not a step to climb.** The hull itself is the walking surface and follows the curve (true spin gravity is normal to it). At the building faces: **S face (z −40): hull = +4.00 = F1, flush threshold, no apron ramp.** **N face (z 39): hull = +3.80, so the apron rises 0.20 m to F1 over 2.4 m at 1:12, falling away from the building** (drains out). The old '1:12 over ~1 m' wording is replaced in spec §3.3.
- Deck build-up: the deck tiles are 0.30 m deep (surface at +4.0, so the tiles sit at +3.70). Where the terrace edge is over the plinth skirt, the skirt top must be at +3.70, not +4.0 (trim 0.3 m off the top course, or a 3.7 m skirt variant). Also the spec says "deck on fill 1.4-4.0 m": confirm the retaining edge is the tt_plinth_skirt language.
  - **Vance answer:** **Use a 3.7 m skirt variant** (top course trimmed 0.3 m) wherever the deck edge sits over the skirt; the deck tile covers +3.70..+4.0. **Yes, the retaining edge uses the tt_plinth_skirt language.**
- The East Spine ramp: 12 m wide x 80 m at 1:20 = 20 x 4 m modules per half (mirrored halves). Do any intermediate landings or rest areas apply (not required at 1:20 under IBC)? What retains the sides of the ramp (fill + skirt, or open structure)?
  - **Vance answer:** **No intermediate landings** (not needed at 1:20; Jared wants decoration, not regulation). **Sides retained by fill + skirt** (stepped courses), the same as the terraces, with guards per the rule above. 20 × 4 m modules per half, mirrored ✓.
- The corner links (terrace to the loop arms, "+4.0..4.2, level") and the Fore Hub Station Walk steps + 1:12 switchback (§3.8) aren't covered by this kit yet. Do they need their own modules?
  - **Vance answer:** **Corner links reuse the terrace deck tiles + skirt** (no new module; +4.0..+4.2 is within the deck tolerance). **The Fore Hub Station Walk steps + 1:12 switchback need their own small kit later** (low priority, not blocking).

## Secondary entrances S/N/E (candidates, Rook 2026-11-05)
- Spec gives S/N at grade and E on the East Plaza terrace, and a ~10 m lift-lobby gap (X 66.5..76.5 / Station Walk x 126.5..136.5), but no F1 door count, clear width, canopy reach or wayfinding for the secondary doors. Candidates are an 8.0 m module (2 × 4 m façade columns) with 1 m façade fillers each side. Confirm width (8 vs 10 m), door count (2 double pairs built) and whether S/N share one asset mirrored on X.
  - **Vance answer:** **8.0 m module, 2 double pairs (4 leaves, 3.6 m clear)**, sitting between two 8 m façade columns: **S and N at X 68..76** (inside the X 66.5..76.5 lift-lobby gap; no fillers needed, the neighbouring bays are standard 4 m bays). **E at Z 33.5..41.5** on the X 140 face. **One asset, mirrored for S/N, rotated for E.** F1 door capacity is far beyond need (the W run alone is 44 m).
- Canopy projects ~2.2 m over the apron / terrace (shorter than the W main's 2.6 m). Check Rim Promenade / East Plaza clear width and egress in front of the doors.
  - **Vance answer:** **Accepted.** It's overhead; the Rim Promenade keeps 9.5 m clear underneath; East Plaza is 30 m deep. Keep 3 m in front of each door clear of furniture.
- Face glyph (S/N/E) is a parameter on the wayfinding blade. Prefer one GLB + face param, or three promoted assets?
  - **Vance answer:** **One GLB + face parameter** (S/N/E).
- E sits on tt_terrace_* at +3.70; S/N sit on tt_terrace_apron at grade. Is a level-adjusted skirt / threshold needed under E, or does the terrace deck already cover it?
  - **Vance answer:** **The terrace deck covers it:** the E threshold is flush at +4.0 (deck top), no extra skirt or threshold piece.
- F2 above the secondary doors is not modelled (module is F1 6.1 m only, matching #74). Confirm F2 treatment.
  - **Vance answer:** Use the standard **F2 façade** (slate + 2.4 m ribbon) with a **1.2 m illuminated sign band at the F2 sill** carrying the S/N/E glyph. Same rule for the W door run (gallery treatment above).

## Foyer ticketing + lobby desk (candidates, Rook 2026-11-06)
- Spec places ticketing in the W foyer (X −12..0, Z 10..69) under the F2 gallery but does not give desk length, station count, accessible bay rules, queue layout or kiosk count. Candidates use an 8.0 m desk (tileable) with a centred 1.0 m accessible bay (top 0.86 m, knee clear), standard top 1.05 m, freestanding kiosks, 1.2 m-centre stanchions (≈1.12 m aisle) and a 4 m backdrop wall. Confirm lengths, counts and placement relative to the 42 m doors and ST-AQS/AQN.
  - **Vance answer:** **Two 8 m desks (16 m total), backs to the X 0 wall, flanking the lobby corridor mouth: Z 22..30 and Z 49..57**, desk front at X −2.5. Each desk = 1 centred 1.0 m accessible bay (top 0.86 m) + 4 standard stations (top 1.05 m) = **10 stations total**. **Queues:** 3-lane serpentine at 1.2 m centres in X −6..−2.5 in front of each desk. **Kiosks: 8**, in two clusters of 4 at X −8.5 (Z 24..28.5 and 50.5..55). The 4 m backdrop wall sits behind each desk on X 0. **Foyer clear passage X −12..−6 (6 m) is kept the full length**, and the 6 m door egress zone stays clear. ST-AQS / AQN (X −6..0, Z 10..20.6 / 58.4..69) are clear of both desks.
- Guest face is modelled +Z (place with yaw so +Z faces the W doors). Confirm orientation vs the foyer long axis (Z).
  - **Vance answer:** **Yaw so +Z faces −X** (toward the W doors); the desk's long axis runs along the foyer's long axis Z.
- Staff screens / ticket pads are props on the desk; are live ticket printers / RFID readers a Gage scripting concern or baked mesh only?
  - **Vance answer:** **Baked mesh only for now.** Any live printer or RFID behaviour is a later Gage scripting item, not part of this kit.
- Backdrop screen band is BLEND cyan glass-like. Should foyer digital signage be opaque-frit alpha-scissor per §3.11.9?
  - **Vance answer:** **Opaque emissive** (no transparency at all), per the Rev 2.8 rule. The same applies to all foyer digital signage.
