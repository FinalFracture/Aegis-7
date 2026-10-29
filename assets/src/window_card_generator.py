#!/usr/bin/env python3
"""Lit window interior card (#6) - 5 approach iterations. Owner: Rook.
Card 3.0 x 1.5 m sits just behind an apartment's exterior window. Pivot is bottom-center, card faces +Z,
geometry extends into -Z (into the room). Unlit/emissive materials, procedurally painted textures.
Outputs design/assets/window_card/iter_0N.glb (+ textures), iter_0N_sheet.png and overview.png."""
import os, numpy as np
from PIL import Image, ImageDraw, ImageFilter
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "design/assets/window_card")
CW, CH = 3.0, 1.5
TW, TH = 1024, 512            # card texture size (2:1 matches 3.0 x 1.5)

# ---------------- per-unit profiles (layout v2 rev C story notes) ----------------
UNITS = {
 "101": dict(tint=(1.00, 0.80, 0.55), lights=0.35, props=["bunk", "table", "chair"], accent="violet"),   # night-shift tech, dim
 "102": dict(tint=(1.00, 0.86, 0.66), lights=1.0, props=["sofa", "plants_down", "hook"], accent="amber"), # elder, plants knocked over
 "103": dict(tint=(1.00, 0.78, 0.52), lights=1.0, props=["table", "chair", "chair", "sofa", "toys"], accent="amber"),  # family, toys by window
 "104": dict(tint=(0.80, 0.90, 1.00), lights=1.0, props=["desk_slates", "chair", "shelf"], accent="violet"),  # researcher, red glyph
 "202": dict(tint=(1.00, 0.82, 0.60), lights=1.0, props=["table", "chair", "chair", "drawing", "toys"], accent="amber"),
 "203": dict(tint=(0.95, 0.85, 0.70), lights=1.0, props=["sofa", "route_model", "plants"], accent="violet"),
 "204": dict(tint=(0.85, 0.92, 1.00), lights=1.0, props=["bench", "chair", "shelf"], accent="violet"),
 "201": dict(tint=(1.00, 0.80, 0.58), lights=0.0, props=["bench", "chair", "bed"], accent="amber"),     # player apt: lights off
}
SHOW = ["103", "104", "101"]     # variants shown on sheets
VIOLET, AMBER = (184, 90, 255), (255, 165, 58)

def px(x, y):  # metres on card (x from left, y from floor) -> pixel
    return int(x / CW * TW), int(TH - y / CH * TH)

def rr(d, x0, y0, x1, y1, fill, r=6):
    a, b = px(x0, y1), px(x1, y0); d.rounded_rectangle([a, b], r, fill=fill)

