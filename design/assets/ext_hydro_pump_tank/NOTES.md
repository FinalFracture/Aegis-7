
## ext_hydro_pump_tank_01b: reactive indicators (Rook, Jared's pick 01 at 1:26 PM CT; NOT promoted yet). Notes for Gage
Generator: assets/src/ext_hydro_pump_tank_01b_generator.py. 400 tris. 1.20 W × 0.82 D × 1.80 H m, pivot at bottom-centre. Clip check PASS at fill 0.05, 0.5 and 1.0.
Nodes (all at the scene root): Skid, Tank, Cabinet, Status, Pipes, Gauge_Frame (titanium), Gauge_Glass (BLEND), WaterLevel_Fill, Temp_Seg_01..Temp_Seg_06.
- **WaterLevel_Fill** (material a7_water_fill, cyan, slightly emissive). Node translation is (0, 0.251, 0), the cavity floor. The mesh runs from local y 0 to 0.698 (full).
  - Drive the level with `scale.y = level` (0..1). Keep the minimum around 0.003 rather than 0 to avoid a degenerate scale, or hide the node at 0.
  - Do not scale above 1.0: the cavity top is 0.949 m.
- **Temp_Seg_01..06** (material a7_amber, emissive #FF9500). Stacked on the cabinet front at x 0.26..0.33, y 0.30..0.88; 01 is at the bottom.
  - For a bar showing value v (0..1), light segments 1..ceil(v×6) and switch the rest off by setting `visible = false`. Alternatively, give each node its own material override with the emission off (the contact sheet uses slate for "off").
  - All six share one material, so use per-node `material_override` rather than editing the shared material.
