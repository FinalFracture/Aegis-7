extends Node
## --qa-tower-swim. Real PlayerBody: float in each tank, climb out, jump the 3 m board.

var ppa: PrefacePlayableArea
var _failures: int = 0
var _stuck: String = ""


func _ready() -> void:
	_qa_run.call_deferred()


func _qa_run() -> void:
	var guard := 0
	while (ppa == null or not ppa.has_meta("exterior_spawned") or ppa._tt_pool == null or ppa._player_body == null) and guard < 4000:
		await get_tree().physics_frame
		guard += 1
	if ppa == null or ppa._player_body == null or ppa._tower == null or ppa._tt_pool == null:
		print("QA_TOWER_SWIM FAIL | setup | player/tower/pool missing")
		print("QA_TOWER_SWIM DONE failures=1")
		get_tree().quit(1)
		return
	ppa._return_to_player()
	_qa_probe_lid()
	# z=12 is a lane centre (ropes at 11.0 and 13.5). The lowest ray can
	# thread a gap between float segments and then the capsule sits on them.
	var lap_drop := Vector3(12.0, 4.0, 12.0)
	print("QA_TOWER_SWIM info | drop | q=(12.00, 4.00, 12.00) lane")
	await _qa_float("lap_float", lap_drop, 1.92, true, 0.035)
	# East stair rails sit on the pool side of the flight. Rise under the
	# surface at the lane centre (clear of the ropes) and cross above them.
	await _qa_exit("lap_stair", Vector3(18.0, 0.45, 2.25), [
		Vector3(24.5, 0.0, 2.25),
		Vector3(28.45, 1.78, 2.25),
		Vector3(28.50, -0.95, 2.25),
		Vector3(28.50, 0.0, 3.4),
		Vector3(28.50, 0.0, 4.6),
	], 1.75, 26000)
	await _qa_exit("lap_ladder_e", Vector3(18.0, 0.45, 19.5), [
		Vector3(24.0, 0.0, 19.5),
		Vector3(26.74, 0.0, 19.5),
	], 1.75, 16000)
	var dive_drop := _qa_open_drop(16.5, 24.0, 24.0, 32.0, 4.0, 1.0)
	await _qa_float("dive_float", dive_drop, 1.92, true, -2.465)
	await _qa_exit("dive_stair", Vector3(20.0, 0.45, 28.15), [
		Vector3(24.2, 1.60, 28.15),
		Vector3(27.25, 1.60, 28.15),
		Vector3(27.25, -0.75, 28.15),
		Vector3(27.25, 0.0, 26.3),
		Vector3(27.25, 0.0, 25.2),
		Vector3(29.4, 0.0, 25.2),
	], 1.75, 28000)
	await _qa_float("river_float", Vector3(12.0, 2.5, 48.5), 0.85, false, 0.035)
	# S-island stair. The south footbridge blocks x 18..20, so the west
	# channel uses the island entry instead of the outer bank.
	await _qa_exit("river_exit", Vector3(12.0, 0.05, 47.7), [
		Vector3(16.3, 0.0, 47.7),
		Vector3(16.3, 0.0, 48.6),
		Vector3(16.3, 0.0, 50.6),
	], 0.72, 20000)
	await _qa_float("runout_float", Vector3(14.0, 2.4, 67.0), 0.92, false, 0.035)
	await _qa_exit("runout_exit", Vector3(14.0, 0.05, 67.0), [
		Vector3(8.0, 0.0, 67.2),
		Vector3(5.75, 0.0, 69.15),
		Vector3(5.75, 0.0, 71.45),
	], 0.72, 18000)
	await _qa_board()
	_qa_splash()
	ppa._qa_ring_release()
	ppa._qa_key(KEY_SPACE, false)
	print("QA_TOWER_SWIM DONE failures=%d" % _failures)
	get_tree().quit(0 if _failures == 0 else 1)


