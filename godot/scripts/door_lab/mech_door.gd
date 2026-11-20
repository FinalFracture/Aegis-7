class_name MechDoor
extends Node3D
## Reusable mechanical door. Pose comes from MechDoorProfile.sample() every
## physics tick so the leaf, its AnimatableBody3D and the mesh (a child of that
## body, or a GLB pivot that owns the body) stay on one timeline.
## Obstruction re-plans from the current q and velocity. It does not play a
## baked clip backwards.

signal state_changed(state_name: String)
signal phase_changed(phase_name: String)
signal cue(cue_name: String)

const ACTOR := "door_lab_actor"
const PROBE := "door_lab_obstruction"
const CAPSULE_DIAMETER := 0.70
const CLEAR_FIT := 0.80

@export var profile: MechDoorProfile
@export var locked: bool = false

var door_id: String = ""
var state: String = "closed"
var phase: String = "idle"
var lamp: String = "closed"
var motion_t: float = 0.0
var direction: String = "open"
var q_now: Array[float] = []
var v_now: Array[float] = []
var trigger_radius: float = 1.0
var cycle_hold_s: float = -1.0
var fault_hits: int = 0
var collider_enabled: bool = true
var record: bool = false
var rows: Array = []
var sim_t: float = 0.0

var _leaves: Array = []
var _hinge: bool = false
var _area: Area3D
var _lamp_mat: StandardMaterial3D
var _lamp_light: OmniLight3D
var _lamp_segs: Array = []
var _shown_color := Color(1, 0.584, 0)
var _shown_energy := 0.6
var _target_color := Color(1, 0.584, 0)
var _target_energy := 0.6
var _open_age: float = 0.0
var _hold_left: float = 0.0
var _brake_t: float = 0.0
var _brake_q: Array[float] = []
var _brake_v: Array[float] = []
var _dwell_left: float = 0.0
var _reopen_from: Array[float] = []
var _reopen_t: float = 0.0
var _reopen_scale: float = 1.0
var _stall: bool = false
var _cue_i: int = 0
var _played: Dictionary = {}
var _interact_held: float = 0.0
var _hw: Array = []
var _approach_axis := Vector3(0, 0, -1)
var _sensor: ShapeCast3D
var _block_sensor: Area3D
var _prev_phase: String = ""
var _open_since_clear: bool = false
var _leaf_phase: Array[String] = []
var _sensor_pos := Vector3(0.0, 1.15, 0.0)
var _sensor_size := Vector3(1.2, 2.0, 0.6)


func bind(p: MechDoorProfile, leaves: Array, hinge: bool) -> void:
	profile = p
	profile.load_table()
	door_id = profile.door_id
	_hinge = hinge
	_leaves = leaves
	q_now.resize(leaves.size())
	v_now.resize(leaves.size())
	_leaf_phase.resize(leaves.size())
	for i in leaves.size():
		q_now[i] = 0.0
		v_now[i] = 0.0
		_leaf_phase[i] = "idle"
	name = "Door_" + door_id
	add_to_group("mech_door")
	trigger_radius = profile.trigger_radius(5.2)
	_cache_hardware()
	_ensure_sensor()
	_ensure_cues()
	_apply_all(0.0, "open")
	_set_lamp("locked" if locked else "closed", true)
	_set_state("closed")


func set_approach(axis: Vector3) -> void:
	_approach_axis = axis.normalized()


func attach_proximity(area: Area3D) -> void:
	_area = area


func attach_lamp(mat: StandardMaterial3D, light: OmniLight3D, segs: Array) -> void:
	_lamp_mat = mat
	_lamp_light = light
	_lamp_segs = segs
	_set_lamp("locked" if locked else "closed", true)


func attach_sensor(cast: ShapeCast3D) -> void:
	_sensor = cast


func configure_sensor(local_pos: Vector3, size: Vector3) -> void:
	_sensor_pos = local_pos
	_sensor_size = size
	if _sensor != null and _sensor.shape is BoxShape3D:
		(_sensor.shape as BoxShape3D).size = size
		_sensor.position = local_pos


func set_locked(on: bool) -> void:
	locked = on
	if locked and (state == "closed" or state == "settled"):
		_set_lamp("locked", false)
		_set_state("closed")


