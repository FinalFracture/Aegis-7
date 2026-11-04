"""Rook: #60 Court Line climbing family (spec §3.11.6 / §3.7.1), V3 style: slate face, tennis-ball holds, amber route tape, gunmetal sub-frame.
kids   : kids' wall panel 1.25 x 5.0 m (Z 15 face, 12 panels), bigger + denser holds, green tape (auto-belay lanes).
boulder: bouldering panel 1.25 x 4.5 m: 3.0 m vertical + 1.5 m faceted overhang (2 facets, 15 deg / 35 deg, top kicked +0.73 m toward +Z),
         kicker struts behind; 300 mm mats are the floor's job.
trim   : 0.25 m bouldering trim with the same profile (19 m wall = 15 panels + trim). Tiles/abuts in X (sheets inset 1 mm per edge).
REUSE: climbing_panel V3 recipe (sit/pts, ball node holds, tape), court-partition SGM posts, Rev C slate. Run: python3 climbing_panel_set.py"""
from modlib import *
import climbing_panel as cp
TF = cp.TF
def T_of(y, z, ang): return trimesh.transformations.translation_matrix((0, y, z)) @ trimesh.transformations.rotation_matrix(np.radians(ang), [1, 0, 0])
def tx(m, T): uv = m.metadata["uv"]; m.apply_transform(T); m.metadata["uv"] = uv; return m

def seg(p, w, L, n, seed, T, r=.045, tape=AM, sp=.26, tag=""):
    tx_ = lambda m: tx(m, T)
    p.add("Face_Sheet", SSL, tx_(box(-w/2 + .001, w/2 - .001, 0, L, -TF, 0)))
    p.add("Sub_Frame", SGM, *[tx_(b) for b in (box(-w/2 + .03, -w/2 + .07, .002, L - .002, -TF - .08, -TF + E), box(w/2 - .07, w/2 - .03, .002, L - .002, -TF - .08, -TF + E),
          box(-w/2 + .07 - E, w/2 - .07 + E, .02, .08, -TF - .06, -TF + E), box(-w/2 + .07 - E, w/2 - .07 + E, L - .08, L - .02, -TF - .06, -TF + E))])
    c = cp.U(trimesh.creation.box(bounds=[[-w/2 + .001, 0, -TF - .08], [w/2 - .001, L, 0]])); c.apply_transform(T); p.add(f"Face{tag}-convcolonly", G, cp.U(c))
    if n:
        cp.W, cp.H = w, L; P = cp.pts(n, seed, m=.14, sp=sp)
        p.add("Holds", BA, *[tx_(cp.sit(node((x, y, 0), r, 0))) for x, y in P])
        p.add("Route_Tape", tape, *[tx_(box(x - .04, x + .04, y - r*3, y - r*3 + .02, .002, .004)) for x, y in P[::3] if y - r*3 > .01])

def build(q):
    p = Part(); w, k = q["w"], q["kind"]
    if k == "kids": seg(p, w, 5.0 - .002, 24, 21, np.eye(4), r=.055, tape=GRN, sp=.24); return p
    nl = 0 if w < .5 else 12
    seg(p, w, 3.0, nl, 31, np.eye(4), tag="0")
    if w < .5: p.add("Route_Tape", AM, box(-.04, .04, 1.5, 1.52, .002, .004))
    y, z = 3.0, 0.0; tops = []
    for i, (dy, ang) in enumerate(((.75, 15), (.75 - .002 - (TF + .08)*np.sin(np.radians(35)), 35))):
        L = dy/np.cos(np.radians(ang)); T = T_of(y, z, ang); seg(p, w, L, 0 if w < .5 else 3, 40 + i, T, tag=str(i + 1)); tops.append(T)
        y, z = y + dy, z + dy*np.tan(np.radians(ang))
    # kicker struts: lower post line (y 2.4) -> back of facet 2 (merged into the sub-frame)
    for sx in ((-1, 1) if w > .5 else ()):
        xp = sx*(w/2 - .05); b = tops[1] @ np.array([xp, .6, -TF - .06, 1])
        p.add("Sub_Frame", SGM, beam((xp, 2.4, -TF - .06), b[:3], .02, .02))
    return p

VAR = [dict(kind="kids", w=1.25, label="Kids' panel 1.25 x 5.0 m: big ball holds, green tape"),
       dict(kind="boulder", w=1.25, label="Boulder panel 1.25 x 4.5 m: 3.0 vertical + 1.5 m faceted overhang"),
       dict(kind="boulder", w=.25, label="Boulder trim 0.25 x 4.5 m, same profile")]
if __name__ == "__main__":
    run("climbing_panel", build, VAR, names=["kids", "boulder", "trim"], suffix="_set", sheet="climbing_panel_set_sheet.png", title="V3 Court Line family: kids / boulder / trim")
