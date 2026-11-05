"""Rook: #77 terrace kit final (Jared pick V1 Court Line, sculpted). Pieces: deck 4x4 (bevelled pavers +-3 mm, recessed joints, joint moss,
raised court-line strips, inset tennis-ball medallion with service-box lines, grass tufts), edge (sculpted deck strip, stepped coping with
drip groove, court lines, guard with base plates + ball finials, kick panels with net relief), ramp 1:20 (bevelled sloped pavers, raised court
lines, kerb coping, guard), apron 1:12 (bevelled pavers, grooved anti-slip nosing, court-line edges). Also tt_plinth_skirt_terrace(+half):
the #76 skirt rebuilt to top out at +3.70 under the deck edge. Run: python3 terrace_final.py"""
from modlib import *
import terrace as T
from terrace import huv, DK, SLOPE, APR, PV, place, seam, walk, guard, tufts_at
import plinth_skirt_final as PS
Q = dict(theme="court")
def bpav(a, b, c, d, ybf, ytf, dh, bev=.012):
    return huv([(x, ybf(x, z), z) for x in (a, b) for z in (c, d)] + [(x, ytf(x, z) + dh - .006, z) for x in (a, b) for z in (c, d)] + [(x, ytf(x, z) + dh, z) for x in (a + bev, b - bev) for z in (c + bev, d - bev)])
def paver_field(p, x0, x1, z0, z1, n, m, ybf, ytf, rng, skip=None, tag=""):
    xs = np.linspace(x0, x1, n + 1); zs = np.linspace(z0, z1, m + 1); A, B = [], []; tops = {}; SK = []
    for i in range(n):
        for j in range(m):
            a, b, c, d = xs[i] + .005, xs[i+1] - .005, zs[j] + .005, zs[j+1] - .005
            if skip and skip(a, b, c, d): SK.append((a, b, c, d)); continue
            dh = rng.choice([-.003, 0, .003]); tops[(i, j)] = dh; (A if (i + j) % 2 == 0 else B).append(bpav(a, b, c, d, ybf, ytf, dh))
    p.add(f"Pavers_A{tag}", PV, *A); p.add(f"Pavers_B{tag}", SL, *B); return xs, zs, SK
def joint_green(p, xs, zs, ytf, rng, n=10, tag=""):
    pts = [(xs[i], zs[j]) for i in range(1, len(xs) - 1) for j in range(1, len(zs) - 1)]; rng.shuffle(pts); M, Tf = [], []
    for k, (x, z) in enumerate(pts[:n]):
        if k % 2: M.append(clump((x, ytf(x, z) - .012, z), .021, k))
        else: Tf += tufts_at([(x, z)], ytf(x, z) - .006, rng)
    if M: p.add(f"Joint_Moss{tag}", LF, *M)
    if Tf: p.add(f"Joint_Tufts{tag}", LF2, *Tf)
def deck(p, x0, x1, z0, z1, rng, medal=True, yb=.2, yt=DK):
    ybf = lambda x, z: yb; ytf = lambda x, z: yt; cx, cz = (x0 + x1)/2, (z0 + z1)/2
    skip = (lambda a, b, c, d: np.hypot(np.clip(cx, a, b) - cx, np.clip(cz, c, d) - cz) < .985) if medal else None
    xs, zs, SK = paver_field(p, x0, x1, z0, z1, 8, 8, ybf, ytf, rng, skip=skip)
    L = [box(x0 + .3, x1 - .3, yt - .004, yt + .006, z0 + .25, z0 + .3), box(x0 + .3, x0 + .35, yt - .004, yt + .006, z0 + .3 + .002, z1 - .3)]
    p.add("Court_Strips_White", WH, *L); p.add("Court_Strip_Amber", AM, box(x1 - .35, x1 - .3, yt - .004, yt + .006, z0 + .3 + .002, z1 - .3))
    if medal:   # inset tennis-ball medallion: slate disc, amber ring, felt-yellow ball with white seams, service-box T lines
        def disc(r, y0, y1, seg=24): return tube((cx, y0, cz), (cx, y1, cz), r, seg)
        p.add("Medallion_Surround", G, *[box(a, b, yb + .001, yt - .008, c, d) for a, b, c, d in SK]); p.add("Medallion_Base", SL, disc(.98, yt - .011, yt - .004))
        p.add("Medallion_Ring", AM, *[tube((cx + .9*np.cos(a), yt - .002, cz + .9*np.sin(a)), (cx + .9*np.cos(b), yt - .002, cz + .9*np.sin(b)), .012, 4) for a, b in zip(np.linspace(0, 2*np.pi, 25)[:-1], np.linspace(0, 2*np.pi, 25)[1:])])
        p.add("Medallion_Ball", BA, disc(.42, yt - .006, yt + .004, 20))
        S = []
        for sgn in (-1, 1):
            t = np.linspace(-1.1, 1.1, 9); P = [(cx + sgn*(.42 - .2*np.cos(u)*1.0) * (1 if sgn > 0 else 1) - sgn*.0, yt + .004, cz + .36*np.sin(u)) for u in t]
            P = [(cx + sgn*(.1 + .22*(1 - np.cos(u))) , yt + .004 + .006 - .01, cz + .34*np.sin(u)) for u in t]
            S += [tube(a, b, .012, 4) for a, b in zip(P[:-1], P[1:])]
        p.add("Medallion_Seams", WH, *S)
        p.add("Medallion_Service_Lines", WH, box(cx - .6, cx + .6, yt - .006, yt + .002, cz + .55, cz + .6), box(cx - .025, cx + .025, yt - .006, yt + .002, cz + .6 + .002, cz + .85))
    joint_green(p, xs, zs, ytf, rng, n=12)
