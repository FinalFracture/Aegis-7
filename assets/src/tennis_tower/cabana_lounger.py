"""Rook: cabana #V2 Leaf Crest lounger + side table rebuild (Jared: "needs some texture solution, the benches are not great").
Slatted lounger: slat frame (side rails, 13 seat slats, 8 backrest slats at 35 deg recline, back struts, tapered legs), tufted pillow
cushions (rounded-edge lofts, 3 seat + 2 back pillows, recessed-look buttons), slatted side table with a lower shelf.
UVs: world-scale box projection (fabric 0.6 m tile, slats 0.5 m along the grain, cushions 0.4 m); slate upholstery option maps into the
starting-area atlas region UV_FABRIC_SLATE (residential_atrium_and_apartment_atlas, u .27-.48 v .30-.48).
Cushion / canvas variation: COLOR_0 vertex colours (low-frequency +-6 % tone, darker tuft seams) written into the GLB (Godot multiplies albedo).
No wood: docs/FIRST_PASS_CHECKLIST + tools/first_pass_check.py forbid wood albedo/material names (Jared-confirmed art direction), so the
"slat" options are powder-coat alloy / brushed alloy / sand mineral composite. Run: python3 cabana_lounger.py"""
from modlib import *
import modlib, cabana
_m = modlib._m
import pygltflib as pg
_m("tt_canvas", "TT_CabanaCanvas_White", (.88, .87, .84), 0, .85)
_m("tt_slat_leaf", "TT_Slat_LeafPowderCoat", (.24, .42, .27), .3, .55)
_m("tt_slat_sand", "TT_Slat_SandComposite", (.66, .58, .47), 0, .7)
_m("tt_cush_leaf", "TT_Cushion_LeafWeave", (.33, .55, .34), 0, .9)
_m("tt_cush_cream", "TT_Cushion_CanvasCream", (.86, .83, .76), 0, .9)
_m("tt_cush_slate", "TT_Upholstery_FabricSlate", (.80, .85, .80), 0, .9)   # tint x atlas slate fabric
_m("tt_button", "TT_Cushion_Button", (.20, .30, .22), 0, .6)
modlib.TEXMAP.update({"TT_Upholstery_FabricSlate": "residential_atrium_and_apartment_atlas_albedo.png"})
CUSH, CANVAS = ("TT_Cushion_LeafWeave", "TT_Cushion_CanvasCream", "TT_Upholstery_FabricSlate"), ("TT_CabanaCanvas_White",)
ATLAS = {"tt_cush_slate": (.27, .48, .30, .48)}
REC = np.radians(35)

def boxuv(m, tile):  # world-scale box projection
    n = m.vertex_normals; v = m.vertices; a = np.abs(n).argmax(1)
    uv = np.where(a[:, None] == 0, v[:, [2, 1]], np.where(a[:, None] == 1, v[:, [0, 2]], v[:, [0, 1]])) / tile
    m.metadata["uv"] = uv; return m
def atlasuv(m, r):
    m = boxuv(m, 1.0); uv = m.metadata["uv"]; lo, hi = uv.min(0), uv.max(0); t = (uv - lo) / np.maximum(hi - lo, 1e-6)
    m.metadata["uv"] = np.c_[r[0] + t[:, 0]*(r[1] - r[0]), r[2] + t[:, 1]*(r[3] - r[2])]; return m
def T(m, M): uv = m.metadata["uv"]; m.apply_transform(M); m.metadata["uv"] = uv; return m
def fit(m, lo): m.apply_translation(np.asarray(lo, float) - m.bounds[0]); return m
def pillow(w, t, L, r=.03):  # rounded-edge cushion along +Y: width w (X), thickness t (Z), length L, softened ends
    return loft(rrect(w, t, min(r, t/2 - .002), 3), [(0, .95, .55), (.02, .99, .9), (.045, 1, 1), (L - .045, 1, 1), (L - .02, .99, .9), (L, .95, .55)])

