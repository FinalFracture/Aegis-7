# QA-03 re-test: VIS-17 + Rev C stair models — 2026-11-02

Tester: QA-03 (visuals). Fresh clone of main at `2ecba00` (includes 2ecba00 and 5d8a9d9).
Method: Godot 4.7 on the box, Compatibility renderer (opengl3), Mesa software rendering under xvfb at 1280x720, from a copy outside the repo. A camera and a test SpotLight3D flashlight (range 18 m, 28°, energy 3, shadows on) were used. Each shot was taken with the flashlight off and on. Screenshots stay on the box only and are not committed. GLB materials were also read statically. No game code was edited.
Out of scope: dark interiors (intended, M-68), lighting look changes (on hold, M-69), and VIS-01 (deferred).

## VIS-17: PASS (closed)
- Repro: from (-8.5, 6.3, -2.0), look toward (-10.18, 5.71, -3.55).
- The solid-white panel is gone, with the flashlight off and on. The alcove reads as dark gunmetal and grating, and the flashlight shows no white or unlit surface there.
- No orphan references remain. The only mention of `QA_BK01_Alcove2C_EastJamb` in game code is the removal comment at preface_playable_area.gd:1122, and a runtime node scan found no `QA_BK01*` node. The design spec still mentions it, which is historical and fine.
- No hole, gap or new z-fighting showed at the header slab or opening edge from this view. The ALCOVE2C hub now uses the normal seat/HubWallBacking path, and no floating backing slab was visible.
- Leftover note, no bug filed: `assets/textures/qa03/door_jamb_gunmetal_{albedo,orm}.png` are no longer used by the jamb. Patch/Gage can decide whether to remove them.

## Rev C stair core (5d8a9d9): quick visual pass
Placement: StairSetSwitchback and StairGuardHandrail at identity, approximately x -1.9..1.9, z -8.9..-0.8, y 0..5.3. The log reports `[M-70] stair core loaded ramps=4 guards=18 fallback_ramps=0`.
Views checked (camera -> target):
- base NE (1.5,1.6,-1.5)->(-1.0,1.2,-6.0)
- flight 1 side (-1.2,1.7,-1.0)->(-1.2,1.5,-6.0)
- mid landing (0.0,3.4,-4.5)->(0.0,2.6,-8.5)
- L2 glass (-1.0,5.8,-1.5)->(0.0,4.4,-6.0)
- tread close-up (-1.2,1.6,-3.6)->(-1.2,0.9,-5.0)

Clean:
- Every visible mesh has a material, and none is magenta or missing.
- All visible primitives have normals and UVs, and shading direction is correct on treads, risers, stringers and underside.
- The `-colonly`/`-convcolonly` meshes are hidden and do not render.
- No z-fighting seen. Slate tread caps sit 15 mm above the WhiteComposite landing top. The door and stringer plate faces only meet hidden back faces. The anchor shoes and the floor showed no flicker.
- Guard glass (BLEND, double-sided, alpha 0.25) sorts correctly against the rails and the handrail behind it. There was no dark halo or flicker, and the flashlight gives a soft hotspot with no blowout.
- No UV stretching is visible, because there are no textures (see VIS-18).
- Flashlight on the treads: the soft beam edge has no shadow acne or peter-panning on nosings or treads.

### VIS-18: Low. Stair GLBs ship untextured flat-color materials
- Both GLBs have `images: []`. WhiteComposite, Slate, Gunmetal, BrushedAlloy, Glass, LockAmber and AccentViolet are all factor-only PBR, with no albedo, ORM or normal maps.
- Under the flashlight, treads and stringers read as smooth plastic next to the textured sector walls and floors. The difference is clearest in the tread close-up at (-1.2,1.6,-3.6)->(-1.2,0.9,-5.0).
- Expected: treads/slate and the cast composite carry albedo, ORM and normal maps that match the sector material set, or the spec explicitly records flat color as intended.

### VIS-19: Low. Flight 2 WhiteComposite underside reads near-white under the flashlight
- Repro: from (0.0,3.4,-4.5) look toward (0.0,2.6,-8.5). The underside of Flight2_Modules and L2_Landing is around x 0.4..1.9, y 2.5..4.2.
- The material has albedo 0.92 and roughness 0.35 with no texture. In the flashlight it reaches near-flat white with no surface detail. This is the brightest surface in the dark stair core, and it pulls attention from the walkway.
- This is a material/albedo issue, not a lighting-look change. A suggested fix is to drop the albedo to about 0.7 and/or add a texture, which ties in with VIS-18.

## Limits
These are software renders only, with no GPU check. The stair-to-sector-wall seam at z -8.9 was only seen at a distance.
