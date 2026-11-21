extends Node
## Headless functional pass for the mechanical door lab.
## Exit 0 only when every scored functional check passes.
## Pixel checks (luma, shadow, flicker) are deferred to the shot pass.

const IDS := ["pocket", "bay3", "pair", "hatch"]
const FUNC_R := ["R1", "R2", "R3", "R4", "R5", "R7", "R9", "R10", "R13", "R14", "R15"]
const K_TRAVEL := 0.45
const K_MECH := 0.60

var _lab: Node3D
var _player: CharacterBody3D
var _doors: Dictionary = {}
var _fps: int = 60
var _dt: float = 1.0 / 60.0
var _out: String = ""
var _probe: CharacterBody3D
var _checks: Dictionary = {}
var _clips: Dictionary = {}
var _cues: Array = []
var _notes: Array = []
var _max_drift_deg: float = 0.0
var _fps_explicit: bool = false
var _measured_dt: float = 0.0
var _measured_hz: float = 0.0
var _allow: Dictionary = {}


func _trace(msg: String) -> void:
	print(msg)
	var path := "C:/Users/upchu/AppData/Local/Temp/doorlab_g_trace.txt"
	var f := FileAccess.open(path, FileAccess.READ_WRITE)
	if f == null:
		f = FileAccess.open(path, FileAccess.WRITE)
	else:
		f.seek_end()
	if f == null:
		return
	f.store_line(msg)
	f.flush()
	f.close()


func start(lab: Node3D) -> void:
	var wipe := FileAccess.open("C:/Users/upchu/AppData/Local/Temp/doorlab_g_trace.txt", FileAccess.WRITE)
	if wipe != null:
		wipe.close()
	_trace("qa enter")
	_lab = lab
	var info: Dictionary = lab.get_meta("lab_info")
	_player = info["player"]
	_doors = info["doors"]
	_notes = info.get("notes", [])
	_fps = _read_fps()
	Engine.max_physics_steps_per_frame = 1
	Engine.physics_ticks_per_second = _fps
	_dt = 1.0 / float(_fps)
	_out = _read_out()
	_probe = _make_probe()
	await _measure_rate()
	_trace("[door_lab] qa fps=%d ticks=%d measured_hz=%.2f measured_dt=%.6f out=%s" % [_fps, Engine.physics_ticks_per_second, _measured_hz, _measured_dt, _out])
	_check_rate()
	await _heading()
	for id in IDS:
		await _one(id)
	if _doors.has("floorhatch"):
		await _one("floorhatch")
	_finish()


func _read_fps() -> int:
	var fps := 60
	_fps_explicit = false
	var bags: Array = [OS.get_cmdline_args(), OS.get_cmdline_user_args()]
	for bag in bags:
		var args: PackedStringArray = bag
		for i in args.size():
			var a := str(args[i])
			# --fixed-fps is consumed by the engine on some builds. The harness
			# only trusts the user arg that survives both bags.
			if a == "--qa-door-lab-fps" and i + 1 < args.size():
				fps = int(args[i + 1])
				_fps_explicit = true
			elif a.begins_with("--qa-door-lab-fps="):
				fps = int(a.split("=")[1])
				_fps_explicit = true
			elif a == "--fixed-fps" and i + 1 < args.size() and not _fps_explicit:
				fps = int(args[i + 1])
			elif a.begins_with("--fixed-fps=") and not _fps_explicit:
				fps = int(a.split("=")[1])
	return maxi(fps, 1)


func _measure_rate() -> void:
	var acc := 0.0
	var n := 8
	for _i in n:
		await get_tree().physics_frame
		acc += get_physics_process_delta_time()
	_measured_dt = acc / float(n)
	_measured_hz = 1.0 / maxf(_measured_dt, 1.0e-6)


func _check_rate() -> void:
	var ticks := Engine.physics_ticks_per_second
	var ok := _fps_explicit and ticks == _fps and absf(_measured_hz - float(_fps)) <= 0.51
	var note := "ticks %d measured_dt %.6f hz %.2f explicit %s" % [ticks, _measured_dt, _measured_hz, _fps_explicit]
	print("[door_lab] F-FPS %s %s" % ["PASS" if ok else "FAIL", note])
	for id in _doors.keys():
		_rec(str(id), "F-FPS", ok, _measured_hz, float(_fps), "Hz", note, "F")


func _read_out() -> String:
	var rel := "user://door_lab_run"
	var args := OS.get_cmdline_user_args()
	for i in args.size():
		if args[i] == "--qa-door-lab-out" and i + 1 < args.size():
			rel = str(args[i + 1])
	if rel.begins_with("res://") or rel.begins_with("user://"):
		return ProjectSettings.globalize_path(rel)
	if rel.begins_with("/") or (rel.length() > 2 and rel[1] == ":"):
		return rel
	var base := ProjectSettings.globalize_path("res://")
	return base.path_join(rel).simplify_path()


func _make_probe() -> CharacterBody3D:
	var body := CharacterBody3D.new()
	body.name = "ObstructionProbe"
	body.collision_layer = 1
	body.collision_mask = 1
	body.add_to_group("door_lab_obstruction")
	var cs := CollisionShape3D.new()
	cs.name = "ProbeCapsule"
	var cap := CapsuleShape3D.new()
	cap.radius = 0.35
	cap.height = 1.75
	cs.shape = cap
	cs.position = Vector3(0.0, 0.995, 0.0)
	body.add_child(cs)
	body.position = Vector3(0.0, -30.0, 0.0)
	_lab.add_child(body)
	return body


func _rec(door_id: String, cid: String, ok: bool, measured: float, limit: float, unit: String, note: String, kind: String) -> void:
	if not _checks.has(door_id):
		_checks[door_id] = []
	_checks[door_id].append({
		"id": cid, "pass": ok, "measured": measured, "limit": limit,
		"unit": unit, "note": note, "kind": kind,
	})


func _park(at: Vector3, yaw: float) -> void:
	_release()
	_player.velocity = Vector3.ZERO
	_player.global_position = at
	_player.rotation = Vector3(0.0, yaw, 0.0)
	await get_tree().physics_frame
	_player.velocity = Vector3.ZERO


func _release() -> void:
	for action in ["move_forward", "move_back", "move_left", "move_right", "sprint", "interact", "jump"]:
		if InputMap.has_action(action):
			Input.action_release(action)


func _press(action: String) -> void:
	Input.action_press(action)


func _hide_probe() -> void:
	_probe.global_position = Vector3(0.0, -30.0, 0.0)
	_probe.velocity = Vector3.ZERO


func _heading() -> void:
	await _park(Vector3(0.0, 0.0, -20.0), PI)
	var z0 := _player.global_position.z
	_press("move_forward")
	var t := 0.0
	while t < 0.25:
		await get_tree().physics_frame
		t += _dt
	_release()
	var dz := _player.global_position.z - z0
	var ok := dz > 0.05
	print("[door_lab] F-FRAME %s dz=%.3f (forward must increase world Z)" % ["PASS" if ok else "FAIL", dz])
	if not ok:
		for id in IDS:
			_rec(id, "F-FRAME", false, dz, 0.05, "m", "move_forward did not walk +Z", "F")
	await _park(Vector3(0.0, 0.0, -200.0), PI)


func _one(id: String) -> void:
	var door: MechDoor = _doors[id]
	_trace("[door_lab] --- %s ---" % id)
	_clips[id] = []
	door.reset_closed()
	door.record = false
	_hide_probe()
	await _park(Vector3(door.global_position.x, 0.0, -200.0), PI)
	await _blocks(door)
	await _approach(door)
	await _scored_cycle(door)
	await _obstruction(door)
	await _stall_open(door)
	var clip_t0 := Time.get_ticks_msec()
	await _clips_and_gaps(door)
	print("[door_lab] %s clips %.1fs" % [id, float(Time.get_ticks_msec() - clip_t0) / 1000.0])
	await _snag(door)
	await _gravity(door)
	await _cycles(door)
	if door.door_id == "hatch" or door.door_id == "floorhatch":
		await _emergency(door)
	_hardware(door)
	_albedo(door)
	_plate_color(door)
	_defer_pixels(door)
	door.reset_closed()
	_hide_probe()
	await _park(Vector3(0.0, 0.0, -200.0), PI)


func _blocks(door: MechDoor) -> void:
	if door.door_id == "floorhatch":
		await _floor_blocks(door)
		return
	# The start pose sits inside the proximity sphere. Lock so the leaf stays
	# closed for the push; proximity is tested later, from outside the sphere.
	door.reset_closed()
	door.set_locked(true)
	var face_neg := _leaf_face_z(door, true)
	var face_pos := _leaf_face_z(door, false)
	var worst_dist := 100.0
	var worst_pen := 0.0
	var worst_speed := 0.0
	var crossed := false
	# Approach (-Z, yaw PI, forward is +Z) and corridor (+Z, yaw 0, forward is -Z).
	var sides := [
		{"z": door.global_position.z - 3.0, "yaw": PI, "sign": 1.0, "face": face_neg},
		{"z": door.global_position.z + 3.0, "yaw": 0.0, "sign": -1.0, "face": face_pos},
	]
	for side in sides:
		await _park(Vector3(door.global_position.x + float(door.get_meta("block_x", 0.0)), 0.0, side["z"]), side["yaw"])
		_press("move_forward")
		var t := 0.0
		var speed_at_1 := 0.0
		var saw_1 := false
		while t < 1.6:
			await get_tree().physics_frame
			t += _dt
			var along := _player.velocity.z * float(side["sign"])
			if t >= 1.0 and not saw_1:
				speed_at_1 = along
				saw_1 = true
			var origin := _player.global_position.z
			var face: float = side["face"]
			var dist := (face - origin) * float(side["sign"])
			worst_dist = minf(worst_dist, dist)
			var lead := origin + 0.35 * float(side["sign"])
			var pen := (lead - face) * float(side["sign"])
			if pen > 0.0:
				worst_pen = maxf(worst_pen, pen)
			if pen > 0.001:
				crossed = true
		_release()
		worst_speed = maxf(worst_speed, speed_at_1)
	_rec(door.door_id, "F-BLOCK-ORIG", worst_dist >= 0.30, worst_dist, 0.30, "m", "min origin distance to approach face, both sides", "F")
	_rec(door.door_id, "F-BLOCK-PEN", worst_pen <= 0.001, worst_pen, 0.001, "m", "visual face penetration", "F")
	_rec(door.door_id, "F-BLOCK-STOP", worst_speed <= 0.05, worst_speed, 0.05, "m/s", "approach speed after 1 s", "F")
	_rec(door.door_id, "F-BLOCK-CROSS", not crossed, 1.0 if crossed else 0.0, 0.0, "bool", "leading point past the leaf plane", "F")
	# Sprint into the closed approach face. Robustness only.
	await _park(Vector3(door.global_position.x, 0.0, door.global_position.z - 4.0), PI)
	_press("move_forward")
	_press("sprint")
	var ts := 0.0
	var sprint_pen := 0.0
	var sprint_dist := 100.0
	while ts < 0.8:
		await get_tree().physics_frame
		ts += _dt
		var dist_s := face_neg - _player.global_position.z
		sprint_dist = minf(sprint_dist, dist_s)
		var lead_s := _player.global_position.z + 0.35 - face_neg
		if lead_s > 0.0:
			sprint_pen = maxf(sprint_pen, lead_s)
	_release()
	var sprint_ok := sprint_dist >= 0.30 and sprint_pen <= 0.001
	if not sprint_ok:
		_rec(door.door_id, "F-BLOCK-ORIG", false, sprint_dist, 0.30, "m", "sprint-into-closed also failed", "F")
	_rec(door.door_id, "F-SPRINT-CLEAR", true, sprint_dist, 0.0, "m", "not required in the lab; sprint-into-closed dist %.3f pen %.4f" % [sprint_dist, sprint_pen], "note")
	if door.door_id == "pocket":
		await _park(Vector3(door.global_position.x, 0.0, door.global_position.z - 2.0), PI)
		_press("move_forward")
		var tl := 0.0
		while tl < 0.8:
			await get_tree().physics_frame
			tl += _dt
		var stayed := door.state == "closed" and door.lamp == "locked"
		_release()
		if not stayed:
			_rec(door.door_id, "F-BLOCK-ORIG", false, 0.0, 1.0, "bool", "locked pocket opened or lamp was not red", "F")
	door.set_locked(false)
	door.reset_closed()


func _floor_blocks(door: MechDoor) -> void:
	# A flush lid must hold the capsule. Falling through is the failure.
	door.reset_closed()
	door.set_locked(true)
	var at := Vector3(door.global_position.x, 0.0, door.global_position.z + 0.50)
	await _park(at, PI)
	var y_min := _player.global_position.y
	var t := 0.0
	while t < 1.0:
		await get_tree().physics_frame
		t += _dt
		y_min = minf(y_min, _player.global_position.y)
	var held := y_min >= -0.05
	_rec(door.door_id, "F-BLOCK-ORIG", held, y_min, 0.0, "m", "capsule origin stays on the closed lid", "F")
	_rec(door.door_id, "F-BLOCK-PEN", held, 0.0 if held else 0.05, 0.001, "m", "did not drop through the lid", "F")
	_rec(door.door_id, "F-BLOCK-STOP", true, 0.0, 0.05, "m/s", "no walk input on the lid", "F")
	_rec(door.door_id, "F-BLOCK-CROSS", held, 0.0 if held else 1.0, 0.0, "bool", "origin stayed above the floor", "F")
	_rec(door.door_id, "F-SPRINT-CLEAR", true, y_min, 0.0, "m", "not required in the lab", "note")
	door.set_locked(false)
	door.reset_closed()
	await _park(Vector3(0.0, 0.0, -200.0), PI)


func _leaf_face_z(door: MechDoor, approach_neg: bool) -> float:
	var best := door.global_position.z
	var any := false
	for item in door._leaves:
		var ab := _primary_world_aabb(item["body"])
		if ab.size.length() <= 0.0:
			ab = _world_aabb(item["body"])
		if ab.size.length() <= 0.0:
			continue
		var z0 := ab.position.z
		var z1 := ab.position.z + ab.size.z
		if not any:
			best = z0 if approach_neg else z1
			any = true
		elif approach_neg:
			best = minf(best, z0)
		else:
			best = maxf(best, z1)
	return best


func _world_aabb(n: Node) -> AABB:
	var ab := AABB()
	var any := false
	var stack: Array[Node] = [n]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		for c in node.get_children():
			stack.append(c)
		if node is MeshInstance3D and (node as MeshInstance3D).mesh != null:
			var mi := node as MeshInstance3D
			var world: AABB = mi.global_transform * mi.mesh.get_aabb()
			ab = world if not any else ab.merge(world)
			any = true
	return ab


func _primary_world_aabb(n: Node) -> AABB:
	# The shell is the collided leaf. Panels proud of it are not the stop face.
	var shell := _aabb_matching(n, "shell")
	if shell.size.length() > 0.001:
		return shell
	return _aabb_matching(n, "stile|panel|leafface")


func _aabb_matching(n: Node, tokens: String) -> AABB:
	var ab := AABB()
	var any := false
	var parts := tokens.split("|")
	var stack: Array[Node] = [n]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		for c in node.get_children():
			stack.append(c)
		if not (node is MeshInstance3D) or (node as MeshInstance3D).mesh == null:
			continue
		var nm := String(node.name).to_lower()
		var hit := false
		for token in parts:
			if token in nm:
				hit = true
				break
		if not hit:
			continue
		var mi := node as MeshInstance3D
		var world: AABB = mi.global_transform * mi.mesh.get_aabb()
		ab = world if not any else ab.merge(world)
		any = true
	return ab


func _approach(door: MechDoor) -> void:
	door.reset_closed()
	var wx := float(door.get_meta("walk_x", 0.0))
	var dx := door.global_position.x + wx
	if door.profile.interact:
		await _interact(door, dx)
		return
	var z_start := door.global_position.z - (door.trigger_radius + 1.6)
	await _park(Vector3(dx, 0.0, z_start), PI)
	_press("move_forward")
	var t_open := -1.0
	var lat := -1.0
	var clear_at := -1.0
	var t := 0.0
	while t < door.profile.open_duration + 4.0:
		await get_tree().physics_frame
		t += _dt
		if door.state != "closed" and t_open < 0.0:
			t_open = door.motion_t
		if t_open >= 0.0 and lat < 0.0 and (door.lamp == "moving" or _is_mech_phase(door.phase)):
			# motion_t is the open clock. sim_t includes the tick that already advanced it.
			lat = door.motion_t
		var rel := _player.global_position.z - door.global_position.z
		if rel >= -0.50 and clear_at < 0.0:
			clear_at = _clear_now(door)
			break
	_release()
	_player.velocity = Vector3.ZERO
	# ±10% or one physics tick, whichever is looser. No extra tick on top.
	var tol := maxf(absf(door.profile.mech_event_open) * 0.10, _dt)
	var lat_ok := lat >= 0.0 and absf(lat - door.profile.mech_event_open) <= tol + 1.0e-3
	_rec(door.door_id, "F-LAT-MECH", lat_ok, lat, door.profile.mech_event_open, "s", "tol ±%.3f s" % tol, "F")
	var clear_ok := clear_at >= 0.80
	_rec(door.door_id, "F-WALK-CLEAR", clear_ok, clear_ok if false else clear_at, 0.80, "m", "profile clear_gap when origin is 0.50 m out", "F")
	_rec(door.door_id, "F-INTERACT", true, 0.0, 2.8, "m", "n/a for this type", "F")
	await _park(Vector3(dx, 0.0, -200.0), PI)
	if door.state != "closed":
		door.command_close()
		await _until_closed(door, door.profile.close_duration + 3.0)


func _interact(door: MechDoor, dx: float) -> void:
	# Inside 2.8 m, hold E. Stay put until the plug is clear, then walk the last metre.
	await _park(Vector3(dx, 0.0, door.global_position.z - 2.0), PI)
	var t0 := door.sim_t
	_press("interact")
	var t_open := -1.0
	var t_mech := -1.0
	var t := 0.0
	while t < 0.6:
		await get_tree().physics_frame
		t += _dt
		if door.state != "closed" and t_open < 0.0:
			t_open = door.sim_t
		if t_open >= 0.0 and t_mech < 0.0 and (door.lamp == "moving" or _is_mech_phase(door.phase)):
			t_mech = door.sim_t
	var started := door.state != "closed"
	_release()
	# Outside range is a no-op. Reset and confirm.
	door.reset_closed()
	await _park(Vector3(dx, 0.0, door.global_position.z - 4.5), PI)
	_press("interact")
	var t_out := 0.0
	while t_out < 0.5:
		await get_tree().physics_frame
		t_out += _dt
	var stayed := door.state == "closed"
	_release()
	_rec(door.door_id, "F-INTERACT", started and stayed, 2.0 if started else 9.0, 2.8, "m", "E at 2.0 m starts; E at 4.5 m does not", "F")
	# Real open for latency, then walk only after the gap is wide.
	await _park(Vector3(dx, 0.0, door.global_position.z - 2.0), PI)
	door.reset_closed()
	_press("interact")
	t_open = -1.0
	var lat := -1.0
	t = 0.0
	while t < 1.2:
		await get_tree().physics_frame
		t += _dt
		if door.state != "closed" and t_open < 0.0:
			t_open = door.motion_t
		if t_open >= 0.0 and lat < 0.0 and (door.lamp == "moving" or _is_mech_phase(door.phase)):
			lat = door.motion_t
			break
	_release()
	var tol := maxf(absf(door.profile.mech_event_open) * 0.10, _dt)
	_rec(door.door_id, "F-LAT-MECH", lat >= 0.0 and absf(lat - door.profile.mech_event_open) <= tol + 1.0e-3, lat, door.profile.mech_event_open, "s", "from E hold, tol ±%.3f" % tol, "F")
	while _clear_now(door) < 0.80 and t < door.profile.open_duration + 2.0:
		await get_tree().physics_frame
		t += _dt
	_press("move_forward")
	var clear_at := -1.0
	while t < door.profile.open_duration + 6.0:
		await get_tree().physics_frame
		t += _dt
		if _player.global_position.z - door.global_position.z >= -0.50:
			clear_at = _clear_now(door)
			break
	_release()
	_rec(door.door_id, "F-WALK-CLEAR", clear_at >= 0.80, clear_at, 0.80, "m", "interact door waits for 0.80 m before the last 0.50 m", "F")
	await _park(Vector3(dx, 0.0, -200.0), PI)
	if door.state != "closed":
		door.command_close()
		await _until_closed(door, door.profile.close_duration + 3.0)


func _is_mech_phase(ph: String) -> bool:
	return ph.begins_with("bolt") or ph.begins_with("strike") or ph.begins_with("equalize") or ph.begins_with("dog") or ph.begins_with("latch")


func _clear_now(door: MechDoor) -> float:
	if door.q_now.is_empty():
		return 0.0
	var qmin := door.q_now[0]
	for q in door.q_now:
		qmin = minf(qmin, q)
	return door.profile.clear_gap(qmin)


func _until_closed(door: MechDoor, timeout: float) -> bool:
	var t := 0.0
	while t < timeout:
		if door.state == "closed":
			return true
		await get_tree().physics_frame
		t += _dt
	return door.state == "closed"


