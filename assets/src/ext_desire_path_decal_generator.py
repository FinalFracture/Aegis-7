"""Rook: #47 desire-path wear decal. 5 candidates -> design/assets/ext_desire_path_decal/ext_desire_path_decal_01..05.glb
Each is a 1.2 x 4.0 m (X x Z) decal segment, tiles along Z, made of 1-3 alpha-BLEND quad layers.
Local pivot bottom-centre (0,0,0), +Z = walking direction. Layer k sits at y = k*0.0015 (>=1.5 mm apart, no coplanar).
Placement: y = paving top 0.05 + 0.003 offset = 0.053 (decal lowest layer 3 mm above paving)."""
import numpy as np, trimesh, json, os
from PIL import Image, ImageDraw, ImageFilter
OUT = "design/assets/ext_desire_path_decal"; W, L = 1.2, 4.0; OFF = 0.003; DY = 0.0015
GUN, SLATE, TI, AMB, CY = (26,30,36), (40,46,56), (150,156,164), (255,149,0), (0,200,230)

def quad(w, l, y, tex, segs=6):
    xs = np.linspace(-w/2, w/2, 2); zs = np.linspace(-l/2, l/2, segs+1)
    V, UV, F = [], [], []
    for z in zs:
        for x in xs: V.append([x, y, z]); UV.append([(x+w/2)/w, (z+l/2)/l])
    for i in range(segs):
        a = i*2; F += [[a, a+2, a+1], [a+1, a+2, a+3]]  # +Y up
    m = trimesh.Trimesh(V, F, process=False)
    mat = trimesh.visual.material.PBRMaterial(baseColorTexture=tex, alphaMode="BLEND", roughnessFactor=.9, metallicFactor=0, doubleSided=False)
    m.visual = trimesh.visual.TextureVisuals(uv=np.array(UV), material=mat); return m

