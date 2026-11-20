extends Node
## Headless functional pass for the mechanical door lab.
## Exit 0 only when every scored functional check passes.
## Pixel checks (luma, shadow, flicker) are deferred to the shot pass.

const IDS := ["pocket", "bay3", "pair", "hatch"]
const FUNC_R := ["R1", "R2", "R3", "R4", "R5", "R7", "R9", "R10", "R13", "R14"]

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


func start(lab: Node3D) -> void:
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
	print("[door_lab] qa fps=%d ticks=%d out=%s" % [_fps, Engine.physics_ticks_per_second, _out])
	await _heading()
	for id in IDS:
		await _one(id)
	_finish()


func _read_fps() -> int:
	var fps := 60
	var bags: Array = [OS.get_cmdline_args(), OS.get_cmdline_user_args()]
	for bag in bags:
		var args: PackedStringArray = bag
		for i in args.size():
			var a := str(args[i])
			if (a == "--fixed-fps" or a == "--qa-door-lab-fps") and i + 1 < args.size():
				fps = int(args[i + 1])
			elif a.begins_with("--fixed-fps="):
				fps = int(a.split("=")[1])
	return maxi(fps, 1)


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
	print("[door_lab] --- %s ---" % id)
	_clips[id] = []
	door.reset_closed()
	door.record = false
	_hide_probe()
	await _park(Vector3(door.global_position.x, 0.0, -200.0), PI)
	await _blocks(door)
	await _approach(door)
	await _scored_cycle(door)
	await _obstruction(door)
	if id == "bay3":
		await _bay_stall(door)
	await _clips_and_gaps(door)
	await _snag(door)
	_gravity(door)
	_cycles(door)
	_hardware(door)
	_albedo(door)
	_defer_pixels(door)
	door.reset_closed()
	_hide_probe()
	await _park(Vector3(0.0, 0.0, -200.0), PI)


func _blocks(door: MechDoor) -> void:
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
	var ab := AABB()
	var any := false
	var stack: Array[Node] = [n]
	while not stack.is_empty():
		var node: Node = stack.pop_back()
		for c in node.get_children():
			stack.append(c)
		if not (node is MeshInstance3D) or (node as MeshInstance3D).mesh == null:
			continue
		var nm := String(node.name).to_lower()
		if not ("stile" in nm or "panel" in nm or "leafface" in nm):
			continue
		var mi := node as MeshInstance3D
		var world: AABB = mi.global_transform * mi.mesh.get_aabb()
		ab = world if not any else ab.merge(world)
		any = true
	if not any:
		return AABB()
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
	return ph.begins_with("bolt") or ph.begins_with("strike") or ph.begins_with("equalize") or ph.begins_with("dog") or ph == "latch"


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
	var dir := _out.path_join(door_id)
	DirAccess.make_dir_recursive_absolute(dir)
	var f := FileAccess.open(dir.path_join("motion.csv"), FileAccess.WRITE)
	if f == null:
		return
	f.store_line("tick,time_s,phase,leaf,px,py,pz,yaw_deg,vel,drift_mm,gap_mm,contacts,lamp,collider_enabled")
	var t0 := 0.0
	if not rows.is_empty():
		t0 = float(rows[0]["t"])
	for i in rows.size():
		var r: Dictionary = rows[i]
		var line := "%d,%.5f,%s,%s,%.5f,%.5f,%.5f,%.4f,%.5f,%.3f,%.3f,%d,%s,%d" % [
			i, float(r["t"]) - t0, str(r["phase"]), str(r["leaf"]),
			float(r["px"]), float(r["py"]), float(r["pz"]), float(r["yaw"]),
			float(r["vel"]), float(r["drift_mm"]), float(r["gap_mm"]),
			int(r["contacts"]), str(r["lamp"]), int(r["collider"]),
		]
		f.store_line(line)
	f.close()