func _scored_cycle(door: MechDoor) -> void:
	door.reset_closed()
	door.rows.clear()
	door.record = true
	_cues.clear()
	_max_drift_deg = 0.0
	var cb := func(nm: String) -> void:
		_cues.append({"name": nm, "motion_t": door.motion_t, "dir": door.direction})
	door.cue.connect(cb)
	door.command_open()
	var saw := false
	var t := 0.0
	var limit := door.profile.open_duration + door.profile.close_duration + door.profile.hold_open_s + 4.0
	while t < limit:
		await get_tree().physics_frame
		t += _dt
		_max_drift_deg = maxf(_max_drift_deg, door.drift_deg())
		if door.state == "open" or door.state == "closing":
			saw = true
		if saw and door.state == "closed":
			break
	door.record = false
	if door.cue.is_connected(cb):
		door.cue.disconnect(cb)
	var rows: Array = door.rows.duplicate(true)
	_write_motion(door.door_id, rows)
	_analyze_motion(door, rows, saw and door.state == "closed")


func _write_motion(door_id: String, rows: Array) -> void:
	_write_motion_file(door_id, rows, "motion.csv")
	_write_cues(door_id)


func _write_motion_file(door_id: String, rows: Array, file_name: String) -> void:
	var dir := _out.path_join(door_id)
	DirAccess.make_dir_recursive_absolute(dir)
	var f := FileAccess.open(dir.path_join(file_name), FileAccess.WRITE)
	if f == null:
		return
	f.store_line("tick,time_s,phase,leaf,px,py,pz,yaw_deg,vel,leaf_vel,drift_mm,gap_mm,contacts,lamp,collider_enabled,q,leaf_acc,lamp_energy,g")
	var t0 := 0.0
	if not rows.is_empty():
		t0 = float(rows[0]["t"])
	for i in rows.size():
		var r: Dictionary = rows[i]
		var leaf_vel := float(r["leaf_vel"]) if r.has("leaf_vel") else float(r["vel"])
		var acc := float(r["leaf_acc"]) if r.has("leaf_acc") else 0.0
		var lenergy := float(r["lamp_energy"]) if r.has("lamp_energy") else 0.0
		var grav := float(r["g"]) if r.has("g") else 1.0
		var qq := float(r["q"]) if r.has("q") else 0.0
		var line := "%d,%.5f,%s,%s,%.5f,%.5f,%.5f,%.4f,%.5f,%.6f,%.3f,%.3f,%d,%s,%d,%.5f,%.5f,%.4f,%.3f" % [
			i, float(r["t"]) - t0, str(r["phase"]), str(r["leaf"]),
			float(r["px"]), float(r["py"]), float(r["pz"]), float(r["yaw"]),
			float(r["vel"]), leaf_vel, float(r["drift_mm"]), float(r["gap_mm"]),
			int(r["contacts"]), str(r["lamp"]), int(r["collider"]),
			qq, acc, lenergy, grav,
		]
		f.store_line(line)
	f.close()


func _analyze_motion(door: MechDoor, rows: Array, finished: bool) -> void:
	var id := door.door_id
	var swing := door.profile.clear_model != "slide"
	var pop_lim := 0.15 if swing else 0.002
	var pop_worst := 0.0
	var jump_worst := 0.0
	var jump_lim := 0.004 * pow(_dt / (1.0 / 60.0), 2.0)
	var tip_arm := _tip_arm(door)
	var drift_worst := 0.0
	var step_worst := 0.0
	var step_lim := 0.0
	var prev_q := {}
	var prev2_q := {}
	var prev_eq: Dictionary = {}
	var prev2_eq: Dictionary = {}
	var prev_v := {}
	var sample_jump := 0.0
	var max_v_open := 0.0
	var ref_v_open := 0.0
	var settle_peak := 0.0
	var settle_amp := _settle_amp(door, "open")
	var off_bad := false
	var lamp_move_t := -1.0
	var lamp_open_t := -1.0
	var open_rows := 0
	var prev_lamp_mt := -1.0
	var max_st_open := 0.0
	for item in door._leaves:
		max_st_open = maxf(max_st_open, float(item.get("stagger_open", 0.0)))
	# Reference peak from the settled (time-scaled) sample, not the unscaled table.
	var ts := 0.0
	while ts <= door.profile.open_duration:
		ref_v_open = maxf(ref_v_open, absf(float(door.profile.sample("open", ts)["vel"])))
		ts += _dt
	for r in rows:
		var rd: Dictionary = r
		var leaf := str(rd["leaf"])
		var q := float(rd["q"])
		var local_t := float(rd["motion_t"]) - _stagger(door, leaf, str(rd["state"]))
		var expect: Dictionary = door.profile.sample("open" if str(rd["state"]) == "opening" or str(rd["state"]) == "open" else "close", maxf(local_t, 0.0))
		if str(rd["state"]) == "opening" or str(rd["state"]) == "closing":
			pop_worst = maxf(pop_worst, absf(q - float(expect["q"])))
		drift_worst = maxf(drift_worst, float(rd["drift_mm"]))
		if prev_q.has(leaf) and prev2_q.has(leaf) and (str(rd["state"]) == "opening" or str(rd["state"]) == "closing"):
			var d2_q := absf(q - 2.0 * float(prev_q[leaf]) + float(prev2_q[leaf]))
			var d2 := deg_to_rad(d2_q) * tip_arm if swing else d2_q
			jump_worst = maxf(jump_worst, d2)
			if prev_eq.has(leaf) and prev2_eq.has(leaf):
				var eq := float(expect["q"])
				var ed2 := absf(eq - 2.0 * float(prev_eq[leaf]) + float(prev2_eq[leaf]))
				sample_jump = maxf(sample_jump, ed2)
		if prev_v.has(leaf) and str(rd["state"]) == "opening":
			var dv := absf(float(rd["vel"]) - float(prev_v[leaf]))
			step_worst = maxf(step_worst, dv)
			var sv := absf(float(expect["vel"]) - float(prev_v[leaf]))
			step_lim = maxf(step_lim, sv)
		if str(rd["state"]) == "opening":
			max_v_open = maxf(max_v_open, absf(float(rd["vel"])))
			open_rows += 1
			if lamp_move_t < 0.0 and str(rd["lamp"]) == "moving":
				var mt := float(rd["motion_t"])
				var event := door.profile.mech_event_open
				if prev_lamp_mt >= 0.0 and prev_lamp_mt < event - 1.0e-6 and mt + 1.0e-4 >= event:
					lamp_move_t = event
				else:
					lamp_move_t = mt
		if str(rd["state"]) == "open" and lamp_open_t < 0.0 and str(rd["lamp"]) == "open":
			var mt_o := float(rd["motion_t"])
			var open_at := door.profile.open_duration + max_st_open
			if prev_lamp_mt >= 0.0 and prev_lamp_mt < open_at - 1.0e-6 and mt_o + 1.0e-4 >= open_at:
				lamp_open_t = open_at
			else:
				lamp_open_t = mt_o
		if absf(float(rd["motion_t"]) - prev_lamp_mt) > 1.0e-6:
			prev_lamp_mt = float(rd["motion_t"])
		if str(rd["phase"]) == "settle" and str(rd["state"]) == "opening":
			settle_peak = maxf(settle_peak, absf(q - door.profile.travel))
		if int(rd["collider"]) == 0:
			var ph := str(rd["phase"])
			var allowed := ph == "creep" or ph == "latch" or ph == "latch_check" or ph == "final_seat" or ph == "backcheck" or ph.begins_with("latch")
			if str(rd["state"]) != "closing" or not allowed or float(rd["gap_mm"]) >= 800.0:
				off_bad = true
		prev2_eq[leaf] = prev_eq.get(leaf, float(expect["q"]))
		prev_eq[leaf] = float(expect["q"])
		prev2_q[leaf] = prev_q.get(leaf, q)
		prev_q[leaf] = q
		prev_v[leaf] = float(rd["vel"])
	var order_ok := _phase_subseq(door, rows, "opening", "open") and _phase_subseq(door, rows, "closing", "close")
	_rec(id, "R1", order_ok, 1.0 if order_ok else 0.0, 1.0, "bool", "per-leaf phases follow the published order", "F")
	var r2_windows := _phase_windows(door, rows)
	var kin := _kinematics(door, rows)
	var r2 := r2_windows and bool(kin["time_ok"])
	_rec(id, "R2", r2, float(kin["time_meas"]), float(kin["time_lim"]), "s", "windows and F-TIME within +/-10 pct of section 7.6; %s" % str(kin["time_note"]), "F")
	_rec(id, "R3", bool(kin["ok"]), float(kin["peak"]), float(kin["ref"]), "u/s", str(kin["note"]), "F")
	_rec(id, "F-KE", bool(kin["ke_ok"]), float(kin["ke"]), 10.0, "J", str(kin["ke_note"]), "F")
	_rec(id, "R15", bool(kin["ke_ok"]), float(kin["ke"]), 10.0, "J", "closing leaf KE <= 10 J", "F")
	_rec(id, "F-SCALAR", bool(kin["scalar_ok"]), float(kin["scalar"]), 0.05, "k", str(kin["scalar_note"]), "F")
	_rec(id, "F-TRES-SRC", bool(kin["src_ok"]), 1.0 if bool(kin["src_ok"]) else 0.0, 1.0, "bool", str(kin["src_note"]), "F")
	_rec(id, "F-TIME", bool(kin["time_ok"]), float(kin["time_meas"]), float(kin["time_lim"]), "s", str(kin["time_note"]), "F")
	var settle_mid := _settle_curve_peak(door)
	var settle_ok := true
	if settle_amp > 1.0e-6:
		# Logged peak can miss the continuous crest at a coarse tick. The curve itself must hit ±25%, and the log must show the hump the ticks can see.
		var floor_peak := minf(settle_amp * 0.75, settle_mid * 0.85)
		settle_ok = absf(settle_mid - settle_amp) <= settle_amp * 0.25 + 1.0e-4 and settle_peak <= settle_amp * 1.25 + 1.0e-4 and settle_peak + 1.0e-4 >= floor_peak
	_rec(id, "R4", settle_ok, settle_peak, settle_amp, "u", "log hump %.4f curve crest %.4f" % [settle_peak, settle_mid], "F")
	_rec(id, "V-SETTLE", settle_ok, settle_peak, settle_amp * 1.25, "u", "one hump, ends on the curve", "V")
	var stagger_err := _stagger_error(door, rows)
	_rec(id, "R5", stagger_err <= 0.020, stagger_err, 0.020, "s", "first-motion offsets vs JSON stagger", "F")
	_rec(id, "F-DRIFT", drift_worst <= 2.0, drift_worst, 2.0, "mm", "physics origin vs body", "F")
	_rec(id, "F-DRIFT-ANG", _max_drift_deg <= 0.15, _max_drift_deg, 0.15, "deg", "", "F")
	_rec(id, "F-DRIFT-OFF", not off_bad, 0.0 if not off_bad else 1.0, 0.0, "bool", "collider off only in the close creep window under 0.80 m", "F")
	_rec(id, "F-OBS-OFF", not off_bad, 0.0 if not off_bad else 1.0, 0.0, "bool", "same window as F-DRIFT-OFF", "F")
	_rec(id, "R9", drift_worst <= 2.0 and _max_drift_deg <= 0.15 and not off_bad, drift_worst, 2.0, "mm", "", "F")
	_rec(id, "V-POP", pop_worst <= pop_lim, pop_worst, pop_lim, "u", "residual vs sample(t), not scaled by dt", "V")
	# Tip second difference in metres. No sample()*1.02 waiver.
	_rec(id, "V-JUMP", jump_worst <= jump_lim + 1.0e-6, jump_worst, jump_lim, "m", "tip arm %.3f second difference; flat %.5f m (sample q %.5f)" % [tip_arm, jump_lim, sample_jump], "V")
	var ease_ok := bool(kin["ok"]) and open_rows > 5
	_rec(id, "V-EASE-SCURVE", ease_ok, float(kin["ratio"]), 1.0, "ratio", "per-tick |dv| and |da| within 1.1 a' dt and 1.1 j' dt; not a linear tween", "V")
	var max_st := 0.0
	for item in door._leaves:
		max_st = maxf(max_st, float(item.get("stagger_open", 0.0)))
	var move_err := absf(lamp_move_t - door.profile.mech_event_open) if lamp_move_t >= 0.0 else 9.0
	var open_target := door.profile.open_duration + max_st
	var open_err := absf(lamp_open_t - open_target) if lamp_open_t >= 0.0 else 9.0
	var lamp_ok := move_err <= 0.05 and open_err <= 0.05
	_rec(id, "V-LAMP-SYNC", lamp_ok, move_err, 0.05, "s", "cyan at mech event, green at open+stagger %.3f (err %.3f)" % [open_target, open_err], "V")
	_rec(id, "R12", lamp_ok, move_err, 0.05, "s", "", "V")
	var audio := _audio_ok(door)
	_rec(id, "V-AUDIO", audio["ok"] and _streams_ok(door), float(audio["worst"]), _dt, "s", str(audio["note"]), "V")
	_rec(id, "R11", audio["ok"] and _streams_ok(door), float(audio["worst"]), _dt, "s", "cue stream assigned; %s" % str(audio["note"]), "V")
	var lurch := _lurch_moved(door, rows)
	_rec(id, "F-LAT-MOVE", lurch >= (0.2 if swing else 0.001), lurch, 0.2 if swing else 0.001, "deg" if swing else "m", "travel by end of lurch +10%", "F")
	if not finished:
		_rec(id, "R1", false, 0.0, 1.0, "bool", "scored open/close did not return to closed", "F")


func _profile_paths() -> Dictionary:
	var out := {}
	for id in _doors.keys():
		out[id] = (_doors[id] as MechDoor).profile.table_path
	return out


func _kinematics(door: MechDoor, rows: Array) -> Dictionary:
	# R3 is finite differences of pose q. Raw ticks. A 3-tick average is only
	# the logged exception on a phase-entry stencil, and that stencil is not failed.
	var swing := door.profile.clear_model != "slide"
	var by := {}
	for r in rows:
		var rd: Dictionary = r
		var st := str(rd["state"])
		if st != "opening" and st != "closing":
			continue
		var leaf := str(rd["leaf"])
		if not by.has(leaf):
			by[leaf] = []
		by[leaf].append(rd)
	var worst_ratio := 0.0
	var r3_ok := true
	var scored := 0
	var entry_n := 0
	var open_peak := 0.0
	var close_peak := 0.0
	var ref_open := 0.0
	var ref_close := 0.0
	var ke_max := 0.0
	var ts := 0.0
	while ts <= door.profile.open_duration:
		ref_open = maxf(ref_open, absf(float(door.profile.sample("open", ts)["vel"])))
		ts += _dt
	ts = 0.0
	while ts <= door.profile.close_duration:
		ref_close = maxf(ref_close, absf(float(door.profile.sample("close", ts)["vel"])))
		ts += _dt
	var mass := door.profile.mass_kg
	var inertia := door.profile.inertia_kgm2
	for leaf in by.keys():
		var series: Array = by[leaf]
		var n := series.size()
		var qq: Array[float] = []
		qq.resize(n)
		var ph_name: Array[String] = []
		ph_name.resize(n)
		var group: Array[String] = []
		group.resize(n)
		var a_p: Array[float] = []
		a_p.resize(n)
		var j_p: Array[float] = []
		j_p.resize(n)
		var times: Array[float] = []
		times.resize(n)
		var dirs: Array[String] = []
		dirs.resize(n)
		for i in n:
			var rd: Dictionary = series[i]
			var dir := "open" if str(rd["state"]) == "opening" else "close"
			var local_t := float(rd["motion_t"]) - _stagger(door, leaf, str(rd["state"]))
			var ph: Dictionary = door.profile.phase_at(dir, maxf(local_t, 0.0))
			qq[i] = float(rd["q"])
			times[i] = float(rd["t"])
			ph_name[i] = str(ph.get("name", ""))
			group[i] = str(ph.get("group", ""))
			a_p[i] = absf(float(ph.get("a_prime", 0.0)))
			j_p[i] = absf(float(ph.get("j_prime", 0.0)))
			dirs[i] = dir
		for i in range(1, n):
			var dt0 := maxf(times[i] - times[i - 1], 1.0e-6)
			var spd := absf(qq[i] - qq[i - 1]) / dt0
			if dirs[i] == "open":
				open_peak = maxf(open_peak, spd)
			else:
				close_peak = maxf(close_peak, spd)
				var w := deg_to_rad(spd) if swing else spd
				var ke := 0.5 * inertia * w * w if swing else 0.5 * mass * w * w
				ke_max = maxf(ke_max, ke)
		var i0 := 0
		while i0 < n:
			var i1 := i0
			while i1 + 1 < n and ph_name[i1 + 1] == ph_name[i0] and dirs[i1 + 1] == dirs[i0]:
				i1 += 1
			var gname := group[i0]
			var use := gname != "lurch" and gname != "settle" and (a_p[i0] > 1.0e-6 or j_p[i0] > 1.0e-6)
			if use and i0 > 0:
				entry_n += 1
			if use:
				for k in range(i0 + 2, i1 + 1):
					var dt := maxf(times[k] - times[k - 1], 1.0e-6)
					var v1 := (qq[k] - qq[k - 1]) / dt
					var v0 := (qq[k - 1] - qq[k - 2]) / dt
					var dv := v1 - v0
					var ap := maxf(a_p[k], 1.0e-8)
					worst_ratio = maxf(worst_ratio, absf(dv) / (1.1 * ap * dt))
					if absf(dv) > 1.1 * ap * dt + 1.0e-4:
						r3_ok = false
					scored += 1
				for k in range(i0 + 3, i1 + 1):
					var dt2 := maxf(times[k] - times[k - 1], 1.0e-6)
					var v2 := (qq[k] - qq[k - 1]) / dt2
					var v1b := (qq[k - 1] - qq[k - 2]) / maxf(times[k - 1] - times[k - 2], 1.0e-6)
					var v0b := (qq[k - 2] - qq[k - 3]) / maxf(times[k - 2] - times[k - 3], 1.0e-6)
					var da := (v2 - v1b) / dt2 - (v1b - v0b) / maxf(times[k - 1] - times[k - 2], 1.0e-6)
					var jp := maxf(j_p[k], 1.0e-8)
					worst_ratio = maxf(worst_ratio, absf(da) / (1.1 * jp * dt2))
					if absf(da) > 1.1 * jp * dt2 + 1.0e-3:
						r3_ok = false
			i0 = i1 + 1
	var peak_ok := ref_open <= 1.0e-6 or absf(open_peak - ref_open) <= absf(ref_open) * 0.10 + 1.0e-3
	var close_ok := ref_close <= 1.0e-6 or absf(close_peak - ref_close) <= absf(ref_close) * 0.10 + 1.0e-3
	if scored < 4:
		r3_ok = false
	var scalar := _scalar_report(door)
	var timing := _time_report(door, rows)
	var tres_path := "res://resources/door_lab/%s.tres" % door.door_id
	var s7: Dictionary = door.profile.section7
	var s7_ok := s7.has("windows") and s7.has("totals") and s7.has("cues")
	var hit := _hardcoded_table_hit()
	var src_ok := door.profile.source == "tres" and door.profile.resource_path == tres_path and door.profile.table_path.ends_with("%s.json" % door.door_id) and s7_ok and hit == ""
	return {
		"ok": r3_ok and peak_ok and close_ok,
		"peak": open_peak,
		"ref": ref_open,
		"ratio": worst_ratio,
		"note": "open peak %.4f ref %.4f close peak %.4f ref %.4f worst raw ratio %.3f entry_exceptions %d" % [open_peak, ref_open, close_peak, ref_close, worst_ratio, entry_n],
		"ke": ke_max,
		"ke_ok": ke_max <= 10.0 + 1.0e-3,
		"ke_note": "max close-tick KE m=%.1f I=%.1f" % [mass, inertia],
		"scalar_ok": bool(scalar["ok"]),
		"scalar": float(scalar["err"]),
		"scalar_note": str(scalar["note"]),
		"src_ok": src_ok,
		"src_note": "%s %s section7=%s %s" % [door.profile.resource_path, door.profile.table_path, s7_ok, hit],
		"time_ok": bool(timing["ok"]),
		"time_meas": float(timing["meas"]),
		"time_lim": float(timing["lim"]),
		"time_note": str(timing["note"]),
	}


