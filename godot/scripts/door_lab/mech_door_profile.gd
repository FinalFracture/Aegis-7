class_name MechDoorProfile
extends Resource
## One profile per door type. Numbers live in the JSON table (table_path).
##
## Jared 2026-11-20 13:50 CT game tempo. Leaf travel uses travel_time_scale
## (0.45). Latch, seal, dog, equalize, and the control gaps use mech_phase_scale
## (0.60). Lurch and settle stay at 1.00. A close leaf whose 0.45x speed would
## exceed 10 J is either close_travel_scale 0.60 or a speed cap (close_v_cap)
## with the 0.45-scaled accel and jerk, so the cruise just gets longer.

@export var door_id: String = ""
@export var table_path: String = ""
@export var travel_time_scale: float = 0.45

var motion: String = "slide"
var travel: float = 1.0
var mass_kg: float = 1.0
var inertia_kgm2: float = 0.0
var v_peak_open: float = 1.0
var v_peak_close: float = 1.0
var hold_open_s: float = 3.0
var pre_equalized: bool = false
var interact: bool = false
var full_clear_m: float = 1.0
var clear_model: String = "slide"
var obstruction: Dictionary = {}
var leaves: Array = []
var meta: Dictionary = {}
var mech_phase_scale: float = 0.60
var lurch_scale: float = 1.0
var settle_scale: float = 1.0
var close_travel_scale: float = 0.45
var close_v_cap: float = 0.0
var expect_open: float = 0.0
var expect_close: float = 0.0
var source: String = ""

var _raw_open: Array = []
var _raw_close: Array = []
var _open: Array = []
var _close: Array = []
var _cues_open: Array = []
var _cues_close: Array = []
var _ready_ok: bool = false
var open_duration: float = 0.0
var close_duration: float = 0.0
var mech_event_open: float = 0.0
var green_open: float = 0.0


func load_table() -> void:
	if _ready_ok:
		return
	var path := table_path
	if path == "":
		push_error("MechDoorProfile %s has no table_path" % door_id)
		return
	if not FileAccess.file_exists(path):
		push_error("MechDoorProfile missing %s" % path)
		return
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("MechDoorProfile bad JSON %s" % path)
		return
	var data: Dictionary = parsed
	if str(data.get("door_id", door_id)) != "" and door_id == "":
		door_id = str(data["door_id"])
	motion = str(data.get("motion", "slide"))
	travel = float(data.get("travel", 1.0))
	mass_kg = float(data.get("mass_kg", 1.0))
	inertia_kgm2 = float(data.get("inertia_kgm2", 0.0))
	v_peak_open = float(data.get("v_peak_open", 1.0))
	v_peak_close = float(data.get("v_peak_close", 1.0))
	hold_open_s = float(data.get("hold_open_s", 3.0))
	pre_equalized = bool(data.get("pre_equalized", false))
	interact = bool(data.get("interact", false))
	full_clear_m = float(data.get("full_clear_m", 1.0))
	clear_model = str(data.get("clear_model", "slide"))
	obstruction = data.get("obstruction", {})
	leaves = data.get("leaves", [])
	meta = data.get("meta", {})
	# The JSON table is the timing authority the .tres points at.
	travel_time_scale = float(data.get("travel_time_scale", travel_time_scale))
	mech_phase_scale = float(data.get("mech_phase_scale", 0.60))
	lurch_scale = float(data.get("lurch_scale", 1.0))
	settle_scale = float(data.get("settle_scale", 1.0))
	close_travel_scale = float(data.get("close_travel_scale", travel_time_scale))
	close_v_cap = float(data.get("close_v_cap", 0.0))
	expect_open = float(data.get("expect_open", 0.0))
	expect_close = float(data.get("expect_close", 0.0))
	_raw_open = data.get("open_phases", [])
	_raw_close = data.get("close_phases", [])
	_open = _compile(_raw_open, "open")
	_close = _compile(_raw_close, "close")
	open_duration = float(_open[_open.size() - 1]["rt1"]) if _open.size() else 0.0
	close_duration = float(_close[_close.size() - 1]["rt1"]) if _close.size() else 0.0
	_cues_open = _map_cues(data.get("cues_open", []), _raw_open, _open)
	_cues_close = _map_cues(data.get("cues_close", []), _raw_close, _close)
	mech_event_open = _first_mech(_open)
	green_open = open_duration
	source = "tres"
	_ready_ok = true


func compiled_phases(direction: String) -> Array:
	return _open if direction == "open" else _close


func phase_at(direction: String, t: float) -> Dictionary:
	var src: Array = _open if direction == "open" else _close
	if src.is_empty():
		return {}
	if t <= 0.0:
		return src[0]
	for ph in src:
		if t <= float(ph["rt1"]) + 1.0e-8:
			return ph
	return src[src.size() - 1]


