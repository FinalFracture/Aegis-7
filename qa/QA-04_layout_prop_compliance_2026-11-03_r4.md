# QA-04 r4: floating-prop retest (2026-11-03, 06:10 CST)
HEAD tested: **cbfb7db** (main at clone time; main is cbfb7db at commit). Gage's claim (cbfb7db): M-64/65/66/72 snapped to their floors with a gap of 0.000; M-71 outline at +0.003. Report only; no game files edited.
**Method:**
- Headless Godot 4.7 ran `preface_playable_area.tscn --qa-placement` from a scratch copy outside the repo (deleted afterwards).
- For each prop I took the world AABB of **every MeshInstance3D**. I raycast down from 0.05 m above each mesh's bottom at its centre and 4 inset corners, ignoring the prop's own colliders, and logged the gap to the surface hit to 0.1 mm.
- Overlaps: a physics shape query with the prop AABB shrunk by 2 mm and raised 4 mm, plus AABB intersection against every other prop.
- Screenshots: windowed run under xvfb (GLES3), in `/workspace/qa04-shots/` (not committed).
- Pass limit: lowest mesh bottom within 0.005 m of the floor below.

## Results
| Bug / LAY | Prop | Pose (r3 → r4) | AABB bottom / floor below | Gap | Result |
|---|---|---|---|---|---|
| M-64 / LAY-21 | Lost_And_Found_Rail_Bins (16 meshes) | (1.40, 0.12→**-0.27**, 5.35) yaw 90 → same X/Z/yaw; AABB XZ 1.248..1.548 × 4.70..6.00 unchanged | 0.1200 / 0.1200 (ExtGroundBody) | **0.0 mm** | **PASS** (floor contact) |
| M-65 / LAY-22 | Task_Lamp_201 (14 meshes) | (-13.2, 4.45→**4.235**, 5.6) yaw 180 → same | 4.2000 / 4.2000 (RevC_Shell_L2_col) | **0.0 mm** | **PASS** |
| M-66 / LAY-23 | Wardrobe_101 (17 meshes) | (-13.65, 0.12→**0.02**, 5.75) yaw 90 → same; AABB XZ -13.900..-13.412 × 4.40..7.10 unchanged | 0.1200 / 0.1200 (ExtGroundBody) | **0.0 mm** | **PASS** (see note) |
| M-72 / LAY-24 | Potted_Plants_Rail_Cradles_102 (11 meshes) | (10.65, 0.12→**-0.08**, 6.35) yaw 0 → same | 0.1200 / 0.1200 (ExtGroundBody) | **0.0 mm** | **PASS** (see note) |
| M-71 | Apt201_ExBench_DustOutline (1 quad) | (-12.05, 4.424→**4.203**, 7.65) | 4.2030 / 4.2000 (RevC_Shell_L2_col) | **+3.0 mm** | **PASS** (matches claim; decal offset ≤ 5 mm) |

Every corner ray matched the centre ray (flat floors). Overlaps with walls, colliders or other props: **none** for all four props; the outline only touches the floor collider it lies on. Gage changed only Y; X, Z, yaw and AABB XZ are identical to r3.

### Per-mesh bottoms (lowest touching parts in bold; gap above the floor)
- **Bins:** **Bins 0.0**, Wall_Plates 80.0, Rail_Bolts 95.0, Wall_Rail / Bin_Hooks 140.0, Bin_Latches 420.0, Bin_Lids 460.0, Board_Brackets 500.0, Board_Frame 560.0, Board_Lamp 566.0, Board_Panel 590.0, Cards 625–780, Pins 670.0 mm.
- **201 lamp:** **Slider_Body 0.0**, Slider_Hooks 5.0, Slider_Latch 23.0, Slider_Status 71.0, Mast_Socket 80.0, Joint_Latches 101.0, Mast 105.0, and the head/boom parts 390–461 mm.
- **101 wardrobe:** **Wall_Plate 0.0**, Uprights / End_Panels / Shelves_1-3 **50.0**, Brackets 150.0, Hook_Clamps 180.0, Wall_Rail 200.0, Straps 220.0, Buckles 228.0, Bracket_Bolts 488.0, Hanging bars 1,720, Retainer bars 1,800, Accent strip 1,970 mm.
- **102 plants:** **Cradles 0.0**, **Cradle_Latches 0.0**, Hook/Pots 30.0, Wall_Plates 40.0, Rail_Bolts 60.0, Wall_Rail 80.0, Pot_Latches 160.0, Grow lids / Foliage 190.0, Stems 200.0 mm.

