#!/usr/bin/env python3
"""Dining chair/stool (#13) - 5 iterations. Owner: Rook.
Pivot bottom-center (0,0,0), front +Z, Y up. Exports design/assets/dining_chair/iter_0N.glb
and iter_0N_sheet.png (Top/Front/Side/Iso, no annotations)."""
import os, numpy as np, trimesh
from trimesh.creation import box, cylinder, annulus
from trimesh.visual.material import PBRMaterial
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "design/assets/dining_chair")
MAT = {
 "alloy": ((0.62,0.64,0.68,1),0.8,0.45,(0,0,0)),
 "dark": ((0.18,0.19,0.22,1),0.7,0.5,(0,0,0)),
 "pad":  ((0.32,0.30,0.36,1),0.0,0.85,(0,0,0)),
 "ceramic": ((0.82,0.80,0.74,1),0.0,0.6,(0,0,0)),
 "violet": ((0.72,0.35,1.0,1),0.0,0.4,(0.72,0.35,1.0)),
 "amber": ((1.0,0.65,0.2,1),0.0,0.4,(1.0,0.6,0.15)),
}

def rot(m, axis, deg):
    m.apply_transform(trimesh.transformations.rotation_matrix(np.radians(deg), axis)); return m
def at(m, x, y, z): m.apply_translation((x, y, z)); return m
def B(sx, sy, sz, x, y, z, ch=True):
    """Box; chamfered (octagon-prism) look via 8-sided extrusion when ch."""
    if not ch: return at(box((sx, sy, sz)), x, y, z)
    c = min(sx, sz) * 0.15
    hx, hz = sx/2, sz/2
    poly = [(-hx+c,-hz),(hx-c,-hz),(hx,-hz+c),(hx,hz-c),(hx-c,hz),(-hx+c,hz),(-hx,hz-c),(-hx,-hz+c)]
    pts = [(px, py, pz) for (px, pz) in poly for py in (-sy/2, sy/2)]
    m = trimesh.convex.convex_hull(np.array(pts))                 # chamfered prism, height Y
    return at(m, x, y, z)
def C(r, h, x, y, z, s=12): return at(cylinder(r, h, sections=s), x, y, z)  # along Z
def CY(r, h, x, y, z, s=12): return at(rot(cylinder(r, h, sections=s), [1,0,0], 90), x, y, z)
def TUBE(p0, p1, r=0.012, s=8):
    return trimesh.creation.cylinder(r, segment=[p0, p1], sections=s)

def finish(parts):
    sc = trimesh.Scene()
    for i, (name, mat, m) in enumerate(parts):
        v = m.vertices; n = m.face_normals
        # box-projected UVs (per-vertex, dominant axis of vertex normal)
        vn = np.abs(m.vertex_normals); ax = vn.argmax(1)
        uv = np.where(ax[:,None]==0, v[:,[2,1]], np.where(ax[:,None]==1, v[:,[0,2]], v[:,[0,1]]))
        c, me, ro, em = MAT[mat]
        pm = PBRMaterial(name=mat, baseColorFactor=c, metallicFactor=me, roughnessFactor=ro, emissiveFactor=em)
        m.visual = trimesh.visual.TextureVisuals(uv=uv, material=pm)
        sc.add_geometry(m, node_name=name, geom_name=name)
    return sc

# ---------------- iterations ----------------
def iter1():  # Folded sheet-alloy stacking chair
    P = []; t = 0.006
    P.append(("Seat", "alloy", B(0.42, 0.02, 0.42, 0, 0.45, 0.01)))
    P.append(("SeatPad", "pad", B(0.38, 0.02, 0.36, 0, 0.47, 0.02)))
    for sx in (-1, 1):  # folded side "C" legs (front & rear legs as one panel)
        P.append((f"Side_{sx}", "alloy", B(0.02, 0.44, 0.40, sx*0.205, 0.22, 0.0)))
        P.append((f"SideCut_{sx}", "dark", B(0.024, 0.26, 0.24, sx*0.205, 0.22, 0.0)))
    P.append(("BackLeg_L", "alloy", B(0.03, 0.44, 0.02, -0.19, 0.68, -0.19)))
    P.append(("BackLeg_R", "alloy", B(0.03, 0.44, 0.02, 0.19, 0.68, -0.19)))
    back = rot(B(0.40, 0.20, 0.02, 0, 0, 0), [1,0,0], -6); at(back, 0, 0.78, -0.205)
    P.append(("Backrest", "alloy", back))
    P.append(("BackBand", "violet", at(rot(B(0.30, 0.012, 0.024, 0, 0, 0, ch=False), [1,0,0], -6), 0, 0.82, -0.21)))
    P.append(("StackLug", "dark", B(0.36, 0.02, 0.03, 0, 0.88, -0.2)))
    return "Folded Sheet-Alloy Stacker", P

