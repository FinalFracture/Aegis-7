"""Rook (Oct 31, box pipeline): platform-back infill (single version, no vote - PM call / Jared waived).
Fills Z -16.596..-15.5 behind the six #16 kerbs (X 9.003..20.997) at platform level y 0.30, sitting on y 0. 11.994 x 1.096 x 0.30.
Top matches the picked #44 paving 04 Tactile Guidance: pearl slabs + slate guide strip with floating cyan tactile bars, 2 m modules, 6 mm joints.
Placement: rotation 0, origin (15.0, 0, -16.048). 4 mm gap to the kerb back (Z -16.6). Shelter #15 rests on kerb backs + infill at y 0.297
(posts embedded 3 mm). Back face at Z -15.5 is a 0.25 m step down to the promenade paving (y 0.05) -> needs #45 ramp / edge (flag)."""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf
from ext_street_furniture_generator import Pod, box, FMAT, _PBR, G, S, T, A, E, xf
import ext_clip_check as cc
from ext_road_curved_generator import PL, CY
D2 = .548   # half depth
def infill():
    p = Pod("ext_platform_infill")
    p.add("Body", S, box(-5.994, 5.994, 0, .25 + E, -D2, D2))
    sl, st, bars = [], [], []
    for x in np.arange(-5, 6, 2):
        sl += [box(x - .997, x + .997, .25, .30, -D2 + .003, -.15 - .003), box(x - .997, x + .997, .25, .30, .15 + .003, D2 - .003)]
        st.append(box(x - .997, x + .997, .25, .30, -.15 + .003, .15 - .003))
        bars += [box(x - .977, x + .977, .302, .306, z - .02, z + .02) for z in (-.08, 0, .08)]
    p.add("Pavers", PL, *sl); p.add("Guide_Strip", S, *st); p.add("Tactile_Bars", CY, *bars)
    return p

def world_set(with_infill=True):
    from ext_tram_platform_kerb_generator import kerb
    from ext_tram_shelter_generator import shelter
    from ext_paving_kit_generator import tile
    Rr = np.eye(4); Rr[0, 0] = Rr[2, 2] = -1; asm = {}
    for i, x in enumerate(range(10, 21, 2)):
        for k, (mk, m) in kerb(2).P.items(): xf(m, R=Rr); m.apply_translation((x, 0, -17.55)); asm[f"K{i}_{k}"] = (mk, m)
    if with_infill:
        for k, (mk, m) in infill().P.items(): m.apply_translation((15.0, 0, -16.048)); asm["I_" + k] = (mk, m)
    sh = sf.recenter(shelter(5))
    for k, (mk, m) in sh.P.items(): xf(m, R=Rr); m.apply_translation((15.0, .297, -16.25)); asm["S_" + k] = (mk, m)
    for i, x in enumerate((10.0, 12.0)):
        for k, (mk, m) in tile(4, "promenade").P.items(): m.apply_translation((x, 0, -15.5 + .004 + 1.0)); asm[f"P{i}_{k}"] = (mk, m)
    return asm

if __name__ == "__main__":
    import validate_models as vm
    from ext_street_furniture_generator import export_final, set_glass_blend, render_view, views, crop, plt
    p = infill(); sf.recenter(p); c = cc.check(p.P)
    out = os.path.join(sf.ROOT, "design/assets/ext_platform_infill"); os.makedirs(out, exist_ok=True); gp = os.path.join(out, "ext_platform_infill.glb")
    tris, _ = export_final(p.P, [gp]); ok = vm.validate_file(gp, require_textures=False)
    asm = world_set(); a = cc.check(asm)
    r = dict(tris=tris, clip_pass=c["pass"], worst=c["worst_overlap"], coplanar=c["coplanar"], size=c["size"], validate=ok,
             asm_bad=[o for o in a["overlap"] if not o[3]], asm_coplanar=a["coplanar"], asm_open=a["open"])
    print("RES", json.dumps(r)); json.dump(r, open(os.path.join(out, "ext_platform_infill_report.json"), "w"), indent=1)
    _, geo = export_final(asm, ["/tmp/inf.glb"]); im = crop(render_view(geo, views()[3], size=900, glass_alpha=.35))
    fig = plt.figure(figsize=(16, 8), facecolor="#F4F2EC"); plt.imshow(im); plt.axis("off")
    plt.title(f"Rook platform-back infill ({tris} tris, clip {'PASS' if c['pass'] and not r['asm_bad'] and not r['asm_coplanar'] else 'FAIL'}) + 6 kerbs + shelter + promenade paving 04", color="#333")
    plt.savefig(os.path.join(out, "ext_platform_infill_fit_sheet.png"), dpi=80, facecolor="#F4F2EC")