func _qa_float(nm: String, drop: Vector3, surface: float, deep: bool, floor_q: float) -> void:
	_qa_place(drop, Vector3(drop.x + 1.0, drop.y, drop.z))
	await get_tree().physics_frame
	ppa._player_body.velocity = Vector3.ZERO
	var t0 := Time.get_ticks_msec()
	var min_y := drop.y
	var last := drop
	var ok := false
	var held := 0
	while Time.get_ticks_msec() - t0 < 7000:
		await get_tree().physics_frame
		var q: Vector3 = ppa._tower_inv * ppa._player_body.global_position
		min_y = minf(min_y, q.y)
		last = q
		if deep:
			if absf(q.y - (surface - 1.52)) < 0.28:
				held += 1
				if held > 25:
					ok = true
					break
			else:
				held = 0
		else:
			var head := q.y + 1.62
			if ppa._player_body.is_on_floor() and head > surface and q.y > floor_q - 0.35:
				ok = true
				break
	if deep and min_y < (surface - 1.52) - 1.0:
		ok = false
	if not ok:
		_stuck = _qa_stuck()
	_qa_report(nm, ok, "q=(%.2f, %.2f, %.2f) min_y=%.2f floor=%s t=%d" % [
		last.x, last.y, last.z, min_y, str(ppa._player_body.is_on_floor()), Time.get_ticks_msec() - t0])


func _qa_exit(nm: String, start: Vector3, goals: Array, deck_y: float, budget_ms: int) -> void:
	_qa_place(start, goals[0])
	await get_tree().physics_frame
	ppa._player_body.velocity = Vector3.ZERO
	var reached := await _qa_go(goals, deck_y, budget_ms)
	var q: Vector3 = ppa._tower_inv * ppa._player_body.global_position
	var out := q.y >= deck_y - 0.02 and not _qa_wet(q)
	if not (reached and out) and _stuck == "":
		_stuck = _qa_stuck()
	_qa_report(nm, reached and out, "q=(%.2f, %.2f, %.2f) wet=%s on_floor=%s" % [
		q.x, q.y, q.z, str(_qa_wet(q)), str(ppa._player_body.is_on_floor())])


func _qa_go(goals: Array, deck_y: float, budget_ms: int) -> bool:
	var t0 := Time.get_ticks_msec()
	var stall_at := t0
	var stall_xz := Vector2(9999.0, 9999.0)
	for g: Vector3 in goals:
		# A negative goal y waits until the body has dropped to -y (onto a tread
		# after clearing a side rail). It does not hold swim-up.
		var rise := g.y
		var descend := rise < -0.01
		var need_y := -rise if descend else rise
		while Time.get_ticks_msec() - t0 < budget_ms:
			var q: Vector3 = ppa._tower_inv * ppa._player_body.global_position
			var dx := g.x - q.x
			var dz := g.z - q.z
			var close := dx * dx + dz * dz < 0.72 * 0.72
			var y_ok := (q.y <= need_y) if descend else (need_y <= 0.05 or q.y >= need_y)
			if close and y_ok:
				break
			var hold_up := not descend and need_y > 0.05 and q.y < need_y
			var walk := not (descend and close)
			if walk:
				_qa_steer(g.x, g.z, q.y)
			ppa._qa_key(KEY_SPACE, hold_up)
			ppa._qa_key(KEY_W, walk)
			await get_tree().physics_frame
			var q2: Vector3 = ppa._tower_inv * ppa._player_body.global_position
			var xz := Vector2(q2.x, q2.z)
			if xz.distance_to(stall_xz) > 0.10:
				stall_xz = xz
				stall_at = Time.get_ticks_msec()
			elif walk and not hold_up and ppa._player_body.is_on_floor() and Time.get_ticks_msec() - stall_at > 1100:
				ppa._qa_key(KEY_SPACE, true)
				await ppa._qa_frames(4)
				ppa._qa_key(KEY_SPACE, false)
				stall_at = Time.get_ticks_msec()
		if Time.get_ticks_msec() - t0 >= budget_ms:
			break
	var last: Vector3 = goals[goals.size() - 1]
	while Time.get_ticks_msec() - t0 < budget_ms:
		var q3: Vector3 = ppa._tower_inv * ppa._player_body.global_position
		if q3.y >= deck_y and not _qa_wet(q3):
			ppa._qa_key(KEY_W, false)
			ppa._qa_key(KEY_SPACE, false)
			return true
		_qa_steer(last.x, last.z, q3.y)
		ppa._qa_key(KEY_SPACE, false)
		ppa._qa_key(KEY_W, true)
		await get_tree().physics_frame
	_stuck = _qa_stuck()
	ppa._qa_key(KEY_W, false)
	ppa._qa_key(KEY_SPACE, false)
	return false


