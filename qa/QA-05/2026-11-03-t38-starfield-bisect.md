# QA-05 — T38 `starfield_rotates_while_vessel_stationary` regression check (2026-11-03)

Box run: Godot 4.7.2, xvfb 1920x1080x24, fresh clone, `--headless --import` before each run, then `godot --qa-reticle-stars-doors`. Box CPU rendering, not Jared's GPU.

## Results
| Commit | Run 1 star_drot | Run 2 star_drot | Result | T38 failures |
|---|---|---|---|---|
| 807511d (before batch) | 0.0419 rad | 0.0421 rad | PASS x2 | 0 |
| b724bdc (after batch) | 0.0415 rad | 0.0422 rad | PASS x2 | 0 |

hab_dpos=0.000000 and hab_drot=0.000000 in all four runs.

```
[T38-QA] PASS | starfield_rotates_while_vessel_stationary | star_drot=0.0415 rad (2.38 deg) hab_dpos=0.000000 hab_drot=0.000000
[T38-QA] DONE failures=0
```

## Verdict: the batch didn't cause it, and there's no bisect and no SYS-25
- I couldn't reproduce it. Both commits pass, and the batch (807511d..b724bdc: f00aab3, e9bf6c9, 2f989e1, e3d9a78, b5a45ad, b724bdc) doesn't touch `godot/scripts/` (3 files, +100/−9, in the scene, data and docs). No script changed, so there was nothing to bisect.
- Likely cause: a timing-sensitive test threshold. `_process` rotates the starfield by `STARFIELD_ROT_SPEED * delta` (TAU/240 = 0.0262 rad/s). The check (preface_playable_area.gd:7782) samples `rotation.x` 90 frames apart and needs `> 0.04`. That's about 1.53 s of wall time, and 90 frames at 60 fps is 1.50 s. So the pass margin is about 1–5%, and it depends on frame pacing: vsync/refresh rate, how fast the machine is, and capture stalls. Gage's 0.039 rad is 90 frames at roughly 61 fps. Older logs (context/reticle_stars_doors_qa_log.md) showed 0.071–0.072 rad back when frames were slower.
- Suggested fix for Gage/Patch (test only): measure the elapsed `_time` and assert `d_star_rot ≈ STARFIELD_ROT_SPEED * dt` (±10%), or lower the threshold to something like 0.02, or wait a fixed time instead of 90 frames.