def build(q):
    p = Part(); rng = np.random.default_rng(q.get("seed", 5)); pc = q["piece"]; h = 2.0; X0, X1 = -h + .001, h - .001
    if pc == "deck":
        p.add("Deck_Slab", G, box(X0, X1, 0, .2 + .002, X0, X1)); p.add("Deck_Drain", SSL, box(X0 + .1, X1 - .1, .2 - .03, .2 + .004, X0 + .04, X0 + .09))
        deck(p, X0, X1, X0 + .1, X1, rng); p.add("Deck-colonly", SL, box(-2, 2, 0, DK, -2, 2))
    if pc == "edge":
        zc0, zc1 = .25, .9
        p.add("Deck_Slab", G, box(X0, X1, 0, .2 + .002, -1.6, zc0 - .002)); deck(p, X0, X1, -1.6, zc0 - .004, rng, medal=False)
        p.add("Coping_Kerb", SL, box(X0, X1, 0, .36, zc0, zc1 - .06), box(X0, X1, .36 - E, .4, zc0 + .04, zc1 - .14), box(X0, X1, .06, .33, zc1 - .06 - E, zc1))
        p.add("Coping_Line", AM, box(X0, X1, .2, .24, zc1 - E, zc1 + .007)); p.add("Coping_Court_Line", WH, box(X0, X1, .4 - E, .404, zc0 + .07, zc0 + .12))
        guard(p, Q, X0, X1, .62, .4)
        p.add("Guard_Frame", G, *[box(x - .063, x + .063, .4 - E, .42, .557, .683) for x in np.arange(X0 + .5, X1 - .3, 1.0)])
        K = []
        for xa in np.arange(X0 + .5, X1 - .3, 1.0)[:-1]:
            K.append(box(xa + .08, xa + 1.0 - .08, .42 + .002, .58, .645, .665))
        p.add("Kick_Panels", SL, *K)
        p.add("Kick_Net_Relief", WH, *[box(xa + .1, xa + .9, y - .004, y + .004, .665 - E, .672) for xa in np.arange(X0 + .5, X1 - .3, 1.0)[:-1] for y in (.46, .5, .54)])
        p.add("Edge-colonly", SL, box(-2, 2, 0, .36, -1.6, zc1))
    if pc == "ramp":
        yt = lambda x, z=0: DK + .2 - SLOPE*(x - X0)
        p.add("Ramp_Body", G, huv([(x, y, z) for x in (X0, X1) for z in (-2.999, 2.4 - .002) for y in (0, yt(x) - .1 + .002)]))
        xs, zs, _ = paver_field(p, X0, X1, -2.999, 2.4 - .004, 4, 6, lambda x, z: yt(x) - .1, lambda x, z: yt(x), rng)
        p.add("Court_Strips_White", WH, *[huv([(x, yt(x) + o, z) for x in (X0, X1) for z in (z0, z0 + .05) for o in (-.0047, .006)]) for z0 in (-2.7, 2.15)])
        p.add("Court_Strip_Amber", AM, huv([(x, yt(x) + o, z) for x in (X0, X1) for z in (-.025, .025) for o in (-.0047, .006)]))
        joint_green(p, xs, zs, lambda x, z: yt(x), rng, n=8)
        p.add("Ramp_Kerb", SL, huv([(x, y, z) for x in (X0, X1) for z in (2.4, 3.0 - .001) for y in (0, yt(x) + .06)]))
        p.add("Kerb_Coping", G, huv([(x, y, z) for x in (X0, X1) for z in (2.38, 2.5) for y in (yt(x) + .06 - E, yt(x) + .1)]))
        guard(p, Q, X0, X1, 2.75, yt(X0) + .06, slope=SLOPE, xref=X0)
        p.add("Guard_Frame", G, *[huv([(x + dx, yt(x + dx) + .06 + o, z) for dx in (-.063, .063) for z in (2.687, 2.813) for o in (-E, .02)]) for x in np.arange(X0 + .5, X1 - .3, 1.0)])
        p.add("Ramp-colonly", SL, huv([(x, y, z) for x in (-2.0, 2.0) for z in (-3.0, 2.4) for y in (0, yt(x))]))
        p.add("Kerb-colonly", SL, huv([(x, y, z) for x in (-2.0, 2.0) for z in (2.4, 3.0) for y in (0, yt(x) + 1.1)]))
    if pc == "apron":
        Z0, Z1 = -.5, .5; yt = lambda z: .05 + APR*(Z1 - z)
        p.add("Apron_Body", G, huv([(x, y, z) for x in (X0, X1) for z in (Z0, Z1 - .12) for y in (0, yt(z) - .04 + .002)]))
        xs, zs, _ = paver_field(p, X0, X1, Z0 + .12, Z1 - .12, 8, 3, lambda x, z: yt(z) - .04, lambda x, z: yt(z), rng)
        p.add("Back_Court_Line", WH, huv([(x, yt(z) - .038 + o, z) for x in (X0 + .012, X1 - .012) for z in (Z0 + .01, Z0 + .11) for o in (-.0047, .03)]))
        yn = yt(Z1 - .12) + .002
        p.add("Nosing", AM, box(X0 + .003, X1 - .003, 0, yn, Z1 - .118, Z1 + .012))
        p.add("Nosing_Grooves", G, *[box(X0 + .02, X1 - .02, yn - .004, yn + .005, z, z + .012) for z in np.linspace(Z1 - .1, Z1 - .01, 4)])
        p.add("End_Court_Lines", WH, *[huv([(x, yt(z) + o, z) for x in (xa, xa + .05) for z in (Z0 + .125, Z1 - .125) for o in (-.0047, .006)]) for xa in (X0 + .15, X1 - .2)])
        joint_green(p, xs, zs, lambda x, z: yt(z), rng, n=6)
        p.add("Apron-colonly", SL, huv([(x, y, z) for x in (-2.0, 2.0) for z in (Z0, Z1) for y in (0, yt(z))]))
    return p
