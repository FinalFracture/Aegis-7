# Cylinder Hab-7 — Aegis-7 Character Suit, Visor, Fabric Weave & Chest Telemetry PBR Texture & Lighting Spec
**Author:** Sloane (Interior, Lighting & Texture Designer)  
**Target Asset:** Aegis-7 Colonial / EVA Rigged & Animated Character (`char_01` with 24–60 frame Walking Animation Cycle)  
**Standard:** Unified "Aegis-7 Standard" (65/35 Dual-Zone Split-Mass Armor Hierarchy, `<1.0%` micro-noise PBR, `alphaMode: "BLEND"` Dichroic AR HUD Visor, 3-Point Rim-Lit Character Showcase)

---

## 1. Aesthetic & Material Hierarchy (65/35 Aegis-7 Character Standard)

To ensure the animated character reads crisply at both third-person gameplay camera distances (`2.5m–8.0m`) and close-up inspection sheets (`1.2m–2.2m`) while walking through Cylinder Hab-7's golden-hour promenades and interior rooms:

1. **65% Hard-Surface Contoured Exo-Armor (`char_suit_armor_albedo.png`):**
   - **Upper / Primary Plates (`y < 0.65` in UV):** Matte Aerospace-White (`#D8DEE6` / `#E4E9F0`, `roughness = 0.34`, `metallic = 0.15`) on the sculpted chest cuirass, clavicle collar, asymmetric shoulder pauldrons, forearm gauntlets, femoral thigh plates, and tibial shin greaves.
   - **Lower / Structural Load-Bearing Chassis (`y >= 0.65` in UV):** Titanium-Gunmetal (`#1A1E24` / `#222730`, `roughness = 0.42`, `metallic = 0.78`) and Brushed Steel (`#88929E`, `roughness = 0.28`, `metallic = 0.85`) on the dorsal life-support backpack frame, waist torque-ring, knee/ankle mechanical clevis hinges, and magnetic-grip boot soles.
   - **High-Visibility EVA Trim:** Signal-Orange (`#D95B26`) and Warm Circadian Amber (`#FFB703`) mission stripes across the upper pectoral plates, right shoulder pauldron, and lower shin cuffs so limb swing during the walk cycle is immediately legible from any angle.
2. **35% Articulated Compression Undersuit & Flex-Bellows Joints (`char_undersuit_ribbed_fabric.png`):**
   - **Left UV Half (`u: 0.0–0.5`):** Deep Orbital Navy (`#1E2D3E`) hexagonal micro-ripstop pressure-suit weave with warm anodized brass/amber (`#A88A4E`) ergonomic seam piping (`roughness = 0.76`, `metallic = 0.05`) for torso, abdomen, neck seal, and inner thighs.
   - **Right UV Half (`u: 0.5–1.0`):** Ballistic Charcoal (`#20252D`) pneumatic flex-bellows ribs (`roughness = 0.68`, `metallic = 0.12`) mapped to high-deformation walking joints (hip flexors, behind knees, elbows, ankles, and shoulder gussets) to visually reinforce clean skeletal skinning and joint articulation.
3. **Translucent Dichroic Gold-Cyan AR HUD Visor (`char_visor_hud_translucent.png`, `alphaMode: "BLEND"`):**
   - Curved dome visor combining a deep sapphire-to-warm-gold dichroic Fresnel gradient (`alpha = 0.35` at center so the sculpted interior helmet rim/head silhouette is visible, rising to `0.72` at grazing angles) with projected internal `#00E5FF` cyan and `#FFB703` amber AR navigation pitch ladders, compass ticks, and biometric arcs (`roughness = 0.06`, `metallic = 0.25`, `specular = 0.95`).
4. **Chest Console & Backpack Life-Support Telemetry (`char_chest_telemetry_emissive.png`):**
   - **Top UV (`v: 0.0–0.64`):** Recessed dark-glass OLED chest unit displaying a live `#52B788` emerald cardiopulmonary ECG waveform, dual `#00E5FF` cyan O2/spin-G circular ring gauges, and `#FFB703` amber thermal/battery bargraphs.
   - **Bottom UV (`v: 0.64–1.0`):** Five dedicated high-intensity emissive trim bands (`#00E5FF` Cyan, `#FFB703` Warm Amber, `#52B788` Biometric Emerald, `#FF6D24` Signal-Orange, `#E6F7FF` Ice-White headlamp) for backpack spine cores, ankle stride beacons, and helmet dual-beam worklights (`emission_energy_multiplier = 2.4`).

---

## 2. Generated Character Texture Suite (`/workspace/game-project/assets/textures/character/`)

