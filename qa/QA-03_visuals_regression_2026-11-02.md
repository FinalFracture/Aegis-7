# QA-03 Visuals Regression Sweep: 2026-11-02
Build: main @ ee10b2b (fresh clone). Tester: QA-03. Scope: regressions and broken materials only. Dark interiors are intended (M-68 closed), and look changes are on hold (M-69), so brightness is not filed. M-70 and the stairs were skipped.
Method: code read, plus a flashlight render run under xvfb with Godot opengl3 on llvmpipe (software rendering, not a GPU). The harness ran from an out-of-repo copy, so no game code was edited. Screenshots are in /workspace/qa03-shots/ (box only, not committed).

## Summary
- VIS-01..15: 13 fixed, 1 open (VIS-01), 1 not re-verified (VIS-14, doc staleness).
- Spec items M-15..19, M-33..36, M-48, M-49: applied correctly in code (2f991a5). No regressions found.
- New: VIS-16 (Low), VIS-17 (Low). No High or Med.

## Re-check VIS-01..VIS-15
| ID | Status | Evidence |
|---|---|---|
| VIS-01 Compatibility renderer | OPEN | project.godot:92-93 still `gl_compatibility`, while the features list says "Forward Plus" |
| VIS-02 / shadow range | FIXED | PPA:2893 `directional_shadow_max_distance = 60.0` |
| VIS-03 / sun below deck | FIXED | PPA:2995-3004 elevation fade clamp((elev+5)/15,0,1) |
| VIS-04 / M-15 blanket emission | FIXED | `_emissive_mats` PPA:276, 3044-3069; 0.22 blanket gone |
| VIS-05 / M-16 emergency restore | FIXED | cache loops PPA:3044-3075 (verified in R3 by luma) |
| VIS-06 / M-17 window glass | FIXED | PPA:1365-1378 alpha 0.14, metallic 0, rim 0.35; mullions PPA:1446 |
| VIS-07 / M-18 single double-sided mesh | FIXED | 3 single-sided meshes (Strip, CapA, CapB), CULL_BACK, render_priority -1/-2, sorting_offset (PPA:1418-1424, 1756, 1773) |
| VIS-08 / M-19 sky reflections | FIXED | playable_area.tscn ambient=Color(2), reflected=BG(0); PPA:385/388; probe UPDATE_ALWAYS PPA:2920 |
| VIS-09 / M-33 starfield caps | FIXED | PPA:4790/4854 `cap_top = false` |
| VIS-10 / M-34 prop glass | FIXED | per-blob tint `_prop_glass_tint` PPA:3254/3346; no blanket cull-disable on props (the remaining CULL_DISABLED PPA:2621 is additive RFID rings, which is OK) |
| VIS-11 / M-35 grass | FIXED | rec_grass albedo/normal/orm PPA:1877-1880 |
| VIS-12 / M-48 dust outline | FIXED (see VIS-16) | lit, textured (qa03/apt201_bench_dust_outline_decal.png), CULL_BACK, depth-draw off, priority -1 |
| VIS-13 / M-49 door jamb | FIXED | gunmetal albedo/ORM triplanar PPA:1131-1149 |
| VIS-14 stale spec refs | NOT RE-VERIFIED | doc-only; Sloane re-anchored to 4.7 in 363b349 |
| VIS-15 unused textures | FIXED | rail, jamb, grass, and dust textures are all referenced now; every `_load_tex()` path resolves |

Also M-36 rail: brushed titanium albedo/ORM PPA:1103-1115 is applied.

## Glass / observation window
- The strip is at r=199.0 and the mullion ribs span r 198.8-199.0. The mullion outer face sits coplanar with the glass, but it faces outward, and the glass is single-sided facing inward, so there is no visible z-fight from inside. The cap perimeter ring (r 198.8-200) is near the cap discs and is not render-verified, so it needs a GPU check from the window.
- Mezzanine glass balustrade (-0.76, 4.78, -4.83): the camera test spot landed in an unlit or occluded volume (luma 2.8 with the flashlight on or off), so the result is inconclusive.

## M-37 assets (not placed yet)
All 13 files load. The 4 decals (#103, #104, #202, #204) are 1024² RGBA with usable alpha. The 8 window cards (101-104, 201-204) are 2048x1024 RGB. They have no alpha channel, so they need an opaque card or emission use, as the spec intends. There is also a preview sheet (2050x950). No defects.

## Flashlight (PlayerFlashlight, PPA:3471-3482)
SpotLight3D attached to the camera at offset (0.10, -0.06, -0.05): energy 2.4, range 16 m, angle 26°, attenuation 0.9, shadows on, bias 0.03, normal bias default. It is not included in the emergency dimming, which is correct for a hand torch. The FP arm and sleeve have their shadows off (PPA:2532, 2645), so there is no self-shadow.
Render results (llvmpipe):
- Atrium (2.0, 1.7, -6.0) looking at (2.0, 1.0, -10.0): luma goes 21.9 to 31.7. The beam shows a clean disc with a soft edge. No blowout, 0% clipped pixels. The floor grate normals respond, with no acne.
- Wall close-up (2.0, 1.6, -8.0) looking at (2.0, 1.6, -12.0): luma goes 19.3 to 28.2. No visible texture stretching, low-res texels or z-fighting on the slatted wall. The monitor is readable and the orange panel is fine.
- Apt 201 dust spot (-12.05, 6.0, 5.5) looking at (-12.05, 4.42, 7.65): luma goes 7.8 to 7.9, so the beam did not reach a lit surface. The camera is probably outside or above the room, so the result is inconclusive.
- Alcove 2C (-8.5, 6.3, -2.0) looking at (-10.18, 5.71, -3.55): see VIS-17.

## New bugs
### VIS-16 [Low] Apt 201 dust outline is still an alpha QuadMesh, not the #54 Decal
- Location: PPA:2152-2181, `Apt201_ExBench_DustOutline` (-12.05, 4.424, 7.65).
- Repro: read `_spawn_apt201_bench_outline`. It builds a QuadMesh with TRANSPARENCY_ALPHA at a fixed y = 4.418 + 0.006. The comment says the floor datum is 4.415, but the same file says the L2 slab top is 4.2.
- Problem: if the floor is 4.2, the quad floats 22 cm. If it is 4.415, it hovers 9 mm, with no z-fight because depth draw is off. Either way it does not conform to the floor, it sorts as transparent, and it is not the Decal the spec calls for.
- Fix: use a Decal node with the M-37 #54 set, or derive y from a floor raycast.

### VIS-17 [Low] Alcove 2C wall display renders as a fully clipped white panel
- Location: seen from (-8.5, 6.3, -2.0) looking at (-10.18, 5.71, -3.55). The panel is at the left of the frame, above the bench.
- Repro: /workspace/qa03-shots/flash_alcove2c_jamb_rail_off.png and _on.png show about 7.9% of pixels at 250+, with the same result with the flashlight on or off.
- Problem: there is no screen content, unlike the atrium monitor, which renders readable UI. This looks like a missing screen texture or emission overdrive. It is a broken material, not a darkness issue. Confirm on GPU.

## Screenshots (box only, not committed)
/workspace/qa03-shots/flash_{atrium,wall_closeup,apt201_dust,alcove2c_jamb_rail,mezz_glass}_{off,on}.png

## Not verified
GPU look, the window cap ring from inside, the Apt 201 and mezzanine spots (camera placement), and z-fighting at distance.
