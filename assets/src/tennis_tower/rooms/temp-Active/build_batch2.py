"""temp-Active batch 2 (scratch, outside repo): rink boards/corner/gate/bench, climbing desk/mats/ring/auto-belay/anchor, gym squat rack/plate tree.
Imports modlib + struct_lib (read-only) for TT palette, TT_GlassScissorActive/PadTeal and finish_scissor (MASK + dither)."""
import os, sys, json
sys.dont_write_bytecode = True
sys.path.insert(0, "/workspace/game-project/assets/src/tennis_tower"); sys.path.insert(0, "/workspace/game-project/assets/src/tennis_tower/structure")
import modlib as ML
from modlib import *
import struct_lib as SLB
from struct_lib import SCR, PAD, finish_scissor
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
ML.GLB_OUT = str(HERE / 'glb')
ML.RENDER_OUT = '/workspace/renders/tennis_tower/rooms/temp-Active'
ML._m("tt_rubber", "TT_PlayRubber_Black", (.07, .075, .08), 0, .9)
RB = "tt_rubber"
def U(m): m.metadata["uv"] = np.zeros((len(m.vertices), 2)); return m
def hull(pts): return U(trimesh.convex.convex_hull(np.asarray(pts, float)))
DS = .128   # metres per scissor texture tile (128 px, 16 mm dot period; mip-friendly)
def puv(m):  # world-planar UV (tile every DS metres) so the fine dither keeps constant scale on every pane
    v = m.vertices; lo, hi = v.min(0), v.max(0); a = 0 if hi[0] - lo[0] >= hi[2] - lo[2] else 2
    m.metadata["uv"] = np.c_[v[:, a] / DS, v[:, 1] / DS]; return m
def frit(x0, x1, y0, y1, w=.025, t=.011):  # opaque ceramic frit frame around a pane (pane edges embed E into it)
    return [box(x0, x1, y0, y0 + w, -t, t), box(x0, x1, y1 - w, y1, -t, t), box(x0, x0 + w, y0 + w, y1 - w, -t, t), box(x1 - w, x1, y0 + w, y1 - w, -t, t)]
def fine_scissor(path):
    """MASK, cutoff 0.5, mip-friendly regular-dot frit, LINEAR + mipmaps, repeat.
    Ceramic frit stays in mesh geometry (frit()); this texture is only the scissor pattern.
    Unique name TT_GlassScissorActive kept. Factor alpha 1.0."""
    import pygltflib as pg, io
    from PIL import Image, ImageDraw, ImageFilter
    g = pg.GLTF2().load(path); blob = bytearray(g.binary_blob()); hit = False
    N, period, radius = 128, 16, 5.2  # 8x8 dots, ~33% fill, slightly antialiased
    for m in g.materials:
        if m.name not in ('TT_GlassScissor', 'TT_GlassScissorActive'): continue
        m.name = 'TT_GlassScissorActive'
        hit = True
        im = Image.new("RGBA", (N, N), (184, 219, 237, 0))
        dots = Image.new("L", (N, N), 0)
        dr = ImageDraw.Draw(dots)
        for i in range(0, N, period):
            for j in range(0, N, period):
                cx, cy = i + period / 2, j + period / 2
                dr.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=255)
        dots = dots.filter(ImageFilter.GaussianBlur(radius=0.8))
        im.putalpha(dots)
        bcf = m.pbrMetallicRoughness.baseColorFactor
        if bcf is not None and len(bcf) >= 4 and bcf[3] < 1.0:
            bcf = list(bcf); bcf[3] = 1.0; m.pbrMetallicRoughness.baseColorFactor = bcf
        b = io.BytesIO(); im.save(b, "PNG"); data = b.getvalue()
        while len(blob) % 4: blob.append(0)
        # 9729=LINEAR, 9987=LINEAR_MIPMAP_LINEAR, 10497=REPEAT
        g.samplers.append(pg.Sampler(magFilter=9729, minFilter=9987, wrapS=10497, wrapT=10497))
        g.bufferViews.append(pg.BufferView(buffer=0, byteOffset=len(blob), byteLength=len(data))); blob.extend(data)
        g.images.append(pg.Image(bufferView=len(g.bufferViews) - 1, mimeType="image/png")); g.textures.append(pg.Texture(source=len(g.images) - 1, sampler=len(g.samplers) - 1))
        m.alphaMode = "MASK"; m.alphaCutoff = .5; m.doubleSided = True; m.pbrMetallicRoughness.baseColorTexture = pg.TextureInfo(index=len(g.textures) - 1)
    if hit:
        while len(blob) % 4: blob.append(0)
        g.buffers[0].byteLength = len(blob); g.set_binary_blob(bytes(blob)); g.save_binary(path)
