# QA-03 visual fix spec: M-15…M-19, M-33…M-37 (Sloane, 2026-11-01)
Source: `qa/MASTER_BUG_LIST.md`, `qa/QA-03_visuals_2026-11-01.md`. I read the code but didn't edit it; line numbers are from `godot/scripts/preface_playable_area.gd` (**PPA**) at HEAD on 2026-11-01.
Renderer: gl_compatibility, Godot 4.3. Colours follow the Aegis-7 Standard. **Apply:** G = Gage (code), R = Rook (mesh), S = Sloane (texture).

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

---
## M-15: blanket drum self-emission
**Root cause:** PPA:1398-1413. Every opaque drum surface gets `dup.emission = bm.albedo_color * 0.22` (:1411), energy 1.0. That is untextured, survives emergency lighting, and flattens the night side.
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
**Root cause:** PPA:2367-2382 hard-codes the restore values: fill 0.34 (:2373; authored 0.28 at :2299) and ambient 0.36 (:2380; authored 0.42 in `preface_playable_area.tscn`:21). It only recolours the task omnis and keeps their energy (:2375-2379). SpotLights (:2351) and emission aren't touched.
**Fix:** capture the authored values once, after `_build_lighting` and the env duplicate (:357): sun energy, fill energy, `env.ambient_light_energy`, `ambient_light_color`, and the colour and energy of every task omni, spot and `_emissive_mats` entry. Restore from that cache only.

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
**Root cause:** PPA:1416-1423 `Mat_ObservationWindowGlass`: albedo (0.82,0.92,0.96, **0.06**), **metallic 0.85**, roughness 0.06.
**Fix (StandardMaterial3D):**
- `transparency = ALPHA` (alphaMode BLEND), `albedo_color = Color(0.70, 0.82, 0.88, 0.14)`
- `metallic = 0.0`, `metallic_specular = 0.5`, `roughness = 0.04`
- `rim_enabled = true`, `rim = 0.35`, `rim_tint = 0.6` (cheap Fresnel; works on Compatibility)
- `cull_mode = BACK` (M-18), `depth_draw_mode = DEPTH_DRAW_DISABLED`, `shadow_casting = OFF`

**Mullions (R):** opaque ribs every 6° across the 36° wedge, so 5 interior ribs plus 2 edge frames. Each is 0.30 m wide and 0.20 m deep, in gunmetal `#1A1E24` with metallic 1 and roughness 0.65, using the existing `facade_titanium_gunmetal_hull.png`. Each cap disc also gets a 1.2 m perimeter ring.

## M-18: one double-sided alpha mesh
**Root cause:** PPA:1424-1490 builds one SurfaceTool ArrayMesh (`ObservationWindowGlass`, :1478) holding the strip and both cap discs, with `CULL_DISABLED` (:1423). Transparent sorting is per instance origin.
**Fix (G):**
- Build 3 MeshInstance3D nodes, `ObservationWindowGlass_Strip`, `_CapA` and `_CapB`, each with its own origin at its own centroid.
- They are single-sided (`CULL_BACK`) with normals facing the habitat interior. Seen from outside the hull, the glass is simply not drawn, which is fine.
- `render_priority`: starfield (opaque/unshaded) n/a, caps **-2**, strip **-1**, prop glass **0**, force-field door planes **+1** and the split seam **+2**. That way the door fields always draw over the window behind them.
- Optionally set `sorting_offset = -50` on the strip to push it back further.

## M-19: sky reflections vs black space; probe bakes too early
**Root cause:**
- `preface_playable_area.tscn`:22 has `reflected_light_source = 2` (Sky) with a blue-grey ProceduralSky, while PPA:357-359 forces `background_mode = BG_COLOR` black.
- Ambient is `ambient_light_source = 3` (**Sky**, :18) with sky contribution 0.32 (:20), so it is also sky-tinted, despite the comment at :356.
- The probe (PPA:2304-2312) is `UPDATE_ONCE` at build time, before interiors stream in.

**Fix:**
- .tscn: `reflected_light_source = 0` (Background, black) and `ambient_light_source = 2` (Color), ambient colour (0.78,0.82,0.88), energy 0.42. Remove the ProceduralSky resource, or keep it only for the editor.
- Probe: `interior = true` (no sky), `intensity = 0.3`. After the interior streaming finishes, and on each respawn (INTERIOR_RESPAWN_Z path), re-trigger the bake: set `update_mode = UPDATE_ALWAYS` for 2 frames, then back to `UPDATE_ONCE`.
- **Caveat:** ReflectionProbe is not rendered by the Compatibility renderer in Godot 4.3. If so, metals get no reflections at all, so raise the metal roughness floor to 0.30 and rely on light specular.
- The window-promenade `rail_mat` (PPA:1150-1153, metallic 0.82, roughness 0.28) should change to roughness 0.36.

