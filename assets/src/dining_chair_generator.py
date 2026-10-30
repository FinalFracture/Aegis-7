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

if __name__ == "__main__" and len(__import__("sys").argv) == 1:
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([iter1, iter2, iter3, iter4, iter5], 1):
        title, parts = fn()
        sc = finish(parts)
        b = sc.bounds; tris = sum(len(g.faces) for g in sc.geometry.values())
        sc.export(os.path.join(OUT, f"iter_0{i}.glb"))
        sheet(sc, os.path.join(OUT, f"iter_0{i}_sheet.png"))
        print(f"iter_0{i} {title}: tris={tris} W={b[1][0]-b[0][0]:.3f} H={b[1][1]-b[0][1]:.3f} D={b[1][2]-b[0][2]:.3f} minY={b[0][1]:.3f}")


# =====================================================================
# FINAL: Floor-Clamped Swivel (refined)  ->  python3 dining_chair_generator.py final
# =====================================================================
from trimesh.visual.material import PBRMaterial as _PBR

FMAT = {
 "alloy":   _PBR(name="BrushedAlloy", baseColorFactor=(0.78,0.79,0.81,1), metallicFactor=0.9, roughnessFactor=0.35),
 "gunmetal":_PBR(name="Gunmetal", baseColorFactor=(0.24,0.25,0.28,1), metallicFactor=0.85, roughnessFactor=0.45),
 "fabric":  _PBR(name="SeatFabric", baseColorFactor=(0.22,0.24,0.29,1), metallicFactor=0.0, roughnessFactor=0.85),
 "amber":   _PBR(name="LockAmber", baseColorFactor=(1.0,0.647,0.227,1), metallicFactor=0.0, roughnessFactor=0.4, emissiveFactor=(1.0,0.647,0.227)),
 "violet":  _PBR(name="AccentViolet", baseColorFactor=(0.72,0.35,1.0,1), metallicFactor=0.0, roughnessFactor=0.4, emissiveFactor=(0.72,0.35,1.0)),
}

def rrect(w, d, r, n=6):
    """Rounded-rect outline (XZ), CCW, n segs per corner."""
    pts = []
    for cx, cz, a0 in ((w/2-r, d/2-r, 0), (-w/2+r, d/2-r, 90), (-w/2+r, -d/2+r, 180), (w/2-r, -d/2+r, 270)):
        for k in range(n+1):
            a = np.radians(a0 + 90*k/n); pts.append((cx + r*np.cos(a), cz + r*np.sin(a)))
    return np.array(pts)

def circle(r, n=24):
    a = np.linspace(0, 2*np.pi, n, endpoint=False); return np.c_[r*np.cos(a), r*np.sin(a)]

def loft(outline, rings):
    """outline (N,2) in XZ; rings list of (y, sx, sz). Closed mesh with capped ends + cyl UVs."""
    N = len(outline); V = []; UV = []
    per = np.r_[0, np.cumsum(np.linalg.norm(np.diff(np.vstack([outline, outline[:1]]), axis=0), axis=1))]
    u = per[:-1] / per[-1]
    for y, sx, sz in rings:
        V += [(p[0]*sx, y, p[1]*sz) for p in outline]; UV += [(uu, y) for uu in u]
    F = []
    for i in range(len(rings)-1):
        for j in range(N):
            a, b = i*N+j, i*N+(j+1) % N; c, d = a+N, b+N
            F += [(a, c, b), (b, c, d)]
    for ring, flip in ((0, True), (len(rings)-1, False)):
        ci = len(V); y = rings[ring][0]; V.append((0, y, 0)); UV.append((0.5, y))
        for j in range(N):
            a, b = ring*N+j, ring*N+(j+1) % N
            F.append((ci, b, a) if flip else (ci, a, b))
    m = trimesh.Trimesh(np.array(V, float), np.array(F), process=False)
    if m.volume < 0: m.invert()
    m.metadata["uv"] = np.array(UV, float)
    return m