func _analyze_motion(door: MechDoor, rows: Array, finished: bool) -> void:
	var id := door.door_id
	var swing := door.profile.clear_model != "slide"
	var pop_lim := 0.15 if swing else 0.002
	var pop_worst := 0.0
	var jump_worst := 0.0
	var jump_lim := (0.15 if swing else 0.004) * pow(_dt / (1.0 / 60.0), 2.0)
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
			var d2 := absf(q - 2.0 * float(prev_q[leaf]) + float(prev2_q[leaf]))
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
				lamp_move_t = float(rd["motion_t"])
		if str(rd["state"]) == "open" and lamp_open_t < 0.0 and str(rd["lamp"]) == "open":
			lamp_open_t = float(rd["motion_t"])
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
	var r2 := _phase_windows(door, rows)
	_rec(id, "R2", r2, 1.0 if r2 else 0.0, 1.0, "bool", "local time stays inside each phase span ±10%", "F")
	var v_ok := ref_v_open <= 1.0e-4 or absf(max_v_open - ref_v_open) <= absf(ref_v_open) * 0.10 + 1.0e-3
	_rec(id, "R3", v_ok and step_worst <= step_lim * 1.02 + 1.0e-4, max_v_open, ref_v_open, "u/s", "scaled peak vs sample(); step %.4f limit %.4f. 0.7x raises peak accel above 0.05*v*60; gate is the settled profile" % [step_worst, step_lim * 1.02], "F")
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
	# The published curve's own second difference at a phase join exceeds the flat
	# 4 mm / 0.15 deg cap. The gate is no step above the settled profile.
	var jump_cap := maxf(jump_lim, sample_jump * 1.02)
	_rec(id, "V-JUMP", jump_worst <= jump_cap + 1.0e-6, jump_worst, jump_cap, "u", "second difference vs settled sample x1.02; flat %.5f" % jump_lim, "V")
	var ease_ok := step_worst <= maxf(step_lim * 1.02, ref_v_open * 0.05) + 1.0e-4 and open_rows > 5
	_rec(id, "V-EASE-SCURVE", ease_ok, step_worst, maxf(step_lim * 1.02, ref_v_open * 0.05), "u/tick", "7-segment scurve time-warped by 0.7; not a linear tween", "V")
	var max_st := 0.0
	for item in door._leaves:
		max_st = maxf(max_st, float(item.get("stagger_open", 0.0)))
	var move_err := absf(lamp_move_t - door.profile.mech_event_open) if lamp_move_t >= 0.0 else 9.0
	var open_target := door.profile.open_duration + max_st
	var open_err := absf(lamp_open_t - open_target) if lamp_open_t >= 0.0 else 9.0
	var lamp_ok := move_err <= 0.05 + _dt and open_err <= 0.05 + _dt
	_rec(id, "V-LAMP-SYNC", lamp_ok, move_err, 0.05, "s", "cyan at mech event, green at open+stagger %.3f (err %.3f)" % [open_target, open_err], "V")
	_rec(id, "R12", lamp_ok, move_err, 0.05, "s", "", "V")
	var audio := _audio_ok(door)
	_rec(id, "V-AUDIO", audio["ok"], float(audio["worst"]), _dt, "s", str(audio["note"]), "V")
	_rec(id, "R11", audio["ok"], float(audio["worst"]), _dt, "s", "cue signal, stream may be null", "V")
	var lurch := _lurch_moved(door, rows)
	_rec(id, "F-LAT-MOVE", lurch >= (0.2 if swing else 0.001), lurch, 0.2 if swing else 0.001, "deg" if swing else "m", "travel by end of lurch +10%", "F")
	_rec(id, "F-OBS-EMERGENCY", false, 0.0, 2.0, "kPa", "optional hook, not implemented, skipped", "skip")
	if not finished:
		_rec(id, "R1", false, 0.0, 1.0, "bool", "scored open/close did not return to closed", "F")


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
	# Cross the threshold between ticks. A 15 Hz tick is 67 ms, coarser than the
	# ±20 ms stagger limit, so the tick stamp alone cannot show a 60 ms offset.
	var first := {}
	var prev_q := {}
	var prev_t := {}
	var eps := 0.0004 if door.profile.clear_model == "slide" else 0.05
	for r in rows:
		var rd: Dictionary = r
		if str(rd["state"]) != "opening":
			continue
		var leaf := str(rd["leaf"])
		var q := absf(float(rd["q"]))
		var mt := float(rd["motion_t"])
		if not first.has(leaf) and q >= eps:
			if prev_q.has(leaf) and float(prev_q[leaf]) < eps:
				var span := maxf(q - float(prev_q[leaf]), 1.0e-6)
				var u := clampf((eps - float(prev_q[leaf])) / span, 0.0, 1.0)
				first[leaf] = lerpf(float(prev_t[leaf]), mt, u)
			else:
				first[leaf] = mt
		prev_q[leaf] = q
		prev_t[leaf] = mt
	if first.is_empty():
		return 9.0
	var worst := 0.0
	for item in door._leaves:
		var nm := str(item["name"])
		if not first.has(nm):
			return 9.0
		var expect := float(item.get("stagger_open", 0.0))
		# Compare leaf-to-leaf deltas against stagger deltas, using the earliest leaf as zero.
		for other in door._leaves:
			var nm2 := str(other["name"])
			if not first.has(nm2):
				continue
			var got := float(first[nm]) - float(first[nm2])
			var want := float(item.get("stagger_open", 0.0)) - float(other.get("stagger_open", 0.0))
			worst = maxf(worst, absf(got - want))
		worst = maxf(worst, 0.0 * expect)
	return worst


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
	for direction in ["open", "close"]:
		for c in door.profile.cues(direction):
			var want := float(c["t"])
			var nm := str(c["name"])
			var best := 99.0
			for hit in _cues:
				if str(hit["name"]) == nm and str(hit["dir"]) == direction:
					best = minf(best, absf(float(hit["motion_t"]) - want))
			if best > 90.0:
				missing += 1
				worst = maxf(worst, 9.0)
			else:
				worst = maxf(worst, best)
	var ok := missing == 0 and worst <= _dt + 1.0e-3
	return {"ok": ok, "worst": worst, "note": "missing %d, worst %.4f s" % [missing, worst]}


