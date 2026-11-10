"""Rook: Tennis Tower stair-core foyer cladding (r3). tt_core_clad_aqn dresses the bare foyer-side S face of ST-AQN
(tt_stair_core_b_m, X -6..0, wall plane Z 58.40) on F1. Wall-mounted, back -Z on the wall, relief <= 0.08 m (<= 0.04 m below +0.3 so the
floor strip Z 57.0..58.35 stays open), top +5.65 under the +5.7 F2 soffit. Two zones around the portal (world X -5.52..-3.38, kept 0.08 m clear):
A = X -3.30..-0.17 (stops 0.02 m short of the X 0 foyer wall), B = X -5.98..-5.60.
Language: layered slate panels with reveals, a brushed-steel tree-column branch relief (TC V4 echo) in two leaf layers, a tennis-court line
inlay, tennis-ball nodes, and Court Wayfinding (stair core V5): amber level disc + arrow chevrons to the portal, stair glyph, aquarium fish
glyph with a chevron toward the corridor. No wood, no planters. Placement (assemble_preview): [-3.075, 0, Z], yaw 180, Z printed by the run.
Run: python3 core_clad.py"""
from modlib import *
H, TOP = 5.65, 5.65
A0, A1, B0, B1 = -2.905, .225, 2.525, 2.905       # local x (yaw 180: world X = -3.075 - x)
FX, FY = -1.45, 1.15                                # aquarium fish glyph centre
ZB, ZP = 0.0, .02                                   # back plane, panel front

def zbox(x0, x1, y0, y1, z0, z1): return box(x0, x1, y0, y1, z0, z1)
def strip(a, b, w, z0, z1):  # flat bar in the wall plane from a to b (x, y), width w
    a, b = np.asarray(a, float), np.asarray(b, float); d = b - a; L = np.linalg.norm(d); ang = np.arctan2(d[1], d[0])
    m = box(0, L, -w/2, w/2, z0, z1); return xf(m, R=trimesh.transformations.rotation_matrix(ang, [0, 0, 1]), t=(a[0], a[1], 0))
def leaf_flat(c, ang, L, W, t=.012):  # leaf lying in the wall plane, long axis at angle ang from +X
    return leaf_dir(c, (np.cos(ang), np.sin(ang), 0), L, W, t=t)

