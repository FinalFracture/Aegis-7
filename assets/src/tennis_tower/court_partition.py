"""Rook: Tennis Tower F1 glass court partition (spec §3.4 / §3.11.5 Rev 2.5, §3.11.9-10). Instanced 2.0 m panel: one steel post
(owned at -X, 2.0 m centres, runs to 5.0 m to carry the net), 12 mm toughened glass 3.0 m tall in a floor channel.
Ball net 3.0 -> 5.0 m is its own asset: v{i}_net.glb, pivot at its base, place at y = +3.0 on the same X/Z.
Tiles every 2.0 m along X; +Z = court side. Run: python3 court_partition.py"""
from modlib import *
import tempfile
GH, NH, PW = 3.0, 2.0, .08

def build(q):
    p = Part(); xp = -1 + PW/2
    p.add("Floor_Channel", G, box(-.999, .999, 0, .08, -.04, .04))
    p.add("Glass_Court_Pane", GL, box(-1 + PW + .004, .995, .08 - E, GH, -.006, .006))
    post = [box(-.997, -1 + PW, .08 - E, GH + NH, -.045, .045)]
    if q.get("fork"):  # Branch Fin echo: Y-fork from 3.0 m carrying the net head rail
        post = [box(-.997, -1 + PW, .08 - E, GH + .4, -.045, .045), node((xp, GH + .4, 0), .04, 1)]
        post += [tube((xp, GH + .4, 0), (xp + s*.35, GH + NH - .04, 0), .028, 6) for s in (-1, 1) if xp + s*.35 > -.999 + .03]
        post += [tube((xp, GH + .4, 0), (xp, GH + NH - .04, 0), .03, 6)]
    p.add("Post_Steel", ST, *post)
    clampx = (-1 + PW + .004, -1 + PW + .1)
    if q.get("leafclamp"):  # leaf-shaped clamp plates on both faces
        for y in (.6, 2.4):
            for s in (-1, 1): p.add("Leaf_Clamps", LF2, leaf((-.82, y - .16, s*(.006 + .012 - E)), .32, .16, t=.012))
        p.add("Kick_Rail_Green", LF, box(-1 + PW + .004, .995, .08 - E, .2, .006 - E, .03))
    else:
        for y in (.6, 2.4):
            for s in (-1, 1): p.add("Pane_Clamps", G, box(clampx[0] - .006, clampx[1], y - .05, y + .05, *sorted((s*(.006 - E), s*.026))))
    if q.get("planter"):  # outside (-Z) planter kick trough
        tr, so, sy = planter(-.95, .95, 0, -.5, -.06, h=.45); p.add("Planter_Trough", G, tr); p.add("Planter_Soil", SO, so)
        p.add("Foliage", LF2, shrubs(-.9, .9, sy, -.28, r=.2, seed=3))
    if q.get("brace"):  # roof Branch Diagonals echo: V-brace above the glass to the next post
        p.add("Head_Brace", ST, tube((-.905, GH + .1, 0), (0, GH + NH - .1, 0), .022, 6), tube((0, GH + NH - .1, 0), (.99, GH + .1, 0), .022, 6), node((0, GH + NH - .1, 0), .045, 1))
    if q.get("sport"):  # court-line amber LED, tennis-ball finial, Leaf Capital leaves at the post head
        p.add("Court_Line_LED", AM, box(-1 + PW + .004, .995, .08 - E, .11, .04 - E, .046))
        p.add("Ball_Finial", BA, node((xp, GH + NH + .065 - E, 0), .065, 1))
        p.add("Leaf_Capital", LF, *[leaf_dir((xp + np.cos(a)*.045, GH + NH - .25, np.sin(a)*.045), (np.cos(a)*.5, 1, np.sin(a)*.5), .3, .12, t=.01) for a in (np.pi/4, 3*np.pi/4, 5*np.pi/4, 7*np.pi/4)])
    return p

def net(q):  # ball net 2.0 x 2.0 m, own asset (alpha-scissor in engine), pivot at its base
    p = Part(); m, ms = q.get("mesh", .1), []
    ms += [box(-.999, .999, 0, .03, -.01, .01), box(-.999, .999, NH - .03, NH, -.01, .01)]
    if q.get("net") == "diamond":
        for c in np.arange(-2.0, 2.0, m*1.4):
            for s in (-1, 1):
                a = np.array([c, 0, 0]); b = a + [s*NH, NH, 0]
                t0, t1 = max(0, (-.999 - a[0]) / (b[0] - a[0]) if s < 0 else (-.999 - a[0]) / (b[0] - a[0])), 1
                ts = sorted([(-.999 - a[0]) / (b[0] - a[0]), (.999 - a[0]) / (b[0] - a[0])]); t0, t1 = max(0, ts[0]), min(1, ts[1])
                if t1 - t0 > .02: ms.append(beam(a + (b - a)*t0, a + (b - a)*t1, .006, .006))
    else:
        ms += [box(x - .003, x + .003, .03 - E, NH - .03 + E, -.003, .003) for x in np.arange(-.95, .96, m)]
        ms += [box(-.999, .999, y - .003, y + .003, -.004, .004) for y in np.arange(.1, NH - .05, m)]
    p.add("Ball_Net_Cord", SL, *ms)
    if q.get("netleaf"): p.add("Net_Leaf_Tags", LF2, *[leaf((x, NH - .03 - E + 0, .01 - E), .25, .12, t=.008) for x in (-.6, 0, .6)])
    return p