def col(p, name, lo, hi): p.add(name + "-convcolonly", G, U(trimesh.creation.box(bounds=[lo, hi])))
def leaves(c, n=5, s=.12):
    return [leaf_dir(c, (np.cos(a), 1.0, 0), s, s*.45, t=.006) for a in np.linspace(.5, np.pi - .5, n)]
RY = lambda a: trimesh.transformations.rotation_matrix(a, [0, 1, 0])

BH, CAP, GT = 1.07, 1.12, 2.40
def board_seg(L, m=0.006, stanchion=True, stripe=True, crest=False, rail=True, clamps=True):
    a, b = -L/2 + .001, L/2 - .001; P = {}
    def add(k, mat, *ms): P.setdefault(k, [mat, []])[1].extend(ms)
    add("Board_Shell", WH, box(a, b, .003, BH, -.05, .05))
    add("Kick_Plate", RB, box(a + m, b - m, 0, .25, .05 - E, .068))
    add("Cap_Pad", PAD, box(a + m, b - m, .88, BH - .01, .05 - E, .085))
    if stripe: add("Court_Stripe", BA, box(a + m, b - m, .52, .58, .05 - E, .056))
    add("Cap_Rail", ALY, box(a + .003, b - .003, BH - E, CAP, -.075, .075))
    add("Sill_Frame", G, box(a + m, b - m, 0, .06, -.32, -.05 + E), *[beam((x, .06 - E, -.29), (x, .86, -.075), .05, .05) for x in (a + m + .1, b - m - .1)],
        *[box(x - .05, x + .05, .78, .94, -.09, -.05 + E) for x in (a + m + .1, b - m - .1)])
    x0 = a + (.07 if stanchion else 0) + m
    px0, px1, py0, py1 = x0 + .006, b - m - .004, CAP - E, GT - .02 + E
    add("Pane_Frit", SL, *frit(px0, px1, py0 + .001, py1 - .001))
    add("Pane_Scissor", SCR, puv(box(px0 + .021, px1 - .021, py0 + .022, py1 - .022, -.008, .008)))
    add("Glazing_Frame", ST, box(a + .002, b - .002, GT - .02, GT + .02, -.022, .022))
    if stanchion: add("Glazing_Frame", ST, box(a + .002, a + .07, CAP - E, GT - .02 + E, -.04, .04))
    if clamps: add("Pane_Clamps_Hardware", G, *[box(x0 - .004, x0 + .05, y - .04, y + .04, *((.011 - E, .023) if s > 0 else (-.023, -.011 + E))) for y in (CAP + .27, GT - .33) for s in (-1, 1)])
    if rail:
        add("Spectator_Rail", ALY, tube((a + m + .02, .98, -.17), (b - m - .02, .98, -.17), .022, 8))
        add("Rail_Bracket_Hardware", ST, *[box(x - .02, x + .02, .95, 1.01, -.19, -.05 + E) for x in (a + m + .25, b - m - .25)])
    if crest: add("Leaf_Crest", LF2, *leaves((0, .30, -.05 - .004), n=5, s=.16))
    return P

def emit(p, P, T=None):
    for k, (mat, ms) in P.items():
        p.add(k, mat, *[xf(mm, R=T[0], t=T[1]) if T is not None else mm for mm in ms])

def board(q):
    p = Part(); emit(p, board_seg(q["L"], crest=q.get("crest", False)))
    col(p, "Board", (-q["L"]/2, 0, -.33), (q["L"]/2, GT + .02, .09)); return p

