# Door Lab: Aesthetic Spec (Sloane, 2026-11-20)
Scene `res://scenes/test/door_lab.tscn`. Godot 4.7 **gl_compatibility**: 8-bit, no HDR, no Decal nodes (use BLEND quads 2 mm proud), and emission clips at about 1.0, so energies below are kept low and use colour to read. Realism is in Vance's `REALISM_SPEC.md`, and the pass bar is in Patch's `QUALITY_BAR.md`. This file covers only the look.

## 1. Door types and material sets
Reuse the existing project materials. Do not author new ones unless a slot is missing. Values are linear albedo / metallic / roughness.

| Part | Material (reuse) | Albedo | Metal | Rough |
|---|---|---|---|---|
| Leaf face, main | `TT_WhiteComposite` / `Mat_Hub_Pearl` #D8DEE6 | 0.85–0.88 max (see §1.1) | 0.0–0.2 | 0.40–0.55 |
| Leaf inset / recess panels | `TT_CarbonSlate` / `Mat_Hub_Graphite` #282E38 | 0.15–0.22 | 0.25–0.5 | 0.55–0.70 |
| Structure, frame, header | `TT_Gunmetal` #1A1E24 (facade_titanium_gunmetal_hull set) | 0.10–0.14 | 0.6–0.8 | 0.45–0.60 |
| Jamb, edges, handles, tracks, hinges | `TT_BrushedAlloy` / `Mat_Hub_BrushedSteel`, qa03 `door_jamb_gunmetal` albedo+ORM | 0.75–0.82 | 0.9–1.0 | 0.30–0.40 |
| Vision glass | `TT_GlassScissor` (MASK), never BLEND on a moving leaf | 0.72 / 0.86 / 0.93 | 0.0 | 0.05–0.10 |
| Status lamps | `Mat_Hub_StateGlow`, `TT_AmberLED`, `TT_CyanLED` | see §3 | 0 | 0.3 |
| Hazard / override | `Mat_Hub_OverrideOrange` | — | 0.1 | 0.45 |
| Gaskets / seals | `TT_CarbonSlate` darkened to 0.08, rough 0.85 (rubber) | 0.06–0.09 | 0 | 0.80–0.90 |

- **Bi-parting sliding pocket:** two leaves with pearl faces and a graphite centre inset. The meeting stiles get a brushed-alloy edge and a 6 mm black gasket. The header pocket is gunmetal, with a thin cyan reveal strip in the soffit.
- **3-leaf bay (telescoping):** each leaf steps 1 tone darker from front to back (pearl, then pearl −8%, then graphite). That way the stack reads as layered when open. Each leaf leading edge gets an alloy edge.
- **Double swing pair `tt_door_pair_18`:** keep its current set (TT_BrushedAlloy, TT_WhiteComposite, TT_CarbonSlate, TT_GlassScissor, TT_AmberLED). Pull albedo to 0.85–0.88 per §1.1. Alloy push plates and kick plates, plus a single amber lamp above each leaf.
- **Heavy bulkhead / hatch:** gunmetal body, graphite recessed panels and brushed-steel dogs/locking wheel. Put `OverrideOrange` only on the manual-release handle and a 45° hazard band on the sill (BLEND quad, alpha 0.9). It should look the heaviest: lowest albedo and the most visible bolts and bevels.