func _qa_board() -> void:
	# Platform is wide (Z +/- 0.5). The blade runs +X over the well.
	_qa_place(Vector3(13.2, 4.95, 25.0), Vector3(17.0, 4.9, 25.0))
	await ppa._qa_frames(20)
	var q0: Vector3 = ppa._tower_inv * ppa._player_body.global_position
	var min_y := q0.y
	var entered := false
	var t0 := Time.get_ticks_msec()
	var settled := 0
	ppa._qa_key(KEY_W, true)
	while Time.get_ticks_msec() - t0 < 8000:
		var q: Vector3 = ppa._tower_inv * ppa._player_body.global_position
		min_y = minf(min_y, q.y)
		_qa_steer(17.6, 25.0, q.y)
		var hop := q.x > 15.2 and q.y > 3.2
		ppa._qa_key(KEY_SPACE, hop)
		ppa._qa_key(KEY_W, true)
		await get_tree().physics_frame
		q = ppa._tower_inv * ppa._player_body.global_position
		min_y = minf(min_y, q.y)
		if q.x > 15.2 and q.x < 27.8 and q.z > 22.3 and q.z < 33.6 and q.y < 1.7:
			entered = true
		if entered and absf(q.y - 0.40) < 0.30:
			settled += 1
			if settled > 20:
				break
		else:
			settled = 0
	ppa._qa_key(KEY_W, false)
	ppa._qa_key(KEY_SPACE, false)
	var qe: Vector3 = ppa._tower_inv * ppa._player_body.global_position
	var soft := min_y > -0.5
	_qa_report("board_water", entered and soft, "q=(%.2f, %.2f, %.2f) min_y=%.2f entered=%s" % [
		qe.x, qe.y, qe.z, min_y, str(entered)])
	if not entered:
		return
	await _qa_exit("board_exit", Vector3(qe.x, qe.y, qe.z), [
		Vector3(24.2, 1.60, 28.15),
		Vector3(27.25, 1.60, 28.15),
		Vector3(27.25, -0.75, 28.15),
		Vector3(27.25, 0.0, 26.3),
		Vector3(27.25, 0.0, 25.2),
		Vector3(29.4, 0.0, 25.2),
	], 1.75, 28000)


func _qa_splash() -> void:
	var top: float = float(ppa._tt_pool.splash_top)
	var ray: float = float(ppa._tt_pool.splash_ray)
	var infill: bool = bool(ppa._tt_pool.splash_infill)
	var raised := top >= 0.90 or ray >= 0.90 or infill
	_qa_report("splash_deck", raised, "mesh=%.3f ray=%.3f infill=%s" % [top, ray, str(infill)])


func _qa_place(q: Vector3, look: Vector3) -> void:
	ppa._qa_key(KEY_W, false)
	ppa._qa_key(KEY_SPACE, false)
	var feet := Vector3(q.x, q.y - 0.08, q.z)
	ppa._qa_tower_place(ppa._tower_xf * feet, ppa._tower_up, ppa._tower_xf * look)
	ppa._player_body.velocity = Vector3.ZERO
	ppa._jump_buffer_t = -1.0
	ppa._coyote_t = -1.0


func _qa_steer(x: float, z: float, y: float) -> void:
	var want: Vector3 = ppa._tower_xf * Vector3(x, y, z)
	ppa._qa_ring_steer(want - ppa._player_body.global_position)


func _qa_wet(q: Vector3) -> bool:
	var hit: Dictionary = ppa._tt_pool.sample(ppa._tower_xf * q, false, null)
	return bool(hit.get("in_water", false))


func _qa_report(nm: String, ok: bool, detail: String) -> void:
	var extra := ""
	if not ok and _stuck != "":
		extra = " | " + _stuck
	print("QA_TOWER_SWIM %s | %s | %s%s" % ["PASS" if ok else "FAIL", nm, detail, extra])
	_stuck = ""
	if not ok:
		_failures += 1


func _qa_probe_lid() -> void:
	_qa_ray_grid("lap_ray", 4.0, 24.0, 4.0, 18.0, 4.0)
	_qa_ray_one("lap_ray", 14.0, 11.0, 4.0)
	_qa_ray_grid("dive_ray", 16.5, 24.0, 24.0, 32.0, 4.0)