### Notes (observations, not failed this round)
- **LAY-21 bins:** the bins now stand on the floor. The wall rail and notice board are still 0.648 m out from the Maintenance W wall (x 0.6) with nothing behind them. In the screenshot the board reads as a free-standing panel on brackets. This is a wall-mounted kit placed off the wall.
- **LAY-23 wardrobe:** only the 2.5 m wall plate touches the floor. The carcass (uprights, end panels, bottom shelves) hangs **50 mm** above the floor. This reads as wall-hung against the west wall at x -13.9, but if it's meant to be floor-standing, the carcass still floats by 50 mm.
- **LAY-24 plants:** the cradles touch the floor, but the wall rail (+80 mm) has no wall behind it (back face z 6.474, mid-room). It reads as a floor planter rack.

## GEO notes (observed only, not scored)
- **GEO-16 (unchanged):** planters Ext_25_hydro_planter_tiered_exterior_1006 (x -16.80..-16.39, z -7..-3) and _1007 (z 3..7), plus Ext_49 dead foliage 1004 (z -2..2), have their bottom at **0.1715**. The ground below is at **0.1200**, so all three float **+51.5 mm**.
  - Paving Ext_44_ext_paving_promenade_556 (x -17.00..-15.00, z -8.50..-6.50) and _602 (z 1.50..3.50) span y 0.1200..0.1786 and sit at 0.0 mm on the ground.
  - Planter AABB overlap: 1006 × 556 and 1007 × 602 each **0.406 × 0.007 × 0.497 m**. The planter base sits 7.1 mm inside the paving top, so on the paving footprint it's buried 7 mm; off it, it floats 51.5 mm. 1004 × 602 overlaps the same way.
- **GEO-14 (my method differs from QA-02's, so counts differ):** I cast a centre ray from each Ext_ root's AABB top, ignoring its own colliders, and counted mesh bottoms more than 5 mm below the first surface hit.
  - **52 walk-surface pieces are sunk:** 42 canal_edge (Ext_46) at -56.8 mm; 9 paving_promenade (Ext_44) from -133.7 to **-350.1 mm** (deepest: _367.._369, _372); 1 kerb_ramp (Ext_45_953) at -51.3 mm.
  - There are also 4 non-walk hits: maglev guideway Ext_17_12/14 at -597 mm and magnet modules Ext_19_19/20 at -434 mm.
  - So 56 hits in total, with walk-surface depths ranging -51.3 to -350.1 mm. QA-02's count of 69 included curbs (-6 / -15 mm) that a centre ray doesn't catch, so I can't confirm 69 with this method.
  - The worst paving depth (-350 mm) is deeper than QA-02's -250 mm. Worth a check on the z -8.9 band after GEO-17's collider clip.

## Screenshots (not committed)
`/workspace/qa04-shots/r4_Lost_And_Found_Rail_Bins.png`, `r4_Task_Lamp_201.png`, `r4_Wardrobe_101.png`, `r4_Potted_Plants_Rail_Cradles_102.png`, `r4_Apt201_ExBench_DustOutline.png`

## LAY status after r4
Closed: LAY-21, 22, 23, 24 (floor contact verified; the notes above are follow-ups). Unchanged from r3: Medium LAY-06, 07, 18; Low LAY-11, 19, 20, 25; Deferred LAY-03, 04, 09, 10.
Open counts: Critical 0 · High 0 · Medium 3 · Low 4.
