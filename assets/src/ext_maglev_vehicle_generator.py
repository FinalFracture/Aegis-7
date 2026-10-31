"""Rook (Oct 30, box pipeline): #19 MAGLEV vehicle (Jared 8:55 PM CT re-do), 2-car set on promoted #17 ext_maglev_guideway (01 T-Beam).
Per candidate N: ext_maglev_car_body_0N.glb (car body w/ cab; car 2 = car 1 rotated 180 about Y) + ext_maglev_magnet_module_0N.glb (x1 per car).
No wheels / bogies / collector. Follows the T-Beam ENVELOPE (track-frame z from track centre, world y):
  underframe y 0.25..0.30 (>= 0.19 over |z|<=0.60); Magnet_Arms legs |z| 0.575..0.70 from y 0.06 up into the floor; Lev_Magnets hooks |z| 0.31..0.70 at
  y 0.060..0.076 (12 mm under Stator_Lev 0.088, 13 mm outside Stator_Guide 0.562); skirts |z| 1.17..1.23 down to y 0.06; body sides <= |z| 1.33.
Floor y 0.30 = platform. Placement + clearances: see PLACE in the report / VOTE_LOG. Aegis-7 + Civic pearl/cyan, amber, BLEND glass, zero wood."""
import os, sys, json, numpy as np, trimesh
sys.path.insert(0, os.path.dirname(__file__))
from ext_tram_vehicle_generator import *
import ext_tram_vehicle_generator as tv, ext_maglev_guideway_generator as mg
from ext_tram_platform_kerb_generator import kerb
OUT = os.path.join(sf.ROOT, "design/assets/ext_maglev_vehicle")
V[2]["nm"] = "Bullet_Nose"
def body(v):
    k = V[v]; p = Pod(f"ext_maglev_car_body_0{v}"); y0, y1 = k["w"]; lw = k.get("lower", k["wall"])
    p.add("Underframe", G, box(-6.0, XN, .25, .30, -1.295, 1.295))   # full floor, no wheel wells (>= y 0.19 over the beam)
    p.add("Skirts", k["skirt"], *[box(-5.9, XN - .1, .06, .25 + E, *sorted((s * 1.17, s * 1.23))) for s in (1, -1)])  # beyond |z| 0.72, down to y 0.06
    segs = [(-6.0, DOORS[0][0]), (DOORS[0][1], DOORS[1][0]), (DOORS[1][1], XN)]
    for s, side in ((1, "L"), (-1, "R")):
        z0, z1 = sorted((s * 1.25, s * 1.30)); zg0, zg1 = sorted((s * 1.269, s * 1.281)); zo = sorted((s * (1.30 - E), s * 1.306))
        for a, b in segs:
            p.add("Lower_Wall", lw, box(a, b, .30 - E, y0, z0, z1))
            n = max(1, round((b - a) / 1.6)); pil = np.linspace(a, b, n + 1)
            p.add("Wall", k["wall"], *[box(max(a + .002, q - .04), min(b - .002, q + .04), y0 - E, y1 + E, z0 + .002, z1 - .002) for q in pil])
            pa = [(max(a + .002, q - .04), min(b - .002, q + .04)) for q in pil]
            p.add("Side_Glass", GL, *[box(pa[i][1] - E, pa[i+1][0] + E, y0 - .002, y1 + .002, zg0, zg1) for i in range(n)])
            p.add("Livery_Stripe", k["liv"], box(a + .01, b - .01, k["ls"][0], k["ls"][1], *zo))
        p.add("Wall", k["wall"], box(-6.0, XN, y1, 3.0, z0, z1))
        for i, (a, b) in enumerate(DOORS, 1):
            p.add(f"Door_{side}_0{i}", k["door"], box(a + .003, b - .003, .303, y1 - .003, *sorted((s * 1.262, s * 1.29))))
            p.add("Door_Sills", A, box(a + .003, b - .003, .30 - E, .303 - .0005, *sorted((s * 1.30, s * 1.33))))
    p.add("End_Wall", k["wall"], box(-5.994, -5.95, .298, 3.0 + E, -1.25 - E, 1.25 + E))
    p.add("Tail_Lights", A, *[box(-6.0, -5.994 + E, 2.6, 2.75, s * .9 - .12, s * .9 + .12) for s in (1, -1)])
    p.add("Coupler", G, box(-6.15, -5.994 + E, .40, .52, -.1, .1))
    p.add("Roof", k["roof"], box(-6.0, XN + .02, 3.0 - E, 3.15, -1.29, 1.29))
    p.add("Roof_Pods", G if k["roof"] != G else T, *[blk(a, b, 3.15 - E, 3.40, -.7, .7, .08, 1) for a, b in k["pods"]])
    # cab nose: stacked lofted sections, raked; first ring sits 4 mm inside the body end
    for i, (mk, a, b, xe, sw) in enumerate(k["nose"]):
        g = mk == GL; m = loftx(b - a + 2 * E, 2.56 if g else 2.58, (a + b) / 2, [(XN - (.0065 if g else E), 1), (xe, sw)], r=.08)
        p.add("Cab_Glass" if mk == GL else "Cab_Nose", mk, m)
    lo = k["nose"][0]; top = k["nose"][-1]
    p.add("Headlights", LM, *[box(lo[3] - E, lo[3] + .012, lo[1] + .2, lo[1] + .34, s * .78 - .12, s * .78 + .12) for s in (1, -1)])
    p.add("Destination_Screen", CY, box(top[3] - E, top[3] + .012, top[1] + .12, top[2] - .12, -.7, .7))
    p.add("Seats", S, *[box(-.6, .6, .30 - E, .75, s * .75, s * 1.15) if s > 0 else box(-.6, .6, .30 - E, .75, -1.15, -.75) for s in (1, -1)],
          *[box(x - 1.1, x + 1.1, .30 - E, .75, *sorted((s * .75, s * 1.15))) for x in (-BX, BX) for s in (1, -1)])
    p.add("Grab_Poles", T, *[cyl(x, z, .02, .75 - E if abs(x) < .7 else .30 - E, 3.0 - E + .002, 8) for x, z in ((0, .3), (0, -.3), (-2.5, 0), (2.5, 0))])
    return p


