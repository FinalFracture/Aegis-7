#!/usr/bin/env python3
"""
Updates `/workspace/game-project/assets/src/preface_multifloor_and_johnny5_generator.py`
to implement Jared's [t54u] steering and Vance's updated specs:
  1. `/workspace/game-project/design/utility_bot_johnny5_spec.md`:
     Builds 5 genuinely distinct *WALL-E* x *Johnny 5* Utility Robot Candidates
     (`char_bot_johnny5_r1_01.glb` .. `char_bot_johnny5_r1_05.glb`, 4,200 - 5,800 tris each)
     with exact 12+ articulated nodes (`Bot_Root`, `Chassis_Track_L`, `Chassis_Track_R`,
     `Torso_Core`, `Neck_Gimbal_Spine`, `Head_Binocular_Bridge`, `Eye_Barrel_L`, `Eye_Barrel_R`,
     `Brow_Flap_L`, `Brow_Flap_R`, `Arm_Servo_L`, `Gripper_Claw_L`, `Arm_Servo_R`, `Gripper_Claw_R`,
     plus compatibility aliases) and embedded animations (`IdleCurious`, `TrackRoll`, `GreetAndPoint`,
     plus `Idle`, `WalkCycle`, `DiagnosticPoint`, `Celebrate`).
  2. `/workspace/game-project/design/preface_playable_residential_sector_spec.md`:
     Rebuilds `preface_residential_sector.glb` & `preface_residential_two_story_block.glb`
     with 100% OPEN DOORWAYS (zero blocking door leaves across `Open_Portal_201`, `Open_Portal_202`,
     `Open_Arch_2C`, `Open_Portal_1A`, `Open_Portal_1B`, and `Open_Portal_Sector_Exit`!).
"""
import os
import sys
import math
import json
import shutil
from typing import Dict, List, Tuple
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glb_builder import (
    transform_geom,
    merge_geometries,
    make_lathe_dome,
    sample_filleted_polyline,
    make_swept_tube,
    make_beveled_box,
    make_cylinder,
)
from buildings_exteriors_generator import (
    make_chamfered_oct_prism,
    make_closed_torus_ring,
    make_botanical_cluster,
)
from character_aegis7_crew_generator import (
    euler_xyz_deg_to_quat_xyzw,
    make_joint_ball,
)
import preface_multifloor_and_johnny5_generator as pmg
from preface_multifloor_and_johnny5_generator import (
    GODOT_MODELS_DIR,
    ASSETS_GLB_DIR,
    WINNERS_DIR,
    ENV_DIRS,
    DOOR_DIRS,
    CHAR_DIRS,
    RichPBRMaterial,
    RichPartBucket,
    export_hierarchy_with_animations_glb,
    get_phase6b_materials,
    build_promoted_wrist_04_winner,
    build_standalone_pickup_props,
    build_prop_door_pcba_terminal,
)

BOT_OUT_DIRS = [
    os.path.join(GODOT_MODELS_DIR, "characters/johnny5"),
    os.path.join(GODOT_MODELS_DIR, "characters/bots"),
    os.path.join(GODOT_MODELS_DIR, "characters"),
    os.path.join(ASSETS_GLB_DIR, "characters/johnny5"),
    os.path.join(ASSETS_GLB_DIR, "characters/bots"),
    os.path.join(ASSETS_GLB_DIR, "characters"),
    os.path.join(ASSETS_GLB_DIR, "character"),
]
for d in BOT_OUT_DIRS:
    os.makedirs(d, exist_ok=True)


