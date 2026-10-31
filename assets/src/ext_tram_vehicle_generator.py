"""Rook (Oct 30, box pipeline): residential exterior list v1 #19 tram vehicle (live, 2-car, ground-fed - NO pantograph, #18 cut).
Per candidate N (01..05): 19a car body w/ cab  design/assets/ext_tram_vehicle/ext_tram_car_body_0N.glb (<=5,800, rotate 180 deg about Y for car 2)
                         19b bogie + collector design/assets/ext_tram_vehicle/ext_tram_bogie_0N.glb   (<=1,500, x4)
Coupler is body-mounted (0.15 m at the -X car-joint end) so bogies stay identical x4; cars meet coupler-to-coupler -> 24.3 m overall.
World fit (track along X, +X = cab of car 1, track centre z = 0 here = scene Z -19.90): top of rail y 0.20, gauge 1.435 (rail centres z +/-0.7535).
  Body GLB pivot = skirt bottom -> place at y 0.12 (underframe 0.25..0.30); passenger floor = y 0.30 (= platform). Roof pods top y 3.40. Body shell 2.6 wide (2.66 over amber door sills).
  Bogie GLB pivot = flange bottom -> place at y 0.175 (tread on TOR 0.20, flanges inside rail heads, 2 mm clear). Bogie centres x +/-3.9 of each car.
  Collector_Shoe rides 5 mm over the centre power rail (top y 0.185). Wheel wells: floor cut-outs + Wheel_Housing tunnels (real cut-outs).
Script nodes (Gage): Door_L_01/02 (+Z side), Door_R_01/02 (-Z side) slide along X; Wheelset_1/2 spin about local Z through their axle centre
  (axle y 0.305 above bogie pivot, x +/-0.8); Headlights, Tail_Lights, Destination_Screen (wordless cyan), Collector_Shoe.
Aegis-7 + Civic pearl/cyan, amber accents, BLEND glass, zero wood.  Run: python3 ext_tram_vehicle_generator.py"""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf
from ext_street_furniture_generator import Pod, box, blk, cyl, FMAT, _PBR, G, S, T, A, GL, E, loft, rrect, xf, export_final, render_view, set_glass_blend, views, crop, plt, cc
FMAT["a7_pearl"] = _PBR(name="A7_PearlAlabaster", baseColorFactor=(0xD8/255, 0xDE/255, 0xE4/255, 1), metallicFactor=0.15, roughnessFactor=0.45)
FMAT["a7_cyan"] = _PBR(name="A7_CivicCyan", baseColorFactor=(0x38/255, 0xB8/255, 0xC8/255, 1), metallicFactor=0.1, roughnessFactor=0.4, emissiveFactor=(.1, .45, .5))
FMAT["a7_lamp"] = _PBR(name="A7_Lamp", baseColorFactor=(1, 1, .95, 1), metallicFactor=0, roughnessFactor=.3, emissiveFactor=(1, 1, .92))
PL, CY, LM = "a7_pearl", "a7_cyan", "a7_lamp"
OUT = os.path.join(sf.ROOT, "design/assets/ext_tram_vehicle")
BX = 3.9; DOORS = [(-2.15, -.85), (.85, 2.15)]; XN = 5.4   # bogie centres, door openings, nose start

def loftx(h, w, yc, rings, r=.06):  # rounded-rect (h tall in y, w wide in z) lofted along X; rings [(x, sw)]
    m = loft(rrect(h, w, r, 2), [(x, 1, s) for x, s in rings]); V = m.vertices.copy()
    m.vertices = np.c_[V[:, 1], V[:, 0] + yc, V[:, 2]]
    if m.volume < 0: m.invert()
    return m
def zcyl(x, y, z0, z1, r, s=14):
    m = cyl(0, 0, r, z0, z1, s); R = np.eye(4); R[:3, :3] = [[1, 0, 0], [0, 0, -1], [0, 1, 0]]; xf(m, R=R); m.apply_translation((x, y, 0)); return m