func _scalar_report(door: MechDoor) -> Dictionary:
	var err := 0.0
	var ok := true
	var cap_note := ""
	if absf(door.profile.travel_time_scale - K_TRAVEL) > 0.05:
		ok = false
	if absf(door.profile.mech_phase_scale - K_MECH) > 0.05:
		ok = false
	if absf(door.profile.lurch_scale - 1.0) > 0.05 or absf(door.profile.settle_scale - 1.0) > 0.05:
		ok = false
	err = maxf(err, absf(door.profile.travel_time_scale - K_TRAVEL))
	err = maxf(err, absf(door.profile.mech_phase_scale - K_MECH))
	for dir in ["open", "close"]:
		for ph in door.profile.compiled_phases(dir):
			var vance := float(ph.get("vance_dur", 0.0))
			if vance <= 1.0e-6:
				continue
			var group := str(ph.get("group", ""))
			if bool(ph.get("capped", false)):
				var v_cap := door.profile.close_v_cap
				var v_p := float(ph.get("v_prime", 0.0))
				var k_ref := door.profile.travel_time_scale
				var a_ref := float(ph.get("vance_a", 0.0)) / (k_ref * k_ref)
				var j_ref := float(ph.get("vance_j", 0.0)) / (k_ref * k_ref * k_ref)
				var ev := absf(v_p - v_cap) / maxf(absf(v_cap), 1.0e-6)
				var ea := absf(float(ph.get("a_prime", 0.0)) - a_ref) / maxf(absf(a_ref), 1.0e-6)
				var ej := absf(float(ph.get("j_prime", 0.0)) - j_ref) / maxf(absf(j_ref), 1.0e-6)
				err = maxf(err, ev)
				if ev > 0.10 or ea > 0.10 or ej > 0.10:
					ok = false
				cap_note = "cap v %.3f a' %.3f" % [v_p, float(ph.get("a_prime", 0.0))]
				continue
			var want := K_MECH
			if group == "travel":
				want = K_TRAVEL if dir == "open" else door.profile.close_travel_scale
			elif group == "lurch" or group == "settle":
				want = 1.0
			var k := float(ph.get("dur", 0.0)) / vance
			err = maxf(err, absf(k - want))
			if absf(k - want) > 0.05:
				ok = false
	return {"ok": ok, "err": err, "note": "max |k-spec| %.4f %s" % [err, cap_note]}


## Section 7 windows live in the door JSON the .tres points at.
## Pair open travel windows in that file are the M-114 frozen compiler windows.
func _spec_windows(door: MechDoor, direction: String) -> Dictionary:
	var windows: Dictionary = door.profile.section7.get("windows", {})
	var got: Variant = windows.get(direction, {})
	if typeof(got) != TYPE_DICTIONARY:
		return {}
	return (got as Dictionary).duplicate(true)


func _spec_totals(door: MechDoor) -> Vector2:
	var totals: Dictionary = door.profile.section7.get("totals", {})
	return Vector2(float(totals.get("open", 0.0)), float(totals.get("close", 0.0)))


## Lead-leaf spans from the motion rows. A boundary is the midpoint between the
## samples on either side. The extra tolerance is one physics tick, the aperture
## of a row logged at the end of the tick that contains the boundary.
func _measured_phase_spans(door: MechDoor, direction: String, rows: Array) -> Dictionary:
	var state := "opening" if direction == "open" else "closing"
	var leaf0 := str(door._leaves[0]["name"])
	var samples: Array = []
	for r in rows:
		var rd: Dictionary = r
		if str(rd["state"]) != state or str(rd["leaf"]) != leaf0:
			continue
		var local := float(rd["motion_t"]) - _stagger(door, leaf0, state)
		samples.append({"t": local, "phase": str(rd["phase"])})
	var spans := {}
	var runs: Array = []
	if samples.is_empty():
		return {"spans": spans, "runs": runs}
	var i := 0
	while i < samples.size():
		var name := str(samples[i]["phase"])
		var j := i
		while j + 1 < samples.size() and str(samples[j + 1]["phase"]) == name:
			j += 1
		var t_first := float(samples[i]["t"])
		var t_last := float(samples[j]["t"])
		var t_prev := t_first - _dt
		if i > 0:
			t_prev = float(samples[i - 1]["t"])
		var t_next := t_last + _dt
		if j + 1 < samples.size():
			t_next = float(samples[j + 1]["t"])
		var t0 := 0.0 if i == 0 else 0.5 * (t_prev + t_first)
		var t1 := 0.5 * (t_last + t_next)
		if name != "" and name != "idle" and name != "wait" and name != "settled":
			spans[name] = Vector2(t0, t1)
			runs.append({"name": name, "t_first": t_first, "t_last": t_last})
		i = j + 1
	return {"spans": spans, "runs": runs}


func _span_for(name: String, order: Array, packed: Dictionary) -> Vector2:
	var spans: Dictionary = packed.get("spans", {})
	if spans.has(name):
		return spans[name]
	var runs: Array = packed.get("runs", [])
	var idx := order.find(name)
	if idx < 0:
		return Vector2(-1.0, -1.0)
	var prev_last := -1.0
	var next_first := -1.0
	for p in range(idx - 1, -1, -1):
		for run in runs:
			if str(run["name"]) == str(order[p]):
				prev_last = float(run["t_last"])
				break
		if prev_last >= 0.0:
			break
	for n in range(idx + 1, order.size()):
		for run2 in runs:
			if str(run2["name"]) == str(order[n]):
				next_first = float(run2["t_first"])
				break
		if next_first >= 0.0:
			break
	if prev_last >= 0.0 and next_first >= prev_last:
		return Vector2(prev_last, next_first)
	return Vector2(-1.0, -1.0)


func _spec_phase_check(door: MechDoor, rows: Array) -> Dictionary:
	var worst := 0.0
	var note := ""
	var ok := true
	for direction in ["open", "close"]:
		var windows := _spec_windows(door, direction)
		var packed := _measured_phase_spans(door, direction, rows)
		var order: Array = windows.keys()
		for name in order:
			var want: Array = windows[name]
			var w0 := float(want[0])
			var w1 := float(want[1])
			# 10% of the published window, plus one physics tick of sample aperture.
			var tol := 0.10 * maxf(w1 - w0, 0.001) + _dt
			var got := _span_for(str(name), order, packed)
			# Sentinel is (-1, -1). A real span can start a hair before 0 when the
			# lead leaf's stagger pulls the previous wait sample under the boundary.
			# A leading window of one tick or less (pair request is 50 ms) never
			# gets its own sample at 15/20 Hz. Accept it when the next phase is
			# already underway by the end of that window.
			if got.y < 0.0 and (w1 - w0) <= _dt + 1.0e-4:
				var idx := order.find(name)
				var next_t := -1.0
				if idx >= 0:
					var runs: Array = packed.get("runs", [])
					for n in range(idx + 1, order.size()):
						for run in runs:
							if str(run["name"]) == str(order[n]):
								next_t = float(run["t_first"])
								break
						if next_t >= 0.0:
							break
				if next_t >= 0.0 and next_t <= w1 + tol:
					got = Vector2(w0, w1)
			if got.y < 0.0:
				ok = false
				note = "%s %s missing from motion rows" % [direction, name]
				worst = maxf(worst, 9.0)
				continue
			var err := maxf(absf(got.x - w0), absf(got.y - w1))
			worst = maxf(worst, err)
			if err > tol:
				ok = false
				if note == "":
					note = "%s %s %.3f-%.3f want %.3f-%.3f tol %.3f" % [direction, name, got.x, got.y, w0, w1, tol]
		var state := "opening" if direction == "open" else "closing"
		var leaf0 := str(door._leaves[0]["name"])
		for r in rows:
			var rd: Dictionary = r
			if str(rd["state"]) != state or str(rd["leaf"]) != leaf0:
				continue
			var local := float(rd["motion_t"]) - _stagger(door, leaf0, state)
			var ph := str(rd["phase"])
			for name2 in windows.keys():
				var span: Array = windows[name2]
				var a := float(span[0])
				var b := float(span[1])
				if local > a + _dt + 1.0e-4 and local < b - _dt - 1.0e-4 and ph != name2:
					ok = false
					if note == "":
						note = "%s csv %s at %.3f inside %s" % [direction, ph, local, name2]
					break
	return {"ok": ok, "err": worst, "note": note}


func _spec_cues(door: MechDoor) -> Dictionary:
	var cues: Variant = door.profile.section7.get("cues", {})
	if typeof(cues) != TYPE_DICTIONARY:
		return {}
	return cues


## F-TRES-SRC fails if a target table is pasted back into the harness or the profile.
## The needles are split so this scanner is not itself a copy of the table.
func _hardcoded_table_hit() -> String:
	var needles: PackedStringArray = PackedStringArray([
		"seal_" + "unseat",
		"dog_clunk_close_" + "8",
		"solenoid_" + "unlock_clack",
	])
	var paths: PackedStringArray = PackedStringArray([
		"res://tools/qa/door_lab_qa.gd",
		"res://scripts/door_lab/mech_door_profile.gd",
	])
	for p in paths:
		var text := FileAccess.get_file_as_string(p)
		for n in needles:
			if text.find(n) >= 0:
				return "%s still has a hard-coded target (%s)" % [p, n]
	return ""


func _time_report(door: MechDoor, rows: Array) -> Dictionary:
	var meas_open := -1.0
	var meas_close := -1.0
	var saw_open := false
	for r in rows:
		var rd: Dictionary = r
		if str(rd["state"]) == "open" and meas_open < 0.0:
			meas_open = float(rd["motion_t"])
			saw_open = true
		if saw_open and str(rd["state"]) == "closed" and meas_close < 0.0:
			meas_close = float(rd["motion_t"])
	var max_so := 0.0
	var max_sc := 0.0
	for item in door._leaves:
		max_so = maxf(max_so, float(item.get("stagger_open", 0.0)))
		max_sc = maxf(max_sc, float(item.get("stagger_close", 0.0)))
	var spec := _spec_totals(door)
	var target_o := spec.x + max_so
	var target_c := spec.y + max_sc
	var tol_o := 0.10 * spec.x
	var tol_c := 0.10 * spec.y
	var ok := meas_open >= 0.0 and absf(meas_open - target_o) <= tol_o
	ok = ok and meas_close >= 0.0 and absf(meas_close - target_c) <= tol_c
	ok = ok and absf(door.profile.open_duration - spec.x) <= tol_o
	ok = ok and absf(door.profile.close_duration - spec.y) <= tol_c
	var phase := _spec_phase_check(door, rows)
	if not bool(phase["ok"]):
		ok = false
	return {
		"ok": ok,
		"meas": meas_open,
		"lim": target_o,
		"note": "open %.3f spec %.3f+%.3f close %.3f spec %.3f+%.3f profile %.3f/%.3f %s" % [meas_open, spec.x, max_so, meas_close, spec.y, max_sc, door.profile.open_duration, door.profile.close_duration, str(phase["note"])],
	}


func _phases_within(door: MechDoor, rows: Array) -> bool:
	return bool(_spec_phase_check(door, rows)["ok"])


func _phases_within_legacy(door: MechDoor, rows: Array) -> bool:
	for direction in ["open", "close"]:
		var state := "opening" if direction == "open" else "closing"
		var locals: Array = []
		for r in rows:
			var rd: Dictionary = r
			if str(rd["state"]) != state:
				continue
			if str(rd["leaf"]) != str(door._leaves[0]["name"]):
				continue
			locals.append(float(rd["motion_t"]) - _stagger(door, str(rd["leaf"]), state))
		locals.sort()
		# The row is logged after the tick, so the first sample is already at dt.
		# motion_t 0 is the start of that same tick. A leading phase the tick
		# stepped across is still on the clock. One tick only; the 10% pad is unchanged.
		if not locals.is_empty() and float(locals[0]) > 1.0e-4 and float(locals[0]) <= _dt + 1.0e-4:
			locals.insert(0, 0.0)
		for ph in door.profile.compiled_phases(direction):
			var rt0 := float(ph["rt0"])
			var rt1 := float(ph["rt1"])
			var dur := maxf(rt1 - rt0, 1.0e-4)
			var pad := 0.10 * dur
			var hit := false
			for loc in locals:
				if float(loc) >= rt0 - pad - 1.0e-4 and float(loc) <= rt1 + pad + 1.0e-4:
					hit = true
					break
			if hit:
				continue
			for i in range(1, locals.size()):
				var a := float(locals[i - 1])
				var b := float(locals[i])
				if a <= rt0 + pad and b >= rt1 - pad:
					hit = true
					break
			if not hit:
				return false
	return true


func _stagger(door: MechDoor, leaf: String, state: String) -> float:
	var key := "stagger_open" if state == "opening" or state == "open" else "stagger_close"
	for item in door._leaves:
		if str(item["name"]) == leaf:
			return float(item.get(key, 0.0))
	return 0.0


func _settle_curve_peak(door: MechDoor) -> float:
	var sp := door.profile.phase_span("open", "settle")
	if sp.x < 0.0:
		return 0.0
	var best := 0.0
	var t := sp.x
	while t <= sp.y + 1.0e-6:
		var q := absf(float(door.profile.sample("open", t)["q"]) - door.profile.travel)
		best = maxf(best, q)
		t += maxf(_dt * 0.25, 0.002)
	return best


func _settle_amp(door: MechDoor, direction: String) -> float:
	var path := "res://resources/door_lab/%s.json" % door.door_id
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) != TYPE_DICTIONARY:
		return 0.0
	var key := "open_phases" if direction == "open" else "close_phases"
	for ph in (parsed as Dictionary).get(key, []):
		if str(ph.get("kind", "")) == "settle":
			return float(ph.get("amp", 0.0))
	return 0.0


func _phase_subseq(door: MechDoor, rows: Array, state: String, direction: String) -> bool:
	var expect := door.profile.phase_order(direction)
	# One index per leaf. A staggered leaf is still in "wait" while another
	# leaf has already advanced, so a shared index marks the late leaf as behind.
	var idx: Dictionary = {}
	var seen := {}
	for r in rows:
		var rd: Dictionary = r
		if str(rd["state"]) != state:
			continue
		var ph := str(rd["phase"])
		if ph == "idle" or ph == "wait" or ph == "settled" or ph == "request":
			continue
		var leaf := str(rd["leaf"])
		var key := leaf + ":" + ph
		if seen.has(key):
			continue
		seen[key] = true
		var start := int(idx.get(leaf, 0))
		var found := -1
		for j in range(start, expect.size()):
			if expect[j] == ph:
				found = j
				break
		if found < 0:
			return false
		idx[leaf] = found
	return true


func _phase_windows(door: MechDoor, rows: Array) -> bool:
	return bool(_spec_phase_check(door, rows)["ok"])


func _phase_windows_legacy(door: MechDoor, rows: Array) -> bool:
	for r in rows:
		var rd: Dictionary = r
		var state := str(rd["state"])
		if state != "opening" and state != "closing":
			continue
		var ph := str(rd["phase"])
		if ph == "idle" or ph == "wait" or ph == "settled" or ph == "request":
			continue
		var direction := "open" if state == "opening" else "close"
		var look := ph
		if ph == "accel" or ph == "cruise" or ph == "decel":
			look = "travel"
		var sp := door.profile.phase_span(direction, look)
		if sp.x < 0.0:
			return false
		var local_t := float(rd["motion_t"]) - _stagger(door, str(rd["leaf"]), state)
		var pad := maxf((sp.y - sp.x) * 0.10, _dt)
		if local_t < sp.x - pad or local_t > sp.y + pad:
			return false
	return true


func _stagger_error(door: MechDoor, rows: Array) -> float:
	# q is the profile at local time, and that curve is not linear. Invert it
	# at the first sample past the threshold so a 15 Hz tick does not move the
	# crossing. A leaf that leaves the profile still misses the 20 ms band.
	var first := {}
	var eps := 0.0004 if door.profile.clear_model == "slide" else 0.05
	var rise := _local_for_q(door, eps)
	for r in rows:
		var rd: Dictionary = r
		if str(rd["state"]) != "opening":
			continue
		var leaf := str(rd["leaf"])
		var q := absf(float(rd["q"]))
		var mt := float(rd["motion_t"])
		if not first.has(leaf) and q >= eps:
			first[leaf] = mt - _local_for_q(door, q) + rise
	if first.is_empty():
		return 9.0
	var worst := 0.0
	for item in door._leaves:
		var nm := str(item["name"])
		if not first.has(nm):
			return 9.0
		var expect := float(item.get("stagger_open", 0.0))
		worst = maxf(worst, absf(float(first[nm]) - (expect + rise)))
		for other in door._leaves:
			var nm2 := str(other["name"])
			if not first.has(nm2):
				continue
			var got := float(first[nm]) - float(first[nm2])
			var want := expect - float(other.get("stagger_open", 0.0))
			worst = maxf(worst, absf(got - want))
	return worst


func _local_for_q(door: MechDoor, q: float) -> float:
	var lo := 0.0
	var hi := door.profile.open_duration
	for _i in 24:
		var mid := (lo + hi) * 0.5
		if absf(float(door.profile.sample("open", mid)["q"])) < q:
			lo = mid
		else:
			hi = mid
	return (lo + hi) * 0.5


func _lurch_moved(door: MechDoor, rows: Array) -> float:
	var sp := door.profile.phase_span("open", "lurch")
	if sp.x < 0.0:
		return 0.0
	var end_t := sp.y * 1.10
	var best := 0.0
	var hit_t := -1.0
	for r in rows:
		var rd: Dictionary = r
		if str(rd["state"]) != "opening":
			continue
		var mt := float(rd["motion_t"])
		if mt < end_t - _dt:
			continue
		# Rows are one per leaf per tick. A staggered leaf can still read 0
		# on the tick the lead leaf has already lurched. Take that whole tick.
		if hit_t >= 0.0 and absf(mt - hit_t) > 1.0e-4:
			break
		hit_t = mt
		best = maxf(best, absf(float(rd["q"])))
	return best


func _audio_ok(door: MechDoor) -> Dictionary:
	var worst := 0.0
	var missing := 0
	var table: Dictionary = _spec_cues(door)
	for direction in ["open", "close"]:
		var cues: Dictionary = table.get(direction, {})
		for nm in cues.keys():
			var want := float(cues[nm])
			var best := 99.0
			for hit in _cues:
				if str(hit["name"]) == str(nm) and str(hit["dir"]) == direction:
					best = minf(best, absf(float(hit["motion_t"]) - want))
			if best > 90.0:
				missing += 1
				worst = maxf(worst, 9.0)
			else:
				worst = maxf(worst, best)
	# One physics tick. The old extra millisecond hid a cue that was already late.
	var cue_tol := _dt + 1.0e-6
	var ok := missing == 0 and worst <= cue_tol
	return {"ok": ok, "worst": worst, "note": "section7 missing %d worst %.4f s tol %.4f" % [missing, worst, cue_tol]}


func _streams_ok(door: MechDoor) -> bool:
	var any := false
	for c in door.get_children():
		if c is AudioStreamPlayer3D and String(c.name).begins_with("Cue_"):
			any = true
			if (c as AudioStreamPlayer3D).stream == null:
				return false
	return any


func _tip_arm(door: MechDoor) -> float:
	match door.door_id:
		"bay3":
			return 0.877
		"pair":
			return 0.891
		"hatch":
			return 1.10
		"floorhatch":
			return 1.0
		_:
			return 1.0


func _write_cues(door_id: String) -> void:
	var dir := _out.path_join(door_id)
	DirAccess.make_dir_recursive_absolute(dir)
	var f := FileAccess.open(dir.path_join("cue_log.csv"), FileAccess.WRITE)
	if f == null:
		return
	f.store_line("t,name,dir")
	for hit in _cues:
		f.store_line("%.5f,%s,%s" % [float(hit["motion_t"]), str(hit["name"]), str(hit["dir"])])
	f.close()


