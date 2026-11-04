"""Rook: Strip 5 Tennis Tower reusable module library (spec design/strip5_tennis_tower_v1.md Rev 2.6).
Parametric primitives + a 5-variant runner. A module needs only a small builder file:
    from modlib import *
    def build(prm): p = Part(); p.add("Fin_A", G, box(...)); ...; return p
    if __name__ == "__main__": run("curtain_wall_panel", build, [dict(...)]*5, title="...")
Reuses the house pipeline: dining_chair_generator (loft/circle/rrect/xf/merge, export_final, render_view),
bath_pod_generator (Pod/cyl/set_glass_blend/views), kitchen_counter_generator (box/crop), ext_clip_check (A1-A5),
validate_models.validate_file. Conventions: metres, Y-up, +Z front, bottom-centre pivot, glass nodes contain 'glass'
(material 'Glass', BLEND), parts embed E = 4 mm (never coplanar). Sloane's PBR textures are embedded as baseColorTexture."""
import os, sys, io, json, numpy as np, trimesh
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.dirname(HERE); sys.path.insert(0, SRC)
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import dining_chair_generator as dc
from dining_chair_generator import FMAT, loft, circle, rrect, xf, merge, export_final, render_view
from bath_pod_generator import Pod, views
from kitchen_counter_generator import crop
from trimesh.visual.material import PBRMaterial as _PBR
import ext_clip_check as cc
import validate_models as vm
ROOT = dc.ROOT; E = .004; TRI_MAX = 6000
TEX = os.path.join(ROOT, "godot/assets/textures")
GLB_OUT = os.path.join(ROOT, "assets/glb/tennis_tower"); RENDER_OUT = "/workspace/renders/tennis_tower"

# ---- Aegis-7 palette (keys) + Sloane texture map (material name -> png) ----
def _m(k, name, rgb, met, rough, em=None, a=1.0):
    FMAT[k] = _PBR(name=name, baseColorFactor=(*rgb, a), metallicFactor=met, roughnessFactor=rough, **({"emissiveFactor": em} if em else {}))
_m("tt_gun", "TT_Gunmetal", (0x1A/255, 0x1E/255, 0x24/255), .8, .5)
_m("tt_steel", "TT_BrushedSteel", (.62, .65, .68), .9, .38)
_m("tt_slate", "TT_CarbonSlate", (0x28/255, 0x2E/255, 0x38/255), .25, .7)
_m("tt_cyan", "TT_CyanLED", (0, .9, 1), 0, .4, em=(0, .9, 1))
_m("tt_amber", "TT_AmberLED", (1, .584, 0), 0, .4, em=(1, .584, 0))
_m("glass", "Glass", (.70, .84, .92), 0, .05, a=.25)
_m("tt_leaf", "TT_Leaf", (.27, .50, .30), 0, .8)
_m("tt_leaf2", "TT_LeafLight", (.46, .66, .36), 0, .8)
_m("tt_soil", "TT_Soil", (.24, .18, .13), 0, .95)
_m("tt_ball", "TT_BallYellow", (.83, .90, .25), 0, .7)
LF, LF2, SO, BA = "tt_leaf", "tt_leaf2", "tt_soil", "tt_ball"
G, ST, SL, CY, AM, GL = "tt_gun", "tt_steel", "tt_slate", "tt_cyan", "tt_amber", "glass"
TEXMAP = {"TT_Gunmetal": "facade_titanium_gunmetal_hull.png", "TT_BrushedSteel": "facade_brushed_steel_gantry.png",
          "TT_CarbonSlate": "facade_titanium_gunmetal_hull.png", "Glass": "residential_atrium_glass_translucent.png"}

# ---------------- primitives (all closed meshes with uv metadata) ----------------
def box(x0, x1, y0, y1, z0, z1):  # 12-tri axis box
    o = np.array([((x1-x0)/2, (z1-z0)/2), (-(x1-x0)/2, (z1-z0)/2), (-(x1-x0)/2, -(z1-z0)/2), ((x1-x0)/2, -(z1-z0)/2)])
    return xf(loft(o, [(y0, 1, 1), (y1, 1, 1)]), t=((x0+x1)/2, 0, (z0+z1)/2))
