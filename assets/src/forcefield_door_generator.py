#!/usr/bin/env python3
"""
RFID Force-Field Door (Residential Sector) - rfid_forcefield_door.glb
Clear opening 1.50 m x 2.45 m. Flush sci-fi frame lives entirely INSIDE a 0.30 m wall
(frame depth 0.28 m, centered on Z=0 -> z in [-0.14, +0.14]; wall faces at +/-0.15).
Nodes: Frame, EmitterStrip, RFIDPanel, StatusLight, FieldPlane.
Pivot bottom-center (0,0,0), +Z = player-facing side. Field plane UV 0..1 over whole opening.
Shader: godot/shaders/forcefield_door.gdshader (apply to FieldPlane in Godot).
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from glb_builder import SubMesh, PBRMaterialDef, make_beveled_box, make_quad_panel, export_glb

OUT = "/workspace/game-project/godot/assets/models/rfid_forcefield_door.glb"

OPEN_W, OPEN_H = 1.50, 2.45
WALL_T = 0.30                 # residential portal wall (door trim faces at z=+/-0.150 in preface_playable_area.gd)
FRAME_D = 0.28                # <= WALL_T, centered
HZ = FRAME_D * 0.5            # 0.14
LINER = 0.16                  # frame band width around opening
GROOVE = 0.04                 # emitter groove width (z) at wall center
OUT_W = OPEN_W + 2 * LINER    # 1.82 wall cutout width
OUT_H = OPEN_H + LINER        # 2.61 wall cutout height

GLOW = (0.72, 0.35, 1.0)       # field/emitter glow tint for this pass (violet-magenta); runtime color comes from shader field_color
M_FRAME = PBRMaterialDef("Mat_FF_Frame_PearlCeramic", (0.78, 0.80, 0.83, 1.0), 0.35, 0.38)
M_INSET = PBRMaterialDef("Mat_FF_Frame_GraphiteInset", (0.14, 0.15, 0.18, 1.0), 0.6, 0.45)
M_EMIT = PBRMaterialDef("Mat_FF_EmitterStrip_Glow", GLOW + (1.0,), 0.0, 0.3, emissive=GLOW)
M_NODES = PBRMaterialDef("Mat_FF_EmitterNodes_Glow", GLOW + (1.0,), 0.0, 0.25, emissive=GLOW)
M_COND = PBRMaterialDef("Mat_FF_Conduits_LightPipe", GLOW + (1.0,), 0.0, 0.3, emissive=tuple(c * 0.8 for c in GLOW))
M_HAZ = PBRMaterialDef("Mat_FF_Threshold_Chevron", (0.80, 0.66, 0.18, 1.0), 0.1, 0.5)
M_PANEL = PBRMaterialDef("Mat_FF_RFIDPanel_Glass", (0.07, 0.09, 0.11, 1.0), 0.4, 0.2)
M_LIGHT = PBRMaterialDef("Mat_FF_StatusLight_Amber", (1.0, 0.62, 0.12, 1.0), 0.0, 0.3, emissive=(1.0, 0.62, 0.12))
M_FIELD = PBRMaterialDef("Mat_FF_FieldPlane", GLOW + (0.45,), 0.0, 0.1,
                         emissive=tuple(c * 0.6 for c in GLOW), double_sided=True, alpha_mode="BLEND")


def merge(parts):
    P, N, U, I = [], [], [], []
    off = 0
    for p, n, u, i in parts:
        P.append(p); N.append(n); U.append(u); I.append(i + off); off += len(p)
    return (np.vstack(P).astype(np.float32), np.vstack(N).astype(np.float32),
            np.vstack(U).astype(np.float32), np.vstack(I).astype(np.uint32))


def box(size, center, bevel=0.012, rot_z_deg=0.0):
    p, n, u, i = make_beveled_box(size, (0.0, 0.0, 0.0), bevel=bevel)
    if rot_z_deg:
        a = np.radians(rot_z_deg)
        R = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]], dtype=np.float32)
        p = p @ R.T; n = n @ R.T
    return p + np.array(center, dtype=np.float32), n, u, i


def ring(parts, o0, o1, z0, z1, bevel):
    """U-shaped band around the opening between offsets o0..o1 from the opening edge, spanning z0..z1."""
    hw = OPEN_W * 0.5
    d, zc = z1 - z0, (z0 + z1) * 0.5
    w = o1 - o0
    top = OPEN_H + o1
    for sx in (1, -1):
        parts.append(box((w, top, d), (sx * (hw + o0 + w * 0.5), top * 0.5, zc), bevel))
    parts.append(box((OPEN_W + 2 * o0, w, d), (0.0, OPEN_H + o0 + w * 0.5, zc), bevel))


def build():
    hw = OPEN_W * 0.5
    frame, inset, emit, nodes, cond, haz = [], [], [], [], [], []
    g = GROOVE * 0.5
    # Stepped, layered bezel (steps down toward the field like a structural portal):
    #   A inner liner (split by emitter groove)  0.000-0.050  z +/-0.095  pearl
    #   B conduit channel                         0.050-0.085  z +/-0.112  graphite (also groove back)
    #   C middle step                             0.085-0.120  z +/-0.126  pearl
    #   D outer structural ring                   0.120-0.160  z +/-0.140  pearl
    for zs in (1, -1):
        z0, z1 = sorted((zs * g, zs * 0.095))
        ring(frame, 0.0, 0.050, z0, z1, 0.012)
    ring(inset, 0.050, 0.085, -0.112, 0.112, 0.0)
    ring(frame, 0.085, 0.120, -0.126, 0.126, 0.010)
    ring(frame, 0.120, LINER, -HZ, HZ, 0.015)

    for zs in (1, -1):
        # Panel seams on the outer ring (crisp graphite cuts), front face sits at 0.142 (<0.150)
        zf = zs * (HZ + 0.001)
        for y in (0.62, 1.30, 1.98):
            for sx in (1, -1):
                inset.append(box((0.040, 0.006, 0.004), (sx * (hw + 0.140), y, zf), 0.0))
        for x in (-0.45, 0.45):
            inset.append(box((0.006, 0.040, 0.004), (x, OPEN_H + 0.140, zf), 0.0))
        # Segmented light pipes in the conduit channel (B), face at 0.118
        zc = zs * 0.1155
        seg_n, y0, y1 = 11, 0.30, OPEN_H - 0.02
        L = (y1 - y0) / seg_n
        for sx in (1, -1):
            for k in range(seg_n):
                cond.append(box((0.018, L * 0.78, 0.007), (sx * (hw + 0.0675), y0 + L * (k + 0.5), zc), 0.0))
        hn = 6
        Lh = (OPEN_W - 0.20) / hn
        for k in range(hn):
            cond.append(box((Lh * 0.78, 0.018, 0.007), (-hw + 0.10 + Lh * (k + 0.5), OPEN_H + 0.0675, zc), 0.0))
        # Corner emitter brackets: angled graphite housings at top corners, upright ones at floor corners,
        # each with a glowing projector pip aimed at the field.
        for sx in (1, -1):
            inset.append(box((0.13, 0.036, 0.040), (sx * (hw + 0.055), OPEN_H + 0.055, zs * 0.115), 0.006, rot_z_deg=-45.0 * sx))
            nodes.append(box((0.040, 0.016, 0.010), (sx * (hw + 0.040), OPEN_H + 0.040, zs * 0.137), 0.0, rot_z_deg=-45.0 * sx))
            inset.append(box((0.036, 0.22, 0.040), (sx * (hw + 0.055), 0.30 - 0.11, zs * 0.115), 0.006))
            nodes.append(box((0.016, 0.06, 0.010), (sx * (hw + 0.050), 0.24, zs * 0.137), 0.0))
            # Threshold chevrons: graphite kick plate on the outer ring at floor + crisp hazard chevrons
            inset.append(box((0.038, 0.22, 0.004), (sx * (hw + 0.140), 0.11, zs * (HZ + 0.001)), 0.0))
            for k in range(3):
                haz.append(box((0.008, 0.040, 0.003), (sx * (hw + 0.140), 0.045 + k * 0.065, zs * (HZ + 0.004)), 0.0, rot_z_deg=40.0 * sx))
    # Emitter lenses in the groove at the 4 corners (where the field is projected from), flush with opening edge
    for sx in (1, -1):
        for y in (0.06, OPEN_H - 0.06):
            nodes.append(box((0.045, 0.12, GROOVE * 0.9), (sx * (hw + 0.0235), y, 0.0), 0.004))
    # Emitter strip: recessed 10 mm back from the opening edge, inside the groove
    es_t, rec = 0.012, 0.010
    for sx in (1, -1):
        emit.append(box((es_t, OPEN_H + rec, GROOVE * 0.6), (sx * (hw + rec + es_t * 0.5), (OPEN_H + rec) * 0.5, 0.0), 0.0))
    emit.append(box((OPEN_W + 2 * rec + 2 * es_t, es_t, GROOVE * 0.6), (0.0, OPEN_H + rec + es_t * 0.5, 0.0), 0.0))

    # RFID panel: flush in wall face beside opening (+X side, front), front face at z=0.148 (< 0.15)
    px = hw + LINER + 0.22
    panel = [box((0.14, 0.24, 0.03), (px, 1.25, 0.148 - 0.015), 0.006)]
    light = [box((0.08, 0.016, 0.006), (px, 1.33, 0.149 - 0.003), 0.0)]

    # Field plane: single quad filling the clear opening at wall center, UV 0..1
    fp = make_quad_panel((-hw, 0.0, 0.0), (hw, 0.0, 0.0), (hw, OPEN_H, 0.0), (-hw, OPEN_H, 0.0), (0.0, 0.0, 1.0, 1.0))

    return [
        SubMesh("Frame", *merge(frame), M_FRAME),
        SubMesh("FrameInset", *merge(inset), M_INSET),
        SubMesh("Conduits", *merge(cond), M_COND),
        SubMesh("EmitterNodes", *merge(nodes), M_NODES),
        SubMesh("ThresholdChevrons", *merge(haz), M_HAZ),
        SubMesh("EmitterStrip", *merge(emit), M_EMIT),
        SubMesh("RFIDPanel", *merge(panel), M_PANEL),
        SubMesh("StatusLight", *merge(light), M_LIGHT),
        SubMesh("FieldPlane", *fp, M_FIELD),
    ]


if __name__ == "__main__":
    subs = build()
    allp = np.vstack([s.positions for s in subs])
    tris = sum(len(s.indices) for s in subs)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    export_glb(OUT, subs, root_name="RFIDForceFieldDoor")
    print("tris", tris)
    print("bbox min", allp.min(0).round(4), "max", allp.max(0).round(4))
    hw = OPEN_W * 0.5
    for sm in subs:
        if sm.name == "FieldPlane": continue
        P = sm.positions
        inside = (np.abs(P[:, 0]) < hw - 1e-4) & (P[:, 1] < OPEN_H - 1e-4)
        assert not inside.any(), f"{sm.name} intrudes into clear opening"
        assert np.abs(P[:, 2]).max() < 0.150, f"{sm.name} protrudes past wall face"
    print("frame depth", round(allp[:, 2].max() - allp[:, 2].min(), 4), "wall", WALL_T)
    for s in subs:
        print(s.name, len(s.indices))