def torus_ring(R, r, nu=32, nv=8):
    V, UV, F = [], [], []
    for i in range(nu):
        a = 2*np.pi*i/nu
        for j in range(nv):
            b = 2*np.pi*j/nv
            V.append(((R + r*np.cos(b))*np.cos(a), r*np.sin(b), (R + r*np.cos(b))*np.sin(a))); UV.append((i/nu, j/nv))
    for i in range(nu):
        for j in range(nv):
            a, b = i*nv+j, i*nv+(j+1) % nv; c, d = ((i+1) % nu)*nv+j, ((i+1) % nu)*nv+(j+1) % nv
            F += [(a, b, c), (b, d, c)]
    m = trimesh.Trimesh(np.array(V), np.array(F), process=False)
    if m.volume < 0: m.invert()
    m.metadata["uv"] = np.array(UV); return m

def xf(m, R=None, t=(0, 0, 0)):
    uv = m.metadata.get("uv")
    if R is not None: m.apply_transform(R)
    m.apply_translation(t); m.metadata["uv"] = uv; return m

def merge(ms):
    uv = np.vstack([m.metadata["uv"] for m in ms]); out = trimesh.util.concatenate(ms)
    out.metadata["uv"] = uv; return out

def shade_split(m, angle=30):
    """Split vertices by crease angle -> per-corner smooth/hard normals. Returns verts, normals, uvs, faces."""
    F = m.faces; fn = m.face_normals; uv0 = m.metadata["uv"]
    cos_t = np.cos(np.radians(angle))
    V, N, UV, NF = [], [], [], np.zeros_like(F)
    v2f = [[] for _ in range(len(m.vertices))]
    for fi, f in enumerate(F):
        for v in f: v2f[v].append(fi)
    area = m.area_faces; key = {}
    for fi, f in enumerate(F):
        for k, v in enumerate(f):
            grp = tuple(sorted(g for g in v2f[v] if fn[g] @ fn[fi] >= cos_t))
            kk = (v, grp)
            if kk not in key:
                n = (fn[list(grp)] * area[list(grp), None]).sum(0); n /= np.linalg.norm(n) + 1e-12
                key[kk] = len(V); V.append(m.vertices[v]); N.append(n); UV.append(uv0[v])
            NF[fi, k] = key[kk]
    return np.array(V), np.array(N), np.array(UV), NF

def swivel_final():
    P = {}
    # FloorPlate: octagonal chamfered slab with beveled top edge
    oct8 = rrect(0.34, 0.34, 0.045, n=1)
    P["FloorPlate"] = ("gunmetal", loft(oct8, [(0, 1, 1), (0.016, 1, 1), (0.026, 0.93, 0.93)]))
    P["LockLight"] = ("amber", loft(rrect(0.06, 0.012, 0.005, 2), [(0.0255, 1, 1), (0.031, 1, 1), (0.033, .85, .6)]))
    xf(P["LockLight"][1], t=(0, 0, 0.13))
    # Column: lathe with flared foot and top collar
    c = circle(1, 20)
    P["Column"] = ("alloy", loft(c, [(0.026, .075, .075), (0.034, .075, .075), (0.06, .05, .05),
                                     (0.35, .046, .046), (0.371, .055, .055)]))
    P["SwivelHub"] = ("gunmetal", loft(c, [(0.37, .085, .085), (0.378, .095, .095), (0.394, .095, .095), (0.401, .088, .088)]))
    # FootRing: torus + 4 spokes from column surface to ring
    parts = [xf(torus_ring(0.17, 0.011, 24, 6), t=(0, 0.2, 0))]
    for a in (45, 135, 225, 315):
        sp = loft(circle(1, 6), [(0.044, .008, .008), (0.165, .008, .008)])
        xf(sp, trimesh.transformations.rotation_matrix(np.radians(-90), [0, 0, 1]), (0, 0, 0))   # along +X
        xf(sp, trimesh.transformations.rotation_matrix(np.radians(a), [0, 1, 0]), (0, 0.2, 0))
        parts.append(sp)
    P["FootRing"] = ("alloy", merge(parts))
    # Seat pan + padded cushion
    rr = rrect(0.45, 0.43, 0.06, 3)
    P["Seat_Pan"] = ("alloy", loft(rr, [(0.401, .95, .95), (0.41, 1, 1), (0.431, 1, 1)]))
    P["Seat_Cushion"] = ("fabric", loft(rrect(0.44, 0.42, 0.07, 3),
        [(0.431, .985, .985), (0.446, 1, 1), (0.462, .99, .99), (0.472, .95, .95), (0.477, .87, .87), (0.479, .76, .76)]))
    # Back spine with L bracket under the seat pan
    spine = loft(rrect(0.06, 0.03, 0.01, 2), [(0.386, 1, 1), (0.80, 1, 1), (0.81, .8, .8)]); xf(spine, t=(0, 0, -0.245))
    brk = loft(rrect(0.07, 0.02, 0.006, 2), [(-0.05, 1, 1), (0.06, 1, 1)])   # along Y, rotate to run along Z
    xf(brk, trimesh.transformations.rotation_matrix(np.radians(90), [1, 0, 0]), (0, 0.3905, -0.205))
    gus = loft(rrect(0.012, 0.06, 0.004, 1), [(0.38, 1, 1), (0.44, .3, .3)]); xf(gus, t=(0, 0, -0.23))
    P["BackSpine"] = ("alloy", merge([spine, brk, gus]))
    # Back panel (tilted 8 deg), padded fabric face over alloy shell kept as single chamfered panel
    tilt = trimesh.transformations.rotation_matrix(np.radians(90 - 8), [1, 0, 0])
    bp = loft(rrect(0.42, 0.22, 0.05, 3), [(-0.018, .95, .9), (-0.012, 1, 1), (0.012, 1, 1), (0.018, .95, .9)])
    xf(bp, tilt, (0, 0.73, -0.212)); P["Back_Panel"] = ("fabric", bp)
    ins = loft(rrect(0.28, 0.012, 0.005, 2), [(0.017, 1, 1), (0.0215, 1, 1)])
    xf(ins, tilt, (0, 0.73, -0.212)); xf(ins, t=(0, 0.045*np.cos(np.radians(8)), 0.045*np.sin(np.radians(8))))
    P["AccentInset"] = ("violet", ins)
    return P