V = {  # body style knobs
 1: dict(nm="Civic_Pearl_Classic", wall=PL, skirt=S, liv=CY, door=CY, roof=G, w=(1.0, 2.3), ls=(.85, .95),
         nose=[(PL, .30, 1.40, 6.0, .86), (GL, 1.40, 2.55, 5.85, .9), (CY, 2.55, 3.0, 5.7, .92)], pods=[(-3.5, -1.0), (1.0, 3.5)]),
 2: dict(nm="Bullet_Nose", wall=PL, skirt=G, liv=A, door=PL, roof=T, w=(1.05, 2.35), ls=(.9, .96),
         nose=[(G, .30, .70, 6.0, .62), (PL, .70, 1.30, 5.98, .66), (GL, 1.30, 2.45, 5.88, .72), (PL, 2.45, 3.0, 5.6, .85)], pods=[(-4.0, 3.0)]),
 3: dict(nm="Carbon_Slate_Express", wall=S, skirt=G, liv=A, door=G, roof=PL, w=(1.0, 2.3), ls=(.88, .94),
         nose=[(S, .30, 1.20, 6.0, .97), (GL, 1.20, 2.6, 5.97, .97), (S, 2.6, 3.0, 5.9, .97)], pods=[(-3.0, -1.8), (-.6, .6), (1.8, 3.0)]),
 4: dict(nm="Panoramic_Glass", wall=PL, skirt=S, liv=CY, door=PL, roof=CY, w=(.85, 2.65), ls=(.72, .8),
         nose=[(PL, .30, 1.10, 6.0, .8), (GL, 1.10, 2.75, 5.8, .84), (PL, 2.75, 3.0, 5.6, .9)], pods=[(-2.0, 2.0)]),
 5: dict(nm="Duo_Tone_Workhorse", wall=PL, skirt=G, liv=CY, door=CY, roof=G, w=(1.1, 2.3), ls=(.32, 1.06), lower=G,
         nose=[(G, .30, 1.10, 6.0, .9), (GL, 1.10, 2.45, 5.9, .92), (PL, 2.45, 3.0, 5.75, .94)], pods=[(-4.5, -2.5), (-1.0, 1.0), (2.5, 4.5)], bumper=True),
}

def body(v):
    k = V[v]; p = Pod(f"ext_tram_car_body_0{v}"); y0, y1 = k["w"]; lw = k.get("lower", k["wall"])
    # underframe: floor with wheel-well cut-outs (|z|<0.95 over bays), side sills
    fl = []
    xs = [-6.0, -BX - 1.25, -BX + 1.25, BX - 1.25, BX + 1.25, XN]
    for i in (0, 2, 4): fl.append(box(xs[i], xs[i+1], .25, .30, -.95, .95))
    fl += [box(-6.0, XN, .25, .30, s * .95 if s > 0 else -1.295, 1.295 if s > 0 else -.95) for s in (1, -1)]
    p.add("Underframe", G, *fl)
    p.add("Skirts", k["skirt"], *[box(a + .02, b - .02, .12, .25 + E, s * 1.2 - .03, s * 1.2 + .03) for a, b in ((-6.0, -BX - 1.3), (-BX + 1.3, BX - 1.3), (BX + 1.3, XN)) for s in (1, -1)])
    for x in (-BX, BX):  # wheel housing tunnels (open below)
        p.add("Wheel_Housing", S, box(x - 1.3, x + 1.3, .85, .90, -1.0, 1.0),
              *[box(x - 1.3 + .002, x + 1.3 - .002, .30 - E, .85 + E, *sorted((s * .955, s * 1.0))) for s in (1, -1)],
              *[box(e - .025, e + .025, .30 - E, .85 + E, -.95 - E, .95 + E) for e in (x - 1.28, x + 1.28)])
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
    p.add("End_Wall", k["wall"], box(-5.994, -5.95, .30 - E, 3.0 + E, -1.25 - E, 1.25 + E))
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
          *[box(x - 1.1, x + 1.1, .90 - E, 1.3, .45, .9) for x in (-BX, BX)], *[box(x - 1.1, x + 1.1, .90 - E, 1.3, -.9, -.45) for x in (-BX, BX)])
    p.add("Grab_Poles", T, *[cyl(x, z, .02, .75 - E if abs(x) < .7 else .30 - E, 3.0 - E + .002, 8) for x, z in ((0, .3), (0, -.3), (-2.5, 0), (2.5, 0))])
    return p

def bogie(v):
    p = Pod(f"ext_tram_bogie_0{v}"); fr = [G, S, G, T, G][v - 1]; acc = [A, CY, A, A, CY][v - 1]
    for i, x in enumerate((-.8, .8), 1):
        p.add(f"Wheelset_{i}", T, zcyl(x, .48, -.864, .864, .07, 10), *[zcyl(x, .48, s * .7035 if s < 0 else .7035, s * .8035 if s < 0 else .8035, .28) if False else zcyl(x, .48, min(s * .7035, s * .8035), max(s * .7035, s * .8035), .28) for s in (1, -1)],
              *[zcyl(x, .48, min(s * .693, s * .7155), max(s * .693, s * .7155), .305) for s in (1, -1)])
    if v in (1, 3, 5):  # box side frames
        p.add("Side_Frames", fr, *[box(-1.2, 1.2, .40, .60, s * .86 if s > 0 else -.93, .93 if s > 0 else -.86) for s in (1, -1)])
    else:  # H-frame: shaped side frames dipping between axles
        p.add("Side_Frames", fr, *[box(-1.2, 1.2, .52, .64, *sorted((s * .86, s * .93))) for s in (1, -1)],
              *[box(x - .14, x + .14, .40, .52 + E, *sorted((s * .86, s * .93))) for x in (-.8, .8) for s in (1, -1)])
    p.add("Bolster", G if fr != G else S, box(-.15, .15, .55, .68, -.86 - E, .86 + E))
    p.add("End_Beams", fr, *[box(e - .04, e + .04, .45, .58, -.86 - E, .86 + E) for e in (-1.155, 1.155)])
    p.add("Springs", acc, *[cyl(x, s * .895, .03, .60 - E, .70, 8) for x in (-.4, .4) for s in (1, -1)] if v not in (2, 4) else [cyl(x, s * .895, .03, .64 - E, .72, 8) for x in (-.4, .4) for s in (1, -1)])
    p.add("Collector_Hanger", T, box(-.03, .03, .215 - E, .55 + E, -.02, .02))
    p.add("Collector_Shoe", acc, box(-.25, .25, .19, .215, -.04, .04))
    return p

