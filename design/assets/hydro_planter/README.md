# #33 Hydro planter: 5 iterations (window/balcony; rooms 103, 202; qty 2; 4.0 W × 0.4 D × 0.6 H)
Generator: `assets/src/hydro_planter_generator.py`. The pivot is bottom-centre, the front faces +Z, and the window/wall is at −Z.
- **Spin-down:** the reservoirs are sealed, the slate grow lids are latched with amber latches, and the plants sit in clipped net cups.
- **Foliage:** low-poly closed clusters in a matte leaf green (non-emissive). They are a placeholder until real plants are modelled.
- **In-cylinder manufacture:** moulded trough, extruded alloy channels.
- **Anchoring:** floor clamps, except option 2, which hangs on the wall rail.

| # | Name | Tris | W×H×D (m) | Description |
|---|------|------|-----------|-------------|
| 1 | Moulded_Trough | 1,792 | 4.00 × 0.54 × 0.40 | One moulded white trough on a gunmetal plinth, a latched slate lid, a violet level window, 12 plants |
| 2 | Rail_Cassettes | 2,176 | 4.00 × 0.41 × 0.37 (wall-hung) | Four 1 m cassettes hooked and latched on a wall rail, leaving the floor clear |
| 3 | Tiered_Steps | 3,472 | 4.00 × 0.64 × 0.40 | Three stepped troughs rising toward the window |
| 4 | NFT_Channels | 3,688 | 3.92 × 0.61 × 0.40 | Three alloy nutrient-film channels on gunmetal frames, with a sealed pump box and green status light |
| 5 | Sprocket_Service | 1,744 | 4.00 × 0.60 × 0.42 | 3.4 m trough with a latched front reservoir drawer, plus a gunmetal service tower with the Sprocket port at 0.45 m and a green dosing status light |

**Recommendation:** #5, Sprocket_Service. Sprocket can top up and dose the reservoir without any human, which fits the family theme, and it is the lowest tri count.
- Choose #2 for a balcony rail where the floor has to stay clear.
- Choose #3 for the most visible greenery.

## Final (Oct 29, 2026): Tiered Steps, EXTERIOR
Jared picked iter_03 Tiered Steps but moved it outdoors (hydro co-op beds / sidewalk planters on Vance's exterior plan); interior #33 is dropped from rooms 103/202.
- `godot/assets/models/hydro_planter_tiered_exterior.glb`: 2,784 tris, 4.0 W × 0.70 H × 0.41 D m, bottom-centre pivot, +Z front, closed meshes. Not placed.
- Curved floor: the tiers ride on a gunmetal base frame lifted 60 mm on six levelling feet. Each foot is a threaded alloy jack in a bolted gunmetal clamp shoe, giving ±25 mm of take-up so the troughs stay level over the floor's curvature (lay the 4 m length along the cylinder axis where possible).
- Spin-down: three latched slate grow lids (amber latches), plants in clipped net cups, sealed slate reservoir along the front.
- Sheet: `final_tiered_exterior_sheet.png`.
