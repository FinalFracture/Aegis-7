# #47 Desire-path wear decal — 5 candidates (Rook, Oct 31 2026)
Generator: `assets/src/ext_desire_path_decal_generator.py`. Segment 1.2 x 4.0 m (X x Z), tiles seamlessly along Z (local +Z = walking direction); chain/rotate segments along the platform -> exit-ramp diagonal across the plaza. Alpha BLEND quads, UV-mapped, procedural textures in Aegis palette (gunmetal/slate/titanium/amber), wordless, no wood. Sloane may swap in final textures on the same quads.
**Placement:** y = 0.053 (paving top 0.05 + 3 mm). Multi-layer candidates stack layers 1.5 mm apart (top layer max y 0.056).

| # | Name | Tris | Justification |
|---|---|---|---|
| 01 | Soft Scuff | 12 | Single wide soft-edged gunmetal darkening; quietest read, most realistic polished-composite wear. |
| 02 | Polished Line | 24 | Titanium burnish core over slate: wear reads as shine, not dirt — fits a clean Aegis hab. |
| 03 | Footfall Trail | 24 | Faint base + paired footfall prints; reads "people walk here" at gameplay distance. |
| 04 | Scuff Streaks | 24 | Darkening + titanium cross-grain scuff streaks; catches the low amber pole light. |
| 05 | Worn Tactile | 36 | Darkening + titanium core + amber flecks of abraded paving-04 tactile inlay; ties to the promoted paving. |

Checks (`ext_desire_path_decal_report.json`): all PASS — pivot bottom-centre (0,0,0), <6000 tris, layer gap 1.5 mm (>1 mm, no coplanar z-fight), paving offset 3 mm (within 2-5 mm, floor contact ±5 mm), normals +Y, UV + BLEND on every layer. Sub-part overlap N/A (flat decal quads, intentionally open single-sided meshes).

## WINNER: 05 Worn Tactile (Jared, Oct 31 2026, via Atlas)
- Promoted -> `godot/assets/models/ext_desire_path_decal.glb` (36 tris, 3 alpha-BLEND layers).
- Placement: y 0.053 (paving 0.05 + 3 mm); 1.2 x 4.0 m segment, tile along local Z at 4.0 m pitch; yaw to follow the platform -> exit-ramp diagonal.