func reset_closed() -> void:
	state = "closed"
	direction = "open"
	motion_t = 0.0
	fault_hits = 0
	_stall = false
	_cue_i = 0
	_played.clear()
	_interact_held = 0.0
	_hold_left = 0.0
	_open_age = 0.0
	for i in _leaves.size():
		q_now[i] = 0.0
		v_now[i] = 0.0
		if i < _leaf_phase.size():
			_leaf_phase[i] = "idle"
	_apply_all(0.0, "open")
	_set_colliders(true)
	_set_lamp("locked" if locked else "closed", true)
	_set_state("closed")
	phase = "idle"
	rows.clear()


func force_q(q: float) -> void:
	for i in _leaves.size():
		q_now[i] = q
		v_now[i] = 0.0
		_pose_leaf(i, q)
	_sync_bodies()


func command_open() -> void:
	if locked:
		_set_lamp("locked", false)
		return
	if state == "opening" or state == "open":
		return
	_begin_open()


func command_close() -> void:
	if state == "closed" or state == "closing":
		return
	_begin_close()


func _physics_process(delta: float) -> void:
	pump(delta)


func pump(delta: float) -> void:
	if profile == null or _leaves.is_empty():
		return
	sim_t += delta
	_poll_triggers(delta)
	_place_sensor()
	match state:
		"opening":
			_tick_profile("open", delta)
			if _obstruction_hit() and door_id == "bay3" and _approach_blocked():
				_stall = true
				state = "stalled"
				_set_state("stalled")
				# A stall is a hold, not the 3-strike fault lamp.
				_set_lamp("moving", false)
		"closing":
			_tick_profile("close", delta)
			if _obstruction_hit():
				_begin_brake()
		"braking":
			_tick_brake(delta)
		"dwell":
			_dwell_left -= delta
			if _dwell_left <= 0.0:
				_begin_reopen()
		"reopening":
			_tick_reopen(delta)
		"stalled":
			if not _obstruction_hit():
				_stall = false
				state = "opening"
				_set_state("opening")
				_set_lamp("moving", false)
		"open":
			_open_age += delta
			if _open_age > 3.0 and lamp == "open":
				_target_energy = 0.4
			_hold_left -= delta
			if _zone_occupied() or locked:
				_hold_left = _hold_seconds()
			elif _hold_left <= 0.0 and not profile.interact:
				_begin_close()
			elif profile.interact and _hold_left <= 0.0:
				_begin_close()
		"fault":
			pass
		"closed":
			pass
	_place_sensor()
	_update_collider_window()
	_log_tick(delta)
	_fade_lamp(delta)


func _process(delta: float) -> void:
	_chase(delta)


func _poll_triggers(delta: float) -> void:
	if locked:
		if state == "closed":
			_set_lamp("locked", false)
		_interact_held = 0.0
		return
	if profile.interact:
		if state == "closed" or state == "open":
			var actor := _nearest_actor()
			var held := Input.is_action_pressed("interact")
			if actor != null and held:
				var d := actor.global_position.distance_to(global_position + Vector3(0, 1.1, 0))
				if d <= 2.8:
					_interact_held += delta
					if _interact_held >= 0.2 and state == "closed":
						_begin_open()
					elif _interact_held >= 0.2 and state == "open":
						_begin_close()
						_interact_held = 0.0
				else:
					_interact_held = 0.0
			else:
				_interact_held = 0.0
		return
	if state == "closed" and _zone_occupied():
		_begin_open()
	elif state == "open" and _zone_occupied():
		_hold_left = _hold_seconds()


func _zone_occupied() -> bool:
	if _area == null:
		return false
	for b in _area.get_overlapping_bodies():
		if b is Node and (b as Node).is_in_group(ACTOR):
			return true
	return false


func _nearest_actor() -> Node3D:
	var best: Node3D = null
	var best_d := 1000.0
	var tree := get_tree()
	if tree == null:
		return null
	for n in tree.get_nodes_in_group(ACTOR):
		if n is Node3D:
			var d := (n as Node3D).global_position.distance_to(global_position)
			if d < best_d:
				best_d = d
				best = n as Node3D
	return best


