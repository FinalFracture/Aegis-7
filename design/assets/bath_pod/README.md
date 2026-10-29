# Bath pod (#8): 5 iterations
Generator: `assets/src/bath_pod_generator.py`. It reuses the swivel chair's loft, 30° normal split, glb writer and soft rasterizer.

**Size and placement:** each pod fits a 2.2 × 2.2 × 2.4 m envelope. Iter_01, iter_04 and iter_05 have one external element that goes past it (see below). The pivot is bottom-center, the doorway faces +Z and Y is up.

**Doorway:** 0.9 m wide × 2.02 m clear above a 0.06 m raised floor, with a gunmetal frame and an emitter strip for a force-field door.

**Sprocket service:** every pod has a ServiceHatch with an amber coupler port centred at 0.45 m on an outside face.

**Spin direction:** spinward is -X. Drains are spiral-ribbed rings offset toward spinward.

**Glass:** shower screens are alpha BLEND in the glb but hidden in the sheet renders.

**Clearance check (`check()`, 2 cm grid):** this checks three things:
- The doorway is at least 0.8 × 2.0 m.
- Each fixture has 0.7 m of clear floor in front of it.
- A 0.4 m-radius player capsule can walk from outside the door to each fixture's clear zone and into the shower tray.

**All five iterations pass.**

## iter_01: Monocoque Capsule (2,600 tris)
A single moulded white-composite shell with 0.55 m rounded corners, a domed roof and a violet seam band. It has a corner shower with a curved tray and a short screen, a vacuum-assist WC on the back wall, and a wall-hung sink and mirror on the right. The grey and black water recycler cassette hangs outside on the +X face (+0.2 m), behind Sprocket's hatch. It is the most "product-like" prefab: one mould, few seams, and easy to keep watertight.

## iter_02: Folded-Panel Cube + Utility Spine (2,256 tris)
Folded brushed-alloy panels with gunmetal seam ribs and a gunmetal roof. A full-height utility spine on the back wall carries the plumbing and the recycler cassettes, with the WC and sink on either side. The shower sits in the front-right corner with a splash fin, and its drain is offset spinward. The door is off-center, and the hatch is on the -X side. It is cheap to make in-cylinder from flat sheet, and every service runs in one replaceable spine.

## iter_03: Wet-Room, Central Drain + Misting Ring (2,528 tris)
An octagonal white shell whose whole floor is the shower. The floor slopes to a spiral drain set 0.12 m spinward of the centre, under a ceiling misting ring with violet nozzles. The WC and sink face each other on the side walls, and a low recycler sits on the back wall with the hatch outside it on -Z. Low-flow mist suits spin gravity and Coriolis, because there is no tall falling column of water. The open plan gives the most clearance of any iteration.

## iter_04: Split-Plan, External Sink (2,208 tris)
The vanity (sink, mirror and gunmetal niche) is outside on the front face, next to the door, so the unit can share it while the pod is in use. The front goes to about 1.56 m in z, so the depth with the sink is about 2.66 m. Inside are the WC, a back-right shower and a low recycler cabinet in the front-right corner. The hatch is on +X. It is the best fit for small units (101/102), where the hallway doubles as the dressing area.

## iter_05: Stacked-Utility, Roof Recycler (2,144 tris)
A low brushed-alloy pod (2.12 m walls) with the recycler stacked on the roof, inside the 2.4 m envelope. A gunmetal utility chase and down-pipe on the -X face lead down to Sprocket's hatch. The WC and sink are on the -X wall, the shower runs along the back, and a green door emitter marks the variant. This keeps the whole floor for fixtures, and the roof unit can be lifted out without entering the pod.

**Recommendation:** iter_02 (Folded-Panel + Utility Spine). It is the simplest to fabricate in-cylinder, all services sit in one spine, and it leaves good clearances; the wet-room misting from iter_03 could be added as an option.

## Final: Monocoque Capsule (3,388 tris)
This is the polished iter_01, built with `python3 assets/src/bath_pod_generator.py final`. It is exported to `godot/assets/models/bath_pod_capsule.glb` (the only final glb), and the sheet is `final_capsule_sheet.png`.

**Footprint:** exactly 2.2 × 2.2 × 2.4 m (bounds ±1.10 / 0–2.40). The recycler cassette now sits in a full-height bay that fills a gap in the shell's +X wall, flush with the outside. On its face it has a gunmetal exterior hatch, an amber Sprocket port at 0.45 m and a green status light. The door frame is recessed into the opening.

**Shell and fillets:**
- The moulded composite shell has 0.55 m rounded corners and a domed roof, with smooth normals and hard edges above 30°.
- The violet emissive band is inset into the wall, not stuck onto it.
- A cove fillet runs where the shell meets the floor.
- The door frame and fixture bases are filleted, with a violet emitter strip in the door head.

**Fixtures and floor:**
- Ceramic-white tray, WC and sink, with alloy taps and shower head.
- Gunmetal floor with a slot drain grate offset spinward (-X).
- Open shower, no glass screen or frame. A subtle 18 mm rounded ceramic floor lip rings the near-flush tray to hold water (a step-over for the player).

**Checks:**
- Doorway is 0.9 × 2.02 m.
- Shower, WC and sink each have a clear 0.7 m zone.
- The 0.4 m player capsule can reach all of them.
- All parts are closed meshes.