def prism(outline_xz, y0, y1, rings=None):  # extrude any XZ outline along Y; rings=[(y,sx,sz)] for tapers
    return loft(np.asarray(outline_xz, float), rings or [(y0, 1, 1), (y1, 1, 1)])
def _orient(m, a, b):  # mesh built along +Y from 0..L -> placed from a to b
    a, b = np.asarray(a, float), np.asarray(b, float); d = b - a; L = np.linalg.norm(d); d /= L
    R = trimesh.geometry.align_vectors([0, 1, 0], d); return xf(m, R=R, t=a)
def tube(a, b, r, seg=8):  # CHS member between two points
    L = np.linalg.norm(np.subtract(b, a)); return _orient(loft(circle(r, seg), [(0, 1, 1), (L, 1, 1)]), a, b)
def beam(a, b, w, h):  # rectangular member between two points (w across X-ish, h across Z-ish)
    L = np.linalg.norm(np.subtract(b, a)); return _orient(box(-w/2, w/2, 0, L, -h/2, h/2), a, b)
def node(c, r, sub=1):  # ball node
    m = trimesh.creation.icosphere(subdivisions=sub, radius=r); m.apply_translation(c)
    v = m.vertices - c; m.metadata["uv"] = np.c_[np.arctan2(v[:, 0], v[:, 2]) / (2*np.pi) + .5, v[:, 1] / (2*r) + .5]; return m
def cap(c, r, h, seg=12, axis="z"):  # disc / cylinder cap, centre c, along axis
    c = np.asarray(c, float); d = {"x": [1, 0, 0], "y": [0, 1, 0], "z": [0, 0, 1]}[axis]
    return tube(c - np.multiply(d, h/2), c + np.multiply(d, h/2), r, seg)
def pane(x0, x1, y0, y1, z, t=.022):  # glass pane (front face toward +Z)
    return box(x0, x1, y0, y1, z - t/2, z + t/2)
def fin(x, y0, y1, depth, t, z0=0.0, belly=0.0):  # mullion fin plate projecting -Z from z0; belly>0 = fish-belly depth gain at mid-height
    o = [(t/2, 0), (-t/2, 0), (-t/2, -depth), (t/2, -depth)]
    if belly <= 0: return xf(prism(o, y0, y1), t=(x, 0, z0))
    ys = np.linspace(y0, y1, 7); rings = [(y, 1, 1 + belly * np.sin(np.pi * (y - y0) / (y1 - y0))) for y in ys]
    return xf(loft(np.array(o, float), rings), t=(x, 0, z0))
def stair(w, rise, tread, n, x=0, z=0):  # solid stepped flight rising toward -Z
    return merge([box(x-w/2, x+w/2, 0, rise*(i+1), z - tread*(i+1), z - tread*i + (E if i else 0)) for i in range(n)])