func _hold_seconds() -> float:
	if cycle_hold_s >= 0.0:
		return cycle_hold_s
	return profile.hold_open_s


func _begin_open() -> void:
	direction = "open"
	motion_t = 0.0
	_cue_i = 0
	_played.clear()
	_stall = false
	state = "opening"
	_set_state("opening")
	# Amber until the first latch / equalize / dog. Cyan is that event, not the request.
	if profile.mech_event_open <= 0.001:
		_set_lamp("moving", false)
	phase = "request"
	_emit_phase("request")


func _begin_close() -> void:
	direction = "close"
	motion_t = 0.0
	_cue_i = 0
	_played.clear()
	state = "closing"
	_set_state("closing")
	_set_lamp("moving", false)
	phase = "prewarn"
	_emit_phase("prewarn")


func _tick_profile(dir: String, delta: float) -> void:
	motion_t += delta
	var stagger_key := "stagger_open" if dir == "open" else "stagger_close"
	var max_end := 0.0
	var phase_now := "settled"
	for i in _leaves.size():
		var leaf: Dictionary = _leaves[i]
		var st := float(leaf.get(stagger_key, 0.0))
		var lt := motion_t - st
		var s: Dictionary = profile.sample(dir, lt)
		var q := float(s["q"])
		var vel := float(s["vel"])
		v_now[i] = vel
		q_now[i] = q
		if i < _leaf_phase.size():
			_leaf_phase[i] = str(s["phase"]) if lt >= 0.0 else "wait"
		_pose_leaf(i, q)
		if lt >= 0.0:
			phase_now = str(s["phase"])
		var end_t := st + profile.duration(dir)
		if end_t > max_end:
			max_end = end_t
	_sync_bodies()
	_fire_cues(dir)
	if phase_now != phase:
		phase = phase_now
		_emit_phase(phase)
	_drive_hardware(dir)
	if dir == "open" and motion_t + 1.0e-5 >= profile.mech_event_open and lamp != "moving" and lamp != "open" and lamp != "fault":
		_set_lamp("moving", false)
	if motion_t >= max_end - 1.0e-4:
		if dir == "open":
			state = "open"
			_open_age = 0.0
			_hold_left = _hold_seconds()
			_set_state("open")
			_set_lamp("open", false)
			phase = "settled"
			_emit_phase("settled")
		else:
			for i in _leaves.size():
				q_now[i] = 0.0
				v_now[i] = 0.0
				_pose_leaf(i, 0.0)
			_sync_bodies()
			fault_hits = 0
			state = "closed"
			_set_state("closed")
			_set_lamp("locked" if locked else "closed", false)
			phase = "idle"
			_emit_phase("idle")


func _fire_cues(dir: String) -> void:
	var list: Array = profile.cues(dir)
	while _cue_i < list.size():
		var c: Dictionary = list[_cue_i]
		if motion_t + 1.0e-5 < float(c["t"]):
			break
		var nm := str(c["name"])
		if not _played.has(nm):
			_played[nm] = true
			cue.emit(nm)
			_blip(nm)
		_cue_i += 1


func _blip(nm: String) -> void:
	var player := get_node_or_null("Cue_" + nm) as AudioStreamPlayer3D
	if player == null or player.stream == null:
		return
	player.play()


func _pose_leaf(i: int, q: float) -> void:
	var leaf: Dictionary = _leaves[i]
	var sign := float(leaf["sign"])
	var body: AnimatableBody3D = leaf["body"]
	if _hinge:
		body.rotation = Vector3(0.0, deg_to_rad(sign * q), 0.0)
	else:
		var rest: Vector3 = leaf["rest"]
		var axis: Vector3 = leaf["axis"]
		body.position = rest + axis * (sign * q)


func _sync_bodies() -> void:
	for leaf in _leaves:
		var body: AnimatableBody3D = leaf["body"]
		if body == null or not body.is_inside_tree():
			continue
		# Reassert static. AnimatableBody3D is constructed kinematic, and that
		# mode defers body_set_state until the next physics flush.
		PhysicsServer3D.body_set_mode(body.get_rid(), PhysicsServer3D.BODY_MODE_STATIC)
		PhysicsServer3D.body_set_state(body.get_rid(), PhysicsServer3D.BODY_STATE_TRANSFORM, body.global_transform)