def run():
    os.makedirs(OUT, exist_ok=True); rep = []; tiles = []; _, _, _, iso = views()
    for v in range(1, 6):
        b, g = body(v), bogie(v); row = {}
        world = {"body": (b, .25), "bogie": (g, .175)}
        for key, (p, wy) in world.items():
            chk_w = cc.check(p.P)  # in world coords (for assembly), then recenter for export
            sf.recenter(p); chk = cc.check(p.P)
            gp = os.path.join(OUT, f"{p.name}.glb"); tris, _ = export_final(p.P, [gp]); set_glass_blend(gp)
            import validate_models as vm; ok = vm.validate_file(gp, require_textures=False, require_blend_glass=(key == "body"))
            row[key] = dict(glb=os.path.relpath(gp, sf.ROOT), tris=tris, clip_pass=chk["pass"], worst=chk["worst_overlap"], bad=[o for o in chk["overlap"] if not o[3]],
                            coplanar=chk["coplanar"], open=chk["open"], size=chk["size"], validate=ok)
        # assembled car 1 (body + 2 bogies) clip check in world, + 2-car preview render
        bb, gg = body(v), bogie(v); asm = {}
        for k2, (mk, m) in bb.P.items(): asm["B_" + k2] = (mk, m)
        for j, x in enumerate((-BX, BX)):
            for k2, (mk, m) in bogie(v).P.items(): m.apply_translation((x, 0, 0)); asm[f"G{j}_{k2}"] = (mk, m)
        ac = cc.check(asm); row["assembly"] = dict(bad=[o for o in ac["overlap"] if not o[3]], coplanar=ac["coplanar"])
        prev = dict(asm)
        for k2, (mk, m) in list(asm.items()):
            m2 = m.copy(); m2.metadata["uv"] = m.metadata["uv"]; R = np.eye(4); R[0, 0] = R[2, 2] = -1; xf(m2, R=R); m2.apply_translation((-12.3, 0, 0)); prev["C2" + k2] = (mk, m2)
        _, geo = export_final(prev, ["/tmp/tram_preview.glb"])
        im = crop(render_view(geo, iso, size=900, shadow=True, glass_alpha=.35))
        _, gg2 = export_final(bogie(v).P, ["/tmp/bogie_prev.glb"]); im2 = crop(render_view(gg2, iso, size=500, shadow=True))
        row.update(cand=v, style=V[v]["nm"]); rep.append(row); print(json.dumps(row))
        tiles.append((f"{v}. {V[v]['nm']}\nbody {row['body']['tris']} | bogie {row['bogie']['tris']} tris | clip {'PASS' if row['body']['clip_pass'] and row['bogie']['clip_pass'] and not row['assembly']['bad'] and not row['assembly']['coplanar'] else 'FAIL'}", im, im2))
    fig, axs = plt.subplots(5, 2, figsize=(20, 26), facecolor="#F4F2EC", gridspec_kw=dict(width_ratios=[3, 1]))
    for (t, im, im2), (a1, a2) in zip(tiles, axs):
        a1.imshow(im); a1.axis("off"); a1.set_title(t, fontsize=12, color="#333"); a2.imshow(im2); a2.axis("off"); a2.set_title("bogie + Collector_Shoe", fontsize=10, color="#333")
    fig.suptitle("Rook  #19 tram vehicle (2-car, ground-fed, no pantograph)  candidates 01-05  |  2-car preview, BLEND glass translucent, iso", fontsize=14, color="#444")
    plt.tight_layout(rect=(0, 0, 1, .97)); sp = os.path.join(OUT, "ext_tram_vehicle_contact_sheet.png"); fig.savefig(sp, dpi=80, facecolor="#F4F2EC"); plt.close(fig)
    json.dump(rep, open(os.path.join(OUT, "ext_tram_vehicle_report.json"), "w"), indent=1); print("sheet", sp)

if __name__ == "__main__": run()