func phase_order(direction: String) -> PackedStringArray:
	var src: Array = _open if direction == "open" else _close
	var names := PackedStringArray()
	var seen := {}
	for ph in src:
		var nm := str(ph["name"])
		if ph["kind"] == "scurve":
			for sub in ["accel", "cruise", "decel"]:
				if not seen.has(sub) and not names.has(sub):
					names.append(sub)
					seen[sub] = true
		else:
			if not seen.has(nm):
				names.append(nm)
				seen[nm] = true
	return names


func cues(direction: String) -> Array:
	return _cues_open if direction == "open" else _cues_close


## rt0, rt1 of the first compiled phase whose name equals or starts with `name_prefix`.
## (-1, -1) when the open or close table has no such phase.
func phase_span(direction: String, name_prefix: String) -> Vector2:
	var src: Array = _open if direction == "open" else _close
	for ph in src:
		var nm := str(ph["name"])
		if nm == name_prefix or nm.begins_with(name_prefix):
			return Vector2(float(ph["rt0"]), float(ph["rt1"]))
	return Vector2(-1.0, -1.0)


func duration(direction: String) -> float:
	return open_duration if direction == "open" else close_duration


func rest_q(direction: String) -> float:
	if direction == "open":
		return 0.0
	return travel


func sample(direction: String, t: float) -> Dictionary:
	var src: Array = _open if direction == "open" else _close
	if src.is_empty():
		return {"q": 0.0, "vel": 0.0, "phase": "idle"}
	if t <= 0.0:
		var q0 := float(src[0]["p0"])
		return {"q": q0, "vel": 0.0, "phase": str(src[0]["name"])}
	if t >= float(src[src.size() - 1]["rt1"]):
		var last: Dictionary = src[src.size() - 1]
		return {"q": _phase_end_q(last), "vel": 0.0, "phase": "settled"}
	for ph in src:
		if t < float(ph["rt0"]) - 1.0e-8:
			break
		if t <= float(ph["rt1"]) + 1.0e-8:
			return _eval_phase(ph, t)
	var tail: Dictionary = src[src.size() - 1]
	return {"q": _phase_end_q(tail), "vel": 0.0, "phase": "settled"}


func _phase_end_q(ph: Dictionary) -> float:
	if ph.has("p1"):
		return float(ph["p1"])
	return float(ph.get("p0", 0.0))


func clear_gap(q: float) -> float:
	if clear_model == "slide":
		if travel <= 0.0:
			return 0.0
		return full_clear_m * clampf(q / travel, 0.0, 1.0)
	var ang := deg_to_rad(clampf(q, 0.0, 180.0))
	return full_clear_m * (1.0 - cos(ang))


func t_open_to_clear(gap_m: float) -> float:
	var t := 0.0
	var step := 1.0 / 240.0
	while t < open_duration + 0.001:
		var s := sample("open", t)
		if clear_gap(float(s["q"])) >= gap_m - 1.0e-4:
			return t
		t += step
	return open_duration


func trigger_radius(walk_speed: float) -> float:
	if interact:
		return 0.0
	var stagger := 0.0
	for item in leaves:
		stagger = maxf(stagger, float(item.get("stagger_open", 0.0)))
	var t_clear := t_open_to_clear(0.80) + stagger
	# One walk tick of pad on top of the 0.85 m approach margin.
	var radius := walk_speed * t_clear + 0.85
	# Bay3 must cover the staggered last leaf. 9.95 m is the lab floor.
	if door_id == "bay3":
		radius = maxf(radius, 9.95)
	return radius


func _group_of(ph: Dictionary) -> String:
	if str(ph.get("group", "")) != "":
		return str(ph["group"])
	var name := str(ph.get("name", ""))
	var kind := str(ph.get("kind", ""))
	if kind == "settle" or name == "settle" or name.begins_with("settle"):
		return "settle"
	if "lurch" in name:
		return "lurch"
	if kind == "scurve" or kind == "cubic":
		return "travel"
	if name in ["travel", "creep", "backcheck", "latch_check", "final_seat"]:
		return "travel"
	return "mech"


func _k_for(group: String, direction: String) -> float:
	if group == "settle":
		return settle_scale
	if group == "lurch":
		return lurch_scale
	if group == "travel":
		if direction == "close":
			return close_travel_scale
		return travel_time_scale
	return mech_phase_scale