def iter2():  # Drum stool w/ mag-anchor foot ring
    P = []
    P.append(("Base", "dark", C(0.20, 0.03, 0, 0, 0, 16)))
    P[-1][2].apply_transform(trimesh.transformations.rotation_matrix(np.radians(-90),[1,0,0])); at(P[-1][2],0,0.015,0)
    P.append(("MagRing", "amber", at(rot(annulus(0.18, 0.20, 0.01, sections=24), [1,0,0], -90), 0, 0.031, 0)))
    P.append(("Drum", "alloy", CY(0.16, 0.40, 0, 0.23, 0, 16)))
    for k, y in enumerate((0.12, 0.34)):
        P.append((f"Band_{k}", "dark", CY(0.165, 0.025, 0, y, 0, 16)))
    P.append(("FootRing", "alloy", at(rot(trimesh.creation.torus(0.21, 0.012, 24, 6), [1,0,0], -90), 0, 0.24, 0)))
    P.append(("Seat", "pad", CY(0.21, 0.06, 0, 0.46, 0, 20)))
    P.append(("Backrest", "alloy", at(rot(B(0.36, 0.30, 0.03, 0, 0, 0), [1,0,0], -8), 0, 0.73, -0.19)))
    P.append(("BackPost", "dark", B(0.06, 0.40, 0.03, 0, 0.58, -0.17)))
    P.append(("BackPad", "pad", at(rot(B(0.30, 0.16, 0.02, 0, 0, 0), [1,0,0], -8), 0, 0.76, -0.17)))
    return "Mag-Anchor Drum Stool", P

def iter3():  # Cantilever tube frame
    P = []; r = 0.013
    pts = lambda sx: [(sx*0.2,0.01,0.18),(sx*0.2,0.01,-0.2),(sx*0.2,0.44,-0.2),(sx*0.2,0.44,0.21)]
    for sx in (-1, 1):
        p = pts(sx)
        P.append((f"RunnerFwd_{sx}", "alloy", TUBE((sx*0.2,0.01,0.2),p[1],r)))
        P.append((f"Upright_{sx}", "alloy", TUBE(p[1],(sx*0.2,0.44,-0.17),r)))
        P.append((f"SeatRail_{sx}", "alloy", TUBE((sx*0.2,0.44,-0.2),p[3],r)))
        P.append((f"BackPost_{sx}", "alloy", TUBE((sx*0.2,0.44,-0.2),(sx*0.2,0.89,-0.25),r)))
        P.append((f"Foot_{sx}", "dark", B(0.04,0.012,0.06,sx*0.2,0.006,0.17,ch=False)))
    P.append(("Crossbar", "alloy", TUBE((-0.2,0.01,-0.2),(0.2,0.01,-0.2),r)))
    P.append(("Seat", "pad", B(0.42, 0.04, 0.42, 0, 0.47, 0.0)))
    P.append(("SeatBand", "dark", B(0.43, 0.012, 0.43, 0, 0.452, 0.0)))
    back = at(rot(B(0.40, 0.24, 0.025, 0, 0, 0), [1,0,0], -6), 0, 0.75, -0.235)
    P.append(("Backrest", "pad", back))
    P.append(("GripSlot", "green" if False else "dark", B(0.12, 0.025, 0.03, 0, 0.85, -0.245, ch=False)))
    return "Cantilever Tube Chair", P

def iter4():  # Printed lattice chair
    P = []
    P.append(("Seat", "ceramic", B(0.44, 0.04, 0.42, 0, 0.43, 0.0)))
    for sx in (-1, 1):
        for sz in (-1, 1):
            P.append((f"Leg_{sx}_{sz}", "ceramic", TUBE((sx*0.19,0,sz*0.18),(sx*0.16,0.41,sz*0.15),0.02,6)))
        # X-lattice side bracing
        P.append((f"LatA_{sx}", "ceramic", TUBE((sx*0.185,0.03,-0.17),(sx*0.165,0.38,0.15),0.009,6)))
        P.append((f"LatB_{sx}", "ceramic", TUBE((sx*0.185,0.03,0.17),(sx*0.165,0.38,-0.15),0.009,6)))
    P.append(("LatBack", "ceramic", TUBE((-0.18,0.05,-0.17),(0.18,0.36,-0.16),0.009,6)))
    # lattice backrest: verticals + diagonals
    for i, x in enumerate(np.linspace(-0.18, 0.18, 5)):
        P.append((f"BackRib_{i}", "ceramic", TUBE((x,0.45,-0.19),(x*1.05,0.9,-0.23),0.011,6)))
    P.append(("BackTop", "ceramic", TUBE((-0.2,0.89,-0.23),(0.2,0.89,-0.23),0.016,6)))
    P.append(("BackMid", "ceramic", TUBE((-0.19,0.67,-0.21),(0.19,0.67,-0.21),0.01,6)))
    P.append(("SeatPad", "pad", B(0.38, 0.015, 0.34, 0, 0.457, 0.02)))
    P.append(("PrintTag", "violet", B(0.06, 0.012, 0.006, 0, 0.42, 0.212, ch=False)))
    return "Printed Lattice Chair", P

