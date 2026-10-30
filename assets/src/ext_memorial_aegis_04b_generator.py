"""Rook (Oct 30, Jared 1:15 PM CT): ext_memorial_aegis_04b = picked cutaway 04 + RFID memorial tags inside the open drum.
Tags hang on 8 titanium wires strung bulkhead-to-bulkhead around the axial sun spine (r 0.22 m); each tag hangs radially OUTWARD
(the drum's spin-gravity "down"). Node tree: Drum_Spin (pivot on the drum axis) -> drum hull/glass/valleys/spine/bulkheads + Tags + wires,
so rotating Drum_Spin about local X spins the drum with its tags; Starport_Spin (same axis) holds the counter-rotating starport/drive.
04 is kept untouched. Run: python3 ext_memorial_aegis_04b_generator.py"""
import os, sys, json, numpy as np, trimesh, pygltflib
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf, ext_memorial_aegis_generator as ag, ext_clip_check as cc
from ext_street_furniture_generator import T, E, box, export_final, set_glass_blend, views, render_view, crop, recenter, FMAT, _PBR, A, plt
ROOT = sf.ROOT; OUT = os.path.join(ROOT, "design/assets/ext_memorial_aegis"); GP = os.path.join(OUT, "ext_memorial_aegis_04b.glb")
L = 3.2; R = 200 * L / 800; xa = -L / 2; dome = .25 * R; xb = xa + 520 * L / 800
X0, X1 = xa + dome + .03 + E, xb - .02 * L - .03 - E   # inner faces of the two bulkhead discs
p = ag.mem(4); CY = .7 + .2 + R; rng = np.random.default_rng(1315)
RW, NW = .22, 8; wires, tv, tt = [], [], []
for k in range(NW):
    th = 2 * np.pi * (k + .5) / NW; c, s = np.cos(th), np.sin(th)
    wires.append(ag.xprism(.003, [(X0 - E, 1), (X1 + E, 1)], CY + RW * c, 6, np.pi / 6, RW * s))
    for x in np.arange(X0 + .05, X1 - .03, .068):
        x += rng.uniform(-.008, .008); ln = .03 + rng.uniform(0, .025)
        m = box(x - .012, x + .012, RW + .002, RW + .002 + ln, -.0015, .0015); uv = m.metadata["uv"]
        m.apply_transform(trimesh.transformations.rotation_matrix(th, (1, 0, 0))); m.apply_translation((0, CY, 0)); m.metadata["uv"] = uv
        (tv if rng.random() < .35 else tt).append(m)
p.add("Tag_Wires", T, *wires); p.add("Tags_Violet", ag.VM, *tv); p.add("Tags_Ti", T, *tt); NTAG = len(tv) + len(tt)
V0 = next(iter(p.P.values()))[1].vertices[0].copy(); recenter(p); d = next(iter(p.P.values()))[1].vertices[0] - V0
AXIS = [0.0, float(CY + d[1]), float(d[2])]; chk = cc.check(p.P)
tris, geo = export_final(p.P, [GP]); set_glass_blend(GP)
DRUM = ("Drum_", "Valley_", "Axial_Sun_Spine", "Bulkhead_Discs", "Fwd_Endcap_Dome", "Aft_Baffle_Bulkhead", "Tag")
PORT = ("Docking_Collar", "Starport_Spine", "Fusion_Coils")
g = pygltflib.GLTF2().load(GP); roots = list(g.scenes[0].nodes); dk, pk = [], []
for i in roots:
    n = g.nodes[i]
    if n.name.startswith(DRUM) or n.name.startswith(PORT):
        n.translation = [0.0, -AXIS[1], -AXIS[2]]; (dk if n.name.startswith(DRUM) else pk).append(i)
for nm, ch in (("Drum_Spin", dk), ("Starport_Spin", pk)):
    g.nodes.append(pygltflib.Node(name=nm, translation=AXIS, children=ch))
g.scenes[0].nodes = [i for i in roots if i not in dk + pk] + [len(g.nodes) - 2, len(g.nodes) - 1]; g.save_binary(GP)
rep = dict(cand="ext_memorial_aegis_04b", tris=tris, tags=NTAG, wires=NW, size=chk["size"], pivot=chk["pivot"], clip_pass=chk["pass"], worst_overlap=chk["worst_overlap"],
           overlaps_over=[o for o in chk["overlap"] if not o[3]], coplanar=chk["coplanar"], open=chk["open"], spin_axis_y=AXIS[1], drum_children=len(dk), glb=os.path.relpath(GP, ROOT))
print(json.dumps(rep)); json.dump(rep, open(os.path.join(OUT, "ext_memorial_aegis_04b_report.json"), "w"), indent=1)
FMAT[A] = _PBR(name="amber", baseColorFactor=(0, 0, 0, 1), metallicFactor=0, roughnessFactor=1, emissiveFactor=(1.0, .58, 0.0))
top, front, side, iso = views()
def Ry(a): a = np.radians(a); return np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])
def Rx(b): b = np.radians(b); return np.array([[1, 0, 0], [0, np.cos(b), -np.sin(b)], [0, np.sin(b), np.cos(b)]])
inner = {k: v for k, v in geo.items() if k.startswith(("Tag", "Axial", "Valley", "Bulkhead"))}
shots = [("iso", geo, iso), ("front (+Z)", geo, front), ("iso from left", geo, Rx(22) @ Ry(-40)), ("high front 3/4", geo, Rx(40) @ Ry(20)),
         (f"close-up: {NTAG} tags on {NW} wires around the sun spine", inner, Rx(25) @ Ry(15))]
fig, axs = plt.subplots(1, 5, figsize=(24, 6.2), facecolor="#F4F2EC")
for ax, (t, gg, Rm) in zip(axs, shots): ax.imshow(crop(render_view(gg, Rm, size=600, shadow=gg is geo, glass_alpha=.35))); ax.axis("off"); ax.set_title(t, fontsize=11, color="#333")
fig.suptitle(f"Rook  ext_memorial_aegis_04b  (cutaway + RFID tags in the drum, parented to Drum_Spin)  {tris} tris | clip {'PASS' if chk['pass'] else 'FAIL'} | "
             f"{chk['size'][0]:.2f} W x {chk['size'][2]:.2f} D x {chk['size'][1]:.2f} H m", fontsize=13, color="#444")
plt.tight_layout(rect=(0, 0, 1, .92)); sp = os.path.join(OUT, "ext_memorial_aegis_04b_contact_sheet.png"); fig.savefig(sp, dpi=90, facecolor="#F4F2EC"); print("sheet", sp)
