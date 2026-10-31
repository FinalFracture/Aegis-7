# #50 Litter / spill drift (Coriolis, antispinward) — 5 candidates (Rook, Oct 31 2026)
Spec (asset list row 50; plan "Coriolis tell"): litter and spills drift antispinward (-Z) along the Spin Streets (now walkways).
Generator: `assets/src/ext_litter_drift_generator.py`. Patch ~1.0-1.2 x 2.7-3.0 m. Pivot bottom-centre (0,0,0); local +Z = spinward: streak heads/sources at +Z, tails and litter density toward -Z.
**Placement:** y 0.05 (paving top), yaw 0 so local -Z = world -Z antispinward (do NOT rotate 180°). Litter rests at local y 0; spill decals at local y 0.003 (+0.0015 per layer) -> world 0.053 / 0.0545.
Solid litter: watertight lying cans/cups, crumpled wrappers, flat packets, ration pouches (titanium, cyan, civic pearl, amber, slate, gunmetal; no wood, no print).

| # | Name | Tris | Justification |
|---|---|---|---|
| 01 | Gutter Drift | 420 | 14 litter pieces only, bunched toward -Z as if piled downstream; clearest read, no decals. |
| 02 | Spill Comet | 194 | One big gunmetal spill streak, cup at the +Z head, tail smearing -Z; single strong tell. |
| 03 | Drip Trail | 268 | Dotted amber drip line from a dropped can + a slate smear + wrappers; reads at walking distance. |
| 04 | Layered Smear | 136 | Faded slate smear under a fresh gunmetal streak (1.5 mm above); repeated spills, all bending -Z. |
| 05 | Cyan Coolant | 230 | Civic-cyan coolant spill + titanium cans; Aegis-coloured mess that still says "drift". |

Checks (`ext_litter_drift_report.json`): all PASS on 3 seeds of ext_clip_check (0 overlaps, 0 coplanar, 0 open), floor contact 0.000 for every piece (±0.005), 0 litter-litter AABB intersections (≥2 cm gaps), 0 litter on decals, decal offsets 3/4.5 mm, pivot (0,0,0), UV + BLEND decals, <6000 tris.
Fix during build: 03 had two decals on the same layer (non-overlapping, but tightened) -> second moved to layer 1 (+1.5 mm).

## APPROVED: all 5 as a variant set (Jared, Oct 31 2026, via Atlas)
- Promoted -> `godot/assets/models/ext_litter_drift_01..05.glb`; pick the variant by what spilled.
- Placement: y 0.05, rotation 0 (drift toward -Z, antispinward). Atlas PM call: 3 patches on the Spin St walkways at X ±17.4.

## Layout — Atlas PM call (not a Jared vote), Oct 31: 3 patches per Spin Street, 6 total, mixed variants, no repeat on a street
Proposed by Rook (positions are a proposal for Gage/Atlas; all y 0.05, rot 0, drift -Z). Patches are ≤1.2 x 3.0 m; spacing is tighter toward -Z (heavier drift at the promenade end).
| Street | Variant | Centre X | Centre Z | Z span | Clearance |
|---|---|---|---|---|---|
| Spin St W | ext_litter_drift_01 | -17.4 | -7.0 | -8.5..-5.5 | 0.8 m north of bollards (Z -9.3) |
| Spin St W | ext_litter_drift_03 | -17.4 | -3.5 | -4.85..-2.15 | |
| Spin St W | ext_litter_drift_05 | -17.4 | +2.0 | +0.6..+3.4 | |
| Spin St E | ext_litter_drift_02 | +17.4 | -7.0 | -8.4..-5.6 | 0.8 m N of bollards; nook (Z ≤ -9.6) is south of the bollards, ≥2.1 m clear |
| Spin St E | ext_litter_drift_04 | +17.4 | -3.5 | -4.95..-2.05 | |
| Spin St E | ext_litter_drift_03 | +17.4 | +2.0 | +0.65..+3.35 | |
Note: X ±17.4 is Atlas's value. Spin St E bollards span X 17.9..22.1, so the street centreline may be nearer X ±20 — TBD for Gage to confirm X so patches sit on the walkway, not across a kerb/curb.