func _apply_all(t: float, dir: String) -> void:
	for i in _leaves.size():
		var s: Dictionary = profile.sample(dir, t)
		q_now[i] = float(s["q"])
		_pose_leaf(i, q_now[i])
	_sync_bodies()


func _obstruction_hit() -> bool:
	if _sensor == null or not collider_enabled:
		return false
	_sensor.force_shapecast_update()
	if not _sensor.is_colliding():
		return false
	var n := _sensor.get_collision_count()
	for i in n:
		var hit := _sensor.get_collider(i)
		if hit is Node:
			var node := hit as Node
			if node.is_in_group(ACTOR) or node.is_in_group(PROBE):
				return true
	return false


func _approach_blocked() -> bool:
	return _obstruction_hit()


func _begin_brake() -> void:
	_brake_t = 0.0
	_brake_q = q_now.duplicate()
	_brake_v = v_now.duplicate()
	state = "braking"
	_set_state("braking")
	phase = "obstruction_brake"
	_emit_phase(phase)
	_set_lamp("moving", false)


func _tick_brake(delta: float) -> void:
	_brake_t += delta
	var spec: Dictionary = profile.obstruction
	var stop_s := float(spec.get("stop_s", 0.2))
	var stop_dist := float(spec.get("stop_dist", 0.06))
	var all_stopped := true
	for i in _leaves.size():
		var v := float(v_now[i])
		var q := float(q_now[i])
		if absf(v) < 1.0e-3:
			v_now[i] = 0.0
			_pose_leaf(i, q)
			continue
		all_stopped = false
		var a := absf(v) / maxf(stop_s - _brake_t + delta, delta)
		var cap_a := float(spec.get("stop_a", 0.0))
		if cap_a > 0.0:
			a = cap_a
		var step := clampf(a * delta, 0.0, absf(v))
		var nv := v - signf(v) * step
		var nq := q + v * delta
		if absf(nq - float(_brake_q[i])) > stop_dist:
			nq = float(_brake_q[i]) + signf(v) * stop_dist
			nv = 0.0
		_brake_v[i] = nv
		q_now[i] = nq
		v_now[i] = nv
		_pose_leaf(i, nq)
		if absf(nv) > 1.0e-3:
			all_stopped = false
	_sync_bodies()
	if all_stopped or _brake_t >= stop_s:
		for i in _leaves.size():
			v_now[i] = 0.0
			_brake_v[i] = 0.0
		_dwell_left = float(spec.get("dwell_s", 0.15))
		state = "dwell"
		_set_state("dwell")
		phase = "obstruction_dwell"
		_emit_phase(phase)


func _begin_reopen() -> void:
	fault_hits += 1
	var spec: Dictionary = profile.obstruction
	var limit := int(spec.get("fault_count", 3))
	if fault_hits >= limit:
		state = "fault"
		_set_state("fault")
		_set_lamp("fault", false)
		phase = "fault"
		_emit_phase("fault")
		# Hatch holds the last safe pose. Others stay open (current or full).
		if door_id != "hatch":
			for i in _leaves.size():
				q_now[i] = profile.travel
				_pose_leaf(i, profile.travel)
			_sync_bodies()
		return
	_reopen_from = q_now.duplicate()
	_reopen_t = 0.0
	var cap := float(spec.get("v_cap", 0.0))
	var peak := profile.v_peak_open
	_reopen_scale = 1.0
	if cap > 0.0 and peak > cap:
		_reopen_scale = peak / cap
	state = "reopening"
	_set_state("reopening")
	_set_lamp("moving", false)
	phase = "reopen"
	_emit_phase("reopen")


