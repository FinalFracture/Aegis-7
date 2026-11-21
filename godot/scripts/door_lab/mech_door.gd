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
var _fade_from_color := Color(1, 0.584, 0)
var _fade_from_energy := 0.6
var _fade_age := 0.15
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
var hinge_axis := Vector3(0, 1, 0)
var emergency := false
var klaxon_fired := false
var klaxon_count := 0
var gravity_g := 1.0
var delta_p := 0.0
var _klaxon_age := 100.0
var _reopen_dur: float = 0.35
var _log_prev_v: Array = []
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
	_drive_hardware("close", true)
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
	klaxon_fired = false
	klaxon_count = 0
	_klaxon_age = 100.0
	emergency = false
	delta_p = 0.0
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


func present_fault() -> void:
	force_q(profile.travel * 0.2)
	_set_lamp("fault", true)
	state = "fault"
	_set_state("fault")
	phase = "fault"


func force_q(q: float) -> void:
	for i in _leaves.size():
		q_now[i] = q
		v_now[i] = 0.0
		_pose_leaf(i, q)
	_sync_bodies()
	_drive_hardware("open" if q > 0.02 else "close", true)


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
		"closing":
			# Pressure rise above 2 kPa, not a script flag, starts the creep.
			if delta_p > 2.0 and _obstruction_hit():
				_emergency_creep(delta)
			else:
				_tick_profile("close", delta)
				if _obstruction_hit() and not emergency:
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
				_target_energy = 0.35
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
	# The row must show this tick's lamp, not the energy from the previous fade.
	_fade_lamp(delta)
	_log_tick(delta)


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
	var area_hit := false
	for b in _area.get_overlapping_bodies():
		if b is Node and (b as Node).is_in_group(ACTOR):
			area_hit = true
			break
	var cs := _area.get_node_or_null("ProximityShape") as CollisionShape3D
	if cs == null or not (cs.shape is BoxShape3D):
		return area_hit
	# The box is this frame. Area overlaps lag one physics frame, so a teleport
	# out of the volume still lists the actor and would start the open clock
	# one tick early. A listed overlap counts only while the capsule still
	# reaches the box. An origin already inside the box counts immediately.
	if _point_in_proximity(cs, 0.0):
		return true
	if area_hit and _point_in_proximity(cs, CAPSULE_DIAMETER * 0.5):
		return true
	return false


func _point_in_proximity(cs: CollisionShape3D, margin: float) -> bool:
	var half: Vector3 = (cs.shape as BoxShape3D).size * 0.5
	half.x += margin
	half.y += margin
	half.z += margin
	var tree := get_tree()
	if tree == null:
		return false
	var xf: Transform3D = cs.global_transform.affine_inverse()
	for n in tree.get_nodes_in_group(ACTOR):
		if not (n is Node3D):
			continue
		var body := n as Node3D
		for extra in [Vector3.ZERO, Vector3(0.0, 1.0, 0.0)]:
			var local: Vector3 = xf * (body.global_position + extra)
			if absf(local.x) <= half.x and absf(local.y) <= half.y and absf(local.z) <= half.z:
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
	var prev_t := motion_t
	var prev_q: Array[float] = []
	prev_q.resize(q_now.size())
	for i in q_now.size():
		prev_q[i] = q_now[i]
	motion_t += _motion_advance(dir, prev_t, delta)
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
	# Opening bay3 / pair: if the capsule is already in the sweep, drop this tick's
	# motion so the leaf never shoves the body. A stall is a hold, not a fault.
	if dir == "open" and (door_id == "bay3" or door_id == "pair") and _obstruction_hit():
		motion_t = prev_t
		for i in _leaves.size():
			q_now[i] = prev_q[i]
			v_now[i] = 0.0
			_pose_leaf(i, prev_q[i])
			if i < _leaf_phase.size():
				_leaf_phase[i] = "stalled"
		_sync_bodies()
		_stall = true
		state = "stalled"
		_set_state("stalled")
		_set_lamp("moving", false)
		return
	_fire_cues(dir)
	if phase_now != phase:
		phase = phase_now
		_emit_phase(phase)
	_drive_hardware(dir, false)
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