def lounger(p, x, q, y0=0.0):
    sm, cm = q["slat"], q["cush"]; F = []; seat_y = .29
    for sx in (-1, 1):   # side rails + tapered legs
        F.append(box(x + sx*.31, x + sx*.35, .22, .30, -.62, 1.0) if sx > 0 else box(x - .35, x - .31, .22, .30, -.62, 1.0))
        for z in (-.55, .92): F.append(prism([(x + sx*.33 - .025, z - .025), (x + sx*.33 + .025, z - .025), (x + sx*.33 + .025, z + .025), (x + sx*.33 - .025, z + .025)], y0, .22 + E, rings=[(y0, .75, .75), (.22 + E, 1, 1)]))
    F += [box(x - .31 - E, x + .31 + E, .27, seat_y, z, z + .07) for z in np.arange(-.34, .99, .1)]          # seat slats
    H = trimesh.transformations.translation_matrix((0, .26, -.36)) @ trimesh.transformations.rotation_matrix(-REC, [1, 0, 0])
    for sx in (-1, 1):   # backrest rails (hinged at the seat rail) + slats, and struts to the seat rails
        F.append(T(box(x + sx*.33 - .02, x + sx*.33 + .02, 0, .82, -.05, 0), H))
        top = H @ np.array([x + sx*.33, .55, -.05, 1]); F.append(beam((x + sx*.33, .24, -.6), top[:3] + np.array([0, -.01, .01]), .03, .03))
    F += [T(box(x - .31 - E, x + .31 + E, y, y + .07, -.025, -.005), H) for y in np.arange(.08, .8, .09)]
    p.add("Lounger_Slat_Frame", sm, *[boxuv(m, .5) for m in F])
    lay = trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0])
    C, B = [], []
    for z0, z1 in ((-.33, .1), (.1, .54), (.54, .98)):          # 3 seat pillows on the slats
        m = fit(T(pillow(.6, .09, z1 - z0 - .004), lay), (x - .3, seat_y - E, z0 + .002)); C.append(m)
        B += [cap((x + bx, seat_y - E + .09 + .002, (z0 + z1)/2), .018, .012, 8, axis="y") for bx in (-.15, .15)]
    for y0b, y1b in ((.12, .46), (.46, .8)):                    # 2 back pillows on the backrest slats
        m = T(fit(pillow(.6, .08, y1b - y0b - .004), (x - .3, y0b + .002, -.005 - E)), H); C.append(m)
        for bx in (-.15, .15): B.append(T(cap((x + bx, (y0b + y1b)/2, -.005 - E + .08 + .002), .018, .012, 8, axis="z"), H))
    p.add("Cushions", cm, *[atlasuv(m, ATLAS[cm]) if cm in ATLAS else boxuv(m, .4) for m in C]); p.add("Cushion_Buttons", "tt_button", *B)

def table(p, x, z, q, y0=0.0):
    sm = q["slat"]; F = [box(x - .24, x + .24, .47, .49, z + k*.1 - .04, z + k*.1 + .04) for k in range(-2, 3)]
    F += [box(x - .22, x + .22, .44, .47 + E, z + s*.17 - .02, z + s*.17 + .02) for s in (-1, 1)]
    F += [box(x - .2, x + .2, .14, .16, z + k*.1 - .035, z + k*.1 + .035) for k in (-1, 0, 1)]
    F += [box(x + sx*.2 - .02, x + sx*.2 + .02, y0, .44 + E, z + sz*.2 - .02, z + sz*.2 + .02) for sx in (-1, 1) for sz in (-1, 1)]
    F[-4:] = [box(x + sx*.2 - .02 + (.005 if sx < 0 else -.005), x + sx*.2 + .02 + (.005 if sx < 0 else -.005), y0, .44 + E, z + sz*.2 - .02, z + sz*.2 + .02) for sx in (-1, 1) for sz in (-1, 1)]
    F += [box(x - .2 + .02 - E, x + .2 - .02 + E, .12, .14 + E, z + s*.2 - .015, z + s*.2 + .015) for s in (-1, 1)]
    p.add("Table_Slat_Frame", sm, *[boxuv(m, .5) for m in F])

def closeup(q):
    p = Part(); lounger(p, 0, q); table(p, .62, .55, q); return p

