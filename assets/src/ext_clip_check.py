"""Rook: 3d-part-clipping-check (model checks A1-A5) for multi-part Pod candidates.
A1 sub-part overlap <= 0.010 m (0.030 m for parts named *Hardware*/*Bolt*/*Hinge*), measured as max penetration of
   one part's vertices + surface samples into another closed part (trimesh signed distance).
A2 no coplanar faces from different parts within 0.001 m over > 1 cm2 (sampled-area estimate, same or opposite facing).
A4 pivot bottom-centre: min_y = 0 (+/-0.005 floor contact), X/Z centre within 0.005 m.
A5 open (non-watertight) parts are reported."""
import numpy as np, trimesh

def _parts(P):
    out = []
    for name, (mk, m) in P.items():
        for k, c in enumerate(m.split(only_watertight=False)): out.append((f"{name}[{k}]", name, c))
    return out

def check(P, n_samp=1500, seed=0):
    rng = np.random.default_rng(seed); parts = _parts(P); res = {"overlap": [], "coplanar": [], "open": [], "pivot": None}
    samp = {}
    for pid, base, m in parts:
        if not m.is_watertight: res["open"].append(pid)
        pts, fi = trimesh.sample.sample_surface(m, n_samp, seed=int(rng.integers(1e9)))
        samp[pid] = (np.vstack([m.vertices, pts]), np.r_[np.full(len(m.vertices), -1), fi])
    worst = 0.0
    for i, (pa, ba, ma) in enumerate(parts):
        for j, (pb, bb, mb) in enumerate(parts):
            if i == j or (ba == bb and pa == pb): continue
            if np.any(ma.bounds[0] > mb.bounds[1] + .002) or np.any(mb.bounds[0] > ma.bounds[1] + .002): continue
            S, fi = samp[pa]
            # penetration of A into B (only if B closed)
            if mb.is_watertight and ba != bb:
                inside = mb.contains(S)
                if inside.any():
                    d = float(trimesh.proximity.signed_distance(mb, S[inside]).max())
                    hw = any(t in (ba + bb).lower() for t in ("hardware", "bolt", "hinge"))
                    lim = .030 if hw else .010
                    if d > 1e-5: res["overlap"].append((pa, pb, round(d, 4), d <= lim)); worst = max(worst, d)
            # coplanar: A surface samples lying within 1 mm of B's surface with parallel normals
            if i < j and ba != bb:
                pts = S[fi >= 0]; ff = fi[fi >= 0]
                cp, dist, tri = trimesh.proximity.closest_point(mb, pts)
                par = np.abs(np.einsum("ij,ij->i", ma.face_normals[ff], mb.face_normals[tri])) > .995
                hit = (dist < .001) & par
                area = ma.area * hit.mean()
                if area > 1e-4: res["coplanar"].append((pa, pb, round(area * 1e4, 2)))
    V = np.vstack([m.vertices for _, _, m in parts]); lo, hi = V.min(0), V.max(0)
    res["pivot"] = dict(min_y=round(float(lo[1]), 4), cx=round(float((lo[0] + hi[0]) / 2), 4), cz=round(float((lo[2] + hi[2]) / 2), 4))
    res["size"] = (hi - lo).round(3).tolist()
    piv_ok = abs(lo[1]) <= .005 and abs(res["pivot"]["cx"]) <= .005 and abs(res["pivot"]["cz"]) <= .005
    res["pass"] = all(ok for *_, ok in res["overlap"]) and not res["coplanar"] and not res["open"] and piv_ok
    res["worst_overlap"] = round(worst, 4); return res