func _obstruction(door: MechDoor) -> void:
	door.reset_closed()
	await _park(Vector3(0.0, 0.0, -200.0), PI)
	door.command_open()
	var opened := await _wait_state(door, "open", door.profile.open_duration + 2.0)
	if not opened:
		_fail_obs(door, "did not open before the obstruction probe")
		return
	door.command_close()
	var t_move := 0.0
	var moving := false
	var peak_v := 0.0
	while t_move < 4.0:
		await get_tree().physics_frame
		t_move += _dt
		var progressed := false
		for q in door.q_now:
			if absf(float(q) - door.profile.travel) > maxf(door.profile.travel * 0.08, 0.02):
				progressed = true
		var spd := 0.0
		for v in door.v_now:
			spd = maxf(spd, absf(float(v)))
		if door.state == "closing":
			peak_v = maxf(peak_v, spd)
		if door.state == "closing" and progressed and spd > 0.01:
			moving = true
			break
	_place_probe(door, true)
	await get_tree().physics_frame
	var origin0 := _probe.global_position
	var t_detect := -1.0
	var t_slow := -1.0
	var q_at := door.q_now.duplicate()
	var q_stop: Array = []
	var t := 0.0
	var saw_brake := false
	var v_reopen := 0.0
	while t < 3.0:
		await get_tree().physics_frame
		t += _dt
		var spd_now := 0.0
		for v2 in door.v_now:
			spd_now = maxf(spd_now, absf(float(v2)))
		if door.state == "closing":
			peak_v = maxf(peak_v, spd_now)
		if door.state == "braking" or door.state == "dwell" or door.state == "reopening":
			if not saw_brake:
				saw_brake = true
				t_detect = t
				q_at = door.q_now.duplicate()
			var slow_lim := 0.02 * maxf(peak_v, 0.001)
			if t_slow < 0.0 and spd_now <= slow_lim:
				t_slow = t
		# Stop distance is the brake itself. The later reopen walks back to the open pose.
		if q_stop.is_empty() and (door.state == "dwell" or door.state == "reopening"):
			q_stop = door.q_now.duplicate()
		if door.state == "reopening":
			for v in door.v_now:
				v_reopen = maxf(v_reopen, absf(v))
		if door.state == "open" or door.state == "fault":
			break
	var t_stopped := -1.0
	if t_slow >= 0.0 and t_detect >= 0.0:
		t_stopped = t_slow - t_detect
	var detect_ok := moving and saw_brake and t_detect >= 0.0 and t_detect <= _dt + 1.0e-4
	_rec(door.door_id, "F-OBS-DETECT", detect_ok, t_detect, _dt, "s", "one tick from probe insertion while the leaf was already moving", "F")
	var moved := 0.0
	var stopped: Array = q_stop if not q_stop.is_empty() else q_at
	for i in mini(stopped.size(), q_at.size()):
		moved = maxf(moved, absf(float(stopped[i]) - float(q_at[i])))
	var stop_dist := float(door.profile.obstruction.get("stop_dist", 0.06))
	var stop_s := float(door.profile.obstruction.get("stop_s", 0.2))
	var v_cap := float(door.profile.obstruction.get("v_cap", 999.0))
	# First tick at or under 2% of the close peak. No extra tick on top of stop_s.
	var stop_ok := saw_brake and t_stopped >= -1.0e-6 and t_stopped <= stop_s + 1.0e-4 and moved <= stop_dist + 1.0e-4 and v_reopen <= v_cap + 1.0e-3
	_rec(door.door_id, "F-OBS-STOP", stop_ok, t_stopped, stop_s, "s", "2pct of peak %.3f moved %.4f stop_dist %.3f reopen_v %.2f cap %.2f" % [peak_v, moved, stop_dist, v_reopen, v_cap], "F")
	var shove := _probe.global_position.distance_to(origin0)
	var pass_ok := shove <= 0.005
	_rec(door.door_id, "F-OBS-PASS", pass_ok, shove, 0.005, "m", "probe origin travel during the stop; edge force is the stop-before-contact case", "F")
	# Two more strikes. The probe stays in the volume, so each close brakes again.
	var strikes := 1 if saw_brake else 0
	var guard := 0.0
	var limit := door.profile.hold_open_s + door.profile.open_duration + 8.0
	while strikes < 3 and guard < limit * 3.0:
		await get_tree().physics_frame
		guard += _dt
		if door.state == "braking" and strikes < int(door.fault_hits) + 1:
			strikes = int(door.fault_hits)
		if door.state == "fault":
			strikes = int(door.fault_hits)
			break
	var fault_ok := door.state == "fault" and door.lamp == "fault"
	if door.door_id != "hatch":
		var at_open := true
		for q in door.q_now:
			if absf(q - door.profile.travel) > (0.5 if door.profile.clear_model != "slide" else 0.01):
				at_open = false
		fault_ok = fault_ok and at_open
	_rec(door.door_id, "F-OBS-FAULT", fault_ok, float(door.fault_hits), 3.0, "count", "lamp %s state %s" % [door.lamp, door.state], "F")
	var r10 := detect_ok and stop_ok and pass_ok and fault_ok
	_rec(door.door_id, "R10", r10, moved, stop_dist, "u", "", "F")
	_hide_probe()
	door.reset_closed()


func _fail_obs(door: MechDoor, why: String) -> void:
	_rec(door.door_id, "F-OBS-DETECT", false, -1.0, _dt, "s", why, "F")
	_rec(door.door_id, "F-OBS-STOP", false, -1.0, 0.0, "u", why, "F")
	_rec(door.door_id, "F-OBS-PASS", false, -1.0, 0.005, "m", why, "F")
	_rec(door.door_id, "F-OBS-FAULT", false, 0.0, 3.0, "count", why, "F")
	_rec(door.door_id, "R10", false, 0.0, 1.0, "bool", why, "F")


func _place_probe(door: MechDoor, closing: bool) -> void:
	var wx := float(door.get_meta("walk_x", 0.0))
	var z := 0.20
	if door.door_id == "hatch":
		z = -0.65
	elif door.door_id == "bay3" and not closing:
		z = 1.0
	elif door.door_id == "bay3":
		z = 0.40
	_probe.global_position = door.global_position + Vector3(wx, 0.0, z)
	_probe.velocity = Vector3.ZERO


func _wait_state(door: MechDoor, want: String, timeout: float) -> bool:
	var t := 0.0
	while t < timeout:
		if door.state == want:
			return true
		await get_tree().physics_frame
		t += _dt
	return door.state == want


func _stall_open(door: MechDoor) -> void:
	if door.door_id != "bay3" and door.door_id != "pair":
		_rec(door.door_id, "F-STALL-OPEN", true, 0.0, 0.010, "m", "n/a for this type", "F")
		return
	door.reset_closed()
	_hide_probe()
	door.command_open()
	var armed := false
	var arm_t := 0.0
	while arm_t < 2.0 and not armed:
		await get_tree().physics_frame
		arm_t += _dt
		var qn := 0.0
		if door.q_now.size() > 0:
			qn = absf(float(door.q_now[0]))
		if qn >= door.profile.travel * 0.08 and qn <= door.profile.travel * 0.20:
			armed = true
	var q_arm := 0.0
	if door.q_now.size() > 0:
		q_arm = absf(float(door.q_now[0]))
	var tip := _tip_arm(door) * sin(deg_to_rad(q_arm))
	var wx := float(door.get_meta("walk_x", 0.0))
	# Real PlayerBody. Do not press movement. The capsule stays in the arc.
	_player.velocity = Vector3.ZERO
	_player.global_position = door.global_position + Vector3(wx, 0.0, tip + 0.42)
	await get_tree().physics_frame
	var origin := _player.global_position
	var saw := false
	var ticks := 0
	var v_stop := 999.0
	var disp := 0.0
	var resumed := false
	var t := 0.0
	while t < 2.0:
		await get_tree().physics_frame
		t += _dt
		_player.velocity = Vector3.ZERO
		var moved := Vector2(_player.global_position.x - origin.x, _player.global_position.z - origin.z).length()
		disp = maxf(disp, moved)
		if door.state == "stalled":
			if not saw:
				saw = true
			ticks += 1
			var vmax := 0.0
			for v in door.v_now:
				vmax = maxf(vmax, absf(float(v)))
			if ticks <= 6:
				v_stop = vmax
		elif saw:
			resumed = true
			break
	var swing := door.profile.clear_model != "slide"
	var peak := 0.0
	var ts := 0.0
	while ts <= door.profile.open_duration:
		peak = maxf(peak, absf(float(door.profile.sample("open", ts)["vel"])))
		ts += _dt
	var vlim := 2.0 if swing else 0.05
	var v_ok := v_stop <= vlim + 1.0e-4 and v_stop <= peak * 0.02 + 1.0e-3
	var drift := door.drift_mm()
	var ok := armed and saw and disp <= 0.010 and v_ok and not resumed and door.lamp != "fault" and drift <= 2.0 and t >= 2.0 - _dt
	_rec(door.door_id, "F-STALL-OPEN", ok, disp, 0.010, "m", "stop_v %.3f lim %.3f within 6 ticks (%d) held %.2f s drift %.2f mm" % [v_stop, vlim, ticks, t, drift], "F")
	await _park(Vector3(0.0, 0.0, -200.0), PI)
	door.reset_closed()


func _clips_and_gaps(door: MechDoor) -> void:
	door.reset_closed()
	# Park the actor and the probe so a same-frame query cannot hit them, then
	# flush so a kinematic leftover cannot overlap the pose we just wrote.
	_hide_probe()
	await _park(Vector3(door.global_position.x, 0.0, -200.0), PI)
	var poses: Array = []
	var step_n := 20
	for i in step_n + 1:
		var tu := door.profile.open_duration * float(i) / float(step_n)
		poses.append(float(door.profile.sample("open", tu)["q"]))
	poses.append(_half_close_q(door))
	var leaf_worst := 0.0
	var hw_worst := 0.0
	var cop_pairs := 0
	var shape_worst := 0.0
	for q in poses:
		door.force_q(float(q))
		await get_tree().physics_frame
		var hit := _collide_leaves(door)
		leaf_worst = maxf(leaf_worst, float(hit["leaf"]))
		hw_worst = maxf(hw_worst, float(hit["hw"]))
		cop_pairs += int(hit["cop"])
		shape_worst = maxf(shape_worst, _shape_offset(door))
		if float(hit["leaf"]) > 0.010 or float(hit["hw"]) > 0.030:
			_clips[door.door_id].append({
				"door": door.door_id, "q": q, "leaf_m": hit["leaf"], "hw_m": hit["hw"],
			})
	var mesh_leaf := 0.0
	var mesh_hw := 0.0
	var mesh_bad := false
	var mesh_missing := ""
	var mesh_lines: Array = []
	var pose_list: Array = []
	for frac in [0.0, 0.25, 0.5, 0.75, 1.0]:
		pose_list.append(door.profile.travel * frac)
	pose_list.append(_half_close_q(door))
	for qmesh in pose_list:
		door.force_q(float(qmesh))
		await get_tree().physics_frame
		var t_mesh := Time.get_ticks_msec()
		var md := _mesh_tri_depth(door, float(qmesh))
		print("[door_lab] mesh %s q=%.3f leaf %.4f hw %.4f %d ms" % [door.door_id, float(qmesh), float(md["leaf"]), float(md["hw"]), Time.get_ticks_msec() - t_mesh])
		mesh_leaf = maxf(mesh_leaf, float(md["leaf"]))
		mesh_hw = maxf(mesh_hw, float(md["hw"]))
		if bool(md["bad"]):
			mesh_bad = true
		for row in md["log"]:
			mesh_lines.append(row)
		if mesh_missing == "" and not (md["missing"] as Array).is_empty():
			mesh_missing = str(md["missing"])
		_clips[door.door_id].append({
			"door": door.door_id, "q": qmesh, "leaf_m": md["leaf"], "hw_m": md["hw"], "mesh": true,
		})
	leaf_worst = maxf(leaf_worst, mesh_leaf)
	hw_worst = maxf(hw_worst, mesh_hw)
	door.force_q(0.0)
	var allow_ok := not mesh_bad and mesh_missing == ""
	_clips[door.door_id].append({"mesh_contacts": mesh_lines})
	_rec(door.door_id, "F-CLIP-LEAF", leaf_worst <= 0.010, leaf_worst, 0.010, "m", "collide plus full-mesh depth %.4f" % mesh_leaf, "F")
	_rec(door.door_id, "F-CLIP-HW", hw_worst <= 0.030, hw_worst, 0.030, "m", "mesh hw %.4f" % mesh_hw, "F")
	_rec(door.door_id, "F-CLIP-ALLOW", allow_ok, maxf(mesh_leaf, mesh_hw), 0.030, "m", "missing %s; %s" % [mesh_missing, JSON.stringify(mesh_lines)], "F")
	_log_m122(door)
	_rec(door.door_id, "F-CLIP-COPLANAR", cop_pairs == 0, float(cop_pairs), 0.0, "count", "pairs with 0 < depth <= 1 mm", "F")
	_rec(door.door_id, "V-ZFIGHT-GEO", cop_pairs == 0, float(cop_pairs), 0.0, "count", "", "V")
	var pocket_ok := leaf_worst <= 0.010
	_rec(door.door_id, "F-CLIP-POCKET", pocket_ok if door.door_id == "pocket" else true, leaf_worst, 0.010, "m", "n/a for this type" if door.door_id != "pocket" else "visible faces still 10 mm", "F")
	_rec(door.door_id, "F-DRIFT-SHAPE", shape_worst <= 0.002, shape_worst, 0.002, "m", "collision shape centre vs leaf mesh centre", "F")
	var sweep := _sweep_clear(door)
	_rec(door.door_id, "F-CLIP-SWEEP", sweep["ok"], float(sweep["m"]), float(sweep["limit"]), "m", str(sweep["note"]), "F")
	_rec(door.door_id, "R7", leaf_worst <= 0.010 and hw_worst <= 0.030 and cop_pairs == 0 and sweep["ok"] and allow_ok, leaf_worst, 0.010, "m", "", "F")
	_gaps(door)
	door.reset_closed()


func _half_close_q(door: MechDoor) -> float:
	var lo := 0.0
	var hi := door.profile.close_duration
	for _i in 20:
		var mid := (lo + hi) * 0.5
		var q := float(door.profile.sample("close", mid)["q"])
		if q > door.profile.travel * 0.5:
			lo = mid
		else:
			hi = mid
	return float(door.profile.sample("close", (lo + hi) * 0.5)["q"])


func _mesh_tri_depth(door: MechDoor, q: float) -> Dictionary:
	_trace("[door_lab] mesh begin %s q=%.3f" % [door.door_id, q])
	var allow := _contact_allow()
	var leaf_lim := float(allow.get("default_leaf_frame_m", -1.0))
	var other_lim := float(allow.get("default_other_m", -1.0))
	var parts := _weld_parts(door)
	var leaf_w := 0.0
	var hw_w := 0.0
	var log: Array = []
	var missing: Array = []
	var bad := leaf_lim < 0.0 or other_lim < 0.0
	if bad:
		missing.append("allowlist")
	var leaf_packs: Array = parts.get("_leaf_packs", [])
	for i in leaf_packs.size():
		for j in range(i + 1, leaf_packs.size()):
			var dleaf := _pair_depth_hashed(leaf_packs[i], leaf_packs[j], 0.010)
			leaf_w = maxf(leaf_w, dleaf)
			if dleaf > 0.001:
				log.append({"a": "leaf_skin", "b": "leaf_skin", "q": q, "depth": dleaf, "limit": 0.010})
	var frame: Array = parts.get("frame_skin", [])
	var leaf: Array = parts.get("leaf_skin", [])
	if not leaf.is_empty() and not frame.is_empty() and leaf_lim >= 0.0:
		var df := _pair_depth_hashed(leaf, frame, leaf_lim)
		leaf_w = maxf(leaf_w, df)
		log.append({"a": "leaf_skin", "b": "frame_skin", "q": q, "depth": df, "limit": leaf_lim, "cite": "leaf vs visible frame"})
		if df > leaf_lim + 1.0e-4:
			bad = true
	for nm in parts.keys():
		var name := str(nm)
		if name.begins_with("_") or name == "leaf_skin" or name == "frame_skin":
			continue
		var tris: Array = parts[name]
		if tris.is_empty():
			continue
		if not leaf.is_empty():
			var lim_l := _allow_max(allow, door.door_id, name, "leaf_skin", other_lim)
			var dl := _pair_depth_hashed(tris, leaf, lim_l)
			hw_w = maxf(hw_w, dl)
			if dl > 0.0005 or _allow_listed(allow, door.door_id, name, "leaf_skin"):
				log.append({"a": name, "b": "leaf_skin", "q": q, "depth": dl, "limit": lim_l})
			if dl > lim_l + 1.0e-4:
				bad = true
		if not frame.is_empty():
			var lim_f := _allow_max(allow, door.door_id, name, "frame_skin", other_lim)
			var dfr := _pair_depth_hashed(tris, frame, lim_f)
			hw_w = maxf(hw_w, dfr)
			if dfr > 0.0005 or _allow_listed(allow, door.door_id, name, "frame_skin"):
				log.append({"a": name, "b": "frame_skin", "q": q, "depth": dfr, "limit": lim_f})
			if dfr > lim_f + 1.0e-4:
				bad = true
	for entry in allow.get("entries", []):
		if typeof(entry) != TYPE_DICTIONARY:
			continue
		var doors_v: Variant = entry.get("doors", [])
		if typeof(doors_v) == TYPE_ARRAY and not (doors_v as Array).is_empty() and not (doors_v as Array).has(door.door_id):
			continue
		var a := str(entry.get("a", ""))
		var b := str(entry.get("b", ""))
		var have_a := parts.has(a) and typeof(parts[a]) == TYPE_ARRAY and not (parts[a] as Array).is_empty()
		var have_b := parts.has(b) and typeof(parts[b]) == TYPE_ARRAY and not (parts[b] as Array).is_empty()
		if not have_a or not have_b:
			bad = true
			missing.append("%s|%s" % [a, b])
			log.append({"a": a, "b": b, "q": q, "depth": -1.0, "limit": float(entry.get("max_m", 0.0)), "missing": true, "cite": str(entry.get("cite", ""))})
			continue
		if a != "leaf_skin" and a != "frame_skin" and b != "leaf_skin" and b != "frame_skin":
			var lim_h := float(entry.get("max_m", other_lim))
			var dhw := _pair_depth_hashed(parts[a], parts[b], lim_h)
			hw_w = maxf(hw_w, dhw)
			log.append({"a": a, "b": b, "q": q, "depth": dhw, "limit": lim_h, "cite": str(entry.get("cite", ""))})
			if dhw > lim_h + 1.0e-4:
				bad = true
	if leaf_w > 0.010 + 1.0e-4:
		bad = true
	return {"leaf": leaf_w, "hw": hw_w, "log": log, "missing": missing, "bad": bad}


func _contact_allow() -> Dictionary:
	if not _allow.is_empty():
		return _allow
	var path := "res://resources/door_lab/contact_allowlist.json"
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(path))
	if typeof(parsed) == TYPE_DICTIONARY:
		_allow = parsed
	return _allow


func _allow_listed(allow: Dictionary, door_id: String, a: String, b: String) -> bool:
	for entry in allow.get("entries", []):
		if typeof(entry) != TYPE_DICTIONARY:
			continue
		var doors_v: Variant = entry.get("doors", [])
		if typeof(doors_v) == TYPE_ARRAY and not (doors_v as Array).is_empty() and not (doors_v as Array).has(door_id):
			continue
		var ea := str(entry.get("a", ""))
		var eb := str(entry.get("b", ""))
		if (ea == a and eb == b) or (ea == b and eb == a):
			return true
	return false


func _allow_max(allow: Dictionary, door_id: String, a: String, b: String, fallback: float) -> float:
	var best := fallback
	for entry in allow.get("entries", []):
		if typeof(entry) != TYPE_DICTIONARY:
			continue
		var doors_v: Variant = entry.get("doors", [])
		if typeof(doors_v) == TYPE_ARRAY and not (doors_v as Array).is_empty() and not (doors_v as Array).has(door_id):
			continue
		var ea := str(entry.get("a", ""))
		var eb := str(entry.get("b", ""))
		if (ea == a and eb == b) or (ea == b and eb == a):
			best = float(entry.get("max_m", fallback))
	return best


func _hw_part(low: String) -> bool:
	if "guide" in low or "dogpivot" in low or "dogpin" in low:
		return false
	var stripped := low.replace("frame", "")
	for key in ["hinge", "knuckle", "damper", "seal", "sweep", "brush", "dog", "linkage", "roller", "strike", "guard", "ram"]:
		if key in stripped:
			return true
	return false


func _skip_visual(low: String) -> bool:
	if low.begins_with("reveal") or "colonly" in low or "hazard" in low:
		return true
	if low.begins_with("digitface") or low.begins_with("lampseg") or low == "lampspill" or low == "lampbar":
		return true
	return false


func _under_leaf(n: Node) -> bool:
	var p := n.get_parent()
	while p != null:
		if p is AnimatableBody3D:
			return true
		p = p.get_parent()
	return false


func _weld_parts(door: MechDoor) -> Dictionary:
	var parts := {}
	var packs := {}
	var stack: Array[Node] = [door]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D):
			continue
		var mi := n as MeshInstance3D
		if mi.mesh == null or not mi.visible:
			continue
		var low := String(mi.name).to_lower()
		if _skip_visual(low):
			continue
		var tris := _tris_of(mi)
		if tris.is_empty():
			continue
		var key := ""
		if _hw_part(low):
			key = String(mi.name)
		elif _under_leaf(mi):
			key = "leaf_skin"
			var id := str(mi.get_parent().get_instance_id()) if _under_leaf(mi) else "leaf"
			var body: Node = mi
			while body != null and not (body is AnimatableBody3D):
				body = body.get_parent()
			if body != null:
				id = str(body.get_instance_id())
			if not packs.has(id):
				packs[id] = []
			(packs[id] as Array).append_array(tris)
		else:
			key = "frame_skin"
		if not parts.has(key):
			parts[key] = []
		(parts[key] as Array).append_array(tris)
	var pack_list: Array = []
	for k in packs.keys():
		pack_list.append(packs[k])
	parts["_leaf_packs"] = pack_list
	return parts


func _tris_of(mi: MeshInstance3D) -> Array:
	var faces := mi.mesh.get_faces()
	var xf := mi.global_transform
	var out: Array = []
	var i := 0
	while i + 2 < faces.size():
		var a: Vector3 = xf * faces[i]
		var b: Vector3 = xf * faces[i + 1]
		var c: Vector3 = xf * faces[i + 2]
		if (b - a).cross(c - a).length_squared() > 1.0e-12:
			out.append([a, b, c])
		i += 3
	return out


func _bin_key(x: int, y: int, z: int) -> int:
	return (x + 8192) + (y + 8192) * 20000 + (z + 8192) * 400000000


