"""Rook: Tennis Tower F3 Glass Box curtain-wall bay (spec §3.5 / §3.11.1 Rev 2.5-2.6). One 4.0 m roof-grid bay x 13.3 m:
heavy fin (600x50) on the grid line, light fin (600x25) at 2.0 m, transoms 150x100 at 3.325/6.65/9.975, 2 x 4 panes 2.0 x 3.325.
width=1.5 gives the Rev 2.5 W/E closure bay (no light fin). Nature/sports theme per Jared. Run: python3 curtain_wall_panel.py"""
from modlib import *
H, FD, TR = 13.3, .6, (3.325, 6.65, 9.975)
SI = .15                                   # r7 (2026-11-11): Sill_Track depth inboard of the glass line; Head_Track keeps -0.65 (pivot / bbox unchanged)

def build(q):
    W = q.get("width", 4.0); p = Part(); x0 = -W/2; hf = (x0 + .035, x0 + .085)  # heavy fin on the grid line
    lt = q.get("light_t", .025); fins = [hf] + ([(x0 + 2 - lt/2, x0 + 2 + lt/2)] if W > 3 else []); jamb = (W/2 - .045, W/2 - .01)
    edges = [e for f in fins for e in f] + [jamb[0]]; bays = list(zip(edges[1::2], edges[2::2]))
    p.add("Sill_Track", G, box(x0, W/2, 0, .15, -SI, .08));   # r7: sill 0.15 m inboard of the glass (was -0.65: swallowed F3 fences / pads)
    p.add("Curtain-colonly", G, box(x0, W/2, 0, H, -.05, .05)); p.add("Head_Track", G, box(x0, W/2, H - .15, H, -FD - .05, .08))
    p.add("End_Jamb", G, box(*jamb, .15 - E, H - .15 + E, -.04, .04))
    for i, (a, b) in enumerate(fins):  # fin profile per variant
        d = FD if i == 0 or not q.get("short_light") else .35
        if q["fin"] == "plate": p.add("Fin_Plates", ST, fin((a+b)/2, .15-E, H-.15+E, d + .03, b-a, z0=.03))
        elif q["fin"] == "leaf": p.add("Fin_Leaf", ST, fin((a+b)/2, .15-E, H-.15+E, .35 + .03, b-a, z0=.03, belly=(d - .35) / .38 + .25))
        elif q["fin"] == "branch":  # trunk tube with Y-forked branches back to the glass line, echoing the tree columns
            c = (a+b)/2; p.add("Fin_Branch", G, fin(c, .15-E, H-.15+E, .16, b-a, z0=.03))
            p.add("Fin_Branch", G, tube((c, .15-E, -.4), (c, H-.15+E, -.4), .06, 8))
            p.add("Fin_Branch", G, box(c - .06, c + .06, 0, .15, -.46, -.34))   # r7 trunk shoe to the deck (the sill no longer runs under the trunk)
            for y in np.arange(1.6, H-.5, 3.325):
                for s in (-1, 1): p.add("Fin_Branch", G, tube((c, y, -.4), (c, y + s*.9, -.13+E), .035, 6))
                p.add("Fin_Branch", G, node((c, y, -.4), .095, 1))
                p.add("Branch_LED", CY, box(c - .008, c + .008, y - .25, y + .25, .03 - E, .042))
    for k, (a, b) in enumerate(bays):  # transoms between fins (embedded E) + glass/spandrel
        for t in TR:
            if q.get("stagger") and k % 2: t += .4 * (1 if t < 8 else -1)
            p.add("Transoms", G, box(a - E, b + E, t - .075, t + .075, -.05, .05))
        ys = [.15] + [t for t in TR] + [H - .15]
        if q.get("stagger") and k % 2: ys = [.15] + [t + .4 * (1 if t < 8 else -1) for t in TR] + [H - .15]
        for r, (y0, y1) in enumerate(zip(ys[:-1], ys[1:])):
            ya, yb = y0 + (.075 if r else 0) - E, y1 - (.075 if r < 3 else 0) + E
            if r == 0 and q.get("spandrel"):
                p.add("Spandrel_Panel", SL, box(a + .002, b - .002, ya, yb, -.03, .03))
                p.add("Green_Wall", LF, green_wall(a + .03, b - .03, ya + .05, yb - .05, .03, r=.13, seed=k*50))
            else: p.add(f"Glass_Pane_{k}{r}", GL, pane(a + .002, b - .002, ya, yb, 0))
    if q.get("planters"):  # interior planter ledges on each transom with trailing vines
        for k, (a, b) in enumerate(bays):
            for j, t in enumerate(TR):
                tr, so, sy = planter(a + .02, b - .02, t + .075 - E, -.42, -.05 + E, h=.26)
                p.add("Planter_Trough", G, tr); p.add("Planter_Soil", SO, so)
                p.add("Foliage", LF if j % 2 else LF2, shrubs(a + .05, b - .05, sy, -.24, r=.15, seed=k*9+j))
                for xv in (a + .3, b - .3):
                    st, lv = vine([(xv, t + .075, -.44), (xv + .05, t - .9, -.47), (xv - .03, t - 1.7, -.46)], seed=j)
                    p.add("Vine_Stems", LF, st); p.add("Vine_Leaves", LF2, lv)
    if q.get("leafcaps"):  # leaf-shaped caps on the fin noses at every transom
        for a, b in fins:
            for t in TR: p.add("Leaf_Caps", LF2, leaf(((a+b)/2, t - .3, .05 + .02 - E), .6, .22, 0, 0, t=.02))
            p.add("Fin_LED", CY, box(a + .007, b - .007, .6, H - .6, .03 - E, .045))
    if q.get("trellis"):  # exterior cable trellis with climbing vine + tennis-ball node caps
        zt = .18
        for (a, b) in fins: p.add("Trellis_Posts", ST, box(a + .007, b - .007, .15 - E, H - .15 + E, .03 - E, zt + .02))
        xs = [(a+b)/2 for a, b in fins] + [sum(jamb)/2]
        for i in range(len(xs) - 1):
            for y in np.arange(.4, H - 2.4, 2.2):
                p.add("Trellis_Cables", ST, tube((xs[i] + .03, y, zt), (xs[i+1] - .03, y + 2.0, zt), .008, 5))
            st, lv = vine([(xs[i] + .2, .15, zt + .03), (xs[i] + .6, 3, zt + .03), (xs[i] + 1.2, 6.5, zt + .03), (xs[i] + .8, 10, zt + .03)], leaf_every=.3, seed=i)
            p.add("Vine_Stems", LF, st); p.add("Vine_Leaves", LF2, lv)
        for a, b in fins:
            for t in TR: p.add("Ball_Caps", BA, node(((a+b)/2, t, zt + .02 + .065 - E), .065, 1))
            pass  # ball seams dropped (clip)
            for t in []: p.add("Ball_Seams", ST, box((a+b)/2 - .07, (a+b)/2 + .07, t - .006, t + .006, zt + .02 + .06, zt + .02 + .14))
    if q.get("louvres"):  # top-row service louvres (greeble) + sports-band LED
        for a, b in bays: p.add("Head_Louvres", G, louvres(a + .01, b - .01, 10.3, 12.9, -.06, 7, d=.1))
        p.add("Court_Line_LED", AM, box(x0 + .1, W/2 - .1, .15 - E, .19, .08 - .03, .081 + .004))
    if q.get("node_caps"):
        for a, b in fins:
            for t in TR: p.add("Node_Caps", G, node(((a+b)/2, t, .05 + .09 - E), .09, 1))
    return p

VARIANTS = [
    dict(label="Planter Ledge: plate fins, planter troughs + trailing vines", fin="plate", planters=True, node_caps=True),
    dict(label="Leaf Blade: fish-belly leaf fins, leaf caps, cyan vein LED", fin="leaf", leafcaps=True),
    dict(label="Branch Fin: Y-forked tree-branch fins, gunmetal nodes, cyan LED", fin="branch"),
    dict(label="Green Spandrel: moss-wall base, staggered transoms, louvres", fin="plate", spandrel=True, stagger=True, louvres=True, short_light=True),
    dict(label="Court Trellis: exterior vine trellis, tennis-ball node caps", fin="plate", trellis=True),
]
if __name__ == "__main__": run("curtain_wall_panel", build, VARIANTS, title="F3 Glass Box 4.0 x 13.3 m bay | nature + sports | +Z exterior, iso")