All 4 textures are `512×512` PNGs (`<1.0%` micro-noise) saved in `/workspace/game-project/assets/textures/character/` and mirrored to `/workspace/game-project/assets/textures/`:

| Texture Filename | Format | UV Layout & Target Geometry | Godot 4 `StandardMaterial3D` Settings |
|---|---|---|---|
| `char_suit_armor_albedo.png` | `512×512` RGB | `v: 0.0–0.65` Matte Aerospace-White (`#D8DEE6`) chest/pauldron/thigh/shin plates with `#D95B26` signal-orange & `#FFB703` amber stripes;<br>`v: 0.65–1.0` Gunmetal (`#222730`) & Brushed Steel (`#88929E`) backpack/joint actuators | `roughness = 0.34`, `metallic = 0.22` (or split into white armor `metallic = 0.15` + gunmetal/steel trim `metallic = 0.80`) |
| `char_undersuit_ribbed_fabric.png` | `512×512` RGB | `u: 0.0–0.5` Orbital Navy (`#1E2D3E`) hex-ripstop torso/thigh fabric with brass seam piping;<br>`u: 0.5–1.0` Charcoal (`#20252D`) ribbed flex-bellows for shoulder/elbow/hip/knee walk-cycle joints | `roughness = 0.74`, `metallic = 0.06` |
| `char_visor_hud_translucent.png` | `512×512` RGBA | Curved helmet visor dome (`alphaMode: "BLEND"`) with dichroic gold-cyan Fresnel sheen and projected AR reticle/compass HUD | `transparency = TRANSPARENCY_ALPHA`, `roughness = 0.06`, `metallic = 0.25`, `emission_enabled = true`, `emission_energy_multiplier = 0.85` |
| `char_chest_telemetry_emissive.png` | `512×512` RGB | `v: 0.0–0.64` Chest OLED ECG/O2/Spin-G display;<br>`v: 0.64–1.0` Solid emissive strips (`#00E5FF` cyan, `#FFB703` amber, `#52B788` emerald, `#FF6D24` orange, `#E6F7FF` white) | `emission_enabled = true`, `emission_texture = char_chest_telemetry_emissive.png`, `emission_energy_multiplier = 2.4`, `roughness = 0.18` |

---

## 3. Godot 4 Character Showcase & Walk-Cycle Lighting Spec (For Gage)

To highlight both the 65/35 hard-surface armor bevels and the limb motion of the walking animation in the character voting sheet and walk-cycle showcase sheet:

1. **Key Light (`DirectionalLight3D` — Warm Golden-Hour Axial Sun):**
   - Color: `#FFE6BF` (`RGB(1.0, 0.90, 0.75)`), Energy: `1.55`, `shadow_enabled = true`, angled at `38°` elevation and `35°` azimuth so the chest cuirass, visor dome, and forward striding leg catch crisp warm highlights.
2. **Cool Rim / Back-Edge Kicker (`DirectionalLight3D` or `SpotLight3D`):**
   - Color: `#5CE1E6` (`RGB(0.36, 0.88, 0.90)`), Energy: `1.15`, positioned behind-left (`-145°` azimuth) to trace a sharp cyan Fresnel rim along the helmet crown, backpack life-support spine, swinging forearms, and trailing boot heel during each walk-cycle keyframe (`t = 0.0, 0.25, 0.50, 0.75`).
3. **Under-Floor Bounce Fill (`OmniLight3D`):**
   - Color: `#8898AA`, Energy: `0.45`, lifting dark `#1E2D3E` undersuit knee/hip folds so skeletal joint deformation remains 100% readable without crushing shadows.

---

## 4. Phase 5B Addendum — 5-Character Distinct Headshot Portrait Atlas (`char_headshot_faces_and_hair_atlas.png`) & Studio Portrait Lighting Rig

### 4.1 `char_headshot_faces_and_hair_atlas.png` (`512×512` RGB, `<1.0%` micro-noise)
Saved in `/workspace/game-project/assets/textures/character/char_headshot_faces_and_hair_atlas.png` (and mirrored to `/workspace/game-project/assets/textures/char_headshot_faces_and_hair_atlas.png`). Divided into **5 horizontal UV bands** (one per character `#01`..`#05`), with **3 horizontal sub-columns** across `u`:
- **`u: 0.00–0.50` (`x: 0..255`):** Sculpted Front Facial Portrait (forehead/cheekbone highlights, nose bridge & nostrils, eyebrows, sclera/irises/pupils with crisp studio catchlights, sculpted lips, and character-specific facial hair, scars, or cybernetic/AR implants).
- **`u: 0.50–0.75` (`x: 256..383`):** Distinct Hair Strands / Braids / Temple-Streak Material Swatch.
- **`u: 0.75–1.00` (`x: 384..511`):** Role-Specific Collar, Neck-Seal, Ear-Comms & Emissive IFF Rank Trim Swatch.

