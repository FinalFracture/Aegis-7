# pcb_validate.py — PCB art validator (Sloane)

Checks routed board-art geometry (JSON) for electrical sanity before UI/texture art ships.

```
python3 tools/pcb_validate.py board_geom.json [more.json ...]
```
or `from pcb_validate import validate; report = validate(geom_dict)` → `{"ok", "errors", "expected_opens", "stats"}`.

**Checks:** per-net connectivity (union-find over pads, vias, traces, GND pours), shorts, unconnected pads, dangling trace ends/stubs, same-layer clearance between different nets (default 0.25 grid units, incl. trace-pad and pad-pad), floating pour islands, bend angles (45° multiples only, never acute).

**Geometry schema** (see docstring): `pads[{id,net,x,y,r}]`, `vias[{net,x,y,r}]` (pads/vias are through-hole, both layers), `traces[{net,layer,w,pts}]`, `pours[{net,layer,cell,cells}]`, `expected_open[{net,gap,groups}]` for intentional gameplay faults (e.g. the cracked RESET_N trace), `clearance`.

Used for `design/ui/troubleshoot_final/` (report: `validation_report.md`).

**Intentional no-connects (optional):** `intentional_unconnected[{pad,reason}]` declares pads that are deliberately left unrouted (e.g. the player-drawn DOOR MOTOR input in `design/ui/troubleshoot_simple_r2/`). They are listed under `intentional_nc` instead of raising `UNCONNECTED PAD`. Files without the key behave exactly as before.