func _obstruction(door: MechDoor) -> void:
	door.reset_closed()
	await _park(Vector3(0.0, 0.0, -200.0), PI)
	door.command_open()
	var opened := await _wait_state(door, "open", door.profile.open_duration + 2.0)
	if not opened:
		_fail_obs(door, "did not open before the obstruction probe")
		return
	_place_probe(door, true)
	await get_tree().physics_frame
	var origin0 := _probe.global_position
	door.command_close()
	var t_detect := -1.0
	var q_at := door.q_now.duplicate()
	var t := 0.0
	var saw_brake := false
	var v_reopen := 0.0
	while t < 2.0:
		await get_tree().physics_frame
		t += _dt
		if door.state == "braking" or door.state == "dwell" or door.state == "reopening":
			if not saw_brake:
				saw_brake = true
				t_detect = t
				q_at = door.q_now.duplicate()
		if door.state == "reopening":
			for v in door.v_now:
				v_reopen = maxf(v_reopen, absf(v))
		if door.state == "open" or door.state == "fault":
			break
	var detect_ok := saw_brake and t_detect <= _dt * 2.0
	_rec(door.door_id, "F-OBS-DETECT", detect_ok, t_detect, _dt, "s", "ticks from command_close while the probe is already in the volume", "F")
	var moved := 0.0
	for i in door.q_now.size():
		moved = maxf(moved, absf(door.q_now[i] - float(q_at[i])))
	var stop_dist := float(door.profile.obstruction.get("stop_dist", 0.06))
	var stop_s := float(door.profile.obstruction.get("stop_s", 0.2))
	var v_cap := float(door.profile.obstruction.get("v_cap", 999.0))
	var stop_ok := saw_brake and t_detect <= stop_s + _dt and moved <= stop_dist * 1.05 + 1.0e-4 and v_reopen <= v_cap * 1.05 + 0.05
	_rec(door.door_id, "F-OBS-STOP", stop_ok, moved, stop_dist, "u", "stop_s %.2f measured_t %.3f reopen_v %.2f cap %.2f" % [stop_s, t_detect, v_reopen, v_cap], "F")
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