def build():
    p = Part(); rng = np.random.default_rng(7)
    # 1 layered slate panels with 10 mm reveals (zone A 3 x 3, zone B 1 x 3) + gunmetal kick (<= 0.03 relief)
    pan = []
    for x0, x1, nx in ((A0, A1, 3), (B0, B1, 1)):
        xs = np.linspace(x0, x1, nx + 1); ys = np.linspace(.3, TOP, 4)
        for i in range(nx):
            for j in range(3): pan.append(zbox(xs[i] + (.005 if i else 0), xs[i+1] - (.005 if i < nx - 1 else 0), ys[j] + (.005 if j else 0), ys[j+1] - (.005 if j < 2 else 0), ZB, ZP))
    p.add("Clad_Panels", SL, *pan)
    p.add("Reveal_Backer", SGM, zbox(A0, A1, .3, TOP, ZB, ZP - .008), zbox(B0, B1, .3, TOP, ZB, ZP - .008)) if False else None
    p.add("Kick_Plate", G, zbox(A0, A1, 0, .3 + E, ZB, .03), zbox(B0, B1, 0, .3 + E, ZB, .03))
    # 2 tennis-court line inlay (alloy, 0.05 lines, z 0.020..0.026) in the upper panels
    cx, cy, cw, ch = -1.35, 4.27, 2.6, 1.9; zl = (ZP - .002, ZP + .006)
    lines = [zbox(cx - cw/2, cx + cw/2, cy - ch/2, cy - ch/2 + .05, *zl), zbox(cx - cw/2, cx + cw/2, cy + ch/2 - .05, cy + ch/2, *zl),
             zbox(cx - cw/2, cx - cw/2 + .05, cy - ch/2 + .05 - E, cy + ch/2 - .05 + E, *zl), zbox(cx + cw/2 - .05, cx + cw/2, cy - ch/2 + .05 - E, cy + ch/2 - .05 + E, *zl),
             zbox(cx - .025, cx + .025, cy - ch/2 + .05 - E, cy + ch/2 - .05 + E, *zl)]   # baseline-to-baseline net line
    for s in (-1, 1): lines.append(zbox(cx + s*.7 - .025, cx + s*.7 + .025, cy - ch/2 + .05 - E, cy + ch/2 - .05 + E, *zl))   # service lines
    lines.append(zbox(cx - .7 + .025 - E, cx + .7 - .025 + E, cy - .025, cy + .025, *zl))   # centre service line
    p.add("Court_Line_Inlay", ALY, *lines)
    # 3 tree-branch relief (brushed steel CHS 50, touching the panels): trunk at x -2.2 forking up and across zone A
    r = .025; zc = ZP + r - E
    T = lambda a, b: tube((a[0], a[1], zc), (b[0], b[1], zc), r, 8)
    br = [((-2.2, .35), (-2.2, 2.2)), ((-2.2, 2.2), (-2.75, 3.6)), ((-2.2, 2.2), (-1.3, 3.1)), ((-1.3, 3.1), (-.2, 3.5)), ((-1.3, 3.1), (-1.0, 4.9)),
          ((-2.75, 3.6), (-2.6, 5.25)), ((-.2, 3.5), (.05, 5.15)), ((-1.0, 4.9), (-.45, 5.3))]
    p.add("Branch_Relief", ST, *[T(a, b) for a, b in br], *[node((b[0], b[1], zc), .035, 0) for a, b in br])
    # 4 two leaf layers along the branches (dark centre z .044, light .066; flat, 24 mm), rejection-sampled against the keep-outs
    lv, lv2 = [], []
    segs = [(np.array(a), np.array(b), r + .008) for a, b in br] + [(np.array(b), np.array(b), .035 + .008) for a, b in br] + [(np.array(b) + (0, .09), np.array(b) + (0, .09), .028 + .008) for a, b in br[5:]]
    segs += [(np.array((2.715, .35)), np.array((2.715, 5.5)), .012 + .008)]
    rects = [(-.55 - .33, -.55 + .33, 1.65 - .33, 1.65 + .33), (-.21, .21, 1.41, 1.89), (-.96, -.12, 2.14, 2.88), (FX - .69, FX + .47, FY - .46, FY + .27)]
    def ok(m, A=(A0, A1)):   # in-plane keep-outs: branch tubes / nodes / balls / vine stem / wayfinding plates, zone edges, soffit
        v = m.vertices[:, :2]
        if v[:, 1].min() < .36 or v[:, 1].max() > TOP - .06: return False
        if not ((v[:, 0].min() > A0 + .02 and v[:, 0].max() < A1 - .02) or (v[:, 0].min() > B0 + .02 and v[:, 0].max() < B1 - .02)): return False
        for p0, p1, rr in segs:
            d = p1 - p0; L2 = float(d @ d); t = np.clip(((v - p0) @ d) / L2, 0, 1) if L2 > 0 else np.zeros(len(v))
            if (np.linalg.norm(v - (p0 + t[:, None]*d), axis=1) < rr).any(): return False
        for x0, x1, y0, y1 in rects:
            if ((v[:, 0] > x0) & (v[:, 0] < x1) & (v[:, 1] > y0) & (v[:, 1] < y1)).any(): return False
        return True
    for a, b in br[1:]:
        a, b = np.array(a), np.array(b)
        for t in np.linspace(.12, 1.0, 7):
            q = a + (b - a)*t; base = np.arctan2(*(b - a)[::-1])
            for s in (-1, 1, -1, 1):
                ang = base + s*rng.uniform(.5, 1.3); L = rng.uniform(.22, .4)
                o = q + (r + .015)*np.array([np.cos(ang), np.sin(ang)])   # leaf base just outside the branch tube
                m = leaf_flat((o[0], o[1], ZP + (.024 if s < 0 else .046)), ang, L, L*.45)
                if ok(m): (lv if s < 0 else lv2).append(m)
    for y in np.arange(.5, 5.4, .32):   # zone B vine of alternating leaves on a steel stem
        for m, dst in ((leaf_flat((2.74, y, ZP + .024), np.pi/2 - .9, .2, .09), lv), (leaf_flat((2.69, y + .16, ZP + .046), np.pi/2 + .9, .2, .09), lv2)):
            if ok(m): dst.append(m)
    p.add("Leaf_Layer_Dark", LF, *lv); p.add("Leaf_Layer_Light", LF2, *lv2)
    p.add("Vine_Stem", ST, tube((2.715, .35, ZP + .012 - E), (2.715, 5.5, ZP + .012 - E), .012, 6))
    # 5 tennis-ball nodes at the branch tips (r 0.028, front <= 0.072)
    p.add("Ball_Nodes", BA, *[node((b[0], b[1] + .09, ZP + .028 - E), .028, 0) for a, b in br[5:]])
    # 6 Court Wayfinding (amber LED on slate backplates, z <= 0.036): level disc + 3 chevrons -> portal, stair glyph, fish glyph + chevron
    bp_, am = [], []
    z0, z1 = ZP - E, ZP + .01; za = (z1 - E, z1 + .006)
    bp_.append(cap((-.55, 1.65, (z0 + z1)/2), .32, z1 - z0, 24))                       # level disc backplate
    am.append(xf(ring_band(.001, 0, h=1, n=24, t=.001), t=(0, -100, 0))) if False else None
    ring = []
    for k in range(24):
        a0, a1 = 2*np.pi*k/24, 2*np.pi*(k+1)/24
        ring.append(strip((-.55 + .27*np.cos(a0), 1.65 + .27*np.sin(a0)), (-.55 + .27*np.cos(a1), 1.65 + .27*np.sin(a1)), .035, *za))
    am += ring
    am += [strip((-.67, 1.65), (-.43, 1.65), .05, *za), strip((-.55, 1.53), (-.55, 1.77), .05, *za)] if False else []
    am += [strip((-.69, yb), (-.55, yb + .14), .045, *za) for yb in (1.5, 1.64)] + [strip((-.55, yb + .14), (-.41, yb), .045, *za) for yb in (1.5, 1.64)]   # double up-chevron (stairs up)
    for k in range(3):   # chevrons pointing +x (to the portal)
        x = -.12 + .14*k; am += [strip((x, 1.8), (x + .1, 1.65), .04, *za), strip((x + .1, 1.65), (x, 1.5), .04, *za)]
    bp_.append(zbox(-.2, .2, 1.42, 1.88, z0, z1))
    # stair glyph (5 steps) above the disc
    sx, sy = -.85, 2.25; st_ = []
    for k in range(5): st_ += [strip((sx + .12*k, sy + .1*k), (sx + .12*k, sy + .1*(k+1)), .035, *za), strip((sx + .12*k - .0175, sy + .1*(k+1)), (sx + .12*(k+1) + .0175, sy + .1*(k+1)), .035, *za)]
    am += st_; bp_.append(zbox(sx - .1, sx + .72, sy - .1, sy + .62, z0, z1))
    # aquarium fish glyph + chevron toward the corridor (-x local = east)
    fx, fy = FX, FY
    fish = [strip((fx - .25, fy), (fx, fy + .15), .035, *za), strip((fx, fy + .15), (fx + .2, fy), .035, *za), strip((fx + .2, fy), (fx, fy - .15), .035, *za), strip((fx, fy - .15), (fx - .25, fy), .035, *za),
            strip((fx + .2, fy), (fx + .35, fy + .12), .035, *za), strip((fx + .35, fy + .12), (fx + .35, fy - .12), .035, *za), strip((fx + .35, fy - .12), (fx + .2, fy), .035, *za)]
    wave = [strip((fx - .3 + .15*k, fy - .32 + (.04 if k % 2 else 0)), (fx - .15 + .15*k, fy - .32 + (0 if k % 2 else .04)), .03, *za) for k in range(5)]
    chev = [strip((fx - .45, fy + .12), (fx - .57, fy), .04, *za), strip((fx - .57, fy), (fx - .45, fy - .12), .04, *za)]
    am += fish + wave + chev; bp_.append(zbox(fx - .68, fx + .46, fy - .45, fy + .26, z0, z1))
    p.add("Wayfinding_Backplate", SGM, *bp_)
    p.add("Wayfinding_Amber", AM, *am)
    # collider: thin wall-mounted slab per zone (relief envelope, open floor stays clear)
    col = trimesh.util.concatenate([trimesh.creation.box(bounds=[[A0, 0, ZB], [A1, TOP, ZP]]), trimesh.creation.box(bounds=[[B0, 0, ZB], [B1, TOP, ZP]])])
    col.metadata["uv"] = np.zeros((len(col.vertices), 2)); p.P["Clad-colonly"] = (G, col)
    return p