func _motion_advance(dir: String, t: float, delta: float) -> float:
	# Floor hatch only. At 1 G and 0.08 G the actuator tracks the profile, so
	# the clock stays kinematic and a raw R3 tick never sees a 0.2 clamp step.
	# Above 1.05 G a positive ratio below 1 is saturation and stretches the tick.
	# A ratio at or below 0 is a sign flip, not saturation.
	if door_id != "floorhatch" or gravity_g <= 1.05:
		return delta
	var s: Dictionary = profile.sample(dir, maxf(t, 0.0))
	var a_des := deg_to_rad(float(s.get("acc", 0.0)))
	var theta := deg_to_rad(float(s.get("q", 0.0)))
	# Rook pass E incr: same numbers, read from the door metas the rig sets (torsion bar 585, weight 687 at 1 G, actuator 530).
	var tm: Dictionary = get_meta("torque_model", {})
	var passive := float(tm.get("torsion_bar_Nm", 585.0)) - float(tm.get("weight_moment_Nm", 687.0)) * gravity_g * cos(theta)
	var inertia := float(tm.get("inertia_kgm2", 46.7))
	var act_max := float(tm.get("actuator_max_Nm", 530.0))
	var ratio := 1.0
	if absf(a_des) > 0.05:
		var actuator := clampf(inertia * a_des - passive, -act_max, act_max)
		var a_act := (actuator + passive) / inertia
		ratio = a_act / a_des
		if ratio <= 0.0 or ratio >= 1.0:
			ratio = 1.0
		else:
			ratio = clampf(ratio, 0.2, 1.0)
	var v_cap := float(get_meta("damper_open_dps", 77.8)) if dir == "open" else float(get_meta("damper_close_dps", 33.3))
	var v_des := absf(float(s.get("vel", 0.0)))
	if v_des > v_cap + 0.05:
		ratio = minf(ratio, v_cap / v_des)
	return delta * ratio


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
	if player == null:
		return
	if player.stream == null:
		player.stream = _stream_for(nm)
	player.play()


func _pose_leaf(i: int, q: float) -> void:
	var leaf: Dictionary = _leaves[i]
	var sign := float(leaf["sign"])
	var body: AnimatableBody3D = leaf["body"]
	if _hinge:
		# Floor hatch swings about local X. Sign -1 lifts a leaf that extends +Z.
		if absf(hinge_axis.x) > 0.5:
			body.rotation = Vector3(deg_to_rad(sign * q), 0.0, 0.0)
		else:
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


func _emergency_creep(delta: float) -> void:
	# Pressure emergency: seat at 5 deg/s, never reverse. Dogs and the seal
	# keep going after the leaf is down, on the close-profile clock.
	emergency = true
	var seated := true
	for i in _leaves.size():
		var q := maxf(0.0, q_now[i] - 5.0 * delta)
		if q > 0.02:
			seated = false
		q_now[i] = q
		v_now[i] = -5.0 if q > 0.0 else 0.0
		_pose_leaf(i, q)
		if i < _leaf_phase.size():
			_leaf_phase[i] = "emergency"
	if seated:
		var dogs := profile.phase_span("close", "dogs")
		if dogs.x >= 0.0 and motion_t < dogs.x:
			motion_t = dogs.x
		else:
			motion_t += delta
		for i in _leaves.size():
			q_now[i] = 0.0
			v_now[i] = 0.0
			_pose_leaf(i, 0.0)
	_sync_bodies()
	_drive_hardware("close", false)
	phase = "emergency"
	state = "closing"
	_set_state("closing")
	_klaxon_age += delta
	if _klaxon_age >= 1.0:
		_klaxon_age = 0.0
		klaxon_fired = true
		klaxon_count += 1
		cue.emit("klaxon_emergency")
		_blip("klaxon_emergency")


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
	# Stop on the tick that reaches stop_s. 6/60 is 0.09999…, so a raw >= test
	# waits one more tick (pair was 0.117 s). Also stop when the next tick would
	# pass stop_s, so a 15 Hz step cannot land past the limit.
	var brake_due := _brake_t + 1.0e-4 >= stop_s or _brake_t + delta > stop_s + 1.0e-4
	if all_stopped or brake_due:
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
	if cap <= 0.0:
		cap = 0.6 if profile.clear_model == "slide" else 40.0
	var dist := 0.0
	for i in _leaves.size():
		dist = maxf(dist, absf(profile.travel - q_now[i]))
	# Raised-cosine peak is (pi/2)*dist/dur. Size dur so that peak equals the cap.
	_reopen_dur = maxf(0.35, (PI * 0.5) * dist / cap)
	_reopen_scale = 1.0
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
	var dur := maxf(_reopen_dur, 0.35)
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
	# AESTHETIC_SPEC §3. Dark lamp albedo keeps energy × peak channel ≤ 1.
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
		_fade_from_color = _target_color
		_fade_from_energy = _target_energy
		_fade_age = 0.15
		_paint_lamp()
	else:
		_fade_from_color = _shown_color
		_fade_from_energy = _shown_energy
		_fade_age = 0.0


