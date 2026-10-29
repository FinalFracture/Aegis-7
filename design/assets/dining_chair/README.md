# Dining chair / stool (#13) — 5 iterations
Generator: `assets/src/dining_chair_generator.py`. Envelope about 0.45 × 0.45 × 0.9 m, seat about 0.45–0.47 m. Pivot is bottom-center, front faces +Z, Y is up, UVs are box-projected. Sheets show Top, Front, Side and Iso views.

## iter_01: Folded Sheet-Alloy Stacker (292 tris)
Two chamfered side panels, each folded from a single sheet of alloy, form the front and rear legs. Each panel has a lightening cutout. A pressed seat pan with a thin pad sits between them, and the back posts carry a slightly raked backrest. A thin violet inset band on the back matches the Bulkhead Hub bands. Stacking lugs on the top rail let the chairs nest and lock vertically, so they stay put during spin-down. Every part is flat-pattern sheet, which suits in-cylinder press and brake fabrication and allows riveted repairs.

## iter_02: Mag-Anchor Drum Stool (900 tris)
A banded alloy drum stands on a weighted base disc that has an amber magnetic anchor ring. The ring clamps the stool to deck plating in low-g or spin-down zones. There is a padded round seat, a foot ring at 0.24 m, and a short post-mounted backrest. The drum is a rolled tube with clamp bands, so there are few parts and it is easy to strip down. Its compact footprint suits tight galley tables.

## iter_03: Cantilever Tube Chair (408 tris)
A continuous bent-tube frame runs from the floor runners up to a cantilevered seat. It has a rear crossbar and rubber foot pads. The flex gives some comfort under spin gravity, and the open frame is light enough to hang on wall rails when a room is cleared. The upholstered seat and back panels have a dark edge band and a grip slot. Tube stock can be bent from recycled alloy in-cylinder.

## iter_04: Printed Lattice Chair (452 tris)
This is a ceramic-polymer chair printed in-cylinder by additive manufacturing. It has splayed legs, X-lattice side bracing and a ribbed lattice backrest, with a thin seat pad. All the material sits on load paths, which keeps mass low, and broken members can be reprinted locally. A small violet print-batch tag on the seat front is the only accent. Its warmer, softer look suits the lived-in residential feel.

## iter_05: Floor-Clamped Swivel (748 tris)
A swivel seat sits on an alloy column, and the column is bolted to a chamfered floor clamp plate. An amber light on the plate shows when the lock is engaged. It has a spoked foot ring, a padded seat on a metal shell, a single-spine backrest and a violet back inset. Because it is fixed, it suits shared mess areas and stays secure during spin-down. The seat lifts off the swivel hub for service.

## Final: Floor-Clamped Swivel (1,480 tris)
This is the refined iter_05, built with `python3 assets/src/dining_chair_generator.py final` (`swivel_final()`). It is exported to `godot/assets/models/dining_chair_swivel.glb` and `final_swivel.glb`, and the sheet is `final_swivel_sheet.png`.
- **Parts:** It has 10 named parts: FloorPlate, Column, SwivelHub, FootRing, Seat_Cushion, Seat_Pan, BackSpine, Back_Panel, LockLight and AccentInset. Each part is a closed, watertight mesh.
- **Geometry:** Round parts are lofted (a 20-segment column with a flared foot and collar, and a 24×6 torus foot ring). Four spokes run from the column surface to the ring.
- **Edges:** The octagonal floor plate is chamfered. The seat pan, back panel and spine are beveled. The cushion has a rounded, padded crown.
- **Back mounting:** The spine has an L-bracket and a gusset under the seat pan.
- **Normals:** Normals are split at a 30° auto-smooth angle and written explicitly to the glb.
- **Materials:** Brushed alloy (metallic 0.9, roughness 0.35), gunmetal for the plate and hub, slate fabric (roughness 0.85), an amber #FFA53A lock light and a violet inset.