def tex_path(rgb, width, alpha, seed, noise=.5, blur=6, edge="soft", wobble=.08):
    rng = np.random.default_rng(seed); H, Wp = 1024, 320
    ys = np.arange(H); cx = Wp/2 + wobble*Wp*np.sin(ys/H*2*np.pi + seed)  # sin over full period -> tiles
    xx = np.arange(Wp)[None]; d = np.abs(xx - cx[:, None]) / (width*Wp/2)
    a = np.clip(1 - d, 0, 1) if edge == "soft" else (d < 1).astype(float)
    n = rng.random((H//16, Wp//16)); n = np.array(Image.fromarray((n*255).astype(np.uint8)).resize((Wp, H), Image.BICUBIC))/255
    n = np.vstack([n[:H//2], n[:H//2][::-1]])  # mirror -> seamless along Z
    a = a * (1 - noise + noise*n) * alpha
    img = Image.new("RGBA", (Wp, H), rgb + (0,)); arr = np.array(img); arr[..., 3] = (a*255).astype(np.uint8)
    return Image.fromarray(arr).filter(ImageFilter.GaussianBlur(blur/4))

def tex_marks(rgb, alpha, seed, kind):
    H, Wp = 1024, 320; img = Image.new("RGBA", (Wp, H), rgb + (0,)); d = ImageDraw.Draw(img); rng = np.random.default_rng(seed)
    for k in range(10 if kind == "steps" else 40):
        y = (k + .5) * H / (10 if kind == "steps" else 40); x = Wp/2 + (rng.random()-.5)*Wp*.3
        if kind == "steps":
            for s in (-1, 1): d.ellipse([x+s*30-14, y-30+s*25, x+s*30+14, y+30+s*25], fill=rgb+(int(alpha*255),))
        else: d.line([x-60, y, x+60, y+rng.integers(-6, 6)], fill=rgb+(int(alpha*255*rng.uniform(.4, 1)),), width=3)
    return img.filter(ImageFilter.GaussianBlur(3))

CANDS = {
 "01": ("Soft Scuff", "single wide soft-edged gunmetal darkening; quietest read, closest to real polished-wear on composite paving",
        [lambda: tex_path(GUN, .9, .55, 1, noise=.6)]),
 "02": ("Polished Line", "titanium-bright burnish where soles polish the slate: wear reads as shine, not dirt (clean Aegis hab)",
        [lambda: tex_path(SLATE, .9, .35, 2), lambda: tex_path(TI, .35, .45, 3, noise=.7)]),
 "03": ("Footfall Trail", "faint gunmetal base + discrete paired footfall prints; storytells 'people walk here' at gameplay distance",
        [lambda: tex_path(GUN, .7, .3, 4), lambda: tex_marks(GUN, .6, 5, "steps")]),
 "04": ("Scuff Streaks", "base darkening + cross-grain scuff streaks; reads strongest under the low amber pole light",
        [lambda: tex_path(GUN, .8, .45, 6), lambda: tex_marks(TI, .45, 7, "streaks")]),
 "05": ("Worn Tactile", "3 layers: darkening, titanium burnish core, and amber fleck where paving-04 tactile inlay is abraded; ties to promoted paving",
        [lambda: tex_path(GUN, .9, .4, 8), lambda: tex_path(TI, .3, .35, 9), lambda: tex_marks(AMB, .35, 10, "streaks")]),
}

def build(c):
    _, _, layers = CANDS[c]; s = trimesh.Scene()
    for k, f in enumerate(layers): s.add_geometry(quad(W, L, k*DY, f()), geom_name=f"layer{k}")
    return s

def check(s):
    gs = list(s.geometry.values()); ys = sorted(g.vertices[:, 1].mean() for g in gs)
    gaps = np.diff(ys) if len(ys) > 1 else np.array([1.])
    V = np.vstack([g.vertices for g in gs]); lo, hi = V.min(0), V.max(0)
    tris = sum(len(g.faces) for g in gs)
    r = dict(tris=int(tris), min_y=float(lo[1]), cx=round(float((lo[0]+hi[0])/2), 4), cz=round(float((lo[2]+hi[2])/2), 4),
             min_layer_gap_m=round(float(gaps.min()), 4), placed_min_y=0.05+OFF, paving_gap_m=OFF,
             normals_up=bool(all((g.face_normals[:, 1] > .99).all() for g in gs)), uv=all(g.visual.uv is not None for g in gs),
             blend=all(g.visual.material.alphaMode == "BLEND" for g in gs))
    r["pass"] = (tris < 6000 and abs(r["min_y"]) <= .005 and abs(r["cx"]) <= .005 and abs(r["cz"]) <= .005
                 and r["min_layer_gap_m"] > .001 and .002 <= OFF <= .005 and r["normals_up"] and r["uv"] and r["blend"])
    return r

if __name__ == "__main__":
    rep = {}
    for c in CANDS:
        s = build(c); s.export(f"{OUT}/ext_desire_path_decal_{c}.glb"); rep[c] = check(s); print(c, rep[c])
    json.dump(rep, open(f"{OUT}/ext_desire_path_decal_report.json", "w"), indent=1)
    # contact sheet: composite layers over paving slate
    cells = []
    for c, (nm, _, layers) in CANDS.items():
        bg = Image.new("RGBA", (320, 1024), (58, 64, 74, 255))
        for f in layers: bg = Image.alpha_composite(bg, f())
        cell = Image.new("RGB", (340, 1090), (12, 14, 18)); cell.paste(bg.convert("RGB"), (10, 10))
        ImageDraw.Draw(cell).text((12, 1046), f"{c} {nm}  {rep[c]['tris']} tris  {'PASS' if rep[c]['pass'] else 'FAIL'}", fill=(255, 149, 0))
        cells.append(cell)
    sheet = Image.new("RGB", (340*5, 1090)); [sheet.paste(im, (i*340, 0)) for i, im in enumerate(cells)]
    sheet.save(f"{OUT}/ext_desire_path_decal_contact_sheet.png")