func _tick_reopen(delta: float) -> void:
	_reopen_t += delta
	var spec: Dictionary = profile.obstruction
	var target := profile.travel
	if door_id == "hatch":
		target = maxf(float(spec.get("reopen_to", 30.0)), 30.0)
		# Keep opening past 30° while the body is still in the sweep so the
		# leaf cannot stop on top of the capsule. 30° is the minimum safe pose.
		if _obstruction_hit():
			target = profile.travel
	var dur := maxf(0.35, profile.duration("open") * 0.45 * _reopen_scale)
	var u := clampf(_reopen_t / dur, 0.0, 1.0)
	# Raised cosine. Starts and ends at v = 0, no linear segment.
	var s := 0.5 - 0.5 * cos(PI * u)
	var done := true
	for i in _leaves.size():
		var a := float(_reopen_from[i])
		var q := lerpf(a, target, s)
		var vel := (target - a) * (0.5 * PI * sin(PI * u)) / dur
		q_now[i] = q
		v_now[i] = vel
		_pose_leaf(i, q)
		if u < 1.0:
			done = false
	_sync_bodies()
	if done or u >= 1.0:
		_open_age = 0.0
		_hold_left = float(spec.get("hold_s", profile.hold_open_s))
		if cycle_hold_s >= 0.0:
			_hold_left = cycle_hold_s
		state = "open"
		_set_state("open")
		_set_lamp("open", false)
		phase = "settled"
		_emit_phase("settled")


func _update_collider_window() -> void:
	var any_on := false
	for i in _leaves.size():
		var ph := _leaf_phase[i] if i < _leaf_phase.size() else phase
		var q := q_now[i] if i < q_now.size() else 0.0
		var allow_off := false
		if state == "closing" and profile.clear_gap(q) < CLEAR_FIT:
			if ph == "creep" or ph == "latch" or ph == "latch_check" or ph == "final_seat" or ph == "backcheck" or ph.begins_with("latch"):
				allow_off = true
		var on := not allow_off
		var body: AnimatableBody3D = _leaves[i]["body"]
		body.collision_layer = 1 if on else 0
		body.collision_mask = 1 if on else 0
		if on:
			any_on = true
	collider_enabled = any_on


func _set_colliders(on: bool) -> void:
	collider_enabled = on
	for leaf in _leaves:
		var body: AnimatableBody3D = leaf["body"]
		body.collision_layer = 1 if on else 0
		body.collision_mask = 1 if on else 0


func _gap_now() -> float:
	var q := 0.0
	if q_now.size() > 0:
		q = q_now[0]
		for v in q_now:
			q = minf(q, v)
	return profile.clear_gap(q)


func _set_state(s: String) -> void:
	state = s
	state_changed.emit(s)


func _emit_phase(p: String) -> void:
	if p == _prev_phase:
		return
	_prev_phase = p
	phase_changed.emit(p)


func _set_lamp(mode: String, instant: bool) -> void:
	if lamp == mode and not instant:
		return
	lamp = mode
	match mode:
		"locked":
			_target_color = Color("#FF2A2A")
			_target_energy = 0.8
		"closed":
			_target_color = Color("#FF9500")
			_target_energy = 0.6
		"moving":
			_target_color = Color("#00E5FF")
			_target_energy = 0.9
		"open":
			_target_color = Color("#3FAF6A")
			_target_energy = 0.7
		"fault":
			_target_color = Color("#FF2A2A")
			_target_energy = 1.0
	if instant:
		_shown_color = _target_color
		_shown_energy = _target_energy
		_paint_lamp()


func _fade_lamp(delta: float) -> void:
	if lamp == "fault":
		var blink := sin(TAU * 2.0 * Time.get_ticks_msec() / 1000.0) > 0.0
		_target_color = Color("#FF2A2A") if blink else Color("#FF9500")
		_target_energy = 1.0
	var k := clampf(delta / 0.15, 0.0, 1.0)
	_shown_color = _shown_color.lerp(_target_color, k)
	_shown_energy = lerpf(_shown_energy, _target_energy, k)
	_paint_lamp()


func _paint_lamp() -> void:
	if _lamp_mat != null:
		_lamp_mat.emission_enabled = true
		_lamp_mat.emission = _shown_color
		_lamp_mat.emission_energy_multiplier = _shown_energy
		# Status hue stays in the emission. Albedo is capped at 0.90.
		var c := _shown_color
		_lamp_mat.albedo_color = Color(minf(c.r, 0.90), minf(c.g, 0.90), minf(c.b, 0.90), c.a)
	if _lamp_light != null:
		_lamp_light.light_color = _shown_color
		_lamp_light.light_energy = 0.15
		_lamp_light.omni_range = 0.6


