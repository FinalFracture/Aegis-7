# Lit window interior card (#6): 5 iterations
Generator: `assets/src/window_card_generator.py`. The card is 3.0 × 1.5 m. Its pivot is bottom-center, it faces +Z, and any depth extends into -Z (into the room).

Materials are unlit (`KHR_materials_unlit`, plus an emissive texture), so the card reads as lit at any exposure. Textures are painted procedurally from per-unit profiles taken from layout v2 rev C:
- 101: dim, bunk
- 102: plants knocked over, empty suit hook
- 103: family, toys by the window
- 104: red solar glyph on the slates
- 202: drawing, toys
- 203: route model
- 204: bench
- 201: lights off

The glbs export unit 103. Each sheet's Exterior view shows units 103, 104 and 101 in a dusk facade seen from about 15 m at eye height. `overview.png` puts all five exterior views side by side. The PNG textures sit next to each glb.

## iter_01: Flat painted quad (2 tris, 1 × 1024×512 RGB)
A single unlit quad carries the whole room painted flat. It is the cheapest option and trivial to swap per unit, because only the texture changes. It has no parallax, so it looks like a poster when viewed at an angle.

## iter_02: Interior box, fake interior mapping (10 tris, 1 × 1024×1024 atlas)
This is a shallow 0.8 m open box: back wall, floor, ceiling and two side walls, all from one atlas. It gives real perspective depth from any angle with no shader work. It needs one atlas per unit, and the props are still painted flat on the back wall.

## iter_03: Layered cutout planes (6 tris, 3 × 1024×512: 1 RGB + 2 RGBA)
There are three planes: the back wall at -1.2 m (oversized), mid furniture at -0.7 m and foreground props at -0.3 m (chairs, toys). This gives strong parallax, and the prop layers can be mixed between units. It uses two alpha-blended planes, so overdraw is slightly higher.

## iter_04: Frosted privacy glass (2 tris, 1 × 1024×512 RGB)
A blurred, desaturated room is painted with a soft person silhouette and frost noise. Its low detail hides the fact that it's a stand-in, and it matches what a privacy film would show. It still differs per unit through tint and blobs, and it costs the same as iter_01.

## iter_05: Blinds over lit room (4 tris, 2 × 1024×512: RGB room + RGBA blinds)
A room quad sits at -0.6 m behind a blinds plane at -0.04 m. The blinds are 55% drawn, with lit slat edges and the room visible below them. They add parallax and a believable reason for less detail. The blind height can vary per unit.

**Recommendation:** iter_05 (blinds), with the iter_03 split of mid and fore layers behind it if extra depth is wanted. It reads as lived-in at 10–20 m, hides the stand-in nature cleanly and costs 4 tris.

## Combo: interior box + layered cutouts (14 tris, 2 × 1024×1024 atlases, embedded)
This combines iter_02 and iter_03. A shallow open box is 1.0 m deep with a 3.0 × 1.5 m opening and has five faces: back wall, floor, ceiling and two side walls. Inside it are two alpha cutout planes: mid furniture at -0.7 m and foreground props (chairs, toys) at -0.3 m.
- **Atlas A (RGB, opaque, used by the box):** back wall in the top half; floor, ceiling and both side walls in 512×256 slots.
- **Atlas B (RGBA, alpha-blended, used by the props):** the mid layer in the top half and the foreground layer in the bottom half.

Per-unit profiles (tint, prop set, lights on or off) only repaint the atlases; the mesh stays the same. The atlases are embedded in each glb. The same PNGs are also saved alongside for review: `combo_<unit>_atlasA_box.png` and `combo_<unit>_atlasB_props.png`.

- **Files:** `combo_103.glb`, `combo_104.glb`, `combo_201.glb` (201 has its lights off). Build them with `python3 assets/src/window_card_generator.py combo`.
- **Renders:**
  - `combo_street.png`: eye height 1.7 m, about 12 m out, night cycle.
  - `combo_far.png`: about 75 m out, with the habitat floor curving up behind the building (R about 450 m) and distant lit blocks.
  - `combo_walkby.png`: 3 oblique frames 4 m apart, showing parallax of the box walls and the prop layers.
  - `combo_sheet.png`: Top, Front, Side and Iso views, plus a strip of the 103, 104 and 201 variants.
