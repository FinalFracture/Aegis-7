"""Rook (Oct 30, box pipeline): residential exterior list v1 #17 (re-do, Jared 8:55 PM CT "Do over. Mag Lev.") maglev guideway module.
Five candidates -> design/assets/ext_maglev_guideway/ext_maglev_guideway_01..05.glb + contact sheet + kerb fit sheet. No rails, no power rail.
10 m along X; top pieces end at x +/-4.997 (6 mm joints), bed slab at +/-4.994. Bed is asymmetric about the track (platform edge trimmed):
track-frame z -1.75 (far) .. +1.396 (platform). GLB pivot = bottom-centre of the bed -> track centre at local z +0.177.
Placement: rotation 0, local +Z = platform side, origin Z -20.077, y 0 (track centre Z -19.90; bed Z -21.65..-18.504, 4 mm to kerb at -18.5).
Script nodes (Gage): Stator_Lev (levitation stator strips), Stator_Guide (lateral guidance stators), Guide_Glow (amber, pulse on approach).
Vehicle envelope per candidate is in ENVELOPE (track-frame z, world y); vehicle floor y 0.30, body side at z +1.33 (7 cm to the kerb face).
Aegis-7 + Civic pearl/cyan, amber accents, zero wood. Joints embed 0.004 m.  Run: python3 ext_maglev_guideway_generator.py"""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import ext_street_furniture_generator as sf
from ext_street_furniture_generator import Pod, box, FMAT, _PBR, G, S, T, A, E, export_final, render_view, views, crop, plt, xf, cc
FMAT["a7_pearl"] = _PBR(name="A7_PearlAlabaster", baseColorFactor=(0xD8/255, 0xDE/255, 0xE4/255, 1), metallicFactor=0.15, roughnessFactor=0.45)
FMAT["a7_cyan"] = _PBR(name="A7_CivicCyan", baseColorFactor=(0x38/255, 0xB8/255, 0xC8/255, 1), metallicFactor=0.1, roughnessFactor=0.4)
PL, CY = "a7_pearl", "a7_cyan"
XB, XT, XI, XS = 4.994, 4.997, 4.988, 4.984   # bed, top pieces, inner pieces, stator strips (half lengths)
ZF, ZP = -1.75, 1.396
def sym(f, a, b): return [f(a, b), f(-b, -a)]   # mirrored z band pair

def guide(v):
    p = Pod(f"ext_maglev_guideway_0{v}")
    p.add("Bed", S, box(-XB, XB, 0, .04, ZF, ZP))
    top = .15 if v == 4 else .04
    if v != 4: p.add("Side_Lines", CY, *[box(-XI, XI, top - E, top + .004, z - .04, z + .04) for z in (ZF + .2, ZP - .2)])
    if v == 1:  # T-Beam: gunmetal web, pearl flange; lev stators under the flange wings, guide stators on flange edges
        p.add("Web", G, box(-XI, XI, .04 - E, .10 + E, -.15, .15))
        p.add("Flange", PL, box(-XT, XT, .10, .16, -.55, .55))
        p.add("Stator_Lev", T, *sym(lambda a, b: box(-XS, XS, .088, .10 + E, a, b), .30, .53))
        p.add("Stator_Guide", CY, *sym(lambda a, b: box(-XS, XS, .105, .155, a, b), .55 - E, .562))
        p.add("Guide_Glow", A, box(-XS, XS, .16 - E, .163, -.03, .03))
    elif v == 2:  # U-Trough: pearl trough walls, lev stators on the trough floor, guide stators on inner wall faces
        p.add("Trough_Walls", PL, *sym(lambda a, b: box(-XT, XT, .04 - E, .20, a, b), .70, .85))
        p.add("Stator_Lev", T, *sym(lambda a, b: box(-XS, XS, .04 - E, .05, a, b), .20, .60))
        p.add("Stator_Guide", CY, *sym(lambda a, b: box(-XS, XS, .08, .18, a, b), .688, .70 + E))
        p.add("Guide_Glow", A, *sym(lambda a, b: box(-XS, XS, .20 - E, .203, a, b), .76, .79))
    elif v == 3:  # Inverted-T Fin: gunmetal centre fin with guide stators on both faces, flat lev stator pads on the bed
        p.add("Fin", G, box(-XI, XI, .04 - E, .22, -.05, .05))
        p.add("Stator_Guide", CY, *sym(lambda a, b: box(-XS, XS, .08, .21, a, b), .05 - E, .062))
        p.add("Stator_Lev", T, *sym(lambda a, b: box(-XS, XS, .04 - E, .05, a, b), .30, .70))
        p.add("Guide_Glow", A, box(-XS, XS, .22 - E, .224, -.03, .03))
        p.add("Fin_Markers", PL, *[box(x - .25, x + .25, .04 - E, .046, -.2, -.12) for x in (-3.75, -1.25, 1.25, 3.75)])
    elif v == 4:  # Embedded Slot: flush slate deck with a real centre slot cut-out; guide stators on slot walls, lev strips on the deck
        p.add("Deck", S, box(-XT, XT, .04 - E, .15, ZF + .002, -.12), box(-XT, XT, .04 - E, .15, .12, ZP - .002))
        p.add("Stator_Guide", CY, *sym(lambda a, b: box(-XS, XS, .06, .14, a, b), .108, .12 + E))
        p.add("Stator_Lev", T, *sym(lambda a, b: box(-XS, XS, .15 - E, .153, a, b), .35, .75))
        p.add("Guide_Glow", A, box(-XS, XS, .04 - E, .044, -.03, .03))
        p.add("Side_Lines", PL, *[box(-XI, XI, .15 - E, .154, z - .04, z + .04) for z in (ZF + .2, ZP - .2)])
    elif v == 5:  # Twin Box Beams: two pearl box beams, lev stators on top, guide stators on inner faces, amber centre glow
        p.add("Box_Beams", PL, *sym(lambda a, b: box(-XT, XT, .04 - E, .18, a, b), .65, .95))
        p.add("Stator_Lev", T, *sym(lambda a, b: box(-XS, XS, .18 - E, .188, a, b), .70, .90))
        p.add("Stator_Guide", CY, *sym(lambda a, b: box(-XS, XS, .07, .17, a, b), .638, .65 + E))
        p.add("Guide_Glow", A, box(-XS, XS, .04 - E, .044, -.04, .04))
    return p
