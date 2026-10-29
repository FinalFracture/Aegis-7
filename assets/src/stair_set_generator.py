"""Rev C asset #3: switchback stair set (2 flights + mid-landing + L2 landing), stair core v1.1 (approved, 818f136).
Coordinates = the stair-core plan coordinates of design/residential_stair_core_v1.py, unchanged, so the glb drops in at identity:
  origin (0,0,0) = building plan origin on the L1 finished floor (core centreline X=0; core clear X -1.9..1.9, Z -8.9..-0.8),
  X axial (fore -X / aft +X), Y up (toward axis), +Z spinward (corridor side at Z -0.8, Sector-4 shell face at Z -8.9).
Guards/handrails (#4) are NOT modeled; only their sockets and wall brackets."""
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import dining_chair_generator as dc
from dining_chair_generator import export_final, FMAT
from bath_pod_generator import blk, cyl, Pod
from kitchen_counter_generator import bev, box
import wardrobe_generator as wg
OUT = os.path.join(dc.ROOT, "design/assets/stair_set")
# ---- plan geometry (copied from design/residential_stair_core_v1.py) ----
RISE = 4.2; NR = 26; R = RISE / NR; T = .28; N1, N2 = 16, 10; FW = 1.5
XC = (-1.9, 1.9); ZS, ZN = -8.9, -0.8; F1 = (-1.9, -1.9 + FW); F2 = (1.9 - FW, 1.9)
ZL = ZS + 1.5; Z1b = ZL + (N1 - 1) * T; Z2t = ZL + (N2 - 1) * T; YL = N1 * R; SLAB_L = .25; SLAB2 = .30
FIN = .015; NOSE = .03   # slate tread finish thickness, orange nosing strip depth

def treads():
    """[(flight, k, x0, x1, za, zb, ytop)] za<zb; nosing at the downhill edge."""
    out = []
    for k in range(1, N1):            # flight 1 rises toward -Z (south) from Z1b
        out.append((1, k, *F1, Z1b - k * T, Z1b - (k - 1) * T, k * R))
    for j in range(1, N2):            # flight 2 rises toward +Z (north) from the mid-landing
        out.append((2, j, *F2, ZL + (j - 1) * T, ZL + j * T, YL + j * R))
    return out

