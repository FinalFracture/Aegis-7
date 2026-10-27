# Cylinder Hab-7 — Interior Biome, Terrain, Water & Lighting Material/Texture Overhaul Spec
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Environment:** Full-Scale (`800m L × 400m Ø`, `R = 200m`) O'Neill Cylinder Hab-7 Interior Showcase (`cylinder_interior_showcase_sheet.png`)  
**Standard:** Unified "Aegis-7 Standard" (`<1.2%` micro-noise PBR, Warm Golden-Hour Axial Sunlight + Lush Terraced Biomes + Specular Ring-River Water + Volumetric Aerial Perspective)

---

## 1. Critique of Initial Interior Render (`/workspace/game-project/godot/renders/cylinder_interior/cylinder_interior_showcase_sheet.png`)

1. **Monotonous Cyan/White Palette (`#00FFFF` + `#FFFFFF`):** The initial 4-camera interior showcase was dominated by sterile white blocky massing, unmodulated `#00FFFF` cyan solarium bands, and uniform cyan window grids across all three $120^\circ$ city valleys.
2. **Flat Emissive Axial Spine & Zero Aerial Perspective:** The central Axial Solar Spine rendered as a flat cyan neon tube without directional golden-hour solar warmth, shadow casting across the `R = 200m` curved ground, or Rayleigh/aerial-perspective depth haze across the `400m` diameter and `800m` axial length.
3. **Untextured Ground, Water & Terraces:** The hydro-canals and solarium park strips read as flat cyan and solid emerald bands rather than tiered botanical terraces, weathered basalt/titanium cliff retaining walls, warm travertine-alloy pedestrian promenades, and deep specular ring-river water.
4. **Uniform Window Emissions:** Every building block shared identical cyan window strips, lacking the lived-in contrast between **Warm Amber/Gold Residential & Civic Clusters (`#FFB703` / `#FFE0A3`)** and **Cool Industrial/Command Telemetry Bays (`#00E5FF` / `#8B6CFF` / `#FF7B29`)**.

---

## 2. Generated Cylinder Interior Material & Texture Suite (`/workspace/game-project/assets/textures/cylinder_interior/`)

All 6 textures are generated at `512×512` PNG (`<1.0%` controlled micro-noise, seamless/tileable UV layout) in `/workspace/game-project/assets/textures/cylinder_interior/` and mirrored to `/workspace/game-project/assets/textures/`:

| Texture File | Format | Primary Palette | Target Mesh / Surface Usage | Recommended PBR Parameters |
|---|---|---|---|---|
| `biome_terraced_botanical_canopy.png` | `512×512` RGB | Deep Forest `#1B4332`, Lush Terraced Green `#2D6A4F`, Sunlit Canopy `#40916C` / `#52B788`, Basalt Curbs `#3E4650` | Agricultural valleys, tiered botanical park belts, hillside arboretum terraces, green roof decks | `roughness = 0.72`, `metallic = 0.02`, subtle normal/bump height from green channel |
| `water_ring_river_specular.png` | `512×512` RGBA | Deep Sapphire `#0A3454`, Turquoise Bank `#15617D`, Golden-Cyan Caustic Shimmer `#80E5FF` / `#FFD166` | Circumferential ring-rivers, axial hydro-canals, central lake basins, cascades | `roughness = 0.08`, `metallic = 0.15`, `specular = 0.85`, `alphaMode = "BLEND"` (alpha `~0.85`) |
| `terrain_basalt_titanium_cliff_rock.png` | `512×512` RGB | Weathered Basalt `#222730` / `#383C44`, Warm Mineral Ochre Strata `#6C655E`, Machined Titanium Ribs `#222830` | Stepped valley retaining cliffs, radial bulkhead Foundations, structural ring-beam embankments | `roughness = 0.68`, `metallic = 0.28` (higher metallic along structural tieback ribs) |
| `terrain_park_promenade_paving.png` | `512×512` RGB | Warm Travertine-Alloy `#B8B5AE` / `#C9C5BC`, Carbon-Slate Seams `#2C323C`, Warm Amber Boulevard Inlays `#FFA518` | Valley floor pedestrian boulevards, waterfront boardwalks, mid-ring plaza overlooks, transit decks | `roughness = 0.42`, `metallic = 0.18`, emissive multiplier `1.5` on amber/cyan lane inlays |
| `window_clusters_warm_amber_vs_cool_industrial.png` | `512×512` RGB | **Left UV (`u < 0.5`):** Warm Circadian Amber/Gold `#FFE0A3` / `#FFA22A` + Botanical `#74C69D`<br>**Right UV (`u >= 0.5`):** Cool Telemetry Cyan `#28E0FF`, UV-Violet `#8A6CFF`, Signal Orange `#FF7D2A` | Residential/Civic terraced mid-rises (`u: 0.0–0.5`) vs. Research/Command/Starport industrial towers (`u: 0.5–1.0`) | Base spandrel `roughness = 0.35`, `metallic = 0.65`; window cells `emission_energy = 2.2` |
| `sky_axial_golden_hour_gradient.png` | `512×512` RGB | Axial Sun Core `#FFF3B0` / `#FFB703` / `#FB8500` transitioning into Cerulean Aerial Haze `#4895EF` / `#1D3557` | Axial Solar Spine diffuser sheath, volumetric sun-shaft cards, and WorldEnvironment sky/reflection backdrop | Unshaded / Emissive (`emission_energy = 2.8` on axial core; `0.35` ambient sky contribution) |