def prop(d, kind, x, tint, k):
    s = lambda c: tuple(int(v) for v in c) + (255,)
    dk = s(np.array([46, 50, 60]) * (0.6 + 0.4 * k)); al = s(np.array([150, 155, 165]) * (0.5 + 0.5 * k))
    fab = s(np.array([70, 76, 92]) * (0.6 + 0.4 * k))
    if kind == "chair":      # swivel chair silhouette
        rr(d, x - .2, .0, x + .2, .02, dk, 2); rr(d, x - .03, .02, x + .03, .40, al, 2)
        rr(d, x - .22, .40, x + .22, .47, fab, 6); rr(d, x - .03, .40, x + .03, .75, al, 2); rr(d, x - .2, .66, x + .2, .86, fab, 8)
    elif kind == "table":
        rr(d, x - .5, .72, x + .5, .76, al, 3); rr(d, x - .45, 0, x - .4, .72, dk, 1); rr(d, x + .4, 0, x + .45, .72, dk, 1)
    elif kind == "sofa":
        rr(d, x - .55, .05, x + .55, .42, fab, 10); rr(d, x - .55, .38, x + .55, .75, fab, 12); rr(d, x - .62, .05, x - .48, .55, dk, 8); rr(d, x + .48, .05, x + .62, .55, dk, 8)
    elif kind in ("bunk", "bed"):
        rr(d, x - .6, .25, x + .6, .45, fab, 8); rr(d, x - .6, .0, x - .55, .9 if kind == "bunk" else .55, al, 2); rr(d, x + .55, 0, x + .6, .9 if kind == "bunk" else .55, al, 2)
        rr(d, x - .5, .42, x - .2, .52, s((200, 200, 210)), 8)
    elif kind in ("desk_slates", "bench"):
        rr(d, x - .6, .74, x + .6, .78, al, 2); rr(d, x - .58, 0, x - .52, .74, dk, 1); rr(d, x + .52, 0, x + .58, .74, dk, 1)
        if kind == "desk_slates":
            for i in range(3):
                xx = x - .4 + i * .35; rr(d, xx - .13, .80, xx + .13, .98, s((25, 28, 34)), 3)
                c = px(xx, .89); d.ellipse([c[0] - 9, c[1] - 9, c[0] + 9, c[1] + 9], fill=(235, 40, 40, 255))
        else:
            rr(d, x - .3, .78, x + .1, .86, s((90, 95, 110)), 2); rr(d, x + .2, .78, x + .4, .95, s((120, 90, 220)), 3)
    elif kind == "shelf":
        for h in (.9, 1.15):
            rr(d, x - .4, h, x + .4, h + .03, al, 1)
            for i in range(4): rr(d, x - .35 + i * .19, h + .03, x - .25 + i * .19, h + .16 + .03 * (i % 2), s((120 + 30 * i, 110, 100)), 1)
    elif kind in ("plants", "plants_down"):
        if kind == "plants":
            rr(d, x - .12, 0, x + .12, .3, dk, 4)
            for i in range(7):
                c = px(x + .25 * np.sin(i * 1.7), .35 + .08 * i); d.ellipse([c[0] - 22, c[1] - 9, c[0] + 22, c[1] + 9], fill=s((60, 120, 70)))
        else:
            d.polygon([px(x - .3, 0), px(x - .05, .25), px(x + .05, .2), px(x - .2, 0)], fill=dk)
            for i in range(5):
                c = px(x + .1 * i, .03); d.ellipse([c[0] - 20, c[1] - 7, c[0] + 20, c[1] + 7], fill=s((60, 110, 65)))
    elif kind == "hook":
        rr(d, x - .03, 1.1, x + .03, 1.2, al, 2)            # empty suit hook
    elif kind == "toys":
        rng = np.random.default_rng(3)
        for i in range(9):
            xx, yy = x + rng.uniform(-.5, .5), rng.uniform(0, .5) + (.25 if i % 3 == 0 else 0)
            c = px(xx, yy); r = int(rng.uniform(8, 16)); col = [(230, 90, 70), (80, 160, 230), (240, 200, 60), (120, 200, 120)][i % 4]
            (d.ellipse if i % 2 else d.rectangle)([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=s(np.array(col) * (0.5 + 0.5 * k)))

def paint(unit):
    """Returns dict of RGBA float layers: back, mid, fore, flat."""
    u = UNITS[unit]; k = max(u["lights"], 0.12); tint = np.array(u["tint"])
    yy = np.linspace(1, 0, TH)[:, None]
    wall = (np.array([0.62, 0.58, 0.54]) * tint)[None, None] * (0.55 + 0.45 * yy[..., None]) * np.ones((TH, TW, 1))
    xs = np.linspace(-1, 1, TW)[None]
    wall *= (1 - 0.25 * xs[..., None] ** 2)
    floor = yy < 0.16; wall[floor[:, 0]] = (np.array([0.32, 0.30, 0.30]) * tint)
    back = Image.fromarray((np.clip(wall * k * 1.1, 0, 1) * 255).astype(np.uint8)).convert("RGBA")
    d = ImageDraw.Draw(back)
    for x in np.arange(0.35, CW, 0.62):                 # chamfered wall panel seams
        a, b = px(x, .25), px(x, 1.5); d.line([a, b], fill=(40, 38, 40, 255), width=3); d.line([(a[0] + 3, a[1]), (b[0] + 3, b[1])], fill=(200, 190, 175, 90), width=1)
    rr(d, 0, 1.02, CW, 1.05, (60, 60, 66, 255), 0)      # inset band
    acc = VIOLET if u["accent"] == "violet" else AMBER
    rr(d, 2.2, 1.025, 2.6, 1.045, acc + (255,), 2)
    if "drawing" in u["props"]: rr(d, 1.3, 1.1, 1.6, 1.35, (235, 230, 215, 255), 2)
    if "route_model" in u["props"]:
        c0 = px(2.1, 1.22); d.ellipse([c0[0] - 60, c0[1] - 28, c0[0] + 60, c0[1] + 28], outline=(200, 200, 215, 255), width=3)
    # ceiling light glow
    g = np.zeros((TH, TW)); g[:6, int(TW * .2):int(TW * .8)] = 1; g = gaussian_filter(g, 40) * 30 * u["lights"]
    lamp = np.zeros((TH, TW)); c = px(0.6, 1.1); lamp[c[1], c[0]] = 1; lamp = gaussian_filter(lamp, 70) * 7000 * u["lights"]
    b = np.asarray(back).astype(float) / 255
    b[..., :3] += (g + lamp)[..., None] * tint * 0.6
    if u["lights"] == 0:          # lights off: cool moonlight + a lone screen glow
        b[..., :3] = b[..., :3] * np.array([0.5, 0.6, 0.9]) * 0.55
        sg = np.zeros((TH, TW)); c = px(2.3, .9); sg[c[1], c[0]] = 1; b[..., :3] += gaussian_filter(sg, 30)[..., None] * 3000 * np.array([.4, .6, 1])
    back = np.clip(b, 0, 1)
    mid = Image.new("RGBA", (TW, TH), (0, 0, 0, 0)); fore = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
    dm, df = ImageDraw.Draw(mid), ImageDraw.Draw(fore)
    big = [p for p in u["props"] if p in ("sofa", "bunk", "bed", "desk_slates", "bench", "shelf", "table", "hook", "plants")]
    slots = np.linspace(0.7, 2.3, max(len(big), 1))
    for p, x in zip(big, slots): prop(dm, p, x, tint, k)
    fslots = iter([0.9, 2.0, 1.45, 2.6])
    for p in u["props"]:
        if p in ("chair", "toys", "plants_down"): prop(df, p, next(fslots), tint, min(1, k * 1.15))
    mid = np.asarray(mid).astype(float) / 255; fore = np.asarray(fore).astype(float) / 255
    fore[..., :3] *= 0.8                       # foreground is closer to the window: a bit backlit
    flat = back.copy()
    for L in (mid, fore): flat[..., :3] = flat[..., :3] * (1 - L[..., 3:]) + L[..., :3] * L[..., 3:]
    return dict(back=back, mid=mid, fore=fore, flat=flat)

def frosted(L):
    f = L["flat"].copy()
    sil = np.zeros((TH, TW)); im = Image.new("L", (TW, TH), 0); d = ImageDraw.Draw(im)
    c = px(1.9, 1.45); d.ellipse([c[0] - 30, c[1] - 30, c[0] + 30, c[1] + 30], fill=255)   # person silhouette
    a, b = px(1.75, 0.0), px(2.05, 1.32); d.rounded_rectangle([a[0], b[1], b[0], a[1]], 25, fill=255)
    sil = np.asarray(im) / 255.0
    f[..., :3] *= (1 - 0.75 * sil[..., None])
    for ch in range(3): f[..., ch] = gaussian_filter(f[..., ch], 14)
    lum = f[..., :3].mean(-1, keepdims=True); f[..., :3] = 0.7 * f[..., :3] + 0.3 * lum
    noise = gaussian_filter(np.random.default_rng(1).normal(0, 1, (TH, TW)), 1.2) * 0.05
    f[..., :3] = np.clip(f[..., :3] * 0.9 + 0.08 + noise[..., None], 0, 1); f[..., 3] = 1
    return f

def blinds(unit):
    u = UNITS[unit]; a = np.zeros((TH, TW, 4)); n = 22; ph = TH / n
    drawn = 0.55                                       # top 55% has blinds lowered, slats tilted
    for i in range(int(n * drawn) + 1):
        y0 = int(i * ph); y1 = int(y0 + ph * 0.72)
        a[y0:y1, :, :3] = np.array([0.80, 0.78, 0.74]) * np.linspace(0.75, 1.0, y1 - y0)[:, None, None] * max(u["lights"], .25)
        a[y0:y1, :, 3] = 0.96
        a[y1 - 2:y1, :, :3] = np.array(u["tint"]) * (0.4 + 0.6 * u["lights"]); a[y1 - 2:y1, :, 3] = 1  # lit slat edge
    yb = int(TH * drawn + ph); a[yb:yb + 10, :, :3] = 0.35; a[yb:yb + 10, :, 3] = 1         # bottom rail
    a[:yb, int(TW * .85):int(TW * .855), :3] = 0.3; a[:yb, int(TW * .85):int(TW * .855), 3] = 1  # cord
    return a

# ---------------- meshes ----------------
def quad(w, h, z, y0=0.0, uv=(0, 0, 1, 1)):
    V = np.array([[-w / 2, y0, z], [w / 2, y0, z], [w / 2, y0 + h, z], [-w / 2, y0 + h, z]])
    u0, v0, u1, v1 = uv
    return V, np.array([[u0, v0], [u1, v0], [u1, v1], [u0, v1]]), np.array([[0, 1, 2], [0, 2, 3]])

def build(it, unit):
    """Returns list of submeshes: (name, V, UV, F, tex RGBA float, alpha_mode)."""
    L = paint(unit)
    if it == 1:
        return [("Card", *quad(CW, CH, 0), L["flat"], "OPAQUE")]
    if it == 2:   # shallow interior box (fake interior mapping), atlas 1024x1024
        D = 0.8; at = np.zeros((1024, 1024, 4)); at[..., 3] = 1
        at[:512] = L["flat"]
        fl = np.zeros((256, 512, 4)); fl[..., 3] = 1; fl[..., :3] = L["flat"][-20, ::2, :3][None] * np.linspace(0.6, 1.0, 256)[:, None, None]
        fl[::32, :, :3] *= 0.7
        ce = np.ones((256, 512, 4)); ce[..., :3] = L["flat"][4, ::2, :3][None] * np.linspace(1.0, 0.6, 256)[:, None, None]
        side = np.ones((256, 512, 4)); side[..., :3] = L["back"][::2, :512, :3][:256] * 0.85
        at[512:768, :512], at[512:768, 512:], at[768:, :512], at[768:, 512:] = fl, ce, side, side[:, ::-1]
        tr = lambda r: (r[0] / 1024, 1 - r[3] / 1024, r[2] / 1024, 1 - r[1] / 1024)   # pixel rect -> uv
        parts = []
        V, U, F = quad(CW, CH, -D, uv=tr((0, 0, 1024, 512))); parts.append(("Back", V, U, F))
        h, w = CH, CW
        V = np.array([[-w/2, 0, 0], [w/2, 0, 0], [w/2, 0, -D], [-w/2, 0, -D]]); u = tr((0, 512, 512, 768))
        parts.append(("Floor", V, np.array([[u[0], u[1]], [u[2], u[1]], [u[2], u[3]], [u[0], u[3]]]), np.array([[0, 2, 1], [0, 3, 2]])))
        V = np.array([[-w/2, h, -D], [w/2, h, -D], [w/2, h, 0], [-w/2, h, 0]]); u = tr((512, 512, 1024, 768))
        parts.append(("Ceiling", V, np.array([[u[0], u[1]], [u[2], u[1]], [u[2], u[3]], [u[0], u[3]]]), np.array([[0, 2, 1], [0, 3, 2]])))
        V = np.array([[-w/2, 0, 0], [-w/2, 0, -D], [-w/2, h, -D], [-w/2, h, 0]]); u = tr((0, 768, 512, 1024))
        parts.append(("WallL", V, np.array([[u[0], u[1]], [u[2], u[1]], [u[2], u[3]], [u[0], u[3]]]), np.array([[0, 1, 2], [0, 2, 3]])))
        V = np.array([[w/2, 0, -D], [w/2, 0, 0], [w/2, h, 0], [w/2, h, -D]]); u = tr((512, 768, 1024, 1024))
        parts.append(("WallR", V, np.array([[u[0], u[1]], [u[2], u[1]], [u[2], u[3]], [u[0], u[3]]]), np.array([[0, 1, 2], [0, 2, 3]])))
        V = np.vstack([p[1] for p in parts]); U = np.vstack([p[2] for p in parts])
        F = np.vstack([p[3] + 4 * i for i, p in enumerate(parts)])
        return [("InteriorBox", V, U, F, at, "OPAQUE")]
    if it == 3:   # layered cutout planes
        return [("Layer_Back", *quad(CW * 1.3, CH * 1.15, -1.2, -0.1), L["back"], "OPAQUE"),
                ("Layer_Mid", *quad(CW, CH, -0.7), L["mid"], "BLEND"),
                ("Layer_Fore", *quad(CW, CH, -0.3), L["fore"], "BLEND")]
    if it == 4:
        return [("FrostedCard", *quad(CW, CH, 0), frosted(L), "OPAQUE")]
    if it == 5:
        return [("Room", *quad(CW * 1.15, CH, -0.6), L["flat"], "OPAQUE"),
                ("Blinds", *quad(CW, CH, -0.04), blinds(unit), "BLEND")]

# ---------------- glb writer (unlit, external PNGs) ----------------
def write_glb(parts, path, tex_prefix):
    from pygltflib import (GLTF2, Scene, Node, Mesh, Primitive, Attributes, Buffer, BufferView, Accessor,
                           Material, PbrMetallicRoughness, TextureInfo, Texture, Image as GImage, Sampler)
    g = GLTF2(); blob = bytearray(); tris = 0; texfiles = []
    g.extensionsUsed = ["KHR_materials_unlit"]; g.samplers = [Sampler(magFilter=9729, minFilter=9987)]
    def add(arr, target, ct, typ, mm=False):
        arr = np.ascontiguousarray(arr); off = len(blob); blob.extend(arr.tobytes())
        while len(blob) % 4: blob.append(0)
        g.bufferViews.append(BufferView(buffer=0, byteOffset=off, byteLength=arr.nbytes, target=target))
        a = Accessor(bufferView=len(g.bufferViews) - 1, componentType=ct, count=len(arr), type=typ)
        if mm: a.min, a.max = arr.min(0).tolist(), arr.max(0).tolist()
        g.accessors.append(a); return len(g.accessors) - 1
    for name, V, U, F, tex, mode in parts:
        fn = f"{tex_prefix}_{name.lower()}.png"; texfiles.append(fn)
        im = (np.clip(tex, 0, 1) * 255).astype(np.uint8)
        Image.fromarray(im if mode == "BLEND" else im[..., :3]).save(os.path.join(os.path.dirname(path), fn))
        g.images.append(GImage(uri=fn)); g.textures.append(Texture(source=len(g.images) - 1, sampler=0))
        ti = len(g.textures) - 1
        g.materials.append(Material(name=name + "_Unlit", alphaMode=mode, doubleSided=False, emissiveFactor=[1, 1, 1],
            emissiveTexture=TextureInfo(index=ti), extensions={"KHR_materials_unlit": {}},
            pbrMetallicRoughness=PbrMetallicRoughness(baseColorTexture=TextureInfo(index=ti), metallicFactor=0, roughnessFactor=1)))
        N = np.zeros_like(V); e1 = V[F[:, 1]] - V[F[:, 0]]; e2 = V[F[:, 2]] - V[F[:, 0]]
        fn_ = np.cross(e1, e2); np.add.at(N, F[:, 0], fn_); np.add.at(N, F[:, 1], fn_); np.add.at(N, F[:, 2], fn_)
        N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
        at = Attributes(POSITION=add(V.astype(np.float32), 34962, 5126, "VEC3", True), NORMAL=add(N.astype(np.float32), 34962, 5126, "VEC3"),
                        TEXCOORD_0=add(np.c_[U[:, 0], 1 - U[:, 1]].astype(np.float32), 34962, 5126, "VEC2"))
        g.meshes.append(Mesh(name=name, primitives=[Primitive(attributes=at, indices=add(F.astype(np.uint32).ravel(), 34963, 5125, "SCALAR"), material=len(g.materials) - 1)]))
        g.nodes.append(Node(name=name, mesh=len(g.meshes) - 1)); tris += len(F)
    g.scenes = [Scene(nodes=list(range(len(g.nodes))))]; g.scene = 0
    g.buffers = [Buffer(byteLength=len(blob))]; g.set_binary_blob(bytes(blob)); g.save_binary(path)
    return tris, texfiles

# ---------------- textured rasterizer ----------------
def raster(items, cam, W, H, bg, ss=2):
    """items: dicts with P(N,3) F(M,3) and either UV+tex (unlit) or color (lit lambert w/ normals). cam(P)->(x,y,w)."""
    S = (W * ss, H * ss); img = np.ones((S[1], S[0], 3)) * np.array(bg); zb = np.full((S[1], S[0]), np.inf)
    L = np.array([-0.4, 0.6, 0.7]); L /= np.linalg.norm(L)
    tris = []
    for it in items:
        sx, sy, w = cam(it["P"]); p = np.c_[sx * ss, sy * ss]
        for f in it["F"]:
            blend = it.get("tex") is not None and it.get("blend", False) or it.get("alpha", 1) < 1
            tris.append((blend, -w[f].mean(), it, f, p, w))
    tris.sort(key=lambda t: (t[0], t[1] if t[0] else 0))
    for blend, _, it, f, p, w in tris:
        a, b, c = p[f]
        x0, y0 = np.floor(np.minimum(np.minimum(a, b), c)).astype(int); x1, y1 = np.ceil(np.maximum(np.maximum(a, b), c)).astype(int)
        x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, S[0] - 1), min(y1, S[1] - 1)
        if x1 < x0 or y1 < y0: continue
        d = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
        if abs(d) < 1e-9: continue
        X, Y = np.meshgrid(np.arange(x0, x1 + 1) + .5, np.arange(y0, y1 + 1) + .5)
        w0 = ((b[1] - c[1]) * (X - c[0]) + (c[0] - b[0]) * (Y - c[1])) / d; w1 = ((c[1] - a[1]) * (X - c[0]) + (a[0] - c[0]) * (Y - c[1])) / d; w2 = 1 - w0 - w1
        ins = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
        iw = 1 / w[f]; den = w0 * iw[0] + w1 * iw[1] + w2 * iw[2]; zz = 1 / den
        zs = zb[y0:y1 + 1, x0:x1 + 1]; m = ins & (zz < zs - 1e-6)
        if not m.any(): continue
        if it.get("tex") is not None:
            uv = it["UV"][f]; q = (w0 * iw[0])[..., None] * uv[0] + (w1 * iw[1])[..., None] * uv[1] + (w2 * iw[2])[..., None] * uv[2]
            q = q / den[..., None]; T = it["tex"]; th, tw = T.shape[:2]
            ui = np.clip((q[..., 0] * tw).astype(int), 0, tw - 1); vi = np.clip(((1 - q[..., 1]) * th).astype(int), 0, th - 1)
            col = T[vi, ui]; rgb, al = col[..., :3] * it.get("gain", 1.0), col[..., 3] if T.shape[2] == 4 else np.ones(vi.shape)
        else:
            P3 = it["P"][f]; n = np.cross(P3[1] - P3[0], P3[2] - P3[0]); n /= np.linalg.norm(n) + 1e-12
            sh = it.get("amb", 0.35) + 0.65 * max(n @ L, 0)
            rgb = np.ones(X.shape + (3,)) * np.array(it["color"]) * sh
            if "grad" in it: rgb = rgb * (1 + it["grad"] * (Y - y0) / max(y1 - y0, 1))[..., None]
            al = np.full(X.shape, it.get("alpha", 1.0))
        sub = img[y0:y1 + 1, x0:x1 + 1]
        if blend:
            m = m & (al > 0.01); sub[m] = sub[m] * (1 - al[m, None]) + rgb[m] * al[m, None]
            if it.get("zwrite", False): zs[m] = zz[m]
        else:
            m = m & (al > 0.5); sub[m] = rgb[m]; zs[m] = zz[m]
    img = np.clip(img, 0, 1)
    return img.reshape(H, ss, W, ss, 3).mean((1, 3))

