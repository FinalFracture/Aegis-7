# Force-field door materials — spec (Sloane, 2026-10-30)
Fulfils the 6 texture/material requests in `design/force_field_door_godot_changes.md`. Maps are in `godot/assets/textures/force_field/` (generator: box script `/workspace/sl_tools/ff_tex.py`, not in repo). Preview: `design/materials/force_field_preview_sheet.png`.
Aegis-7 Standard: amber `#FF9500`, cyan `#00E5FF`, signal orange `#D95B26`, steel `#88929E`. ORM = R AO / G roughness / B metallic. Sizes are powers of two, ≤1024. Tiling maps are periodic by construction. Albedo micro-noise is at most ±0.5%.

## 1. Field plane — `FieldPlane` (or `FieldPlane_A/B`) in `rfid_forcefield_door.glb`
| Map | Size | Notes |
|---|---|---|
| `ff_field_lockout_amber_albedo.png` | 512² RGBA, tiles XY | Amber lattice; alpha 0.30–0.55 |
| `ff_field_lockout_amber_emission.png` | 512² | Amber lattice + 64 scanlines |
| `ff_field_ready_cyan_albedo.png` / `_emission.png` | 512² | Same lattice in cyan (ready/idle). The current in-game violet can tint this. |
| `ff_field_stall_noise_mask.png` | 512² RGB, tiles XY | R = low-freq blotches, G = horizontal tear bands, B = dropout cells (binary) |

The existing `forcefield_door.gdshader` keeps doing the drawing. These maps go in as optional `field_tex`, `field_emit` and `stall_mask` samplers (Gage). If the shader isn't extended, use a StandardMaterial3D with the settings below.

Base material: `transparency = ALPHA` (BLEND), `cull_mode = DISABLED`, `shading_mode = UNSHADED` (or lit with roughness 0.1, metallic 0), `depth_draw = OPAQUE_ONLY`, no shadows, UV scale (2, 2) per metre.

| State | Map set | Opacity × | Emission energy | UV scroll (u, v / s) | Flicker / mask | Collider |
|---|---|---|---|---|---|---|
| **Full** (closed, ready) | cyan | 1.0 (shader `opacity` 0.45) | 1.2 | (0, 0.05) | `static_strength` 0.35, `jitter` 0.004 | ON |
| **Amber lockout** | amber | 1.0 | 1.5, pulsing ±15% at 0.5 Hz | (0, 0.03) | `arc_strength` 0.8 | ON |
| **Stall** (partial power, ~40%) | amber (or cyan) + stall mask | 0.40 base; mask R × 0.5 + G bands scrolling (0, 0.8/s); B cells drop out for 1–3 frames at random | 0.6–1.4 random-walk, 12 Hz | (0.02, 0.25) jerky | `jitter` 0.012, `static_strength` 0.8. **Never fully transparent: minimum alpha 0.15 across the whole plane** | **ON** |
| **Refused** (deny scan) | amber | Spike to 1.6 for 0.08 s, then 0.3 s decay back to the prior state | 3.0 peak | — | One-shot; B-mask dropout flash | ON |
| **Released** | — | Dissolve 0 → 1 over 0.8 s (existing) | → 0 | — | — | OFF at end |

## 2. Split-field seam — `FieldSeam` (new quad, 0.12 m wide, at the A/B centre line)
`ff_split_seam_albedo.png` (128×1024 RGBA, tiles V) and `ff_split_seam_emission.png`. BLEND, unshaded, emission energy 2.0, UV scroll v 0.4/s. Hide it once both halves are in phase or released. In the stall state, flicker it with the same 12 Hz random walk.

## 3. Emitter coil banks — `Emitter_Coil_A` / `Emitter_Coil_B` (jamb rails + header phase bars)
`ff_emitter_coil_albedo.png`, `ff_emitter_coil_orm.png` (1024²). The atlas splits into V 0–0.78 for coil windings (steel, metallic 1, roughness ~0.32–0.37) and V 0.78–0.94 for 12 phase bars (signal orange, metallic 0, roughness 0.55). Opaque.
Emission: `ff_emitter_coil_emission_inphase.png` (all 12 bars cyan, energy 2.0) and `_outphase.png` (alternate bars orange, energy 1.6, blink 2 Hz). **Off** = emission disabled (energy 0, no map).

## 4. Header calibration nodes — `Node_Calib_01..03`
`ff_calib_node_albedo.png` and `ff_calib_node_emission_states.png` (512×256). The 3 cells are off / amber / cyan. Map one cell to each node with a UV offset of u = 0, 1/3 or 2/3 (scale 1/3, 1). Emission energy 2.5. Use the amber cell while calibrating and pulse it at 1 Hz in the stall state.

## 5. Threshold strip — `Threshold` (extends `Mat_FF_Threshold_Chevron`)
`ff_threshold_strip_albedo.png` with `ff_threshold_strip_amber_emission.png` / `_cyan_emission.png` (1024×128, tiles U). Roughness 0.6, metallic 0. Emission energy 1.8. UV scroll u 0.25/s toward the opening while ready; static while amber. Amber → cyan on release (0.3 s crossfade).

## 6. Inspection transom glass — `Transom_Glass` (preface room, 2.40 × 0.85 m)
`ff_transom_glass_albedo.png` (512² RGBA, alpha ≈ 0.32) and `ff_transom_glass_orm.png` (roughness 0.08–0.16 smudge, metallic 0). BLEND, roughness from ORM.G, specular 0.5, no emission.