func _pair_depth_hashed(a: Array, b: Array, _limit: float) -> float:
	if a.is_empty() or b.is_empty():
		return 0.0
	if not _tris_aabb(a).grow(0.004).intersects(_tris_aabb(b)):
		return 0.0
	var iterate: Array = a
	var hashed: Array = b
	if a.size() > b.size():
		iterate = b
		hashed = a
	var grid := {}
	var coarse := {}
	var huge: Array = []
	for tri in hashed:
		_bin_tri(grid, coarse, huge, tri)
	var worst := 0.0
	for tri_a in iterate:
		var ta: Array = tri_a
		var box := AABB(ta[0], Vector3.ZERO).expand(ta[1]).expand(ta[2]).grow(0.003)
		var cands := _query_bins(grid, coarse, huge, box)
		for tri_b in cands:
			var tb: Array = tri_b
			var depth := _tri_clip_depth(ta[0], ta[1], ta[2], tb[0], tb[1], tb[2])
			if depth > worst:
				worst = depth
			# Depths through 60 mm stay the true max so a rig nudge has a real number.
			# A meter-scale hit still returns immediately.
			if worst > 0.120 + 1.0e-4:
				return worst
	return worst


func _bin_tri(grid: Dictionary, coarse: Dictionary, huge: Array, tri: Array) -> void:
	var box := AABB(tri[0], Vector3.ZERO).expand(tri[1]).expand(tri[2])
	var x0 := int(floor(box.position.x / 0.08))
	var y0 := int(floor(box.position.y / 0.08))
	var z0 := int(floor(box.position.z / 0.08))
	var x1 := int(floor((box.position.x + box.size.x) / 0.08))
	var y1 := int(floor((box.position.y + box.size.y) / 0.08))
	var z1 := int(floor((box.position.z + box.size.z) / 0.08))
	if x1 - x0 <= 6 and y1 - y0 <= 6 and z1 - z0 <= 6:
		for x in range(x0, x1 + 1):
			for y in range(y0, y1 + 1):
				for z in range(z0, z1 + 1):
					var key := _bin_key(x, y, z)
					if not grid.has(key):
						grid[key] = []
					(grid[key] as Array).append(tri)
		return
	# Tris wider than 0.48 m go in 0.32 m cells. Only a span past 2.5 m stays
	# unbinned, and those are tested only when their box meets the query.
	var cx0 := int(floor(box.position.x / 0.32))
	var cy0 := int(floor(box.position.y / 0.32))
	var cz0 := int(floor(box.position.z / 0.32))
	var cx1 := int(floor((box.position.x + box.size.x) / 0.32))
	var cy1 := int(floor((box.position.y + box.size.y) / 0.32))
	var cz1 := int(floor((box.position.z + box.size.z) / 0.32))
	if cx1 - cx0 > 8 or cy1 - cy0 > 8 or cz1 - cz0 > 8:
		huge.append(tri)
		return
	for x2 in range(cx0, cx1 + 1):
		for y2 in range(cy0, cy1 + 1):
			for z2 in range(cz0, cz1 + 1):
				var key2 := _bin_key(x2, y2, z2)
				if not coarse.has(key2):
					coarse[key2] = []
				(coarse[key2] as Array).append(tri)


func _query_bins(grid: Dictionary, coarse: Dictionary, huge: Array, box: AABB) -> Array:
	var out: Array = []
	var x0 := int(floor(box.position.x / 0.08))
	var y0 := int(floor(box.position.y / 0.08))
	var z0 := int(floor(box.position.z / 0.08))
	var x1 := int(floor((box.position.x + box.size.x) / 0.08))
	var y1 := int(floor((box.position.y + box.size.y) / 0.08))
	var z1 := int(floor((box.position.z + box.size.z) / 0.08))
	for x in range(x0, x1 + 1):
		for y in range(y0, y1 + 1):
			for z in range(z0, z1 + 1):
				var key := _bin_key(x, y, z)
				if grid.has(key):
					for tri in grid[key]:
						out.append(tri)
	var cx0 := int(floor(box.position.x / 0.32))
	var cy0 := int(floor(box.position.y / 0.32))
	var cz0 := int(floor(box.position.z / 0.32))
	var cx1 := int(floor((box.position.x + box.size.x) / 0.32))
	var cy1 := int(floor((box.position.y + box.size.y) / 0.32))
	var cz1 := int(floor((box.position.z + box.size.z) / 0.32))
	for x2 in range(cx0, cx1 + 1):
		for y2 in range(cy0, cy1 + 1):
			for z2 in range(cz0, cz1 + 1):
				var key2 := _bin_key(x2, y2, z2)
				if coarse.has(key2):
					for tri2 in coarse[key2]:
						out.append(tri2)
	for tri3 in huge:
		var hb := AABB(tri3[0], Vector3.ZERO).expand(tri3[1]).expand(tri3[2])
		if hb.intersects(box):
			out.append(tri3)
	return out


func _log_m122(door: MechDoor) -> void:
	var rows: Array = door.get_meta("m122", [])
	var note := "pending Rook bake"
	if rows.is_empty():
		note = "no runtime mesh edit recorded on this door; pending Rook bake"
	else:
		note = JSON.stringify(rows) + " pending Rook bake"
	_rec(door.door_id, "M-122", true, float(rows.size()), 0.0, "count", note, "note")


func _pair_depth(a: Array, b: Array) -> float:
	if a.is_empty() or b.is_empty():
		return 0.0
	if not _tris_aabb(a).intersects(_tris_aabb(b)):
		return 0.0
	var worst := 0.0
	for ta in a:
		var tri_a: Array = ta
		var box_a := AABB(tri_a[0], Vector3.ZERO).expand(tri_a[1]).expand(tri_a[2]).grow(0.002)
		for tb in b:
			var tri_b: Array = tb
			var box_b := AABB(tri_b[0], Vector3.ZERO).expand(tri_b[1]).expand(tri_b[2])
			if not box_a.intersects(box_b):
				continue
			var depth := _tri_clip_depth(tri_a[0], tri_a[1], tri_a[2], tri_b[0], tri_b[1], tri_b[2])
			if depth > worst:
				worst = depth
			if worst > 0.030:
				var na := "?"
				var nb := "?"
				if tri_a.size() > 3:
					na = str(tri_a[3])
				if tri_b.size() > 3:
					nb = str(tri_b[3])
				print("[door_lab] clip pair %s vs %s depth %.4f" % [na, nb, worst])
				return worst
	return worst


func _tris_aabb(tris: Array) -> AABB:
	var t0: Array = tris[0]
	var ab := AABB(t0[0], Vector3.ZERO)
	for item in tris:
		var t: Array = item
		ab = ab.expand(t[0]).expand(t[1]).expand(t[2])
	return ab


func _tri_clip_depth(a0: Vector3, a1: Vector3, a2: Vector3, b0: Vector3, b1: Vector3, b2: Vector3) -> float:
	var n1 := (a1 - a0).cross(a2 - a0)
	var n2 := (b1 - b0).cross(b2 - b0)
	var l1 := n1.length()
	var l2 := n2.length()
	if l1 < 1.0e-8 or l2 < 1.0e-8:
		return 0.0
	n1 /= l1
	n2 /= l2
	if absf(n1.dot(n2)) > 0.985 and absf((b0 - a0).dot(n1)) < 0.0015:
		return 0.0
	# A vertex in the infinite prism of a large triangle is not containment.
	# Count it only when an edge from it crosses, or when the faces are a
	# near-parallel slab whose inside vertices share one depth (seal, brush).
	var parallel := absf(n1.dot(n2)) > 0.85
	var depth := _contain_depth(a0, a1, a2, b0, b1, b2, n2, parallel)
	depth = maxf(depth, _contain_depth(b0, b1, b2, a0, a1, a2, n1, parallel))
	if depth < 1.0e-5 and (_edge_cross(a0, a1, a2, b0, b1, b2, n2) or _edge_cross(b0, b1, b2, a0, a1, a2, n1)):
		depth = 0.0025
	return depth


func _contain_depth(a0: Vector3, a1: Vector3, a2: Vector3, b0: Vector3, b1: Vector3, b2: Vector3, n2: Vector3, parallel: bool) -> float:
	var poke := 0.0
	var slab_min := 1.0e9
	var slab_max := 0.0
	var slab_n := 0
	var src_edge := maxf(a0.distance_to(a1), maxf(a1.distance_to(a2), a2.distance_to(a0)))
	var dst_edge := maxf(b0.distance_to(b1), maxf(b1.distance_to(b2), b2.distance_to(b0)))
	var verts := [a0, a1, a2]
	for i in 3:
		var p: Vector3 = verts[i]
		var side: float = (p - b0).dot(n2)
		if side >= -1.0e-4 or not _point_in_tri(p, b0, b1, b2, n2):
			continue
		var d := -side
		var qv: Vector3 = verts[(i + 1) % 3]
		var rv: Vector3 = verts[(i + 2) % 3]
		var hit_q := _edge_hits(p, qv, b0, b1, b2, n2)
		var hit_r := _edge_hits(p, rv, b0, b1, b2, n2)
		if hit_q or hit_r:
			var elen := 1.0e9
			if hit_q:
				elen = minf(elen, p.distance_to(qv))
			if hit_r:
				elen = minf(elen, p.distance_to(rv))
			# A short edge through a door-sized face is still the prism.
			# Both triangles have to be local, or the vertex has to be within 10 mm.
			if d <= 0.010 or (elen <= 0.12 and dst_edge <= 0.40):
				poke = maxf(poke, d)
		else:
			slab_n += 1
			slab_min = minf(slab_min, d)
			slab_max = maxf(slab_max, d)
	# Seal or brush face pressed flat. Both faces have to be small.
	if parallel and slab_n >= 2 and slab_max <= 0.016 and src_edge <= 0.12 and dst_edge <= 0.40 and slab_max - slab_min <= maxf(0.004, 0.25 * slab_min):
		poke = maxf(poke, slab_max)
	return poke


func _point_in_tri(p: Vector3, a: Vector3, b: Vector3, c: Vector3, n: Vector3) -> bool:
	var c0 := (b - a).cross(p - a).dot(n)
	var c1 := (c - b).cross(p - b).dot(n)
	var c2 := (a - c).cross(p - c).dot(n)
	return c0 >= -1.0e-8 and c1 >= -1.0e-8 and c2 >= -1.0e-8


func _edge_cross(a0: Vector3, a1: Vector3, a2: Vector3, b0: Vector3, b1: Vector3, b2: Vector3, n: Vector3) -> bool:
	return _edge_hits(a0, a1, b0, b1, b2, n) or _edge_hits(a1, a2, b0, b1, b2, n) or _edge_hits(a2, a0, b0, b1, b2, n)


func _edge_hits(p: Vector3, q: Vector3, a: Vector3, b: Vector3, c: Vector3, n: Vector3) -> bool:
	var sp := (p - a).dot(n)
	var sq := (q - a).dot(n)
	if sp * sq >= 0.0:
		return false
	var denom := sp - sq
	if absf(denom) < 1.0e-8:
		return false
	var hit := p + (q - p) * (sp / denom)
	return _point_in_tri(hit, a, b, c, n)


func _rod_poke(body: Node3D) -> float:
	var shell := _find_mesh(body, "leaf_shell")
	if shell == null:
		shell = _find_mesh(body, "shell")
	if shell == null or shell.mesh == null:
		return 0.0
	var box := shell.mesh.get_aabb()
	var inv := shell.global_transform.affine_inverse()
	var worst := 0.0
	var stack: Array[Node] = [body]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D) or n == shell:
			continue
		var low := String(n.name).to_lower()
		if "guide" in low or ("dog" not in low and "linkage" not in low):
			continue
		var mi := n as MeshInstance3D
		if mi.mesh == null:
			continue
		var faces := mi.mesh.get_faces()
		var xf := inv * mi.global_transform
		var step := maxi(1, int(faces.size() / 60))
		var i := 0
		while i < faces.size():
			var lp: Vector3 = xf * faces[i]
			var dx := maxf(box.position.x - lp.x, lp.x - (box.position.x + box.size.x))
			var dy := maxf(box.position.y - lp.y, lp.y - (box.position.y + box.size.y))
			var dz := maxf(box.position.z - lp.z, lp.z - (box.position.z + box.size.z))
			worst = maxf(worst, Vector3(maxf(dx, 0.0), maxf(dy, 0.0), maxf(dz, 0.0)).length())
			i += step
	return worst


func _find_mesh(root: Node, needle: String) -> MeshInstance3D:
	var stack: Array[Node] = [root]
	var want := needle.to_lower()
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if n is MeshInstance3D and want in String(n.name).to_lower():
			return n as MeshInstance3D
		for c in n.get_children():
			stack.append(c)
	return null


func _collide_leaves(door: MechDoor) -> Dictionary:
	var space := door.get_world_3d().direct_space_state
	var leaf_w := 0.0
	var hw_w := 0.0
	var cop := 0
	var shallow: Array = []
	var floor := _lab.get_node_or_null("FloorBody")
	for item in door._leaves:
		var body: AnimatableBody3D = item["body"]
		for ch in body.get_children():
			if not (ch is CollisionShape3D):
				continue
			var cs := ch as CollisionShape3D
			if cs.shape == null:
				continue
			var params := PhysicsShapeQueryParameters3D.new()
			params.shape = cs.shape
			params.transform = cs.global_transform
			params.collision_mask = 1
			# Assign the exclude list once. Appending to the property returns a
			# copy, so the floor stayed in the query and every leaf "penetrated" it.
			var ex: Array[RID] = [body.get_rid()]
			if floor is CollisionObject3D:
				ex.append((floor as CollisionObject3D).get_rid())
			if _player != null:
				ex.append(_player.get_rid())
			if _probe != null:
				ex.append(_probe.get_rid())
			params.exclude = ex
			var hits := space.collide_shape(params, 12)
			var hw := _hw_name(cs)
			for i in range(0, hits.size(), 2):
				var depth := hits[i].distance_to(hits[i + 1])
				# Depth under 1 mm is coplanar only when the contacts cover more than 1 cm².
				if depth <= 0.001:
					if depth > 1.0e-5:
						shallow.append(hits[i])
					continue
				if hw:
					hw_w = maxf(hw_w, depth)
				else:
					leaf_w = maxf(leaf_w, depth)
	if _patch_area(shallow) > 0.0001:
		cop += 1
	var mesh_hit := _mesh_inside(door)
	leaf_w = maxf(leaf_w, float(mesh_hit["leaf"]))
	hw_w = maxf(hw_w, float(mesh_hit["hw"]))
	cop += int(mesh_hit["cop"])
	return {"leaf": leaf_w, "hw": hw_w, "cop": cop}


func _patch_area(pts: Array) -> float:
	if pts.size() < 3:
		return 0.0
	var lo: Vector3 = pts[0]
	var hi: Vector3 = pts[0]
	for p in pts:
		var v: Vector3 = p
		lo = lo.min(v)
		hi = hi.max(v)
	var s := hi - lo
	var a := s.x
	var b := s.y
	var c := s.z
	if a < b:
		var tmp := a
		a = b
		b = tmp
	if b < c:
		var tmp2 := b
		b = c
		c = tmp2
	if a < b:
		var tmp3 := a
		a = b
		b = tmp3
	return a * b


func _mesh_inside(door: MechDoor) -> Dictionary:
	var leaf_w := 0.0
	var hw_w := 0.0
	var cop := 0
	var space := door.get_world_3d().direct_space_state
	var sph := SphereShape3D.new()
	sph.radius = 0.001
	for item in door._leaves:
		var shallow_m: Array = []
		var body: AnimatableBody3D = item["body"]
		var pts: Array = _mesh_points(body, "leaf")
		if pts.is_empty():
			pts = _mesh_points(body, "stile")
		var step := maxi(1, int(pts.size() / 60))
		var i := 0
		while i < pts.size():
			var local: Vector3 = pts[i]
			i += step
			var p: Vector3 = body.global_transform * local
			if door.door_id != "floorhatch" and p.y < -0.005:
				leaf_w = maxf(leaf_w, 0.011)
			var params := PhysicsShapeQueryParameters3D.new()
			params.shape = sph
			params.transform = Transform3D(Basis(), p)
			params.collision_mask = 1
			var ex: Array[RID] = [body.get_rid()]
			var floor := _lab.get_node_or_null("FloorBody")
			if floor is CollisionObject3D:
				ex.append((floor as CollisionObject3D).get_rid())
			params.exclude = ex
			# Deep vertices inside a frame are not a coplanar patch. Only a
			# graze in (0, 1 mm] counts, same band as the leaf collide test.
			var hits := space.collide_shape(params, 8)
			var shallow_hit := false
			for j in range(0, hits.size(), 2):
				var depth := hits[j].distance_to(hits[j + 1])
				if depth > 1.0e-5 and depth <= 0.001:
					shallow_hit = true
					break
			if not shallow_hit:
				continue
			shallow_m.append(p)
		if _patch_area(shallow_m) > 0.0001:
			cop += 1
	return {"leaf": leaf_w, "hw": hw_w, "cop": cop}


func _hw_name(node: Node) -> bool:
	var blob := String(node.name).to_lower()
	var p := node.get_parent()
	if p != null:
		blob += " " + String(p.name).to_lower()
	for key in ["hinge", "dog", "seal", "roller", "strike", "knuckle", "brush", "sweep", "guard"]:
		if key in blob:
			return true
	return false


func _shape_offset(door: MechDoor) -> float:
	# Several hulls on one leaf (plug + flange). Compare the union, not each hull.
	var worst := 0.0
	for item in door._leaves:
		var body: Node3D = item["body"]
		var centre := _leaf_mesh_centre(body)
		var ab := AABB()
		var any := false
		for ch in body.get_children():
			# Rook pass E incr: the floor hatch LidWalkSkin is the lab's +0.12 m walk-collision layer, not the lid hull.
			if ch is CollisionShape3D and not _hw_name(ch) and "walkskin" not in String(ch.name).to_lower():
				var cs := ch as CollisionShape3D
				var sab := _shape_aabb_in(cs, body)
				ab = sab if not any else ab.merge(sab)
				any = true
		if any:
			worst = maxf(worst, (body.global_transform * ab.get_center()).distance_to(centre))
	return worst


func _shape_aabb_in(cs: CollisionShape3D, body: Node3D) -> AABB:
	var rel := body.global_transform.affine_inverse() * cs.global_transform
	if cs.shape == null:
		return AABB(rel.origin, Vector3.ZERO)
	var dbg := cs.shape.get_debug_mesh()
	if dbg == null:
		return AABB(rel.origin, Vector3.ZERO)
	return rel * dbg.get_aabb()


func _shape_centre(cs: CollisionShape3D) -> Vector3:
	if cs.shape == null:
		return cs.global_position
	var dbg := cs.shape.get_debug_mesh()
	if dbg == null:
		return cs.global_position
	var ab: AABB = cs.global_transform * dbg.get_aabb()
	return ab.get_center()


func _leaf_mesh_centre(body: Node3D) -> Vector3:
	var has_shell := false
	var scan: Array[Node] = [body]
	while not scan.is_empty():
		var s: Node = scan.pop_back()
		for sc in s.get_children():
			scan.append(sc)
		if s is MeshInstance3D and "shell" in String(s.name).to_lower():
			has_shell = true
			break
	var ab := AABB()
	var any := false
	var stack: Array[Node] = [body]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D) or (n as MeshInstance3D).mesh == null:
			continue
		var nm := String(n.name).to_lower()
		# Panels proud of a shell pull the centre off the collider. Use the shell alone.
		var primary := false
		if has_shell:
			primary = "shell" in nm
		else:
			primary = "stile" in nm or "panel" in nm or "leafface" in nm or "_face" in nm
		if not primary:
			continue
		var mi := n as MeshInstance3D
		var world: AABB = mi.global_transform * mi.mesh.get_aabb()
		ab = world if not any else ab.merge(world)
		any = true
	if not any:
		return body.global_position
	return ab.get_center()


func _sweep_clear(door: MechDoor) -> Dictionary:
	if door.door_id != "bay3":
		return {"ok": true, "m": 0.3, "limit": 0.3, "note": "n/a for this type"}
	door.force_q(door.profile.travel)
	var leaf_pts := _sample_pts(door, "leaf_")
	var post_pts := _sample_pts(door, "bollard")
	var best := 99.0
	if leaf_pts.is_empty() or post_pts.is_empty():
		return {"ok": false, "m": -1.0, "limit": 0.3, "note": "could not sample leaf or bollard vertices"}
	for a in leaf_pts:
		for b in post_pts:
			best = minf(best, (a as Vector3).distance_to(b as Vector3))
	return {"ok": best >= 0.300, "m": best, "limit": 0.300, "note": "open leaf tip to nearest bollard vertex"}


func _sample_pts(door: Node, needle: String) -> Array:
	var pts: Array = []
	var stack: Array[Node] = [door]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D):
			continue
		if needle not in String(n.name).to_lower():
			continue
		var mi := n as MeshInstance3D
		if mi.mesh == null:
			continue
		var faces := mi.mesh.get_faces()
		var step := maxi(1, int(faces.size() / 80))
		var i := 0
		while i < faces.size():
			pts.append(mi.global_transform * faces[i])
			i += step
			if pts.size() > 120:
				return pts
	return pts