func _chase(delta: float) -> void:
	if _lamp_segs.is_empty():
		return
	var moving := lamp == "moving" or state == "closing" or state == "opening" or state == "reopening"
	var n := _lamp_segs.size()
	var head := 0
	if moving:
		var dir := 1.0 if state == "opening" or state == "reopening" else -1.0
		var u := fposmod(Time.get_ticks_msec() / 400.0 * dir, 1.0)
		head = int(u * n) % n
	for i in n:
		var seg: MeshInstance3D = _lamp_segs[i]
		var mat := seg.get_surface_override_material(0) as StandardMaterial3D
		if mat == null:
			continue
		var on := (not moving) or i == head or i == (head + n - 1) % n
		mat.emission_energy_multiplier = _shown_energy if on else _shown_energy * 0.15
		mat.emission = _shown_color


func _cache_hardware() -> void:
	_hw.clear()
	var stack: Array[Node] = [self]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if n.has_meta("door_hw"):
			_hw.append(n)


func _drive_hardware(dir: String) -> void:
	var q := q_now[0] if q_now.size() else 0.0
	var span := maxf(profile.travel, 0.001)
	var u := clampf(q / span, 0.0, 1.0)
	for n in _hw:
		var kind := str(n.get_meta("door_hw"))
		if kind == "roller" and n is Node3D:
			var r := float(n.get_meta("roller_r", 0.03))
			var spins := (q / maxf(r, 0.005))
			(n as Node3D).rotation.x = spins
		elif kind == "dog" and n is Node3D:
			var local_t := _phase_u(["dogs"])
			var st := float(n.get_meta("stagger", 0.0))
			var du := clampf((local_t - st) / 0.55, 0.0, 1.0)
			if dir == "close":
				du = 1.0 - du
			var rest: Vector3 = n.get_meta("rest")
			var retract: Vector3 = n.get_meta("retract")
			(n as Node3D).position = rest + retract * du
		elif kind == "wheel" and n is Node3D:
			var du2 := _phase_u(["dogs"])
			if dir == "close":
				du2 = 1.0 - du2
			(n as Node3D).rotation.z = deg_to_rad(-90.0 * du2)
		elif kind == "needle" and n is Node3D:
			var eu := _phase_u(["equalize"])
			(n as Node3D).rotation.z = deg_to_rad(-70.0 * (1.0 - eu))
		elif kind == "seal" and n is Node3D:
			var deflated := _phase_u(["seal_deflate", "seal_unseat"])
			if dir == "close":
				deflated = 1.0 - _phase_u(["seal_inflate", "creep"])
			var sc := lerpf(1.0, 0.72, clampf(deflated, 0.0, 1.0))
			(n as Node3D).scale = Vector3(sc, 1.0, sc)
		elif kind == "rod" and n is Node3D:
			_stretch_rod(n as Node3D)


func _phase_u(names: Array) -> float:
	var src := "open" if direction != "close" else "close"
	var saw := false
	var after := true
	for nm in names:
		var sp := profile.phase_span(src, str(nm))
		if sp.x < 0.0:
			continue
		saw = true
		if motion_t < sp.x - 1.0e-4:
			after = false
			continue
		if motion_t <= sp.y + 1.0e-4:
			return clampf((motion_t - sp.x) / maxf(sp.y - sp.x, 1.0e-4), 0.0, 1.0)
	if not saw:
		return 0.0
	return 1.0 if after else 0.0


func _name_in(nm: String, names: Array) -> bool:
	for w in names:
		if nm == str(w) or nm.begins_with(str(w)):
			return true
	return false


func _stretch_rod(rod: Node3D) -> void:
	var a := rod.get_node_or_null("AnchorA") as Node3D
	var b := rod.get_node_or_null("AnchorB") as Node3D
	if rod.has_meta("anchor_a") and rod.get_meta("anchor_a") is Node3D:
		a = rod.get_meta("anchor_a")
	if rod.has_meta("anchor_b") and rod.get_meta("anchor_b") is Node3D:
		b = rod.get_meta("anchor_b")
	var mesh := rod.get_node_or_null("Mesh") as MeshInstance3D
	if a == null or b == null or mesh == null:
		return
	var pa := a.global_position
	var pb := b.global_position
	var mid := (pa + pb) * 0.5
	var d := pa.distance_to(pb)
	rod.global_position = mid
	if d > 1.0e-4:
		rod.look_at(pb, Vector3.UP)
	mesh.scale = Vector3(1.0, 1.0, maxf(d, 0.01))