VARIANTS = [
    dict(label="Branch Post: Y-fork post head carries the net (Branch Fin)", fork=True, net="square"),
    dict(label="Leaf Clamp: leaf glass clamps, green kick rail, diamond net", leafclamp=True, net="diamond"),
    dict(label="Garden Kick: planter trough on the spectator side", planter=True, net="square", mesh=.12),
    dict(label="Branch Brace: V-brace over the glass (Branch Diagonals)", brace=True, net="diamond"),
    dict(label="Court Line: amber line LED, ball finial, Leaf Capital head", sport=True, net="square", netleaf=True),
]

def combo_geo(q):  # panel + net at +3.0, 3 bays side by side, for the player-height sheet
    P = {}
    for k in range(3):
        for tag, part, dy in (("p", recenter(build(q)) if False else build(q), 0), ("n", net(q), GH)):
            for nm, (mk, m) in part.P.items():
                m = m.copy(); m.metadata["uv"] = part.P[nm][1].metadata["uv"]; m.apply_translation((k*2.0, dy, 0)); P[f"{tag}{k}_{nm}"] = (mk, m)
    fd, tp = tempfile.mkstemp(suffix=".glb"); os.close(fd); _, geo = export_final(P, [tp]); os.remove(tp); return geo

def door(q):  # §3.11.5 door bay (2 per box), V3 Garden Kick style: fixed sidelight + 1.0 m clear opening, door leaf parked open 90°
    p = Part(); xp = -1 + PW/2; jx = (-.14, -.06); oh = 2.2
    p.add("Floor_Channel", G, box(-.999, jx[0] + E, 0, .08, -.04, .04))
    p.add("Glass_Sidelight", GL, box(-1 + PW + .004, jx[0] + E, .08 - E, GH, -.006, .006))
    p.add("Post_Steel", ST, box(-.997, -1 + PW, .08 - E, GH + NH, -.045, .045), box(jx[0], jx[1], 0, GH, -.045, .045))
    p.add("Door_Header", G, box(jx[1] - E, .999, oh, oh + .1, -.04, .04))
    p.add("Glass_Transom", GL, box(jx[1] + .004, .995, oh + .1 - E, GH, -.006, .006))
    p.add("Door_Leaf_Frame", G, box(.93, .97, 0.02, oh - .02, .05, .1))  # leaf hinge stile, swung onto the court side
    p.add("Glass_Door_Leaf", GL, box(.944, .956, .1, oh - .1, .1 - E + .0, .96))
    p.add("Pull_Handle", ST, box(.97 - E, 1.0, .9, 1.2, .85, .89))
    tr, so, sy = planter(-.95, jx[0] - .02, 0, -.5, -.06, h=.45); p.add("Planter_Trough", G, tr); p.add("Planter_Soil", SO, so)
    p.add("Foliage", LF2, shrubs(-.9, jx[0] - .06, sy, -.28, r=.2, seed=3))
    return p

if __name__ == "__main__" and sys.argv[1:] == ["door"]:
    run("court_partition", door, [dict(VARIANTS[2], label="Garden Kick door bay: 1.0 m clear opening, leaf parked open")], names=["v3_door"], suffix="_door", sheet="door_sheet.png")
elif __name__ == "__main__":
    rp = run("court_partition", build, VARIANTS, title="2.0 m panel: 3.0 m glass + post to 5.0 m | nature + sports")
    rn = run("court_partition", net, VARIANTS, title="ball net 2.0 x 2.0 m (own asset, place at +3.0)", suffix="_net")
    a = np.radians(4); eye = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])  # player eye ~1.7 m, looking at the glass from the court (+Z)
    iso = views()[3]; fig, axs = plt.subplots(2, 5, figsize=(24, 13), facecolor="#F4F2EC")
    for i, q in enumerate(VARIANTS):
        g = combo_geo(q)
        for r, (R, nm) in enumerate(((iso, "iso"), (eye, "player height, from court"))):
            ax = axs[r, i]; ax.imshow(np.clip(crop(render_view(g, R, size=560, shadow=r == 0, glass_alpha=.35)), 0, 1)); ax.axis("off")
            ax.set_title((f"V{i+1}  {q['label'].replace(': ', chr(10))}\npanel {rp[i]['tris']} tris {'PASS' if rp[i]['passed'] else 'FAIL'} | net {rn[i]['tris']} tris {'PASS' if rn[i]['passed'] else 'FAIL'}\n" if r == 0 else "") + f"3 bays + net, {nm}", fontsize=10)
    fig.suptitle("Rook | Tennis Tower court_partition V1-V5 | 2.0 m panel + separate ball net | top: iso, bottom: player height", fontsize=13)
    plt.tight_layout(rect=(0, 0, 1, .95)); fig.savefig(os.path.join(RENDER_OUT, "court_partition", "court_partition_contact_sheet.png"), dpi=80, facecolor="#F4F2EC"); plt.close(fig)
