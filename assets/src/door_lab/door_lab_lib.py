"""Rook door_lab (2026-11-20): shared rig/export/QA library for the door-lab GLBs (Gage sprint, scenes/test/door_lab.tscn).
Builds a node TREE (unlike modlib's flat Part): empty group nodes (leaf_L, leaf, ...) whose origin is the real pivot,
mesh children per part, *-colonly / *-convcolonly colliders parented under the moving node they belong to.
Conventions (handoff v6 section 2): metres, Y-up, +Z out, bottom-centre pivot, < 6k tris, UVs + normals, glass only BLEND.
Pose evaluation (pose deltas per node, in node-local space) drives the clip check, the motion sweep and the preview renders."""
import os, sys, io, json, numpy as np, trimesh
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.dirname(HERE)
sys.path.insert(0, SRC); sys.path.insert(0, os.path.join(SRC, "tennis_tower"))
from modlib import (FMAT, _m, box, tube, cap, loft, rrect, circle, xf, merge, finish_glb, G, ST, SL, CY, AM, ALY, SGM, SSL, E)
import dining_chair_generator as dc
import ext_clip_check as cc
import validate_models as vm
from bath_pod_generator import views
from kitchen_counter_generator import crop
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
ROOT = dc.ROOT
OUT_GLB = os.path.join(ROOT, "godot/assets/models/door_lab"); OUT_RENDER = "/workspace/renders/door_lab"
TF = trimesh.transformations
# door_lab-only material: the status light gets its own emissive material so Gage can recolour it without touching other cyan
# Sloane AESTHETIC_SPEC 2026-11-20: status lamp default amber #FF9500 (closed idle), pearl leaf faces #D8DEE6 (0.847/0.871/0.902),
# rubber seals 0.06-0.09 / rough 0.85, cyan reveal = TT_CyanLED #00E5FF.
_m("dl_status", "DL_StatusLamp", (1.0, .584, 0.0), 0, .3, em=(1.0, .584, 0.0))
_m("dl_seal", "DL_SealRubber", (.07, .075, .08), 0, .85)
_m("dl_pearl", "DL_PearlComposite", (.847, .871, .900), .1, .48)   # #D8DEE6, blue capped at the 0.90 albedo limit
_m("dl_reveal", "TT_CyanLED", (0.0, .898, 1.0), 0, .3, em=(0.0, .898, 1.0))
_m("dl_glow", "DL_GaugeFace", (.08, .09, .10), 0, .3, em=(0.0, .45, .5))
STAT, SEAL, PEARL, REV, GLOW = "dl_status", "dl_seal", "dl_pearl", "dl_reveal", "dl_glow"

def uvp(m):  # planar uv fallback (x+z, y)
    v = m.vertices; m.metadata["uv"] = np.c_[v[:, 0] + .5*v[:, 2], v[:, 1] + .5*v[:, 2]]; return m

def mk(V, F):
    m = trimesh.Trimesh(np.asarray(V, float), np.asarray(F, int), process=False); m.fix_normals(); return uvp(m)

def rr_xy(w, h, r, n=4, c=(0, 0)):
    p = rrect(w, h, max(r, 1e-4), n); return p + np.asarray(c, float)

def sweep_rr(w, h, r, prof, n=4, c=(0, 0), axis_z=True):
    """closed profile [(off, z), ...] swept around a rounded rect (w x h, corner r, centre c) in XY; off>0 grows outward."""
    rings = [rr_xy(w + 2*o, h + 2*o, r + o, n, c) for o, _ in prof]; N = len(rings[0]); K = len(prof)
    V = [(x, y, z) for (o, z), ring in zip(prof, rings) for x, y in ring]; F = []
    for k in range(K):
        for j in range(N):
            a, b = k*N + j, k*N + (j + 1) % N; c2, d = ((k + 1) % K)*N + j, ((k + 1) % K)*N + (j + 1) % N
            F += [(a, b, d), (a, d, c2)]
    return mk(V, F)