func _fade_lamp(delta: float) -> void:
	if lamp == "fault":
		var blink := sin(TAU * 2.0 * Time.get_ticks_msec() / 1000.0) > 0.0
		_target_color = Color("#FF2A2A") if blink else Color("#FF9500")
		_target_energy = 1.0
	# Fixed 0.15 s smoothstep. Elapsed time, not an exponential per-tick lerp.
	_fade_age = minf(_fade_age + delta, 0.15)
	var u := clampf(_fade_age / 0.15, 0.0, 1.0)
	var s := u * u * (3.0 - 2.0 * u)
	_shown_color = _fade_from_color.lerp(_target_color, s)
	_shown_energy = lerpf(_fade_from_energy, _target_energy, s)
	_paint_lamp()


func _paint_lamp() -> void:
	if _lamp_mat != null:
		_lamp_mat.emission_enabled = true
		_lamp_mat.emission = _shown_color
		_lamp_mat.emission_energy_multiplier = _shown_energy
		# Dark amber body. A grey albedo plus a bright emission clips to a lemon bar.
		_lamp_mat.albedo_color = Color(0.10, 0.06, 0.0, 1.0)
	# Chase segments are separate materials. A still frame never runs _chase, so paint them here too.
	for seg in _lamp_segs:
		var mi := seg as MeshInstance3D
		if mi == null:
			continue
		var mat := mi.get_surface_override_material(0) as StandardMaterial3D
		if mat == null:
			continue
		mat.emission_enabled = true
		mat.emission = _shown_color
		mat.emission_energy_multiplier = _shown_energy
		mat.albedo_color = Color(0.10, 0.06, 0.0, 1.0)
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


func _drive_hardware(dir: String, forced: bool = false) -> void:
	var q := q_now[0] if q_now.size() else 0.0
	var span := maxf(profile.travel, 0.001)
	var travel_u := clampf(q / span, 0.0, 1.0)
	for n in _hw:
		if not (n is Node3D):
			continue
		var node := n as Node3D
		var kind := str(node.get_meta("door_hw"))
		if kind == "roller" or kind == "roller_z":
			_spin_roller(node, q, kind == "roller_z")
		elif kind == "dog" or kind == "dog_x":
			_pose_dog(node, dir, forced, travel_u, kind == "dog_x")
		elif kind == "wheel" or kind == "wheel_z":
			_pose_wheel(node, dir, forced, travel_u, kind == "wheel_z")
		elif kind == "needle" or kind == "needle_z":
			_pose_needle(node, kind == "needle_z")
		elif kind == "seal" or kind == "seal_z":
			_pose_seal(node, dir, forced, travel_u, kind == "seal_z")
		elif kind == "rod":
			_stretch_rod(node)
		elif kind == "piston":
			_aim_piston(node)
		elif kind == "stay":
			_pose_stay(node)


func _rest_basis(node: Node3D) -> Basis:
	if not node.has_meta("rest_basis"):
		node.set_meta("rest_basis", node.basis)
	return node.get_meta("rest_basis")


func _rest_pos(node: Node3D) -> Vector3:
	if not node.has_meta("rest"):
		node.set_meta("rest", node.position)
	return node.get_meta("rest")


func _spin_roller(node: Node3D, q: float, about_z: bool) -> void:
	var r := float(node.get_meta("roller_r", 0.03))
	var sgn := float(node.get_meta("roller_sign", 1.0))
	var spins := sgn * q / maxf(r, 0.005)
	if about_z:
		node.basis = _rest_basis(node) * Basis(Vector3(0, 0, 1), spins)
	else:
		node.rotation.x = spins


func _dog_throw_u(dir: String, forced: bool, travel_u: float) -> float:
	# 0 = retracted (open), 1 = thrown (closed).
	# Rook pass E incr: any lift retracts the dogs in a forced pose (was > 0.02, which showed thrown dogs on a lid lifted <= 2.1 deg).
	if forced:
		return 0.0 if travel_u > 0.0 else 1.0
	var local_t := _phase_u(["dogs"])
	if dir == "close":
		return local_t
	return 1.0 - local_t