---

## 3. Overhauled Color Palette & Zonal Material Assignment (Breaking the 3-Valley Monotony)

To eliminate visual repetition across the three $120^\circ$ land valleys and three solarium/river strips, each sector receives a distinct material temperature and architectural rhythm while staying unified under the **Aegis-7 65/35 Split-Mass Standard**:

### 3.1 The Three $120^\circ$ Habitat Valleys (Distinct Biome & Window Signatures)
1. **Valley A ($0^\circ$ — Bottom Civic & Terraced Botanical Promenade):**
   - **Ground & Terraces:** Lush tiered greenery (`biome_terraced_botanical_canopy.png`) stepped up weathered basalt/titanium cliffs (`terrain_basalt_titanium_cliff_rock.png`) flanking a wide central pedestrian boulevard (`terrain_park_promenade_paving.png`) and meandering ring-river (`water_ring_river_specular.png`).
   - **Building Palette:** Warm Titanium-Alabaster (`#E2DFD7`) and Brushed Champagne-Bronze (`#B89F7D`) upper tiers (`65%`) over Dark Basalt-Slate (`#222730`) podiums (`35%`), using **Warm Circadian Amber/Gold Windows** (`u: 0.0–0.5` of `window_clusters_warm_amber_vs_cool_industrial.png`).
2. **Valley B ($120^\circ$ — Port-Side Agrarian Arboretum & Hydro-Basin Terraces):**
   - **Ground & Terraces:** Dominated by stepped botanical orchard terraces (`#2D6A4F` / `#52B788`), wide ring-river reservoirs and aquaculture canals (`water_ring_river_specular.png`), and warm copper-anodized irrigation bridges (`#C87D55`).
   - **Building Palette:** Low-rise terraced biodomes and agro-towers with soft circadian gold (`#FFE0A3`) and emerald-tinted (`#74C69D`) greenhouse glazing.
3. **Valley C ($240^\circ$ — Starboard High-Tech Research, Command & Transit Ridge):**
   - **Ground & Terraces:** Exposed basalt-titanium cliff terraces (`terrain_basalt_titanium_cliff_rock.png`) and multi-level transit plazas (`terrain_park_promenade_paving.png`).
   - **Building Palette:** Brushed Silver-Alloy (`#D0D7E0`) and Anodized Cobalt-Slate (`#2B3A4E`) towers using **Cool Telemetry Cyan, UV-Violet & Signal-Orange Windows** (`u: 0.5–1.0` of `window_clusters_warm_amber_vs_cool_industrial.png`).

---

## 4. Godot 4 Lighting, Axial Sun & Volumetric Aerial-Perspective Spec (For Gage)