func _compile(raw: Array, direction: String) -> Array:
	var out: Array = []
	var cursor := 0.0
	var k_ref := maxf(travel_time_scale, 1.0e-4)
	for item in raw:
		var ph: Dictionary = item
		var dur := float(ph["t1"]) - float(ph["t0"])
		var group := _group_of(ph)
		var capped := direction == "close" and group == "travel" and str(ph.get("kind", "")) == "scurve" and close_v_cap > 0.0
		var k := 1.0 if capped else _k_for(group, direction)
		var c := ph.duplicate(true)
		c["group"] = group
		c["k"] = k
		c["time_scale"] = k
		c["vance_dur"] = dur
		c["capped"] = capped
		c["vance_v"] = float(ph.get("v", 0.0))
		c["vance_a"] = float(ph.get("a", 0.0))
		c["vance_j"] = float(ph.get("j", 0.0))
		c["a_prime"] = 0.0
		c["j_prime"] = 0.0
		c["v_prime"] = 0.0
		c["rt0"] = cursor
		var p0 := float(ph.get("p0", 0.0))
		var p1 := float(ph.get("p1", p0))
		var span := dur * k
		if str(ph.get("kind", "")) == "scurve":
			var dist := absf(p1 - p0)
			var v := float(ph["v"])
			var a := float(ph["a"])
			var j := float(ph["j"])
			if capped:
				var a_p := a / (k_ref * k_ref)
				var j_p := j / (k_ref * k_ref * k_ref)
				c["segs"] = _build_segs(dist, close_v_cap, a_p, j_p)
				c["a_prime"] = a_p
				c["j_prime"] = j_p
				c["v_prime"] = close_v_cap
				c["time_scale"] = 1.0
				c["k"] = 1.0
				span = _seg_dur(c["segs"])
			else:
				c["segs"] = _build_segs(dist, v, a, j)
				var kk := maxf(k, 1.0e-4)
				c["a_prime"] = a / (kk * kk)
				c["j_prime"] = j / (kk * kk * kk)
				c["v_prime"] = v / kk
			c["dist"] = dist
			c["sign"] = 1.0 if p1 >= p0 else -1.0
		elif str(ph.get("kind", "")) == "cubic" or str(ph.get("kind", "")) == "cosine":
			var D := maxf(span, 1.0e-6)
			var L := absf(p1 - p0)
			if str(ph.get("kind", "")) == "cubic":
				c["a_prime"] = 6.0 * L / (D * D)
				c["j_prime"] = 12.0 * L / (D * D * D)
				c["v_prime"] = 1.5 * L / D
			else:
				c["a_prime"] = 0.5 * PI * PI * L / (D * D)
				c["j_prime"] = 0.5 * PI * PI * PI * L / (D * D * D)
				c["v_prime"] = 0.5 * PI * L / D
		c["rt1"] = cursor + span
		c["dur"] = span
		out.append(c)
		cursor = float(c["rt1"])
	return out


func _seg_dur(segs: Array) -> float:
	var total := 0.0
	for s in segs:
		total += float(s["dur"])
	return total


func _build_segs(distance: float, v: float, a: float, j: float) -> Array:
	var segs: Array = []
	if distance <= 1.0e-8 or v <= 0.0 or a <= 0.0 or j <= 0.0:
		segs.append({"dur": 0.0, "jerk": 0.0, "name": "cruise"})
		return segs
	var tj := a / j
	var v_jerk := 0.5 * a * tj
	if 2.0 * v_jerk > v:
		tj = sqrt(v / j)
		v_jerk = 0.5 * j * tj * tj
		a = j * tj
	var t_ca := maxf(0.0, (v - 2.0 * v_jerk) / a)
	var t_acc := 2.0 * tj + t_ca
	var d_acc := v * t_acc * 0.5
	var t_c := 0.0
	if 2.0 * d_acc < distance:
		t_c = (distance - 2.0 * d_acc) / v
	else:
		t_c = 0.0
	segs.append({"dur": tj, "jerk": j, "name": "accel"})
	segs.append({"dur": t_ca, "jerk": 0.0, "name": "accel"})
	segs.append({"dur": tj, "jerk": -j, "name": "accel"})
	segs.append({"dur": t_c, "jerk": 0.0, "name": "cruise"})
	segs.append({"dur": tj, "jerk": -j, "name": "decel"})
	segs.append({"dur": t_ca, "jerk": 0.0, "name": "decel"})
	segs.append({"dur": tj, "jerk": j, "name": "decel"})
	return segs