def solid_rr(w, h, r, prof, n=4, c=(0, 0)):
    """open profile [(off, z)] from back to front; ends capped with fans (outline is convex)."""
    rings = [rr_xy(w + 2*o, h + 2*o, r + o, n, c) for o, _ in prof]; N = len(rings[0]); K = len(prof)
    V = [(x, y, z) for (o, z), ring in zip(prof, rings) for x, y in ring]; F = []
    for k in range(K - 1):
        for j in range(N):
            a, b = k*N + j, k*N + (j + 1) % N; F += [(a, b, b + N), (a, b + N, a + N)]
    for k in (0, K - 1):
        ci = len(V); V.append((c[0], c[1], prof[k][1]))
        F += [(ci, k*N + (j + 1) % N, k*N + j) for j in range(N)]
    return mk(V, F)

def ring_between(inner, outer, z0, z1):
    """annulus between two closed XY outlines with equal point counts (CCW), extruded z0..z1."""
    N = len(inner); L = [inner, outer]; V = []
    for zz in (z0, z1):
        for ring in L: V += [(x, y, zz) for x, y in ring]
    # rings: 0 inner z0, 1 outer z0, 2 inner z1, 3 outer z1
    F = []
    def quad(r0, r1):
        for j in range(N):
            a, b = r0*N + j, r0*N + (j + 1) % N; c2, d = r1*N + j, r1*N + (j + 1) % N; F.extend([(a, b, d), (a, d, c2)])
    quad(0, 1); quad(1, 3); quad(3, 2); quad(2, 0)
    return mk(V, F)

def bplate(x0, x1, y0, y1, z0, z1, bev=.01, front=True, n=1):
    """chunky beveled plate (rounded-rect outline in XY), bevel on the +Z face (front=True) or -Z face."""
    w, h = x1 - x0, y1 - y0; c = ((x0 + x1)/2, (y0 + y1)/2); r = min(bev*1.5, w/2 - 1e-3, h/2 - 1e-3)
    prof = [(0, z0), (0, z1 - bev), (-bev, z1)] if front else [(-bev, z0), (0, z0 + bev), (0, z1)]
    return solid_rr(w, h, r, prof, n, c)

def annulus_z(c, ri, ro, z0, z1, seg=12):
    return xf(ring_between(circle(ri, seg), circle(ro, seg), z0, z1), t=(c[0], c[1], 0))

def torus(R, r, seg=20, sseg=6):
    m = trimesh.creation.torus(R, r, major_sections=seg, minor_sections=sseg); return uvp(m)  # axis = Z

def slice_y0(m):
    s = trimesh.intersections.slice_mesh_plane(m, plane_normal=[0, 1, 0], plane_origin=[0, 0, 0], cap=True)
    s = trimesh.Trimesh(s.vertices, s.faces, process=True); s.fix_normals(); return uvp(s)

def T(t=(0, 0, 0), yaw=0.0, axis=(0, 1, 0)):
    M = TF.rotation_matrix(yaw, axis) if yaw else np.eye(4); M = M.copy(); M[:3, 3] = t; return M