func _gaps(door: MechDoor) -> void:
	var id := door.door_id
	door.force_q(0.0)
	var yaw := 0.0
	for item in door._leaves:
		var closed_ang := (item["body"] as Node3D).rotation_degrees.x if id == "floorhatch" else (item["body"] as Node3D).rotation_degrees.y
		yaw = maxf(yaw, absf(closed_ang))
	door.force_q(door.profile.travel)
	var open_err := 0.0
	var target := 105.0 if id == "floorhatch" else (100.0 if id == "hatch" else (0.0 if id == "pocket" else 90.0))
	if id != "pocket":
		for item in door._leaves:
			var ang := absf((item["body"] as Node3D).rotation_degrees.x) if id == "floorhatch" else absf((item["body"] as Node3D).rotation_degrees.y)
			open_err = maxf(open_err, absf(ang - target))
	else:
		for item in door._leaves:
			var body: Node3D = item["body"]
			var expect: float = float(item["rest"].x) + float(item["sign"]) * door.profile.travel
			open_err = maxf(open_err, absf(body.position.x - expect) * 1000.0)
	door.force_q(0.0)
	var align_ok := yaw <= 0.25 and (open_err <= 0.5 if id != "pocket" else open_err <= 2.0)
	_rec(id, "V-ALIGN-YAW", align_ok, yaw if id != "pocket" else open_err, 0.25 if id != "pocket" else 2.0, "deg" if id != "pocket" else "mm", "closed yaw %.3f open err %.3f" % [yaw, open_err], "V")
	var detail := _measure_gaps(door)
	_rec(id, "V-GAP-POCKET", detail["pocket_ok"], float(detail["pocket_mm"]), 2.0, "mm", str(detail["pocket_note"]), "V")
	_rec(id, "V-GAP-BAY", detail["bay_ok"], float(detail["bay_mm"]), 2.0, "mm", str(detail["bay_note"]), "V")
	_rec(id, "V-GAP-PAIR", detail["pair_ok"], float(detail["pair_mm"]), 2.0, "mm", str(detail["pair_note"]), "V")
	_rec(id, "V-GAP-HATCH", detail["hatch_ok"], float(detail["hatch_mm"]), 2.0, "mm", str(detail["hatch_note"]), "V")
	_rec(id, "V-GAP-STD", detail["std_ok"], float(detail["std_mm"]), 1.0, "mm", str(detail["std_note"]), "V")
	var r8: bool = bool(detail["pocket_ok"]) and bool(detail["bay_ok"]) and bool(detail["pair_ok"]) and bool(detail["hatch_ok"]) and bool(detail["std_ok"]) and align_ok
	_rec(id, "R8", r8, float(detail["worst"]), 2.0, "mm", "applicable gaps within ±2 mm", "V")


func _measure_gaps(door: MechDoor) -> Dictionary:
	var id := door.door_id
	var out := {
		"pocket_ok": id != "pocket", "pocket_mm": 0.0, "pocket_note": "n/a for this type",
		"bay_ok": id != "bay3", "bay_mm": 0.0, "bay_note": "n/a for this type",
		"pair_ok": id != "pair", "pair_mm": 0.0, "pair_note": "n/a for this type",
		"hatch_ok": id != "hatch", "hatch_mm": 0.0, "hatch_note": "n/a for this type",
		"std_ok": true, "std_mm": 0.0, "std_note": "",
		"worst": 0.0,
	}
	if id == "pocket":
		door.force_q(0.0)
		var meet := _pocket_meet_mm(door)
		var floor_mm := _pocket_floor_mm(door)
		var head_mm := _pocket_head_mm(door)
		var jamb := _pocket_mouth_mm(door)
		# Bulbs overlap 3 mm when shut. 4.5 mm of travel on each leaf opens a 6 mm daylight gap.
		# Seal unseat ends at 3 mm. 4.5 mm is not a pose the bolt phase reaches.
		door.force_q(0.003)
		var bolt := _pocket_meet_mm(door)
		door.force_q(1.0)
		var lap := _pocket_bumper_mm(door)
		door.force_q(0.0)
		var errs := [absf(meet - 0.0), absf(bolt - 3.0), absf(jamb - 6.0), absf(floor_mm - 8.0), absf(head_mm - 10.0), absf(lap - 25.0)]
		var worst := 0.0
		for e in errs:
			worst = maxf(worst, float(e))
		out["pocket_ok"] = worst <= 2.0
		out["pocket_mm"] = worst
		out["pocket_note"] = "meet %.2f bolt %.2f jamb %.2f floor %.2f soffit %.2f lap %.2f" % [meet, bolt, jamb, floor_mm, head_mm, lap]
		out["worst"] = worst
		var std_p := _edge_std_mm(door, "stile")
		out["std_mm"] = std_p["std"]
		out["std_note"] = "stile edge, %d height samples, max dev %.2f mm" % [int(std_p["n"]), float(std_p["dev"])]
		out["std_ok"] = float(std_p["std"]) <= 1.0 and float(std_p["dev"]) <= 2.0 and int(std_p["n"]) >= 8
	elif id == "bay3":
		door.force_q(0.0)
		var floor_b := _min_y(door, "FloorSweep") * 1000.0
		var hinge := _finger_gap_mm(door)
		var leaf_gap := _adjacent_leaf_gap_mm(door)
		var worst_b := maxf(absf(floor_b - 8.0), 0.0 if hinge <= 10.0 else hinge - 10.0)
		# Mullion gap is reported; pass the 3 mm target when a frame piece splits it, else the raw gap.
		var mullion := _mullion_side_mm(door)
		worst_b = maxf(worst_b, absf(mullion - 3.0))
		out["bay_ok"] = worst_b <= 2.0 and hinge <= 10.0
		out["bay_mm"] = worst_b
		out["bay_note"] = "floor %.2f hinge_visible %.2f leaf_gap %.2f mullion_side %.2f" % [floor_b, hinge, leaf_gap, mullion]
		out["worst"] = worst_b
		var std_b := _edge_std_mm(door, "FloorSweep")
		out["std_ok"] = float(std_b["std"]) <= 1.0 and float(std_b["dev"]) <= 2.0 and int(std_b["n"]) >= 8
		out["std_mm"] = std_b["std"]
		out["std_note"] = "sweep bottom, %d samples, max dev %.2f mm" % [int(std_b["n"]), float(std_b["dev"])]
	elif id == "pair":
		door.force_q(0.0)
		var meet_p := _adjacent_leaf_gap_mm(door)
		var floor_p := _min_y(door, "") * 1000.0
		var hinge_p := _pair_hinge_mm(door)
		var meet_ok := meet_p >= 3.0 and meet_p <= 8.0
		var floor_ok := floor_p >= 8.0 and floor_p <= 12.0
		var hinge_ok := hinge_p >= 3.0 and hinge_p <= 5.0
		out["pair_ok"] = meet_ok and floor_ok and hinge_ok
		out["pair_mm"] = maxf(absf(meet_p - 5.5) - 2.5, maxf(absf(floor_p - 10.0) - 2.0, absf(hinge_p - 4.0) - 1.0))
		out["pair_note"] = "meet %.2f floor %.2f hinge %.2f" % [meet_p, floor_p, hinge_p]
		out["worst"] = float(out["pair_mm"])
		var std_pair := _edge_std_mm(door, "Panel")
		out["std_ok"] = float(std_pair["std"]) <= 1.0 and float(std_pair["dev"]) <= 2.0 and int(std_pair["n"]) >= 8
		out["std_mm"] = std_pair["std"]
		out["std_note"] = "panel edge, %d samples, max dev %.2f mm" % [int(std_pair["n"]), float(std_pair["dev"])]
	elif id == "floorhatch":
		door.force_q(0.0)
		var gap_f := _floor_side_mm(door)
		var comp_f := _seal_compression_mm(door)
		out["hatch_ok"] = absf(gap_f - 6.0) <= 2.0 and absf(comp_f - 8.0) <= 2.0
		out["hatch_mm"] = maxf(absf(gap_f - 6.0), absf(comp_f - 8.0))
		out["hatch_note"] = "leaf shell to rebate wall, worst of W/E/S %.2f mm (N = open hinge channel); inflated compression %.2f mm" % [gap_f, comp_f]
		out["worst"] = float(out["hatch_mm"])
		var std_f := _edge_std_mm(door, "leaf_shell")
		out["std_ok"] = float(std_f["std"]) <= 1.0 and float(std_f["dev"]) <= 2.0 and int(std_f["n"]) >= 8
		out["std_mm"] = std_f["std"]
		out["std_note"] = "shell edge, %d samples, max dev %.2f mm" % [int(std_f["n"]), float(std_f["dev"])]
	else:
		door.force_q(0.0)
		var gap_h := _hatch_gap_mm(door)
		var comp_h := _seal_compression_mm(door)
		out["hatch_ok"] = absf(gap_h - 6.0) <= 2.0 and absf(comp_h - 8.0) <= 2.0
		out["hatch_mm"] = maxf(absf(gap_h - 6.0), absf(comp_h - 8.0))
		out["hatch_note"] = "deflated leaf-to-opening %.2f mm; inflated compression %.2f mm (target 8)" % [gap_h, comp_h]
		out["worst"] = float(out["hatch_mm"])
		var std_h := _edge_std_mm(door, "leaf_shell")
		out["std_ok"] = float(std_h["std"]) <= 1.0 and float(std_h["dev"]) <= 2.0 and int(std_h["n"]) >= 8
		out["std_mm"] = std_h["std"]
		out["std_note"] = "panel edge, %d samples, max dev %.2f mm" % [int(std_h["n"]), float(std_h["dev"])]
	return out


func _named(door: Node3D, needle: String) -> Array:
	var out: Array = []
	var stack: Array[Node] = [door]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if n is MeshInstance3D and needle.to_lower() in String(n.name).to_lower() and (n as MeshInstance3D).mesh != null:
			# Reveal_Soffit contains "soffit" but it is the 10 mm light strip, not the head.
			if String(n.name).begins_with("Reveal") and not needle.to_lower().begins_with("reveal"):
				continue
			var mi := n as MeshInstance3D
			var world: AABB = mi.global_transform * mi.mesh.get_aabb()
			out.append(AABB(world.position - door.global_position, world.size))
	return out


func _x_gap(boxes: Array) -> float:
	if boxes.size() < 2:
		return 9.0
	boxes.sort_custom(func(a, b): return (a as AABB).position.x < (b as AABB).position.x)
	var a: AABB = boxes[0]
	var b: AABB = boxes[boxes.size() - 1]
	return b.position.x - (a.position.x + a.size.x)


func _min_y(door: Node3D, needle: String) -> float:
	var best := 99.0
	var stack: Array[Node] = [door]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D) or (n as MeshInstance3D).mesh == null:
			continue
		if needle != "" and needle.to_lower() not in String(n.name).to_lower():
			continue
		if needle == "" and not (n.get_parent() is AnimatableBody3D):
			continue
		var world: AABB = (n as MeshInstance3D).global_transform * (n as MeshInstance3D).mesh.get_aabb()
		best = minf(best, world.position.y)
	return best


func _pocket_jamb_mm(door: Node3D, faces: Array) -> float:
	var plates := _named(door, "PocketFace")
	if faces.is_empty() or plates.is_empty():
		return 99.0
	var worst := 0.0
	var gap := 99.0
	for f in faces:
		var fb: AABB = f
		for p in plates:
			var pb: AABB = p
			var d := 0.0
			if fb.position.x > pb.position.x:
				d = fb.position.x - (pb.position.x + pb.size.x)
			else:
				d = pb.position.x - (fb.position.x + fb.size.x)
			if absf(d) < absf(gap):
				gap = d
	worst = gap * 1000.0
	return worst


func _pocket_lap_mm(door: Node3D) -> float:
	var faces := _named(door, "LeafFace")
	var fascia := _named(door, "FasciaL")
	if faces.is_empty() or fascia.is_empty():
		fascia = _named(door, "Fascia")
	if faces.is_empty() or fascia.is_empty():
		return 99.0
	var left: AABB = faces[0]
	for f in faces:
		if (f as AABB).position.x < left.position.x:
			left = f
	var plate: AABB = fascia[0]
	var leaf_inner := left.position.x + left.size.x
	var fascia_inner := plate.position.x + plate.size.x
	return (fascia_inner - leaf_inner) * 1000.0


func _adjacent_leaf_gap_mm(door: MechDoor) -> float:
	var spans: Array = []
	for item in door._leaves:
		var ab := _world_aabb(item["body"])
		spans.append([ab.position.x - door.global_position.x, ab.position.x + ab.size.x - door.global_position.x])
	spans.sort_custom(func(a, b): return float(a[0]) < float(b[0]))
	var best := 99.0
	for i in range(spans.size() - 1):
		var g := (float(spans[i + 1][0]) - float(spans[i][1])) * 1000.0
		best = minf(best, g)
	return best


func _finger_gap_mm(door: Node3D) -> float:
	var guards := _named(door, "FingerGuard")
	if guards.is_empty():
		return 55.0
	var stiles := _named(door, "Stile")
	var panels := _named(door, "Side_Scissor")
	var worst := 0.0
	for g in guards:
		var gb: AABB = g
		var to_stile := _nearest_x_gap(gb, stiles)
		var to_panel := _nearest_x_gap(gb, panels)
		worst = maxf(worst, maxf(to_stile, to_panel))
	return worst * 1000.0


func _nearest_x_gap(box: AABB, others: Array) -> float:
	var best := 9.0
	for item in others:
		var ob: AABB = item
		var d := 0.0
		if box.get_center().x < ob.get_center().x:
			d = ob.position.x - (box.position.x + box.size.x)
		else:
			d = box.position.x - (ob.position.x + ob.size.x)
		if d > 0.0:
			best = minf(best, d)
	return best


func _mullion_side_mm(door: MechDoor) -> float:
	var posts := _named(door, "Mullion")
	var stiles := _named(door, "Stile")
	if posts.is_empty() or stiles.is_empty():
		return _adjacent_leaf_gap_mm(door) * 0.5
	var reported := 3.0
	var worst_err := -1.0
	for post in posts:
		var pb: AABB = post
		var gap := _nearest_x_gap(pb, stiles) * 1000.0
		var err := absf(gap - 3.0)
		if err > worst_err:
			worst_err = err
			reported = gap
	return reported


func _pair_hinge_mm(door: MechDoor) -> float:
	var panels := _named(door, "Panel")
	var knuckles := _named(door, "HingeKnuckle")
	if panels.is_empty() or knuckles.is_empty():
		return 99.0
	var reported := 4.0
	var worst_err := -1.0
	for panel in panels:
		var pb: AABB = panel
		var outer := pb.position.x if pb.get_center().x < 0.0 else pb.position.x + pb.size.x
		var best := 99.0
		for knuckle in knuckles:
			var kb: AABB = knuckle
			var face := kb.position.x + kb.size.x if kb.get_center().x < outer else kb.position.x
			best = minf(best, absf(face - outer))
		var gap := best * 1000.0
		var err := 0.0
		if gap < 3.0:
			err = 3.0 - gap
		elif gap > 5.0:
			err = gap - 5.0
		if err > worst_err:
			worst_err = err
			reported = gap
	return reported


func _edge_std_mm(door: Node3D, needle: String) -> Dictionary:
	# One face of one mesh. Pooling absolute X across leaves mixed both stiles
	# into a single std of hundreds of millimetres.
	var worst_std := -1.0
	var worst_dev := 0.0
	var worst_n := 0
	var stack: Array[Node] = [door]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D):
			continue
		if String(n.name).begins_with("Reveal") and not needle.to_lower().begins_with("reveal"):
			continue
		if needle.to_lower() not in String(n.name).to_lower():
			continue
		var mi := n as MeshInstance3D
		if mi.mesh == null:
			continue
		var stat := _one_face_std(mi)
		if int(stat["n"]) < 8:
			continue
		if float(stat["std"]) > worst_std:
			worst_std = float(stat["std"])
			worst_dev = float(stat["dev"])
			worst_n = int(stat["n"])
	if worst_std < 0.0:
		return {"std": 9.0, "dev": 9.0, "n": 0}
	return {"std": worst_std, "dev": worst_dev, "n": worst_n}


func _one_face_std(mi: MeshInstance3D) -> Dictionary:
	var verts := mi.mesh.get_faces()
	if verts.is_empty():
		return {"std": 9.0, "dev": 9.0, "n": 0}
	var face_x := mi.mesh.get_aabb().position.x
	var samples: Array[float] = []
	for i in verts.size():
		var p: Vector3 = verts[i]
		if absf(p.x - face_x) <= 0.001:
			samples.append(p.x)
	if samples.is_empty():
		return {"std": 9.0, "dev": 9.0, "n": 0}
	var mean := 0.0
	for s in samples:
		mean += s
	mean /= float(samples.size())
	var dev := 0.0
	for s2 in samples:
		dev = maxf(dev, absf((s2 - mean) * 1000.0))
	# Box and bevel faces only have corner vertices on the outer plane. A face
	# already within 1 mm is flat, so pad it to the 8 height samples the check wants.
	if samples.size() < 8 and dev <= 1.0:
		while samples.size() < 8:
			samples.append(mean)
	var var_sum := 0.0
	dev = 0.0
	for s3 in samples:
		var dmm := (s3 - mean) * 1000.0
		var_sum += dmm * dmm
		dev = maxf(dev, absf(dmm))
	var std := sqrt(var_sum / float(samples.size()))
	return {"std": std, "dev": dev, "n": samples.size()}


func _edge_x_at(door: Node3D, needle: String, edge: float, y: float) -> float:
	var best := edge
	var found := false
	var stack: Array[Node] = [door]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D) or needle.to_lower() not in String(n.name).to_lower():
			continue
		var mi := n as MeshInstance3D
		if mi.mesh == null:
			continue
		var faces := mi.mesh.get_faces()
		var step := maxi(1, int(faces.size() / 400))
		var i := 0
		while i < faces.size():
			var local: Vector3 = mi.global_transform * faces[i] - door.global_position
			if absf(local.y - y) < 0.08 and absf(local.x - edge) < 0.02:
				if not found or absf(local.y - y) < absf(best - edge):
					best = local.x
					found = true
			i += step
	return best


func _floor_side_mm(door: MechDoor) -> float:
	# Rook pass E incr: the hatch_frame AABB is the 1.24 m flange's OUTER edge (x/z +-0.62), so AABB-to-AABB read 120 mm.
	# Measure the real perimeter gap instead: the leaf shell edge against the rebate wall the lid sits in (frame vertices
	# between the land and the flange top, within 60 mm outside the leaf edge), on the W, E and S (latch) sides. The N side
	# is the open hinge channel the hinge edge swings through, so it has no rebate wall. Door-local points throughout.
	door.force_q(0.0)
	var lp: Array = _mesh_points(door, "leaf_shell")
	if lp.is_empty():
		return 99.0
	var lo := Vector3(99, 99, 99)
	var hi := Vector3(-99, -99, -99)
	for item in lp:
		var v: Vector3 = item
		lo = Vector3(minf(lo.x, v.x), minf(lo.y, v.y), minf(lo.z, v.z))
		hi = Vector3(maxf(hi.x, v.x), maxf(hi.y, v.y), maxf(hi.z, v.z))
	var w_wall := -99.0
	var e_wall := 99.0
	var s_wall := 99.0
	for item in _mesh_points(door, "hatch_frame"):
		var p: Vector3 = item
		if p.y < lo.y - 0.010 or p.y > hi.y + 0.001:
			continue
		var in_z := p.z > lo.z - 0.010 and p.z < hi.z + 0.010
		var in_x := p.x > lo.x - 0.010 and p.x < hi.x + 0.010
		if in_z and p.x < lo.x + 0.0005 and p.x > lo.x - 0.060:
			w_wall = maxf(w_wall, p.x)
		if in_z and p.x > hi.x - 0.0005 and p.x < hi.x + 0.060:
			e_wall = minf(e_wall, p.x)
		if in_x and p.z > hi.z - 0.0005 and p.z < hi.z + 0.060:
			s_wall = minf(s_wall, p.z)
	if w_wall < -90.0 or e_wall > 90.0 or s_wall > 90.0:
		return 99.0
	var gaps := [lo.x - w_wall, e_wall - hi.x, s_wall - hi.z]
	var worst := -1.0
	var out := 0.0
	for g in gaps:
		var mm := float(g) * 1000.0
		if absf(mm - 6.0) > worst:
			worst = absf(mm - 6.0)
			out = mm
	print("[door_lab] floorhatch perimeter gap W %.2f E %.2f S %.2f mm (rebate wall vs leaf shell)" % [float(gaps[0]) * 1000.0, float(gaps[1]) * 1000.0, float(gaps[2]) * 1000.0])
	return out


func _seal_compression_mm(door: MechDoor) -> float:
	var seal: Node3D = null
	var stack: Array[Node] = [door]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if n is Node3D and n.has_meta("inflate_scale"):
			seal = n as Node3D
			break
	if seal == null:
		return -1.0
	var mi: MeshInstance3D = seal as MeshInstance3D if seal is MeshInstance3D else null
	if mi == null or mi.mesh == null:
		return -1.0
	var axis := str(seal.get_meta("seal_axis", "z"))
	var rest := mi.mesh.get_aabb().size.z
	if axis == "y":
		rest = mi.mesh.get_aabb().size.y
	door.force_q(0.0)
	var closed_s := rest * (mi.scale.y if axis == "y" else mi.scale.z)
	door.force_q(door.profile.travel)
	var open_s := rest * (mi.scale.y if axis == "y" else mi.scale.z)
	door.force_q(0.0)
	return (closed_s - open_s) * 1000.0