func _eval_phase(ph: Dictionary, t: float) -> Dictionary:
	var kind := str(ph["kind"])
	var dur := maxf(float(ph["dur"]), 1.0e-6)
	var u := clampf((t - float(ph["rt0"])) / dur, 0.0, 1.0)
	var p0 := float(ph["p0"])
	var p1 := float(ph.get("p1", p0))
	if kind == "hold" or kind == "latch":
		return {"q": p0, "vel": 0.0, "phase": str(ph["name"])}
	if kind == "cosine":
		var s := 0.5 - 0.5 * cos(PI * u)
		var ds := 0.5 * PI * sin(PI * u)
		return {"q": lerpf(p0, p1, s), "vel": (p1 - p0) * ds / dur, "phase": str(ph["name"])}
	if kind == "cubic":
		var s2 := u * u * (3.0 - 2.0 * u)
		var ds2 := 6.0 * u * (1.0 - u)
		return {"q": lerpf(p0, p1, s2), "vel": (p1 - p0) * ds2 / dur, "phase": str(ph["name"])}
	if kind == "settle":
		var amp := float(ph.get("amp", 0.0))
		var travel_sign := float(ph.get("sign", 1.0))
		var hump := sin(PI * u)
		hump = hump * hump
		var dxdu := amp * PI * sin(2.0 * PI * u)
		return {
			"q": p1 + travel_sign * amp * hump,
			"vel": travel_sign * amp * dxdu / dur,
			"phase": str(ph["name"]),
		}
	if kind == "scurve":
		var sc := float(ph["time_scale"])
		var tu := (t - float(ph["rt0"])) / maxf(sc, 1.0e-6)
		var local := _eval_segs(ph["segs"], tu)
		var sgn := float(ph["sign"])
		return {
			"q": p0 + sgn * local.x,
			"vel": sgn * local.y / maxf(sc, 1.0e-6),
			"phase": local_name(ph, tu),
		}
	return {"q": p0, "vel": 0.0, "phase": str(ph["name"])}


func local_name(ph: Dictionary, tu: float) -> String:
	var acc_t := 0.0
	var segs: Array = ph["segs"]
	for s in segs:
		var sd: Dictionary = s
		var d := float(sd["dur"])
		if tu <= acc_t + d + 1.0e-6:
			return str(sd["name"])
		acc_t += d
	return "decel"


func _eval_segs(segs: Array, tu: float) -> Vector2:
	var tt := 0.0
	var p := 0.0
	var vel := 0.0
	var acc := 0.0
	for s in segs:
		var sd: Dictionary = s
		var d := float(sd["dur"])
		var jk := float(sd["jerk"])
		if tu <= tt + d + 1.0e-9:
			var h := maxf(0.0, tu - tt)
			var p2 := p + vel * h + 0.5 * acc * h * h + (1.0 / 6.0) * jk * h * h * h
			var v2 := vel + acc * h + 0.5 * jk * h * h
			return Vector2(p2, v2)
		var h2 := d
		var np := p + vel * h2 + 0.5 * acc * h2 * h2 + (1.0 / 6.0) * jk * h2 * h2 * h2
		var nv := vel + acc * h2 + 0.5 * jk * h2 * h2
		var na := acc + jk * h2
		p = np
		vel = nv
		acc = na
		tt += d
	return Vector2(p, vel)


func _map_cues(cues_in: Array, raw: Array, compiled: Array) -> Array:
	var out: Array = []
	for c in cues_in:
		var cd: Dictionary = c
		var tu := float(cd["t"])
		var mapped := tu
		var hit := false
		for i in range(raw.size()):
			var rp: Dictionary = raw[i]
			if tu >= float(rp["t0"]) - 1.0e-4 and tu <= float(rp["t1"]) + 1.0e-4:
				var cp: Dictionary = compiled[i]
				var sc := float(cp["k"]) if not bool(cp.get("capped", false)) else (float(cp["dur"]) / maxf(float(cp["vance_dur"]), 1.0e-6))
				if bool(cp.get("capped", false)):
					mapped = float(cp["rt0"]) + (tu - float(rp["t0"])) / maxf(float(rp["t1"]) - float(rp["t0"]), 1.0e-6) * float(cp["dur"])
				else:
					mapped = float(cp["rt0"]) + (tu - float(rp["t0"])) * sc
				hit = true
				break
		if not hit and raw.size() > 0 and compiled.size() > 0:
			var last_raw: Dictionary = raw[raw.size() - 1]
			var past := tu - float(last_raw["t1"])
			if past > 0.0 and past <= 0.05:
				var last_cp: Dictionary = compiled[compiled.size() - 1]
				mapped = float(last_cp["rt1"])
		out.append({"t": mapped, "name": str(cd["name"]), "loop": bool(cd.get("loop", false)), "stop": bool(cd.get("stop", false))})
	out.sort_custom(func(a, b): return float(a["t"]) < float(b["t"]))
	return out


func _first_mech(compiled: Array) -> float:
	for ph in compiled:
		var kind := str(ph["kind"])
		if kind == "latch" or str(ph["name"]).begins_with("equalize") or str(ph["name"]).begins_with("bolt") or str(ph["name"]).begins_with("strike") or str(ph["name"]).begins_with("dog"):
			return float(ph["rt0"])
	return 0.0