def ortho(R, center, span, W, H):
    def cam(P):
        q = (P - center) @ R.T
        return q[:, 0] / span * W + W / 2, H / 2 - q[:, 1] / span * W, 100 - q[:, 2]
    return cam

def persp(eye, target, fov, W, H):
    f = target - eye; f /= np.linalg.norm(f); r = np.cross(f, [0, 1, 0]); r /= np.linalg.norm(r); u = np.cross(r, f)
    t = np.tan(np.radians(fov) / 2)
    def cam(P):
        q = P - eye; x, y, z = q @ r, q @ u, q @ f
        return (x / z / t) * W / 2 + W / 2, H / 2 - (y / z / t) * W / 2, z
    return cam

def card_items(parts, offset=(0, 0, 0), gain=1.0):
    return [dict(P=V + np.array(offset), F=F, UV=U, tex=T, blend=(m == "BLEND"), gain=gain) for _, V, U, F, T, m in parts]

def box_items(x0, y0, z0, x1, y1, z1, color, **kw):
    V = np.array([[x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0], [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]], float)
    F = np.array([[0, 2, 1], [0, 3, 2], [4, 5, 6], [4, 6, 7], [0, 1, 5], [0, 5, 4], [3, 7, 6], [3, 6, 2], [0, 4, 7], [0, 7, 3], [1, 2, 6], [1, 6, 5]])
    return dict(P=V, F=F, color=color, **kw)