def corner(q):
    p = Part(); R0, n = q["R"], q["n"]; dth = np.pi/2/n; L = 2*R0*np.sin(dth/2) + .02
    for i in range(n):
        ph = (i + .5)*dth; rm = R0*np.cos(dth/2); T = (RY(ph + np.pi), (rm*np.sin(ph), 0, rm*np.cos(ph)))
        emit(p, board_seg(L, m=.03, stanchion=(i % 2 == 0), crest=(i == n//2) and q.get("crest", False), rail=q.get("rail", True), clamps=False), T)
        c = U(trimesh.creation.box(bounds=[(-L/2, 0, -.33), (L/2, GT + .02, .09)])); p.add(f"Corner{i}-convcolonly", G, xf(c, R=T[0], t=T[1]))
    return p

def gate(q):
    p = Part(); a, b = -.999, .999; g0, g1 = -.50, .50
    for (x0, x1) in ((a, g0 - .045), (g1 + .045, b)):
        p.add("Board_Shell", WH, box(x0, x1, .003, BH, -.05, .05)); p.add("Kick_Plate", RB, box(x0 + .01, x1 - .01, 0, .25, .05 - E, .068))
        p.add("Cap_Pad", PAD, box(x0 + .01, x1 - .01, .88, BH - .01, .05 - E, .085)); p.add("Cap_Rail", ALY, box(x0 + .003, x1 - .003, BH - E, CAP, -.075, .075))
        p.add("Court_Stripe", BA, box(x0 + .01, x1 - .01, .52, .58, .05 - E, .056)); p.add("Sill_Frame", G, box(x0 + .01, x1 - .01, 0, .06, -.32, -.05 + E))
    p.add("Gate_Posts", ST, box(a, a + .07, CAP - E, GT - .02 + E, -.04, .04), box(g0 - .045 - E, g0 - .005, 0, GT - .02 + E, -.056, .056), box(g1 + .005, g1 + .045 + E, 0, GT - .02 + E, -.056, .056))
    p.add("Gate_Posts", ST, box(a + .002, b - .002, GT - .02, GT + .02, -.05, .05))
    q0 = (g0 - .045) - 0.332; q1 = g0 - .045
    p.add("Pane_Frit", SL, *frit(q0 + .002, q1 - .002, CAP - E, GT - .016))
    p.add("Pane_Scissor", SCR, puv(box(q0 + .023, q1 - .023, CAP + .017, GT - .037, -.008, .008)))
    q0 = g1 + .045; q1 = (g1 + .045) + 0.404
    p.add("Pane_Frit", SL, *frit(q0 + .002, q1 - .002, CAP - E, GT - .016))
    p.add("Pane_Scissor", SCR, puv(box(q0 + .023, q1 - .023, CAP + .017, GT - .037, -.008, .008)))
    l0, l1 = g0 + .012, g1 - .012
    p.add("Gate_Leaf_Board", WH, box(l0, l1, .015, BH, -.045, .045)); p.add("Gate_Leaf_Kick", RB, box(l0 + .01, l1 - .01, .02, .25, .045 - E, .063))
    p.add("Gate_Leaf_Pad", PAD, box(l0 + .01, l1 - .01, .88, BH - .01, .045 - E, .08)); p.add("Gate_Leaf_Stripe", BA, box(l0 + .01, l1 - .01, .52, .58, .045 - E, .051))
    p.add("Gate_Leaf_Frame", ALY, box(l0, l1, BH - E, CAP, -.06, .06), box(l0, l0 + .04, CAP - E, GT - .05, -.025, .025), box(l1 - .04, l1, CAP - E, GT - .05, -.025, .025), box(l0 + .04 - E, l1 - .04 + E, GT - .09, GT - .05, -.025, .025))
    p.add("Gate_Leaf_Pane_Frit", SL, *frit(l0 + .042, l1 - .042, CAP + .005, GT - .092))
    p.add("Gate_Leaf_Pane_Scissor", SCR, puv(box(l0 + .063, l1 - .063, CAP + .026, GT - .113, -.008, .008)))
    p.add("Gate_Hinge_Hardware", G, *[box(g0 - .02, l0 + .03, y - .05, y + .05, .043, .07) for y in (.18, .9, 1.9)])
    p.add("Gate_Latch_Hardware", AM, box(l1 - .03, g1 + .02, .7, .82, -.075, -.041))
    p.add("Gate_Handle", ALY, tube((l1 - .14, .78, -.045 + E), (l1 - .14, .78, -.11), .015, 8), tube((l1 - .14, .78 - .015, -.11), (l1 - .14, .98, -.11), .015, 8))
    p.add("Gate_Sign_LED", CY, box(-.2, .2, .6, .7, -.045 - .004, -.045 + E))
    col(p, "GateFixedW", (a, 0, -.33), (g0, GT + .02, .09)); col(p, "GateFixedE", (g1, 0, -.33), (b, GT + .02, .09)); col(p, "GateLeaf", (l0, .015, -.06), (l1, GT - .05, .08))
    return p

def pbench(q):
    p = Part(); L = q["L"]; a, b = -L/2, L/2; bk = q.get("back", True)
    if q.get("slim"):  # depth 0.24 m (back z=-0.02, front z=0.22); no bottle shelf (it will not fit)
        xs = np.linspace(a + .1, b - .1, q.get("legs", 3)); fr = []
        for x in xs:
            fr += [box(x - .025, x + .025, .02, .44, -.02, .03), box(x - .025, x + .025, .02, .44, .17, .22),
                   box(x - .025, x + .025, .02, .06, -.02 + E, .22 - E), box(x - .025, x + .025, .44 - E, .47, -.02, .22),
                   box(x - .018, x + .018, .47 - E, .68, -.012, .018)]
        fr += [box(a + .05, b - .05, .40, .44 - E, .08, .12), box(a + .05, b - .05, .64, .68, -.008, .012)]
        p.add("Frame_Weldment", G, *fr)
        p.add("Feet", RB, *[box(x - .05, x + .05, 0, .02 + E, z - .025, z + .025) for x in xs for z in (.005, .195)])
        p.add("Seat_Slats", RB, box(a, b, .47 - E, .52, .035, .115), box(a, b, .47 - E, .52, .135, .22))
        p.add("Back_Pad", PAD, box(a + .02, b - .02, .52, .70, -.02, .03))
        col(p, "Bench", (a, 0, -.02), (b, .70, .22)); return p
    xs = np.linspace(a + .1, b - .1, q.get("legs", 3)); fr = []
    for x in xs: fr += [box(x - .03, x + .03, .02, .44, -.22, -.16), box(x - .03, x + .03, .02, .44, .16, .22), box(x - .03, x + .03, .02, .06, -.16 - E, .16 + E), box(x - .03, x + .03, .44 - E, .47, -.24, .24)]
    fr += [box(a + .05, b - .05, .40, .44 - E, -.03, .03)]
    if bk: fr += [box(x - .025, x + .025, .47 - E, .95, -.27, -.22) for x in xs]
    p.add("Frame_Weldment", G, *fr)
    p.add("Feet", RB, *[box(x - .05, x + .05, 0, .02 + E, z - .04, z + .04) for x in xs for z in (-.19, .19)])
    p.add("Seat_Slats", RB, *[box(a, b, .47 - E, .52, z - .045, z + .045) for z in (-.15, -.05, .05, .15)])
    if bk:
        p.add("Back_Pad", PAD, box(a + .02, b - .02, .70, .92, -.22 - E, -.17))
        p.add("Back_Stripe", BA, box(a + .02, b - .02, .79, .83, -.17 - E, -.166))
    p.add("Bottle_Shelf", ALY, box(a + .2, b - .2, .16, .18, -.15, .12))
    p.add("Shelf_Brackets_Hardware", ST, *[box(x - .02, x + .02, .12, .16 + E, -.14, .11) for x in xs])
    bx = np.arange(a + .35, b - .3, .45)
    p.add("Bottles", BA, *[tube((x, .18 - E, -.08), (x, .38, -.08), .035, 8) for x in bx])
    p.add("Bottle_Caps", CY, *[tube((x, .38 - E, -.08), (x, .41, -.08), .02, 8) for x in bx])
    col(p, "Bench", (a, 0, -.27), (b, .95 if bk else .52, .24)); return p

def desk(q):
    p = Part(); L = q["L"]; a, b = -L/2 + .001, L/2 - .001; H = 1.05; D = .80; rng = np.random.default_rng(q.get("seed", 1)); acc = q.get("acc")
    if acc: body = [box(a, acc[0], .1, H - .04, -D/2, D/2 - .06), box(acc[1], b, .1, H - .04, -D/2, D/2 - .06), box(acc[0] - E, acc[1] + E, .1, .30, -D/2, -D/2 + .25)]
    else: body = [box(a, b, .1, H - .04, -D/2, D/2 - .06)]
    p.add("Desk_Body", G, *body)
    p.add("Plinth_Rubber", RB, box(a + .03, b - .03, 0, .1 + E, -D/2 + .03, D/2 - .09))
    if acc: top = [box(a, acc[0] - .003, H - .04 - E, H, -D/2 - .02, D/2 + .03), box(acc[1] + .003, b, H - .04 - E, H, -D/2 - .02, D/2 + .03), box(acc[0] + E, acc[1] - E, .82, .86, -D/2 - .02, D/2 + .03)]
    else: top = [box(a, b, H - .04 - E, H, -D/2 - .02, D/2 + .03)]
    p.add("Counter_Top", ALY, *top)
    zf = D/2 - .06; st = []
    for x0 in np.arange(a + .02, b - .3, .55):
        x1 = min(x0 + .5 + rng.uniform(-.06, .02), b - .02)
        if acc and x1 > acc[0] - .02 and x0 < acc[1] + .02: continue
        for (y0, y1) in ((.12, .52), (.56, H - .08)):
            dz = rng.uniform(.03, .06); j = rng.uniform(-.03, .03, 4)
            st.append(hull([(x0 + .01, y0, zf - E), (x1 - .01, y0, zf - E), (x0 + .01, y1, zf - E), (x1 - .01, y1, zf - E),
                            (x0 + .06 + j[0], y0 + .05, zf + dz), (x1 - .06 + j[1], y0 + .05 + j[2], zf + dz*.8), (x0 + .07 + j[3], y1 - .05, zf + dz*.9), (x1 - .06, y1 - .06, zf + dz)]))
    p.add("Stone_Fascia", SL, *st)
    p.add("Reveal_LED", CY, box((acc[1] + .03) if acc else a + .02, b - .02, H - .075, H - .05, zf - E, zf + .015))
    p.add("Shoe_Cubbies", ST, box(a + .05, b - .05, .14, .16, -D/2 - .2, -D/2 + E), *[box(a + .05, b - .05, y - .01, y + .01, -D/2 - .2, -D/2 + E) for y in (.45, .75)],
          *[box(x - .01, x + .01, .16 - E, .74, -D/2 - .2, -D/2 + E) for x in np.arange(a + .06, b - .04, .3)], *[box(x - .01, x + .01, .46 - E, .74 + E, -D/2 - .2, -D/2 + E) for x in []])
    p.add("Rental_Shoes", RB, *[box(x + .04, x + .26, y, y + .09, -D/2 - .18, -D/2 - .02) for x in np.arange(a + .07, b - .35, .3) for y in (.16 - E, .46 - E)])
    p.add("Screen", CY, box(-.25, .25, H + .25, H + .55, -.05 - .0, -.045))
    p.add("Screen_Stand", G, box(-.03, .03, H - E, H + .25 + E, -.09, -.05 + E), box(-.26, .26, H + .24, H + .56, -.07, -.05 + E))
    col(p, "Desk", (a, 0, -D/2 - .2), (b, H, D/2 + .03))
    # holds and emblem on the fascia: sit on stones -> place on desk body face between stones instead (gap strip y .52..56)
    p.add("Climbing_Holds", BA, *[clump((x, .54, zf + .022 - E), .026, k) for k, x in enumerate(np.arange(a + .3, b - .2, .55)) if not (acc and acc[0] - .15 < x < acc[1] + .15)])
    return p

MH = .30
def mat(q):
    p = Part(); W, D = q["W"], q["D"]; a, b = -W/2 + .001, W/2 - .001; z0, z1 = -D/2 + .001, D/2 - .001; ch = q.get("chamfer", 0)
    core = [box(a, b, 0, MH - .02, z0, z1 - ch)]
    if ch: core.append(hull([(a, 0, z1 - ch - E), (b, 0, z1 - ch - E), (a, MH - .02, z1 - ch - E), (b, MH - .02, z1 - ch - E), (a, 0, z1), (b, 0, z1), (a, .06, z1), (b, .06, z1)]))
    p.add("Mat_Core", RB, *core)
    p.add("Mat_Cover", PAD, box(a + .002, b - .002, MH - .02 - E, MH, z0 + .002, z1 - ch - .002))
    p.add("Velcro_Seam_Flap", AM if q.get("amber") else SL, box(a + .004, b - .004, MH - E, MH + .004, z0 + .006, z0 + .07))
    p.add("Leaf_Print", LF2, *[leaf((x, MH + .002 - E, z), .22, .1, yaw=y, pitch=-np.pi/2, t=.004) for x, z, y in ((-W*.25, .3, .4), (W*.22, -.35, 2.1))])
    p.add("Ball_Dots", BA, *[box(x - .04, x + .04, MH - E, MH + .003, z - .04, z + .04) for x, z in ((-W*.3, -.5), (W*.3, .55 - ch))])
    col(p, "Mat", (-W/2, 0, -D/2), (W/2, MH, D/2)); return p

def mat_ring_corner(q):
    p = Part(); R = q["R"]; th = np.linspace(0, np.pi/2, q.get("n", 10) + 1)
    pts = lambda y, r: [(0, y, 0)] + [(r*np.cos(t), y, r*np.sin(t)) for t in th]
    p.add("Mat_Core", RB, hull(pts(0, R) + pts(MH - .02, R)))
    pc = lambda y: [(.01, y, .01)] + [(.01 + (R - .025)*np.cos(t), y, .01 + (R - .025)*np.sin(t)) for t in th]
    p.add("Mat_Cover", PAD, hull(pc(MH - .02 - E) + pc(MH)))
    p.add("Ball_Dots", BA, box(R*.3, R*.3 + .08, MH - E, MH + .003, R*.3, R*.3 + .08))
    col(p, "MatCorner", (0, 0, 0), (R, MH, R)); return p

def autobelay(q):
    p = Part()
    p.add("Mount_Plate", ST, box(-.22, .22, .12, .62, 0, .012))
    p.add("Mount_Bolts_Hardware", G, *[tube((x, y, .012 - E), (x, y, .03), .014, 8) for x in (-.18, .18) for y in (.16, .58)])
    p.add("Housing", WH, tube((0, .38, .012 - E), (0, .38, .16), .17, 18))
    p.add("Housing_Cap", G, tube((0, .38, .16 - E), (0, .38, .19), .13, 18))
    p.add("Brand_Ring_LED", CY, tube((0, .38, .19 - E), (0, .38, .196), .06, 14))
    p.add("Guide_Throat", G, box(-.05, .05, .16, .22, .04, .13))
    p.add("Webbing", BA, box(-.022, .022, .12, .16 + E, .082, .088))
    k = [tube((-.03, .12 + E, .085), (.03, .12 + E, .085), .009, 6), tube((-.03, .02, .085), (.03, .02, .085), .009, 6),
         tube((-.03, .12 + E + .009, .085), (-.03, .02 - .009, .085), .009, 6), tube((.03, .12 + E + .009, .085), (.03, .02 - .009, .085), .009, 6)]
    p.add("Carabiner_Hardware", ALY, *k)
    col(p, "AutoBelay", (-.22, .011, 0), (.22, .62, .2)); return p

def anchor(q):
    p = Part()
    p.add("Anchor_Plate", ST, box(-.12, .12, .02, .32, 0, .01))
    p.add("Anchor_Bolts_Hardware", G, *[tube((x, .27, .01 - E), (x, .27, .028), .011, 8) for x in (-.07, .07)])
    p.add("Hangers", ALY, *[box(x - .02, x + .02, .17, .25, .01 - E, .016) for x in (-.07, .07)])
    ch = []
    for s in (-1, 1):
        for i in range(3):
            x = s*(.07 - .014*i); yt = .175 - .042*i; yb = yt - .05; w = .012
            if i % 2 == 0: pts = [(x - w, yt, .022), (x + w, yt, .022), (x + w, yb, .022), (x - w, yb, .022)]
            else: pts = [(x, yt, .022 - w), (x, yt, .022 + w), (x, yb, .022 + w), (x, yb, .022 - w)]
            ch += [tube(pts[k], pts[(k + 1) % 4], .004, 6) for k in range(4)]
    p.add("Chain_Links_Hardware", ST, *ch)
    p.add("Lower_Off_Ring", BA, tube((-.03, .035, .023), (.03, .035, .023), .02, 10))
    col(p, "Anchor", (-.12, .015, 0), (.12, .32, .04)); return p

def squat(q):
    p = Part(); W, Dp, H = 1.22, 1.22, 2.30; u = .0375
    up = [(sx*W/2, sz*Dp/2) for sx in (-1, 1) for sz in (-1, 1)]
    fr = [box(x - u, x + u, .06 - E, H, z - u, z + u) for x, z in up]
    fr += [box(-W/2 - u, W/2 + u, H - E, H + .075, z - u, z + u) for z in (-Dp/2, Dp/2)] + [box(x - u, x + u, H - E, H + .075, -Dp/2 + u - E, Dp/2 - u + E) for x in (-W/2, W/2)]
    fr += [box(x - u, x + u, .012, .06, -Dp/2 - .1, Dp/2 + .1) for x in (-W/2, W/2)] + [box(-W/2 + u - E, W/2 - u + E, .012, .06, -Dp/2 - u, -Dp/2 + u)]
    fr += [box(x - u, x + u, H, H + .23, Dp/2 - u, Dp/2 + .14) for x in (-W/2, W/2)]
    p.add("Rack_Frame", G, *fr)
    p.add("Rubber_Feet", RB, *[box(x - u - .01, x + u + .01, 0, .012 + E, z - .06, z + .06) for x in (-W/2, W/2) for z in (-Dp/2 - .03, Dp/2 + .03)])
    p.add("Hole_Strips_LED", AM, *[box(x + u - E, x + u + .003, .4, 2.1, z - .012, z + .012) for x, z in up if x > 0])
    jh = 1.40; ys = .62
    p.add("J_Hooks_Hardware", ST, *[box(x - u - .008, x + u + .008, jh - .06, jh, Dp/2 + u - E, Dp/2 + u + .09) for x in (-W/2, W/2)])
    p.add("Safety_Arms", ST, *[box(x - u + .006, x + u - .006, ys - .05, ys, -Dp/2 + u - E, Dp/2 - u + E) for x in (-W/2, W/2)])
    p.add("Safety_Pads", RB, *[box(x - u + .01, x + u - .01, ys - E, ys + .012, -Dp/2 + u + .05, Dp/2 - u - .05) for x in (-W/2, W/2)])
    bz = Dp/2 + u + .05; by = jh + .014
    p.add("Barbell", ALY, tube((-.86, by, bz), (.86, by, bz), .014, 10))
    p.add("Barbell_Sleeves_Hardware", ST, *[tube((s*(.86 - E), by, bz), (s*1.1, by, bz), .025, 10) for s in (-1, 1)])
    p.add("Bumper_Plates", RB, *[tube((s*(.89 + .035*i) - .015, by, bz), (s*(.89 + .035*i) + .015, by, bz), r, 18) for s in (-1, 1) for i, r in enumerate((.225, .225, .16))])
    p.add("Pullup_Bar", ALY, tube((-W/2 + u - E, H + .2, Dp/2 + .12), (W/2 - u + E, H + .2, Dp/2 + .12), .016, 8))
    col(p, "Rack", (-W/2 - u, 0, -Dp/2 - .1), (W/2 + u, H + .25, Dp/2 + .14)); return p

def platetree(q):
    p = Part()
    p.add("Base_Frame", G, box(-.35, .35, .012, .05, -.06, .06), box(-.06, .06, .012, .05, -.35, .35), box(-.04, .04, .05 - E, 1.25, -.04, .04))
    p.add("Feet", RB, *[box(x - .05, x + .05, 0, .012 + E, z - .05, z + .05) for x, z in ((-.29, 0), (.29, 0), (0, -.29), (0, .29))])
    pegs, plates = [], []
    for y, r in zip((.32, .62, .92), (.225, .19, .15)):
        for s in (-1, 1):
            pegs.append(tube((s*(.04 - E), y, 0), (s*.26, y, 0), .025, 8))
            plates += [tube((s*(.06 + .04*k), y, 0), (s*(.06 + .04*k + .035), y, 0), r, 18) for k in range(2)]
    p.add("Pegs_Hardware", ST, *pegs); p.add("Bumper_Plates", RB, *plates)
    p.add("Ball_Finial", BA, node((0, 1.25 + .05 - E, 0), .055, 1))
    col(p, "PlateTree", (-.36, 0, -.35), (.36, 1.31, .35)); return p

SETS = {
 "tt_rink_board_1m": (board, [dict(label="Rink board 1.0 m filler: same section as 2 m, own stanchion", L=1.0)]),
 "tt_rink_board_2m": (board, [dict(label="Rink board 2.0 m: 1.07 board, pad cap, 1.3 m scissor glass, spectator rail, leaf crest", L=2.0, crest=True), dict(label="Rink board 2.0 m plain", L=2.0)]),
 "tt_rink_board_corner": (corner, [dict(label="Rink corner 90 deg, R 4.0 m board line, 6 chords", R=4.0, n=6, crest=True)]),
 "tt_rink_board_gate": (gate, [dict(label="Rink gate 2.0 m: 1.0 m leaf board+scissor glass, hinges, latch")]),
 "tt_rink_players_bench": (pbench, [dict(label="Players bench 4.0 m, padded back, bottle shelf", L=4.0), dict(label="Players bench 4.0 m backless", L=4.0, back=False)]),
 "tt_rink_players_bench_slim": (pbench, [dict(label="Slim players bench 4.0 m, depth 0.24 m, >=0.9 m walkway in 1.16 m board-to-pad gap", L=4.0, slim=True)]),
 "tt_climb_rental_desk": (desk, [dict(label="Rental desk 4.5 m module, stone fascia, shoe cubbies", L=4.5), dict(label="Rental desk 4.5 m, accessible 0.86 m bay", L=4.5, acc=(.6, 1.5), seed=3)]),
 "tt_climb_mat_300": (mat, [dict(label="Mat 300 mm 2.0 x 2.0 field tile", W=2.0, D=2.0), dict(label="Mat 300 mm 2.0 x 2.0 edge tile, 0.25 chamfer +Z", W=2.0, D=2.0, chamfer=.25, amber=True)]),
 "tt_climb_mat_ring_corner": (mat_ring_corner, [dict(label="TC-S4 ring corner quarter disc R 2.0 x 0.3", R=2.0)]),
 "tt_climb_mat_ring_side": (mat, [dict(label="TC-S4 ring side 1.24 x 2.0 x 0.3", W=1.24, D=2.0)]),
 "tt_climb_mat_300_2x15": (mat, [dict(label="Mat 300 mm 2.0 x 1.5 cut tile (TC-S4 north infill)", W=2.0, D=1.58)]),
 "tt_climb_mat_300_124x15": (mat, [dict(label="Mat 300 mm 1.24 x 1.58 cut tile (TC-S4 north leftover)", W=1.24, D=1.58)]),
 "tt_climb_mat_300_088x24": (mat, [dict(label="Mat 300 mm 0.88 x 2.42 cut tile (TC-S4 west remnant)", W=0.88, D=2.42)]),
 "tt_climb_mat_300_188x40": (mat, [dict(label="Mat 300 mm 1.88 x 4.0 cut tile (TC-S4 east remnant)", W=1.88, D=4.0)]),
 "tt_climb_mat_300_14x28": (mat, [dict(label="Mat 300 mm 1.4 x 2.8 collar west of TC-S3", W=1.4, D=2.8)]),
 "tt_climb_mat_300_06x16": (mat, [dict(label="Mat 300 mm 0.6 x 1.6 collar south of TC-S3 trunk", W=0.6, D=1.6)]),
 "tt_climb_auto_belay": (autobelay, [dict(label="Auto-belay unit, wall plate, webbing stub, carabiner")]),
 "tt_climb_anchor": (anchor, [dict(label="Top anchor: plate, 2 hangers, chains, lower-off ring")]),
 "tt_gym_squat_rack": (squat, [dict(label="Power rack 1.22 x 1.22 x 2.3, J-hooks, safeties, loaded bar")]),
 "tt_gym_plate_tree": (platetree, [dict(label="Plate tree 3 tiers, 12 bumper plates")]),
}
if __name__ == "__main__":
    for mod in (sys.argv[1:] or list(SETS)):
        b, prm = SETS[mod]; run(mod, b, prm, title="temp-Active batch 2", names=[f"{mod}_v{i+1}" for i in range(len(prm))], post=fine_scissor)