def _col(c):
    c = np.asarray(c, float)
    return [round(float(x), 4) for x in (c/255 if c.max() > 1.0001 or np.asarray(c).dtype == np.uint8 else c)]

def export_final(P, paths):
    import pygltflib
    from pygltflib import GLTF2, Scene, Node, Mesh, Primitive, Attributes, Buffer, BufferView, Accessor, Material, PbrMetallicRoughness
    g = GLTF2(); blob = bytearray(); mats = {}
    def add(arr, target, ctype, typ):
        arr = np.ascontiguousarray(arr); off = len(blob); blob.extend(arr.tobytes())
        while len(blob) % 4: blob.append(0)
        g.bufferViews.append(BufferView(buffer=0, byteOffset=off, byteLength=arr.nbytes, target=target))
        acc = Accessor(bufferView=len(g.bufferViews)-1, componentType=ctype, count=len(arr), type=typ)
        if typ == "VEC3" and target == 34962 and ctype == 5126: acc.min = arr.min(0).tolist(); acc.max = arr.max(0).tolist()
        g.accessors.append(acc); return len(g.accessors)-1
    tot = 0; nodes = []; geo = {}
    for name, (mk, m) in P.items():
        V, N, UV, F = shade_split(m); geo[name] = (mk, V, N, F); tot += len(F)
        if mk not in mats:
            pm = FMAT[mk]; mats[mk] = len(g.materials)
            bc, emf = _col(pm.baseColorFactor), _col(pm.emissiveFactor if pm.emissiveFactor is not None else [0, 0, 0])
            g.materials.append(Material(name=pm.name, emissiveFactor=emf,
                pbrMetallicRoughness=PbrMetallicRoughness(baseColorFactor=bc, metallicFactor=float(pm.metallicFactor), roughnessFactor=float(pm.roughnessFactor))))
        a = Attributes(POSITION=add(V.astype(np.float32), 34962, 5126, "VEC3"), NORMAL=add(N.astype(np.float32), 34962, 5126, "VEC3"),
                       TEXCOORD_0=add(UV.astype(np.float32), 34962, 5126, "VEC2"))
        idx = add(F.astype(np.uint32).ravel(), 34963, 5125, "SCALAR")
        g.meshes.append(Mesh(name=name, primitives=[Primitive(attributes=a, indices=idx, material=mats[mk])]))
        g.nodes.append(Node(name=name, mesh=len(g.meshes)-1)); nodes.append(len(g.nodes)-1)
    g.scenes = [Scene(nodes=nodes)]; g.scene = 0
    g.buffers = [Buffer(byteLength=len(blob))]; g.set_binary_blob(bytes(blob))
    for p in paths: os.makedirs(os.path.dirname(p), exist_ok=True); g.save_binary(p)
    return tot, geo