# ------------------------------------------------------------------ rig
class Rig:
    """nodes: name -> dict(parent, W (closed-pose world 4x4), mesh (material, local mesh) | None)."""
    def __init__(s, name): s.name = name; s.N = {}; s.order = []; s.extras = {}
    def group(s, name, parent=None, W=None):
        s.N[name] = dict(parent=parent, W=np.eye(4) if W is None else W, mesh=None); s.order.append(name); return name
    def part(s, name, parent, mat, meshes, world=True, W=None):
        """mesh part node; world=True: meshes are in closed-pose world coords and the node sits on its parent's origin."""
        assert ("glass" in name.lower()) == (mat == "glass"), name
        m = merge(meshes) if isinstance(meshes, (list, tuple)) else meshes
        Wn = W if W is not None else (s.N[parent]["W"].copy() if parent else np.eye(4))
        if world: uv = m.metadata["uv"]; m = m.copy(); m.apply_transform(np.linalg.inv(Wn)); m.metadata["uv"] = uv
        s.N[name] = dict(parent=parent, W=Wn, mesh=(mat, m)); s.order.append(name); return name
    def local(s, n):
        p = s.N[n]["parent"]; return (np.linalg.inv(s.N[p]["W"]) if p else np.eye(4)) @ s.N[n]["W"]
    def pose(s, deltas=None):
        deltas = deltas or {}; out = {}
        for n in s.order:
            p = s.N[n]["parent"]; out[n] = (out[p] if p else np.eye(4)) @ s.local(n) @ deltas.get(n, np.eye(4))
        return out
    def world_parts(s, deltas=None, colliders=False):
        Wp = s.pose(deltas); P = {}
        for n in s.order:
            mm = s.N[n]["mesh"]
            if not mm or (("colonly" in n) != colliders and not colliders == "all"): continue
            m = mm[1].copy(); m.apply_transform(Wp[n]); m.metadata["uv"] = mm[1].metadata["uv"]; P[n] = (mm[0], m)
        return P
    def shift(s, d):
        for n in s.order: s.N[n]["W"] = T(d) @ s.N[n]["W"]
    def recenter(s):
        V = np.vstack([m.vertices for _, m in s.world_parts().values()]); lo, hi = V.min(0), V.max(0)
        d = (-(lo[0] + hi[0])/2, -lo[1], -(lo[2] + hi[2])/2); s.shift(d); return np.array(d)
    def children(s, n): return [c for c in s.order if s.N[c]["parent"] == n]
    def tree(s, n=None, depth=0, lines=None):
        lines = [] if lines is None else lines
        for c in ([x for x in s.order if s.N[x]["parent"] is None] if n is None else s.children(n)):
            W = s.N[c]["W"]; L = s.local(c); q = TF.quaternion_from_matrix(L); yaw = np.degrees(2*np.arctan2(q[2], q[0])) if abs(q[2]) > 1e-9 else 0.0
            mm = s.N[c]["mesh"]; tri = len(mm[1].faces) if mm else 0
            lines.append(f"{'  '*depth}{c}{'' if mm else ' (group)'}  world_origin=({W[0,3]:.4f}, {W[1,3]:.4f}, {W[2,3]:.4f})"
                         + (f"  local_yaw={yaw:.2f}deg" if abs(yaw) > 1e-6 else "") + (f"  tris={tri}" if mm else ""))
            s.tree(c, depth + 1, lines)
        return lines
    # ---------------- glb export
    def export(s, path):
        import pygltflib as pg
        g = pg.GLTF2(); blob = bytearray(); mats = {}; idx = {}
        def add(arr, target, ctype, typ):
            arr = np.ascontiguousarray(arr); off = len(blob); blob.extend(arr.tobytes())
            while len(blob) % 4: blob.append(0)
            g.bufferViews.append(pg.BufferView(buffer=0, byteOffset=off, byteLength=arr.nbytes, target=target))
            acc = pg.Accessor(bufferView=len(g.bufferViews) - 1, componentType=ctype, count=len(arr), type=typ)
            if typ == "VEC3" and target == 34962: acc.min = arr.min(0).tolist(); acc.max = arr.max(0).tolist()
            g.accessors.append(acc); return len(g.accessors) - 1
        tris = dict(visual=0, collider=0)
        for n in s.order:
            L = s.local(n); q = TF.quaternion_from_matrix(L)  # w x y z
            node = pg.Node(name=n, translation=[float(v) for v in L[:3, 3]])
            if getattr(s, "extras", {}).get(n): node.extras = dict(s.extras[n])   # glTF extras -> Godot node metadata
            if abs(q[0] - 1) > 1e-9: node.rotation = [float(q[1]), float(q[2]), float(q[3]), float(q[0])]
            mm = s.N[n]["mesh"]
            if mm:
                mk_, m = mm; V, Nn, UV, F = dc.shade_split(m)
                tris["collider" if "colonly" in n else "visual"] += len(F)
                if mk_ not in mats:
                    pm = FMAT[mk_]; mats[mk_] = len(g.materials)
                    bc = dc._col(pm.baseColorFactor); emf = dc._col(pm.emissiveFactor if pm.emissiveFactor is not None else [0, 0, 0])
                    g.materials.append(pg.Material(name=pm.name, emissiveFactor=emf, pbrMetallicRoughness=pg.PbrMetallicRoughness(
                        baseColorFactor=bc, metallicFactor=float(pm.metallicFactor), roughnessFactor=float(pm.roughnessFactor))))
                a = pg.Attributes(POSITION=add(V.astype(np.float32), 34962, 5126, "VEC3"), NORMAL=add(Nn.astype(np.float32), 34962, 5126, "VEC3"),
                                  TEXCOORD_0=add(UV.astype(np.float32), 34962, 5126, "VEC2"))
                g.meshes.append(pg.Mesh(name=n, primitives=[pg.Primitive(attributes=a, indices=add(F.astype(np.uint32).ravel(), 34963, 5125, "SCALAR"), material=mats[mk_])]))
                node.mesh = len(g.meshes) - 1
            idx[n] = len(g.nodes); g.nodes.append(node)
        for n in s.order:
            ch = [idx[c] for c in s.children(n)]
            if ch: g.nodes[idx[n]].children = ch
        g.scenes = [pg.Scene(name=s.name, nodes=[idx[n] for n in s.order if s.N[n]["parent"] is None])]; g.scene = 0
        g.buffers = [pg.Buffer(byteLength=len(blob))]; g.set_binary_blob(bytes(blob))
        os.makedirs(os.path.dirname(path), exist_ok=True); g.save_binary(path); finish_glb(path)
        return tris

