"""Rook: Tennis Tower Glass Box space-frame roof tile (spec §3.11.2 Rev 2.5/2.6, §3.11.10). 5x5 bays on the 4.0 m grid = 20x20 m,
square-on-square, 3.0 m deep c/c: top + bottom chords CHS 219, diagonals CHS 168, ball nodes Ø350; roof panes 2.0x4.0 m with a glazing bar.
Flat (2% fall is a design note; the faceted ridge is a separate crown piece, not in this tile). Tile owns the nodes on its -X/-Z edges;
boundary chords stop 1 mm short so tiles abut at 20.0 m with no overlap. Run: python3 roof_bay.py"""
from modlib import *
N, B, D, RC, RD, RN = 5, 4.0, 3.0, .1095, .084, .175
L = N * B

def _trim(a, b):  # member ending on a neighbour-owned edge node (x or z = L) stops 2 mm off that node's surface
    a, b = np.asarray(a, float), np.asarray(b, float)
    if b[0] > L - .01 or b[2] > L - .01: d = b - a; b = b - d / np.linalg.norm(d) * (RN + .002)
    return a, b

def frame(q):
    st, nodes = [], []; yb, yt = RN, RN + D
    top = [(i*B, yt, j*B) for i in range(N) for j in range(N)]; bot = [((i+.5)*B, yb, (j+.5)*B) for i in range(N) for j in range(N)]
    for x, y, z in top:  # top chords to +X / +Z (last one stops 1 mm short of the neighbour tile's node)
        st += [tube((x, y, z), (min(x + B, L - RN - .002), y, z), RC, 4), tube((x, y, z), (x, y, min(z + B, L - RN - .002)), RC, 4)]
    for x, y, z in bot:
        st += [tube((x, y, z), (min(x + B, L - RN - .002), y, z), RC, 4), tube((x, y, z), (x, y, min(z + B, L - RN - .002)), RC, 4)]
        if x - B/2 < .01: st.append(tube((.001, y, z), (x, y, z), RC, 4))
        if z - B/2 < .01: st.append(tube((x, y, .001), (x, y, z), RC, 4))
    for b in bot:
        b = np.array(b)
        if q.get("branch"):  # tree-column echo: stem up 1.0 m, crown node, 4 branches to the top nodes
            c = b + [0, 1.0, 0]; st += [tube(b, c, RD*1.3, 5), node(c, .16, -1)]
            st += [tube(*_trim(c, b + [sx*B/2, D, sz*B/2]), RD*.8, 4) for sx in (-1, 1) for sz in (-1, 1)]
        else: st += [tube(*_trim(b, b + [sx*B/2, D, sz*B/2]), RD, 4) for sx in (-1, 1) for sz in (-1, 1)]
    nodes = [node(p, RN, -1) for p in top + bot]
    return st, nodes, yt