def exterior(it, W=900, H=420):
    """Facade at dusk with three windows (units in SHOW); window glass at z=+0.2, wall face z=+0.35."""
    items = []; xs = [-3.8, 0.0, 3.8]; wall = (0.33, 0.35, 0.40); sill = 0.9
    # wall made of panels around three openings
    edges = [-6.0] + sum([[x - CW / 2, x + CW / 2] for x in xs], []) + [6.0]
    for i in range(0, len(edges), 2):
        items.append(box_items(edges[i], -1.2, 0.05, edges[i + 1], 3.6, 0.35, wall))
    for x in xs:
        items.append(box_items(x - CW / 2, -1.2, 0.05, x + CW / 2, sill, 0.35, wall))
        items.append(box_items(x - CW / 2, sill + CH, 0.05, x + CW / 2, 3.6, 0.35, wall))
        fr = (0.16, 0.16, 0.19)
        items += [box_items(x - CW / 2 - .08, sill - .08, .3, x + CW / 2 + .08, sill, .4, fr), box_items(x - CW / 2 - .08, sill + CH, .3, x + CW / 2 + .08, sill + CH + .08, .4, fr),
                  box_items(x - CW / 2 - .08, sill, .3, x - CW / 2, sill + CH, .4, fr), box_items(x + CW / 2, sill, .3, x + CW / 2 + .08, sill + CH, .4, fr),
                  box_items(x - .02, sill, .18, x + .02, sill + CH, .24, fr)]
        items.append(box_items(x - CW / 2, sill - .02, .38, x - CW / 2 + .5, sill, .42, (0.72, 0.35, 1.0), amb=1.0))   # violet sill accent
        glass = dict(P=np.array([[x - CW / 2, sill, .2], [x + CW / 2, sill, .2], [x + CW / 2, sill + CH, .2], [x - CW / 2, sill + CH, .2]]),
                     F=np.array([[0, 1, 2], [0, 2, 3]]), color=(0.55, 0.65, 0.78), alpha=0.16, amb=1.0, grad=-0.5)
        items.append(glass)
    for x, unit in zip(xs, SHOW):
        items += card_items(build(it, unit), (x, sill, 0.0))
    # slab band between floors
    items.append(box_items(-6, -1.2, 0.35, 6, -0.9, 0.5, (0.22, 0.23, 0.27)))
    items.append(box_items(-6, 3.3, 0.35, 6, 3.6, 0.5, (0.22, 0.23, 0.27)))
    cam = persp(np.array([2.5, 1.65, 15.0]), np.array([0.0, 1.6, 0.0]), 34, W, H)
    return raster(items, cam, W, H, (0.12, 0.13, 0.17))