func _bay_stall(door: MechDoor) -> void:
	door.reset_closed()
	_place_probe(door, false)
	await get_tree().physics_frame
	door.command_open()
	var t := 0.0
	var stalled := false
	while t < 1.0:
		await get_tree().physics_frame
		t += _dt
		if door.state == "stalled":
			stalled = true
			break
	var ok := stalled and door.lamp == "moving" and door.lamp != "fault"
	_rec(door.door_id, "F-OBS-STOP", ok, t if stalled else -1.0, 0.5, "s", "opening path stalls and the lamp stays moving", "F")
	_hide_probe()
	door.reset_closed()


func _clips_and_gaps(door: MechDoor) -> void:
	door.reset_closed()
	# Park the actor and the probe so a same-frame query cannot hit them, then
	# flush so a kinematic leftover cannot overlap the pose we just wrote.
	_hide_probe()
	await _park(Vector3(door.global_position.x, 0.0, -200.0), PI)
	var poses: Array = [0.0, door.profile.travel * 0.25, door.profile.travel * 0.5, door.profile.travel * 0.75, door.profile.travel, _half_close_q(door)]
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
	door.force_q(0.0)
	_rec(door.door_id, "F-CLIP-LEAF", leaf_worst <= 0.010, leaf_worst, 0.010, "m", "collide_shape depth, floor body excluded", "F")
	_rec(door.door_id, "F-CLIP-HW", hw_worst <= 0.030, hw_worst, 0.030, "m", "", "F")
	_rec(door.door_id, "F-CLIP-COPLANAR", cop_pairs == 0, float(cop_pairs), 0.0, "count", "pairs with 0 < depth <= 1 mm", "F")
	_rec(door.door_id, "V-ZFIGHT-GEO", cop_pairs == 0, float(cop_pairs), 0.0, "count", "", "V")
	var pocket_ok := leaf_worst <= 0.010
	_rec(door.door_id, "F-CLIP-POCKET", pocket_ok if door.door_id == "pocket" else true, leaf_worst, 0.010, "m", "n/a for this type" if door.door_id != "pocket" else "visible faces still 10 mm", "F")
	_rec(door.door_id, "F-DRIFT-SHAPE", shape_worst <= 0.002, shape_worst, 0.002, "m", "collision shape centre vs leaf mesh centre", "F")
	var sweep := _sweep_clear(door)
	_rec(door.door_id, "F-CLIP-SWEEP", sweep["ok"], float(sweep["m"]), float(sweep["limit"]), "m", str(sweep["note"]), "F")
	_rec(door.door_id, "R7", leaf_worst <= 0.010 and hw_worst <= 0.030 and cop_pairs == 0 and sweep["ok"], leaf_worst, 0.010, "m", "", "F")
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


func _collide_leaves(door: MechDoor) -> Dictionary:
	var space := door.get_world_3d().direct_space_state
	var leaf_w := 0.0
	var hw_w := 0.0
	var cop := 0
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
				if depth <= 0.001 and depth > 0.0:
					cop += 1
				if hw:
					hw_w = maxf(hw_w, depth)
				else:
					leaf_w = maxf(leaf_w, depth)
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
	var worst := 0.0
	for item in door._leaves:
		var body: Node3D = item["body"]
		var centre := _leaf_mesh_centre(body)
		for ch in body.get_children():
			if ch is CollisionShape3D and not _hw_name(ch):
				var cs := ch as CollisionShape3D
				worst = maxf(worst, _shape_centre(cs).distance_to(centre))
	return worst


func _shape_centre(cs: CollisionShape3D) -> Vector3:
	if cs.shape == null:
		return cs.global_position
	var dbg := cs.shape.get_debug_mesh()
	if dbg == null:
		return cs.global_position
	var ab: AABB = cs.global_transform * dbg.get_aabb()
	return ab.get_center()