def build(q):
    p = Part(); st, nodes, yt = frame(q); p.add("Space_Frame", ST, *st, *nodes)
    if q.get("led"): p.add("Node_LED_Caps", CY, *[box(x - .06, x + .06, -.03, E, z - .06, z + .06) for x, _, z in [((i+.5)*B, 0, (j+.5)*B) for i in range(N) for j in (0, 2, 4)]])
    gy = yt + RC - E; panes, bars, solid, sky = [], [], [], []
    for i in range(N):
        for j in range(N):
            x0, z0 = i*B, j*B
            if q.get("sky") and (i + j) % 2 == 0 and 0 < i < N-1 and 0 < j < N-1:  # raised glass lantern pockets
                sky.append((x0 + 2, z0 + 2)); continue
            bars.append(box(x0 + 1.96, x0 + 2.04, gy - .003, gy + .06, z0 + .12, z0 + B - .12))
            for k in (0, 1):
                xa = x0 + k*2.045 + (.11 if k == 0 else 0); xb = x0 + 1.955 + k*1.92 + (0 if k == 0 else -.11)
                if q.get("leafpanel") and (i*3 + j + k) % 4 == 0:
                    solid.append(box(xa, xb, gy, gy + .03, z0 + .12, z0 + B - .12)); continue
                panes.append(pane(xa, xb, gy + .011, gy + .033, 0).apply_translation([0, 0, 0]) if False else box(xa, xb, gy, gy + .022, z0 + .12, z0 + B - .12))
    p.add("Roof_Glass_Panes", GL, *panes); p.add("Glazing_Bars", G, *bars)
    if solid:
        p.add("Leaf_Infill_Panels", SL, *solid)
        p.add("Leaf_Relief", LF, *[leaf((m.bounds[0][0] + .95, gy + .03 - .003, m.bounds[0][2] + .35), 3.2, 1.4, pitch=np.pi/2 - .12, t=.02) for m in solid])
    for cx, cz in sky:
        h = 1.2; ms = [box(cx - 1.9, cx + 1.9, gy, gy + .1, cz - 1.9, cz - 1.8), box(cx - 1.9, cx + 1.9, gy, gy + .1, cz + 1.8, cz + 1.9),
                       box(cx - 1.9, cx - 1.8, gy, gy + .1, cz - 1.8 + E, cz + 1.8 - E), box(cx + 1.8, cx + 1.9, gy, gy + .1, cz - 1.8 + E, cz + 1.8 - E)]
        p.add("Lantern_Curbs", G, *ms)
        V = np.array([(cx-1.8, gy+.1-E, cz-1.8), (cx+1.8, gy+.1-E, cz-1.8), (cx+1.8, gy+.1-E, cz+1.8), (cx-1.8, gy+.1-E, cz+1.8), (cx, gy+h, cz)])
        F = np.array([[0, 4, 1], [1, 4, 2], [2, 4, 3], [3, 4, 0], [0, 1, 2], [0, 2, 3]]); m = trimesh.Trimesh(V, F, process=False); m.fix_normals()
        m.metadata["uv"] = np.c_[(V[:, 0] - cx)/3.6 + .5, (V[:, 2] - cz)/3.6 + .5]; p.add("Lantern_Glass", GL, m)
        p.add("Lantern_Leaf_Finial", LF2, leaf_dir((cx, gy + h - .003, cz), (0, 1, 0), .9, .45, t=.03))
    if q.get("planters"):  # hanging planter pockets under 9 bottom nodes
        for i in (0, 2, 4):
            for j in (0, 2, 4):
                cx, cz = (i+.5)*B, (j+.5)*B
                p.add("Hanger_Rods", ST, *[box(cx + s*.435 - .012, cx + s*.435 + .012, -1.0 - E, RN - RC + E, cz - .012, cz + .012) for s in (-1, 1)])
                tr, so, sy = planter(cx - .45, cx + .45, -1.5, cz - .45, cz + .45, h=.5)
                p.add("Planter_Trough", G, tr.apply_translation([0, 0, 0])); p.add("Planter_Soil", SO, so)
                p.add("Foliage", LF2, clump((cx, sy + .3 - E, cz + .0), .3, i*5+j))
    if q.get("vines"):  # vines trailing along bottom chords (Z lines 1 and 3)
        for j in (1, 3):
            z = (j+.5)*B; s, l = vine([(.3, RN - RC - .03, z), (6, RN - RC - .2, z + .1), (12, RN - RC - .04, z - .1), (19.5, RN - RC - .25, z)], r=.02, leaf_every=.8, leaf_len=.35, seed=j, outward=True)
            p.add("Vine_Stems", LF, s); p.add("Vine_Leaves", LF2, l)
    return p

VARIANTS = [
    dict(label="Leaf Infill: opaque slate panels with leaf relief in a scattered pattern", leafpanel=True),
    dict(label="Lantern Pockets: raised glass skylight pyramids with leaf finials", sky=True),
    dict(label="Hanging Gardens: 9 planter pockets under the bottom nodes", planters=True),
    dict(label="Branch Diagonals: Y-fork tree-crown diagonals (tree column echo)", branch=True),
    dict(label="Vine Chords: vines trailing the bottom chords, cyan LED nodes", vines=True, led=True),
]
if __name__ == "__main__": run("roof_bay", build, VARIANTS, title="20x20 m tile, 4.0 m grid, 3.0 m deep | flat, ridge crown separate | nature")
