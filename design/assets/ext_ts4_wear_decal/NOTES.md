# #49 TS-4 wear decal set — 5 candidates (Rook, Oct 31 2026)
Spec (asset list row 49): patch tape + mismatched liner decals + dead-foliage material swap for one west-sidewalk TS-4 (plan: "hydro beds patched with amber tape and mismatched liners; one west planter is dead").
Generator: `assets/src/ext_ts4_wear_decal_generator.py` (sheet: `ext_ts4_wear_decal_sheet.py`).
Each candidate = `ext_ts4_wear_decal_NN.glb` (overlay quads) + `ext_ts4_dead_foliage_NN.glb` (TS-4 copy, Foliage/Foliage_Light swapped to a DeadFoliage material).
**Placement:** overlay shares the TS-4 pivot — give it the same transform as the planter it dresses. Quads face +Z, 3 mm in front of the riser faces (z 0.200/0.059/-0.061); tape layer sits +1.5 mm over liners. Zones avoid latches (x 0, ±1.5) and lids. Alpha BLEND, UV-mapped, wordless, Aegis palette (amber tape, slate/gunmetal/civic-pearl liners, titanium rivets).

| # | Name | Tris | Justification |
|---|---|---|---|
| 01 | Amber Field Patch | 6 | Two amber tape strips + one slate liner; minimum story, strongest amber read. |
| 02 | Mismatched Pearl | 8 | Civic-pearl spare liners (wrong shade) taped at seams; "mismatched" reads literally. |
| 03 | Riveted Repair | 6 | Gunmetal bolted plates with titanium rivets + lip tape; engineered make-do. |
| 04 | Layered Bodge | 14 | Liner over liner over tape on all tiers; heaviest neglect. |
| 05 | Single Scar | 4 | One long tape seal + one small liner; subtle, lets dead foliage carry the beat. |

Checks (`ext_ts4_wear_decal_report.json`, tested against the promoted TS-4): all PASS — min clearance to any TS-4 part 3 mm (in 2-5 mm), 0 decal points inside any closed part, overlapping decals ≥1.5 mm apart (0 coplanar), <6000 tris, UV + BLEND. Sub-part overlap/cut-out N/A (open single-sided quads by design). Dead-foliage variants reuse TS-4 geometry unchanged (material-only swap).

## WINNER: 02 Mismatched Pearl (Jared, Oct 31 2026, via Atlas)
- Promoted -> `godot/assets/models/ext_ts4_wear_decal.glb` (8 tris) + `godot/assets/models/ext_ts4_dead_foliage.glb`.
- Placement: the decal overlay shares the TS-4 pivot — use the identical transform of the TS-4 it dresses. `ext_ts4_dead_foliage.glb` REPLACES (not overlays) the one dead west-sidewalk TS-4 (row 25: back to Spin St W kerb, X -16.8..-16.39, one of z0 -7 / -2 / 3; which instance is a layout call).
- **Atlas PM call (not a Jared vote), Oct 31:** the dead TS-4 is the middle west-sidewalk spot, X -16.6, Z -2.
