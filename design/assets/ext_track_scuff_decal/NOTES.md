# #51 Maglev track & scuff decals — 5 candidates (Rook, Oct 31 2026)
Spec (asset list row 51, maglev rewording): guideway dust + stator wear streaks, platform-edge foot scuffs, kerb scuffs at the stop. Sprocket's wheel-track decals (apron X 1..5.6, Z 9..11.65, + service door jamb) are KEPT, untouched — no Sprocket decal files exist in the repo yet (they're a Sloane texture item); this set only touches the guideway and stop kerbs on the -Z side, ~29 m away.
Generator: `assets/src/ext_track_scuff_decal_generator.py` (also draws the sheet).
Per candidate NN: `ext_track_scuff_guideway_NN.glb` + `ext_track_scuff_kerb_NN.glb` — overlays that share the host pivot.
**Placement:** guideway overlay = same transform as each `ext_maglev_guideway.glb` module (rot 0, origin Z -20.077, 10 m X pitch). Kerb overlay = same transform as each `ext_tram_platform_kerb.glb` (rot 180°, origin Z -17.55) at the stop. Surfaces: bed top y 0.040, flange top 0.160, deck top 0.294 (horizontal), kerb body front z 0.940 (vertical); decals 3 mm off (+1.5 mm per layer). Alpha BLEND, UV-mapped, wordless, Aegis palette.

| # | Name | Tris | Justification |
|---|---|---|---|
| 01 | Fine Dust | 6 | Light slate dust on the guideway bed + faint edge sole scuffs; most restrained. |
| 02 | Stator Burnish | 8 | Titanium burnish streaks on the flange where the magnets ride + dust + edge scuffs; reads maglev, not wheels. |
| 03 | Boarding Wear | 8 | Heavy foot scuffs at the boarding edge/deck + kerb-face scuffs + light dust; busy stop. |
| 04 | Amber Strike | 8 | Amber heat-tinted stator wear over a gunmetal film + kerb-face scuffs; ties to the amber accent. |
| 05 | Full Wear Set | 14 | All four beats layered; densest story. |

Checks (`ext_track_scuff_decal_report.json`, against the promoted guideway + kerb): all PASS — clearance to host 3 mm (2-5 mm), 0 decal points inside closed host parts, stacked layers 1.5 mm apart (0 coplanar), 0 overlap with the Sprocket apron/jamb zone (world-space test), UV + BLEND, <6000 tris. Sub-part overlap N/A (open single-sided quads). Avoided by design: tactile bars (z 0.40-0.68) and safety line (z 0.81-0.87) on the deck, Guide_Glow on the flange.

## WINNER: 03 Boarding Wear (Jared, Oct 31 2026, via Atlas)
- Promoted -> `godot/assets/models/ext_track_scuff_guideway.glb` + `godot/assets/models/ext_track_scuff_kerb.glb`.
- Transforms: guideway overlay = identical transform to every `ext_maglev_guideway.glb` module (rot 0, origin Z -20.077, y 0, 10 m X pitch). Kerb overlay = identical transform to every `ext_tram_platform_kerb.glb` at the stop (rot 180°, origin Z -17.55, y 0). Sprocket wheel-track decals untouched.
