"""Arrival: foyer River Queue kit with corrected TICKETS glyphs on the backdrop.

The shared foyer_desk_final.glyph_word draws a backwards S (upper stem on the
right, lower stem on the left), so the last letter reads as a 2. The C aperture
is only ~0.15 of the letter width, so from the foyer glance (Patch shot 05) it
reads as an L. Together that is the "TILKET2" on the ticketing signs. The
glyphs are sculpted mesh on tt_foyer_backdrop, not a texture or UV fault, and
not on tt_foyer_desk. This file leaves foyer_desk.py and foyer_desk_final.py
untouched, overrides glyph_word, and re-exports tt_foyer_backdrop.glb.

Desk +Z / backdrop +Z face the W doors (placements yaw -90). Letters advance
in local +X and are readable from the guest side.

Run from tennis_tower/:
python3 rooms/temp-Arrival/foyer_desk_arrival.py
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TT = os.path.dirname(os.path.dirname(HERE))  # .../tennis_tower
sys.path.insert(0, TT)
sys.path.insert(0, os.path.join(TT, "structure"))
from modlib import *
import foyer_desk_final as F


def stroke(x0, x1, y0, y1, z0, z1, bev=.005):
    return [box(x0, x1, y0, y1, z0, z1), box(x0 + bev, x1 - bev, y0 + bev, y1 - bev, z1 - E, z1 + .006)]


def glyph_word(word, x0, y0, y1, z_face, cell=.22, gap=.06, thick=.022):
    """Sculpted bevelled block capitals, readable from +Z (guest / W-door side)."""
    def letter(ch, cx):
        w, t = cell * .85, cell * .18
        zh0, zh1 = z_face, z_face + thick
        M = []
        midy = (y0 + y1) / 2
        if ch == "T":
            M += stroke(cx - w/2, cx + w/2, y1 - t, y1, zh0, zh1)
            M += stroke(cx - t/2, cx + t/2, y0, y1 - t + E, zh0, zh1)
        elif ch == "I":
            M += stroke(cx - t/2, cx + t/2, y0, y1, zh0, zh1)
            M += stroke(cx - w*.35, cx + w*.35, y1 - t*.6, y1, zh0, zh1)
            M += stroke(cx - w*.35, cx + w*.35, y0, y0 + t*.6, zh0, zh1)
        elif ch == "C":
            # Open C (right side clear). Shared version only reached cx+w*0.35,
            # which reads as an L from a glancing foyer view.
            M += stroke(cx - w/2, cx - w/2 + t, y0 + t*.4, y1 - t*.4, zh0, zh1)
            M += stroke(cx - w/2, cx + w/2, y1 - t, y1, zh0, zh1)
            M += stroke(cx - w/2, cx + w/2, y0, y0 + t, zh0, zh1)
            M += stroke(cx + w/2 - t, cx + w/2, y1 - t*2.4, y1, zh0, zh1)
            M += stroke(cx + w/2 - t, cx + w/2, y0, y0 + t*2.4, zh0, zh1)
        elif ch == "K":
            M += stroke(cx - w/2, cx - w/2 + t, y0, y1, zh0, zh1)
            for i in range(4):
                yy0 = midy + (y1 - midy) * i / 4; yy1 = midy + (y1 - midy) * (i + 1) / 4
                xx0 = cx - w/2 + t + (w - t) * i / 4; xx1 = xx0 + (w - t) / 4 + t * .5
                M += stroke(xx0, xx1, yy0, yy1, zh0, zh1, bev=.003)
                yy0 = midy - (midy - y0) * (i + 1) / 4; yy1 = midy - (midy - y0) * i / 4
                M += stroke(xx0, xx1, yy0, yy1, zh0, zh1, bev=.003)
        elif ch == "E":
            M += stroke(cx - w/2, cx - w/2 + t, y0, y1, zh0, zh1)
            M += stroke(cx - w/2 + t - E, cx + w/2, y1 - t, y1, zh0, zh1)
            M += stroke(cx - w/2 + t - E, cx + w*.2, midy - t/2, midy + t/2, zh0, zh1)
            M += stroke(cx - w/2 + t - E, cx + w/2, y0, y0 + t, zh0, zh1)
        elif ch == "S":
            # Forward S: upper bowl opens to the right (stem on the left),
            # lower bowl opens to the left (stem on the right). The shared
            # strokes were mirrored, which reads as a 2.
            M += stroke(cx - w/2, cx + w/2, y1 - t, y1, zh0, zh1)
            M += stroke(cx - w/2, cx - w/2 + t, midy, y1 - t + E, zh0, zh1)
            M += stroke(cx - w/2, cx + w/2, midy - t/2, midy + t/2, zh0, zh1)
            M += stroke(cx + w/2 - t, cx + w/2, y0 + t - E, midy, zh0, zh1)
            M += stroke(cx - w/2, cx + w/2, y0, y0 + t, zh0, zh1)
        elif ch == " ":
            pass
        else:
            M += stroke(cx - w/2, cx + w/2, midy - t/2, midy + t/2, zh0, zh1)
        return M
    out = []; x = x0
    for ch in word:
        out += letter(ch, x + cell / 2); x += cell + gap
    return out


def build(q):
    F.glyph_word = glyph_word
    F.stroke = stroke
    return F.build(q)


def promote():
    """Re-export the backdrop only; desk / kiosk / stanchion glyphs are unchanged."""
    p = recenter(build(dict(piece="backdrop", seed=44)))
    gp = os.path.join(ROOT, "godot/assets/models", "tt_foyer_backdrop.glb")
    tris, _ = export_final(p.P, [gp]); finish_glb(gp)
    V = np.vstack([m.vertices for n, (mk, m) in p.P.items() if "colonly" not in n])
    lo, hi = V.min(0), V.max(0)
    print("tt_foyer_backdrop.glb", "tris", int(tris), "bbox", lo.round(4).tolist(), hi.round(4).tolist())
    return p, int(tris), lo, hi, gp


def clip_check(p):
    vis = {k: v for k, v in p.P.items() if "colonly" not in k}
    chk = cc.check(vis, n_samp=400)
    bad = [o for o in chk["overlap"] if not o[3] and o[0][:2] != o[1][:2]]
    hardware = ("Cable", "Pebble", "LED", "Ring", "Moss", "Bezel")
    hard_ok, hard_bad = [], []
    for o in bad:
        # o typically (a, b, depth, allowed_flag, ...)
        depth = o[2] if len(o) > 2 else None
        names = f"{o[0]} {o[1]}"
        if any(h in names for h in hardware) and (depth is None or depth <= 0.030 + 1e-6):
            hard_ok.append(o)
        elif depth is not None and depth <= 0.010 + 1e-6:
            hard_ok.append(o)
        else:
            hard_bad.append(o)
    cop = [c for c in chk["coplanar"] if c[0][:2] != c[1][:2]]
    return dict(overlap=hard_bad[:8], overlap_n=len(hard_bad),
                hardware_ok=len(hard_ok), coplanar=cop[:8], coplanar_n=len(cop),
                worst=(max((o[2] for o in bad), default=0)),
                pass_=not hard_bad and not cop)


if __name__ == "__main__":
    p, tris, lo, hi, gp = promote()
    assert tris < 6000, tris
    assert abs(lo[1]) <= 0.005, lo
    chk = clip_check(p)
    print("CLIP", {k: chk[k] for k in ("overlap_n", "coplanar_n", "worst", "hardware_ok", "pass_")})
    if not chk["pass_"]:
        print("CLIP_FAIL overlap", chk["overlap"])
        print("CLIP_FAIL coplanar", chk["coplanar"])
        sys.exit(1)