def iter5():  # Floor-clamped swivel
    P = []
    P.append(("ClampPlate", "dark", B(0.30, 0.02, 0.30, 0, 0.01, 0)))
    for i, (x, z) in enumerate([(-.12,-.12),(.12,-.12),(-.12,.12),(.12,.12)]):
        P.append((f"Bolt_{i}", "alloy", CY(0.012, 0.01, x, 0.025, z, 6)))
    P.append(("LockLight", "green_dummy" if False else "amber", B(0.05, 0.006, 0.01, 0, 0.022, 0.15, ch=False)))
    P.append(("Column", "alloy", CY(0.04, 0.36, 0, 0.20, 0, 12)))
    P.append(("Collar", "dark", CY(0.06, 0.05, 0, 0.06, 0, 12)))
    P.append(("SwivelHub", "dark", CY(0.09, 0.03, 0, 0.395, 0, 14)))
    P.append(("Seat", "pad", B(0.44, 0.05, 0.42, 0, 0.435, 0.0)))
    P.append(("SeatShell", "alloy", B(0.45, 0.02, 0.43, 0, 0.405, 0.0)))
    P.append(("BackArm", "alloy", B(0.06, 0.30, 0.03, 0, 0.58, -0.2)))
    back = at(rot(B(0.42, 0.20, 0.035, 0, 0, 0), [1,0,0], -8), 0, 0.79, -0.215)
    P.append(("Backrest", "pad", back))
    P.append(("BackInset", "violet", at(rot(B(0.30, 0.01, 0.01, 0, 0, 0, ch=False), [1,0,0], -8), 0, 0.84, -0.195)))
    P.append(("Footrest", "alloy", at(rot(trimesh.creation.torus(0.17, 0.01, 20, 6), [1,0,0], -90), 0, 0.2, 0)))
    for i, a in enumerate((0, 90, 180, 270)):
        a = np.radians(a)
        P.append((f"Spoke_{i}", "alloy", TUBE((0.04*np.sin(a),0.2,0.04*np.cos(a)),(0.17*np.sin(a),0.2,0.17*np.cos(a)),0.008,6)))
    return "Floor-Clamped Swivel", P

# ---------------- sheet ----------------
def draw(ax, mesh, R, colors, title):
    v = mesh.vertices @ R.T
    f = mesh.faces
    depth = v[f][:, :, 2].mean(1); order = np.argsort(depth)
    nrm = mesh.face_normals @ R.T
    shade = 0.55 + 0.45 * np.clip(np.abs(nrm @ np.array([0.3, 0.5, 0.8])/np.linalg.norm([0.3,.5,.8])), 0, 1)
    fc = colors * shade[:, None]
    ax.add_collection(PolyCollection(v[f][order][:, :, :2], facecolors=np.clip(fc[order],0,1),
                                     edgecolors=(0.15,0.15,0.18,0.5), linewidths=0.25))
    ax.set_aspect("equal"); ax.autoscale(); ax.margins(0.08); ax.axis("off")
    ax.set_title(title, y=-0.08, fontsize=10, color="#444")

def sheet(scene, path):
    meshes, cols = [], []
    for name, g in scene.geometry.items():
        m = scene.dump(concatenate=False)
    for m in scene.dump(concatenate=False):
        c = np.array(m.visual.material.baseColorFactor[:3], float)
        c = c/255 if c.max() > 1 else c
        meshes.append(m); cols.append(np.tile(c, (len(m.faces), 1)))
    M = trimesh.util.concatenate(meshes); Cc = np.vstack(cols)
    I = np.eye(3)
    top = np.array([[1,0,0],[0,0,-1],[0,1,0]])     # look down -Y, front (+Z) at bottom
    front = I                                       # look from +Z
    side = np.array([[0,0,-1],[0,1,0],[1,0,0]])     # from +X... front to the left
    def iso():
        a, b = np.radians(35), np.radians(30)
        Ry = np.array([[np.cos(a),0,np.sin(a)],[0,1,0],[-np.sin(a),0,np.cos(a)]])
        Rx = np.array([[1,0,0],[0,np.cos(b),-np.sin(b)],[0,np.sin(b),np.cos(b)]])
        return Rx @ Ry
    fig, axs = plt.subplots(2, 2, figsize=(10, 10), facecolor="#F4F2EC")
    for ax, R, t in zip(axs.flat, [top, front, side, iso()], ["Top", "Front", "Side", "Iso"]):
        ax.set_facecolor("#F4F2EC"); draw(ax, M, R, Cc, t)
    plt.tight_layout(); fig.savefig(path, dpi=110, facecolor="#F4F2EC"); plt.close(fig)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        title, parts = fn()
        sc = finish(parts)
        b = sc.bounds; tris = sum(len(g.faces) for g in sc.geometry.values())
        sc.export(os.path.join(OUT, f"iter_0{i}.glb"))
        sheet(sc, os.path.join(OUT, f"iter_0{i}_sheet.png"))
        print(f"iter_0{i} {title}: tris={tris} W={b[1][0]-b[0][0]:.3f} H={b[1][1]-b[0][1]:.3f} D={b[1][2]-b[0][2]:.3f} minY={b[0][1]:.3f}")
