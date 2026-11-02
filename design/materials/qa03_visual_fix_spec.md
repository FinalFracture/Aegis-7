# QA-03 visual fix spec: M-15…M-19, M-33…M-37 (Sloane, 2026-11-01)
Source: `qa/MASTER_BUG_LIST.md`, `qa/QA-03_visuals_2026-11-01.md`. I read the code but didn't edit it. References are by **function + node name** in `godot/scripts/preface_playable_area.gd` (**PPA**), checked against main at c593f58 (re-anchored for M-50).
Renderer: **gl_compatibility, Godot 4.7** (`project.godot`: features "4.7", rendering_method gl_compatibility). Colours follow the Aegis-7 Standard. **Apply:** G = Gage (code), R = Rook (mesh), S = Sloane (texture).

| ID | One-line fix | Apply |
|---|---|---|
| M-15 | Delete the blanket 22% albedo emission; give emission only to luminous surfaces | G |
| M-16 | Cache the authored light values and restore from the cache; dim everything (task, spot, emission) on a curve | G |
| M-17 | Window glass: dielectric (metallic 0), alpha 0.14, cool tint, rim; add mullions | G + R |
| M-18 | Split the strip and the 2 caps into 3 single-sided meshes, each with its own render_priority | G |
| M-19 | Reflections from a black background, ambient from COLOR; re-trigger the probe after interiors stream in | G |
| M-33 | Remove the starfield caps from the CylinderMesh; separate planar-UV cap discs; anisotropic filtering | G |
| M-34 | Keep the authored glass tints and cull modes; use DISABLED only for thin single-plane parts | G |
| M-35 | Grass slab gets `textures/qa03/rec_grass_*` (made) | G (+S done) |
| M-36 | Alcove 2C rails get `textures/qa03/rail_brushed_titanium_*` (made) | G (+S done) |
| M-37 | Window cards ×8 + removal decal set: spec only (open handoff) | S → G |
| M-48 | Apt201 bench dust outline: replace the solid tan quad with the RGBA decal texture on a BLEND quad (made) | G (+S done) |
| M-49 | Door jamb: gunmetal brushed texture set (made) on `jamb_mat` | G (+S done) |
| M-50 | Spec re-anchored to Godot 4.7 and to function/node names | S (done) |

---
## M-15: blanket drum self-emission
**Root cause:** PPA `_cut_observation_window()`, in the `[CYL-01]` emission loop over the drum meshes. Every opaque drum surface gets `dup.emission = bm.albedo_color * 0.22`, energy 1.0. That is untextured, survives emergency lighting, and flattens the night side.
**Fix:**
- Delete the loop. The night side should be lifted by ambient (M-19/window section), not by emission.
- Enable emission only where a material name matches the list below; leave everything else at `emission_enabled = false`.
- Use `emission_texture` = the surface's own emission map if one exists. Otherwise use the albedo texture with `emission` = white × the factor below, so the texture shows instead of a flat tint.