func _pose_dog(node: Node3D, dir: String, forced: bool, travel_u: float, along_x: bool) -> void:
	var thrown := _dog_throw_u(dir, forced, travel_u)
	if not along_x:
		var st := float(node.get_meta("stagger", 0.0))
		var du := clampf((_phase_u(["dogs"]) - st) / 0.55, 0.0, 1.0)
		if dir == "close":
			du = 1.0 - du
		if forced:
			du = 1.0 if travel_u > 0.0 else 0.0
		var rest: Vector3 = node.get_meta("rest")
		var retract: Vector3 = node.get_meta("retract")
		node.position = rest + retract * du
		return
	var rest_p := _rest_pos(node)
	var rest_b := _rest_basis(node)
	var throw_m := float(node.get_meta("throw_m", 0.025))
	node.basis = rest_b
	node.position = rest_p + rest_b * Vector3(throw_m * thrown, 0.0, 0.0)


func _pose_wheel(node: Node3D, dir: String, forced: bool, travel_u: float, about_z: bool) -> void:
	var thrown := _dog_throw_u(dir, forced, travel_u)
	if about_z:
		var ax: Vector3 = node.get_meta("wheel_axis", Vector3(0, 0, 1))
		node.basis = _rest_basis(node) * Basis(ax, deg_to_rad(float(node.get_meta("wheel_deg", 90.0)) * thrown))
		return
	var du2 := _phase_u(["dogs"])
	if dir == "close":
		du2 = 1.0 - du2
	if forced:
		du2 = 1.0 if travel_u > 0.0 else 0.0
	node.rotation.z = deg_to_rad(-90.0 * du2)


func _pose_needle(node: Node3D, about_z: bool) -> void:
	var eu := _phase_u(["equalize"])
	if about_z:
		node.basis = _rest_basis(node) * Basis(Vector3(0, 0, 1), deg_to_rad(-70.0 * (1.0 - eu)))
		return
	node.rotation.z = deg_to_rad(-70.0 * (1.0 - eu))


func _pose_seal(node: Node3D, dir: String, forced: bool, travel_u: float, scale_z: bool) -> void:
	var deflated := _phase_u(["seal_deflate", "seal_unseat"])
	if dir == "close" and not forced:
		deflated = 1.0 - _phase_u(["seal_inflate", "creep"])
	if forced:
		deflated = 1.0 if travel_u > 0.02 else 0.0
	deflated = clampf(deflated, 0.0, 1.0)
	if scale_z:
		var inflated := float(node.get_meta("inflate_scale", 1.476))
		var z := lerpf(inflated, 1.0, deflated)
		if str(node.get_meta("seal_axis", "z")) == "y":
			node.scale = Vector3(1.0, z, 1.0)
		else:
			node.scale = Vector3(1.0, 1.0, z)
		return
	var sc := lerpf(1.0, 0.72, deflated)
	node.scale = Vector3(sc, 1.0, sc)


func _aim_piston(node: Node3D) -> void:
	var partner: Node3D = node.get_meta("piston_partner") if node.has_meta("piston_partner") else null
	if partner == null:
		return
	var origin := node.global_position
	var aim := partner.global_position
	if origin.distance_to(aim) < 1.0e-3:
		return
	node.look_at(aim, Vector3.UP, bool(node.get_meta("piston_front_z", false)))
	node.global_position = origin


func _pose_stay(node: Node3D) -> void:
	# Tables vs leaf opening fraction, evenly spaced 0..travel. stay_table = degrees about local X (floor-hatch stay arm);
	# stay_slide_table = metres along local Z (Rook rev 2 side-wall stay slider and detent plunger).
	var span := maxf(profile.travel, 0.001)
	var f := clampf((q_now[0] if q_now.size() else 0.0) / span, 0.0, 1.0)
	var tab: PackedFloat32Array = node.get_meta("stay_table", PackedFloat32Array())
	if tab.size() >= 2:
		node.basis = _rest_basis(node) * Basis(Vector3(1, 0, 0), deg_to_rad(_table_at(tab, f)))
	var slide: PackedFloat32Array = node.get_meta("stay_slide_table", PackedFloat32Array())
	if slide.size() >= 2:
		node.position = _rest_pos(node) + _rest_basis(node) * Vector3(0.0, 0.0, _table_at(slide, f))