def build():
    p = Pod("Stair_Set_Switchback")
    for f, k, x0, x1, za, zb, yt in treads():
        if f == 1:   # cast, closed below (under-stair store)
            p.add("Flight1_Cast", "white", box(x0, x1, 0, yt - FIN, za, zb))
            zn = zb - NOSE
        else:        # bolted modular step, open below (L1 walk passes under)
            p.add("Flight2_Modules", "white", box(x0, x1, yt - .25, yt - FIN, za, zb))
            p.add("Flight2_Stringer_Plates", "gunmetal", box(x0 - .02, x0, yt - .3, yt + .01, za, zb + .02), box(x1 - .0, x1 + .0001, yt - .3, yt - .29, za, za + .001)) if False else \
            p.add("Flight2_Stringer_Plates", "gunmetal", box(x0 - .02, x0, yt - .3, yt + .01, za, zb))
            zn = za
        p.add("Treads_Slate", "slate", box(x0, x1, yt - FIN, yt, za, zb) if f == 2 else box(x0, x1, yt - FIN, yt, za, zb))
        p.add("Nosing_Emergency", "amber", box(x0 + .03, x1 - .03, yt - .003, yt + .002, min(zn, zn + NOSE) if f == 2 else zn, (zn + NOSE) if f == 2 else zn + NOSE))
    # flight 1 top riser block up to the mid-landing (riser 16) + store front/door on the well side
    p.add("Flight1_Cast", "white", box(*F1, 0, YL - SLAB_L, ZL, ZL + .001 + T * 0 + .0) if False else box(*F1, 0, .001, ZL, ZL + .001))
    p.add("Store_Door", "gunmetal", box(F1[1] + .0, F1[1] + .012, .05, .95, -6.4, -5.6))
    p.add("Store_Door_Latch", "amber", box(F1[1] + .012, F1[1] + .02, .5, .56, -5.7, -5.65))
    # mid-landing (Z -8.9..-7.4, top Y 2.585, soffit 2.335) and L2 landing (Z -4.88..-0.8, top 4.2, slab 0.30)
    p.add("Mid_Landing", "white", bev(3.8, 1.5, YL - SLAB_L, YL - FIN, .01, .005, 1, 0, (ZS + ZL) / 2))
    p.add("Mid_Landing_Slate", "slate", box(*XC, YL - FIN, YL, ZS, ZL))
    p.add("L2_Landing", "white", bev(3.8, ZN - Z2t, RISE - SLAB2, RISE - FIN, .01, .005, 1, 0, (Z2t + ZN) / 2))
    p.add("L2_Landing_Slate", "slate", box(*XC, RISE - FIN, RISE, Z2t, ZN))
    p.add("Nosing_Emergency", "amber", box(XC[0] + .03, F2[0] - .0, RISE - .003, RISE + .002, Z2t, Z2t + NOSE),   # L2 edge over flight 1 + well
          box(F2[0] + .03, F2[1] - .03, YL - .003, YL + .002, ZL, ZL + NOSE))                                    # mid-landing edge at flight 2 start
    # spin-down anchoring: bolted gunmetal wall plates (walls X +-1.9, shell face Z -8.9) + floor shoes
    for x, s in ((XC[0], 1), (XC[1], -1)):
        for z in (-8.6, -7.7):
            p.add("Wall_Anchor_Plates", "gunmetal", box(min(x, x + s * .012), max(x, x + s * .012), YL - .24, YL - .04, z - .12, z + .12))
        for z in (-4.6, -2.6, -1.1):
            p.add("Wall_Anchor_Plates", "gunmetal", box(min(x, x + s * .012), max(x, x + s * .012), RISE - .29, RISE - .05, z - .12, z + .12))
    for z in (-6.0, -4.0):
        p.add("Wall_Anchor_Plates", "gunmetal", box(XC[0], XC[0] + .012, .4, .6, z - .12, z + .12))
    for x in (-1.5, 0, 1.5): p.add("Wall_Anchor_Plates", "gunmetal", box(x - .15, x + .15, YL - .24, YL - .04, ZS, ZS + .012))
    for z in (-3.1, -3.25): pass
    p.add("Floor_Anchor_Shoes", "gunmetal", box(F1[0] + .05, F1[1] - .05, 0, .02, Z1b, Z1b + .06))
    # #4 interface: guard sockets (well edges, landing edges, L2 edge) + handrail wall brackets both sides
    socks = []
    for k in range(1, N1, 3): socks.append((F1[1] + .02, k * R, Z1b - (k - .5) * T))
    for j in range(1, N2, 3): socks.append((F2[0] - .02, YL + j * R, ZL + (j - .5) * T))
    socks += [(x, YL, ZL - .05) for x in (-.3, .3)] + [(x, RISE, Z2t + .05) for x in (-1.6, -1.0, -.4, .2)]
    for x, y, z in socks: p.add("Guard_Sockets", "alloy", box(x - .03, x + .03, y - .06, y + .005, z - .04, z + .04))
    br = [(XC[0], k * R + .9, Z1b - (k - .5) * T) for k in range(2, N1, 4)] + [(XC[1], YL + j * R + .9, ZL + (j - .5) * T) for j in (2, 6)]
    br += [(F2[0] + .0, YL + j * R + .9 - 99, 0) for j in ()]
    for x, y, z in br:
        s = 1 if x < 0 else -1
        p.add("Handrail_Brackets", "alloy", box(min(x, x + s * .06), max(x, x + s * .06), y - .02, y + .02, z - .03, z + .03))
    # emergency stringer LEDs on flight 2 open edge + well face of flight 1
    p.add("Stringer_LEDs", "violet", *[box(F2[0] - .025, F2[0] - .02, YL + j * R - .2, YL + j * R - .17, ZL + (j - 1) * T, ZL + j * T) for j in range(1, N2)],
          *[box(F1[1], F1[1] + .005, k * R - .2, k * R - .17, Z1b - k * T, Z1b - (k - 1) * T) for k in range(2, N1)])
    return p

