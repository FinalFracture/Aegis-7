"""Contact sheet and per-door motion graphs for a door-lab run directory."""
import csv
import sys
from pathlib import Path

from PIL import Image, ImageDraw


def main() -> None:
    run = Path(sys.argv[1]).resolve()
    for csv_path in sorted(run.glob("*/motion.csv")):
        _graph(csv_path, csv_path.with_name("motion.png"))
    shots = sorted(run.glob("*/*/*.png"))
    shots = [p for p in shots if p.parent.name == "shots"]
    if not shots:
        print("no shots under", run)
        return
    _sheet(shots, run / "contact_sheet.png")
    print("contact_sheet", len(shots), "frames")


def _graph(csv_path: Path, dest: Path) -> None:
    rows = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    if not rows:
        return
    leaves = []
    for row in rows:
        if row["leaf"] not in leaves:
            leaves.append(row["leaf"])
    use_yaw = False
    for row in rows:
        if abs(float(row["yaw_deg"])) > 1.0:
            use_yaw = True
            break
    key = "q" if "q" in rows[0] else ("yaw_deg" if use_yaw else "px")
    series = {leaf: [] for leaf in leaves}
    phases = []
    t_max = 1.0
    v_min = 0.0
    v_max = 1.0
    prev_phase = None
    for row in rows:
        t = float(row["time_s"])
        v = float(row[key])
        series[row["leaf"]].append((t, v, row.get("phase", "")))
        t_max = max(t_max, t)
        v_min = min(v_min, v)
        v_max = max(v_max, v)
        phase = row.get("phase", "")
        if phase != prev_phase:
            phases.append((t, phase))
            prev_phase = phase
    if abs(v_max - v_min) < 1.0e-6:
        v_max = v_min + 1.0
    w, h = 960, 360
    img = Image.new("RGB", (w, h), (246, 244, 240))
    draw = ImageDraw.Draw(img)
    left, top, right, bottom = 64, 28, w - 16, h - 36
    draw.rectangle((left, top, right, bottom), outline=(40, 40, 40))
    for tick in range(5):
        u = tick / 4.0
        x = left + u * (right - left)
        y = bottom - u * (bottom - top)
        draw.line((x, bottom, x, bottom + 4), fill=(40, 40, 40))
        draw.line((left - 4, y, left, y), fill=(40, 40, 40))
        draw.text((x - 12, bottom + 6), "%.2f" % (u * t_max), fill=(40, 40, 40))
        draw.text((4, y - 6), "%.2f" % (v_min + u * (v_max - v_min)), fill=(40, 40, 40))
    for t, phase in phases:
        x = left + (t / t_max) * (right - left)
        draw.line((x, top, x, bottom), fill=(190, 180, 160))
        draw.text((x + 1, top + 1), str(phase)[:8], fill=(90, 70, 40))
    colors = ((20, 90, 140), (160, 70, 30), (30, 120, 70), (90, 50, 130))
    for i, leaf in enumerate(leaves):
        pts = []
        for t, v, _phase in series[leaf]:
            x = left + (t / t_max) * (right - left)
            y = bottom - ((v - v_min) / (v_max - v_min)) * (bottom - top)
            pts.append((x, y))
        if len(pts) >= 2:
            draw.line(pts, fill=colors[i % len(colors)], width=2)
    label = key
    draw.text((left, 6), "%s  %s" % (csv_path.parent.name, label), fill=(20, 20, 20))
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest)


def _sheet(shots: list, dest: Path) -> None:
    cols = 10
    thumb_w = 192
    thumb_h = 108
    label_h = 16
    rows = (len(shots) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), (24, 26, 30))
    draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(shots):
        im = Image.open(path).convert("RGB")
        im.thumbnail((thumb_w, thumb_h))
        c = i % cols
        r = i // cols
        x = c * thumb_w
        y = r * (thumb_h + label_h)
        sheet.paste(im, (x, y))
        draw.text((x + 2, y + thumb_h), path.name[:28], fill=(220, 220, 220))
    dest.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dest)


if __name__ == "__main__":
    main()