### 1.1 TT_WhiteComposite albedo fix
The shipped TT_WhiteComposite measures 0.92–0.94, which is over the project cap of 0.9. **Door lab uses 0.847 / 0.871 / 0.902 (#D8DEE6)**, the palette value. If it looks right in the renders, the same value becomes the global fix. Leave other assets alone until it is approved.

## 2. Wear and edge highlights (subtle, under 1.2% micro-noise)
- **Edges:** 2–4 mm bevel on every leaf edge and frame arris, so the specular catches a thin highlight. **No razor-sharp 90° edges on hero parts.**
- **Wear location:** only where hands, carts and feet touch: the handle zone (0.9–1.2 m), the bottom 0.15 m kick zone, the meeting-stile edges and the hatch sill. Use the ORM roughness channel −0.10 to −0.15 (polished) on alloy, and a 3–5% albedo lift on paint. **No grime, rust, stripes or scratches.** Aegis-7 is clean and maintained.
- **Not allowed:** wood looks, stencilled numbers over 1 per door, noisy textures, and coplanar decals (embed 2 mm or more).

## 3. Status lights (emissive)
Use one lamp strip per door (header or jamb), plus a hub ring on the bulkhead. Colour does the work; energy stays low.

| State | Colour | Energy | Behaviour |
|---|---|---|---|
| Locked | Red #FF2A2A | 0.8 | steady |
| Closed (unlocked, idle) | Amber #FF9500 | 0.6 | steady (standby) |
| Opening / closing | Cyan #00E5FF | 0.9 | chase along the strip toward the travel direction, about 0.4 s per pass |
| Open | Green #3FAF6A | 0.7 | steady; fades to 0.4 after 3 s |
| Fault / jam | Red #FF2A2A plus Amber #FF9500 alternating | 1.0 | 2 Hz blink, 50% duty; leaf stops with a 4 mm settle |

- Energy × the colour's brightest channel stays at or under 1.0, so nothing clips to white.
- Fade between states over 0.15 s. **No hard snapping.**
- Each lamp lights a small OmniLight3D (range 0.6 m, energy 0.15, same colour, no shadows), so the jamb picks up a coloured spill.

## 4. Frame and jamb trim lighting
- A recessed cyan `TT_CyanLED` reveal strip, 10 mm, runs in the head soffit and both jambs at energy 0.5, steady in every state. Status colour lives only in the lamp, never in the reveal.
- Use one downlight (SpotLight3D, 35°, energy 0.6, 4000 K #FFE9D2, shadows on) per doorway, 0.4 m in front of the head, so the leaf face has a top-down gradient and the bevel highlight. This is the light that sells the material.
- Gameplay interiors stay dark (Jared). **The lab rig is for review only.** Don't copy §5 into game scenes, and don't use the lab to justify brighter rooms.

## 5. Lab lighting rig and hero cameras
- **Environment:** ambient energy 0.15 (dark slate #1A1E24), filmic tonemap with the white point left at the project default, glow off, and one ReflectionProbe (box, covering the lab) so the alloy and glass have something to reflect.
- **Key light:** DirectionalLight3D, energy 0.5, pitch −35°, yaw 30° off the door normal, shadows on (PCF soft).
- **Fill light:** OmniLight3D, energy 0.2, behind and above the camera, no shadows.
- **Rim light:** a SpotLight3D behind the door wall through the opening, energy 0.4, cyan-tinted #CFF7FF. It only reads when the door is open (shows depth).
- **Floor:** `TT_CarbonSlate`, roughness 0.6, so the status light gives a soft reflection.
- **Cameras** (Camera3D, 16:9, 1920×1080):

| ID | Name | Placement | FOV | Use |
|---|---|---|---|---|
| A | Hero 3/4 | 3.2 m from the door, 1.6 m high, 30° off-axis, looking at the leaf centre | 50° | main score shot, every state |
| B | Square-on | 4.0 m on axis, 1.5 m high | 40° | symmetry, gaps, alignment |
| C | Detail | 0.9 m from the jamb or handle, 1.1 m high, 45° | 35° | edges, wear, lamp spill |
| D | Player eye | 1.8 m, 1.65 m high, on axis | project player FOV (75°) | what the player actually sees |
| E | Low threshold | 1.2 m, 0.35 m high, looking up 10° | 45° | sill, hazard band, the bottom of the leaf travel |

- **Render set per door:** A in each of the 5 states, B closed, C closed and open, D in mid-travel, E open. For motion, use A as a 24 fps strip of 8 frames across one open cycle.

## 6. Motion feel
- **Sliding pocket and 3-leaf bay:** ease-in-out (cubic), 0.9 s open and 1.1 s close. A 40 ms anticipation pause after the unlock and before motion. The 3-leaf bay's leaves start 60 ms apart, front to back, so the leaves visibly telescope. End with a soft settle of 3 mm or less and no bounce.
- **Double swing pair:** ease-out (quad), 0.8 s to 90°. A 50 ms lag on the second leaf. Closing ease-in to 10°, then a soft 0.25 s damper to shut. **No slam.**
- **Heavy bulkhead / hatch:** must feel heavy. Wheel/dogs rotate first (0.5 s, ease-in-out), with a 0.15 s hold. The leaf follows, slow-in fast-middle slow-out over 1.8 s. End with a 2 mm overshoot and settle (0.2 s).
- Every door: lamp state changes **with** the motion start (opening, cyan) and at the final settle (open, green), never after it.

## 7. Aesthetic scoring rubric
Score 1–5 for each criterion, from Hero camera A plus the matching extra shots. **Pass:** average 4.0 or higher, **and** no criterion below 3, **and** criteria 1, 3 and 6 at 4 or higher.

| # | Criterion | 5 = | 1 = |
|---|---|---|---|
| 1 | **Material read** | pearl, graphite, gunmetal and alloy are clearly separate; metal reads as metal; albedo 0.9 or less | flat, plastic, washed out or placeholder |
| 2 | **Edge and form definition** | bevel highlights on every edge, panel depth visible, layered silhouette | box-like, sharp, no highlights |
| 3 | **Status light clarity** | the state is obvious from 4 m in a dark room; correct colours; no clipping or bloom smear | unclear, wrong colour or clipped white |
| 4 | **Trim and lighting integration** | reveal strip, downlight gradient and lamp spill all present and balanced | flat-lit or overlit; reveal missing |
| 5 | **Wear restraint** | wear only in touch zones, subtle, under 1.2% noise | grime/stripes/noise, or sterile CG with no wear |
| 6 | **Motion character** | matches §6 easing; no snaps, pops, clipping or jitter; lamps synced | linear, snappy, bouncing, or lamps out of sync |
| 7 | **Palette and style compliance** | zero wood; amber #FF9500 and cyan #00E5FF exact; fits Aegis-7 / Tennis Tower | off-palette, wood, or stray colours |
| 8 | **Artifact-free** | no z-fighting, shadow acne, light leaks, BLEND sorting errors, or stretched UVs | visible artifacts in the hero shot |

Sloane logs the scores per door in `context/VOTE_LOG.md` with the render paths, and fixes to apply are given as numbered notes against this spec's sections.
