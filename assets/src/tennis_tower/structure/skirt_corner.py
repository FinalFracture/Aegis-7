"""Rook r8b (2026-11-15): spec Rev 3.7.1 #7 plaza corner (X 168..171.4, Z 12.6..16) + TTQA-043. No new skirt piece: the last S-row
terrace skirt (was 957, X 164..168, Z 13.7 yaw 180) and the first E-row skirt (was 908, X 170.3, Z 16..20 yaw 90) are re-cut from the
same tt_plinth_skirt_terrace generator at 7.4 m and trimmed to a mitred meet on the diagonal X + Z = 184 (inner core corner X 169.2 /
Z 14.8 -> outer mat corner X 171.4 / Z 12.6): no overlap, no slit. A 0.2 m corner post (convcolonly) closes the outer wall corner
(X 170.22..170.42, Z 13.58..13.78); the wall parts stop at its faces (+5 mm bite). Mat/stones run to the mitre. Exported in building
coords via struct_lib.export_chunk (layout -> assemble_preview.structure()); assemble_preview.site() skips the two replaced modules.
Run: python3 skirt_corner.py"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from struct_lib import *
from scipy.spatial import cKDTree
import terrace_final as TF
MITRE = 184.0; PX0, PX1, PZ0, PZ1 = 170.22, 170.42, 13.58, 13.78    # 0.2 m post, inner corner on the mitre 3 cm inside the most recessed wall corner (cap / mid courses, X 170.25 Z 13.75)
SOLID = ("Skirt_Core", "Base_Mat", "Course0_Facets", "Course1_Facets", "Course2_Facets", "Course3_Facets", "Cap_Course", "Cap_Court_Line", "Cap_Drip_Edge")
MAT_PARTS = ("Base_Mat", "River_Stones", "Grass_Tufts", "Moss_Edge", "Mat-colonly")
def yawM(deg, t):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    M = np.eye(4); M[0, 0], M[0, 2], M[2, 0], M[2, 2] = c, s, -s, c; M[:3, 3] = t; return M
SCATTER = ("Tennis_Ball_Holds", "Jug_Holds", "Crimp_Holds", "Sloper_Holds", "Grip_Relief", "Seam_Tape", "Moss_Edge", "River_Stones", "Grass_Tufts")
# per-part cut offset (m, along the cut normal): both pieces cut each part on the same plane (no gap, no overlap across the mitre), while
# parts inside one piece never share a cap plane (A2 coplanar rule)
OFF = {"Base_Mat": .0045, "Cap_Court_Line": .0015, "Cap_Course": .003, "Cap_Drip_Edge": -.0015, "Skirt_Core": -.003, "Course1_Facets": .0015, "Course3_Facets": .0015}
def keep_side(v, planes):
    return np.all([(v - o) @ n >= -1e-9 for n, o in planes], axis=0)
def cut(m, planes, solid):
    """split into components: keep the ones fully inside, drop the outside ones; crossing ones are capped-sliced (solids) or dropped (scatter)."""
    uv0 = m.metadata.get("uv"); tree = cKDTree(m.vertices) if uv0 is not None else None; out = []
    for c in m.split(only_watertight=False):
        ins = keep_side(c.vertices, planes)
        if ins.all(): out.append(c); continue
        if not ins.any() or not solid: continue
        for n, o in planes:
            c = trimesh.intersections.slice_mesh_plane(c, np.asarray(n, float), np.asarray(o, float), cap=True)
            if len(c.faces) == 0: break
        if len(c.faces): out.append(c)
    if not out: return None
    r = trimesh.util.concatenate(out)
    if uv0 is not None: r.metadata["uv"] = uv0[tree.query(r.vertices)[1]]
    return r
def thin(m, keep):
    """keep every `keep`-th connected component (decor scatter only) to hold the 6k budget on the 7.4 m cut."""
    cs = m.split(only_watertight=False)
    if len(cs) < 4: return m
    uv0 = m.metadata["uv"]; tree = cKDTree(m.vertices); r = trimesh.util.concatenate(cs[::keep]); r.metadata["uv"] = uv0[tree.query(r.vertices)[1]]; return r
def side(name, yaw, centre, keep_dir, thin_k):
    from modlib import recenter
    p = recenter(TF.skirt_terrace(dict(width=7.4, seed=7)))   # GLB convention: bottom-centre of the visual AABB at the origin
    M = yawM(yaw, centre); parts, cols = [], []; d = 1 / math.sqrt(2)
    for k, (mk, m) in p.P.items():
        m = m.copy(); uv = m.metadata["uv"]; m.apply_transform(M); m.metadata["uv"] = uv
        if k in ("River_Stones", "Grass_Tufts") and thin_k > 1: m = thin(m, thin_k)
        o = OFF.get(k, 0.0); c0 = MITRE / 2 + o * d          # plane X + Z = 184 + o*sqrt2 (shifted o metres toward the E piece)
        if keep_dir < 0:   # S piece keeps X + Z <= ..., walls stop at the post W face X 170.22 (+5 mm bite, + o)
            pl = [([-d, 0, -d], [c0, 0, c0])] + ([] if k in MAT_PARTS else [([-1, 0, 0], [PX0 + .005 + o, 0, 0])])
        else:              # E piece keeps X + Z >= ..., walls stop at the post N face Z 13.78 (-5 mm bite, - o)
            pl = [([d, 0, d], [c0, 0, c0])] + ([] if k in MAT_PARTS else [([0, 0, 1], [0, 0, PZ1 - .005 - o])])
        c = cut(m, pl, solid=(k not in SCATTER))
        if c is None: continue
        (cols if "colonly" in k else parts).append((k, mk, c))
    return p, parts, cols
def gen(kind, width=4.0):
    from modlib import recenter
    import plinth_skirt_final as PS
    if kind == "terrace": return recenter(TF.skirt_terrace(dict(width=width, seed=7)))
    h0 = PS.HT; PS.HT = 4.0
    try: return recenter(PS.build(dict(width=width, seed=7)))
    finally: PS.HT = h0
def trimmed(kind, yaw, centre, n, c):
    """existing 4 m module (kind terrace / plinth) at its placement, cut to the half-space n . (x, z) <= c (mitre), per-part offsets as OFF."""
    p = gen(kind); M = yawM(yaw, centre); parts, cols = [], []; n = np.array([n[0], 0, n[1]], float); n /= np.linalg.norm(n)
    for k, (mk, m) in p.P.items():
        m = m.copy(); uv = m.metadata["uv"]; m.apply_transform(M); m.metadata["uv"] = uv
        o = OFF.get(k, 0.0) * (1 if kind == "terrace" else -1)          # terrace keeps the +o side of the shared plane, plinth the other
        pt = n * (c + o)                                                 # plane point on the normal through the origin
        cc_ = cut(m, [(-n, pt)], solid=(k not in SCATTER))
        if cc_ is None: continue
        (cols if "colonly" in k else parts).append((k, mk, cc_))
    return parts, cols
# TTQA-043 inside corners (terrace skirt row end vs the exposed building plinth skirt): (name, terrace (yaw, centre), plinth (yaw, centre),
# mitre normal n (terrace side keeps n.(x,z) <= c), c) - the plane runs from the wall-face corner to the mat corner
INSIDE = [("sw", (180, (-14.0, -4.0, 13.7)), (-90, (-12.0, -4.0, 11.5)), (1, -1), -25.7 / math.sqrt(2)),
          ("nw", (0, (-14.0, -4.0, 66.3)), (-90, (-12.0, -4.0, 67.5)), (1, 1), 54.3 / math.sqrt(2)),
          ("ne", (0, (142.0, -4.0, 66.3)), (90, (140.0, -4.0, 67.5)), (-1, 1), -73.7 / math.sqrt(2)),
          ("se", (180, (142.0, -4.0, 13.7)), (90, (140.0, -4.0, 11.5)), (-1, -1), -153.7 / math.sqrt(2))]
def footed():
    """TTQA-043 slit: the E/W terrace skirt rows bottom at y -4.0 while the drum dips to -4.048 (facets) at Z 36..44; this variant adds a
    0.2 m cast footing under the mat (inset 10 mm, 4 mm bite into the mat) so the module embeds 0.15 m; place at y -4.2."""
    p = gen("terrace"); f = box(-1.989, 1.989, -.2, .004, -1.09, 1.09)
    parts = [(k, mk, [m]) for k, (mk, m) in p.P.items() if "colonly" not in k] + [("Footing", SL, [f])]
    cols = [(k, [m]) for k, (mk, m) in p.P.items() if "colonly" in k] + [("Footing-colonly", [f.copy()])]
    return parts, cols
def build(REP, LAY):
    # S piece: yaw 180 at (167.7, -4, 13.7) spans X 164..171.4; keeps X + Z <= 184 and (walls) X <= 170.345
    _, ps, cs = side("s", 180, (167.7, -4.0, 13.7), -1, 3)
    # E piece: yaw 90 at (170.3, -4, 16.3) spans Z 12.6..20; keeps X + Z >= 184 and (walls) Z >= 13.655
    _, pe, ce = side("e", 90, (170.3, -4.0, 16.3), 1, 3)
    post = box(PX0, PX1, -4.0 + .045, -.3, PZ0, PZ1)
    out = {}
    for nm, ps_, cs_, extra in (("tt_plinth_skirt_terrace_mitre_s", ps, cs, None), ("tt_plinth_skirt_terrace_mitre_e", pe, ce, post)):
        parts = [(k, mk, [m]) for k, mk, m in ps_]; cols = [(k, [m]) for k, mk, m in cs_]
        if extra is not None: parts.append(("Corner_Post", SL, [extra])); cols.append(("Corner_Post-convcolonly", [extra.copy()]))
        out[nm] = export_chunk(nm, parts, cols, REP, layout=LAY, note="Rev 3.7.1 #7 plaza corner: terrace skirt re-cut 7.4 m, mitred on X+Z=184" + (" + 0.2 m corner post" if extra is not None else ""))
    for nm, (ty, tc), (py, pc), n, c in INSIDE:
        n2 = (n[0], n[1])
        tp, tcl = trimmed("terrace", ty, tc, n2, c)
        pp, pcl = trimmed("plinth", py, pc, (-n2[0], -n2[1]), -c)
        for an, ps_, cs_ in ((f"tt_plinth_skirt_terrace_mitre_{nm}", tp, tcl), (f"tt_plinth_skirt_mitre_{nm}", pp, pcl)):
            out[an] = export_chunk(an, [(k, mk, [m]) for k, mk, m in ps_], [(k, [m]) for k, mk, m in cs_], REP, layout=LAY,
                                   note=f"TTQA-043 / Rev 3.7.1 #7 {nm.upper()} inside corner: skirt trimmed to the mitre (no overlap, no slit)")
    fp, fc = footed()
    out["tt_plinth_skirt_terrace_footed"] = export_chunk("tt_plinth_skirt_terrace_footed", fp, fc, REP, layout=None,
                                                         note="TTQA-043: terrace skirt + 0.2 m footing (E/W rows Z 32..48, y -4.2)")
    return out
if __name__ == "__main__":
    LAY = json.load(open(LAYOUT)); REP = []
    build(REP, LAY); json.dump(LAY, open(LAYOUT, "w"), indent=1)
    print("FAILED", [r["asset"] for r in REP if not r["passed"]])