To convey the true **400m diameter (`R = 200m`) and 800m length** in `/workspace/game-project/godot/renders/cylinder_interior/cylinder_interior_showcase_sheet.png`, replace the flat cyan lighting with a warm golden-hour circadian sun + cool sky scatter + volumetric aerial depth setup:

### 4.1 Axial Solar Spine (`AxialSolarLightRig`)
- **Visual Mesh Material:** Replace solid `#00FFFF` cyan emission on the central spine with `sky_axial_golden_hour_gradient.png` + warm solar core emission (`#FFD166` / `#FFA62B`, `emission_energy_multiplier = 3.2`) along the `640m` habitat drum, transitioning to cool Starport Approach beacons (`#00E5FF` / `#FF7B29`) only inside the `160m` Aft Zero-G Starport Throat.
- **Primary Directional / Omni Sun Sources:**
  - **Key Axial Sun (`DirectionalLight3D` or arrayed `OmniLight3D` nodes along $r = 0, z \in [-300, +300]$):**
    - Color: **Warm Golden-Hour Sunlight `#FFE3B3`** (`RGB(1.0, 0.89, 0.70)`)
    - Energy: `1.65` (Directional) / `2.4` (Omni array with `omni_range = 320.0`, `omni_attenuation = 0.85`)
    - Shadows: `shadow_enabled = true`, `shadow_Softness / blur = 1.5` so buildings and cliffs cast crisp-to-soft cross-valley shadows onto terraced slopes.
  - **Cross-Cylinder Sky Bounce / Counter-Fill (`DirectionalLight3D` or Sky Ambient):**
    - Color: **Soft Cerulean / Botanical Bounce `#68A6C8`** (`RGB(0.41, 0.65, 0.78)`)
    - Energy: `0.45` (lifts shadowed cliff faces so dark `#222730` basalt retains readable detail without washing out golden highlights).

### 4.2 Volumetric Fog & Aerial Perspective Across the 400m Diameter (`WorldEnvironment`)
- **Background / Ambient Light:**
  - `background_mode = BG_SKY` (using `sky_axial_golden_hour_gradient.png` or `ProceduralSkyMaterial` with `sky_top_color = #233D5B`, `sky_horizon_color = #E8B878`, `ground_horizon_color = #5E8C76`, `ground_bottom_color = #1E2D38`).
  - `ambient_light_source = AMBIENT_SOURCE_SKY`, `ambient_light_sky_contribution = 0.55`, `ambient_light_energy = 0.65`.
- **Depth / Aerial Perspective Fog (Crucial for 400m Cross-Cylinder Scale):**
  - `fog_enabled = true`
  - `fog_light_color = Color(0.58, 0.72, 0.84)` (Soft warm-cerulean atmospheric scatter)
  - `fog_light_energy = 0.42`
  - `fog_sun_scatter = 0.38` (Creates warm golden forward-scatter haloes around the central Axial Solar Spine)
  - `fog_density = 0.0014` (Calibrated so foreground promenade at `0–60m` is razor-sharp, mid-ring terraces at `120–200m` pick up ~18% atmospheric veil, and the overhead ceiling city at `350–400m` and far `800m` endcap recede into a cinematic hazy blue-gold aerial perspective).
- **Volumetric Fog & Glow (Post-Processing):**
  - `volumetric_fog_enabled = true`, `volumetric_fog_density = 0.0022`, `volumetric_fog_albedo = Color(0.92, 0.86, 0.76)`, `volumetric_fog_emission = Color(0.10, 0.16, 0.22)`, `volumetric_fog_anisotropy = 0.55` (produces subtle crepuscular sun-rays radiating from the central solar spine past the overhead suspension bridges and tower silhouettes).
  - `glow_enabled = true`, `glow_intensity = 0.55`, `glow_bloom = 0.12`, `glow_hdr_threshold = 1.15` (soft halation on warm amber residential windows, specular river reflections, and the golden axial spine).
  - `tonemap_mode = TONEMAPPER_ACES`, `tonemap_exposure = 1.05`, `ssao_enabled = true` (`ssao_radius = 2.5`, `ssao_intensity = 1.8`), `ssr_enabled = true` (for live reflections of warm amber towers and green terraces in the `water_ring_river_specular.png` canals).
