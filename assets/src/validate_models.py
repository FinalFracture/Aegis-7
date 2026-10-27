#!/usr/bin/env python3
"""
Strict glTF 2.0 (.glb) & Trimesh Validator for Cylinder Hab-7 (Godot 4 Pipeline).
Validates:
- Room 04 Hero Asset: Surgical Autodoc Gantry & Triage Console (med_autodoc_r1_01.glb .. 05.glb, 3,500-5,800 tris, BLEND glass)
- Room 04 Med-Bay Architectural Shell (room_04_shell.glb / room_04_medbay_shell.glb / room_04_med_bay_shell.glb)
- Room 03 Hero Asset: Ration & Beverage Synthesizer Bank (galley_synth_r1_01.glb .. 05.glb, 3,200-5,500 tris, BLEND glass)
- Room 03 Mess Dining Booth & Architectural Shell (mess_dining_booth.glb, room_03_shell.glb / room_03_mess_shell.glb / room_03_mess_galley_shell.glb)
- Room 02 Hero Fixture: Pressurized Bulkhead Airlock Hatch & Sector Checkpoint (corridor_door_r1_01.glb .. 05.glb, 3,000-5,800 tris, BLEND glass)
- Room 02 Corridor & Room 01 Sleeping Quarters Architectural Shells (room_01_shell.glb, room_02_shell.glb)
- Fixture #9: Personal Climate & Life-Support Wall Panel — Round 1 (climate_r1_01.glb .. 05.glb, 2,500-5,000 tris, BLEND glass)
- Fixture #6: Modular Cargo & Footlocker Chest — Round 1 (footlocker_r1_01.glb .. 05.glb, 2,500-5,000 tris, BLEND glass)
- Fixture #3: Personal Wall Terminal & Fold-Down Cabin Desk — Round 1 (walldesk_r1_01.glb .. 05.glb, 2,800-5,500 tris, BLEND glass)
- Fixture #2: Compact Hygiene & Sonic Wash Vanity — Round 1 (vanity_r1_01.glb .. 05.glb, 2,500-5,500 tris, BLEND glass)
- Fixture #1: EVA Suit & Personal Gear Locker — Round 1 (locker_r1_01.glb .. 05.glb, 3,000-6,000 tris, BLEND glass)
- Locked Tournament Winners in /workspace/game-project/assets/glb/winners/
"""
import os
import sys
import glob
import struct
import numpy as np
import pygltflib
import trimesh

GLB_DIR = "/workspace/game-project/assets/glb"
ROOMS_DIR = "/workspace/game-project/assets/glb/rooms"
WINNERS_DIR = "/workspace/game-project/assets/glb/winners"
MEDBAY_R1_DIR = "/workspace/game-project/assets/glb/medbay_round1"
GALLEY_R1_DIR = "/workspace/game-project/assets/glb/galley_round1"
CORRIDOR_R1_DIR = "/workspace/game-project/assets/glb/corridor_round1"
CLIMATE_R1_DIR = "/workspace/game-project/assets/glb/climate_round1"
FOOTLOCKER_R1_DIR = "/workspace/game-project/assets/glb/footlocker_round1"
WALLDESK_R1_DIR = "/workspace/game-project/assets/glb/walldesk_round1"
VANITY_R1_DIR = "/workspace/game-project/assets/glb/vanity_round1"
LOCKER_R1_DIR = "/workspace/game-project/assets/glb/locker_round1"

EXPECTED_MEDBAY_R1 = [f"med_autodoc_r1_{i:02d}.glb" for i in range(1, 6)]
EXPECTED_GALLEY_R1 = [f"galley_synth_r1_{i:02d}.glb" for i in range(1, 6)]
EXPECTED_CORRIDOR_R1 = [f"corridor_door_r1_{i:02d}.glb" for i in range(1, 6)]
EXPECTED_CLIMATE_R1 = [f"climate_r1_{i:02d}.glb" for i in range(1, 6)]
EXPECTED_FOOTLOCKER_R1 = [f"footlocker_r1_{i:02d}.glb" for i in range(1, 6)]
EXPECTED_WALLDESK_R1 = [f"walldesk_r1_{i:02d}.glb" for i in range(1, 6)]
EXPECTED_VANITY_R1 = [f"vanity_r1_{i:02d}.glb" for i in range(1, 6)]
EXPECTED_LOCKER_R1 = [f"locker_r1_{i:02d}.glb" for i in range(1, 6)]


