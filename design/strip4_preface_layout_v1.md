# Strip 4 Preface Area (B1) Layout v1 (Vance, 2026-11-01)

Jared approved this (via Atlas): update the preface layout and add the props, leaving the canal out for now. Sources: `strip4_plan.md` §3/§4 (v2.2), `residential_exterior_plan_v1.md` v1.3, `residential_apartment_layout_v2.md` Rev C.2/C.2a, `prop43_relocation.md` rev3, `godot/scripts/preface_playable_area.gd`, and trimesh measurements of `godot/assets/models/preface_residential_sector.glb` and the prop GLBs. No renders and no code in this commit.

## 1. Site: B1 Preface block (strip x 50..150, z 6..62.8)
Local-to-strip transform (strip4_plan §3): **x = 100 + X, z = 36.0 − Z** (y unchanged; deck at the R 200 floor). See open question L1: as written, this is a mirror, not a rotation.

| Element | Local (X, Z) | Strip 4 (x, z) | Status |
|---|---|---|---|
| Preface building P-1 (28 × 18, 2 storeys) | −14..14, −9..9 | x 86..114, z 27..45 | existing |
| Service walkway (Sprocket and carts, 4 m) | Z 11.8..15.8 | x 50..150, z 20.2..24.2 | per plan |
| Sector-4 exit (main door) | X 0, Z −9 | (100, 45) | opens onto the plaza |
| Sector-4 plaza and promenade | Z −9..−18.3 | x 82..118, z 45..54.3 | Plaza runs to z 54.3 while the canal is deferred |
| Canal (2.5 m water + coping) | — | z 51.4..54.3 | **DEFERRED** (Jared). Keep the strip free; paving is temporary |
| Memorial nook (monument rotated 180°, faces +z) | 17.4..21.6, −12.7..−9.6 | x 117.4..121.6, z 45.6..48.7 | see conflict C1 |
| Spin Walk W / E (6 m, planter islands) | — | x 77..83 / x 117..123, z 6..62.8 | per plan |
| West access tower (7 × 5) | — | x 85..92, z 54.3..59.3 | per plan |
| East access tower (7 × 5) | — | x 107..114, z 54.3..59.3 | per plan |
| x 100 S4\|5 platform (deck +5.40) | — | x 85..115, z 57.93..61.43 | cantilevered off the rib |
| Forecourt walk (2.0 m) | — | x 50..150, z 59.3..61.3 | links the towers |
| x 100 cross-walk (6 m) | — | x 97..103 | P-1 exemption; detours via Spin Walk W/E (plan §7 fix) |
| Rest of block | — | x 50..77 and 123..150 | open green/paving for now (Vance proposal). No new buildings |

Walk lanes: the main door goes onto the plaza, then straight +z to the forecourt between the towers (x 92..107, 15 m wide). The towers take you up to the platform. Spin Walk W/E carry the axial flow, and the service walkway covers the back (−Z face). All lanes are 2 m or wider, and building interiors keep 0.9 m paths.

Note: Atlas asked for "x 50–100", but P-1 is centred at x 100 (86..114) and the memorial is at x 117–122, so the layout covers the whole B1 block, x 50..150.

## 2. Interior props: the 13 Rev C.2 props (sector-local frame of preface_playable_area.gd)
**Important:** `preface_residential_sector.glb` has **not been rebuilt to the Rev C grid**. It still has the old atrium/mezzanine with Room 1A (East Lounge, x −12.10..−4.90), Room 1B (West Storage, x 0.90..8.10), the laundry segment on the hall north wall (z 8.76), Tech_Apartment_Upper (201) and Room_2B suite (202). Apartments **103/104/203/204 do not exist** in the GLB. Props for those rooms get **provisional** spots below (Vance proposal) and move at the rebuild.

Mapping note: the Rev C doc X numbers are offset from the sector coords on the laundry wall. For example, #38 is doc X −2.6..0.4 and code −3.35..−0.35, so code = doc − 0.75. Elsewhere the Rev C grid has no counterpart yet. Use the sector coords below.