func _qa_open_drop(x0: float, x1: float, z0: float, z1: float, from_y: float, fallback_y: float) -> Vector3:
	var best_y := 999.0
	var best := Vector3((x0 + x1) * 0.5, fallback_y, (z0 + z1) * 0.5)
	var x := x0
	while x <= x1 + 0.01:
		var z := z0
		while z <= z1 + 0.01:
			var hit := _qa_down(x, from_y, z, -4.0)
			var y := 800.0
			if hit.is_empty():
				y = -800.0
			else:
				y = (ppa._tower_inv * (hit["position"] as Vector3)).y
			if y < best_y:
				best_y = y
				best = Vector3(x, from_y, z)
			z += 4.0
		x += 4.0
	if best_y >= 0.50:
		best = Vector3(best.x, fallback_y, best.z)
	print("QA_TOWER_SWIM info | drop | q=(%.2f, %.2f, %.2f) hit_y=%.3f" % [best.x, best.y, best.z, best_y])
	return best


func _qa_ray_grid(label: String, x0: float, x1: float, z0: float, z1: float, from_y: float) -> void:
	var x := x0
	while x <= x1 + 0.01:
		var z := z0
		while z <= z1 + 0.01:
			_qa_ray_one(label, x, z, from_y)
			z += 4.0
		x += 4.0


func _qa_ray_one(label: String, x: float, z: float, from_y: float) -> void:
	var hit := _qa_down(x, from_y, z, -4.0)
	if hit.is_empty():
		print("QA_TOWER_SWIM info | %s | %.2f,%.2f,none,miss" % [label, x, z])
		return
	var p: Vector3 = ppa._tower_inv * (hit["position"] as Vector3)
	print("QA_TOWER_SWIM info | %s | %.2f,%.2f,%.3f,%s" % [label, x, z, p.y, _qa_hit_name(hit)])


func _qa_down(x: float, y0: float, z: float, y1: float) -> Dictionary:
	var xf: Transform3D = ppa._tower.global_transform
	var rq := PhysicsRayQueryParameters3D.create(xf * Vector3(x, y0, z), xf * Vector3(x, y1, z), 1)
	if ppa._player_body != null:
		rq.exclude = [ppa._player_body.get_rid()]
	return ppa.get_world_3d().direct_space_state.intersect_ray(rq)


func _qa_hit_name(hit: Dictionary) -> String:
	return _qa_col_name(hit.get("collider"), int(hit.get("shape", -1)))


func _qa_col_name(col: Object, shape_i: int) -> String:
	if col == null or not (col is Node):
		return "?"
	var n := col as Node
	var nm := str(n.name)
	if n.get_parent() != null:
		nm = str(n.get_parent().name) + "/" + nm
	if col is CollisionObject3D and shape_i >= 0:
		var owner_id := (col as CollisionObject3D).shape_find_owner(shape_i)
		if owner_id >= 0:
			var own: Object = (col as CollisionObject3D).shape_owner_get_owner(owner_id)
			if own is Node:
				nm += "/" + str((own as Node).name)
	return nm


func _qa_stuck() -> String:
	var b: CharacterBody3D = ppa._player_body
	var q: Vector3 = ppa._tower_inv * b.global_position
	var blk := "slide="
	for sc_i: int in range(b.get_slide_collision_count()):
		var kc: KinematicCollision3D = b.get_slide_collision(sc_i)
		var n: Vector3 = ppa._tower_xf.basis.inverse() * kc.get_normal()
		blk += "%s n=%s; " % [_qa_col_name(kc.get_collider(), kc.get_collider_shape_index()), str(n.snapped(Vector3(0.01, 0.01, 0.01)))]
	var down := _qa_down(q.x, q.y + 0.2, q.z, q.y - 3.0)
	if down.is_empty():
		blk += "down=miss"
	else:
		var py: float = (ppa._tower_inv * (down["position"] as Vector3)).y
		blk += "down=%s@%.2f" % [_qa_hit_name(down), py]
	var fwd := -b.global_transform.basis.z
	var up := b.up_direction
	fwd -= up * fwd.dot(up)
	if fwd.length() > 0.01:
		fwd = fwd.normalized()
		var heights := PackedFloat32Array([0.25, 0.7, 1.3])
		for h_v: float in heights:
			var from: Vector3 = b.global_position + up * h_v
			var rq := PhysicsRayQueryParameters3D.create(from, from + fwd * 1.4, 1)
			rq.exclude = [b.get_rid()]
			var hit: Dictionary = ppa.get_world_3d().direct_space_state.intersect_ray(rq)
			if hit.has("position"):
				blk += " h%.2f:%s@%.2f" % [h_v, _qa_hit_name(hit), from.distance_to(hit["position"])]
	return blk
