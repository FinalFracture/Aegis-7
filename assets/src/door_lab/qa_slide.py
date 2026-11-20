"""Rook door_lab QA for the bi-parting slider: clip check closed / open / sweep, previews."""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from door_lab_lib import *
import biparting_slide as bs
rig = bs.build(); rig.recenter(); rep = {}
for lab, f in (("closed", 0.0), ("open", 1.0)):
    c = clip(rig, bs.deltas(f)); rep[lab] = summarize(c); print(lab, json.dumps(rep[lab], default=str))
mov = [n for n in rig.order if n.startswith(("leaf_", "roller_")) and rig.N[n]["mesh"] and "colonly" not in n]
fix = [n for n in rig.order if n in ("frame", "top_track", "threshold", "drive_belt", "status_light", "reveal_strips")]
sw = []
for f in np.linspace(0, 1, 26):
    P = rig.world_parts(bs.deltas(f)); d = penetration({k: P[k] for k in mov}, {k: P[k] for k in fix}, n_samp=300)
    sw.append((round(float(f), 2), round(d[0], 4), d[1], d[2]))
rep["sweep_worst"] = max(sw, key=lambda r: r[1]); print("sweep worst", rep["sweep_worst"])
os.makedirs(OUT_RENDER, exist_ok=True)
for lab, f in (("closed", 0.0), ("open", 1.0)):
    render(rig, bs.deltas(f), os.path.join(OUT_RENDER, f"door_lab_biparting_slide_{lab}.png"))
    render(rig, bs.deltas(f), os.path.join(OUT_RENDER, f"door_lab_biparting_slide_{lab}_front.png"), R=views()[1])
json.dump(rep, open(os.path.join(OUT_RENDER, "biparting_slide_qa.json"), "w"), indent=1, default=str)