## M-33: starfield end caps stretched / shimmer
**Root cause:** PPA:4499-4535. `CylinderMesh` with `cap_top/bottom = true` (:4526) shares `uv1_scale (6,3)` (:4515) with the barrel. Radial cap UVs smear the stars, and filtering is `LINEAR_WITH_MIPMAPS` (:4516), so stars fade at 2200 m.
**Fix (G):**
- Set `cap_top = cap_bottom = false`.
- Add 2 caps as `PlaneMesh` (4400 × 4400 m, oriented on the axis) with their own material: `uv1_triplanar = false`, planar UV `uv1_scale = (4, 4)`, same star texture, unshaded, `CULL_BACK` facing inward.
- Barrel: `uv1_scale = (9, 3)`. That gives 1536 m × 1600 m per tile, about square instead of 2304 × 1600.
- Both use `TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC`.
- Generate stars at least 2 px wide in `_make_procedural_starfield_texture` (PPA:4425), with beacon diffraction crosses at least 3 px, so the mips keep them.

## M-34: prop glass forced grey-blue; all prop surfaces double-sided
**Root cause:**
- PPA:2451 sets `smat.cull_mode = CULL_DISABLED` for every imported surface.
- PPA:2454 replaces the glass albedo with Color(0.35,0.42,0.47, a∈[0.22,0.30]), with metallic 0.16 (:2456).

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
**Root cause:** PPA:1561-1565, flat `albedo_color (0.24,0.52,0.18)`, no textures, `CULL_DISABLED`.
**Fix:**
- **S (done):** `godot/assets/textures/qa03/rec_grass_albedo.png`, `rec_grass_normal.png` and `rec_grass_orm.png` (512², seamless).
- **G:**
  - `albedo_color` white with `albedo_texture` = the albedo map.
  - `normal_enabled`, `normal_scale 0.6`.
  - `roughness_texture` = the ORM with channel G (0.88-0.96); AO from R with `ao_light_affect 0.3`.
  - `uv1_scale` = (arc length / 2 m, slab width / 2 m), `cull_mode BACK`.

## M-36: Alcove 2C rail flat grey
**Root cause:** PPA:1063-1076. `rail_mat` is untextured albedo (0.78,0.80,0.83), metallic 0.35, roughness 0.38, used on `Seam03_Alcove2C_EastRail` (:1073) and on `Seam03_Alcove2C_Rail` via `edge_mat` (:1075-1076).
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
- **#54 Removal decal set** (:73). These are Decal nodes (Compatibility supports Decal in 4.3: verify), with 1024² albedo + alpha and normal.
  - Pieces: dust outlines for the lab bench and workbench, shelf ghost + 6 anchor holes, planter clamp-bolt marks + water ring.
  - albedo_mix 0.85, `normal_fade 0.5`, upper/lower fade 0.3, cull mask world only.
  - Placement: units 104 and 201, 204 (emitter bench outline), 103 and 202.
  - **S** makes the textures; **G** places them.

---
## Gage's cylinder observation window (36° slice, orbiting starfield + sun), gl_compatibility values
**Glass:** as in M-17:
- alpha 0.14, albedo (0.70,0.82,0.88), metallic 0, specular 0.5, roughness 0.04, rim 0.35 / tint 0.6
- CULL_BACK, no depth write, no shadows
- render_priority: strip -1 / caps -2
- mullions every 6° (R)

**Sun `DirectionalLight3D`** (replaces the "AtriumGoldenHourSunlight" values at PPA:2280-2292):
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
- SSR off (it's Forward+ only, already handled at :354).

**Starfield:** unshaded, unaffected by lights or exposure (M-33 settings).

## Caveats
- I had no GPU and took no renders, so these values come from reading the code. I haven't verified them in-engine. Patch should run a `--render-all` pass after Gage applies them.
- Godot 4.3 Compatibility may not render the ReflectionProbe, or may handle Decals and tonemap/glow differently (M-19, M-37, window). Gage should check the engine docs and adjust.
- The `ambient_light_source` enum values (Color = 2, Sky = 3) and `reflected_light_source` (BG = 0, Sky = 2) are from the Godot 4 Environment enums.