| Surface (name contains) | emission_energy_multiplier |
|---|---|
| `luminaire`, `ceiling_panel`, `lightstrip` | 2.0 |
| `signage`, `header_sign` | 1.5 |
| `status`, `led` | 3.0 |
| `oled`, amber bars (#FF9500) | 1.2 |
| `holo`, `lens` | 0.8 (existing ×0.8 rule, M-34) |
| everything else | 0 (off) |

Register every emissive material in `_emissive_mats: Array` with its authored energy, so M-16 can dim them.

## M-16: emergency lighting toggle
**Root cause:** PPA `_set_emergency_lighting()` hard-codes the restore values: fill 0.34 (authored 0.28 on `AtriumSkyBounceFill` in `_setup_sector_lighting()`) and ambient 0.36 (authored 0.42 in the `preface_playable_area.tscn` Environment). It only recolours the task omnis (`_task_lights`) and keeps their energy. The SpotLights created in `_setup_sector_lighting()` and the emission aren't touched.
**Fix:** capture the authored values once, at the end of `_setup_sector_lighting()`, after the env duplicate in `_ready()`: sun energy, fill energy, `env.ambient_light_energy`, `ambient_light_color`, and the colour and energy of every task omni, spot and `_emissive_mats` entry. Restore from that cache only.

| Channel | Nominal (authored) | Emergency |
|---|---|---|
| Sun | 0.78 (window section if retuned) | 0.05 |
| Fill `AtriumSkyBounceFill` | **0.28** | 0.03 |
| Ambient energy / colour | **0.42** / (0.78,0.82,0.88) | 0.10 / `#3A1A16` |
| Task omnis | cached colour and energy (0.7-0.9) | `#C2402A`, energy × 0.25 |
| SpotLights | cached | energy × 0.15 |
| Emissive surfaces (M-15 list) | cached energy | × 0.10. Red emergency strips (if present) go to 2.5 |

**Dim curve:**
- **Turning on:** a 1.2 s tween, `TRANS_EXPO` / `EASE_OUT`, preceded by 3 brownout flickers in the first 0.3 s (energy ×0.4 → ×1 → ×0.2 → ×0.8 → curve start).
- **Restoring:** 2.5 s, `TRANS_SINE` / `EASE_IN_OUT`, with the luminaires staggered by 0.08 s per light in array order.
- Kill any running tween before starting a new one.

## M-17: observation window glass invisible / wrong
**Root cause:** PPA `_cut_observation_window()`, material `Mat_ObservationWindowGlass`: albedo (0.82,0.92,0.96, **0.06**), **metallic 0.85**, roughness 0.06.
**Fix (StandardMaterial3D):**
- `transparency = ALPHA` (alphaMode BLEND), `albedo_color = Color(0.70, 0.82, 0.88, 0.14)`
- `metallic = 0.0`, `metallic_specular = 0.5`, `roughness = 0.04`
- `rim_enabled = true`, `rim = 0.35`, `rim_tint = 0.6` (cheap Fresnel; works on Compatibility)
- `cull_mode = BACK` (M-18), `depth_draw_mode = DEPTH_DRAW_DISABLED`, `shadow_casting = OFF`

**Mullions (R):** opaque ribs every 6° across the 36° wedge, so 5 interior ribs plus 2 edge frames. Each is 0.30 m wide and 0.20 m deep, in gunmetal `#1A1E24` with metallic 1 and roughness 0.65, using the existing `facade_titanium_gunmetal_hull.png`. Each cap disc also gets a 1.2 m perimeter ring.

## M-18: one double-sided alpha mesh
**Root cause:** PPA `_cut_observation_window()` builds one SurfaceTool ArrayMesh (node `ObservationWindowGlass`) holding the strip and both cap discs, with `CULL_DISABLED`. Transparent sorting is per instance origin.
**Fix (G):**
- Build 3 MeshInstance3D nodes, `ObservationWindowGlass_Strip`, `_CapA` and `_CapB`, each with its own origin at its own centroid.
- They are single-sided (`CULL_BACK`) with normals facing the habitat interior. Seen from outside the hull, the glass is simply not drawn, which is fine.
- `render_priority`: starfield (opaque/unshaded) n/a, caps **-2**, strip **-1**, prop glass **0**, force-field door planes **+1** and the split seam **+2**. That way the door fields always draw over the window behind them.
- Optionally set `sorting_offset = -50` on the strip to push it back further.

## M-19: sky reflections vs black space; probe bakes too early
**Root cause:**
- The `preface_playable_area.tscn` Environment has `reflected_light_source = 2` (Sky) with a blue-grey ProceduralSky, while PPA `_ready()` forces `background_mode = BG_COLOR` black.
- Ambient is `ambient_light_source = 3` (**Sky**) with sky contribution 0.32, so it is also sky-tinted, despite the `[CYL-01]` comment in `_ready()`.
- The probe `AtriumBoxReflectionProbe` (`_setup_sector_lighting()`) is `UPDATE_ONCE` at build time, before interiors stream in.

**Fix:**
- .tscn: `reflected_light_source = 0` (Background, black) and `ambient_light_source = 2` (Color), ambient colour (0.78,0.82,0.88), energy 0.42. Remove the ProceduralSky resource, or keep it only for the editor.
- Probe: `interior = true` (no sky), `intensity = 0.3`. After the interior streaming finishes, and on each respawn (INTERIOR_RESPAWN_Z path), re-trigger the bake: set `update_mode = UPDATE_ALWAYS` for 2 frames, then back to `UPDATE_ONCE`.
- **Godot 4.7 Compatibility supports ReflectionProbe (at most 2 per mesh)**, so the probe fix does take effect. Keep at most 2 probes overlapping any mesh; extra ones are silently dropped.
- The window-promenade `rail_mat` (PPA `_build_cylinder_hab7_fullscale_world()`, metallic 0.82, roughness 0.28) should change to roughness 0.36.

## M-33: starfield end caps stretched / shimmer
**Root cause:** PPA `_build_starfield_outer_cylinder()`, node `StarfieldOuterBarrelMesh`, material `Mat_StarfieldOuterCylinder`. The `CylinderMesh` with `cap_top/bottom = true` shares `uv1_scale (6,3)` with the barrel. Radial cap UVs smear the stars, and filtering is `LINEAR_WITH_MIPMAPS`, so stars fade at 2200 m.
**Fix (G):**
- Set `cap_top = cap_bottom = false`.
- Add 2 caps as `PlaneMesh` (4400 × 4400 m, oriented on the axis) with their own material: `uv1_triplanar = false`, planar UV `uv1_scale = (4, 4)`, same star texture, unshaded, `CULL_BACK` facing inward.
- Barrel: `uv1_scale = (9, 3)`. That gives 1536 m × 1600 m per tile, about square instead of 2304 × 1600.
- Both use `TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC`.
- Generate stars at least 2 px wide in `_make_procedural_starfield_texture()`, with beacon diffraction crosses at least 3 px, so the mips keep them.

## M-34: prop glass forced grey-blue; all prop surfaces double-sided
**Root cause:**
- PPA `_upgrade_sector_materials()` sets `smat.cull_mode = CULL_DISABLED` for every imported surface.
- The same function replaces the glass albedo with Color(0.35,0.42,0.47, a∈[0.22,0.30]), with metallic 0.16.

**Fix (G):**
- Keep the authored `cull_mode` (glTF default BACK). Set DISABLED only when the material or mesh name contains `foliage`, `leaf`, `card`, `decal`, `cloth`, `transom`, `holo` or `field`, i.e. single-plane parts.
- Closed glass volumes (both faces modeled) stay BACK.
- Glass: keep the authored RGB, clamp alpha to [0.14, 0.40], `metallic = 0`, `roughness = max(authored, 0.04)`, `metallic_specular = 0.5`.

Per-prop tints, used only when the glTF has no colour (white):

| Prop glass (name contains) | albedo RGBA |
|---|---|
| `viewport`, `window` | (0.70, 0.82, 0.88, 0.14) |
| `hydro` (cylinder) | (0.72, 0.90, 0.80, 0.22) |
| `suitbay`, `locker` | (0.75, 0.85, 0.95, 0.18) |
| `sonic_shield` (vanity) | (0.80, 0.86, 0.95, 0.20) |
| `autodoc`, `med` canopy | (0.85, 0.92, 0.95, 0.20) |
| `holo`, `lens` | Keep the authored colour, alpha 0.35, unshaded, emission ×0.8, DISABLED cull |
| `transom` | (0.72, 0.80, 0.86, 0.32) |

## M-35: grass slab placeholder
**Root cause:** PPA `_add_recreation_grass_slab()`, flat `albedo_color (0.24,0.52,0.18)`, no textures, `CULL_DISABLED`.
**Fix:**
- **S (done):** `godot/assets/textures/qa03/rec_grass_albedo.png`, `rec_grass_normal.png` and `rec_grass_orm.png` (512², seamless).
- **G:**
  - `albedo_color` white with `albedo_texture` = the albedo map.
  - `normal_enabled`, `normal_scale 0.6`.
  - `roughness_texture` = the ORM with channel G (0.88-0.96); AO from R with `ao_light_affect 0.3`.
  - `uv1_scale` = (arc length / 2 m, slab width / 2 m), `cull_mode BACK`.

## M-36: Alcove 2C rail flat grey
**Root cause:** PPA `_add_playtest_seam_blocks()`. `rail_mat` is untextured albedo (0.78,0.80,0.83), metallic 0.35, roughness 0.38, used on `Seam03_Alcove2C_EastRail` and on `Seam03_Alcove2C_Rail` via `edge_mat`.
**Fix:**
- **S (done):** `godot/assets/textures/qa03/rail_brushed_titanium_albedo.png` and `rail_brushed_titanium_orm.png` (512², brushing along U, ~1% swing).
- **G:** for both materials:
  - albedo white with `albedo_texture` = the albedo map.
  - `metallic 1.0` with `metallic_texture` = the ORM B channel, `roughness_texture` = the ORM G channel (0.34-0.40).
  - `uv1_triplanar = true`, `uv1_scale = (2,2,2)`.

## M-37: window cards ×8 + removal decals (open handoff; spec only)
- **#6 Lit window interior card ×8** (`design/residential_asset_list_rev_c.md`:14). One 3.0 × 1.5 m quad per apartment window, 0.15 m behind the glass, built from the existing combos in `design/assets/window_card/`.
  - Material: unshaded, albedo + emission from the same atlas (1024×512), emission energy 0.9 day / 1.3 night, ×0.10 in emergency (M-16 list).
  - Parallax-interior variant optional (`combo_*` box atlases exist). `cull_mode BACK`, opaque.
  - **S** delivers 8 atlases + glb (one per unit); **G** places them.
- **#54 Removal decal set** (:73). Godot 4.7 Compatibility does **not** support Decal nodes (they arrive in 4.8), so each piece ships as a 1024² RGBA texture on a BLEND quad. Swap to Decal nodes once the project moves to 4.8+ or a Forward+/Mobile build. The Apt201 bench outline is done (M-48).
  - Pieces: dust outlines for the lab bench and workbench, shelf ghost + 6 anchor holes, planter clamp-bolt marks + water ring.
  - albedo_mix 0.85, `normal_fade 0.5`, upper/lower fade 0.3, cull mask world only.
  - Placement: units 104 and 201, 204 (emitter bench outline), 103 and 202.
  - **S** makes the textures; **G** places them.

## M-48: Apt201 bench dust outline is a solid tan quad
**Root cause:** PPA `_spawn_apt201_bench_outline()`, node `Apt201_ExBench_DustOutline` at (-12.05, 4.418, 7.65). It's a 3.7 × 2.5 m QuadMesh with a solid unshaded tan albedo (0.55,0.50,0.42, 0.55), `CULL_DISABLED`, 3 mm above the floor. That risks z-fighting and ignores lighting and emergency mode.
**Fix:**
- **S (done):** `godot/assets/textures/qa03/apt201_bench_dust_outline_decal.png`, 1024² RGBA. It's a soft dust ridge along the old bench footprint (3.1 × 1.9 m inset), light falloff outside, a near-clean interior, 4 faint leg marks, and alpha 0 at the borders. Mapped 1:1 onto the existing 3.7 × 2.5 m quad, so it needs no UV change.
- **G (4.7 Compatibility, no Decal nodes):** keep the quad and its size and position, raised to y = 4.418 + 0.006. Material:
  - `transparency = ALPHA`, `albedo_color = white`, `albedo_texture` = the decal PNG.
  - **Lit** (remove UNSHADED, so it dims in emergency), `roughness = 1.0`, `metallic = 0`.
  - `cull_mode = BACK` (face up), `render_priority = -1`.
  - `depth_draw_mode = DISABLED`, `shadow_casting = OFF`.
- **G (later, Godot 4.8+ or Forward+/Mobile):** replace it with a `Decal` node, size (3.7, 0.2, 2.5), `texture_albedo` = the same PNG, `albedo_mix 0.85`, upper/lower fade 0.3, cull mask world only, and delete the quad.

## M-49: door jamb untextured flat grey
**Root cause:** PPA `_add_playtest_seam_blocks()` builds `jamb_mat` (albedo (0.26,0.29,0.33), metallic 0.8, roughness 0.34, untextured) for `QA_BK01_Alcove2C_EastJamb`.
**Fix:**
- **S (done):** `godot/assets/textures/qa03/door_jamb_gunmetal_albedo.png` and `door_jamb_gunmetal_orm.png`, 512², seamless. Carbon-slate gunmetal `#282E38` (zero-wood palette) with vertical brushing at ~1% swing. ORM: AO 0.95, roughness 0.60–0.69, metallic 1.
- **G:** `jamb_mat` gets:
  - `albedo_color = white` with `albedo_texture` = the albedo map.
  - `metallic = 1.0` with `metallic_texture` = ORM (channel B), and `roughness_texture` = ORM (channel G).
  - `uv1_triplanar = true`, `uv1_scale = (2,2,2)`.
  - Roughness around 0.65 matches the titanium/gunmetal values in 8705e13 and avoids the mirror look.

---
## Gage's cylinder observation window (36° slice, orbiting starfield + sun), gl_compatibility values
**Glass:** as in M-17:
- alpha 0.14, albedo (0.70,0.82,0.88), metallic 0, specular 0.5, roughness 0.04, rim 0.35 / tint 0.6
- CULL_BACK, no depth write, no shadows
- render_priority: strip -1 / caps -2
- mullions every 6° (R)

**Sun `DirectionalLight3D`** (replaces the `AtriumGoldenHourSunlight` values in `_setup_sector_lighting()`):
- `light_color = #FFF6EA` (unfiltered space sun, 5800 K)
- `light_energy = 1.4` at full exposure, multiplied by `clamp((elevation_deg + 5) / 15, 0, 1)`. Elevation is measured against the local deck up vector. This fades the sun to 0 below the deck horizon and fixes the "lit from under the deck" half of the revolution (QA-03 above VIS-04).
- `shadow_enabled = true`, `directional_shadow_mode = PARALLEL_2_SPLITS` (cheaper on Compatibility), `directional_shadow_max_distance = 60`, `shadow_bias = 0.03`, `shadow_normal_bias = 1.5`, `shadow_blur = 1.0`
- `light_angular_distance = 0.5`

**Fill:** `AtriumSkyBounceFill` stays at 0.28 with `#C8DCF0` and no shadow. Scale it by 0.5 + 0.5 × the sun factor, so the night side keeps half.

**Environment:**
- Background: black colour.
- Ambient: `ambient_light_source = COLOR`, (0.62, 0.68, 0.78), energy 0.30. This is lower than 0.42 because the sun is brighter; keep 0.42 if the sun stays at 0.78.
- `reflected_light_source = BG`.
- Tonemap: `tonemap_mode = FILMIC (2)`, `tonemap_exposure = 1.0`, `tonemap_white = 4.0`.
- Glow: `glow_enabled = true`, intensity 0.4, bloom 0.05, `glow_hdr_threshold = 1.0`. Keep it subtle so the starfield doesn't bloom into fog.
- SSR off (it's Forward+ only, already handled in `_ready()`).

**Starfield:** unshaded, unaffected by lights or exposure (M-33 settings).

## Caveats
- I had no GPU and took no renders, so these values come from reading the code. I haven't verified them in-engine. Patch should run a `--render-all` pass after Gage applies them.
- **Godot 4.7 Compatibility (re-checked for M-50 against docs.godotengine.org/en/4.7):**
  - ReflectionProbe is supported, at most 2 per mesh.
  - Decal nodes are **not** supported (only from 4.8), so use BLEND quads (M-37, M-48).
  - The colour buffer is RGBA8 (LDR, no HDR), so emission above about 1.0 clips and `tonemap_white` / glow thresholds act on clamped values. Keep emission energies at or below the M-15 table and treat glow as subtle. Verify in a render.
  - SSR, SSIL, VoxelGI and SDFGI are not available; there is no debanding.
- The `ambient_light_source` enum values (Color = 2, Sky = 3) and `reflected_light_source` (BG = 0, Sky = 2) are from the Godot 4 Environment enums.

---
## Round 3 (2026-11-01): M-68, M-69, M-06
Checked against main a7c20cd. These are diagnoses from reading the code plus Patch's llvmpipe shots (`/workspace/qa_shots_r2/m16_atrium_normal.png`, mean 11.5; `m17_m18_window_up.png`, mean 190). I didn't run a new render, so all values need a GPU confirmation (T-02).

### M-68 [High]: atrium near-black after M-15
**Root causes:**
1. **Omni energies are tuned as if there's no falloff.** In `_setup_sector_lighting()` the 6 task omnis (`Apt201_TaskLamp27` … `Atrium_Midhead_BounceFill`) use energy 0.70–0.90 with `omni_attenuation 1.2`. Godot 4 omni lights fall off with roughly inverse-square distance. The only atrium-wide light, `Atrium_Midhead_BounceFill` at (0, 7.85, -2.2), is about 8.7 m from the QA spot (2, 0.12, -6), which leaves roughly 1% of its energy there. The rest sit inside side rooms.
2. **The sun can't reach L1.** `AtriumGoldenHourSunlight` (1.4) only enters through the skylight. The L2 slabs shadow the ground-floor corridor, and the orbit `_sun_energy_factor()` fades it further.
3. **Ambient and fill are too weak for dark albedos.** Ambient is COLOR (0.62,0.68,0.78) × 0.30 from the .tscn and the `_ready()` env override. `AtriumSkyBounceFill` is 0.28 × (0.5–1.0). The zero-wood palette's gunmetal/slate surfaces (albedo ≈ 0.10–0.16) reflect only about 0.02 linear.
4. **Luminaire emission doesn't light anything.** `_build_ceiling_luminaire()` sets the `LuminaireDiffuser` emission to 0.85. There's no GI on gl_compatibility, so it doesn't light any surfaces; only the matching omni does, and that's case 1.
5. **Filmic `tonemap_white 4.0` darkens the midtones** in Compatibility's LDR pipeline.
6. **Compatibility per-object light cap:** `rendering/limits/opengl/max_lights_per_object` (default 8; not set in `project.godot`). Large merged sector meshes take at most 8 omni/spot lights, so extra lights may not show on walls.

**Corrected rig** (Gage, in `_setup_sector_lighting()` and the `_ready()` env override plus .tscn; `_cache_authored_lighting()` and M-16 keep working on these new values):

| Element | Value |
|---|---|
| Ambient (`_ready()` + .tscn) | COLOR (0.70, 0.74, 0.80), **energy 0.55** |
| `AtriumSkyBounceFill` | **0.65**, `#C8DCF0`, no shadow, still ×(0.5+0.5·sun factor). It isn't shadowed, so it reaches L1. |
| `AtriumGoldenHourSunlight` | 0.9 (see M-69); shadows unchanged |
| New **atrium ceiling panels** (6), via `_build_ceiling_luminaire()` + OmniLight3D, named `Atrium_CeilingPanel_01..06` | Positions: y 8.40 on a grid of x ∈ {-9, 0, 9} × z ∈ {-5, 4}. Panel 2.2 × 0.45 m, `#EBF0F5`, **energy 4.5, range 14, attenuation 1.0**, no shadow |
| New **L1 corridor under-slab lights** (4), `L1_Corridor_Light_01..04` | Positions: y 3.60, x ∈ {-9, -3, 3, 9}, z -6.0. Panel 1.4 × 0.36 m, `#F5E2C4`, **energy 2.5, range 8, attenuation 1.0**, no shadow |
| Existing task omnis (6) | Energies ×4 (0.70→2.8, 0.85→3.4, 0.84→3.4, 0.90→3.6). `Atrium_Midhead_BounceFill` 0.74→3.0. Keep ranges; attenuation 1.2→1.0 |
| Spots `Apt201_CeilingDownSpot`, `Room1B_CeilingDownSpot` | 0.42 → **3.0**, range 3.5 → **5.5**, angle unchanged, shadows on |
| `LuminaireDiffuser` emission (all panels) | **1.0** (8-bit clip point), emission = the light colour. Every panel has a matching OmniLight3D at the same position minus 0.15 m in y |
| `project.godot` | `rendering/limits/opengl/max_lights_per_object = 16` |
| Tonemap | Filmic, exposure **1.0**, white **2.0** (was 4.0) |

**Target:** atrium/L1 mean ≈ 90–110/255. If a GPU check comes in under 85, raise the ambient to 0.65 first, then the panel energies to 5.5. If it's over 120, lower the fill to 0.5.
**Emergency (M-16):** the cached ×0.25 / ×0.15 / ×0.10 multipliers now act on these values, so no change is needed. Ambient emergency stays at 0.10.

### M-69 [Med]: window/drum view blown out
**Root causes:**
- `AtriumGoldenHourSunlight` is 1.4 on the drum shell's aerospace-white panels (albedo ≈ 0.80–0.85, e.g. `deck.albedo_color (0.8,0.82,0.86)` in `_build_cylinder_hab7_fullscale_world()`). That's >1.0 linear, so it clips in 8-bit.
- **Glow** (intensity 0.4, `glow_hdr_threshold 1.0`) blooms everything near clip into a white haze.
- `Mat_ObservationWindowGlass` (alpha 0.14 + rim 0.35) adds a white veil over the whole view.
- `tonemap_white 4.0` with exposure 1.0 doesn't compress anything, because nothing in LDR exceeds 1.

**Values:**

| Item | Value |
|---|---|
| Sun | **0.9**, `#FFF6EA`, factor fade unchanged |
| Drum shell / deck albedo (`_build_cylinder_hab7_fullscale_world()` materials) | Multiply by **0.72**, e.g. deck (0.58, 0.59, 0.62). Keep it lit, not unshaded. Albedo luma should stay ≤ 0.62. |
| Glow | **Off** on gl_compatibility (`glow_enabled = false`), or intensity 0.15 with threshold 0.95 if Jared wants some bloom |
| `Mat_ObservationWindowGlass` | alpha **0.10**, rim **0.15**, rim_tint 0.6. Everything else as M-17. |
| Emissive cyan strips in the window view | Emission ≤ 1.0 (M-15 table already) |
| Tonemap | Filmic, exposure 1.0, white **2.0** (shared with M-68) |

**Target:** 110–140/255. The sunlit shell lands at about 0.9 × 0.6 ≈ 0.54 linear, roughly 190 sRGB before filmic and about 150 after. The shadow side comes from ambient 0.55 × 0.6 plus the fill, and black space pulls the frame mean down. Sun-to-shade contrast stays about 3:1, so the sun is still readable.

### M-06: jagged slice edges (from M-69 shot)
- **Gage (root fix):** `_cut_observation_window()` drops whole shell triangles that cross the 36° slice planes, which leaves the saw-tooth. Clip each crossing triangle exactly against the two slice planes (θ = a0, a0+36°): split it at the plane intersection and keep the inner part, so the cut edge is a clean straight line.
- **Rook (cosmetic cover):** a frame mesh `ObservationWindowFrame`. It's a 0.6 m wide × 0.3 m deep gunmetal edge trim along both slice edges (800 m long) plus a 1.2 m rim ring per cap, using `door_jamb_gunmetal_*` / `facade_titanium_gunmetal_hull.png`, with metallic 1 and roughness 0.65.
- Gage places the frame and the M-17 mullions in the same pass. The trim hides any leftover sub-cm jaggies from shadow-acne or precision.

---
## M-37 delivered (2026-11-02): window cards #6 ×8 + removal decals #54
Preview: `design/materials/m37_window_cards_decals_preview_sheet.png`. Generator: box-only `/workspace/sl_tools/m37.py`. The lighting look is unchanged: the cards are self-lit stand-ins and don't add any lights.

### Window cards (`godot/assets/textures/window_cards/`)
- **Files:** `window_card_<unit>_albedo_emission.png`, 2048×1024 RGB, one per unit: 101, 102, 103, 104, 201, 202, 203, 204.
- **Look:** iter_01 flat card with the iter_05 blinds look baked in, gunmetal mullions and frame, and an OLED amber `#FF9500` wall clock plus status strip. No noise, so well under 1.2% micro-noise.
- **Per-unit content** (from the window-card README profiles):

| Unit | Content |
|---|---|
| 101 | Dim, bunk |
| 102 | Knocked-over plant, empty suit hook |
| 103 | Family, toys |
| 104 | Red solar glyph, desk terminal |
| 201 | Lights off; the clock reads `--:--` |
| 202 | Drawing, toys |
| 203 | Route model |
| 204 | Bench |

**Gage apply** (a new helper, e.g. `_place_window_cards()`, called after the sector loads in `_ready()` / `_assemble_open_doorless_sector()`):
- **Node:** one MeshInstance3D per unit, named `WindowCard_<unit>`, with a QuadMesh 3.0 × 1.5 m.
- **Placement:** bottom-centre on each apartment's exterior window, 0.15 m inside the glass, facing out (+normal toward the street/atrium). Use the window positions of each unit in the sector GLB (layout v2 rev C).
- **Material:** StandardMaterial3D with:
  - `shading_mode = UNSHADED`, `albedo_texture` = the unit's PNG, `albedo_color = white`
  - `transparency = DISABLED`, `cull_mode = BACK`, `texture_filter = LINEAR_WITH_MIPMAPS_ANISOTROPIC`
  - shadow casting off
- **Emergency (M-16):** add each card to the cached list and set `albedo_color` to (0.12, 0.12, 0.12) when emergency mode is on, restoring white on exit. These materials are unshaded, so this is a colour multiplier, not an emission energy.

### Removal decals #54 (`godot/assets/textures/removal_decals/`, 1024² RGBA, BLEND quads; 4.7 Compatibility has no Decal nodes)

| File | Unit / surface | Quad size | Notes |
|---|---|---|---|
| `decal_104_lab_bench_dust_outline.png` | 104, floor under the removed lab bench | 2.6 × 1.4 m | Dust ridge + 4 leg marks |
| `decal_204_emitter_bench_outline.png` | 204, floor under the removed emitter bench | 2.2 × 1.2 m | Dust ridge + faint centre scorch |
| `decal_103_shelf_ghost_anchor_holes.png` | 103, wall where the shelf hung | 2.0 × 2.0 m | Grime around a clean silhouette, shelf lines, 6 anchor holes |
| `decal_202_planter_clamp_water_ring.png` | 202, floor under the removed planter | 1.2 × 1.2 m | Water ring + 4 clamp-bolt marks |
| `qa03/apt201_bench_dust_outline_decal.png` (M-48) | 201, `Apt201_ExBench_DustOutline` | 3.7 × 2.5 m | Already specced in M-48 |

**Gage apply:** a helper `_spawn_removal_decals()` modelled on `_spawn_apt201_bench_outline()`, with one QuadMesh MeshInstance3D per row, named `<Unit>_RemovalDecal_<name>`.
- **Floor decals:** `orientation = FACE_Y`, raised 6 mm.
- **Wall decal:** `FACE_Z`, 4 mm off the wall.
- **Material (same as M-48):**
  - `transparency = ALPHA`, `albedo_texture` = the PNG, albedo white
  - **lit** (not unshaded, so it follows emergency and dark interiors), `roughness 1.0`, `metallic 0`
  - `cull_mode = BACK`, `depth_draw_mode = DISABLED`, `render_priority = -1`, no shadows
- **Placement:** the exact positions are the removed props' footprints in layout v2 rev C (`design/residential_asset_list_rev_c.md` #54). Gage reads them from the sector GLB node origins of the removed props.