def sheet(it, parts, path, ext):
    fig = plt.figure(figsize=(13, 9.6), facecolor="#F4F2EC"); gs = fig.add_gridspec(2, 3, height_ratios=[1, 1.15])
    R_top = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]]); R_side = np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]])
    a, b = np.radians(35), np.radians(25)
    Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]); Rx = np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]])
    allV = np.vstack([p[1] for p in parts]); c = (allV.min(0) + allV.max(0)) / 2
    bg = (0.955, 0.948, 0.925)
    views = [("Top", R_top), ("Front", np.eye(3)), ("Side", R_side), ("Iso", Rx @ Ry)]
    axes = [fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[0, 2]), fig.add_subplot(gs[1, 0])]
    for ax, (t, R) in zip(axes, views):
        items = card_items(parts)
        # faint edge frame so thin planes stay readable from Top/Side
        for _, V, _, F, _, _ in parts:
            mn, mx = V.min(0), V.max(0); e = 0.012
            items.append(box_items(mn[0] - e, mn[1] - e, mn[2] - e, mx[0] + e, mx[1] + e, mx[2] + e, (0.45, 0.47, 0.52), alpha=0.18, amb=0.9))
        ax.imshow(raster(items, ortho(R, c, 3.9, 520, 420), 520, 420, bg)); ax.axis("off"); ax.set_title(t, y=-0.08, fontsize=11, color="#555")
    ax = fig.add_subplot(gs[1, 1:]); ax.imshow(ext); ax.axis("off")
    ax.set_title("Exterior view (units " + ", ".join(SHOW) + ")", y=-0.08, fontsize=11, color="#555")
    plt.tight_layout(); fig.savefig(path, dpi=100, facecolor="#F4F2EC"); plt.close(fig)

NAMES = {1: "Flat painted quad", 2: "Interior box (fake interior mapping)", 3: "Layered cutout planes", 4: "Frosted privacy glass", 5: "Blinds over lit room"}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); exts = []
    for it in range(1, 6):
        parts = build(it, "103")
        tris, tex = write_glb(parts, os.path.join(OUT, f"iter_0{it}.glb"), f"iter_0{it}_u103")
        ext = exterior(it); exts.append(ext)
        sheet(it, parts, os.path.join(OUT, f"iter_0{it}_sheet.png"), ext)
        print(f"iter_0{it} {NAMES[it]}: tris={tris} textures={[(t, Image.open(os.path.join(OUT, t)).size) for t in tex]}")
    fig, axs = plt.subplots(1, 5, figsize=(25, 3.6), facecolor="#F4F2EC")
    for i, (ax, e) in enumerate(zip(axs, exts), 1):
        ax.imshow(e); ax.axis("off"); ax.set_title(f"{i}. {NAMES[i]}", y=-0.13, fontsize=12, color="#444")
    plt.tight_layout(); fig.savefig(os.path.join(OUT, "overview.png"), dpi=90, facecolor="#F4F2EC"); plt.close(fig)