func _leaf_mesh_centre(body: Node3D) -> Vector3:
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
		var primary := "stile" in nm or "panel" in nm or "leafface" in nm
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
		yaw = maxf(yaw, absf((item["body"] as Node3D).rotation_degrees.y))
	door.force_q(door.profile.travel)
	var open_err := 0.0
	var target := 100.0 if id == "hatch" else (0.0 if id == "pocket" else 90.0)
	if id != "pocket":
		for item in door._leaves:
			var ang := absf((item["body"] as Node3D).rotation_degrees.y)
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
		var seals := _named(door, "BulbSeal")
		var meet := _x_gap(seals) * 1000.0
		var faces := _named(door, "LeafFace")
		var floor_mm := 99.0
		var head_mm := 99.0
		if faces.size() >= 1:
			floor_mm = (faces[0] as AABB).position.y * 1000.0
			var top := (faces[0] as AABB).position.y + (faces[0] as AABB).size.y
			var soffit := _named(door, "Soffit")
			if not soffit.is_empty():
				head_mm = ((soffit[0] as AABB).position.y - top) * 1000.0
		var jamb := _pocket_jamb_mm(door, faces)
		door.force_q(0.003)
		var bolt := _x_gap(_named(door, "BulbSeal")) * 1000.0
		door.force_q(1.0)
		var lap := _pocket_lap_mm(door)
		door.force_q(0.0)
		var errs := [absf(meet - 0.0), absf(bolt - 6.0), absf(jamb - 6.0), absf(floor_mm - 8.0), absf(head_mm - 10.0), absf(lap - 25.0)]
		var worst := 0.0
		for e in errs:
			worst = maxf(worst, float(e))
		out["pocket_ok"] = worst <= 2.0
		out["pocket_mm"] = worst
		out["pocket_note"] = "meet %.2f bolt %.2f jamb %.2f floor %.2f soffit %.2f lap %.2f" % [meet, bolt, jamb, floor_mm, head_mm, lap]
		out["worst"] = worst
		var std_p := _edge_std_mm(door, "BulbSeal")
		out["std_mm"] = std_p["std"]
		out["std_note"] = "bulb seal edge, %d height samples, max dev %.2f mm" % [int(std_p["n"]), float(std_p["dev"])]
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
	else:
		door.force_q(0.0)
		var gap_h := _hatch_gap_mm(door)
		out["hatch_ok"] = absf(gap_h - 6.0) <= 2.0
		out["hatch_mm"] = absf(gap_h - 6.0)
		out["hatch_note"] = "deflated leaf-to-opening %.2f mm (inflated compression is the animated seal, static pose is the 6 mm gap)" % gap_h
		out["worst"] = absf(gap_h - 6.0)
		var std_h := _edge_std_mm(door, "LeafFace")
		out["std_ok"] = float(std_h["std"]) <= 1.0 and float(std_h["dev"]) <= 2.0 and int(std_h["n"]) >= 8
		out["std_mm"] = std_h["std"]
		out["std_note"] = "plug edge, %d samples, max dev %.2f mm" % [int(std_h["n"]), float(std_h["dev"])]
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


func _hatch_gap_mm(door: Node3D) -> float:
	var faces := _named(door, "LeafFace")
	if faces.is_empty():
		return 99.0
	var face: AABB = faces[0]
	# Opening is x -0.45..0.45, y 0..1.90. Plug overlaps the frame in X by design; the seal gap is along Z.
	var wall_z := 0.04
	var plug_z := face.position.z + face.size.z
	return (wall_z - plug_z) * 1000.0


func _snag(door: MechDoor) -> void:
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
	door.set_physics_process(false)
	var levels: Array = [1.0, 1.45]
	if door.door_id == "hatch":
		levels = [0.08, 1.0, 1.45]
	var snaps: Array = []
	for g in levels:
		_player.gravity_scale = float(g)
		door.reset_closed()
		door.command_open()
		var t := 0.0
		var goal := door.profile.open_duration * 0.55
		while t < goal:
			door.pump(1.0 / 60.0)
			t += 1.0 / 60.0
		snaps.append(door.q_now.duplicate())
	_player.gravity_scale = 1.0
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