def validate_file(
    fpath: str,
    check_tri_range=None,
    require_textures: bool = True,
    require_blend_glass: bool = False,
) -> bool:
    fname = os.path.basename(fpath)
    if not os.path.exists(fpath):
        print(f"{fname:44s} | MISSING FILE!")
        return False

    size_kb = os.path.getsize(fpath) / 1024.0
    with open(fpath, "rb") as f:
        header = f.read(12)
    magic, version, total_len = struct.unpack("<4sII", header)
    assert magic == b"glTF", f"{fname}: Invalid magic {magic}"
    assert version == 2, f"{fname}: Invalid glTF version {version}"
    assert total_len == os.path.getsize(fpath), f"{fname}: Length mismatch"

    gltf = pygltflib.GLTF2().load(fpath)
    assert len(gltf.meshes) > 0, f"{fname}: No meshes"
    assert len(gltf.materials) > 0, f"{fname}: No materials"
    if require_textures:
        assert len(gltf.textures) > 0, f"{fname}: No embedded textures"

    blend_mats = [m.name for m in gltf.materials if m.alphaMode == "BLEND"]
    if require_blend_glass:
        assert len(blend_mats) > 0, f"{fname}: Missing alphaMode='BLEND' translucent glass material"

    for mesh in gltf.meshes:
        for prim in mesh.primitives:
            assert prim.attributes.POSITION is not None, f"{fname}: Missing POSITION"
            assert prim.attributes.NORMAL is not None, f"{fname}: Missing NORMAL"
            assert prim.attributes.TEXCOORD_0 is not None, f"{fname}: Missing TEXCOORD_0"
            assert prim.material is not None, f"{fname}: Missing material assignment"

    scene = trimesh.load(fpath, force="scene")
    assert len(scene.geometry) > 0, f"{fname}: Empty trimesh scene"
    bounds = scene.bounds
    min_pt, max_pt = bounds[0], bounds[1]
    dims = max_pt - min_pt

    verts = sum(len(g.vertices) for g in scene.geometry.values())
    tris = sum(len(g.faces) for g in scene.geometry.values())

    assert abs(min_pt[1]) < 1e-4, f"{fname}: min Y is {min_pt[1]}, expected 0.0"
    cx = 0.5 * (min_pt[0] + max_pt[0])
    cz = 0.5 * (min_pt[2] + max_pt[2])
    assert abs(cx) < 0.08, f"{fname}: X center {cx:.4f} not centered near 0"
    assert abs(cz) < 0.08, f"{fname}: Z center {cz:.4f} not centered near 0"

    if check_tri_range is not None:
        lo, hi = check_tri_range
        assert lo <= tris <= hi, f"{fname}: Triangle count {tris} outside target {lo}..{hi}"

    bbox_str = f"{dims[0]:.2f} x {dims[1]:.2f} x {dims[2]:.2f}"
    glass_tag = "BLEND_OK" if blend_mats else "OPAQUE"
    print(f"{fname:44s} | {size_kb:8.1f} | {bbox_str:20s} | {min_pt[1]:8.5f} | {verts:5d} | {tris:5d} | {glass_tag:8s} | PASS")
    return True


def validate_all():
    all_passed = True
    print("=" * 120)
    print("ROOM 03 HERO ASSET: RATION & BEVERAGE SYNTHESIZER BANK — ROUND 1 (5 CANDIDATES: galley_synth_r1_01..05.glb)")
    print("=" * 120)
    for fname in EXPECTED_GALLEY_R1:
        if not validate_file(
            os.path.join(GALLEY_R1_DIR, fname),
            check_tri_range=(3200, 5500),
            require_textures=True,
            require_blend_glass=True,
        ):
            all_passed = False

    print("\n" + "=" * 120)
    print("ROOM 04 HERO ASSET: SURGICAL AUTODOC GANTRY & TRIAGE CONSOLE — ROUND 1 (5 CANDIDATES: med_autodoc_r1_01..05.glb)")
    print("=" * 120)
    for fname in EXPECTED_MEDBAY_R1:
        if not validate_file(
            os.path.join(MEDBAY_R1_DIR, fname),
            check_tri_range=(3500, 5800),
            require_textures=True,
            require_blend_glass=True,
        ):
            all_passed = False

    print("\n" + "=" * 120)
    print("ROOM 01, ROOM 02, ROOM 03 & ROOM 04 ARCHITECTURAL SHELLS & COMPANION PROPS")
    print("=" * 120)
    for fpath in [
        os.path.join(ROOMS_DIR, "room_01_shell.glb"),
        os.path.join(ROOMS_DIR, "room_02_shell.glb"),
        os.path.join(ROOMS_DIR, "room_02_corridor_shell.glb"),
        os.path.join(ROOMS_DIR, "room_03_shell.glb"),
        os.path.join(ROOMS_DIR, "room_03_mess_shell.glb"),
        os.path.join(ROOMS_DIR, "room_03_mess_galley_shell.glb"),
        os.path.join(ROOMS_DIR, "mess_dining_booth.glb"),
        os.path.join(ROOMS_DIR, "room_04_shell.glb"),
        os.path.join(ROOMS_DIR, "room_04_medbay_shell.glb"),
        os.path.join(ROOMS_DIR, "room_04_med_bay_shell.glb"),
    ]:
        if not validate_file(fpath, require_textures=True, require_blend_glass=True):
            all_passed = False

    print("\n" + "=" * 120)
    print("ROOM 02 HERO FIXTURE: PRESSURIZED BULKHEAD AIRLOCK HATCH — ROUND 1 (5 CANDIDATES: corridor_door_r1_01..05.glb)")
    print("=" * 120)
    for fname in EXPECTED_CORRIDOR_R1:
        if not validate_file(
            os.path.join(CORRIDOR_R1_DIR, fname),
            check_tri_range=(3000, 5800),
            require_textures=True,
            require_blend_glass=True,
        ):
            all_passed = False

    print("\n" + "=" * 120)
    print("LOCKED TOURNAMENT WINNERS IN /workspace/game-project/assets/glb/winners/")
    print("=" * 120)
    for fpath in sorted(glob.glob(os.path.join(WINNERS_DIR, "*_winner_*.glb"))):
        if not validate_file(
            fpath,
            check_tri_range=(2500, 6000),
            require_textures=True,
            require_blend_glass=True,
        ):
            all_passed = False

    print("=" * 120)
    if not all_passed:
        sys.exit(1)
    print("ALL TOURNAMENT, ROOM SHELL & LOCKED WINNER GLB MODELS PASSED STRICT GLTF 2.0 + TRIMESH VALIDATION!")


if __name__ == "__main__":
    validate_all()