MAGS = {1: ("continuous", A), 2: ("3_frames", CY), 3: ("faired", A), 4: ("4_frames", CY), 5: ("continuous_glowline", CY)}
def magnets(v):
    p = Pod(f"ext_maglev_magnet_module_0{v}"); kind, glow = MAGS[v]
    runs = {"continuous": [(-5.8, 5.2)], "faired": [(-5.8, 5.2)], "continuous_glowline": [(-5.8, 5.2)],
            "3_frames": [(-5.6, -2.4), (-1.6, 1.6), (2.0, 5.2)], "4_frames": [(-5.7, -3.4), (-2.6, -.3), (.3, 2.6), (3.0, 5.2)]}[kind]
    for a, b in runs:
        for s in (1, -1):
            p.add("Magnet_Arms", G, box(a, b, .064, .25 + E, *sorted((s * .575, s * .70))))
            p.add("Lev_Magnets", T, box(a + .002, b - .002, .060, .076, *sorted((s * .31, s * (.575 + E)))))
            p.add("Lev_Glow", glow, box(a + .05, b - .05, .12, .16, *sorted((s * (.70 - E), s * .706))))
    if kind == "faired": p.add("Fairings", PL, *[box(-5.7, 5.1, .10, .252, *sorted((s * (.70 - E), s * .74))) for s in (1, -1)]); p.P.pop("Lev_Glow"); \
        p.add("Lev_Glow", glow, *[box(-5.6, 5.0, .14, .18, *sorted((s * (.74 - E), s * .746))) for s in (1, -1)])
    if kind == "continuous_glowline": p.add("Lev_Glow", glow, *[box(-5.6, 5.0, .06 - .0, .064, *sorted((s * .40, s * .56))) for s in ()] or [box(-5.6, 5.0, .21, .23, *sorted((s * (.70 - E), s * .706))) for s in (1, -1)])
    return p

def world(v, car2=False, xc=0.0):  # world-placed body + magnets for one car (track centre Z -19.90)
    P = {}
    for tag, p in (("B", body(v)), ("M", magnets(v))):
        for k, (mk, m) in p.P.items():
            if car2: R = np.eye(4); R[0, 0] = R[2, 2] = -1; xf(m, R=R)
            m.apply_translation((xc, 0, -19.90)); P[f"{'C2' if car2 else 'C1'}{tag}_{k}"] = (mk, m)
    return P

def slab(geo_P, x0, x1):  # section slab between two X planes (capped) for the end-on view
    out = {}
    for k, (mk, m) in geo_P.items():
        if m.bounds[1][0] < x0 or m.bounds[0][0] > x1: continue
        s = m.slice_plane((x0, 0, 0), (1, 0, 0), cap=True)
        if s is None or not len(s.faces): continue
        s = s.slice_plane((x1, 0, 0), (-1, 0, 0), cap=True)
        if s is None or not len(s.faces): continue
        s.metadata["uv"] = np.zeros((len(s.vertices), 2)); out[k] = (mk, s)
    return out