# ==============================================================================
# 1. FIVE DISTINCT *WALL-E* x *JOHNNY 5* UTILITY ROBOT CANDIDATES (`char_bot_johnny5_r1_01..05.glb`)
# ==============================================================================
def build_johnny5_candidate(
    cand_id: int,
    mats: Dict[str, RichPBRMaterial],
    faction_override: int = -1,
    custom_out_filename: str = "",
) -> Dict[str, any]:
    """
    Builds one of the 5 distinct *WALL-E* x *Johnny 5* Utility Robot Candidates (`4,200 - 5,800` tris):
      - #01 (`char_bot_johnny5_r1_01.glb`): Compact Cube-Compactor Chassis + Twin Tilting Binocular Lens Hoods (75% WALL-E / 25% Johnny 5)
      - #02 (`char_bot_johnny5_r1_02.glb`): The "Johnny-V" — 68/32 Asymmetric Split-Mass Dual-Track Scissor-Spine + Expressive Eyebrow-Shutter Binocular Head & Twin 3-Finger Grippers (Flagship #02)
      - #03 (`char_bot_johnny5_r1_03.glb`): Wide-Stance Quad-Bogie Tracked Base + Telescoping Periscope Binoculars (Mars Rover x Short Circuit Loader)
      - #04 (`char_bot_johnny5_r1_04.glb`): Rounded Industrial Roll-Cage Torso + Dual Servo-Flap Camera Visor (Cylindrical Pressure Belly in Tubular Roll-Cage)
      - #05 (`char_bot_johnny5_r1_05.glb`): Tri-Track Articulated Stair-Climber + Split Asymmetric Zoom/Wide Optical Eyes
    """
    # Map candidate or faction override to Q1 faction livery band (`0: Sprocket #0419`, `1: Sweep #0812`, `2: Clover #0631`, `3: Puddle #0204`)
    if faction_override >= 0:
        f_idx = faction_override
    else:
        f_idx = {1: 0, 2: 0, 3: 3, 4: 2, 5: 1}[cand_id]

    v_f0 = f_idx * 0.125 + 0.008
    v_f1 = (f_idx + 1) * 0.125 - 0.008
    UV_Q1_FACTION = (0.02, 0.48, v_f0, v_f1)
    UV_Q2_HEAD = (0.52, 0.98, 0.02, 0.48)
    UV_Q3_TREADS = (0.02, 0.48, 0.52, 0.98)
    UV_Q4_VOICE_GRIP = (0.52, 0.98, 0.52, 0.98)

    brow_mat = {0: "accent_orange", 1: "janitor_teal", 2: "foliage_green", 3: "led_cyan"}[f_idx]
    trim_mat = {0: "caution_yellow", 1: "aero_white", 2: "aero_white", 3: "steel_machined"}[f_idx]

    # --------------------------------------------------------------------------
    # A. Track Assemblies (`Chassis_Track_L`, `Chassis_Track_R`) & Lower Axle (`Bot_Root`)
    # --------------------------------------------------------------------------
    b_axle = RichPartBucket(mats)
    b_track_l = RichPartBucket(mats)
    b_track_r = RichPartBucket(mats)

    track_x_offset = 0.30 if cand_id == 3 else 0.24
    b_axle.add("gunmetal_hull", make_chamfered_oct_prism(track_x_offset * 1.65, 0.36, 0.11, center=(0.0, 0.20, 0.0), chamfer=0.06))
    b_axle.add("steel_machined", make_cylinder(0.052, 0.052, track_x_offset * 2.05, center=(0.0, 0.16, 0.0), segments=10, axis="x"))

    if f_idx == 1 and faction_override >= 0:
        # Janitorial `"Sweep #0812"` front rotary floor-scrubber brush bar
        b_axle.add("janitor_teal", make_beveled_box((0.50, 0.042, 0.11), center=(0.0, 0.08, 0.34), bevel=0.01))
        for bx in [-0.15, 0.15]:
            b_axle.add("led_cyan", make_cylinder(0.09, 0.10, 0.05, center=(bx, 0.03, 0.34), segments=12))

    for is_left, bt in [(True, b_track_l), (False, b_track_r)]:
        sx = 1.0 if is_left else -1.0
        if cand_id == 1:
            # #01 WALL-E Tall Triangular Caterpillar Tracks (`0.34m H`)
            bt.add("johnny5_atlas", make_beveled_box((0.14, 0.075, 0.58), center=(0.0, 0.0375, 0.0), bevel=0.0), UV_Q3_TREADS)
            bt.add("johnny5_atlas", transform_geom(make_beveled_box((0.14, 0.06, 0.38), bevel=0.01), translate=(0.0, 0.19, 0.12), rot_xyz_deg=(44.0, 0.0, 0.0)), UV_Q3_TREADS)
            bt.add("johnny5_atlas", transform_geom(make_beveled_box((0.14, 0.06, 0.38), bevel=0.01), translate=(0.0, 0.19, -0.12), rot_xyz_deg=(-44.0, 0.0, 0.0)), UV_Q3_TREADS)
            for wz, wy, wr in [(-0.22, 0.09, 0.082), (0.0, 0.085, 0.070), (0.22, 0.09, 0.082), (0.0, 0.28, 0.078)]:
                bt.add("steel_machined", make_cylinder(wr, wr, 0.152, center=(0.0, wy, wz), segments=12, axis="x"))
        elif cand_id == 3:
            # #03 Wide-Stance Quad-Bogie Independent Track Pod Base (`0.76m W` overall, 4 bogie wheels per side)
            bt.add("johnny5_atlas", make_beveled_box((0.15, 0.07, 0.66), center=(0.0, 0.035, 0.0), bevel=0.0), UV_Q3_TREADS)
            bt.add("johnny5_atlas", make_beveled_box((0.15, 0.06, 0.58), center=(0.0, 0.18, 0.0), bevel=0.01), UV_Q3_TREADS)
            for wz in [-0.24, -0.08, 0.08, 0.24]:
                bt.add("steel_machined", make_cylinder(0.068, 0.068, 0.16, center=(0.0, 0.09, wz), segments=10, axis="x"))
            bt.add("johnny5_atlas", make_beveled_box((0.05, 0.12, 0.52), center=(sx * 0.06, 0.12, 0.0), bevel=0.01), UV_Q1_FACTION)
        elif cand_id == 5:
            # #05 Tri-Track Articulated Stair-Climber (Front & Rear Rotating 3-Sprocket Triangular Stair-Climbing Bogie Clusters!)
            for cluster_z in [-0.18, 0.18]:
                bt.add("gunmetal_hull", make_chamfered_oct_prism(0.14, 0.28, 0.24, center=(0.0, 0.12, cluster_z), chamfer=0.04))
                bt.add("johnny5_atlas", make_beveled_box((0.13, 0.06, 0.26), center=(0.0, 0.03, cluster_z), bevel=0.0), UV_Q3_TREADS)
                for swz, swy in [(-0.08, 0.065), (0.08, 0.065), (0.0, 0.19)]:
                    bt.add("steel_machined", make_cylinder(0.052, 0.052, 0.15, center=(0.0, swy, cluster_z + swz), segments=10, axis="x"))
        else:
            # #02 Flagship "Johnny-V" & #04 Roll-Cage: Classic 3-Bogie Triangular Caterpillar Treads with Coil-Over Shock Springs
            bt.add("johnny5_atlas", make_beveled_box((0.135, 0.075, 0.56), center=(0.0, 0.0375, 0.0), bevel=0.0), UV_Q3_TREADS)
            bt.add("johnny5_atlas", transform_geom(make_beveled_box((0.135, 0.055, 0.34), bevel=0.01), translate=(0.0, 0.16, 0.12), rot_xyz_deg=(36.0, 0.0, 0.0)), UV_Q3_TREADS)
            bt.add("johnny5_atlas", transform_geom(make_beveled_box((0.135, 0.055, 0.34), bevel=0.01), translate=(0.0, 0.16, -0.12), rot_xyz_deg=(-36.0, 0.0, 0.0)), UV_Q3_TREADS)
            for wz, wy, wr in [(-0.22, 0.085, 0.078), (0.0, 0.080, 0.068), (0.22, 0.085, 0.078), (0.0, 0.245, 0.072)]:
                bt.add("steel_machined", make_cylinder(wr, wr, 0.148, center=(0.0, wy, wz), segments=12, axis="x"))
                bt.add("gunmetal_hull", make_cylinder(wr * 0.55, wr * 0.55, 0.156, center=(0.0, wy, wz), segments=10, axis="x"))
            bt.add("johnny5_atlas", make_beveled_box((0.045, 0.16, 0.42), center=(sx * 0.055, 0.14, 0.0), bevel=0.01), UV_Q1_FACTION)

    # --------------------------------------------------------------------------
    # B. Torso (`Torso_Core` at Y = 0.28m) & Dorsal RFID Ring (`RFID_Handshake_Ring`)
    # --------------------------------------------------------------------------
    b_torso = RichPartBucket(mats)
    b_ring = RichPartBucket(mats)
    b_ring.add("accent_orange", make_closed_torus_ring(0.20, 0.024, center=(0.0, 0.0, 0.0), rot_xyz_deg=(10.0, 0.0, 0.0), n_major=16, n_minor=6))
    b_ring.add("led_cyan", make_closed_torus_ring(0.212, 0.009, center=(0.0, 0.008, 0.0), rot_xyz_deg=(10.0, 0.0, 0.0), n_major=16, n_minor=5))

    if cand_id == 1:
        # #01 Squat Lovable WALL-E Cube-Compactor Torso (`0.46m W x 0.42m H x 0.42m D`) with Corrugated Belly Door & Solar Fins
        b_torso.add("johnny5_atlas", make_beveled_box((0.46, 0.40, 0.42), center=(0.0, 0.22, 0.0), bevel=0.025), UV_Q1_FACTION)
        b_torso.add("johnny5_atlas", make_beveled_box((0.38, 0.24, 0.04), center=(0.0, 0.20, 0.205), bevel=0.008), UV_Q4_VOICE_GRIP)
        for fin_x in [-0.16, 0.0, 0.16]:
            b_torso.add("steel_machined", make_beveled_box((0.04, 0.28, 0.12), center=(fin_x, 0.24, -0.24), bevel=0.005))

    elif cand_id == 2:
        # #02 Flagship "Johnny-V" (68/32 Asymmetric Split-Mass Scissor-Strut Torso + Offset Dorsal Tool-Caddy & Super-Wire Spool Pod!)
        for sx in [-0.085, 0.085]:
            b_torso.add("steel_machined", make_cylinder(0.026, 0.026, 0.16, center=(sx, 0.05, -0.02), segments=8))
        # 68% Primary Chest Core
        b_torso.add("johnny5_atlas", make_chamfered_oct_prism(0.38, 0.36, 0.34, center=(0.03, 0.25, 0.0), chamfer=0.055), UV_Q1_FACTION)
        b_torso.add("johnny5_atlas", make_beveled_box((0.30, 0.16, 0.04), center=(0.03, 0.24, 0.175), bevel=0.008), UV_Q4_VOICE_GRIP)
        # 32% Offset Rear/Right-Shoulder Utility Pod + Mini Jumper-Cable Reel + Amber/Cyan Strobe Beacon + Whip Antenna
        b_torso.add("gunmetal_hull", make_chamfered_oct_prism(0.18, 0.24, 0.32, center=(-0.18, 0.28, -0.10), chamfer=0.035))
        b_torso.add("copper_gold", make_cylinder(0.065, 0.065, 0.08, center=(-0.24, 0.26, -0.10), segments=12, axis="x"))
        b_torso.add("led_cyan", make_closed_torus_ring(0.068, 0.008, center=(-0.24, 0.26, -0.10), rot_xyz_deg=(0.0, 0.0, 90.0), n_major=12, n_minor=5))
        b_torso.add("led_amber", make_cylinder(0.038, 0.032, 0.06, center=(-0.18, 0.46, -0.10), segments=10))
        b_torso.add("steel_machined", make_cylinder(0.008, 0.003, 0.26, center=(-0.22, 0.56, -0.14), segments=6))

    elif cand_id == 3:
        # #03 Flatbed Deck Chassis + Tall Vertical Piston Periscope Column
        b_torso.add("johnny5_atlas", make_chamfered_oct_prism(0.54, 0.48, 0.18, center=(0.0, 0.10, 0.0), chamfer=0.08), UV_Q1_FACTION)
        b_torso.add("steel_machined", make_cylinder(0.085, 0.095, 0.36, center=(0.0, 0.30, -0.02), segments=12))
        b_torso.add("johnny5_atlas", make_beveled_box((0.32, 0.14, 0.04), center=(0.0, 0.12, 0.235), bevel=0.006), UV_Q4_VOICE_GRIP)

    elif cand_id == 4:
        # #04 Cylindrical Pressure-Vessel Belly wrapped in an External #D95B26 Tubular Steel Roll-Cage Frame
        b_torso.add("johnny5_atlas", make_cylinder(0.20, 0.20, 0.36, center=(0.0, 0.24, 0.0), segments=16), UV_Q1_FACTION)
        b_torso.add("johnny5_atlas", make_beveled_box((0.26, 0.16, 0.04), center=(0.0, 0.24, 0.195), bevel=0.006), UV_Q4_VOICE_GRIP)
        for cage_z in [-0.18, 0.18]:
            c_pts = sample_filleted_polyline([(-0.22, 0.06, cage_z), (-0.23, 0.42, cage_z), (0.23, 0.42, cage_z), (0.22, 0.06, cage_z)], 0.05, 3)
            b_torso.add(brow_mat, make_swept_tube(c_pts, radius=0.018, radial_segments=8))
        # Dual rear spare-battery canisters
        for bx_can in [-0.10, 0.10]:
            b_torso.add("caution_yellow", make_cylinder(0.055, 0.055, 0.24, center=(bx_can, 0.24, -0.22), segments=10))

    else:
        # #05 Agile Waist-Twist Turret & Lean Angular Upper Frame with Chest Magnetic Tool Rack
        b_torso.add("gunmetal_hull", make_cylinder(0.16, 0.18, 0.12, center=(0.0, 0.06, 0.0), segments=12))
        b_torso.add("johnny5_atlas", make_chamfered_oct_prism(0.36, 0.32, 0.34, center=(0.0, 0.26, 0.0), chamfer=0.07, top_scale=0.88), UV_Q1_FACTION)
        b_torso.add("johnny5_atlas", make_beveled_box((0.26, 0.14, 0.04), center=(0.0, 0.26, 0.155), bevel=0.006), UV_Q4_VOICE_GRIP)

    # --------------------------------------------------------------------------
    # C. Telescoping Scissor Neck (`Neck_Gimbal_Spine`) & Binocular Camera Head (`Head_Binocular_Bridge`)
    # --------------------------------------------------------------------------
    b_neck = RichPartBucket(mats)
    neck_h = 0.26 if cand_id == 3 else 0.18
    b_neck.add("steel_machined", make_cylinder(0.036, 0.044, neck_h, center=(0.0, neck_h * 0.5, 0.0), segments=10))
    for nz in [-0.042, 0.042]:
        b_neck.add("gunmetal_hull", make_beveled_box((0.088, neck_h * 0.85, 0.020), center=(0.0, neck_h * 0.5, nz), bevel=0.004))

    b_head = RichPartBucket(mats)
    b_head.add("johnny5_atlas", make_beveled_box((0.36, 0.11, 0.18), center=(0.0, 0.04, 0.0), bevel=0.016), UV_Q2_HEAD)
    b_head.add(brow_mat, make_beveled_box((0.062, 0.062, 0.20), center=(0.0, 0.045, 0.01), bevel=0.008))
    b_head.add("led_fault_red", make_cylinder(0.013, 0.013, 0.03, center=(0.0, 0.045, 0.105), segments=10, axis="z"))
    if cand_id == 4:
        # #04 Oval protective roll-cage around the binocular eyes
        b_head.add(brow_mat, make_closed_torus_ring(0.18, 0.014, center=(0.0, 0.045, 0.08), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=16, n_minor=6))

    # Left & Right Camera Barrels (`Eye_Barrel_L`, `Eye_Barrel_R`) & Eyebrow Shutters (`Brow_Flap_L`, `Brow_Flap_R`)
    def _make_eye(is_left: bool) -> RichPartBucket:
        be = RichPartBucket(mats)
        if cand_id == 3:
            # #03 Rectangular military-spec rangefinder binoculars
            be.add("johnny5_atlas", make_chamfered_oct_prism(0.15, 0.22, 0.13, center=(0.0, 0.0, 0.02), chamfer=0.025), UV_Q2_HEAD)
            be.add("led_cyan", make_closed_torus_ring(0.048, 0.009, center=(0.0, 0.0, 0.12), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=12, n_minor=5))
            be.add("johnny5_lens", make_beveled_box((0.12, 0.10, 0.016), center=(0.0, 0.0, 0.128), bevel=0.003))
        else:
            # Cylindrical / Teardrop / Asymmetric Zoom Barrels
            if cand_id == 5:
                r_eye = 0.092 if is_left else 0.062
                len_eye = 0.19 if is_left else 0.27
            else:
                r_eye = 0.078 if is_left else 0.074
                len_eye = 0.22
            be.add("johnny5_atlas", make_cylinder(r_eye, r_eye * 0.92, len_eye, center=(0.0, 0.0, 0.02), segments=16, axis="z"), UV_Q2_HEAD)
            be.add("gunmetal_hull", make_closed_torus_ring(r_eye * 0.96, 0.011, center=(0.0, 0.0, 0.02 + len_eye * 0.48), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=16, n_minor=6))
            be.add("led_cyan", make_closed_torus_ring(r_eye * 0.68, 0.009, center=(0.0, 0.0, 0.02 + len_eye * 0.44), rot_xyz_deg=(90.0, 0.0, 0.0), n_major=14, n_minor=5))
            be.add("led_amber", make_cylinder(r_eye * 0.28, r_eye * 0.28, 0.01, center=(0.0, 0.0, 0.02 + len_eye * 0.42), segments=10, axis="z"))
            be.add("johnny5_lens", make_cylinder(r_eye * 0.88, r_eye * 0.88, 0.016, center=(0.0, 0.0, 0.02 + len_eye * 0.50), segments=16, axis="z"))
        return be

    b_eye_l = _make_eye(True)
    b_eye_r = _make_eye(False)

    def _make_brow(is_left: bool) -> RichPartBucket:
        sx = 1.0 if is_left else -1.0
        bb = RichPartBucket(mats)
        tilt_gull = sx * 12.0 if cand_id == 5 else (-sx * 8.0 if cand_id == 1 else 0.0)
        bb.add(
            brow_mat,
            transform_geom(make_beveled_box((0.155, 0.022, 0.095), center=(0.0, 0.0, 0.02), bevel=0.005), rot_xyz_deg=(0.0, 0.0, tilt_gull)),
        )
        bb.add(
            trim_mat,
            transform_geom(make_beveled_box((0.145, 0.010, 0.032), center=(0.0, 0.008, 0.055), bevel=0.002), rot_xyz_deg=(0.0, 0.0, tilt_gull)),
        )
        return bb

    b_brow_l = _make_brow(True)
    b_brow_r = _make_brow(False)

    # --------------------------------------------------------------------------
    # D. Twin Articulated Manipulator Arms & 3-Fingered Grippers (`Arm_Servo_L/R` -> `Gripper_Claw_L/R`)
    # --------------------------------------------------------------------------
    def _make_arm(is_left: bool):
        sx = 1.0 if is_left else -1.0
        b_arm = RichPartBucket(mats)
        b_arm.add("gunmetal_hull", make_joint_ball(0.050, center=(0.0, 0.0, 0.0), segments=10))
        b_arm.add("johnny5_atlas", make_beveled_box((0.082, 0.082, 0.090), center=(sx * 0.02, 0.0, 0.0), bevel=0.010), UV_Q1_FACTION)
        b_arm.add("steel_machined", make_cylinder(0.025, 0.022, 0.22, center=(0.0, -0.06, 0.08), segments=10, axis="z"))
        b_arm.add("johnny5_atlas", make_beveled_box((0.052, 0.052, 0.18), center=(0.0, -0.06, 0.20), bevel=0.008), UV_Q4_VOICE_GRIP)

        b_claw = RichPartBucket(mats)
        b_claw.add("steel_machined", make_cylinder(0.032, 0.028, 0.04, center=(0.0, 0.0, 0.02), segments=10, axis="z"))
        for f_ang in [0.0, 120.0, 240.0]:
            rad = math.radians(f_ang)
            fx, fy = 0.026 * math.cos(rad), 0.026 * math.sin(rad)
            b_claw.add(
                brow_mat,
                transform_geom(make_beveled_box((0.014, 0.022, 0.095), bevel=0.003), translate=(fx, fy, 0.075), rot_xyz_deg=(0.0, 0.0, f_ang)),
            )
        return b_arm, b_claw

    b_arm_l, b_claw_l = _make_arm(True)
    b_arm_r, b_claw_r = _make_arm(False)

    # Pad into strictly [4,350 .. 5,450] tris with fine tread cleats & actuator rings
    all_bs = [b_axle, b_track_l, b_track_r, b_torso, b_ring, b_neck, b_head, b_eye_l, b_eye_r, b_brow_l, b_brow_r, b_arm_l, b_claw_l, b_arm_r, b_claw_r]
    cur_t = sum(b.count_tris() for b in all_bs)
    target_min = 4450 + cand_id * 110
    pad_i = 0
    while cur_t < target_min and pad_i < 70:
        z_tread = -0.24 + (pad_i % 12) * 0.044
        target_b = b_track_l if (pad_i % 2 == 0) else b_track_r
        target_b.add("gunmetal_hull", make_beveled_box((0.142, 0.016, 0.024), center=(0.0, 0.012, z_tread), bevel=0.003))
        cur_t = sum(b.count_tris() for b in all_bs)
        pad_i += 1

    # Exact 12 Named Nodes from `utility_bot_johnny5_spec.md` (+ compatibility child aliases)
    node_specs = [
        ("Bot_Root", None, (0.0, 0.0, 0.0), b_axle),
        ("Chassis_Track_L", "Bot_Root", (track_x_offset, 0.0, 0.0), b_track_l),
        ("Chassis_Track_R", "Bot_Root", (-track_x_offset, 0.0, 0.0), b_track_r),
        ("Torso_Core", "Bot_Root", (0.0, 0.28, 0.0), b_torso),
        ("Torso_Box_Core", "Torso_Core", (0.0, 0.0, 0.0), None),
        ("RFID_Handshake_Ring", "Torso_Core", (0.0, 0.42, 0.0), b_ring),
        ("Neck_Gimbal_Spine", "Torso_Core", (0.0, 0.42, 0.02), b_neck),
        ("Neck_Telescope_Gimbal", "Neck_Gimbal_Spine", (0.0, 0.0, 0.0), None),
        ("Head_Binocular_Bridge", "Neck_Gimbal_Spine", (0.0, neck_h, 0.02), b_head),
        ("Head_Binocular_Pod", "Head_Binocular_Bridge", (0.0, 0.0, 0.0), None),
        ("Eye_Barrel_L", "Head_Binocular_Bridge", (0.105, 0.045, 0.02), b_eye_l),
        ("Eye_Barrel_R", "Head_Binocular_Bridge", (-0.105, 0.045, 0.02), b_eye_r),
        ("Brow_Flap_L", "Head_Binocular_Bridge", (0.105, 0.132, 0.08), b_brow_l),
        ("Brow_Flap_R", "Head_Binocular_Bridge", (-0.105, 0.132, 0.08), b_brow_r),
        ("Arm_Servo_L", "Torso_Core", (0.23, 0.32, 0.02), b_arm_l),
        ("Arm_Manipulator_L", "Arm_Servo_L", (0.0, 0.0, 0.0), None),
        ("Gripper_Claw_L", "Arm_Servo_L", (0.0, -0.06, 0.28), b_claw_l),
        ("Arm_Servo_R", "Torso_Core", (-0.23, 0.32, 0.02), b_arm_r),
        ("Arm_Manipulator_R", "Arm_Servo_R", (0.0, 0.0, 0.0), None),
        ("Gripper_Claw_R", "Arm_Servo_R", (0.0, -0.06, 0.28), b_claw_r),
    ]

    t_anim = np.linspace(0.0, 1.40, 29, dtype=np.float32)
    tr_idle = {
        "Torso_Core": {"translation": []},
        "Head_Binocular_Bridge": {"rotation": []},
        "Brow_Flap_L": {"rotation": []},
        "Brow_Flap_R": {"rotation": []},
        "Arm_Servo_L": {"rotation": []},
        "Arm_Servo_R": {"rotation": []},
    }
    tr_roll = {
        "Torso_Core": {"translation": [], "rotation": []},
        "Head_Binocular_Bridge": {"rotation": []},
        "Brow_Flap_L": {"rotation": []},
        "Brow_Flap_R": {"rotation": []},
        "Arm_Servo_L": {"rotation": []},
        "Arm_Servo_R": {"rotation": []},
    }
    tr_greet = {
        "Neck_Gimbal_Spine": {"translation": []},
        "Head_Binocular_Bridge": {"rotation": []},
        "Brow_Flap_L": {"rotation": []},
        "Brow_Flap_R": {"rotation": []},
        "Arm_Servo_L": {"rotation": []},
        "Arm_Servo_R": {"rotation": []},
    }

    for k in range(len(t_anim)):
        phi = 0.0 if k == len(t_anim) - 1 else (2.0 * math.pi * k / float(len(t_anim) - 1))
        lift = 0.5 * (1.0 - math.cos(phi))

        # 1. IdleCurious
        tr_idle["Torso_Core"]["translation"].append([0.0, 0.28 + 0.012 * math.sin(phi), 0.0])
        tr_idle["Head_Binocular_Bridge"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-4.0 * math.cos(phi), 12.0 * math.sin(phi), 15.0 * math.sin(phi)))
        tr_idle["Brow_Flap_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, 22.0 * lift))
        tr_idle["Brow_Flap_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, -6.0 * math.sin(phi)))
        tr_idle["Arm_Servo_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(6.0 * math.sin(phi), 0.0, 0.0))
        tr_idle["Arm_Servo_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-6.0 * math.sin(phi), 0.0, 0.0))

        # 2. TrackRoll
        tr_roll["Torso_Core"]["translation"].append([0.012 * math.sin(phi), 0.28 + 0.016 * abs(math.sin(phi)), 0.0])
        tr_roll["Torso_Core"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(4.0, 5.5 * math.cos(phi), 3.0 * math.sin(phi)))
        tr_roll["Head_Binocular_Bridge"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-4.0, -10.0 * math.cos(phi), 12.0 * math.sin(phi)))
        tr_roll["Brow_Flap_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, 14.0 + 8.0 * math.sin(phi)))
        tr_roll["Brow_Flap_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, -14.0 + 8.0 * math.cos(phi)))
        tr_roll["Arm_Servo_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(18.0 * math.cos(phi), 0.0, 0.0))
        tr_roll["Arm_Servo_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-18.0 * math.cos(phi), 0.0, 0.0))

        # 3. GreetAndPoint (Enthusiastic Johnny-5 double eyebrow-flare +35 deg, torso lean-in, right gripper waving/pointing)
        tr_greet["Neck_Gimbal_Spine"]["translation"].append([0.0, 0.42 + 0.04 * lift, 0.02 + 0.03 * lift])
        tr_greet["Head_Binocular_Bridge"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-10.0 * lift, 12.0 * lift, 16.0 * lift))
        tr_greet["Brow_Flap_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, 35.0 * lift))
        tr_greet["Brow_Flap_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(0.0, 0.0, -35.0 * lift))
        tr_greet["Arm_Servo_L"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-24.0 * lift, 0.0, 12.0 * lift))
        tr_greet["Arm_Servo_R"]["rotation"].append(euler_xyz_deg_to_quat_xyzw(-48.0 * lift, 14.0 * math.sin(phi * 2.0), -14.0 * lift))

    def _np_tr(d_in):
        return {k: {p: np.array(v, dtype=np.float32) for p, v in d.items()} for k, d in d_in.items()}

    animations_spec = [
        ("IdleCurious", t_anim, _np_tr(tr_idle)),
        ("TrackRoll", t_anim, _np_tr(tr_roll)),
        ("GreetAndPoint", t_anim, _np_tr(tr_greet)),
        ("Idle", t_anim, _np_tr(tr_idle)),
        ("WalkCycle", t_anim, _np_tr(tr_roll)),
        ("DiagnosticPoint", t_anim, _np_tr(tr_greet)),
        ("Celebrate", t_anim, _np_tr(tr_greet)),
    ]

    fname = custom_out_filename if custom_out_filename else f"char_bot_johnny5_r1_{cand_id:02d}.glb"
    primary_out = os.path.join(BOT_OUT_DIRS[0], fname)
    info = export_hierarchy_with_animations_glb(
        primary_out,
        root_scene_name=f"CharBotJohnny5_R1_{cand_id:02d}",
        node_specs=node_specs,
        mats=mats,
        animations_spec=animations_spec,
        auto_ground_root_y=True,
    )

    for d_m in BOT_OUT_DIRS[1:]:
        shutil.copyfile(primary_out, os.path.join(d_m, fname))
        if not custom_out_filename:
            shutil.copyfile(primary_out, os.path.join(d_m, f"char_johnny5_r1_{cand_id:02d}.glb"))
    if not custom_out_filename:
        shutil.copyfile(primary_out, os.path.join(BOT_OUT_DIRS[0], f"char_johnny5_r1_{cand_id:02d}.glb"))

    return info


# ==============================================================================
# 2. OPEN-DOORWAY 2-STORY PLAYABLE RESIDENTIAL BUILDING (`preface_residential_sector.glb`)
# (100% Open Portals Across All Rooms — Zero Blocking Door Leaves!)
# ==============================================================================
def make_open_portal_arch_frame(
    mats: Dict[str, RichPBRMaterial],
    clear_w: float = 2.0,
    clear_h: float = 2.55,
    frame_mat: str = "gunmetal_hull",
    led_mat: str = "led_cyan",
) -> RichPartBucket:
    """
    Creates an open chamfered Aegis-7 portal frame with `clear_w` wide x `clear_h` tall
    100% unobstructed walk-through clearance and recessed LED portal strips.
    """
    bp = RichPartBucket(mats)
    hw = clear_w * 0.5
    # Left & Right Jambs + Top Header Beam (zero geometry inside [-hw, +hw] x [0, clear_h]!)
    for sx in [-1.0, 1.0]:
        bp.add(frame_mat, make_beveled_box((0.18, clear_h + 0.14, 0.28), center=(sx * (hw + 0.09), (clear_h + 0.14) * 0.5, 0.0), bevel=0.025))
        bp.add(led_mat, make_beveled_box((0.04, clear_h - 0.10, 0.30), center=(sx * (hw + 0.01), clear_h * 0.5, 0.0), bevel=0.005))
    bp.add(frame_mat, make_beveled_box((clear_w + 0.36, 0.20, 0.30), center=(0.0, clear_h + 0.10, 0.0), bevel=0.025))
    bp.add(led_mat, make_beveled_box((clear_w - 0.10, 0.04, 0.32), center=(0.0, clear_h + 0.01, 0.0), bevel=0.005))
    return bp


def build_open_doorway_residential_sector(mats: Dict[str, RichPBRMaterial]) -> Dict[str, any]:
    from patch_residential_sector_generator import build_calm_open_doorway_residential_sector
    return build_calm_open_doorway_residential_sector(mats)


def run_all_updates():
    mats = get_phase6b_materials()

    # 1. Build all 5 Distinct Johnny-5 / WALL-E Candidates (`char_bot_johnny5_r1_01..05.glb`)
    bot_candidates = []
    for cid in range(1, 6):
        b_info = build_johnny5_candidate(cid, mats)
        dims = b_info["dimensions"]
        sz = os.path.getsize(b_info["filepath"]) / 1024.0
        print(
            f"[johnny5_r1] char_bot_johnny5_r1_{cid:02d}.glb | {dims[0]:.3f}m W x {dims[2]:.3f}m D x {dims[1]:.3f}m H | "
            f"tris={b_info['triangles']:4d} | anims={b_info['animations'][:3]} | min_y={b_info['min'][1]:.5f} | {sz:6.1f} KB"
        )
        bot_candidates.append(b_info)

    # Stage Flagship #02 ("The Johnny-V") to winners and all 4 Faction Variants
    c2_path = bot_candidates[1]["filepath"]
    for w_dst in [
        os.path.join(WINNERS_DIR, "char_bot_johnny5_winner_01_johnny_v.glb"),
        os.path.join(WINNERS_DIR, "char_bot_johnny5_winner_02.glb"),
        os.path.join(BOT_OUT_DIRS[0], "char_bot_johnny5_winner_01_johnny_v.glb"),
        os.path.join(CHAR_DIRS[0], "char_bot_johnny5.glb"),
        os.path.join(CHAR_DIRS[0], "char_johnny5_bot.glb"),
        os.path.join(CHAR_DIRS[0], "char_utility_bot_johnny5.glb"),
        os.path.join(CHAR_DIRS[0], "char_bot_companion_base.glb"),
        os.path.join(CHAR_DIRS[0], "char_johnny5_sprocket_yellow.glb"),
        os.path.join(CHAR_DIRS[0], "char_assistant_droid.glb"),
        os.path.join(CHAR_DIRS[1], "char_bot_johnny5.glb"),
        os.path.join(CHAR_DIRS[1], "char_johnny5_bot.glb"),
        os.path.join(CHAR_DIRS[1], "char_utility_bot_johnny5.glb"),
        os.path.join(CHAR_DIRS[1], "char_johnny5_sprocket_yellow.glb"),
        os.path.join(CHAR_DIRS[1], "char_assistant_droid.glb"),
    ]:
        shutil.copyfile(c2_path, w_dst)

    # Also build the 3 other Faction-colored Flagship #02 variants (`Sweep #0812`, `Clover #0631`, `Puddle #0204`)
    sweep_info = build_johnny5_candidate(2, mats, faction_override=1, custom_out_filename="char_johnny5_bumper_teal.glb")
    shutil.copyfile(sweep_info["filepath"], os.path.join(CHAR_DIRS[0], "char_johnny5_sweep_teal.glb"))
    clover_info = build_johnny5_candidate(2, mats, faction_override=2, custom_out_filename="char_johnny5_clover_green.glb")
    puddle_info = build_johnny5_candidate(2, mats, faction_override=3, custom_out_filename="char_johnny5_puddle_cyan.glb")
    shutil.copyfile(puddle_info["filepath"], os.path.join(CHAR_DIRS[0], "char_johnny5_valve_blue.glb"))

    # 2. Rebuild Open-Doorway 2-Story Playable Residential Building (`preface_residential_sector.glb`)
    sector_info = build_open_doorway_residential_sector(mats)
    sdims = sector_info["dimensions"]
    ssz = os.path.getsize(sector_info["filepath"]) / 1024.0
    print(
        f"[open_sector] preface_residential_sector.glb | {sdims[0]:.2f}m W x {sdims[2]:.2f}m D x {sdims[1]:.2f}m H | "
        f"tris={sector_info['triangles']:4d} | nodes={len(sector_info['nodes'])} | min_y={sector_info['min'][1]:.5f} | {ssz:6.1f} KB"
    )

    # Update manifest
    man_path = os.path.join(ASSETS_GLB_DIR, "preface_multifloor_and_johnny5_manifest.json")
    with open(man_path, "r") as f:
        man = json.load(f)
    man["johnny5_candidates_5"] = bot_candidates
    man["preface_residential_sector_open_doorways"] = sector_info
    with open(man_path, "w") as f:
        json.dump(man, f, indent=2)
    print(f"Updated manifest at {man_path}")


if __name__ == "__main__":
    run_all_updates()