Yaw: local +Z is the front. yaw 180 has its back to the +z (north) wall; −90 has its back to a +x wall and faces −x; +90 has its back to a −x wall and faces +x. y is the pivot (L1 floor 0.235, L2 floor 4.415). The VOTE_LOG has no entries for these interior props (they were approved in the Rev C.2 doc, 519cc5d + 759f4c8). The 13 are the brief's list: 9 Rev C.2 props + 4 wired (#38, #39, #42, #43).

Clearance method: each prop's footprint, plus a 1.2 m front zone (floor +0.05..1.8 m), was tested against every triangle AABB in the sector GLB, the existing props, pickups (spools, batteries), door zones (portal width × 1.2 m inside), the Rostov/probe spots and each other. **Every spot below returned 0 hits.**

| # | Prop | GLB | Room | Position (x, y, z) | Yaw | Mount | Footprint (x × z, world) | Verified clearance |
|---|---|---|---|---|---|---|---|---|
| 1 | Prop38 folding counter 3.0 | folding_counter_fold_leaf_3p0.glb | Laundry seg., hall N wall | (−1.85, 0.235, 8.45) | 180 | wall | −3.35..−0.35 × 8.15..8.76 | wired; 0.15 m gap to #39, clear of the pillar at −0.28 |
| 2 | Prop39 flip seat | laundry_bench_wall_flip_seat.glb | Laundry seg., hall N wall | (−4.10, 0.235, 8.55) | 180 | wall | −4.70..−3.50 × 8.35..8.75 | wired |
| 3 | Prop42 substation | substation_wall_ladder_busway.glb | Hall N wall (east) | (10.68, 0.235, 8.35) | 180 | wall | 9.43..11.93 × 7.95..8.75 | wired |
| 4 | Prop43 spares dispenser (rev3) | spares_gravity_dispenser.glb | 1A East Lounge, +x wall | (−5.16, 0.235, 5.20) | −90 | wall | −5.41..−4.91 × 4.25..6.15 | front zone to x −6.61 clear. **Not applied yet**: code still has (−8.00, 0.235, 8.50) yaw 180 (8855f8c), which fails the front zone |
| 5 | Suit storage service combo (102 "suit missing from hook") | suit_storage_service_combo.glb | 1B West Storage, +x wall | (7.82, 0.235, 4.85) | −90 | floor, wall-backed | 7.57..8.07 × 3.60..6.10 | 0 hits; front zone x 6.37..7.57; clear of battery (7.2, 7.1), probe (5.6, 6.0) and door 1B |
| 6 | Lost-and-found rail bins #55 | lost_and_found_rail_bins.glb | 1B West Storage, −x wall | (1.08, 0.235, 5.35) | 90 | wall (bins y 0.62..1.64) | 0.93..1.23 × 4.70..6.00 | 0 hits. **Moved off the laundry wall** (C.2a wanted X −4.3..−3.0, now Prop39); 1B is the next room east |
| 7 | Tea set rail caddy | tea_set_rail_caddy.glb | 1B West Storage, N wall | (1.50, 0.235, 7.89) | 180 | floor (see Q P2) | 1.31..1.69 × 7.79..7.99 | 0 hits; front zone z 6.59..7.79 |
| 8 | Clutter kit magnet dock | clutter_kit_magnet_dock.glb | 202 suite, −x wall | (5.69, 4.415, 5.025) | 90 | wall-base | 5.57..5.81 × 4.545..5.755 | 0 hits; GLB pivot off-centre (local x −0.73..0.48) is accounted for |
| 9 | Dobsonian telescope pier (104) | telescope_pier_dobsonian.glb | **provisional** 202 suite, N wall | (7.00, 4.415, 8.12) | 180 | floor | 6.74..7.26 × 7.78..8.38 | 0 hits. 104 absent; move at rebuild |
| 10 | Lab crate frame 104 | lab_crate_frame_104.glb | **provisional** 202 suite, N wall (beside the telescope, as C.2 intends) | (8.40, 4.415, 8.09) | 180 | floor | 7.90..8.90 × 7.78..8.38 | 0 hits; 0.64 m from #9 |
| 11 | Cycler route lightbox (203 Aldrin Cycler model) | cycler_route_lightbox.glb | **provisional** 202 suite, +x wall | (13.36, 4.415, 7.00) | −90 | wall (0.12 deep) | 13.36..13.48 × 6.55..7.45 | 0 hits; clear of battery (10.70, 7.20). 203 absent |
| 12 | Lab crate frame 204 (lid ajar, emitter parts) | lab_crate_frame_204.glb | **provisional** 1A East Lounge, −x wall SW corner | (−11.72, 0.235, 3.60) | 90 | floor | −12.07..−11.36 × 3.15..4.05 | 0 hits; clear of door 1A (x −9.88..−7.12). 204 absent |
| 13 | Reading bench book cubbies (4.0 m) | reading_bench_book_cubbies.glb | **NO CLEAR SPOT** | — | — | floor | 4.0 × 0.4 | Every wall run in 1A/1B/201/202 was scanned; the longest clear run is about 3.1 m (202 N wall, x 6.55..9.65). Not forced. Options: (a) place at the Rev C rebuild; (b) Rook makes a 3.0 m variant for the 202 N wall (that would displace #9/#10); (c) outdoor on the plaza (exterior asset list) |

Paths, doors, egress: all front zones stay outside the door zones (1A, 1B, 201, 202 portals + 1.2 m) and outside the hall/corridor. Room widths after the zones: 1B keeps over 3.5 m clear between the ±x zones, and 202 keeps x 7.01..12.16 clear at z 4.5..6.5. The 0.9 m paths and the Sector-4 exit lane are untouched.

## 3. Conflicts / open questions
- **L1 (transform):** `x = 100 + X, z = 36 − Z` mirrors the building (det −1), so the asymmetric interiors would be handed. A 180° yaw would be `x = 100 − X, z = 36 − Z`, which moves the memorial to x 78.4..82.6 (inside Spin Walk W). Jared/Rook: mirror or rotate?
- **C1 (memorial vs Spin Walk E):** the memorial nook x 117.4..121.6 sits inside Spin Walk E (x 117..123). Vance proposal: keep the nook and narrow Spin Walk E to x 121.6..127.6 next to the plaza (z 45..54.3), or shift the walk +4.6 m for all of B1. Needs Jared's call.
- **C2 (P-1 cross-walk):** already handled by the plan's exemption and the Spin Walk detour. No new change.
- **C3 (rebuild):** 103/104/203/204 are missing from the GLB, so #9–#12 are provisional and #13 has no spot. Rev C rebuild timing: Gage/Atlas.
- **P1 (Prop43):** rev3 is not in the code yet. Gage to apply it.
- **P2 (caddy):** the tea set caddy is 0.2 m tall and probably belongs on a rail or table. Confirm its mount height with Rook; the floor spot is checked clear either way.
- **P3 (#55 notice board):** `ext_notice_board.glb` is an exterior asset. Not placed here.
- Canal: deferred. Q5 (length) is still open, and Q2 (preface axial slot) is on hold.

## Rev 1.1 (Jared via Atlas, 2026-11-01): supersedes L1, C1 and the cubby question
- **L1: rotate 180°, no mirror.** Local to strip: `x = 100 − X`, `z = 36 − Z` (yaw on strip = local yaw + 180°). Interiors keep their handedness. The building footprint is unchanged at x 86..114, z 27..45, and the main door stays at (100, 45) facing the plaza.
- **C1: the memorial moves; both Spin Walks stay put** (W x 77..83, E x 117..123). The rotated old nook (x 78.4..82.6) would sit inside Spin Walk W, so the new spot is on the plaza west of the door: **x 87.0..91.2, z 46.5..49.6** (4.2 × 3.1 m, the same nook size), with the monument facing +z toward the station forecourt. That leaves 4.0 m clear to Spin Walk W, 8.8 m to the door axis and 1.5 m to the building face, and it's clear of the station towers (z ≥ 54.3). Vance proposal on the facing; the bench sits on its south side as in v1.3.
- **Cubbies (#13):** these wait for the Rev C rebuild.
- The interior prop table (sector-local) is unchanged.