def seat_row(length, y, z, seat_w=.5, depth=.42, h=.42, back=.35):  # row of moulded seats along X
    n = max(1, int(length // seat_w)); ms = []
    for i in range(n):
        cx = -length/2 + seat_w*(i+.5); ms += [box(cx-.22, cx+.22, y, y+h*.1, z-depth, z), box(cx-.22, cx+.22, y+h*.1-E, y+h*.1+back, z-depth, z-depth+.04)]
    return merge(ms)
def louvres(x0, x1, y0, y1, z, n, t=.03, d=.12):  # horizontal greeble slats
    hs = np.linspace(y0, y1, n + 2)[1:-1]; return merge([box(x0, x1, h - t/2, h + t/2, z - d, z) for h in hs])

# ---------------- greenery primitives (low-poly, closed) ----------------
def clump(c, r, seed=0, sub=0):  # jittered icosphere foliage blob (20 tris at sub=0)
    m = node(c, r, sub); rng = np.random.default_rng(seed); v = m.vertices - c
    m.vertices = c + v * rng.uniform(.82, 1.0, (len(v), 1)) * [1, .85, 1]; return m
def leaf(c, length, width, yaw=0.0, pitch=0.0, t=.012):  # flat lancet leaf (diamond lens, 8 tris), long axis +Y before rotation
    V = np.array([(0, 0, 0), (width/2, length*.35, 0), (0, length, 0), (-width/2, length*.35, 0), (0, length*.35, t), (0, length*.35, -t)])
    F = np.array([[0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4], [1, 0, 5], [2, 1, 5], [3, 2, 5], [0, 3, 5]])
    m = trimesh.Trimesh(V, F, process=False); m.metadata["uv"] = np.c_[V[:, 0]/width + .5, V[:, 1]/length]
    return xf(m, R=trimesh.transformations.euler_matrix(pitch, yaw, 0, "rxyz"), t=c)
def planter(x0, x1, y0, z0, z1, h=.3, wall=.03):  # trough (open-top look via inset soil slab) -> (trough, soil, soil_top_y)
    return box(x0, x1, y0, y0+h, z0, z1), box(x0+wall, x1-wall, y0+h-E, y0+h+.02, z0+wall, z1-wall), y0+h+.02
def shrubs(x0, x1, y, z, r=.16, n=None, seed=0):  # row of clumps sitting on y (embedded E)
    n = n or max(1, int((x1-x0) // (1.6*r))); xs = np.linspace(x0+r, x1-r, n)
    return merge([clump((x, y + r*.85 - E, z), r, seed+i) for i, x in enumerate(xs)])
def green_wall(x0, x1, y0, y1, z, r=.14, seed=0):  # grid of clumps on a +Z face at z (embedded E)
    xs = np.arange(x0+r, x1-r+1e-6, 1.7*r); ys = np.arange(y0+r, y1-r+1e-6, 1.7*r); k = 0; ms = []
    for j, y in enumerate(ys):
        for x in xs + (r*.85 if j % 2 else 0):
            if x < x1 - r: ms.append(clump((x, y, z + r - E), r, seed+k)); k += 1
    return merge(ms)
def vine(pts, r=.012, leaf_every=.45, leaf_len=.16, seed=0, outward=False):  # polyline stem tubes + leaves -> (stem, leaves)
    pts = np.asarray(pts, float); stem = merge([tube(a, b, r, 5) for a, b in zip(pts[:-1], pts[1:])]); ls = []; rng = np.random.default_rng(seed)
    for a, b in zip(pts[:-1], pts[1:]):
        L = np.linalg.norm(b-a)
        for k in range(1, max(2, int(L // leaf_every))):
            q = a + (b-a)*k/max(2, int(L // leaf_every)); ls.append(leaf(q + [0, 0, r*2.2], leaf_len, leaf_len*.5, rng.uniform(-.6, .6), 1.2 if outward else rng.choice([-1.2, 1.2])))
    return stem, merge(ls)

def ring_band(r, y, h=.05, n=16, t=.02):  # segmented annular band hugging a round host of radius r (embed E), e.g. LED rings
    w = 2*r*np.tan(np.pi/n) + .002
    return merge([xf(box(-w/2, w/2, y - h/2, y + h/2, r - E, r - E + t), R=trimesh.transformations.rotation_matrix(k*2*np.pi/n, [0, 1, 0])) for k in range(n)])
def leaf_dir(c, d, length, width, t=.02):  # leaf whose long axis points along direction d
    d = np.asarray(d, float); return xf(leaf((0, 0, 0), length, width, t=t), R=trimesh.geometry.align_vectors([0, 1, 0], d / np.linalg.norm(d)), t=c)

class Part(Pod):
    """Pod + name guard: only glass-material parts may contain 'glass' (and they must)."""
    def __init__(s, name="module"): super().__init__(name)
    def add(s, part, mat, *meshes):
        assert ("glass" in part.lower()) == (mat == GL), f"naming rule: {part} / {mat}"
        super().add(part, mat, *meshes)

def recenter(p):
    V = np.vstack([m.vertices for _, m in p.P.values()]); lo, hi = V.min(0), V.max(0); d = (-(lo[0]+hi[0])/2, -lo[1], -(lo[2]+hi[2])/2)
    for k, (mk, m) in p.P.items(): uv = m.metadata["uv"]; m.apply_translation(d); m.metadata["uv"] = uv
    return p

# ---------------- GLB post-process: BLEND glass + Sloane textures ----------------
def finish_glb(path):
    import pygltflib as pg
    g = pg.GLTF2().load(path); blob = bytearray(g.binary_blob()); cache = {}
    if not g.samplers: g.samplers.append(pg.Sampler(magFilter=9729, minFilter=9987, wrapS=10497, wrapT=10497))
    for m in g.materials:
        if m.name == "Glass": m.alphaMode = "BLEND"; m.doubleSided = True
        f = TEXMAP.get(m.name); fp = f and os.path.join(TEX, f)
        if not fp or not os.path.exists(fp): continue
        if fp not in cache:
            from PIL import Image
            im = Image.open(fp).convert("RGBA" if m.name == "Glass" else "RGB").resize((256, 256)); b = io.BytesIO(); im.save(b, "PNG", optimize=True); data = b.getvalue()
            while len(blob) % 4: blob.append(0)
            g.bufferViews.append(pg.BufferView(buffer=0, byteOffset=len(blob), byteLength=len(data))); blob.extend(data)
            g.images.append(pg.Image(bufferView=len(g.bufferViews)-1, mimeType="image/png")); g.textures.append(pg.Texture(source=len(g.images)-1, sampler=0))
            cache[fp] = len(g.textures) - 1
        m.pbrMetallicRoughness.baseColorTexture = pg.TextureInfo(index=cache[fp])
    while len(blob) % 4: blob.append(0)
    g.buffers[0].byteLength = len(blob); g.set_binary_blob(bytes(blob)); g.save_binary(path)

def name_rule(p):
    return all(("glass" in k.lower()) == (mk == GL) for k, (mk, _) in p.P.items())

# ---------------- variant runner ----------------
def run(module, builder, params, title="", tri_max=TRI_MAX, suffix=""):
    """builder(prm) -> Part. params: list of 5 dicts, each with 'label'. Writes v1..v5.glb, validates, renders, contact sheet."""
    gdir = os.path.join(GLB_OUT, module); rdir = os.path.join(RENDER_OUT, module); os.makedirs(gdir, exist_ok=True); os.makedirs(rdir, exist_ok=True)
    iso = views()[3]; rep = []; tiles = []
    for i, prm in enumerate(params, 1):
        p = recenter(builder(prm)); chk = cc.check(p.P, n_samp=400)
        gp = os.path.join(gdir, f"v{i}{suffix}.glb"); tris, geo = export_final(p.P, [gp]); finish_glb(gp)
        try: ok_v = vm.validate_file(gp, check_tri_range=(1, tri_max), require_textures=False, require_blend_glass=any(mk == GL for mk, _ in p.P.values()))
        except AssertionError as e: print('VALIDATE FAIL', e); ok_v = False
        r = dict(v=f"v{i}", label=prm.get("label", ""), tris=int(tris), clip_pass=chk["pass"], worst_overlap=chk["worst_overlap"],
                 bad_overlaps=[o for o in chk["overlap"] if not o[3]], coplanar=chk["coplanar"], open=chk["open"], pivot=chk["pivot"], size=chk["size"],
                 names_ok=name_rule(p), validate=bool(ok_v), passed=bool(ok_v and chk["pass"] and tris <= tri_max and name_rule(p)))
        rep.append(r); print(json.dumps(r))
        im = crop(render_view(geo, iso, size=640, shadow=True, glass_alpha=.35)); plt.imsave(os.path.join(rdir, f"v{i}{suffix}.png"), np.clip(im, 0, 1))
        tiles.append((f"V{i}  {r['label'].replace(': ', chr(10)).replace(', ', chr(10))}\n{tris} tris | {'PASS' if r['passed'] else 'FAIL'}", im))
    fig, axs = plt.subplots(1, len(tiles), figsize=(4.4*len(tiles), 9), facecolor="#F4F2EC")
    for ax, (t, im) in zip(np.atleast_1d(axs), tiles): ax.imshow(np.clip(im, 0, 1)); ax.axis("off"); ax.set_title(t, fontsize=10, color="#222")
    fig.suptitle(f"Rook | Tennis Tower {module} V1-V5 | {title}", fontsize=13, color="#333"); plt.tight_layout(rect=(0, 0, 1, .95))
    sp = os.path.join(rdir, f"{module}{suffix}_contact_sheet.png"); fig.savefig(sp, dpi=90, facecolor="#F4F2EC"); plt.close(fig)
    json.dump(rep, open(os.path.join(rdir, f"report{suffix}.json"), "w"), indent=1); print("sheet", sp); return rep
