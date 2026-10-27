# 3D Asset & Prop Pipeline Specification (Godot 4) — Project *Cylinder Hab-7*
**Owner:** Rook (3D Modeling Specialist — `11c68e8e-c070-4e83-a926-21e9dfb70523`)  
**Team:** Atlas (PM), Sloane (Interior & Environment Designer), Gage (Godot 4 Dev), Scribe (Context Manager)

## 1. Directory Layout
- `/workspace/game-project/assets/glb/` — Final exported binary glTF 2.0 (`.glb`) assets ready for Godot 4 import (`room_shell.glb`, `bunk_bed.glb`, `retro_desk_crt.glb`, `wardrobe_locker.glb`, `lounge_chair.glb`, `coffee_table.glb`, `floor_lamp.glb`, `area_rug.glb`, `hydro_planter.glb`).
- `/workspace/game-project/assets/src/` — Primary procedural Python mesh, texture, validation, and preview rendering scripts:
  - `generate_textures.py` — Generates high-resolution seamless PNG textures in `/workspace/game-project/assets/textures/` (respecting any pre-existing files from Sloane).
  - `glb_builder.py` — Core beveled/chamfered primitive & lathe generator and binary glTF 2.0 (`.glb`) serializer with embedded PNG `baseColorTexture` and `pbrMetallicRoughness` + `emissiveFactor`.
  - `generate_models.py` — Builds all 9 hero `.glb` models and writes `manifest_summary.json`.
  - `validate_models.py` — Validates all 9 `.glb` models via `pygltflib` and `trimesh` (checking binary headers, normals, UV0s, materials, bounding boxes, and `min Y == 0.0`).
  - `render_asset_sheet.py` — Renders the multi-panel shaded 3D preview sheet + texture swatches to `/workspace/game-project/assets/renders/asset_sheet.png`.
- `/workspace/game-project/assets/scripts/` — Symlinks to `/workspace/game-project/assets/src/` for quick CLI execution.
- `/workspace/game-project/assets/textures/` — Seamless PBR and UI PNG textures.
- `/workspace/game-project/assets/renders/asset_sheet.png` — High-resolution 3D shaded preview sheet of all 9 models + 8 texture swatches.
- `/workspace/game-project/assets/ASSET_MANIFEST.md` — Complete catalog of completed props, bounding boxes, vertex/triangle counts, materials, and room placement coordinates.

## 2. Godot 4 Export & Coordinate Standards
- **Format:** Binary glTF 2.0 (`.glb`) with self-contained embedded PNG textures and named submesh nodes.
- **Coordinate System:** Right-handed, `-Z` Forward, `+Y` Up (standard glTF 2.0 / Godot 4 convention).
- **Scale & Units:** `1.0 unit = 1.0 meter`. Room shell interior footprint is `4.0m wide (X: -2.0 to +2.0) × 5.0m deep (Z: -2.5 to +2.5) × 3.0m tall (Y: 0.0 to +3.0)`.
- **Pivot / Origin Placement:**
  - Every floor-standing asset and `room_shell.glb` has its origin centered in `X` and `Z` `(0, 0)` and its minimum `Y` resting cleanly at `Y = 0.0000m` (`|min_y| < 1e-5`).
- **Architectural Apertures (`room_shell.glb`):**
  - **North Wall (`Z = -2.5m`):** Open panoramic chamfered viewport aperture (`X: -1.25m to +1.25m`, `Y: 0.85m to 2.35m`) with deep sill and brushed brass bezel so exterior O'Neill Cylinder sunlight and vista backdrop shine directly into the room.
  - **South Wall (`Z = +2.5m`):** Framed bulkhead corridor doorway (`X: -0.55m to +0.55m`, `Y: 0.0m to 2.20m`) with recessed sliding door panel.
  - **Collision Suffixes:** Floor structural slab uses `-col` (`Floor_StructuralSlab-col`) for automatic Godot 4 static collision generation.

## 3. Rebuilding & Validating Assets
```bash
python3 /workspace/game-project/assets/src/generate_textures.py
python3 /workspace/game-project/assets/src/generate_models.py
python3 /workspace/game-project/assets/src/validate_models.py
python3 /workspace/game-project/assets/src/render_asset_sheet.py
```