def verify():
    tr = treads(); f1 = [t for t in tr if t[0] == 1]; f2 = [t for t in tr if t[0] == 2]
    ys = [0] + [t[6] for t in f1] + [YL] + [t[6] for t in f2] + [RISE]
    rs = np.diff(ys); ok = dict(
        risers=len(rs), riser_h=(rs.min().round(4), rs.max().round(4)), flight1_risers=len(f1) + 1, flight2_risers=len(f2) + 1,
        treads=(len(f1), len(f2)), tread_d=round(T, 3), run1=round(Z1b - ZL, 3), run2=round(Z2t - ZL, 3), total_rise=round(sum(rs), 4),
        mid_landing=(ZS, ZL, round(YL, 4), round(YL - SLAB_L, 4)), L2_landing=(round(Z2t, 3), ZN, round(ZN - Z2t, 3)), bottom_landing=round(ZN - Z1b, 3),
        z_fit=round((ZL - ZS) + (Z1b - ZL) + (ZN - Z1b), 3))
    assert len(rs) == 26 and np.allclose(rs, R) and len(f1) + 1 == 16 and len(f2) + 1 == 10 and abs(sum(rs) - 4.2) < 1e-9
    return ok

if __name__ == "__main__":
    print(verify()); os.makedirs(OUT, exist_ok=True); p = build()
    gp = os.path.join(dc.ROOT, "godot/assets/models/stair_set_switchback.glb"); tris, geo = export_final(p.P, [gp])
    V = np.vstack([g[1] for g in geo.values()]); print("tris", tris, "bounds", V.min(0).round(3), V.max(0).round(3))
    sp = os.path.join(OUT, "final_stair_set_sheet.png"); r = wg.sheet(p, sp, "Final  #3 switchback stair set (stair core v1.1; guards/handrails #4 not shown)")
    os.remove(sp.replace("_sheet.png", ".glb")); print("non-watertight", r[4])

def add_reverse_iso(sp, p):
    """Append a second iso from the shell side (south-west, looking at flight 2 under the L2 landing)."""
    from PIL import Image
    from dining_chair_generator import render_view, shade_split
    from kitchen_counter_generator import tonemap, crop
    from bath_pod_generator import views
    geo = {k: (mk,) + tuple(shade_split(m)[i] for i in (0, 1, 3)) for k, (mk, m) in p.P.items()}
    saved = tonemap(); iso = views()[3]; a = np.pi; Ry = np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
    im = render_view(geo, iso @ Ry, size=760, shadow=True); ns = render_view(geo, iso @ Ry, size=760, shadow=False); FMAT.update(saved)
    fg = np.abs(ns - ns[0, 0]).sum(2) > .03; im[fg] = np.clip(im[fg] * 1.12 + .02, 0, 1); im = crop(im)
    a_ = Image.open(sp).convert("RGB"); b = Image.fromarray((np.clip(im, 0, 1) * 255).astype(np.uint8))
    s = a_.height / 2 / b.height; b = b.resize((int(b.width * s), int(b.height * s)))
    c = Image.new("RGB", (a_.width + b.width + 20, a_.height), (244, 242, 236)); c.paste(a_, (0, 0)); c.paste(b, (a_.width + 10, a_.height // 4))
    from PIL import ImageDraw; ImageDraw.Draw(c).text((a_.width + 20, a_.height // 4 - 20), "Iso (from shell side: flight 2 + mid-landing)", fill=(85, 85, 85)); c.save(sp)
if __name__ == "__main__": add_reverse_iso(sp, p)
