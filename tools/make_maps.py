"""Plan sheets for Hab-7. Numbers from design/strip4_plan.md v2.2 and
design/cylinder_master_plan.md v3 (section 4 network, section 3 strip names).
Run from any cwd; PNGs are written next to this file. Matplotlib Agg only.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Patch
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
# Map renders go to godot/renders/maps/ (not next to this script).
MAPS_OUT = os.path.join(HERE, "..", "godot", "renders", "maps")
PAPER, INK = "#f7f5f0", "#1c1915"
CYAN, MAGENTA, ORANGE = "#0098B8", "#E0148C", "#FF8C00"
VIOLET, BLUE = "#7C3AED", "#2B7FDB"
Z_LO, Z_HI = -62.83, 62.83
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "savefig.facecolor": "auto", "hatch.linewidth": 0.5,
    "axes.unicode_minus": False,
})


def _kind_color(kind):
    return {"v": MAGENTA, "p": ORANGE}.get(kind, INK)


def _rect(ax, x0, x1, z0, z1, fc, ec="#3a342c", ls="-", lw=0.7, hatch=None, z=3):
    ax.add_patch(Rectangle((x0, z0), x1 - x0, z1 - z0, fc=fc, ec=ec, ls=ls,
                           lw=lw, hatch=hatch, zorder=z))


def _bubble(ax, n, x, z, kind="n", target=None):
    col = _kind_color(kind)
    kw = dict(ha="center", va="center", fontsize=11, fontweight="bold", color=col,
              zorder=30, clip_on=False,
              bbox=dict(boxstyle="circle,pad=0.18", fc="white", ec=col, lw=1.25))
    if target is None:
        ax.text(x, z, str(n), **kw)
    else:
        ax.annotate(str(n), xy=target, xytext=(x, z),
                    arrowprops=dict(arrowstyle="-", color=col, lw=0.6), **kw)


def _margin(ax, x, y_ax, text, color, target=None, italic=False, weight="bold", ha="center"):
    style = "italic" if italic else "normal"
    bbox = dict(boxstyle="round,pad=0.16", fc="white", ec=color, lw=0.7, alpha=0.95)
    common = dict(ha=ha, va="center", fontsize=11, color=color, fontstyle=style,
                  fontweight=weight, clip_on=False, zorder=28, bbox=bbox)
    if target is None:
        ax.text(x, y_ax, text, transform=ax.get_xaxis_transform(), **common)
    else:
        ax.annotate(text, xy=target, xycoords="data", xytext=(x, y_ax),
                    textcoords=ax.get_xaxis_transform(),
                    arrowprops=dict(arrowstyle="-", color=color, lw=0.55), **common)


def _leader(ax, x, y_ax, xz, color):
    ax.annotate("", xy=xz, xycoords="data", xytext=(x, y_ax),
                textcoords=ax.get_xaxis_transform(),
                arrowprops=dict(arrowstyle="-", color=color, lw=0.55),
                clip_on=False, zorder=18)


def _cross_gaps():
    gaps = []
    for c in range(50, 751, 50):
        half = 6.0 if c in (200, 400, 600) else 3.0
        gaps.append((c - half, c + half))
    return gaps


def _free(x0, x1, gaps):
    cur, segs = x0, []
    for a, b in gaps:
        if b <= cur or a >= x1:
            continue
        aa, bb = max(a, x0), min(b, x1)
        if aa > cur:
            segs.append((cur, aa))
        cur = max(cur, bb)
    if cur < x1 - 0.1:
        segs.append((cur, x1))
    return segs


def _pack(x0, x1, length=20.0, gap=4.0, min_len=12.0):
    out, x = [], x0
    while x < x1 - 0.1:
        room = x1 - x
        if room < min_len:
            break
        w = length if room >= length else room
        out.append((round(x, 2), round(x + w, 2)))
        x = x + w + gap
    return out


def _housing():
    """20 m units, 4 m gaps, broken at cross walks. -z units skip K-1."""
    rows = []
    for _name, x0, x1 in (("B/C", 255, 395), ("D/E", 455, 595), ("F", 655, 795)):
        for s0, s1 in _free(x0, x1, _cross_gaps()):
            for a, b in _pack(s0, s1):
                for sign, z0, z1 in ((1, 24, 42), (-1, -42, -24)):
                    if sign < 0 and a < 343 and b > 303 and x0 == 255:
                        continue  # K-1 occupies this footprint
                    rows.append((a, b, z0, z1, _name, sign))
    return rows


def _scale_and_compass(fig, ax):
    fig.canvas.draw()
    p0 = fig.transFigure.inverted().transform(ax.transData.transform((0, 0)))
    p1 = fig.transFigure.inverted().transform(ax.transData.transform((100, 0)))
    pos = ax.get_position()
    y = max(0.035, pos.y0 - 0.055)
    x0 = pos.x0 + 0.01
    dx = p1[0] - p0[0]
    fig.add_artist(Line2D([x0, x0 + dx], [y, y], transform=fig.transFigure,
                          color=INK, lw=5, solid_capstyle="butt"))
    fig.text(x0 + dx / 2, y + 0.012, "100 m", ha="center", va="bottom",
             fontsize=13, fontweight="bold", color=INK)
    fig.text(x0, y - 0.028, "FORE -x / AFT +x, z spinward toward S4|5",
             ha="left", va="top", fontsize=12, color=INK)


def draw_strip4():
    fig = plt.figure(figsize=(34, 12), dpi=200, facecolor=PAPER)
    ax = fig.add_axes([0.042, 0.17, 0.66, 0.70])
    leg = fig.add_axes([0.735, 0.035, 0.25, 0.92])
    fig.suptitle("STRIP 4 - SPIN STREET RESIDENTIAL (144 deg) - plan v2.2 / network v3 - R 200 m",
                 fontsize=20, fontweight="bold", color=INK, y=0.975)
    ax.set_xlim(0, 800)
    ax.set_ylim(Z_LO, Z_HI)
    ax.set_aspect("equal", adjustable="box")
    ax.set_axisbelow(True)
    ax.set_xticks(range(0, 801, 50))
    ax.set_yticks(list(range(-60, 61, 10)))
    ax.grid(True, color="#e0dbd2", lw=0.6, zorder=0)
    ax.tick_params(labelsize=9, top=True, bottom=True, labeltop=True, labelbottom=True,
                   left=True, right=True, labelleft=True, labelright=True, length=3)
    ax.set_xlabel("x  axial length (m)", fontsize=12)
    ax.set_ylabel("z  arc (m)", fontsize=12)
    for sp in ax.spines.values():
        sp.set_color("#2a2622")
    ax.add_patch(Rectangle((0, Z_LO), 800, Z_HI - Z_LO, fc="#fbfaf7", ec="none", zorder=0))

    # Walks. Commons (12 m) replace the 6 m cross walks at 200/400/600.
    _rect(ax, 0, 800, 45, 51.4, "#f6ddc4", ORANGE, "-.", 0.9, "///", 2)
    _rect(ax, 0, 800, -54.5, -45, "#f8d5e8", MAGENTA, "--", 1.1, None, 2)
    _rect(ax, 0, 800, -6, 6, "#e6c36a", "#8a6a28", "-", 0.6, None, 2)
    for c in range(50, 751, 50):
        if c in (200, 400, 600):
            _rect(ax, c - 6, c + 6, Z_LO, Z_HI, "#f7d0e4", MAGENTA, "--", 1.15, None, 3)
        else:
            _rect(ax, c - 3, c + 3, Z_LO, Z_HI, "#f3ead6", "#b3a48a", "-", 0.4, None, 3)
    ax.text(18, 0, "SPINE WALK", ha="center", va="center", fontsize=11,
            fontweight="bold", color="#3a2a10", zorder=6)
    ax.text(173, -49.75, "RIB WALK", ha="center", va="center", fontsize=11,
            fontstyle="italic", color=MAGENTA, zorder=6)

    # Buildings (section 6, v2 coordinates).
    _rect(ax, 86, 114, 27, 45, "#f0c27a", "#6b4a16", "-", 0.9, None, 4)
    ax.text(100, 31, "P-1", ha="center", va="center", fontsize=11, fontweight="bold", zorder=6)
    ha = [(53, 73), (77, 97), (103, 123), (127, 147), (153, 171), (175, 193)]
    for i, (a, b) in enumerate(ha):
        _rect(ax, a, b, -42, -24, "#f3ddb8", "#6b5428", z=4)
        ax.text((a + b) / 2, -33, "H-A%d" % (i + 1), ha="center", va="center", fontsize=11, zorder=6)
    span = 195 - 155
    gap, n = 1.0, 4
    w = (span - gap * (n - 1)) / n
    x = 155
    for i in range(n):
        _rect(ax, x, x + w, 10, 40, "#dce8c8", "#4d6a32", z=4)
        ax.text(x + w / 2, 25, "C-%d" % (i + 1), ha="center", va="center", fontsize=11, rotation=90, zorder=6)
        x += w + gap
    _rect(ax, 210, 240, -20, 20, "#f8d0e4", MAGENTA, "--", 1.3, None, 4)
    ax.text(225, 0, "M-1", ha="center", va="center", fontsize=11, fontweight="bold", color=MAGENTA, zorder=6)
    for a, b, z0, z1, name, sign in _housing():
        _rect(ax, a, b, z0, z1, "#f6e4c4" if sign > 0 else "#edd7b0", "#6b5428", z=4)
        tag = {"B/C": "H-B" if sign > 0 else "H-C", "D/E": "H-D" if sign > 0 else "H-E", "F": "H-F"}[name]
        ax.text((a + b) / 2, (z0 + z1) / 2, tag, ha="center", va="center", fontsize=11, zorder=6)
    _rect(ax, 303, 343, -44.5, -32.5, "#d5e4f5", "#2a5278", z=5)
    ax.text(323, -38.5, "K-1", ha="center", va="center", fontsize=11, fontweight="bold", zorder=6)
    _rect(ax, 407, 437, -44.5, -30.5, "#f8d0e4", MAGENTA, "--", 1.3, None, 5)
    ax.text(422, -37.5, "G-1", ha="center", va="center", fontsize=11, fontweight="bold", color=MAGENTA, zorder=6)
    _rect(ax, 610, 640, -40, -20, "#efe4d2", "#6b5428", z=4)
    ax.text(625, -30, "R-1", ha="center", va="center", fontsize=11, fontweight="bold", zorder=6)
    _rect(ax, 117.4, 121.6, 45.6, 48.7, VIOLET, "#4c1d95", "-", 0.8, None, 6)

    # Canal, basin, supply, culvert — Q5 on hold.
    _rect(ax, 40, 530, 51.4, 54.3, "#8ec8f0", ORANGE, "-.", 1.0, "...", 5)
    _rect(ax, 518, 545, 45, 54.3, "#5aa6e0", ORANGE, "-.", 1.2, "///", 5)
    _rect(ax, 38.75, 41.25, Z_LO, 51.4, "#8ec8f0", ORANGE, "-.", 0.8, "...", 5)
    _rect(ax, 528.75, 531.25, 54.3, Z_HI, "#8ec8f0", ORANGE, "-.", 0.8, "...", 5)

    # Seam ribs (3 m), end-cap rings (12 m), S4|5 guideway.
    _rect(ax, 0, 800, Z_LO, Z_LO + 3, "#d5d8de", "#6b7280", "-", 0.6, None, 6)
    _rect(ax, 0, 800, Z_HI - 3, Z_HI, "#c5f1f8", "#0e7490", "-", 0.6, None, 6)
    _rect(ax, 0, 12, Z_LO, Z_HI, "#6d28a0", "#3b0764", "-", 0.4, None, 7)
    _rect(ax, 788, 800, Z_LO, Z_HI, "#6d28a0", "#3b0764", "-", 0.4, None, 7)
    ax.plot([0, 800], [Z_HI, Z_HI], color=CYAN, lw=3.6, solid_capstyle="butt",
            zorder=9, clip_on=False)
    ax.text(6, 0, "FORE\nRING", ha="center", va="center", fontsize=11, color="white",
            fontweight="bold", rotation=90, zorder=8)
    ax.text(794, 0, "AFT\nRING", ha="center", va="center", fontsize=11, color="white",
            fontweight="bold", rotation=90, zorder=8)

    stations = [
        (0, "S1 FORE HUB", True), (100, "S2 x100", False), (200, "S3 x200", False),
        (300, "S4 x300", False), (400, "S5 x400", False), (500, "S6 x500", False),
        (600, "S7 x600", False), (700, "S8 x700", False), (800, "S9 AFT", True),
    ]
    for c, _lab, transfer in stations:
        x0, x1 = max(0, c - 15), min(800, c + 15)
        _rect(ax, x0, x1, 57.93, 61.43, "#b9f0f8", "#0e7490", "-", 0.8, None, 8)
        spans = ([(0, 7), (7, 14), (14, 21), (21, 28)] if c == 0
                 else [(772, 779), (779, 786), (786, 793), (793, 800)] if transfer
                 else [(c - 15, c - 8), (c + 7, c + 14)])
        for a, b in spans:
            _rect(ax, a, b, 54.3, 59.3, "#e7fbfe", "#0e7490", "-", 0.7, None, 8)
    for xg in (200, 400):
        ax.scatter([xg], [Z_LO], s=90, marker="s", c=MAGENTA, edgecolors="white",
                   linewidths=0.6, zorder=10, clip_on=False)

    # Block outlines on top of fills. B1 is the Q2 hold.
    blocks = [
        (1, "n", 0, 50, -62.8, 62.8), (2, "p", 50, 150, 6, 62.8),
        (3, "n", 50, 200, -62.8, -6), (4, "n", 150, 200, 6, 62.8),
        (5, "v", 200, 250, -62.8, 62.8), (6, "n", 250, 400, -62.8, 62.8),
        (7, "v", 400, 450, -62.8, 62.8), (8, "n", 450, 600, -62.8, 62.8),
        (9, "n", 600, 650, -62.8, 62.8), (10, "n", 650, 800, -62.8, 62.8),
    ]
    for _n, kind, x0, x1, z0, z1 in blocks:
        col = _kind_color(kind)
        ls = {"v": "--", "p": "-."}.get(kind, "-")
        hatch = "///" if kind == "p" else None
        fc = "#fff1e0" if kind == "p" else "none"
        _rect(ax, x0, x1, z0, z1, fc, col if kind != "n" else "#5c564c", ls,
              1.5 if kind != "n" else 0.8, hatch, 7)

    bubbles = [
        (1, 24, 22, "n", None), (2, 70, 16, "p", None), (3, 118, -14, "n", None),
        (4, 176, 52, "n", (176, 28)), (5, 225, 33, "v", None), (6, 268, 14, "n", None),
        (7, 430, 16, "v", None), (8, 488, 14, "n", None), (9, 628, 14, "n", None),
        (10, 710, 14, "n", None), (11, 100, 39, "n", None),
        (12, 140, 36, "n", (119.5, 47.15)), (13, 350, 14, "p", (350, 48.2)),
        (14, 531, 28, "p", (531.5, 49.6)), (15, 40, 38, "n", (8, 59.6)),
        (16, 768, 16, "n", (792, 59.6)), (17, 520, 0, "n", None),
        (18, 48, -49.7, "v", None), (19, 200, 12, "v", None),
        (20, 168, -16, "v", (200, Z_LO)), (21, 560, 16, "n", (560, Z_HI)),
    ]
    for n, x, z, kind, tgt in bubbles:
        _bubble(ax, n, x, z, kind, tgt)
    _leader(ax, 168, -16, (400, Z_LO), MAGENTA)

    # Margin callouts, kept off the 50 m ticks.
    for c, lab, _t in stations:
        dx = 28 if c < 800 else -32
        _margin(ax, c + dx, 1.13, lab, CYAN, (min(max(c, 8), 792), 59.6), weight="bold")
    _margin(ax, 70, 1.34, "FORE RING (0 m)\n2-level transfer · rail +10.2", "#5b218a", (6, 40), ha="left")
    _margin(ax, 250, 1.34, "PENDING JARED (Q2)", ORANGE, (100, 55), weight="bold")
    _margin(ax, 455, 1.34, "S4|5 MAGLEV (rail top +5.26)", CYAN, (455, Z_HI), weight="bold")
    _margin(ax, 620, 1.34, "PENDING JARED (Q5)", ORANGE, (280, 52.8), weight="bold")
    _leader(ax, 620, 1.34, (531.5, 50), ORANGE)
    _leader(ax, 620, 1.34, (530, 58), ORANGE)
    _margin(ax, 760, 1.34, "AFT RING (800 m)\n2-level transfer · rail +10.2", "#5b218a", (794, 40), ha="right")
    _margin(ax, 400, -0.15, "S3|4 RIB - NO LINE", "#4b5563", (400, Z_LO + 1.5), weight="bold")
    _margin(ax, 130, -0.36, "VANCE PROPOSAL", MAGENTA, (130, -49.7), italic=True, weight="medium")
    _margin(ax, 400, -0.36, "COMMONS WALKS · VANCE PROPOSAL", MAGENTA, (400, 20), italic=True, weight="medium")
    _leader(ax, 400, -0.36, (200, 30), MAGENTA)
    _leader(ax, 400, -0.36, (600, 30), MAGENTA)
    _margin(ax, 640, -0.36, "RIB CROSSINGS · VANCE PROPOSAL", MAGENTA, (400, Z_LO), italic=True, weight="medium")
    _leader(ax, 640, -0.36, (200, Z_LO), MAGENTA)
    ax.text(55, 8, "SUPPLY", fontsize=11, color=ORANGE, fontweight="bold", ha="left", zorder=12)
    ax.text(536, 58, "CULVERT", fontsize=11, color=ORANGE, fontweight="bold", ha="left", zorder=12)
    ax.text(140, 40, "MEMORIAL #29", fontsize=11, color=VIOLET, fontweight="bold", ha="left", zorder=12)

    _legend(leg)
    _scale_and_compass(fig, ax)
    os.makedirs(MAPS_OUT, exist_ok=True)
    path = os.path.join(MAPS_OUT, "strip4_plan.png")
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def _legend(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, transform=ax.transAxes, fc="#fffdf8",
                           ec="#c9c2b4", lw=0.8, zorder=0))
    ax.text(0.05, 0.985, "LEGEND", fontsize=16, fontweight="bold", va="top", color=INK)
    ax.text(0.05, 0.955, "Circled numbers match the plan.", fontsize=11, va="top", color="#444")
    swatches = [
        (0.90, "#fff", INK, "-", None, "Normal  —  adopted geometry"),
        (0.865, "#f8d0e4", MAGENTA, "--", None, "VANCE PROPOSAL  —  assumption, not a constraint"),
        (0.83, "#fff1e0", ORANGE, "-.", "///", "PENDING JARED  —  on hold (Q2 preface, Q5 canal)"),
    ]
    for y, fc, ec, ls, hatch, label in swatches:
        ax.add_patch(Rectangle((0.05, y), 0.06, 0.022, fc=fc, ec=ec, ls=ls, lw=1.2,
                               hatch=hatch, transform=ax.transAxes, clip_on=False))
        ax.text(0.13, y + 0.011, label, fontsize=11, va="center", color=ec if ec != INK else INK,
                fontstyle="italic" if ec == MAGENTA else "normal",
                fontweight="bold" if ec == ORANGE else "normal")
    rows = [
        (1, "n", "B-Fore", "x 0..50, z -62.8..62.8"),
        (2, "p", "B1 Preface  ·  PENDING JARED (Q2)", "x 50..150, z 6..62.8"),
        (3, "n", "B2 Housing Row A", "x 50..200, z -62.8..-6"),
        (4, "n", "B3 Courtyard Homes", "x 150..200, z 6..62.8"),
        (5, "v", "B4 Commons 200 / M-1  ·  VANCE PROPOSAL", "block x 200..250; M-1 x 210..240, z -20..20"),
        (6, "n", "B5 Housing B/C + K-1 Clinic/School", "x 250..400; K-1 x 303..343, z -44.5..-32.5"),
        (7, "v", "B6 Civic Gate G-1  ·  VANCE PROPOSAL", "x 400..450; G-1 x 407..437, z -44.5..-30.5"),
        (8, "n", "B7 Housing D/E + Headwater Basin", "x 450..600; basin x 518..545, z 45..54.3"),
        (9, "n", "B8 Commons 600 / R-1 Rec yard", "x 600..650; R-1 x 610..640, z -40..-20"),
        (10, "n", "B9 Aft Housing", "x 650..800, z -62.8..62.8"),
        (11, "n", "Preface building P-1", "x 86..114, z 27..45"),
        (12, "n", "Memorial #29", "x 117.4..121.6, z 45.6..48.7"),
        (13, "p", "Canal Promenade + canal  ·  PENDING JARED", "prom. z 45..51.4; canal x 40..530, z 51.4..54.3; supply x 40"),
        (14, "p", "Headwater Basin + culvert x530  ·  PENDING JARED", "basin x 518..545, z 45..54.3; culvert x 530 to S4|5"),
        (15, "n", "Fore Hub S1", "platform x 0..15 (clipped), z 57.93..61.43; 4 towers"),
        (16, "n", "Aft transfer S9", "platform x 785..800 (clipped), z 57.93..61.43; 4 towers"),
        (17, "n", "Spine Walk", "z -6..6, x 0..800 (12 m)"),
        (18, "v", "Rib Walk  ·  VANCE PROPOSAL", "z -54.5..-45"),
        (19, "v", "Commons Walks x200/400/600  ·  VANCE PROPOSAL", "x c-6..c+6, full z (12 m)"),
        (20, "v", "Rib crossings x200/x400  ·  VANCE PROPOSAL", "gated markers at z -62.83, to strip 3"),
        (21, "n", "S4|5 guideway + locals S2..S8", "z +62.83, x 0..800, rail top +5.26; locals x 100..700"),
    ]
    y = 0.79
    for n, kind, title, coord in rows:
        col = _kind_color(kind)
        ax.text(0.055, y, str(n), fontsize=11, fontweight="bold", color=col, ha="center", va="center",
                bbox=dict(boxstyle="circle,pad=0.16", fc="white", ec=col, lw=1.0))
        ax.text(0.10, y + 0.008, title, fontsize=11, color=col, va="center",
                fontstyle="italic" if kind == "v" else "normal",
                fontweight="bold" if kind == "p" else "medium")
        ax.text(0.10, y - 0.014, coord, fontsize=9, color="#4a453e", va="center")
        y -= 0.034


def draw_unrolled():
    names = [
        "The Long Window", "Meridian Science Quarter", "Cascade Biosphere (Valley B)",
        "Civic Commons", "Spin Street Residential (Valley A)", "The Green (Recreation)",
        "Lantern Row Residential", "Terrace Farms", "Foundry Reach (Valley C)",
        "Signal & Cargo Yards",
    ]
    cols = ["#8ecae6", "#9b8ec4", "#7dcea0", "#d5d8e8", "#f0c27a",
            "#8fd48f", "#e09a8a", "#c5d67a", "#e0a15a", "#8eabc4"]
    arc = 1256.6
    fig = plt.figure(figsize=(30, 12), dpi=200, facecolor=PAPER)
    ax = fig.add_axes([0.055, 0.08, 0.73, 0.80])
    leg = fig.add_axes([0.80, 0.10, 0.185, 0.74])
    fig.suptitle("CYLINDER HAB-7 UNROLLED - network v3 (5 axial lines, 2 end-cap rings) - 2026-10-31",
                 fontsize=20, fontweight="bold", color=INK, y=0.97)
    ax.set_xlim(0, 800)
    ax.set_ylim(0, 360)
    ax.set_xticks(range(0, 801, 100))
    ax.set_yticks(range(0, 361, 18))
    ax.tick_params(labelsize=9, top=True, labeltop=True, length=3)
    ax.set_xlabel("axial length x (m)    Fore 0  →  Aft 800", fontsize=12)
    ax.set_ylabel("angle around axis (deg)", fontsize=12)
    ax.set_axisbelow(True)
    ax.grid(True, color="#e4dfd6", lw=0.5, zorder=0)
    for sp in ax.spines.values():
        sp.set_color("#2a2622")

    def band(k, y0, y1):
        _rect(ax, 0, 800, y0, y1, cols[k], "none", z=1,
              hatch="//" if k == 0 else None, lw=0)
        # recolor alpha by drawing a white wash on non-highlighted strips
        if k != 4:
            _rect(ax, 0, 800, y0, y1, "white", "none", z=1, lw=0)
            ax.patches[-1].set_alpha(0.45)

    for k in range(10):
        lo, hi = 36 * k - 18, 36 * k + 18
        if k == 0:
            band(0, 0, 18)
            band(0, 342, 360)
            ax.text(430, 9, "0   The Long Window", ha="center", va="center", fontsize=13,
                    fontweight="bold", color="#0f3a52", zorder=4)
            ax.text(430, 351, "0   The Long Window  (wraps across 342..18)", ha="center",
                    va="center", fontsize=12, fontweight="bold", color="#0f3a52", zorder=4)
        else:
            band(k, lo, hi)
            weight = "bold"
            ax.text(400, 36 * k, "%d   %s    θ %d°" % (k, names[k], 36 * k),
                    ha="center", va="center", fontsize=13, fontweight=weight,
                    color="#3a2a08" if k == 4 else "#243028", zorder=4)
    ax.add_patch(Rectangle((0, 126), 800, 36, fc="none", ec="#b87410", lw=2.6, zorder=5))

    line_k = {0, 2, 4, 6, 8}
    for k in range(10):
        y = 18 + 36 * k
        is_line = k in line_k
        ax.plot([0, 800], [y, y], color=CYAN if is_line else "#8b9098",
                lw=3.2 if is_line else 0.9, zorder=5, solid_capstyle="butt")
        lab = "S%d|%d" % (k, (k + 1) % 10)
        if not is_line:
            lab += "  rib only"
        ax.text(640, y + (2.2 if is_line else -2.4), lab, ha="center", va="center", fontsize=11,
                color=CYAN if is_line else "#4b5563", fontweight="bold" if is_line else "normal",
                bbox=dict(fc="white", ec="none", alpha=0.75, pad=0.5), zorder=6)
    # Freight track beside S8|9 (306°), into the Aft Hub.
    ax.plot([0, 790], [309, 309], color="#7a4b24", lw=1.6, ls="--", zorder=5)
    ax.annotate("", xy=(800, 306), xytext=(790, 309),
                arrowprops=dict(arrowstyle="-|>", color="#7a4b24", lw=1.3), zorder=6)
    ax.text(200, 314, "FREIGHT (S8|9 only) -> AFT HUB", fontsize=11, color="#7a4b24",
            fontstyle="italic", fontweight="bold", ha="center",
            bbox=dict(fc="white", ec="#7a4b24", pad=1.2), zorder=6)

    _rect(ax, 0, 12, 0, 360, "#6d28a0", "#3b0764", z=3, lw=0.3)
    _rect(ax, 788, 800, 0, 360, "#6d28a0", "#3b0764", z=3, lw=0.3)
    ax.text(6, 180, "FORE RING", rotation=90, ha="center", va="center", fontsize=11,
            color="white", fontweight="bold", zorder=4)
    ax.text(794, 180, "AFT RING", rotation=90, ha="center", va="center", fontsize=11,
            color="white", fontweight="bold", zorder=4)

    xs, ys = [], []
    for k in line_k:
        y = 18 + 36 * k
        for x in (0, 800):
            xs.append(x)
            ys.append(y)
    ax.scatter(xs, ys, s=160, marker="s", c="white", edgecolors=CYAN, linewidths=1.4,
               zorder=7, clip_on=False)
    lx, ly = [], []
    for k in sorted(line_k):
        y = 18 + 36 * k
        for x in range(100, 701, 100):
            lx.append(x)
            ly.append(y)
    ax.scatter(lx, ly, s=36, marker="o", c=CYAN, edgecolors="white", linewidths=0.4, zorder=7)
    ax.scatter([0], [162], s=520, marker="*", c="#f5c518", edgecolors="#3a2a08",
               linewidths=0.6, zorder=8, clip_on=False)
    ax.scatter([800], [306], s=520, marker="*", c="#f5c518", edgecolors="#3a2a08",
               linewidths=0.6, zorder=8, clip_on=False)
    ax.text(36, 172, "FORE HUB", fontsize=12, fontweight="bold", color="#7a5b00", zorder=9,
            bbox=dict(fc="white", ec="#e6c200", pad=1.5))
    ax.text(748, 318, "AFT HUB", fontsize=12, fontweight="bold", color="#7a5b00", ha="right",
            zorder=9, bbox=dict(fc="white", ec="#e6c200", pad=1.5))
    ax.text(16, 28, "45 stops = 10 transfers + 35 locals", fontsize=13, fontweight="bold",
            color=INK, zorder=9, bbox=dict(boxstyle="round,pad=0.35", fc="#fff4cc", ec="#333", lw=1.0))

    ax2 = ax.twinx()
    ax2.set_ylim(0, arc)
    ax2.set_yticks([arc * d / 360.0 for d in range(0, 361, 36)])
    ax2.set_yticklabels(["%.0f" % (arc * d / 360.0) for d in range(0, 361, 36)])
    ax2.tick_params(labelsize=9, length=3)
    ax2.set_ylabel("arc length (m) at R 200     full turn = 1256.6 m", fontsize=12)
    ax2.grid(False)

    _unrolled_legend(leg)
    os.makedirs(MAPS_OUT, exist_ok=True)
    path = os.path.join(MAPS_OUT, "cylinder_unrolled.png")
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def _unrolled_legend(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, transform=ax.transAxes, fc="#fffdf8",
                           ec="#c9c2b4", lw=0.8))
    ax.text(0.06, 0.97, "LEGEND", fontsize=16, fontweight="bold", va="top")
    rows = [
        (CYAN, "-", 3.2, "Axial maglev line (5)\nS0|1, S2|3, S4|5, S6|7, S8|9"),
        ("#8b9098", "-", 1.2, "Seam rib only (5)\nS1|2, S3|4, S5|6, S7|8, S9|0"),
        ("#6d28a0", "-", 6, "Fore Ring x=0 and Aft Ring x=800\ntwo-level, ring rail +10.2"),
        ("#7a4b24", "--", 1.8, "Freight track, S8|9 only,\ninto the Aft Hub"),
        ("#b87410", "-", 2.4, "Strip 4 highlighted\nSpin Street Residential"),
    ]
    y = 0.88
    for color, ls, lw, text in rows:
        ax.plot([0.06, 0.18], [y, y], color=color, ls=ls, lw=lw, transform=ax.transAxes,
                solid_capstyle="butt", clip_on=False)
        ax.text(0.22, y, text, fontsize=11, va="center", color=INK)
        y -= 0.12
    ax.scatter([0.12], [y], s=140, marker="s", c="white", edgecolors=CYAN, linewidths=1.4,
               transform=ax.transAxes, clip_on=False)
    ax.text(0.22, y, "Transfer (ring × line)  ·  10", fontsize=11, va="center")
    y -= 0.08
    ax.scatter([0.12], [y], s=40, marker="o", c=CYAN, transform=ax.transAxes, clip_on=False)
    ax.text(0.22, y, "Local stop, x 100..700  ·  35", fontsize=11, va="center")
    y -= 0.08
    ax.scatter([0.12], [y], s=280, marker="*", c="#f5c518", edgecolors="#3a2a08",
               transform=ax.transAxes, clip_on=False)
    ax.text(0.22, y, "Hub  ·  Fore (0, S4|5)\n         Aft (800, S8|9)", fontsize=11, va="center")
    y -= 0.11
    ax.text(0.06, y, "45 stops = 10 transfers + 35 locals.\n"
            "Strip k is 36° centred at 36k°.\n"
            "Strip 0 wraps 342°..18°.\n"
            "36° = 125.66 m of arc at R 200.\n"
            "Lines on every other seam.\n"
            "Rings only at the end caps.",
            fontsize=11, va="top", color="#333")


def main():
    units = _housing()
    assert len(units) > 0
    for a, b, _z0, _z1, _n, _s in units:
        for g0, g1 in _cross_gaps():
            assert b <= g0 + 0.01 or a >= g1 - 0.01
    p1, p2 = draw_strip4(), draw_unrolled()
    print(p1)
    print(p2)


if __name__ == "__main__":
    main()