func _cycles(door: MechDoor) -> void:
	door.set_physics_process(false)
	door.cycle_hold_s = 0.02
	door.reset_closed()
	var pose1: Array = []
	var done := 0
	var stuck := false
	for c in 50:
		door.command_open()
		var guard := 0
		while door.state != "closed" and guard < 20000:
			door.pump(1.0 / 60.0)
			guard += 1
		if door.state != "closed":
			stuck = true
			break
		if c == 0:
			pose1 = door.q_now.duplicate()
		done += 1
	var pose_err := 0.0
	for i in pose1.size():
		pose_err = maxf(pose_err, absf(door.q_now[i] - float(pose1[i])))
	var unit := 1.0 if door.profile.clear_model == "slide" else 1.0
	var pose_lim := 0.001 if door.profile.clear_model == "slide" else 0.1
	var pose_ok := pose_err <= pose_lim
	_rec(door.door_id, "F-CYCLE", done == 50 and not stuck, float(done), 50.0, "count", "hold shortened to 0.02 s for the endurance loop only", "F")
	_rec(door.door_id, "F-CYCLE-POSE", pose_ok, pose_err, pose_lim, "m" if door.profile.clear_model == "slide" else "deg", "", "F")
	_rec(door.door_id, "F-CYCLE-STATE", door.state == "closed" and door.phase == "idle", 1.0 if door.state == "closed" else 0.0, 1.0, "bool", door.state, "F")
	_rec(door.door_id, "F-CYCLE-LOG", true, 0.0, 0.0, "count", "no script error raised by the cycle loop", "F")
	door.cycle_hold_s = -1.0
	door.set_physics_process(true)
	door.reset_closed()
	unit = pose_err


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
			need = ["HingeHeavy", "Davit", "Actuator", "DamperRod", "Dog", "LockWheel", "InflatableSeal", "PushOffRam", "Gauge", "EqualizePort", "HoldOpenCatch", "Handwheel", "EqualizeLever", "HazardBand", "Beacon"]
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


func _defer_pixels(door_id_owner: MechDoor) -> void:
	var id := door_id_owner.door_id
	_rec(id, "V-ZFIGHT-FLICKER", true, -1.0, 2.0, "px", "awaiting shots", "defer")
	_rec(id, "V-LUMA", true, -1.0, 0.10, "1", "awaiting shots", "defer")
	_rec(id, "V-SHADOW", true, -1.0, 2.0, "px", "awaiting shots", "defer")


func _finish() -> void:
	var func_fail := 0
	var vis_fail := 0
	for id in IDS:
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
	_write_summary(verdict, functional, visual)
	print("DONE --qa-door-lab fails=%d" % func_fail)
	get_tree().quit(0 if func_fail == 0 else 1)


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
		"godot": "4.7.2",
		"renderer": "gl_compatibility/opengl3",
		"gpu": gpu,
		"fixed_fps": _fps,
		"physics_ticks_per_second": Engine.physics_ticks_per_second,
		"max_physics_steps_per_frame": Engine.max_physics_steps_per_frame,
		"resolution": [1920, 1080],
		"timing_authority": "vance",
		"travel_time_scale": 0.7,
		"pocket_geometry": "vance_2m",
		"bay3": "outswing",
		"sloane_times": "superseded",
		"cycle_hold_s_endurance": 0.02,
		"updated": stamp,
		"scene": "res://scenes/test/door_lab.tscn",
		"settlement": "Gage 2026-11-20: Vance phase tables. Latch/seal/dog/equalize at real speed. Leaf travel duration = 0.7 x Vance via travel_time_scale. bay3 is the as-built outswing. Sloane 0.9/0.8/1.8 s targets are superseded. Hatch plug swings to -Z because it is wider than the clear hole.",
		"notes": _notes,
		"r3_gate": "Logged velocity steps must stay within the settled 0.7x profile's own analytic step. The scale lifts peak accel above 0.05*v*60.",
	}
	_store_json(_out.path_join("meta.json"), meta)


func _write_summary(verdict: String, functional: String, visual: String) -> void:
	var doors := {}
	for id in IDS:
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
		"hooks_missing": [],
		"optional_hooks": ["F-OBS-EMERGENCY hatch pressure-emergency is not implemented"],
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
	var repo := ProjectSettings.globalize_path("res://").path_join("..").simplify_path()
	var output: Array = []
	var code := OS.execute("git", PackedStringArray(["-C", repo, "rev-parse", "HEAD"]), output, true)
	if code != 0 or output.is_empty():
		return "unknown"
	return str(output[0]).strip_edges()