func _log_tick(_delta: float) -> void:
	if not record:
		return
	var drift := _drift()
	var gap := _gap_now() * 1000.0
	# AnimatableBody3D has no contact monitor. Snag checks use the player's slide contacts.
	var contacts := 0
	for i in _leaves.size():
		var leaf: Dictionary = _leaves[i]
		var body: AnimatableBody3D = leaf["body"]
		var o := body.global_position
		rows.append({
			"t": sim_t,
			"motion_t": motion_t,
			"phase": _leaf_phase[i] if i < _leaf_phase.size() else phase,
			"leaf": str(leaf["name"]),
			"px": o.x, "py": o.y, "pz": o.z,
			"q": q_now[i],
			"yaw": body.rotation_degrees.y,
			"vel": v_now[i],
			"drift_mm": drift * 1000.0,
			"gap_mm": gap,
			"contacts": contacts,
			"lamp": lamp,
			"collider": 1 if body.collision_layer != 0 else 0,
			"state": state,
		})


func _drift() -> float:
	var worst := 0.0
	for leaf in _leaves:
		var body: AnimatableBody3D = leaf["body"]
		if not body.is_inside_tree():
			continue
		var phys: Transform3D = PhysicsServer3D.body_get_state(body.get_rid(), PhysicsServer3D.BODY_STATE_TRANSFORM)
		worst = maxf(worst, phys.origin.distance_to(body.global_position))
		var pivot: Node3D = leaf["pivot"]
		worst = maxf(worst, pivot.global_position.distance_to(body.global_position))
	return worst


func drift_mm() -> float:
	return _drift() * 1000.0


func _ensure_sensor() -> void:
	_sensor = ShapeCast3D.new()
	_sensor.name = "SweepSensor"
	var box := BoxShape3D.new()
	box.size = Vector3(0.7, 1.7, 0.55) if _hinge else Vector3(1.6, 2.1, 0.5)
	if door_id == "hatch":
		box.size = Vector3(0.7, 1.7, 0.5)
	elif door_id == "pocket":
		box.size = Vector3(1.7, 2.1, 0.45)
	elif door_id == "pair":
		box.size = Vector3(1.5, 2.1, 0.5)
	_sensor.shape = box
	_sensor.target_position = Vector3(0, 0, 0.02)
	_sensor.collision_mask = 1
	_sensor.collide_with_areas = false
	_sensor.collide_with_bodies = true
	_sensor.enabled = false
	add_child(_sensor)
	for leaf in _leaves:
		_sensor.add_exception(leaf["body"])


func _place_sensor() -> void:
	if _sensor == null:
		return
	var watch := state == "closing" or state == "braking" or state == "dwell" or state == "reopening"
	if state == "opening" and door_id == "bay3":
		watch = true
	_sensor.enabled = watch
	if not watch:
		return
	_sensor.position = _sensor_pos


func _ensure_cues() -> void:
	var seen := {}
	for direction in ["open", "close"]:
		for c in profile.cues(direction):
			var nm := str(c["name"])
			if seen.has(nm):
				continue
			seen[nm] = true
			var p := AudioStreamPlayer3D.new()
			p.name = "Cue_" + nm
			p.unit_size = 2.0
			add_child(p)


func drift_deg() -> float:
	var worst := 0.0
	for leaf in _leaves:
		var body: AnimatableBody3D = leaf["body"]
		if not body.is_inside_tree():
			continue
		var phys: Transform3D = PhysicsServer3D.body_get_state(body.get_rid(), PhysicsServer3D.BODY_STATE_TRANSFORM)
		worst = maxf(worst, rad_to_deg(phys.basis.get_rotation_quaternion().angle_to(body.global_basis.get_rotation_quaternion())))
	return worst
