"""Rook (Oct 30, Jared 1:26 PM CT): ext_hydro_pump_tank_01b = picked Side_Tank 01 + reactive indicators (not promoted).
 - Sight-glass level column on the cabinet front: titanium back plate/caps/rails, BLEND glass front pane, closed cavity.
 - WaterLevel_Fill: separate node, mesh local y 0..0.698 with node translation at the cavity floor -> scale.y 0..1 fills upward.
 - Temp_Seg_01..06: separate amber emissive nodes, bottom (01) to top (06).
Clip check is run at fill 0.05 / 0.5 / 1.0. Run: python3 ext_hydro_pump_tank_01b_generator.py"""
import os, sys, json, numpy as np, pygltflib
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf, ext_memorial_hydro_generator as mh, ext_clip_check as cc
from ext_street_furniture_generator import T, G, A, GL, E, box, export_final, set_glass_blend, views, render_view, crop, recenter, FMAT, _PBR, plt
OUT = os.path.join(sf.ROOT, "design/assets/ext_hydro_pump_tank"); GP = os.path.join(OUT, "ext_hydro_pump_tank_01b.glb")
F = .35; Y0, Y1 = .251, .949; X = (.133, .187); Z = (.373, .405); H = Y1 - Y0; NSEG = 6
WATER = "a7_water"
FMAT[WATER] = _PBR(name="a7_water_fill", baseColorFactor=(0.0, .55, .75, 1), metallicFactor=0, roughnessFactor=.15, emissiveFactor=(0, .12, .18))
def make(fill):
    p = mh.pump(1); p.name = "ext_hydro_pump_tank_01b"
    p.add("Gauge_Frame", T, box(.12, .2, .2, 1.0, F - E, .37), box(.12, .2, .2, .25, .37 - E, .42), box(.12, .2, .95, 1.0, .37 - E, .42),
          box(.12, .13, .25 - E, .95 + E, .37 - E, .42), box(.19, .2, .25 - E, .95 + E, .37 - E, .42))
    p.add("Gauge_Glass", GL, box(.13 - E, .19 + E, .25 - E, .95 + E, .409, .415))
    p.add("WaterLevel_Fill", WATER, box(X[0], X[1], Y0, Y0 + max(H * fill, .002), Z[0], Z[1]))
    for i in range(NSEG):
        y = .3 + i * .1; p.add(f"Temp_Seg_{i + 1:02d}", A, box(.26, .33, y, y + .08, F - E, F + .006))
    return recenter(p)
res = {}
for f in (.05, .5, 1.0):
    c = cc.check(make(f).P); res[f] = dict(pass_=c["pass"], worst=c["worst_overlap"], over=[o for o in c["overlap"] if not o[3]], cop=c["coplanar"], open=c["open"], size=c["size"], pivot=c["pivot"])
p = make(1.0); tris, geo = export_final(p.P, [GP]); set_glass_blend(GP)
# re-pivot WaterLevel_Fill to its base: vertices -= base, node.translation = base
g = pygltflib.GLTF2().load(GP); blob = bytearray(g.binary_blob()); base = np.array([0, Y0, 0], np.float32)
for n in g.nodes:
    if n.name == "WaterLevel_Fill":
        acc = g.accessors[g.meshes[n.mesh].primitives[0].attributes.POSITION]; bv = g.bufferViews[acc.bufferView]; o = bv.byteOffset + (acc.byteOffset or 0)
        v = np.frombuffer(bytes(blob[o:o + acc.count * 12]), np.float32).reshape(-1, 3) - base; blob[o:o + acc.count * 12] = v.tobytes()
        acc.min, acc.max = v.min(0).tolist(), v.max(0).tolist(); n.translation = base.tolist()
g.set_binary_blob(bytes(blob)); g.save_binary(GP)
nodes = [n.name for n in pygltflib.GLTF2().load(GP).nodes]
rep = dict(cand="ext_hydro_pump_tank_01b", tris=tris, nodes=nodes, fill_pivot=[0, Y0, 0], fill_height=H, clip={str(k): v for k, v in res.items()}, glb=os.path.relpath(GP, sf.ROOT))
print(json.dumps(rep)); json.dump(rep, open(os.path.join(OUT, "ext_hydro_pump_tank_01b_report.json"), "w"), indent=1)
FMAT[A] = _PBR(name="amber", baseColorFactor=(0, 0, 0, 1), metallicFactor=0, roughnessFactor=1, emissiveFactor=(1.0, .58, 0.0))
top, front, side, iso = views(); tiles = []
for f, lit, t in ((.15, 2, "LOW  fill 0.15, Temp_Seg_01..02 on"), (.5, 4, "MID  fill 0.50, Temp_Seg_01..04 on"), (1.0, 6, "FULL fill 1.00, Temp_Seg_01..06 on")):
    q = make(f)
    for i in range(lit, NSEG): mk, m = q.P[f"Temp_Seg_{i + 1:02d}"]; q.P[f"Temp_Seg_{i + 1:02d}"] = (sf.S, m)
    _, gq = export_final(q.P, ["/tmp/_p01b.glb"])
    tiles.append((t + " (iso)", crop(render_view(gq, iso, size=560, shadow=True, glass_alpha=.35))))
    tiles.append((t.split()[0] + " close-up (front)", crop(render_view({k: v for k, v in gq.items() if k.startswith(("Gauge", "WaterLevel", "Temp"))}, front, size=420, shadow=False, glass_alpha=.35))))
fig, axs = plt.subplots(1, 6, figsize=(26, 6.4), facecolor="#F4F2EC")
for ax, (t, im) in zip(axs, tiles): ax.imshow(im); ax.axis("off"); ax.set_title(t, fontsize=10, color="#333")
fig.suptitle(f"Rook  ext_hydro_pump_tank_01b  (01 + sight-glass WaterLevel_Fill + amber Temp_Seg_01..06)  {tris} tris | clip " +
             " / ".join(f"{k}: {'PASS' if v['pass_'] else 'FAIL'}" for k, v in res.items()), fontsize=13, color="#444")
plt.tight_layout(rect=(0, 0, 1, .92)); sp = os.path.join(OUT, "ext_hydro_pump_tank_01b_contact_sheet.png"); fig.savefig(sp, dpi=90, facecolor="#F4F2EC"); print("sheet", sp)