T.build_orig = T.build
def skirt_terrace(q):   # #76 skirt rebuilt to top out at +3.70 (top course 3.0..3.58 + cap 3.58..3.70)
    h0 = PS.HT; PS.HT = 3.7
    try: return PS.build(q)
    finally: PS.HT = h0
PIECES = ("deck", "edge", "ramp", "apron")
if __name__ == "__main__":
    import facade_bay_final as FB, shutil
    T.build = build
    REP = run("terrace_final", build, [dict(piece=pc, label=pc) for pc in PIECES], title="terrace final", names=[f"tt_terrace_{pc}" for pc in PIECES], sheet="terrace_final_run_sheet.png")
    PS.HT = 3.7
    SREP = run("plinth_skirt_terrace", PS.build, [dict(width=4.0, seed=7, label="terrace"), dict(width=2.0, seed=12, label="terrace half")], title="skirt terrace", names=["tt_plinth_skirt_terrace", "tt_plinth_skirt_terrace_half"], sheet="skirt_terrace_run.png")
    SS = {str(w): PS.seam_check(w)["pass_"] for w in ([4, 4], [4, 2], [2, 4])}; PS.HT = 4.0
    d, e_, r, a = [dict(piece=pc) for pc in PIECES]
    SE = dict(deck_x=seam(d, [(4, 0, 0)])[0], deck_z=seam(d, [(0, 0, 4)])[0], edge_x=seam(e_, [(4, 0, 0)])[0], ramp_chain=seam(r, [(4, -.2, 0)])[0], ramp_mirror=seam(r, [(0, 0, 0)], mirror=-3.0)[0], apron_x=seam(a, [(4, 0, 0)])[0])
    WK = dict(ramp=walk(r), apron=walk(a)); print("SEAM", SE, "SKIRT", SS, "WALK", WK)
    rdir = os.path.join(RENDER_OUT, "terrace_final"); json.dump(dict(rep=REP, srep=SREP, seams=SE, skirt_seams=SS, walk=WK), open(os.path.join(rdir, "report.json"), "w"), indent=1, default=str)
    Ry = lambda el, az: (lambda a, b: np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]]) @ np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]]))(np.radians(az), np.radians(el))
    fig = plt.figure(figsize=(30, 22), facecolor="#F4F2EC"); gs = fig.add_gridspec(2, 5)
    shots = [("deck", (30, 28)), ("deck", (9, 60)), ("edge", (12, 30)), ("ramp", (16, 35)), ("apron", (14, 20))]
    for j, (pc, (el, az)) in enumerate(shots):
        p = recenter(build(dict(piece=pc))); _, geo = export_final(p.P, [f"/tmp/tf_{j}.glb"]); geo = {k: v for k, v in geo.items() if "colonly" not in k}
        im = crop(render_view(geo, Ry(el, az), size=800, shadow=False, glass_alpha=.35)); ax = fig.add_subplot(gs[0, j]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
        rr = REP[PIECES.index(pc)]; ex = f" | walk {'PASS' if WK[pc]['pass'] else 'FAIL'} 1:{WK[pc]['grade_1_in']}" if pc in WK else ""
        ax.set_title(f"tt_terrace_{pc} ({'low raking' if el < 10 else '3/4'})\n{rr['tris']} tris | {'PASS' if rr['passed'] else 'FAIL'}{ex}", fontsize=11)
    A = {}
    for k in range(3):
        x = 2 + 4*k; place(A, FB.build(dict(width=4.0)), (x, 4.0, -9.25), f"F{k}")
        for j in range(2): place(A, build(d), (x, 3.7, -7.0 + 4*j), f"D{k}{j}")
        place(A, build(e_), (x, 3.7, 0), f"E{k}")
    PS.HT = 3.7
    for k in range(3): place(A, PS.build(dict(width=4.0, seed=7)), (2 + 4*k, 0, .5), f"S{k}")
    PS.HT = 4.0
    for k in range(2):
        place(A, build(r), (14 + 4*k, 3.5 - .2*k, -5.0), f"R{k}"); A[f"FILL{k}"] = (SSL, box(12 + 4*k + .001, 16 + 4*k - .001, -.3, 3.5 - .2*k + .002, -8.0, -2.0))
    Pt = Part()
    for n, (mk, m) in A.items():
        if "uv" not in m.metadata: m.metadata["uv"] = np.zeros((len(m.vertices), 2))
        Pt.add(n, mk, m)
    _, g2 = export_final(Pt.P, ["/tmp/tfv.glb"]); im = crop(render_view(g2, Ry(14, 32), size=1500, shadow=False, glass_alpha=.35))
    ax = fig.add_subplot(gs[1, :]); ax.imshow(np.clip(im, 0, 1)); ax.axis("off")
    ax.set_title(f"vignette: tt_facade_bay at +4.0 on tt_terrace_deck, tt_terrace_edge over tt_plinth_skirt_terrace (top +3.70), tt_terrace_ramp x2 | tiling {'PASS' if all(SE.values()) else 'FAIL'} | skirt_terrace seams {'PASS' if all(SS.values()) else 'FAIL'} ({SREP[0]['tris']}/{SREP[1]['tris']} tris)", fontsize=12)
    fig.suptitle("Rook | #77 tt_terrace_* (V1 Court Line, sculpted) + tt_plinth_skirt_terrace(_half) | FINAL", fontsize=16)
    plt.tight_layout(rect=(0, 0, 1, .96)); sp = os.path.join(rdir, "terrace_final_sheet.png"); fig.savefig(sp, dpi=75, facecolor="#F4F2EC"); print("SHEET", sp)