# ---------- soft-shaded numpy rasterizer ----------
def render_view(geo, R, size=520, ss=2, shadow=True, glass_alpha=None):
    """glass_alpha (e.g. 0.35): draw materials with baseColor alpha < 1 in a second, depth-tested but blended pass (translucent BLEND glass)."""
    from scipy.ndimage import gaussian_filter
    S = size*ss; bg = np.array([0.955, 0.948, 0.925])
    allV = np.vstack([v for _, v, _, _ in geo.values()]) @ R.T
    lo, hi = allV[:, :2].min(0), allV[:, :2].max(0); span = (hi-lo).max()*1.25; ctr = (lo+hi)/2
    def to_px(P): return np.c_[(P[:, 0]-ctr[0])/span*S + S/2, S/2 - (P[:, 1]-ctr[1])/span*S]
    img = np.tile(bg, (S, S, 1)); zb = np.full((S, S), -1e9)
    if shadow:   # soft contact shadow: footprint flattened onto y=0
        mask = np.zeros((S, S))
        for _, V, _, F in geo.values():
            Vf = V.copy(); Vf[:, 1] = 0; p = to_px(Vf @ R.T)
            for t in F:
                a, b, c = p[t]; x0, y0 = np.floor(np.minimum(np.minimum(a, b), c)).astype(int); x1, y1 = np.ceil(np.maximum(np.maximum(a, b), c)).astype(int)
                x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, S-1), min(y1, S-1)
                if x1 < x0 or y1 < y0: continue
                X, Y = np.meshgrid(np.arange(x0, x1+1)+.5, np.arange(y0, y1+1)+.5)
                d = (b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
                if abs(d) < 1e-9: continue
                w0 = ((b[1]-c[1])*(X-c[0])+(c[0]-b[0])*(Y-c[1]))/d; w1 = ((c[1]-a[1])*(X-c[0])+(a[0]-c[0])*(Y-c[1]))/d
                ins = (w0 >= 0) & (w1 >= 0) & (w0+w1 <= 1); mask[y0:y1+1, x0:x1+1][ins] = 1
        sh = gaussian_filter(mask, S*0.012) * 0.28 + gaussian_filter(mask, S*0.04) * 0.15
        img *= (1 - sh)[..., None]
    key = np.array([-0.45, 0.75, 0.55]); key /= np.linalg.norm(key)
    fill = np.array([0.6, 0.25, 0.5]); fill /= np.linalg.norm(fill)
    rim = np.array([0.1, 0.4, -0.9]); rim /= np.linalg.norm(rim)
    view = R.T @ np.array([0, 0, 1.0])   # direction to camera in world
    occ = np.zeros((S, S))
    _items = list(geo.items())
    if glass_alpha is not None:
        _items = [it for it in _items if _col(FMAT[it[1][0]].baseColorFactor)[3] >= 1] + [it for it in _items if _col(FMAT[it[1][0]].baseColorFactor)[3] < 1]
    for name, (mk, V, N, F) in _items:
        _blend = glass_alpha is not None and _col(FMAT[mk].baseColorFactor)[3] < 1
        pm = FMAT[mk]; base = np.array(_col(pm.baseColorFactor)[:3]); met = pm.metallicFactor; rough = pm.roughnessFactor
        em = np.array(_col(pm.emissiveFactor if pm.emissiveFactor is not None else [0, 0, 0]))
        Pv = V @ R.T; p = to_px(Pv); z = Pv[:, 2]
        for t in F:
            a, b, c = p[t]
            x0, y0 = np.floor(np.minimum(np.minimum(a, b), c)).astype(int); x1, y1 = np.ceil(np.maximum(np.maximum(a, b), c)).astype(int)
            x0, y0 = max(x0, 0), max(y0, 0); x1, y1 = min(x1, S-1), min(y1, S-1)
            if x1 < x0 or y1 < y0: continue
            d = (b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
            if abs(d) < 1e-12: continue
            X, Y = np.meshgrid(np.arange(x0, x1+1)+.5, np.arange(y0, y1+1)+.5)
            w0 = ((b[1]-c[1])*(X-c[0])+(c[0]-b[0])*(Y-c[1]))/d; w1 = ((c[1]-a[1])*(X-c[0])+(a[0]-c[0])*(Y-c[1]))/d; w2 = 1-w0-w1
            ins = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
            if not ins.any(): continue
            zz = w0*z[t[0]]+w1*z[t[1]]+w2*z[t[2]]
            sub = zb[y0:y1+1, x0:x1+1]; upd = ins & (zz > sub)
            if not upd.any(): continue
            n = w0[upd, None]*N[t[0]]+w1[upd, None]*N[t[1]]+w2[upd, None]*N[t[2]]
            n /= np.linalg.norm(n, axis=1, keepdims=True)+1e-9
            if n @ view is not None:
                flip = (n @ view) < 0; n[flip] *= -1
            dk, df = np.clip(n@key, 0, 1), np.clip(n@fill, 0, 1)
            nv = np.clip(n@view, 0, 1); rimt = (1-nv)**2.5 * np.clip(n@rim*0.5+0.6, 0, 1)
            hemi = 0.5 + 0.5*n[:, 1]
            sp_pow = 2/(rough**4+1e-3) ; sp_pow = min(sp_pow, 400)
            h = key+view; h /= np.linalg.norm(h); spec = np.clip(n@h, 0, 1)**sp_pow * (1.4 if met > .5 else 0.25) * (1-rough*0.6)
            fres = 0.04 + 0.96*(1-nv)**5
            dif_col = base*(1-met)
            spec_col = base*met + 0.04*(1-met)
            env = (0.35 + 0.45*hemi)[:, None]*(spec_col if met > .5 else 0)  # cheap env for metal
            col = dif_col*(0.25*hemi[:, None] + 0.8*dk[:, None] + 0.3*df[:, None]) \
                + env + spec[:, None]*np.maximum(spec_col, 0.25) + 0.25*rimt[:, None] + fres[:, None]*0.08 + em*0.9
            subi = img[y0:y1+1, x0:x1+1]
            if _blend: subi[upd] = subi[upd]*(1-glass_alpha) + col*glass_alpha; continue
            subi[upd] = col; sub[upd] = zz[upd]
    # screen-space AO from depth
    fg = zb > -1e8
    zf = np.where(fg, zb, np.nan); zfill = np.where(fg, zb, zb[fg].min() if fg.any() else 0)
    blur = gaussian_filter(zfill, S*0.01)
    ao = np.clip((blur - zfill) / (span*0.02), 0, 1)*0.35
    img[fg] *= (1-ao[fg])[:, None]
    img = np.clip(img, 0, 1) ** (1/1.1)
    img = img.reshape(size, ss, size, ss, 3).mean((1, 3))
    return img

def final_sheet(geo, path):
    top = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]]); front = np.eye(3); side = np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]])
    a, b = np.radians(35), np.radians(25)
    Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
    Rx = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]])
    fig, axs = plt.subplots(2, 2, figsize=(10, 10.4), facecolor="#F4F2EC")
    for ax, R, t, shd in zip(axs.flat, [top, front, side, Rx @ Ry], ["Top", "Front", "Side", "Iso"], [False, True, True, True]):
        ax.imshow(render_view(geo, R, shadow=shd)); ax.axis("off"); ax.set_title(t, y=-0.06, fontsize=11, color="#555")
    plt.tight_layout(); fig.savefig(path, dpi=110, facecolor="#F4F2EC"); plt.close(fig)

if __name__ == "__main__" and len(__import__("sys").argv) > 1 and __import__("sys").argv[1] == "final":
    P = swivel_final()
    for n, (_, m) in P.items():
        assert m.is_watertight, n
    tot, geo = export_final(P, [os.path.join(ROOT, "godot/assets/models/dining_chair_swivel.glb"), os.path.join(OUT, "final_swivel.glb")])
    allv = np.vstack([g[1] for g in geo.values()]); print("tris", tot, "bounds", allv.min(0).round(3), allv.max(0).round(3))
    final_sheet(geo, os.path.join(OUT, "final_swivel_sheet.png"))
