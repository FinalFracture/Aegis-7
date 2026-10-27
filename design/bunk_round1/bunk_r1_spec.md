# Sci-Fi Bunk Pod — Round 1 Design, Sculpting, Texture & Lighting Specification
**Project:** *Cylinder Hab-7* (800m × 400m O'Neill Cylinder Space Habitat)  
**Pipeline Stage:** Prop Variation Tournament — Round 1 of 4 (`bunk_r1_01` through `bunk_r1_10`)  
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Teams:** Rook (3D Sculpting & UV Mapping) & Gage (Godot 4 Scene Integration, Lighting & Beauty Renders)

---

## 1. Shared Standards & Technical Rules for All 10 Bunk Attempts

### 1.1 Output Paths & Naming Convention
- **3D Models (`.glb`):** `/workspace/game-project/assets/glb/bunk_round1/bunk_r1_01.glb` through `/workspace/game-project/assets/glb/bunk_round1/bunk_r1_10.glb`
- **Texture Library (`.png`):** `/workspace/game-project/assets/textures/bunk_round1/` (16 custom 1024×1024 textures listed in Section 2)
- **Individual Beauty Renders (`.png`):** `/workspace/game-project/assets/renders/bunk_round1/bunk_r1_01.png` through `bunk_r1_10.png`
- **10-Panel Tournament Voting Sheet:** `/workspace/game-project/assets/renders/bunk_round1/bunk_round1_voting_sheet.png`

### 1.2 Target Footprint, Scale & Pivot Orientation
- **Units:** `1.0 unit = 1.0 meter` (Godot 4 standard metric scale).
- **Bounding Box Envelope:**
  - **Width (`X` axis):** `2.15m – 2.30m` (spanning from `X = -1.10m` head-end to `X = +1.10m` foot-end).
  - **Depth (`Z` axis):** `1.10m – 1.35m` (spanning from `Z = -0.60m` rear bulkhead wall to `Z = +0.60m` front alcove opening; `bunk_r1_08` conversation pit extends forward steps to `Z = +0.75m`).
  - **Height (`Y` axis):** `2.00m – 2.35m` (`Y = 0.00m` floor level to `Y = 2.00m–2.35m` upper crown/arch).
- **World Origin & Pivot Point:**
  - Every `.glb` root node MUST have its origin at **Bottom-Center (`X = 0.0, Y = 0.0, Z = 0.0`)**, resting flush on the `Y = 0` floor plane.
  - **Front Orientation (`+Z` Forward):** The open entry side of the bunk alcove faces **`+Z`**, the rear bulkhead wall is at **`-Z`**, the **Headboard / Pillow End** is at **`-X` (Left)**, and the **Foot End** is at **`+X` (Right)**. This ensures all 10 bunks frame identically in the tournament camera rig.

### 1.3 Polygon Budget & Performance Target
- **Triangle Budget:** **`2,200 – 5,500 triangles`** per complete hero bunk asset (realistic medium-detail 3D tailored for low-end PCs).
- **UV Unwrapping Rules:**
  - All meshes must carry clean, non-overlapping or intentionally tiled `UV0` coordinates.
  - Align wood grain UVs along the long axis of timber rails/beams; align tambour slats horizontally (`U` along width, `V` perpendicular across slats); map `crt_telemetry_panel.png` and `oneill_solarium_vista.png` using specific UV sub-quadrants or 0–1 bounds as detailed below.

### 1.4 Strict Anti-Boxy / Organic Modeling Rules for Rook
Never use raw unmodified box primitives. Every bunk candidate must exhibit tactile, sculpted silhouettes:
1. **Structural Shells & Arches:** All fiberglass pods, recessed niches, and bulkhead frames must use **multi-segment bevels/chamfers (4–8 segments)**, stadium curves, or lathe/revolve arches (`16–32` radial segments).
2. **Sculpted Organic Pillows & Bolsters:** Pillows must have pinched/tapered corners, puffed center bellies, subtle center head-indentation creases, and natural resting tilt against headboards (`12×12`+ subdivided grid with sinusoidal/radial vertex deformation).
3. **Draped Quilts, Duvets & Blankets:** Bedding must drape organically over the front mattress edge (`+Z` face) with soft sinusoidal cloth folds, tucked corners, and layered throw blanket overhangs—never a flat rectangular slab.
4. **Tufted Upholstery & Bumpers:** Diamond-tufted headboards (`01`, `10`) and wrap-around velour bumpers (`06`, `08`) must have physical vertex dimpling/arc curvature to catch grazing light alongside the normal/albedo maps.
5. **Spline Tubing, Ladders & Trailing Vines:** Use smooth 3D spline extrusions (`8–12` sides per tube cross-section) for gooseneck lamps, bent chrome cantilever struts, zero-G roll bars, asymmetric crew ladders, and trailing hydroponic vine stalks.

---

## 1A. URGENT TEXTURE DIRECTION UPDATE (Jared Feedback — Clean, Calm & Understated)
- **Zero Busy 2D Patterns:** All textures in `/workspace/game-project/assets/textures/bunk_round1/` and studio/room textures in `/workspace/game-project/assets/textures/` have been regenerated as **clean, calm, understated, low-contrast surfaces (`<1.5%–2.5%` micro-grain/weave variation)**.
- **3D Geometry Carries the Form:** There are **NO painted-on stripes, NO diamond grids, NO dark tambour grooves, NO riveted seam lines, and NO high-contrast geometric wallpaper or parquet lines**. All tufting, baffles, slats, ribs, and cloth folds come purely from Rook's 3D geometry and Gage's lighting/shadows.
- **Studio Backdrop & Floor:** `wallpaper_retro_geometric.png` is now a calm architectural matte off-white plaster (`#EAE4D8`, `<1.5%` micro-texture), and `wood_parquet_warm.png` is a calm, low-contrast warm walnut-oak floor (`#7A5C43`, `<2.5%` gentle grain).

## 2. Texture Library Manifest (`/workspace/game-project/assets/textures/bunk_round1/`)

All 16 textures are generated at **1024×1024 PNG (RGB)** and verified in `/workspace/game-project/assets/textures/bunk_round1/`.

| # | Filename | Primary Material Description | UV Tiling Scale | Roughness | Metallic | Emission / Notes |
|---|----------|------------------------------|-----------------|-----------|----------|------------------|
| 1 | `fiberglass_cream_shell.png` | 70s molded ABS/fiberglass cream-white shell with satin variation, panel seams & warm patina | `1.0 × 1.0` (or `2.0 × 2.0`) | `0.32` | `0.02` | None (high specular clearcoat feel) |
| 2 | `leatherette_tufted_cognac.png` | Deeply diamond-tufted cognac/amber leatherette upholstery with button dimples & pebble grain | `1.5 × 1.0` | `0.48` | `0.00` | None |
| 3 | `quilted_duvet_orange_cream.png` | Cassette-futurism baffled orange & warm cream ripstop duvet with stitch channels & puff shading | `1.0 × 1.0` | `0.68` | `0.00` | UV `V: 0.68–0.88` has cream stripe band |
| 4 | `hull_steel_rib_olive.png` | Heavy structural charcoal-olive painted hull steel with riveted ribs & brushed metal edge wear | `1.0 × 1.0` (`2.0` on beams) | `0.45` | `0.65` | None |
| 5 | `acoustic_hex_padding.png` | Perforated & beveled octagonal acoustic bulkhead wall tiles in warm slate-taupe | `2.0 × 1.5` | `0.82` | `0.00` | None |
| 6 | `canvas_military_olive.png` | Heavyweight olive-drab & khaki utility duck canvas weave with organic rumple shading | `1.0 × 1.0` | `0.85` | `0.00` | UV `V: 0.82–0.90` has khaki web stripe |
| 7 | `wood_teak_tambour_slats.png` | Mid-century warm teak slatted tambour shutter with per-slat grain & dark shadow grooves | `1.0 × 1.0` (`V` across slats) | `0.42` | `0.00` | 32 horizontal slats per `V` tile |
| 8 | `wood_walnut_warm.png` | Rich architectural walnut/teak timber with cathedral figure & warm satin varnish | `1.0 × 1.0` (`2.0` on frames) | `0.38` | `0.00` | Grain runs along `Y`/`V` axis |
| 9 | `waffle_knit_ochre_throw.png` | Deep tactile honeycomb waffle-knit throw blanket in harvest ochre / mustard gold | `1.5 × 1.5` | `0.88` | `0.00` | High tactile relief shading |
| 10 | `velour_terracotta_plush.png` | Lush mid-century corduroy/velour upholstery in burnt terracotta & rust with welt piping | `1.5 × 1.0` | `0.78` | `0.00` | 4 horizontal bolster bands per `V` tile |
| 11 | `linen_botanical_oatmeal.png` | Unbleached organic oatmeal/flax slub linen bedding with woven sage accent stripe | `1.0 × 1.0` | `0.84` | `0.00` | UV `V: 0.78–0.89` has sage trim band |
| 12 | `foliage_hydro_vines.png` | Dense variegated emerald/jade pothos & philodendron leaf canopy with bright venation | `1.5 × 1.5` | `0.52` | `0.00` | Use on planter bed & leaf cluster cards |
| 13 | `metal_brushed_brass_trim.png` | Anisotropic brushed warm brass & bronze hardware for arch frames, sconces & grab bars | `1.0 × 1.0` | `0.26` | `0.88` | Warm gold metallic sheen |
| 14 | `metal_chrome_anodized.png` | Sleek brushed chrome / satin anodized aluminum for cantilevered tracks, ladders & roll bars | `1.0 × 1.0` | `0.22` | `0.90` | Cool silver-steel metallic sheen |
| 15 | `crt_telemetry_panel.png` | 4-quadrant cassette-futurism telemetry atlas: Q1 Amber CRT (`U:0–0.5, V:0–0.5`), Q2 Green CRT (`U:0.5–1, V:0–0.5`), Q3 Backlit Switches (`U:0–0.5, V:0.5–1`), Q4 Amber Diffuser & LED Bars (`U:0.5–1, V:0.5–1`) | Atlas (`0–1` sub-UVs) | `0.20` | `0.15` | Enable **Emission** (`energy = 1.8–2.5`) using same texture as `emission_texture` |
| 16 | `oneill_solarium_vista.png` | Exterior panoramic viewport vista of the 800m × 400m O'Neill cylinder curving green farmland, river ribbon & axial sun | `1.0 × 1.0` (0–1 fit) | `0.15` | `0.00` | Enable **Emission** (`energy = 1.4`) to simulate sunlit exterior daylight |

---

## 3. Detailed Per-Attempt Specifications (`bunk_r1_01` through `bunk_r1_10`)

---

### Attempt 01: `bunk_r1_01` (`01_cassette_capsule`) — 70s Molded Fiberglass Capsule Pod
*Inspired by 1970s Nakagin Capsule Tower & Syd Mead orbital crew pods.*

- **Color Palette (Hex Codes):**
  - Primary Shell: Warm Molded Cream `#EEE5D2`
  - Interior Upholstered Lining: Deep Cognac Amber `#A8562A`
  - Primary Bedding / Duvet: International Cassette Orange `#DA6026` & Cream Band `#ECE0C6`
  - Hardware & Bezel Trim: Brushed Anodized Chrome `#CED4DC`
  - Emissive Practical Accent: Warm Amber Strip & Telemetry CRT `#FFB024`
- **Surface Materials & Texture Assignments:**
  - `Outer_Capsule_Shell` & `Rounded_Stadium_Lip`: `fiberglass_cream_shell.png` (`roughness: 0.30`, `metallic: 0.02`)
  - `Headboard_Tufted_Wall` & `Inner_Backwall_Pad`: `leatherette_tufted_cognac.png` (`roughness: 0.48`, `metallic: 0.0`)
  - `Mattress_Base` & `Plumped_Pillows`: `linen_botanical_oatmeal.png` (`roughness: 0.82`)
  - `Baffled_Duvet_Quilt`: `quilted_duvet_orange_cream.png` (`roughness: 0.68`, mapped so the cream stripe band sits near the folded top edge)
  - `Telemetry_Console_Faceplate`: `crt_telemetry_panel.png` (UV mapped to Quadrant 1 Amber Bio-Telemetry `U:0.0–0.5, V:0.0–0.5` + Quadrant 3 Rocker Switches `U:0.0–0.5, V:0.5–1.0`, `emission_enabled: true`, `emission_energy: 2.2`)
  - `Grab_Rail_And_Vents`: `metal_chrome_anodized.png` (`roughness: 0.22`, `metallic: 0.90`)
- **Organic Shape & Sculpting Brief for Rook:**
  - Sculpt a monocoque fiberglass shell (`2.20m × 1.20m × 2.05m`) with a sweeping **stadium-oval front opening** (`R = 0.42m` corner fillets) and a thick rolled lip bezel (`0.08m` radius tube along the stadium perimeter).
  - Inside the left (`-X`) wall, build a **curved, concave diamond-tufted headboard** with physical vertex cushioning.
  - Sculpt a plush mattress (`Y = 0.48m` top surface) topped with **two pinched-corner ergonomic pillows** and a **thick baffled duvet** that drapes 0.22m down the front edge with 5 sinusoidal cloth waves.
  - Embed a canted **side telemetry control recess** on the rear wall (`Z = -0.52m, Y = 0.95m`) and a recessed storage drawer curve under the bed base.
- **3-Point + Practical Emissive Lighting Rig (Gage / Rook):**
  - **Key Light (`DirectionalLight3D` or `SpotLight3D`):** Pos `(2.4, 2.8, 2.6)` looking at `(0.0, 0.9, 0.0)`, Color `#FFF1E0` (4200K warm studio), Energy `1.35`, Shadow Blur `1.5`.
  - **Fill Light:** Pos `(-2.5, 1.6, 2.2)`, Color `#C8D8F0` (cool habitat skylight bounce), Energy `0.45`.
  - **Rim / Back Light:** Pos `(-1.8, 2.6, -1.6)`, Color `#FFD2A6`, Energy `0.85` (highlights curved fiberglass shoulder).
  - **Practical Lights (Inside Alcove):**
    1. `Practical_Amber_Strip` (`OmniLight3D`): Local Pos `(0.00, 1.68, -0.15)`, Color `#FF9E2C` (2400K amber), Energy `1.65`, Range `2.2m`, Attenuation `1.4` + emissive strip mesh (`emission_energy: 3.2`).
    2. `Practical_CRT_Glow` (`OmniLight3D`): Local Pos `(0.35, 0.98, -0.42)`, Color `#FFB838`, Energy `0.65`, Range `1.1m`.

---

### Attempt 02: `bunk_r1_02` (`02_bulkhead_berth`) — Industrial Hull-Rib Recessed Berth
*Heavy structural O'Neill cylinder pressure-hull framing paired with warm brass marine fixtures.*

- **Color Palette (Hex Codes):**
  - Primary Structural Ribs: Industrial Hull Olive-Charcoal `#424A3C`
  - Interior Acoustic Tiles: Warm Slate-Taupe `#7C7872`
  - Blanket & Bedding: Military Olive Drab `#626848` & Khaki Hem `#9A906C`
  - Hardware & Sconce Cage: Brushed Marine Brass `#CCA254`
  - Emissive Practical Accent: Warm Caged Tungsten `#FFAE42`
- **Surface Materials & Texture Assignments:**
  - `Curved_IBeam_Hull_Ribs` & `Lower_Bulkhead_Drawer_Fronts`: `hull_steel_rib_olive.png` (`roughness: 0.45`, `metallic: 0.65`)
  - `Recessed_Backwall_Acoustic_Panels`: `acoustic_hex_padding.png` (`roughness: 0.82`, `metallic: 0.0`, UV tiled `2.5 × 1.5`)
  - `Rumpled_Canvas_Blanket`: `canvas_military_olive.png` (`roughness: 0.85`)
  - `Mattress_Sheet_And_Bolster`: `linen_botanical_oatmeal.png` (`roughness: 0.84`)
  - `Brass_Grab_Handles` & `Caged_Sconce_Guard`: `metal_brushed_brass_trim.png` (`roughness: 0.26`, `metallic: 0.88`)
  - `Vent_Louvers_And_Latches`: `metal_chrome_anodized.png` (`roughness: 0.28`, `metallic: 0.85`)
- **Organic Shape & Sculpting Brief for Rook:**
  - Frame the left (`X = -1.05m`) and right (`X = +1.05m`) sides with **massive curved C-channel / I-beam structural ribs** that curve inward at the top (`Y = 1.65m` to `2.15m`) matching the 400m cylinder hull curvature, complete with gusset brackets.
  - Line the interior rear and side walls with segmented padded acoustic panels.
  - Sculpt a rugged crew mattress (`Y = 0.52m`) with a **heavyweight canvas blanket showing pronounced diagonal rumple ridges and folded-back top corner**, plus two plump cylindrical/rectangular crew pillows.
  - Model a **bent tubular brass grab-handle** (`R = 0.018m` spline tube) on the left rib and an **industrial wire-caged bulkhead sconce** at the head wall (`X = -0.88m, Y = 1.25m, Z = -0.35m`).
  - Under the berth (`Y = 0.0m–0.44m`), model two recessed angled cargo lockers with T-handle latches.
- **3-Point + Practical Emissive Lighting Rig (Gage / Rook):**
  - **Key Light:** Pos `(2.2, 2.6, 2.5)`, Color `#FFE8C8`, Energy `1.25`, Shadow Blur `1.4`.
  - **Fill Light:** Pos `(-2.4, 1.5, 2.0)`, Color `#9EB4C8` (cool steel bay ambient), Energy `0.40`.
  - **Rim / Back Light:** Pos `(1.9, 2.7, -1.5)`, Color `#FFBE78`, Energy `0.95` (grazes the riveted olive I-beam flanges).
  - **Practical Lights (Inside Alcove):**
    1. `Practical_Caged_Sconce` (`OmniLight3D`): Local Pos `(-0.82, 1.22, -0.30)`, Color `#FFA834` (2500K tungsten bulb), Energy `1.85`, Range `2.4m`, Attenuation `1.5` + glowing bulb core mesh (`emission: #FFD888`, `energy: 4.0`).
    2. `Practical_Underberth_Strip` (`OmniLight3D`): Local Pos `(0.0, 0.14, 0.48)`, Color `#FF8C24`, Energy `0.55`, Range `1.2m`.

---

### Attempt 03: `bunk_r1_03` (`03_cantilever_couchette`) — Suspended Cantilever Couchette
*Mid-century modern Dieter Rams / architectural floating timber-and-chrome couchette.*

- **Color Palette (Hex Codes):**
  - Cantilevered Bed Frame & Wall Slat Backing: Warm Satin Walnut `#7A4A2A` & Teak `#9E6034`
  - Vertical Wall Tracks & Cantilever Struts: Brushed Anodized Chrome `#D0D6DE`
  - Primary Throw Blanket: Harvest Ochre Waffle-Knit `#D89A2A`
  - Mattress & Overstuffed Bolster: Oatmeal Flax Linen `#E0D5C0`
  - Emissive Practical Accent: Twin Warm Halogen Goosenecks `#FFE09E`
- **Surface Materials & Texture Assignments:**
  - `Floating_Walnut_Bed_Tray` & `Floating_Nightstand_Wing`: `wood_walnut_warm.png` (`roughness: 0.36`, `metallic: 0.0`)
  - `Rear_Accent_Wall_Panel`: `wood_teak_tambour_slats.png` (`roughness: 0.42`, `metallic: 0.0`)
  - `Bulkhead_Mounting_Tracks`, `Cantilever_Support_Tubes` & `Gooseneck_Stems`: `metal_chrome_anodized.png` (`roughness: 0.20`, `metallic: 0.92`)
  - `Draped_Waffle_Throw`: `waffle_knit_ochre_throw.png` (`roughness: 0.88`)
  - `Mattress_Core` & `Cylindrical_Bolster_Pillow`: `linen_botanical_oatmeal.png` (`roughness: 0.84`)
  - `Lamp_Shade_Trim_Rings`: `metal_brushed_brass_trim.png` (`roughness: 0.25`, `metallic: 0.88`)
- **Organic Shape & Sculpting Brief for Rook:**
  - Create **two vertical machined chrome wall tracks** at `X = -0.85m` and `X = +0.85m` (`Z = -0.52m`) with curved diagonal **swept tubular chrome cantilever arms** that suspend the bed platform at `Y = 0.46m` with completely open floor clearance underneath (`Y = 0.0m–0.38m` open air).
  - Sculpt the **floating walnut bed tray** with rounded boat-hull bottom edges (`0.06m` bevel radius) and an integrated cantilevered side shelf.
  - Place a **long overstuffed cylindrical bolster pillow** (`R = 0.14m`, cinched ends) + two angled rest pillows at `-X`, and a **thick ochre waffle-knit throw blanket** draped asymmetrically across the foot/middle of the mattress with natural hanging folds.
  - Sculpt **twin flexible spline gooseneck reading lamps** curving out from the upper headboard wall (`Y = 1.35m, X = -0.88m, Z = -0.35m` and `-0.10m`) with conical spun-brass/chrome shades aimed at the pillows.
- **3-Point + Practical Emissive Lighting Rig (Gage / Rook):**
  - **Key Light:** Pos `(2.3, 2.7, 2.6)`, Color `#FFF4E4`, Energy `1.35`, Shadow Blur `1.6` (casts crisp floating shadow under the cantilevered bed).
  - **Fill Light:** Pos `(-2.3, 1.4, 2.2)`, Color `#D4E2F4`, Energy `0.50`.
  - **Rim / Back Light:** Pos `(0.0, 2.8, -1.8)`, Color `#FFE2B8`, Energy `0.80`.
  - **Practical Lights (Inside Alcove):**
    1. `Practical_Gooseneck_Spot_A` (`SpotLight3D` or `OmniLight3D`): Local Pos `(-0.75, 1.24, -0.22)` aimed at `(-0.55, 0.65, -0.05)`, Color `#FFE09E` (3000K halogen), Energy `1.70`, Range `2.0m`.
    2. `Practical_Gooseneck_Spot_B` (`OmniLight3D`): Local Pos `(-0.75, 1.24, 0.12)`, Color `#FFD88A`, Energy `1.35`, Range `1.8m`.

---

### Attempt 04: `bunk_r1_04` (`04_privacy_shutter_pod`) — Tambour Roll-Top Privacy Pod
*Cozy enclosed capsule with a curved slatted teak tambour roll-top door half-drawn.*

- **Color Palette (Hex Codes):**
  - Outer Pod Shell: Molded Satin Cream `#EDE4D0`
  - Tambour Roll-Top Shutter: Mid-Century Teak `#9E6034` with Deep Groove `#1C120C`
  - Contoured Mattress & Pillows: Natural Oatmeal Linen `#E0D5C0` & Sage Accent `#708A68`
  - Shutter Guide Tracks & Handle Bar: Brushed Brass `#CCA254`
  - Emissive Practical Accent: Phosphor-Green CRT `#5CFF8A` & Warm Ceiling Cove `#FFB84D`
- **Surface Materials & Texture Assignments:**
  - `Curved_Pod_Housing`: `fiberglass_cream_shell.png` (`roughness: 0.32`, `metallic: 0.02`)
  - `Curved_Tambour_Shutter_Door`: `wood_teak_tambour_slats.png` (`roughness: 0.40`, `metallic: 0.0`, UV mapped so the 32 slats run horizontally along the shutter width)
  - `Ergonomic_Wave_Mattress` & `Dual_Plumped_Pillows`: `linen_botanical_oatmeal.png` (`roughness: 0.84`)
  - `Folded_Foot_Duvet`: `quilted_duvet_orange_cream.png` (`roughness: 0.68`)
  - `Recessed_CRT_Micro_Monitor`: `crt_telemetry_panel.png` (UV mapped to **Quadrant 2 Phosphor-Green Radar** `U:0.5–1.0, V:0.0–0.5`, `emission_enabled: true`, `emission_energy: 2.4`)
  - `Shutter_Track_Trim` & `Pull_Handle`: `metal_brushed_brass_trim.png` (`roughness: 0.26`, `metallic: 0.88`)
- **Organic Shape & Sculpting Brief for Rook:**
  - Build a curved hood-profile sleep pod (`2.20m × 1.25m × 2.10m`) whose upper front canopy curves along a smooth quarter-cylinder arc (`R = 0.65m` from `Y = 1.35m` to `Y = 2.05m`).
  - Model the **half-drawn slatted tambour shutter** following that exact curved track from the top crown down to `Y = 1.28m` across the front opening, complete with a brass grab handle bar on its bottom slat so the viewer still sees clearly into the cozy lit interior below `Y = 1.28m`.
  - Sculpt an **ergonomic S-curve contoured mattress** (slightly raised knee bolster and inclined head rest) with **two plump pillows** (`-X`) and a neatly folded quilted foot blanket (`+X`).
  - Tuck a **recessed angled CRT status micro-monitor** into the inner back wall (`X = -0.35m, Y = 1.02m, Z = -0.48m`).
- **3-Point + Practical Emissive Lighting Rig (Gage / Rook):**
  - **Key Light:** Pos `(2.2, 2.3, 2.7)`, Color `#FFF0DC`, Energy `1.30`, Shadow Blur `1.5`.
  - **Fill Light:** Pos `(-2.4, 1.5, 2.1)`, Color `#C4D8EC`, Energy `0.45`.
  - **Rim / Back Light:** Pos `(1.6, 2.5, -1.6)`, Color `#FFD49E`, Energy `0.85`.
  - **Practical Lights (Inside Alcove):**
    1. `Practical_Hidden_Shutter_Cove` (`OmniLight3D`): Local Pos `(0.0, 1.48, -0.10)`, Color `#FFB444` (2600K warm cove), Energy `1.75`, Range `2.1m`.
    2. `Practical_Green_CRT_Light` (`OmniLight3D`): Local Pos `(-0.35, 1.02, -0.38)`, Color `#5CFF8A` (phosphor green accent), Energy `0.75`, Range `1.1m`.

---

### Attempt 05: `bunk_r1_05` (`05_zero_g_conversion_bunk`) — Spin-Down Hybrid Restraint Bunk
*Engineered for Cylinder Hab-7 spin-down maintenance cycles—padded roll bars + quilted restraint sleep sack.*

- **Color Palette (Hex Codes):**
  - Molded Bay Shell: Satin Cream-White `#EEE5D2`
  - Padded Bulkhead Back & Cubbies: Acoustic Slate-Taupe `#7C7872`
  - Quilted Sleep Sack & Restraint Pads: Cassette Orange `#DA6026` & Cream `#ECE0C6`
  - Restraint Straps & Buckles: Olive Webbing `#626848` & Anodized Chrome `#CED4DC`
  - Emissive Practical Accent: Warm Indirect Cove & Telemetry Bar `#FFAA32`
- **Surface Materials & Texture Assignments:**
  - `Upper_And_Lower_Molded_Bays`: `fiberglass_cream_shell.png` (`roughness: 0.34`, `metallic: 0.02`)
  - `Interior_Impact_Padding`: `acoustic_hex_padding.png` (`roughness: 0.80`, `metallic: 0.0`)
  - `Quilted_Sleep_Sack_Cocoon` & `Roll_Bar_Foam_Sleeves`: `quilted_duvet_orange_cream.png` (`roughness: 0.65`)
  - `Restraint_Webbing_Straps`: `canvas_military_olive.png` (`roughness: 0.82`)
  - `Tubular_Roll_Bars` & `Quick_Release_Buckles`: `metal_chrome_anodized.png` (`roughness: 0.22`, `metallic: 0.90`)
  - `Spin_Gravity_Status_Panel`: `crt_telemetry_panel.png` (Quadrant 1 + Quadrant 4 LED bar array, `emission_enabled: true`, `emission_energy: 2.2`)
- **Organic Shape & Sculpting Brief for Rook:**
  - Construct a padded orbital berth featuring **two curved tubular safety roll-bars** (`R = 0.032m` chrome spline tubes wrapped in thick `R = 0.055m` segmented orange/cream foam bolsters) arcing across the front entry at `X = -0.45m` and `X = +0.45m`.
  - Sculpt a **contoured quilted sleep-sack cocoon** on the mattress with a folded-open top flap, **three organic curved fabric restraint straps** arching over the sleep sack with metallic quick-release center buckles, and a sculpted neck-cradle pillow.
  - Carve **three rounded recessed storage cubbies** with elastic retention nets/bars into the rear bulkhead wall (`Y = 1.25m`).
- **3-Point + Practical Emissive Lighting Rig (Gage / Rook):**
  - **Key Light:** Pos `(2.3, 2.6, 2.5)`, Color `#FFF2E2`, Energy `1.30`, Shadow Blur `1.4`.
  - **Fill Light:** Pos `(-2.5, 1.6, 2.2)`, Color `#C2D6EE`, Energy `0.48`.
  - **Rim / Back Light:** Pos `(-1.6, 2.7, -1.7)`, Color `#FFC890`, Energy `0.85`.
  - **Practical Lights (Inside Alcove):**
    1. `Practical_Indirect_Cove_Upper` (`OmniLight3D`): Local Pos `(-0.25, 1.72, -0.25)`, Color `#FFA830`, Energy `1.60`, Range `2.2m`.
    2. `Practical_Cubby_Glow` (`OmniLight3D`): Local Pos `(0.45, 1.25, -0.40)`, Color `#FFBE48`, Energy `0.85`, Range `1.3m`.

---

### Attempt 06: `bunk_r1_06` (`06_solarium_window_daybed`) — Viewport-Integrated Alcove Bunk
*Panoramic curved viewport cut right into the bunk backwall looking out across the 800m × 400m O'Neill cylinder.*

- **Color Palette (Hex Codes):**
  - Architectural Alcove Surround: Warm Satin Walnut `#7A4A2A`
  - Plush Daybed Cushions & Bolsters: Burnt Terracotta Velour `#BC5236`
  - Throw Blanket & Pillow Accents: Oatmeal Linen `#E0D5C0` & Ochre `#D89A2A`
  - Viewport Bezel Frame: Brushed Warm Brass `#CCA254`
  - Emissive Practical Accent: Golden Cylinder Sunlight `#FFF2C8` + Reading Spot `#FFB84D`
- **Surface Materials & Texture Assignments:**
  - `Curved_Wood_Alcove_Surround` & `Base_Drawers`: `wood_walnut_warm.png` (`roughness: 0.36`, `metallic: 0.0`)
  - `Deep_Tufted_Daybed_Mattress` & `Wrap_Around_Back_Cushions`: `velour_terracotta_plush.png` (`roughness: 0.78`, `metallic: 0.0`)
  - `Panoramic_Viewport_Glass_Vista`: `oneill_solarium_vista.png` (`roughness: 0.12`, `metallic: 0.0`, `emission_enabled: true`, `emission_energy: 1.45` so the curving green farmland and axial sun glow realistically)
  - `Viewport_Stadium_Bezel` & `Reading_Sconce`: `metal_brushed_brass_trim.png` (`roughness: 0.25`, `metallic: 0.88`)
  - `Tossed_Throw_Pillows`: `linen_botanical_oatmeal.png` & `waffle_knit_ochre_throw.png`
- **Organic Shape & Sculpting Brief for Rook:**
  - Build a warm curved walnut alcove (`2.25m × 1.25m × 2.15m`) whose rear wall (`Z = -0.52m`) features a **large stadium-curved panoramic viewport window (`1.55m wide × 0.85m tall`, centered at `Y = 1.32m`)** framed by a deep beveled brass pressure bezel (`0.09m` depth) and slight concave window recess.
  - Below the viewport (`Y = 0.45m–0.92m`), sculpt **lush, deep-channeled terracotta velour daybed cushions** with a wrap-around U-shaped backrest bolster, **four organically tossed/angled throw pillows**, and a soft draped linen blanket over the front lip.
- **3-Point + Practical Emissive Lighting Rig (Gage / Rook):**
  - **Key Light:** Pos `(2.1, 2.7, 2.5)`, Color `#FFF6E5` (5000K axial solarium daylight), Energy `1.40`, Shadow Blur `1.5`.
  - **Fill Light:** Pos `(-2.3, 1.5, 2.2)`, Color `#CDE6D8` (verdant cylinder farmland bounce), Energy `0.52`.
  - **Rim / Back Light:** Pos `(0.0, 2.2, -1.5)`, Color `#FFF0B8`, Energy `1.10`.
  - **Practical Lights (Inside Alcove):**
    1. `Practical_Viewport_Sun_Glow` (`OmniLight3D`): Local Pos `(0.00, 1.32, -0.32)`, Color `#FFF0C2` (warm axial sunlight streaming through viewport onto terracotta cushions), Energy `1.75`, Range `2.5m`.
    2. `Practical_Reading_Spot` (`OmniLight3D`): Local Pos `(-0.88, 1.45, -0.18)`, Color `#FFB448`, Energy `1.10`, Range `1.6m`.

---

### Attempt 07: `bunk_r1_07` (`07_double_decker_crew_rack`) — Asymmetric Twin Crew Rack
*Lower wide lounge-berth + upper offset sleek sleep pod with bent-tube chrome ladder and gathered privacy curtain.*

- **Color Palette (Hex Codes):**
  - Structural Frame & Lower Bulkhead: Hull Olive-Charcoal `#424A3C`
  - Upper Offset Sleep Pod Shell: Satin Cream Fiberglass `#EEE5D2`
  - Lower Lounge Berth Bedding: Olive Drab Canvas `#626848` & Terracotta Cushion `#BC5236`
  - Upper Berth Bedding & Gathered Curtain: Cassette Orange/Cream `#DA6026` & Oatmeal Linen `#E0D5C0`
  - Bent-Tube Ladder & Curtain Rod: Anodized Chrome `#D0D6DE`
  - Emissive Practical Accent: Dual Alcove Reading Strips `#FFA834`
- **Surface Materials & Texture Assignments:**
  - `Lower_Berth_Frame`: `hull_steel_rib_olive.png` (`roughness: 0.45`, `metallic: 0.65`)
  - `Upper_Offset_Pod_Shell`: `fiberglass_cream_shell.png` (`roughness: 0.32`, `metallic: 0.02`)
  - `Lower_Berth_Mattress_And_Backrest`: `velour_terracotta_plush.png` & `canvas_military_olive.png`
  - `Upper_Berth_Duvet`: `quilted_duvet_orange_cream.png`
  - `Gathered_Privacy_Curtain`: `linen_botanical_oatmeal.png` (`roughness: 0.85`)
  - `Bent_Tube_Ladder_And_Curtain_Rail`: `metal_chrome_anodized.png` (`roughness: 0.22`, `metallic: 0.90`)
  - `Alcove_Status_Panels`: `crt_telemetry_panel.png` (`emission_enabled: true`, `emission_energy: 2.0`)
- **Organic Shape & Sculpting Brief for Rook:**
  - Design an **asymmetric two-tier architecture** (`2.25m wide × 1.30m deep × 2.30m tall`):
    - **Lower Tier (`Y = 0.38m`):** Full-width deep lounge-berth (`2.15m` wide) with an angled sofa-back bolster cushion so it doubles as a daytime settee.
    - **Upper Tier (`Y = 1.38m`):** Offset molded capsule berth (`1.75m` wide, shifted toward `-X`) leaving a dynamic step-up void on the right (`+X`).
  - Sculpt a **continuous bent-tube chrome ladder** (`R = 0.022m` spline with curved top standoffs and non-slip rungs) climbing the right side (`X = +0.62m, Z = +0.52m`).
  - Along the lower berth's left front edge (`X = -1.00m` to `-0.35m`), sculpt a **gathered fabric privacy curtain** with sinusoidal vertical pleat waves and a pinched tie-back strap.
- **3-Point + Practical Emissive Lighting Rig (Gage / Rook):**
  - **Key Light:** Pos `(2.4, 2.8, 2.7)`, Color `#FFF1E0`, Energy `1.35`, Shadow Blur `1.5`.
  - **Fill Light:** Pos `(-2.5, 1.6, 2.2)`, Color `#C4D6EC`, Energy `0.48`.
  - **Rim / Back Light:** Pos `(1.8, 2.8, -1.7)`, Color `#FFD098`, Energy `0.85`.
  - **Practical Lights (Inside Alcove):**
    1. `Practical_Lower_Berth_Light` (`OmniLight3D`): Local Pos `(-0.40, 1.12, -0.25)`, Color `#FFA630`, Energy `1.45`, Range `1.9m`.
    2. `Practical_Upper_Pod_Light` (`OmniLight3D`): Local Pos `(-0.30, 2.02, -0.20)`, Color `#FFBE48`, Energy `1.45`, Range `1.8m`.

---

### Attempt 08: `bunk_r1_08` (`08_conversation_pit_bunk`) — Sunken Step-Up Habitat Bed
*1970s sunken conversation-pit lounge bed set into a raised teak platform with curved steps and wrap-around velour bumpers.*

- **Color Palette (Hex Codes):**
  - Raised Platform & Curved Corner Steps: Architectural Walnut/Teak `#7A4A2A`
  - Wrap-Around Padded Pit Bumpers: Burnt Terracotta Plush Velour `#BC5236`
  - Sunken Mattress & Tossed Pillows: Oatmeal Flax Linen `#E0D5C0` & Ochre Waffle `#D89A2A`
  - Step Trim & Corner Rail: Brushed Brass `#CCA254`
  - Emissive Practical Accent: Warm Under-Step Neon Tube `#FF8E28` & Headboard Cove `#FFC458`
- **Surface Materials & Texture Assignments:**
  - `Raised_Teak_Platform` & `Curved_Corner_Steps`: `wood_walnut_warm.png` (`roughness: 0.36`, `metallic: 0.0`)
  - `Wrap_Around_Velour_Bumper_Rolls`: `velour_terracotta_plush.png` (`roughness: 0.78`, `metallic: 0.0`)
  - `Sunken_Mattress` & `Pillows`: `linen_botanical_oatmeal.png` (`roughness: 0.84`)
  - `Draped_Corner_Throw`: `waffle_knit_ochre_throw.png` (`roughness: 0.88`)
  - `Rear_Slatted_Wall_Screen`: `wood_teak_tambour_slats.png` (`roughness: 0.42`)
  - `Brass_Step_Nosing_And_Sconce`: `metal_brushed_brass_trim.png` (`roughness: 0.25`, `metallic: 0.88`)
- **Organic Shape & Sculpting Brief for Rook:**
  - Build a wide **raised walnut deck platform (`Y = 0.0m` to `Y = 0.44m`)** with **two sweeping quarter-round curved corner steps** at the front-right (`+X, +Z`, `Y = 0.15m` and `Y = 0.30m`) featuring recessed under-lip LED diffuser channels.
  - Surround the mattress well (`Y = 0.44m` to `Y = 0.86m`) with **plump, tubular/bullnose wrap-around terracotta velour bumper bolsters** (`0.22m` thick with rounded miter corners) on the back, left, right, and partial front.
  - Inside the sunken pit, sculpt a plush mattress with **five organically arranged/tilted pillows** and a rumpled ochre waffle throw spilling over the front step edge, backed by a curved walnut slatted headboard screen rising to `Y = 1.95m`.
- **3-Point + Practical Emissive Lighting Rig (Gage / Rook):**
  - **Key Light:** Pos `(2.3, 2.8, 2.6)`, Color `#FFF2DF`, Energy `1.35`, Shadow Blur `1.5`.
  - **Fill Light:** Pos `(-2.4, 1.6, 2.3)`, Color `#D0DCED`, Energy `0.48`.
  - **Rim / Back Light:** Pos `(-1.7, 2.6, -1.6)`, Color `#FFC68A`, Energy `0.85`.
  - **Practical Lights (Inside Alcove):**
    1. `Practical_Understep_Neon` (`OmniLight3D`): Local Pos `(0.65, 0.22, 0.58)`, Color `#FF8E24` (warm amber neon under-step glow), Energy `1.55`, Range `1.8m` + emissive neon tube strips (`emission_energy: 3.5`).
    2. `Practical_Pit_Backwall_Cove` (`OmniLight3D`): Local Pos `(-0.20, 1.35, -0.35)`, Color `#FFBC4C`, Energy `1.50`, Range `2.2m`.

---

### Attempt 09: `bunk_r1_09` (`09_botanical_sleeper`) — Bio-Integrated Hydro-Bunk
*Ecological O'Neill habitat sleep nook with an arched overhead hydroponic planter trough and trailing lush vines.*

- **Color Palette (Hex Codes):**
  - Curved Timber Nook & Planter Trough: Warm Walnut `#7A4A2A` & Cream Inner Liner `#EEE5D2`
  - Hydroponic Foliage & Trailing Vines: Variegated Emerald `#2E7D3B` & Chartreuse Vein `#76B843`
  - Bedding & Pillows: Unbleached Oatmeal Linen `#E0D5C0` with Sage Stripe `#708A68`
  - Irrigation Tubes & Hardware: Brushed Brass `#CCA254`
  - Emissive Practical Accent: Warm Full-Spectrum Grow-Light `#FFE6A8`
- **Surface Materials & Texture Assignments:**
  - `Curved_Walnut_Arch_Frame` & `Hydro_Planter_Trough`: `wood_walnut_warm.png` (`roughness: 0.38`, `metallic: 0.0`)
  - `Interior_Alcove_Backwall`: `fiberglass_cream_shell.png` (`roughness: 0.35`)
  - `Hydroponic_Canopy_Bed` & `Trailing_Leaf_Clusters`: `foliage_hydro_vines.png` (`roughness: 0.50`, `metallic: 0.0`)
  - `Organic_Linen_Mattress`, `Draped_Sheet` & `Pillows`: `linen_botanical_oatmeal.png` (`roughness: 0.84`)
  - `Throw_Blanket_Fold`: `waffle_knit_ochre_throw.png` (`roughness: 0.88`)
  - `Brass_Mist_Pipes_And_Grow_Reflector`: `metal_brushed_brass_trim.png` (`roughness: 0.26`, `metallic: 0.88`)
- **Organic Shape & Sculpting Brief for Rook:**
  - Sculpt a serene arched walnut sleep nook (`2.20m × 1.25m × 2.15m`) featuring an **integrated curved overhead hydroponic planter trough** (`Y = 1.58m–1.85m`) spanning across the front-top arch and wrapping down the right (`+X`) cascading column.
  - Populate the trough with **3D mounded foliage masses and 8–12 trailing 3D vine splines** adorned with angled leaf cluster cards/geometry (`foliage_hydro_vines.png`) cascading organically 0.35m–0.65m down the sides of the bunk opening.
  - Below, sculpt a soft natural linen bed (`Y = 0.48m`) with **draped oatmeal sheets (showing the sage woven band)**, three plump organic pillows, and a brass mist-irrigation tube along the planter rim.
- **3-Point + Practical Emissive Lighting Rig (Gage / Rook):**
  - **Key Light:** Pos `(2.2, 2.7, 2.5)`, Color `#FFF8E8`, Energy `1.35`, Shadow Blur `1.5`.
  - **Fill Light:** Pos `(-2.3, 1.5, 2.2)`, Color `#CFE8D4` (soft botanical chlorophyll bounce), Energy `0.50`.
  - **Rim / Back Light:** Pos `(1.7, 2.7, -1.6)`, Color `#FFE8B0`, Energy `0.85`.
  - **Practical Lights (Inside Alcove):**
    1. `Practical_Hydro_Grow_Light_A` (`OmniLight3D`): Local Pos `(-0.35, 1.65, 0.10)`, Color `#FFE4A0` (3500K warm botanical grow-light filtering through vines), Energy `1.65`, Range `2.3m` + emissive grow-bar strip (`emission_energy: 3.0`).
    2. `Practical_Hydro_Grow_Light_B` (`OmniLight3D`): Local Pos `(0.45, 1.55, 0.15)`, Color `#FFD888`, Energy `1.35`, Range `2.0m`.

---

### Attempt 10: `bunk_r1_10` (`10_officer_stateroom_alcove`) — Executive Stateroom Arch Bed
*Dramatic arched brushed-brass & walnut bulkhead niche with a diamond-tufted curved headboard and twin warm globe sconces.*

- **Color Palette (Hex Codes):**
  - Outer Arch Bulkhead Surround: Rich Architectural Walnut `#7A4A2A`
  - Inner Beveled Arch Liner & Sconce Hardware: Brushed Warm Brass `#CCA254`
  - Curved Diamond-Tufted Headboard: Deep Cognac Leatherette `#A8562A`
  - Layered Bedding: Oatmeal Linen Base `#E0D5C0`, Terracotta Velour Coverlet `#BC5236` & Ochre Waffle Throw `#D89A2A`
  - Emissive Practical Accent: Twin Warm Opal Globe Sconces `#FFD288`
- **Surface Materials & Texture Assignments:**
  - `Monumental_Walnut_Arch_Wall` & `Pedestal_Base`: `wood_walnut_warm.png` (`roughness: 0.34`, `metallic: 0.0`)
  - `Beveled_Brass_Arch_Casing` & `Sconce_Backplates`: `metal_brushed_brass_trim.png` (`roughness: 0.24`, `metallic: 0.90`)
  - `Curved_Diamond_Tufted_Headboard`: `leatherette_tufted_cognac.png` (`roughness: 0.46`, `metallic: 0.0`)
  - `Primary_Mattress_And_Euro_Pillows`: `linen_botanical_oatmeal.png` (`roughness: 0.82`)
  - `Quilted_Velour_Coverlet`: `velour_terracotta_plush.png` (`roughness: 0.76`)
  - `Folded_Ochre_Foot_Throw`: `waffle_knit_ochre_throw.png` (`roughness: 0.88`)
  - `Stateroom_Comms_Panel`: `crt_telemetry_panel.png` (Quadrant 1 + Quadrant 3, `emission_enabled: true`, `emission_energy: 1.8`)
- **Organic Shape & Sculpting Brief for Rook:**
  - Sculpt a **grand barrel-vaulted / stadium-arched walnut & brushed-brass alcove niche** (`2.25m × 1.30m × 2.25m`) with a wide beveled brass inner arch liner (`0.14m` deep chamfered brass reveal).
  - Against the left (`-X`) and curving onto the rear wall, build a **sweeping wrap-around diamond-tufted cognac leatherette headboard** with sculpted button dimples and a brass top rail.
  - Dress the bed with **three layered textiles**: a crisp oatmeal sheet, a draped terracotta velour duvet with soft overhanging waves, and a folded ochre waffle-knit throw across the foot (`+X`), plus **four tiered pillows** (two tall Euro shams + two plump sleeping pillows).
  - Mount **twin mid-century opal-glass globe sconces on curved brass stems** (`R = 0.09m` glowing spheres at `X = -0.85m, Y = 1.35m, Z = -0.35m` and `X = +0.85m, Y = 1.35m, Z = -0.35m`).
- **3-Point + Practical Emissive Lighting Rig (Gage / Rook):**
  - **Key Light:** Pos `(2.3, 2.7, 2.6)`, Color `#FFF1DC`, Energy `1.35`, Shadow Blur `1.5`.
  - **Fill Light:** Pos `(-2.4, 1.5, 2.2)`, Color `#D2DFEE`, Energy `0.45`.
  - **Rim / Back Light:** Pos `(0.0, 2.8, -1.7)`, Color `#FFD699`, Energy `0.95` (catches the brushed brass arch reveal).
  - **Practical Lights (Inside Alcove):**
    1. `Practical_Globe_Sconce_Left` (`OmniLight3D`): Local Pos `(-0.82, 1.35, -0.28)`, Color `#FFCA70` (2700K warm opal globe), Energy `1.55`, Range `2.2m` + emissive globe sphere (`emission: #FFE4AC`, `energy: 3.2`).
    2. `Practical_Globe_Sconce_Right` (`OmniLight3D`): Local Pos `(0.82, 1.35, -0.28)`, Color `#FFCA70`, Energy `1.35`, Range `2.0m` + emissive globe sphere (`emission: #FFE4AC`, `energy: 3.2`).

---

## 4. Render & Tournament Voting Sheet Framing Guide (`Gage` & `Rook`)

To ensure Jared can compare all 10 Round-1 Bunk Pod candidates side-by-side on a fair, visually rich playing field:

1. **Individual Candidate Renders (`/workspace/game-project/assets/renders/bunk_round1/bunk_r1_01.png` .. `bunk_r1_10.png`):**
   - **Resolution:** `1280 × 960` (4:3 aspect ratio) or `1600 × 1200`.
   - **Standard Camera Transform (3/4 Front-Isometric Alcove Beauty Angle):**
     - **Camera Position:** `(1.85, 1.65, 2.55)`
     - **Camera Look-At Target:** `(0.00, 0.92, -0.05)`
     - **FOV:** `42°`
     - *Why this angle:* Shows the full outer silhouette, looking Slightly Down (`~16°`) and Left into the headboard (`-X`) and rear alcove (`-Z`) so the pillows, draped blanket overhangs, telemetry screens, and warm practical sconces are clearly visible.
   - **Studio Backdrop & Floor Pedestal:**
     - Place each bunk on a dark warm charcoal-slate cyclorama floor (`#23252A`, `roughness: 0.55`) so the warm interior practical lights cast a rich pool of light onto the floor in front of the bunk.
   - **Environment / Tonemapping (`WorldEnvironment`):**
     - `tonemap_mode = ACES` (or `Filmic`), `tonemap_exposure = 1.05`, `ssao_enabled = true` (`radius = 0.45`, `intensity = 1.8`), `glow_enabled = true` (`intensity = 0.45`, `bloom = 0.08`) to give CRT monitors and reading sconces a natural retro-futuristic halation.

2. **Numbered 10-Panel Tournament Voting Sheet (`/workspace/game-project/assets/renders/bunk_round1/bunk_round1_voting_sheet.png`):**
   - **Grid Layout:** **5 columns × 2 rows** (or **2 columns × 5 rows**) high-resolution composite sheet (`3200 × 1600` or `2560 × 3200`).
   - **Card Overlays:** Each cell must include a clean high-contrast badge in the top-left corner (`#01 CASSETTE CAPSULE`, `#02 BULKHEAD BERTH`, ..., `#10 OFFICER STATEROOM ALCOVE`) with its archetype subtitle so Jared can vote immediately by number (`01`–`10`).