ITERS = [(1, "T_Beam"), (2, "U_Trough"), (3, "Inverted_T_Fin"), (4, "Embedded_Slot"), (5, "Twin_Box_Beams")]
ENVELOPE = {  # vehicle must stay outside the guideway by these (track-frame z bands, world y); floor y 0.30, body side z -1.33..+1.33
 1: "guideway top y 0.163. Underframe >= y 0.19 over |z|<=0.60; magnet arms in |z| 0.575..0.70 down to y 0.06, hooking under the flange to |z| 0.31 at y 0.060..0.076 (12 mm under Stator_Lev 0.088, 13 mm outside Stator_Guide 0.562); outside |z|>0.72 skirts down to y 0.06.",
 2: "guideway top y 0.203 (walls). Keel/magnet module inside |z|<=0.675 down to y 0.065 (15 mm over Stator_Lev 0.05, 13 mm to Stator_Guide 0.688); underframe >= y 0.225 over walls |z| 0.675..0.875; outside |z|>0.875 skirts to y 0.06.",
 3: "guideway top y 0.224 (fin). Underframe slot |z|<=0.08 must clear up to y >= 0.25 (26 mm over fin glow, 18 mm to Stator_Guide 0.062); lev pads |z| 0.28..0.72 bottom >= y 0.065; rest of underside/skirts >= y 0.06.",
 4: "guideway top y 0.154 (flush deck). Flat underside >= y 0.168 (15 mm over Stator_Lev 0.153); keel fin |z|<=0.09 down into the slot to y 0.06 (18 mm to Stator_Guide 0.108); skirts over the deck >= y 0.17.",
 5: "guideway top y 0.188 (beam stators). Underframe >= y 0.205 over beams |z| 0.63..0.97; centre keel between beams |z|<=0.62 down to y 0.06 (18 mm to Stator_Guide 0.638); outer skirts |z|>=0.97 to y 0.06.",
}
sf.ASSETS["maglev"] = ("ext_maglev_guideway", guide, ITERS, 400, "#17 maglev guideway 10x3.15 (trimmed platform edge, track centre local z +0.177)")

def kerb_fit(v):  # world assembly: guideway (rot 0, track at Z -19.90) + 6x promoted kerb 02 (rot 180, origins Z -17.55)
    from ext_tram_platform_kerb_generator import kerb
    asm = {}
    for k, (mk, m) in guide(v).P.items(): m.apply_translation((15, 0, -19.90)); asm["M_" + k] = (mk, m)
    Rr = np.eye(4); Rr[0, 0] = Rr[2, 2] = -1
    for i, x in enumerate(range(10, 21, 2)):
        for k, (mk, m) in kerb(2).P.items(): xf(m, R=Rr); m.apply_translation((x, 0, -17.55)); asm[f"K{i}_" + k] = (mk, m)
    a = cc.check(asm)
    zm = max(m.vertices[:, 2].max() for k, (mk, m) in asm.items() if k.startswith("M_")); zk = min(m.vertices[:, 2].min() for k, (mk, m) in asm.items() if k.startswith("K"))
    return dict(bad=[o for o in a["overlap"] if not o[3]], coplanar=a["coplanar"], open=a["open"], gap=round(zk - zm, 4)), asm

if __name__ == "__main__":
    rep = sf.build("maglev"); import validate_models as vm
    out = os.path.join(sf.ROOT, "design/assets/ext_maglev_guideway"); tiles = []
    for r, (v, nm) in zip(rep, ITERS):
        r["validate"] = vm.validate_file(os.path.join(sf.ROOT, r["glb"]), require_textures=False)
        r["kerb_fit"], asm = kerb_fit(v); r["envelope"] = ENVELOPE[v]; print(r["cand"], r["validate"], json.dumps(r["kerb_fit"]))
        _, geo = export_final(asm, ["/tmp/mg_fit.glb"]); tiles.append((f"{v}. {nm} + 6x kerb 02 (gap {r['kerb_fit']['gap']*1000:.0f} mm)", crop(render_view(geo, views()[3], size=700, glass_alpha=.35))))
    fig, axs = plt.subplots(1, 5, figsize=(24, 6), facecolor="#F4F2EC")
    for ax, (t, im) in zip(axs, tiles): ax.imshow(im); ax.axis("off"); ax.set_title(t, fontsize=11, color="#333")
    fig.suptitle("Rook  #17 maglev guideway - world fit with promoted kerb (Z -18.5 seam), iso", fontsize=13, color="#444")
    plt.tight_layout(rect=(0, 0, 1, .92)); fig.savefig(os.path.join(out, "ext_maglev_guideway_kerb_fit_sheet.png"), dpi=80, facecolor="#F4F2EC"); plt.close(fig)
    json.dump(rep, open(os.path.join(out, "ext_maglev_guideway_report.json"), "w"), indent=1)
