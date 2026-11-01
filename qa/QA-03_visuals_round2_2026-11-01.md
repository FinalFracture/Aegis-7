# QA-03 Visuals Round 2: 2026-11-01
Tester: QA-03 (Grok Bot). Fresh clone of main at `27a8e35`. Checked against Sloane's spec `design/materials/qa03_visual_fix_spec.md` (583a3ac). Static code review plus headless review only. No GPU renders were taken and none are committed. No game code was edited.
Main file: `godot/scripts/preface_playable_area.gd` (PPA). Since 583a3ac, the line numbers have shifted by about +8 to +210.

## Summary
- **Spec compliance: 0 / 10 items applied.** Since 583a3ac, the only commits that touched PPA are 04bbed0 and 1c322a2, which are prop and egress work. None of M-15..M-19 or M-33..M-37 is in code, and the sun/fill/environment values for the window are not in code either. The qa03 textures (grass, rail) exist but nothing references them: `grep -rn "qa03/" godot` returns 0 hits.
- **Prior bugs:** 11 still open, 0 fixed, 0 regressed.
- **New bugs:** VIS-12..VIS-15. Med 1, Low 3.
- **Totals open:** High 3, Med 6, Low 6 (15).

## Re-check VIS-01..VIS-11
| Bug | Sev | Status | Evidence at 27a8e35 |
|---|---|---|---|
| VIS-01 Compatibility renderer vs Forward+ tuning | High | OPEN | project.godot:92-93 `gl_compatibility`; features list still says "Forward Plus" |
| VIS-02 Shadow range 45 m, sun leaks through hull | High | OPEN | PPA:2496 `directional_shadow_max_distance = 45.0` (spec: 60 plus elevation fade) |
| VIS-03 Orbiting sun lights deck from below | High | OPEN | PPA:3384 rotates the sun basis with the starfield; there is no elevation clamp/fade (spec: energy × clamp((elev+5)/15,0,1)) |
| VIS-04 / M-15 Blanket 22% emission | Med | OPEN | PPA:1419 `dup.emission = bm.albedo_color * 0.22`; no `_emissive_mats` |
| VIS-05 / M-16 Emergency restore values | Med | OPEN | PPA:2580 fill restores to 0.34 (authored 0.28); PPA:2589 ambient restores to 0.36 (authored 0.42); no cache, tween or spot/emission dimming |
| VIS-06 / M-17 Window glass invisible/metallic | Med | OPEN | PPA:1429 `metallic = 0.85`; alpha still 0.06; no rim; no mullions |
| VIS-07 / M-18 Single double-sided alpha mesh | Med | OPEN | PPA:1431 `CULL_DISABLED`; still one ObservationWindowGlass mesh; no render_priority anywhere in PPA |
| VIS-08 / M-19 Sky reflections vs black BG | Med | OPEN | tscn:18 `ambient_light_source = 3` (Sky), tscn:22 `reflected_light_source = 2` (Sky); probe PPA:2518 UPDATE_ONCE, no re-trigger |
| VIS-09 / M-33 Starfield caps stretched | Low | OPEN | PPA:4737 `cm.cap_top = true`; PPA:4726 `uv1_scale (6,3)` |
| VIS-10 / M-34 Prop glass grey-blue, all double-sided | Low | OPEN | PPA:2659 CULL_DISABLED on every surface; PPA:2662 forced Color(0.35,0.42,0.47) |
| VIS-11 / M-35 Grass slab untextured | Low | OPEN | PPA:1570 flat (0.24,0.52,0.18); PPA:1572 CULL_DISABLED; rec_grass_* unused |

Also open: **M-36**, the Alcove 2C rail is still untextured (rail_brushed_titanium_* unused), and **M-37** has no window cards or decals.
Environment window values not applied: tscn:24-25 has exposure 0.98 / white 1.65 (spec 1.0 / 4.0); sun is 0.78 warm golden-hour at a fixed -72° (spec #FFF6EA, 1.4, faded).

## New bugs
### VIS-12 [Med] Apt 201 "dust outline" is a solid, unshaded, semi-opaque tan slab
- **Location:** PPA `_spawn_apt201_bench_outline` (added in 04bbed0), node `Apt201_ExBench_DustOutline`, world (-12.05, 4.418, 7.65), Apt 201 L2.
- **Problem:** A 3.7×2.5 m QuadMesh with a flat Color(0.55,0.50,0.42, **0.55**), `SHADING_MODE_UNSHADED`, CULL_DISABLED and no texture. It reads as a uniform beige rug that ignores lighting: it does not darken on the night side or in emergency mode (it is not on any dim list), and it glows relative to the floor around it. It sits 3 mm above the floor datum (4.415), so z-fighting/shimmer is likely at distance. It is not the M-37 #54 Decal that the spec calls for.
- **Repro:** Load the preface → go to Apt 201 L2 by the old bench spot → toggle emergency lighting → the rectangle stays at the same brightness.
- **Expected:** A Decal (or shaded alpha-textured quad) with a dust-outline albedo/alpha, per M-37.

### VIS-13 [Low] New door jamb material is untextured flat grey
- **Location:** PPA ~:1080-1086 `jamb_mat` (added after 583a3ac): albedo (0.26,0.29,0.33), roughness 0.34, no textures.
- **Problem:** Same placeholder look as VIS-11/M-36. The jambs read as plastic next to the textured facade.
- **Repro:** Walk to any Rev C door jamb and inspect at under 2 m.
- **Expected:** facade_titanium_gunmetal / brushed titanium textures (triplanar).

### VIS-14 [Low] The fix spec's engine assumptions and line references are stale
- **Location:** `design/materials/qa03_visual_fix_spec.md`.
- **Problem:** The spec says Godot 4.3 and bases its caveats (ReflectionProbe, Decal and glow support on Compatibility) on 4.3. The project was reimported with 4.7.2 (c46ce39; project.godot features "4.7"). PPA line numbers are off by up to about 210, for example the emission loop at 1419 (spec says 1411) and the emergency toggle at 2578-2589 (spec says 2367-2382). There is a risk of misapplied edits.
- **Repro:** Compare the spec's references with HEAD.
- **Expected:** Sloane/Gage re-anchor by symbol name and re-check the caveats against 4.7 Compatibility.

### VIS-15 [Low] Unused quick-win textures shipped in the repo
- **Location:** `godot/assets/textures/qa03/` (5 PNGs, about 560 KB).
- **Problem:** The assets are imported but never referenced, so they add build size with no visual effect until M-35/M-36 are wired in.
- **Repro:** `grep -rn "qa03/" godot --include=*.gd --include=*.tscn --include=*.tres` returns nothing.

## Not verified
No GPU renders, so dark or blown-out areas, glass blending and backdrop shimmer were inferred from code, not seen. Patch should run `--render-all` after Gage applies the spec.