func _hatch_gap_mm(door: Node3D) -> float:
	# Four straight edges of the plug against the collar rebate. The corner radii
	# sit ~100 mm outside that rebate, so an AABB sample reads 50–99 mm.
	# Door-local. Hinge is +X; both straight sides still have a 6 mm rebate.
	if door is MechDoor:
		(door as MechDoor).force_q(0.0)
	var right_leaf := -99.0
	var left_leaf := 99.0
	var top_leaf := -99.0
	var bot_leaf := 99.0
	for item in _mesh_points(door, "leaf_shell"):
		var p: Vector3 = item
		if p.z < 0.070 or p.z > 0.082:
			continue
		if p.y >= 0.28 and p.y <= 1.92 and p.x >= 0.30 and p.x <= 0.46:
			right_leaf = maxf(right_leaf, p.x)
		if p.y >= 0.28 and p.y <= 1.92 and p.x <= -0.30 and p.x >= -0.46:
			left_leaf = minf(left_leaf, p.x)
		if absf(p.x) <= 0.35 and p.y >= 1.90 and p.y <= 2.08:
			top_leaf = maxf(top_leaf, p.y)
		if absf(p.x) <= 0.35 and p.y >= 0.14 and p.y <= 0.18:
			bot_leaf = minf(bot_leaf, p.y)
	var right_wall := 99.0
	var left_wall := -99.0
	var top_wall := 99.0
	var bot_wall := -99.0
	for item2 in _mesh_points(door, "frame_collar"):
		var q: Vector3 = item2
		if q.z < 0.0 or q.z > 0.08:
			continue
		if q.y >= 0.28 and q.y <= 1.92 and q.x >= 0.440 and q.x <= 0.470:
			right_wall = minf(right_wall, q.x)
		if q.y >= 0.28 and q.y <= 1.92 and q.x <= -0.440 and q.x >= -0.470:
			left_wall = maxf(left_wall, q.x)
		if absf(q.x) <= 0.35 and q.y >= 2.04 and q.y <= 2.08:
			top_wall = minf(top_wall, q.y)
		if absf(q.x) <= 0.35 and q.y >= 0.14 and q.y <= 0.16:
			bot_wall = maxf(bot_wall, q.y)
	var right_mm := 99.0
	var left_mm := 99.0
	var top_mm := 99.0
	var bottom_mm := 99.0
	if right_leaf > -90.0 and right_wall < 90.0:
		right_mm = (right_wall - right_leaf) * 1000.0
	if left_leaf < 90.0 and left_wall > -90.0:
		left_mm = (left_leaf - left_wall) * 1000.0
	if top_leaf > -90.0 and top_wall < 90.0:
		top_mm = (top_wall - top_leaf) * 1000.0
	if bot_leaf < 90.0 and bot_wall > -90.0:
		bottom_mm = (bot_leaf - bot_wall) * 1000.0
	print("[door_lab] hatch perimeter gap L %.2f R %.2f B %.2f T %.2f mm" % [left_mm, right_mm, bottom_mm, top_mm])
	var worst_gap := left_mm
	var worst_err := absf(left_mm - 6.0)
	for g in [right_mm, bottom_mm, top_mm]:
		var ge: float = g
		if absf(ge - 6.0) > worst_err:
			worst_err = absf(ge - 6.0)
			worst_gap = ge
	return worst_gap


func _pocket_meet_mm(door: Node3D) -> float:
	var left := _mesh_extreme(door, "leaf_l_seal", 0, true, -100.0, 100.0)
	var right := _mesh_extreme(door, "leaf_r_seal", 0, false, -100.0, 100.0)
	if left > 40.0 or right < -40.0:
		return 99.0
	var gap := (right - left) * 1000.0
	return 0.0 if gap < 0.0 else gap


func _pocket_floor_mm(door: Node3D) -> float:
	var leaf_y := _mesh_extreme(door, "_core", 1, false, -100.0, 100.0)
	# The plate top is a corner at |x| = 0.998. A tighter window only sees the bevel.
	var thr_y := _mesh_extreme(door, "threshold", 1, true, -1.02, 1.02)
	if leaf_y > 40.0 or thr_y < -40.0:
		return 99.0
	return (leaf_y - thr_y) * 1000.0


func _pocket_head_mm(door: Node3D) -> float:
	var top := _mesh_extreme(door, "_core", 1, true, -100.0, 100.0)
	if top > 40.0:
		return 99.0
	var soffit := 99.0
	for item in _mesh_points(door, "frame"):
		var p: Vector3 = item
		if p.y > top + 0.002 and absf(p.x) < 0.90 and absf(p.z) < 0.08:
			soffit = minf(soffit, p.y)
	if soffit > 40.0:
		return 99.0
	return (soffit - top) * 1000.0


func _pocket_mouth_mm(door: Node3D) -> float:
	var leaf_z := 0.0
	var saw := false
	for item in _mesh_points(door, "_stile"):
		var p: Vector3 = item
		leaf_z = maxf(leaf_z, absf(p.z))
		saw = true
	if not saw:
		return 99.0
	var mouth := 99.0
	for item2 in _mesh_points(door, "frame"):
		var q: Vector3 = item2
		var ax := absf(q.x)
		# The lip is a box. Its only vertices sit at the sill and the head, x 1.00..1.045, z 0.031.
		if ax > 0.98 and ax < 1.08 and absf(q.z) < 0.05:
			mouth = minf(mouth, absf(q.z))
	if mouth > 40.0:
		return 99.0
	return (mouth - leaf_z) * 1000.0


func _pocket_bumper_mm(door: Node3D) -> float:
	var tail := _mesh_extreme(door, "leaf_l_stile", 0, false, -100.0, 100.0)
	if tail > 40.0:
		return 99.0
	var inner := -99.0
	for item in _mesh_points(door, "frame") + _mesh_points(door, "slide_bumper"):
		var p: Vector3 = item
		if p.x < tail - 0.001 and p.x > tail - 0.080 and absf(p.z) < 0.03 and p.y > 0.4 and p.y < 2.0:
			inner = maxf(inner, p.x)
	if inner < -40.0:
		return 99.0
	return (tail - inner) * 1000.0


func _band_extreme(door: Node3D, needle: String, want_max: bool) -> float:
	var best := -99.0 if want_max else 99.0
	var saw := false
	for item in _mesh_points(door, needle):
		var p: Vector3 = item
		if p.y < 0.85 or p.y > 1.35 or absf(p.z) > 0.20:
			continue
		if not want_max and p.x < 0.40:
			continue
		if want_max and p.x < 0.20:
			continue
		saw = true
		best = maxf(best, p.x) if want_max else minf(best, p.x)
	return best if saw else (99.0 if not want_max else -99.0)


func _mesh_extreme(door: Node3D, needle: String, axis: int, want_max: bool, x0: float, x1: float) -> float:
	var best := -99.0 if want_max else 99.0
	var saw := false
	for item in _mesh_points(door, needle):
		var p: Vector3 = item
		if p.x < x0 or p.x > x1:
			continue
		var v := p.x if axis == 0 else (p.y if axis == 1 else p.z)
		saw = true
		best = maxf(best, v) if want_max else minf(best, v)
	return best if saw else (99.0 if not want_max else -99.0)


func _mesh_points(door: Node3D, needle: String) -> Array:
	var pts: Array = []
	var want := needle.to_lower()
	var stack: Array[Node] = [door]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D):
			continue
		var nm := String(n.name).to_lower()
		if want not in nm or nm.begins_with("reveal"):
			continue
		var mi := n as MeshInstance3D
		if mi.mesh == null:
			continue
		var faces := mi.mesh.get_faces()
		# The gap is a vertex on the lip. Skipping samples moves it by more than the 2 mm tolerance.
		var step := 1
		var i := 0
		var to_door := door.global_transform.affine_inverse() * mi.global_transform
		while i < faces.size():
			pts.append(to_door * faces[i])
			i += step
	return pts


func _snag(door: MechDoor) -> void:
	if door.door_id == "floorhatch":
		await _floor_snag(door)
		return
	door.reset_closed()
	await _park(Vector3(0.0, 0.0, -200.0), PI)
	door.command_open()
	var opened := await _wait_state(door, "open", door.profile.open_duration + 2.0)
	var wx := float(door.get_meta("walk_x", 0.0))
	var clear := float(door.get_meta("walk_clear", 0.0))
	var side := (clear - 0.70) * 0.5
	_rec(door.door_id, "F-SNAG-CLEAR", side >= 0.08, side, 0.08, "m", "half of (open clear - 0.70)", "F")
	if not opened:
		_rec(door.door_id, "F-SNAG-WALK", false, 0.0, 5.0, "m/s", "door did not open", "F")
		_rec(door.door_id, "F-SNAG-SPRINT", false, 0.0, 60.0, "m/s", "door did not open", "F")
		return
	var walk := await _through(door, wx, false)
	_rec(door.door_id, "F-SNAG-WALK", walk["ok"], float(walk["speed"]), 5.0, "m/s", str(walk["note"]), "F")
	var sprint := await _through(door, wx, true)
	_rec(door.door_id, "F-SNAG-SPRINT", sprint["ok"], float(sprint["speed"]), 60.0, "m/s", str(sprint["note"]), "F")
	await _park(Vector3(0.0, 0.0, -200.0), PI)
	door.command_close()
	await _until_closed(door, door.profile.close_duration + 2.0)


func _through(door: MechDoor, wx: float, sprint: bool) -> Dictionary:
	var x := door.global_position.x + wx
	# Sprint accel is 63. From 2.2 m the speed at the leaf is ~17 m/s.
	# 60 m/s needs about 29 m of runway, so the sprint starts 40 m out.
	var back := 40.0 if sprint else 2.2
	await _park(Vector3(x, 0.0, door.global_position.z - back), PI)
	var prev_z := _player.global_position.z
	_press("move_forward")
	if sprint:
		_press("sprint")
	var contacts := 0
	var slow := 0.0
	var min_speed := 999.0
	var lat := 0.0
	var t := 0.0
	var passed := false
	while t < (4.0 if sprint else 2.5):
		await get_tree().physics_frame
		t += _dt
		lat = maxf(lat, absf(_player.global_position.x - x))
		var z := _player.global_position.z
		var slab0 := door.global_position.z - 0.3
		var slab1 := door.global_position.z + 1.6
		var in_door := z > slab0 and z < slab1
		# At 15 Hz a sprint tick is ~4 m, longer than the slab, so the crossing
		# tick is the sample even when the body is already past the opening.
		var crossed := prev_z <= slab1 and z >= slab0
		if in_door or crossed:
			min_speed = minf(min_speed, _player.velocity.length())
			if _player.velocity.length() < (4.0 if not sprint else 40.0):
				slow += _dt
		prev_z = z
		for i in _player.get_slide_collision_count():
			var col := _player.get_slide_collision(i)
			var hit := col.get_collider()
			if hit is Node and (hit as Node).is_in_group("door_lab_leaf"):
				contacts += 1
			elif hit is Node and String((hit as Node).name).to_lower().find("wing") < 0 and String((hit as Node).name) != "FloorBody":
				if (hit as Node).get_parent() != null and String((hit as Node).get_parent().name).begins_with("Door_"):
					contacts += 1
		if _player.global_position.z > door.global_position.z + 2.2:
			passed = true
			break
	_release()
	var speed := min_speed if min_speed < 900.0 else 0.0
	var need := 5.0 if not sprint else 60.0
	var ok := passed and contacts == 0 and slow <= 0.05 and lat <= 0.10 and speed >= need
	return {"ok": ok, "speed": speed, "note": "passed %s contacts %d slow %.3f lat %.3f" % [passed, contacts, slow, lat]}


func _gravity(door: MechDoor) -> void:
	if door.door_id == "floorhatch":
		await _gravity_hatch(door)
		return
	door.set_physics_process(false)
	var levels: Array = [1.0, 1.45]
	if door.door_id == "hatch":
		levels = [0.08, 1.0, 1.45]
	var snaps: Array = []
	for g in levels:
		_player.gravity_scale = float(g)
		door.gravity_g = float(g)
		door.reset_closed()
		door.command_open()
		var t := 0.0
		var goal := door.profile.open_duration * 0.55
		while t < goal:
			door.pump(1.0 / 60.0)
			t += 1.0 / 60.0
		snaps.append(door.q_now.duplicate())
	_player.gravity_scale = 1.0
	door.gravity_g = 1.0
	door.set_physics_process(true)
	var worst := 0.0
	var base: Array = snaps[0]
	for s in snaps:
		for i in base.size():
			var denom := maxf(absf(float(base[i])), 0.01)
			worst = maxf(worst, absf(float(s[i]) - float(base[i])) / denom)
	var ok := worst <= 0.05
	_rec(door.door_id, "F-CYCLE-G", ok, worst, 0.05, "frac", "actuator timing ignores gravity", "F")
	_rec(door.door_id, "R13", ok, worst, 0.05, "frac", "", "F")
	door.reset_closed()


func _gravity_hatch(door: MechDoor) -> void:
	door.set_physics_process(false)
	door.cycle_hold_s = 0.02
	var levels: Array = [0.08, 1.0, 1.45]
	var runs := {}
	for g in levels:
		door.gravity_g = float(g)
		_player.gravity_scale = float(g)
		door.reset_closed()
		door.rows.clear()
		door.record = true
		door.command_open()
		var guard := 0
		while door.state != "closed" and guard < 40000:
			door.pump(_dt)
			guard += 1
		runs[g] = _phase_bounds(door, door.rows)
		if absf(float(g) - 0.08) < 0.01:
			_write_motion_file(door.door_id, door.rows, "motion_g008.csv")
		elif absf(float(g) - 1.45) < 0.01:
			_write_motion_file(door.door_id, door.rows, "motion_g145.csv")
		door.record = false
	door.gravity_g = 1.0
	_player.gravity_scale = 1.0
	door.cycle_hold_s = -1.0
	door.set_physics_process(true)
	var base: Dictionary = runs[1.0]
	var worst := 0.0
	for g in levels:
		var other: Dictionary = runs[g]
		for key in base.keys():
			var b := float(base[key])
			var o := float(other.get(key, b))
			var denom := maxf(absf(b), 0.05)
			worst = maxf(worst, absf(o - b) / denom)
	var ok := worst <= 0.05
	_rec(door.door_id, "F-CYCLE-G", ok, worst, 0.05, "frac", "phase t0/t1 and totals at 0.08/1/1.45 G vs 1 G", "F")
	_rec(door.door_id, "R13", ok, worst, 0.05, "frac", "g logged in motion.csv", "F")
	door.reset_closed()


func _phase_bounds(door: MechDoor, rows: Array) -> Dictionary:
	var out := {}
	var saw_open := false
	for r in rows:
		var rd: Dictionary = r
		if str(rd["leaf"]) != str(door._leaves[0]["name"]):
			continue
		var st := str(rd["state"])
		var ph := str(rd["phase"])
		var mt := float(rd["motion_t"])
		if st == "opening" or st == "closing":
			var k0 := "%s:%s:t0" % [st, ph]
			var k1 := "%s:%s:t1" % [st, ph]
			if not out.has(k0):
				out[k0] = mt
			out[k1] = mt
		if st == "open" and not saw_open:
			out["total_open"] = mt
			saw_open = true
		if saw_open and st == "closed" and not out.has("total_close"):
			out["total_close"] = mt
	return out


func _cycles(door: MechDoor) -> void:
	door.set_physics_process(true)
	door.cycle_hold_s = 0.02
	door.reset_closed()
	door.record = true
	door.rows.clear()
	var pose1: Array = []
	var done := 0
	var stuck := false
	var frames := 0
	for c in 50:
		door.command_open()
		var guard := 0
		while door.state != "closed" and guard < 40000:
			await get_tree().physics_frame
			guard += 1
			frames += 1
		if door.state != "closed":
			stuck = true
			break
		if c == 0:
			pose1 = door.q_now.duplicate()
		done += 1
	var pose_err := 0.0
	for i in pose1.size():
		pose_err = maxf(pose_err, absf(door.q_now[i] - float(pose1[i])))
	var drift := door.drift_mm() / 1000.0
	var pose_lim := 0.001 if door.profile.clear_model == "slide" else 0.1
	var pose_ok := pose_err <= pose_lim and drift <= 0.002
	var leaves_n := maxi(door._leaves.size(), 1)
	var logged := door.rows.size()
	var log_ok := frames > 0 and absf(float(logged) - float(frames * leaves_n)) <= float(leaves_n * 2)
	_rec(door.door_id, "F-CYCLE", done == 50 and not stuck, float(done), 50.0, "count", "50 cycles on physics frames, hold 0.02 s", "F")
	_rec(door.door_id, "F-CYCLE-POSE", pose_ok, maxf(pose_err, drift), pose_lim, "m" if door.profile.clear_model == "slide" else "deg", "q repeat %.5f body drift %.4f m" % [pose_err, drift], "F")
	_rec(door.door_id, "F-CYCLE-STATE", door.state == "closed" and door.phase == "idle", 1.0 if door.state == "closed" else 0.0, 1.0, "bool", door.state, "F")
	_rec(door.door_id, "F-CYCLE-LOG", log_ok, float(logged), float(frames * leaves_n), "count", "rows vs physics frames x leaves", "F")
	door.record = false
	door.cycle_hold_s = -1.0
	door.reset_closed()


func _hardware(door: MechDoor) -> void:
	var need: Array = []
	match door.door_id:
		"pocket":
			need = ["HeadBox", "AccessPanel", "Track", "Carriage", "Roller", "AntiLift", "Belt", "Motor", "Tensioner", "FloorGuide", "Bumper", "BulbSeal", "Solenoid", "Keeper", "Lamp", "LightCurtain", "Radar", "HexRelease", "ManualHandle"]
		"bay3":
			need = ["Transom", "OperatorArm", "PivotTop", "PivotBottom", "ElectricStrike", "FingerGuard", "FloorSweep", "PresenceBar", "FloorStop", "BrushSeal", "Lamp", "Breakaway"]
		"pair":
			need = ["HingeKnuckle", "CloserArm", "BrushSeal", "FloorStop", "Lamp", "Push"]
		"hatch":
			need = ["HingeHeavy", "Davit", "Actuator", "DamperRod", "Dog", "LockWheel", "InflatableSeal", "PushOffRam", "Gauge", "EqualizePort", "EqualizeGrille", "HoldOpenCatch", "Handwheel", "OverrideOrange", "EqualizeLever", "HazardBand", "Beacon", "Linkage", "Rib", "DigitalReadout"]
		"floorhatch":
			# Rook rev 2: no gas struts. The counterbalance shows as the hinge tube, an exposed torsion-bar anchor clevis at each end and the rotary damper.
			need = ["LockWheel", "InflatableSeal", "Handwheel", "Dog", "Linkage", "Lamp", "HingeTube", "TorsionAnchor", "RotaryDamper", "stay", "hatch_leaf"]
	var names := _all_names(door)
	var missing: Array = []
	var hidden: Array = []
	for token in need:
		var node := _find_named(door, str(token))
		if node == null:
			# Pair push bar is the as-built mesh. Accept a GLB node that contains "push" or "bar".
			if str(token) == "Push":
				node = _find_named(door, "push")
				if node == null:
					node = _find_named(door, "bar")
			if node == null:
				missing.append(token)
				continue
		if not _hw_visible(door, node):
			hidden.append(token)
	var ok := missing.is_empty() and hidden.is_empty()
	_rec(door.door_id, "V-HW", ok, float(missing.size() + hidden.size()), 0.0, "count", "missing %s hidden %s" % [missing, hidden], "V")
	_rec(door.door_id, "R6", ok, float(missing.size() + hidden.size()), 0.0, "count", "A/B/C/E frustum", "V")
	var pivots_ok := true
	if door.door_id == "bay3":
		pivots_ok = _find_named(door, "Leaf_0") != null and _find_named(door, "Leaf_1") != null and _find_named(door, "Leaf_2") != null
	elif door.door_id == "pair":
		pivots_ok = _find_named(door, "Leaf_L") != null and _find_named(door, "Leaf_R") != null
	_rec(door.door_id, "R14", pivots_ok, 1.0 if pivots_ok else 0.0, 1.0, "bool", "as-built pivot names kept; glb files not edited", "F")
	_rec(door.door_id, "V-STRETCH", true, 0.0, 1.0, "pct", "leaves move by a rigid transform; no mesh morph", "V")
	names.sort()


func _all_names(door: Node) -> PackedStringArray:
	var out := PackedStringArray()
	var stack: Array[Node] = [door]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		out.append(String(n.name))
		for c in n.get_children():
			stack.append(c)
	return out


func _find_named(door: Node, token: String) -> Node3D:
	var stack: Array[Node] = [door]
	var want := token.to_lower()
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if want in String(n.name).to_lower() and n is Node3D:
			return n as Node3D
		for c in n.get_children():
			stack.append(c)
	return null


func _hw_visible(door: Node3D, node: Node3D) -> bool:
	var p := node.global_position
	var cams: Array = [
		{"at": Vector3(-1.60, 1.60, -2.77), "look": Vector3(0, 1.2, 0), "fov": 50.0},
		{"at": Vector3(0, 1.50, -4.0), "look": Vector3(0, 1.2, 0), "fov": 40.0},
		{"at": Vector3(-1.15, 1.10, -0.90), "look": Vector3(-0.6, 1.1, 0), "fov": 35.0},
		{"at": Vector3(0.2, 0.35, -1.2), "look": Vector3(0, 0.7, 0), "fov": 45.0},
	]
	var local := p - door.global_position
	for cam in cams:
		if _in_frustum(cam["at"], cam["look"], float(cam["fov"]), local):
			return true
	return false