def full(q):
    p = cabana.build(dict(cabana.VARIANTS[1], fabric="tt_canvas"))
    for k in [k for k in p.P if k.startswith(("Lounger_Frame", "Cushions", "Side_Table"))]: del p.P[k]
    for k in ("Fabric_Roof", "Fabric_Back_Drop", "Fabric_Rolls"): boxuv(p.P[k][1], .6)
    for sx in (-1, 1): lounger(p, sx*.8, q)
    table(p, 0, -.35, q)
    del p.P["Cabana-convcolonly"]; U = lambda m: (m.metadata.__setitem__("uv", np.zeros((len(m.vertices), 2))), m)[1]
    hulls = [trimesh.creation.box(bounds=[[sx*cabana.PC - cabana.PW, 0, sz*cabana.PC - cabana.PW], [sx*cabana.PC + cabana.PW, cabana.EAVE, sz*cabana.PC + cabana.PW]]) for sx in (-1, 1) for sz in (-1, 1)]
    for sx in (-1, 1):
        x = sx*.8; hulls.append(trimesh.creation.box(bounds=[[x - .35, 0, -.62], [x + .35, .38, 1.0]]))
        hulls.append(trimesh.convex.convex_hull(np.vstack([p.P["Lounger_Slat_Frame"][1].vertices[(np.abs(p.P["Lounger_Slat_Frame"][1].vertices[:, 0] - x) < .4) & (p.P["Lounger_Slat_Frame"][1].vertices[:, 2] < -.3) & (p.P["Lounger_Slat_Frame"][1].vertices[:, 1] > .25)]])))
    hulls.append(trimesh.creation.box(bounds=[[-.24, 0, -.6], [.24, .49, -.1]]))
    p.add("Cabana-convcolonly", G, *[U(h) for h in hulls]); return p

def vcolor(path):  # COLOR_0 tone variation on cushions + canvas (multiplies albedo in Godot/glTF)
    g = pg.GLTF2().load(path); blob = bytearray(g.binary_blob())
    for mesh in g.meshes:
        for pr in mesh.primitives:
            nm = g.materials[pr.material].name
            if nm not in CUSH + CANVAS: continue
            a = g.accessors[pr.attributes.POSITION]; bv = g.bufferViews[a.bufferView]
            P = np.frombuffer(bytes(blob[bv.byteOffset + (a.byteOffset or 0): bv.byteOffset + (a.byteOffset or 0) + a.count*12]), np.float32).reshape(-1, 3)
            amp = .06 if nm in CUSH else .04
            t = 1 - amp*(.5 + .5*np.sin(P[:, 0]*9.1 + P[:, 2]*5.3) * np.cos(P[:, 1]*7.7 - P[:, 2]*3.1))
            if nm in CUSH: t *= 1 - .08*np.exp(-((np.mod(P[:, 2] + .33, .44) - .22)**2)/.002)   # darker tuft seams between pillows
            col = np.c_[t, t*.995, t*.985, np.ones(len(t))].astype(np.float32); data = col.tobytes()
            while len(blob) % 4: blob.append(0)
            g.bufferViews.append(pg.BufferView(buffer=0, byteOffset=len(blob), byteLength=len(data), target=34962)); blob.extend(data)
            g.accessors.append(pg.Accessor(bufferView=len(g.bufferViews) - 1, componentType=5126, count=len(t), type="VEC4")); pr.attributes.COLOR_0 = len(g.accessors) - 1
    while len(blob) % 4: blob.append(0)
    g.buffers[0].byteLength = len(blob); g.set_binary_blob(bytes(blob)); g.save_binary(path)

OPTS = [dict(label="L1 Leaf Slat: leaf powder-coat slats, cream canvas tufted cushions", slat="tt_slat_leaf", cush="tt_cush_cream"),
        dict(label="L2 Sand Composite: sand mineral-composite slats, leaf-weave tufted cushions", slat="tt_slat_sand", cush="tt_cush_leaf"),
        dict(label="L3 Alloy + Slate: brushed alloy slats, slate upholstery (starting-area atlas)", slat=ALY, cush="tt_cush_slate")]
if __name__ == "__main__":
    cv = trimesh.transformations.rotation_matrix(0, [0, 1, 0])[:3, :3]
    run("cabana", closeup, OPTS, names=["lounger_L1", "lounger_L2", "lounger_L3"], suffix="_lounger", sheet="cabana_lounger_closeups.png", title="V2 lounger + side table close-ups", post=vcolor)
    run("cabana", full, OPTS, names=["v2_L1", "v2_L2", "v2_L3"], suffix="_v2full", sheet="cabana_v2_full_sheet.png", title="V2 Leaf Crest full cabana with the new loungers", post=vcolor)