# ------------------------------------------------------------------ QA
def clip(rig, deltas=None, names=None, n_samp=400):
    P = rig.world_parts(deltas)
    if names is not None: P = {k: v for k, v in P.items() if k in names}
    return cc.check(P, n_samp=n_samp)

def summarize(chk):
    bad = [o for o in chk["overlap"] if not o[3]]
    return dict(pass_=chk["pass"] if "pass" in chk else None, worst_overlap=chk.get("worst_overlap"), bad_overlaps=bad,
                coplanar=chk["coplanar"], open=chk["open"], pivot=chk["pivot"])

def penetration(moving, fixed, n_samp=600, seed=1):
    """max depth of moving-part surface samples inside fixed closed parts (and vice versa)."""
    worst = (0.0, None, None)
    for na, (_, a) in moving.items():
        for nb, (_, b) in fixed.items():
            if np.any(a.bounds[0] > b.bounds[1] + .002) or np.any(b.bounds[0] > a.bounds[1] + .002): continue
            for (p, q, pn, qn) in ((a, b, na, nb), (b, a, nb, na)):
                for comp in q.split(only_watertight=False):
                    if not comp.is_watertight: continue
                    S = np.vstack([p.vertices, trimesh.sample.sample_surface(p, n_samp, seed=seed)[0]])
                    ins = comp.contains(S)
                    if ins.any():
                        d = float(trimesh.proximity.signed_distance(comp, S[ins]).max())
                        if d > worst[0]: worst = (d, pn, qn)
    return worst

def render(rig, deltas, path, R=None, title=None, size=720):
    P = rig.world_parts(deltas); geo = {}
    for n, (mk_, m) in P.items():
        V, Nn, UV, F = dc.shade_split(m); geo[n] = (mk_, V, Nn, F)
    R = views()[3] if R is None else R
    im = crop(dc.render_view(geo, R, size=size, shadow=True)); os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.imsave(path, np.clip(im, 0, 1)); return path

# ------------------------------------------------------------------ pass C additions (Rook 2026-11-20, Vance REALISM_SPEC section 9)
# OverrideOrange: same name/values as Sloane's door_hub_kit "orange" (Mat_Hub_OverrideOrange) so Gage's _retint keeps it.
_m("dl_orange", "Mat_Hub_OverrideOrange", (.851, .357, .149), .1, .45)
_m("dl_green", "TT_StatusGreen", (.25, .69, .42), 0, .4, em=(.25, .69, .42))
ORANGE, GREEN = "dl_orange", "dl_green"

def Vm(m):
    m = trimesh.Trimesh(m.vertices, m.faces, process=True); m.fix_normals(); return m