func _table_at(tab: PackedFloat32Array, f: float) -> float:
	var u := f * float(tab.size() - 1)
	var i := mini(int(floor(u)), tab.size() - 2)
	return lerpf(tab[i], tab[i + 1], u - float(i))


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
		var prev_v := float(_log_prev_v[i]) if i < _log_prev_v.size() else v_now[i]
		var acc := (v_now[i] - prev_v) / maxf(_delta, 1.0e-5)
		var yaw := body.rotation_degrees.x if absf(hinge_axis.x) > 0.5 else body.rotation_degrees.y
		rows.append({
			"t": sim_t,
			"motion_t": motion_t,
			"phase": _leaf_phase[i] if i < _leaf_phase.size() else phase,
			"leaf": str(leaf["name"]),
			"px": o.x, "py": o.y, "pz": o.z,
			"q": q_now[i],
			"yaw": yaw,
			"vel": v_now[i],
			"leaf_vel": deg_to_rad(v_now[i]) if _hinge else v_now[i],
			"leaf_acc": acc,
			"drift_mm": drift * 1000.0,
			"gap_mm": gap,
			"contacts": contacts,
			"lamp": lamp,
			"lamp_energy": _shown_energy,
			"collider": 1 if body.collision_layer != 0 else 0,
			"state": state,
			"g": gravity_g,
		})
	_log_prev_v = v_now.duplicate()


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
	elif door_id == "floorhatch":
		box.size = Vector3(0.70, 0.55, 0.70)
	_sensor.shape = box
	_sensor.target_position = Vector3(0, 0, 0.02)
	_sensor.collision_mask = 1
	_sensor.collide_with_areas = false
	_sensor.collide_with_bodies = true
	_sensor.enabled = false
	if "debug_shape_custom_color" in _sensor:
		_sensor.debug_shape_custom_color = Color(0, 0, 0, 0)
	add_child(_sensor)
	for leaf in _leaves:
		_sensor.add_exception(leaf["body"])


func _place_sensor() -> void:
	if _sensor == null:
		return
	var watch := state == "closing" or state == "braking" or state == "dwell" or state == "reopening" or state == "stalled"
	if state == "opening" and (door_id == "bay3" or door_id == "pair"):
		watch = true
	_sensor.enabled = watch
	if not watch:
		return
	_sensor.position = _sensor_pos


func _stream_for(nm: String) -> AudioStreamWAV:
	var n := nm.to_lower()
	if "klaxon" in n:
		return _tone(420.0, 1400, 0.22, 70.0)
	if "hiss" in n:
		return _noise(1400, 0.35)
	if "whine" in n or "hum" in n:
		return _tone(160.0, 1800, 0.55, 240.0)
	if "thud" in n or "thunk" in n or "bumper" in n:
		return _tone(70.0, 700, 0.9, 40.0)
	if "clack" in n or "clunk" in n or "tap" in n or "pop" in n:
		return _tone(1500.0, 240, 1.0, 50.0)
	return _tone(880.0, 480, 1.0, 90.0)


func _tone(freq: float, count: int, amp: float, decay: float) -> AudioStreamWAV:
	var stream := AudioStreamWAV.new()
	stream.format = AudioStreamWAV.FORMAT_8_BITS
	stream.mix_rate = 8000
	stream.stereo = false
	var data := PackedByteArray()
	data.resize(count)
	for i in count:
		var env := exp(-float(i) / maxf(decay, 1.0))
		var s := sin(TAU * freq * float(i) / 8000.0) * env * amp
		data[i] = int(clampf(128.0 + s * 110.0, 0.0, 255.0))
	stream.data = data
	return stream


func _noise(count: int, amp: float) -> AudioStreamWAV:
	var stream := AudioStreamWAV.new()
	stream.format = AudioStreamWAV.FORMAT_8_BITS
	stream.mix_rate = 8000
	stream.stereo = false
	var data := PackedByteArray()
	data.resize(count)
	var hold := 0.0
	for i in count:
		if i % 3 == 0:
			hold = sin(float(i) * 12.9898) * 43758.5453
			hold = hold - floor(hold)
			hold = (hold * 2.0 - 1.0) * amp
		var env := exp(-float(i) / 500.0)
		data[i] = int(clampf(128.0 + hold * env * 100.0, 0.0, 255.0))
	stream.data = data
	return stream


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
			p.stream = _stream_for(nm)
			add_child(p)
	if not seen.has("klaxon_emergency"):
		var alarm := AudioStreamPlayer3D.new()
		alarm.name = "Cue_klaxon_emergency"
		alarm.unit_size = 4.0
		alarm.stream = _stream_for("klaxon_emergency")
		add_child(alarm)


func drift_deg() -> float:
	var worst := 0.0
	for leaf in _leaves:
		var body: AnimatableBody3D = leaf["body"]
		if not body.is_inside_tree():
			continue
		var phys: Transform3D = PhysicsServer3D.body_get_state(body.get_rid(), PhysicsServer3D.BODY_STATE_TRANSFORM)
		worst = maxf(worst, rad_to_deg(phys.basis.get_rotation_quaternion().angle_to(body.global_basis.get_rotation_quaternion())))
	return worst