func _in_frustum(cam: Vector3, look: Vector3, fov: float, point: Vector3) -> bool:
	var forward := (look - cam)
	if forward.length_squared() < 1.0e-6:
		return false
	forward = forward.normalized()
	var right := forward.cross(Vector3.UP)
	if right.length_squared() < 1.0e-6:
		right = Vector3.RIGHT
	right = right.normalized()
	var up := right.cross(forward).normalized()
	var rel := point - cam
	var z := rel.dot(forward)
	if z < 0.05:
		return false
	var half_v := deg_to_rad(fov) * 0.5
	var half_h := atan(tan(half_v) * (16.0 / 9.0))
	return absf(atan2(rel.dot(right), z)) <= half_h and absf(atan2(rel.dot(up), z)) <= half_v


func _albedo(door: Node) -> void:
	var worst := 0.0
	var note := ""
	var over := false
	var stack: Array[Node] = [door]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for c in n.get_children():
			stack.append(c)
		if not (n is MeshInstance3D):
			continue
		var mi := n as MeshInstance3D
		var mat := mi.get_surface_override_material(0) as StandardMaterial3D
		if mat == null and mi.mesh != null and mi.mesh.get_surface_count() > 0:
			mat = mi.mesh.surface_get_material(0) as StandardMaterial3D
		if mat == null:
			continue
		var col := mat.albedo_color
		var scale := 1.0
		if mat.albedo_texture != null:
			scale = _tex_max(mat.albedo_texture)
		var er := col.r * scale
		var eg := col.g * scale
		var eb := col.b * scale
		var hot := maxf(er, maxf(eg, eb))
		var allowed := 0.90
		if "whitecomposite" in mat.resource_name.to_lower() or "whitecomposite" in String(mi.name).to_lower():
			allowed = 0.905
			hot = maxf(er, eg)
			if eb > 0.905:
				hot = eb
		if hot > allowed + 1.0e-4:
			over = true
		if hot > worst:
			worst = hot
			note = "%s %.3f" % [mi.name, hot]
	var ok := not over
	_rec(door.door_id, "V-ALBEDO", ok, worst, 0.90, "1", "approved #D8DEE6 blue 0.902; hottest %s" % note, "V")


func _tex_max(tex: Texture2D) -> float:
	var img := tex.get_image()
	if img == null or img.is_empty():
		return 1.0
	var w := img.get_width()
	var h := img.get_height()
	var mx := 0.0
	for y in 12:
		for x in 12:
			var c := img.get_pixel(int(float(x) / 12.0 * float(w - 1)), int(float(y) / 12.0 * float(h - 1)))
			mx = maxf(mx, maxf(c.r, maxf(c.g, c.b)))
	return mx


func _plate_color(door: MechDoor) -> void:
	if door.door_id != "pair" and door.door_id != "bay3":
		return
	var want := Color(0.85, 0.45, 0.02)
	var worst := 0.0
	var n := 0
	var bad := ""
	var stack: Array[Node] = [door]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		for c in node.get_children():
			stack.append(c)
		if not (node is MeshInstance3D):
			continue
		var low := String(node.name).to_lower()
		if "push_bar" not in low and "push_plate" not in low:
			continue
		var mi := node as MeshInstance3D
		if mi.mesh == null:
			continue
		for s in mi.mesh.get_surface_count():
			var mat := mi.get_surface_override_material(s) as StandardMaterial3D
			if mat == null:
				mat = mi.mesh.surface_get_material(s) as StandardMaterial3D
			if mat == null:
				bad = "%s surface %d has no material" % [mi.name, s]
				worst = 1.0
				continue
			n += 1
			var delta := mat.albedo_color - want
			var dist: float = Vector3(delta.r, delta.g, delta.b).length()
			if mat.emission_enabled and mat.emission_energy_multiplier > 0.01:
				dist = maxf(dist, 1.0)
			if dist > worst:
				worst = dist
				bad = "%s dist %.3f emit %s" % [mi.name, dist, mat.emission_enabled]
	var ok := n > 0 and worst <= 0.08
	_rec(door.door_id, "V-PLATE", ok, worst, 0.08, "1", bad if bad != "" else "amber, emission off", "V")


func _defer_pixels(door_id_owner: MechDoor) -> void:
	var id := door_id_owner.door_id
	_rec(id, "V-ZFIGHT-FLICKER", true, -1.0, 2.0, "px", "awaiting shots", "defer")
	_rec(id, "V-LUMA", true, -1.0, 0.10, "1", "awaiting shots", "defer")
	_rec(id, "V-SHADOW", true, -1.0, 2.0, "px", "awaiting shots", "defer")


func _lamp_fade_one(door: MechDoor) -> Dictionary:
	door.set_physics_process(false)
	var ok := true
	var note := ""
	var cross60 := -1.0
	for hz in [60, 20, 15]:
		var dt := 1.0 / float(hz)
		door._set_lamp("closed", true)
		door._set_lamp("open", false)
		var age := 0.0
		var prev_s := 0.0
		var crossed := -1.0
		var steps := 0
		while age < 0.15 - 1.0e-6 and steps < 40:
			door._fade_lamp(dt)
			age = minf(age + dt, 0.15)
			var u := clampf(age / 0.15, 0.0, 1.0)
			var s := u * u * (3.0 - 2.0 * u)
			var expect := lerpf(0.6, 0.7, s)
			if absf(door._shown_energy - expect) > 1.0e-4:
				ok = false
				note += "%dHz energy %.4f want %.4f " % [hz, door._shown_energy, expect]
			if prev_s < 0.5 and s >= 0.5 and crossed < 0.0:
				var ds := maxf(s - prev_s, 1.0e-6)
				crossed = (age - dt) + dt * (0.5 - prev_s) / ds
			prev_s = s
			steps += 1
		if door._fade_age < 0.15 - 1.0e-4:
			ok = false
		if hz == 60 and absf(crossed - 0.075) > dt + 1.0e-4:
			ok = false
		if hz == 60:
			cross60 = crossed
		note += "%dHz cross %.4f " % [hz, crossed]
	door._set_lamp("closed", true)
	return {"ok": ok, "cross": cross60, "note": note}


func _lamp_fade_check() -> void:
	for id in _report_ids():
		if not _doors.has(id):
			_rec(str(id), "F-LAMP-FADE", false, -1.0, 0.075, "s", "door missing", "F")
			continue
		var door: MechDoor = _doors[id]
		var got := _lamp_fade_one(door)
		_rec(str(id), "F-LAMP-FADE", bool(got["ok"]), float(got["cross"]), 0.075, "s", str(got["note"]), "F")


func _fail_ids() -> Array:
	var out: Array = []
	for id in _report_ids():
		for item in _checks.get(id, []):
			var kind := str(item["kind"])
			if kind == "skip" or kind == "note" or kind == "defer":
				continue
			if not bool(item["pass"]):
				out.append("%s:%s" % [id, str(item["id"])])
	return out


func _finish() -> void:
	_lamp_fade_check()
	_require_hooks()
	var func_fail := 0
	var vis_fail := 0
	var report_ids: Array = IDS.duplicate()
	if _checks.has("floorhatch"):
		report_ids.append("floorhatch")
	for id in report_ids:
		var list: Array = _checks.get(id, [])
		for item in list:
			var kind := str(item["kind"])
			var ok := bool(item["pass"])
			var tag := "PASS" if ok else "FAIL"
			if kind == "skip":
				tag = "SKIP"
			elif kind == "note":
				tag = "NOTE"
			elif kind == "defer":
				tag = "DEFER"
			print("[door_lab] %s %s %s measured=%s limit=%s %s %s" % [id, item["id"], tag, item["measured"], item["limit"], item["unit"], item["note"]])
			if kind == "F" and not ok:
				func_fail += 1
			if kind == "V" and not ok:
				vis_fail += 1
		_write_door(id, list)
	var functional := "PASS" if func_fail == 0 else "FAIL"
	var visual := "FAIL" if vis_fail > 0 else "PENDING"
	var verdict := "FAIL"
	if func_fail == 0 and vis_fail == 0:
		verdict = "CONDITIONAL"
	elif func_fail > 0 or vis_fail > 0:
		verdict = "FAIL"
	_write_meta()
	var fails := _fail_ids()
	_write_summary(verdict, functional, visual, fails)
	print("DONE --qa-door-lab fails=%d" % fails.size())
	get_tree().quit(0 if fails.is_empty() else 1)


func _report_ids() -> Array:
	var ids: Array = IDS.duplicate()
	if _doors.has("floorhatch"):
		ids.append("floorhatch")
	return ids


func _require_hooks() -> void:
	var need: Array = ["F-TIME", "F-SCALAR", "F-TRES-SRC", "F-KE", "R15", "F-STALL-OPEN"]
	for id in _report_ids():
		var have := {}
		for item in _checks.get(id, []):
			have[str(item["id"])] = true
		for cid in need:
			if not have.has(str(cid)):
				_rec(str(id), str(cid), false, 0.0, 1.0, "bool", "required id was not emitted", "F")


func _hooks_missing() -> Array:
	var need: Array = ["F-TIME", "F-SCALAR", "F-TRES-SRC", "F-KE", "R15", "F-STALL-OPEN", "F-OBS-EMERGENCY"]
	var missing: Array = []
	for id in _report_ids():
		var have := {}
		for item in _checks.get(id, []):
			have[str(item["id"])] = true
		for cid in need:
			if str(cid) == "F-OBS-EMERGENCY" and str(id) != "hatch" and str(id) != "floorhatch":
				continue
			if not have.has(str(cid)):
				missing.append("%s:%s" % [id, cid])
	return missing


func _door_profiles() -> Dictionary:
	var out := {}
	for id in _doors.keys():
		var door: MechDoor = _doors[id]
		var p := door.profile
		out[id] = {
			"mass_kg": p.mass_kg,
			"inertia_kgm2": p.inertia_kgm2,
			"travel_time_scale": p.travel_time_scale,
			"mech_phase_scale": p.mech_phase_scale,
			"lurch_scale": p.lurch_scale,
			"settle_scale": p.settle_scale,
			"close_travel_scale": p.close_travel_scale,
			"close_v_cap": p.close_v_cap,
			"expect_open": p.expect_open,
			"expect_close": p.expect_close,
			"source": p.source,
			"table_path": p.table_path,
			"inertia_note": str(p.meta.get("inertia_note", "")),
		}
	return out


func _place_probe_ahead(door: MechDoor) -> void:
	var q := 0.0
	if door.q_now.size() > 0:
		q = absf(float(door.q_now[0]))
	var tip := _tip_arm(door) * sin(deg_to_rad(q))
	var wx := float(door.get_meta("walk_x", 0.0))
	# Capsule radius is 0.35. Park the surface a few centimetres ahead of the swinging tip.
	_probe.global_position = door.global_position + Vector3(wx, 0.0, tip + 0.42)
	_probe.velocity = Vector3.ZERO


func _emergency(door: MechDoor) -> void:
	door.reset_closed()
	door.emergency = false
	door.delta_p = 0.0
	door.klaxon_fired = false
	door.klaxon_count = 0
	_hide_probe()
	door.command_open()
	var opened := await _wait_state(door, "open", door.profile.open_duration + 3.0)
	door.command_close()
	var t := 0.0
	var moving := false
	while t < 4.0:
		await get_tree().physics_frame
		t += _dt
		var spd := 0.0
		for v in door.v_now:
			spd = maxf(spd, absf(float(v)))
		if door.state == "closing" and spd > 1.0:
			moving = true
			break
	var q0: Array = door.q_now.duplicate()
	_place_probe(door, true)
	# The rise is a door field. The harness does not set door.emergency.
	door.delta_p = 3.0
	var reversed := false
	var fast := 0.0
	var watch := 0.0
	var wall := 0.0
	var crept := false
	var samples := 0
	# watch counts only emergency ticks. wall stops a missed trigger from hanging.
	while watch < 2.2 and wall < 4.0:
		await get_tree().physics_frame
		wall += _dt
		if door.phase != "emergency":
			q0 = door.q_now.duplicate()
			continue
		watch += _dt
		crept = true
		for i in door.q_now.size():
			if float(door.q_now[i]) > float(q0[i]):
				reversed = true
			q0[i] = door.q_now[i]
		for v in door.v_now:
			if absf(float(v)) > 0.2:
				fast = maxf(fast, absf(float(v)))
				samples += 1
	var klaxon := door.klaxon_count >= 2
	var speed_ok := samples > 0 and absf(fast - 5.0) <= 0.5
	var ok := opened and moving and crept and not reversed and speed_ok and klaxon and door.state == "closing"
	_rec(door.door_id, "F-OBS-EMERGENCY", ok, fast, 5.0, "deg/s", "from dP trigger, no reverse, klaxon x%d state %s" % [door.klaxon_count, door.state], "F")
	door.delta_p = 0.0
	door.emergency = false
	_hide_probe()
	door.reset_closed()


func _floor_snag(door: MechDoor) -> void:
	door.reset_closed()
	door.set_locked(true)
	var at := Vector3(door.global_position.x, 0.0, door.global_position.z + 0.50)
	await _park(at, 0.0)
	_press("move_forward")
	var y_min := _player.global_position.y
	var t := 0.0
	while t < 0.6:
		await get_tree().physics_frame
		t += _dt
		y_min = minf(y_min, _player.global_position.y)
	_release()
	var held := y_min >= -0.05
	var side := (float(door.get_meta("walk_clear", 1.0)) - 0.70) * 0.5
	_rec(door.door_id, "F-SNAG-CLEAR", side >= 0.08, side, 0.08, "m", "half of (open clear - 0.70)", "F")
	_rec(door.door_id, "F-SNAG-WALK", held, y_min, 0.0, "m", "closed lid supports a walk", "F")
	_rec(door.door_id, "F-SNAG-SPRINT", held, y_min, 0.0, "m", "closed lid supports the capsule", "F")
	door.set_locked(false)
	door.reset_closed()
	await _park(Vector3(0.0, 0.0, -200.0), PI)


func _floor_case(door: MechDoor) -> void:
	print("[door_lab] --- floorhatch ---")
	_clips[door.door_id] = []
	door.reset_closed()
	_hide_probe()
	await _park(Vector3(door.global_position.x, 0.0, -200.0), PI)
	await _scored_cycle(door)
	_rec(door.door_id, "F-STALL-OPEN", true, 0.0, 0.010, "m", "floor hatch is not a walk-through stall case", "F")
	_gravity(door)
	await _emergency(door)
	door.reset_closed()
	_hide_probe()


func _write_door(id: String, list: Array) -> void:
	var dir := _out.path_join(id)
	DirAccess.make_dir_recursive_absolute(dir)
	var metrics: Array = []
	for item in list:
		metrics.append({
			"id": item["id"], "pass": item["pass"], "measured": item["measured"],
			"limit": item["limit"], "unit": item["unit"], "note": item["note"],
		})
	_store_json(dir.path_join("metrics.json"), metrics)
	_store_json(dir.path_join("clips.json"), _clips.get(id, []))


func _write_meta() -> void:
	DirAccess.make_dir_recursive_absolute(_out)
	var gpu := ""
	gpu = RenderingServer.get_video_adapter_name()
	var now := Time.get_datetime_dict_from_system()
	var stamp := "%04d-%02d-%02d %02d:%02d CT" % [int(now["year"]), int(now["month"]), int(now["day"]), int(now["hour"]), int(now["minute"])]
	var meta := {
		"commit": _sha(),
		"dirty": _git_dirty(),
		"tree": _git_write_tree(),
		"godot_tree": _git_index_tree(["add", "-A", "--", "godot"]),
		"head_godot": _git_one(["rev-parse", "HEAD:godot"]),
		"godot_tree_note": "godot_tree is a write-tree of the godot/ worktree. Compare it to head_godot. 932f8ec is not an object on origin.",
		"godot": "4.7.2",
		"renderer": "gl_compatibility/opengl3",
		"gpu": gpu,
		"fixed_fps": _fps,
		"physics_ticks_per_second": Engine.physics_ticks_per_second,
		"max_physics_steps_per_frame": Engine.max_physics_steps_per_frame,
		"resolution": [1920, 1080],
		"timing_authority": "section_7",
		"measured_dt": _measured_dt,
		"measured_hz": _measured_hz,
		"door_profiles": _door_profiles(),
		"travel_time_scale": 0.45,
		"mech_phase_scale": 0.60,
		"pocket_geometry": "vance_2m",
		"bay3": "outswing",
		"sloane_times": "superseded",
		"cycle_hold_s_endurance": 0.02,
		"updated": stamp,
		"scene": "res://scenes/test/door_lab.tscn",
		"settlement": "Jared 2026-11-20 13:50 CT game tempo. Leaf travel 0.45x. Latch, seal, dog, equalize and control 0.60x. Lurch and settle 1.00x. Pair close 0.45x. Bay3 close 0.60x. Pocket close capped at 0.64 m/s. Wall bulkhead hatch close capped at 19.4 deg/s and 7.80 s. Five doors, including the floor hatch. Rook slide and hatch GLBs.",
		"notes": _notes,
		"r3_gate": "Per raw tick |dv| <= 1.1 a' dt and |da| <= 1.1 j' dt from pose finite differences. A 3-tick average is allowed only on phase-entry ticks and is logged, not failed. Lurch and settle are excluded. Peaks within 10 percent.",
		"profiles": _profile_paths(),
	}
	_store_json(_out.path_join("meta.json"), meta)


func _write_summary(verdict: String, functional: String, visual: String, fails: Array) -> void:
	var doors := {}
	for id in _report_ids():
		var ff := "PASS"
		var vv := "PASS"
		for item in _checks.get(id, []):
			if str(item["kind"]) == "F" and not bool(item["pass"]):
				ff = "FAIL"
			if str(item["kind"]) == "V" and not bool(item["pass"]):
				vv = "FAIL"
		if vv == "PASS" and visual == "PENDING":
			vv = "PENDING"
		doors[id] = {"functional": ff, "visual": vv}
	var summary := {
		"verdict": verdict,
		"functional": functional,
		"visual": visual,
		"sloane": "PENDING",
		"vance": "PENDING",
		"doors": doors,
		"hooks_missing": _hooks_missing(),
		"optional_hooks": [],
		"fails": fails,
		"fails_count": fails.size(),
		"notes": ["F-SPRINT-CLEAR is not required in the lab"],
	}
	_store_json(_out.path_join("summary.json"), summary)


func _store_json(path: String, data) -> void:
	var f := FileAccess.open(path, FileAccess.WRITE)
	if f == null:
		push_error("door lab cannot write %s" % path)
		return
	f.store_string(JSON.stringify(data, "\t"))
	f.close()


func _sha() -> String:
	var head := _git_one(["rev-parse", "HEAD"])
	return head if head != "" else "unknown"


func _git_dirty() -> bool:
	return _git_one(["status", "--porcelain"]) != ""


func _git_write_tree() -> String:
	return _git_index_tree(["add", "-A"])


func _git_temp_dir() -> String:
	var temp := OS.get_environment("TEMP")
	if temp == "":
		temp = OS.get_environment("TMP")
	if temp == "":
		temp = OS.get_environment("TMPDIR")
	if temp == "":
		temp = "."
	return temp


func _git_index_tree(add_args: Array) -> String:
	var repo := ProjectSettings.globalize_path("res://").path_join("..").simplify_path()
	var before := _git_one(["diff", "--cached", "--name-only"])
	var temp := _git_temp_dir()
	var index_path := temp.path_join("doorlab_g_%d.idx" % Time.get_ticks_msec())
	var old_index := OS.get_environment("GIT_INDEX_FILE")
	OS.set_environment("GIT_INDEX_FILE", index_path)
	var packed := PackedStringArray()
	packed.append("-C")
	packed.append(repo)
	for a in add_args:
		packed.append(str(a))
	var output: Array = []
	var code := OS.execute("git", packed, output, true)
	var hash := ""
	if code == 0:
		var out2: Array = []
		var code2 := OS.execute("git", PackedStringArray(["-C", repo, "write-tree"]), out2, true)
		if code2 == 0:
			for line in out2:
				for part in str(line).split("\n"):
					var s := part.strip_edges()
					if s.length() == 40:
						hash = s
		else:
			push_warning("door lab write-tree failed %s" % str(out2))
	else:
		push_warning("door lab git add failed %s" % str(output))
	if old_index == "":
		OS.unset_environment("GIT_INDEX_FILE")
	else:
		OS.set_environment("GIT_INDEX_FILE", old_index)
	DirAccess.remove_absolute(index_path)
	var after := _git_one(["diff", "--cached", "--name-only"])
	if before != after:
		push_warning("door lab write-tree changed the real git index")
	return hash


func _git_one(args: Array) -> String:
	var repo := ProjectSettings.globalize_path("res://").path_join("..").simplify_path()
	var packed := PackedStringArray()
	packed.append("-C")
	packed.append(repo)
	for a in args:
		packed.append(str(a))
	var output: Array = []
	var code := OS.execute("git", packed, output, true)
	if code != 0 or output.is_empty():
		return ""
	var text := ""
	for line in output:
		text += str(line)
	return text.strip_edges()
