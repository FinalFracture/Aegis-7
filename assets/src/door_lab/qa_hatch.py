"""Rook door_lab QA for the bulkhead hatch: clip check closed(dogged) / closed(undogged) / 50% / open, swing sweep, previews."""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from door_lab_lib import *
import bulkhead_hatch as bh
rig = bh.build(); rig.recenter(); rep = {}
quick = "--quick" in sys.argv
poses = (("closed_dogged", 0, 1), ("closed_undogged", 0, 0), ("half_50pct", .5, 0), ("open", 1, 0))
for lab, fo, fb in poses:
    c = clip(rig, bh.deltas(rig, fo, fb), n_samp=250 if quick else 400); rep[lab] = summarize(c); print(lab, json.dumps(rep[lab], default=str), flush=True)
mov = [n for n in rig.order if (n.startswith(("leaf", "latch_bolt", "dog_handwheel", "piston")) and rig.N[n]["mesh"] and "colonly" not in n)]
fix = [n for n in rig.order if rig.N[n]["parent"] is None and rig.N[n]["mesh"] and "colonly" not in n and not n.startswith("piston")]
sw = []
# dogging motion (leaf closed): bolts 0..1
for fb in np.linspace(0, 1, 6):
    P = rig.world_parts(bh.deltas(rig, 0, fb)); d = penetration({k: P[k] for k in mov}, {k: P[k] for k in fix}, n_samp=200)
    sw.append(("dog", round(float(fb), 2), round(d[0], 4), d[1], d[2]))
# swing (bolts retracted) every 5 deg; pistons vs leaf too
for fo in np.linspace(0, 1, 22 if not quick else 8):
    P = rig.world_parts(bh.deltas(rig, fo, 0)); d = penetration({k: P[k] for k in mov if not k.startswith("piston")}, {k: P[k] for k in fix}, n_samp=200)
    d2 = penetration({k: P[k] for k in ("piston_body", "piston_rod")}, {k: P[k] for k in list(fix) + [m for m in mov if not m.startswith("piston") and m != "leaf_damper_mount"]}, n_samp=200)
    w = max((d, d2), key=lambda r: r[0]); sw.append(("swing", round(float(fo*bh.OPEN_DEG), 1), round(w[0], 4), w[1], w[2]))
rep["sweep"] = sw; rep["sweep_worst"] = max(sw, key=lambda r: r[2]); print("sweep worst", rep["sweep_worst"])
if not quick:
    for lab, fo, fb in (("closed", 0, 1), ("open", 1, 0)):
        render(rig, bh.deltas(rig, fo, fb), os.path.join(OUT_RENDER, f"door_lab_bulkhead_hatch_{lab}.png"))
        render(rig, bh.deltas(rig, fo, fb), os.path.join(OUT_RENDER, f"door_lab_bulkhead_hatch_{lab}_front.png"), R=views()[1])
json.dump(rep, open(os.path.join(OUT_RENDER, "bulkhead_hatch_qa.json"), "w"), indent=1, default=str)