def run():
    os.makedirs(OUT, exist_ok=True); rep = []; tiles = []; _, _, side, iso = views()
    for v in range(1, 6):
        row = dict(cand=v, style=V[v]["nm"], magnets=MAGS[v][0])
        for key, p in (("body", body(v)), ("magnets", magnets(v))):
            lo = np.vstack([m.vertices for _, m in p.P.values()]); mn, mx = lo.min(0), lo.max(0)
            off = dict(x=round(float((mn[0] + mx[0]) / 2), 4), y=round(float(mn[1]), 4), z=round(float((mn[2] + mx[2]) / 2), 4))
            sf.recenter(p); chk = cc.check(p.P); gp = os.path.join(OUT, f"{p.name}.glb"); tris, _ = export_final(p.P, [gp]); set_glass_blend(gp)
            import validate_models as vm; ok = vm.validate_file(gp, require_textures=False, require_blend_glass=(key == "body"))
            row[key] = dict(glb=os.path.relpath(gp, sf.ROOT), tris=tris, clip_pass=chk["pass"], worst=chk["worst_overlap"], bad=[o for o in chk["overlap"] if not o[3]],
                            coplanar=chk["coplanar"], open=chk["open"], size=chk["size"], validate=ok, origin_in_car_frame=off)
        # assembly: car 1 (cab +X) centred x 12.15, car 2 rotated at x -0.15 -> couplers meet at x 6.0; 3 guideway modules x 0..30 ; 6 kerbs X 10..20
        asm = {}; asm.update(world(v, False, 12.15)); asm.update(world(v, True, -.156))
        for j, xg in enumerate((-5.0, 5.0, 15.0)):
            for k, (mk, m) in mg.guide(1).P.items(): m.apply_translation((xg, 0, -19.90)); asm[f"G{j}_{k}"] = (mk, m)
        Rr = np.eye(4); Rr[0, 0] = Rr[2, 2] = -1
        for i, x in enumerate(range(10, 21, 2)):
            for k, (mk, m) in kerb(2).P.items(): xf(m, R=Rr); m.apply_translation((x, 0, -17.55)); asm[f"K{i}_{k}"] = (mk, m)
        a = cc.check(asm)
        veh = [m for k, (mk, m) in asm.items() if k.startswith("C")]; zmax = max(m.vertices[:, 2].max() for m in veh)
        row["assembly"] = dict(bad=[o for o in a["overlap"] if not o[3]], coplanar=a["coplanar"], open=a["open"], kerb_gap=round(-18.5 - zmax, 4))
        rep.append(row); print(json.dumps(row))
        _, geo = export_final(asm, ["/tmp/ml_asm.glb"]); im = crop(render_view(geo, iso, size=900, shadow=True, glass_alpha=.35))
        sec = slab(asm, 9.0, 9.6); _, g2 = export_final(sec, ["/tmp/ml_sec.glb"]); im2 = crop(render_view(g2, side, size=600, shadow=False, glass_alpha=.35))
        tiles.append((f"{v}. {V[v]['nm']} + magnets {MAGS[v][0]}\nbody {row['body']['tris']} | magnets {row['magnets']['tris']} tris | kerb gap {row['assembly']['kerb_gap']*1000:.0f} mm", im, im2))
    fig, axs = plt.subplots(5, 2, figsize=(20, 26), facecolor="#F4F2EC", gridspec_kw=dict(width_ratios=[2.2, 1]))
    for (t, im, im2), (a1, a2) in zip(tiles, axs):
        a1.imshow(im); a1.axis("off"); a1.set_title(t, fontsize=12, color="#333"); a2.imshow(im2); a2.axis("off"); a2.set_title("end-on section x 9.0-9.6 over T-beam + kerb (platform = left)", fontsize=10, color="#333")
    fig.suptitle("Rook  #19 MAGLEV vehicle (2-car) on promoted T-Beam guideway + kerbs  candidates 01-05  |  BLEND glass translucent", fontsize=14, color="#444")
    plt.tight_layout(rect=(0, 0, 1, .97)); sp = os.path.join(OUT, "ext_maglev_vehicle_contact_sheet.png"); fig.savefig(sp, dpi=80, facecolor="#F4F2EC"); plt.close(fig)
    json.dump(rep, open(os.path.join(OUT, "ext_maglev_vehicle_report.json"), "w"), indent=1); print("sheet", sp)

if __name__ == "__main__": run()