if __name__ == "__main__":
    p = build(); V = np.vstack([m.vertices for k, (_, m) in p.P.items() if "colonly" not in k]); lo0, hi0 = V.min(0), V.max(0)
    p = recenter(p); gp = os.path.join(ROOT, "godot/assets/models", "tt_core_clad_aqn.glb"); tris, geo = export_final(p.P, [gp]); finish_glb(gp)
    chk = cc.check({k: v for k, v in p.P.items() if "colonly" not in k}, n_samp=400)
    try: ok_v = vm.validate_file(gp, check_tri_range=(1, TRI_MAX), require_textures=False, require_blend_glass=False)
    except AssertionError as e: print("VALIDATE FAIL", e); ok_v = False
    V = np.vstack([m.vertices for k, (_, m) in p.P.items() if "colonly" not in k]); lo, hi = V.min(0), V.max(0)
    low = np.vstack([m.vertices for k, (_, m) in p.P.items() if "colonly" not in k]); low = low[low[:, 1] < .3]
    zp = 58.398 + lo[2]   # yaw 180: back face (local min z) 2 mm off the wall plane Z 58.40
    print(json.dumps(dict(glb="tt_core_clad_aqn.glb", tris=int(tris), clip_pass=bool(chk["pass"]), worst_overlap=chk["worst_overlap"], bad=[o for o in chk["overlap"] if not o[3]],
                          coplanar=chk["coplanar"], open=chk["open"][:6], n_open=len(chk["open"]), pivot=chk["pivot"], validate=bool(ok_v), bbox=[lo.round(4).tolist(), hi.round(4).tolist()],
                          relief=round(float(hi[2] - lo[2]), 4), relief_below_0p3=round(float(low[:, 2].max() - lo[2]), 4), x_shift=round(float(-(lo0[0] + hi0[0])/2), 4), place_z=round(float(zp), 4)), default=str))
    im = crop(render_view({k: v for k, v in geo.items() if "colonly" not in k}, [0, 1.2, 9], size=900, shadow=True)) if False else None