| Band / Character | Vertical UV Range (`v`) | Pixel Rows (`y`) | Skin Tone & Facial Features (`u: 0.0–0.5`) | Hair Style & Palette (`u: 0.5–0.75`) | Headgear / Collar Trim (`u: 0.75–1.0`) |
|---|---|---|---|---|---|
| **`#01` Flight Officer** | `v: 0.00–0.20` | `y: 0..101` | Warm Bronze (`#C68B63`), Hazel irises (`#8A6C38`), clean-shaven | Dark Espresso (`#261C18`) brushed strands | Aerospace-White (`#D8DEE6`) + Cobalt (`#244E8A`) & Cyan (`#00D2FF`) |
| **`#02` Aegis-7 Commander** | `v: 0.20–0.40` | `y: 102..203` | Medium Olive (`#D49E7A`), trimmed charcoal beard/stubble, glowing `#00E5FF` cyan AR monocle over right eye | Charcoal (`#383D45`) with Silver temple streaks (`#B8C2CC`) | Gunmetal (`#222830`) + Signal-Orange (`#D95B26`) & Cyan (`#00E5FF`) |
| **`#03` Heavy EVA Engineer** | `v: 0.40–0.60` | `y: 204..305` | Deep Rich Umber (`#6E422C`), Amber-Brown irises (`#A8682A`), hazard-gold forehead telemetry node | Dark Textured Braids (`#1A1412` / `#3A2E28`) | Weathered Gunmetal (`#30363E`) + Industrial Hazard-Gold (`#FFB703`) |
| **`#04` Bio-Med Specialist** | `v: 0.60–0.80` | `y: 306..407` | Warm Ivory (`#F0C8B0`), Emerald-Green irises (`#34B276`), bioluminescent emerald/UV-violet temple neural nodes | Platinum-Silver (`#DCE3EA`) with Emerald tips (`#52B788`) | Sterile White (`#E4EBF0`) + Emerald (`#52B788`) & UV-Violet (`#8A6CFF`) |
| **`#05` Tactical Recon** | `v: 0.80–1.00` | `y: 408..511` | Cool Sunlit Tan (`#B98360`), Steel-Grey irises (`#8494A4`), diagonal left-cheek scar + stealth-amber cheekbone IFF stripe | Ash-Black Undercut (`#1E2024` / `#444A54`) | Matte Stealth-Slate (`#2B303A`) + Tactical Amber/Crimson (`#FF6D24`) |

### 4.2 3-Point Close-Up Portrait Studio Lighting Rig (For Gage's Headshot Showcase Sheet)
To ensure all 5 faces, eyes, hair textures, and headgear silhouettes read with portrait-grade clarity (without being obscured by dark visor tint):
1. **Open/Retracted or High-Clarity Visor Mode for Headshots:** Set visor alpha (`char_visor_hud_translucent.png`) to `alpha <= 0.18` (or raise/retract the front visor shield on the headshot bust view) so skin tones, irises, catchlights, beard/scars, and hair strands are 100% unobstructed.
2. **Portrait Key Light (`DirectionalLight3D` or `OmniLight3D` — Warm Rembrandt Studio Key):**
   - Color: `#FFF0DB` (`RGB(1.0, 0.94, 0.86)`), Energy: `1.65`, positioned `28°` off-axis (front-right, slightly above eye level at `Y = 1.78m`) to sculpt the nose bridge, cheekbones, brow ridge, and iris catchlight.
3. **Portrait Fill Light (`OmniLight3D` — Soft Neutral-Warm Skin Fill):**
   - Color: `#D8E4F0` (`RGB(0.85, 0.89, 0.94)`), Energy: `0.75`, positioned front-left at `Y = 1.62m` so the shadowed side of darker and lighter complexions alike (`#6E422C` through `#F0C8B0`) retains rich subsurface warmth and eye detail.
4. **Hair & Shoulder Rim Kicker (`SpotLight3D` / `DirectionalLight3D` — Cool Cyan-Silver Edge Light):**
   - Color: `#66E8FF` (`RGB(0.40, 0.91, 1.0)`), Energy: `1.20`, positioned behind-left (`Y = 1.92m`) to separate dark espresso/braided/undercut hair and gunmetal collars cleanly from the studio background.