def boolean(op, ms):
    r = getattr(trimesh.boolean, op)([Vm(m) for m in ms], engine="manifold"); r.fix_normals(); return uvp(r)

def prism_x(pts_yz, x0, x1):
    """Rook M-122: straight prism along X of a simple polygon given in (y, z) (one solid instead of a union of boxes)."""
    from shapely.geometry import Polygon
    m = trimesh.creation.extrude_polygon(Polygon(pts_yz).buffer(0), x1 - x0)
    M = np.eye(4); M[:3, :3] = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]; M[0, 3] = x0
    m.apply_transform(M); m.fix_normals(); return uvp(m)

def handwheel(R=.18, r_rim=.012, spokes=5, hub_r=.03, hub_h=.04, seg=18, sseg=6, spoke_w=.016):
    """handwheel in its own frame: axis = local Z, rim torus at z=0, spokes radial, hub boss. Returns a list of meshes."""
    ms = [torus(R, r_rim, seg, sseg), cap((0, 0, 0), hub_r, hub_h, 10, "z")]
    for k in range(spokes):
        a = 2*np.pi*k/spokes
        ms.append(xf(box(hub_r - .004, R - r_rim*.4, -spoke_w/2, spoke_w/2, -spoke_w*.35, spoke_w*.35), R=TF.rotation_matrix(a, [0, 0, 1])))
    return ms

def place_axis(ms, c, z_dir):
    """move meshes built around local Z to centre c with local Z along z_dir (unit)."""
    R = trimesh.geometry.align_vectors([0, 0, 1], np.asarray(z_dir, float)); out = []
    for m in ms:
        M = R.copy(); M[:3, 3] = c; out.append(xf(m.copy(), R=M))
    return out

def mirror_rig(rig, name=None):
    """left-hand copy: mirror every node in X (W' = M W M, local mesh mirrored; trimesh keeps the winding outward on reflection).
    Animation in the mirrored rig: rotations about local Y and Z flip sign, translations along local X flip sign."""
    M = np.diag([-1.0, 1, 1, 1]); out = Rig(name or rig.name)
    for n in rig.order:
        d = rig.N[n]; mm = None
        if d["mesh"]:
            mk_, m = d["mesh"]; uv = m.metadata["uv"]; m2 = m.copy(); m2.apply_transform(M); m2.metadata["uv"] = uv; mm = (mk_, m2)   # trimesh re-winds reflected meshes itself
        out.N[n] = dict(parent=d["parent"], W=M @ d["W"] @ M, mesh=mm); out.order.append(n)
    out.extras = dict(getattr(rig, "extras", {}))
    return out

def tri_count(rig):
    return sum(len(rig.N[n]["mesh"][1].faces) for n in rig.order if rig.N[n]["mesh"] and "colonly" not in n)

# ------------------------------------------------------------------ pass G (Rook 2026-11-21, Gage pocket open-detail readability)
# Separate slots so the pocket head hardware reads against the alloy track / black belt / gunmetal head box. Untextured PBR factors;
# meshes keep the shared planar UV0 (uvp) like every other door-lab part, so Sloane's PBR sets can be dropped onto these names later.
# Names avoid Gage's _retint substrings (glass/vision/cyan/led/pearl/scissor/dog/linkage); the bumper keeps "Rubber" so _retint leaves it dark.
# Sloane VOTE_LOG #87 (bc70ada) slot ruling on REALISM_SPEC 13.3: 5 new DL_ slots -> 1. Bumper/end stop rubber -> DL_SealRubber;
# polished keeper/bolt and the (now clear-zinc) belt clamp -> TT_BrushedAlloy (polish only via the 2 wear rule, roughness -0.15);
# acetal anti-lift tyre -> TT_WhiteComposite; DL_SolenoidRed kept (no existing red paint slot).
_m("dl_solred", "DL_SolenoidRed", (.56, .05, .04), 0, .45)         # red powder-coated solenoid can
BUMP, YZN, SRED, POL, ACET = "dl_seal", "tt_alloy", "dl_solred", "tt_alloy", "tt_white"
