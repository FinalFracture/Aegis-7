extends Node
## --qa-tower-collide. Real PlayerBody walks that must stop at walls, glass,
## lift doors and guard rails. Prints QA_TOWER_COLLIDE DONE failures=N.

const _FB := preload("res://scripts/tennis_tower_fixes/tt_collider_fallback.gd")
const GUARD_JSON := "res://scripts/tennis_tower_fixes/tt_guard_rails.json"

var ppa: PrefacePlayableArea
var _failures: int = 0


func _ready() -> void:
	_run.call_deferred()


func _run() -> void:
	var guard: int = 0
	while (ppa == null or not ppa.has_meta("exterior_spawned")) and guard < 4000:
		await get_tree().physics_frame
		guard += 1
	if ppa == null or ppa._player_body == null or ppa._tower == null:
		print("QA_TOWER_COLLIDE FAIL | setup | player or tower missing")
		print("QA_TOWER_COLLIDE DONE failures=1")
		get_tree().quit(1)
		return
	await _wall("lift_981_side", Vector3(63.5, 0.05, 13.0), Vector3(68.5, 0.0, 13.0), 220, "x", 66.9, true)
	await _wall("lift_982_F2_in", Vector3(68.5, 6.15, 18.0), Vector3(68.5, 6.1, 12.8), 280, "z", 14.2, false)
	await _wall("lift_983_F3_in", Vector3(68.5, 12.25, 18.0), Vector3(68.5, 12.2, 12.8), 280, "z", 14.2, false)
	await _wall("stair_b963_westwall", Vector3(55.0, 0.05, 6.0), Vector3(60.5, 0.0, 6.0), 220, "x", 58.6, true)
	await _wall("stair_a955_wall", Vector3(73.5, 0.05, 6.5), Vector3(73.5, 0.0, 13.5), 220, "z", 10.2, true)
	await _wall("court_pane_x61.5", Vector3(61.5, 0.05, 24.5), Vector3(61.5, 0.0, 30.5), 220, "z", 28.0, true)
	await _wall("court_pane_z33", Vector3(71.5, 0.05, 33.0), Vector3(77.5, 0.0, 33.0), 220, "x", 74.9, true)
	await _wall("restroom_1010", Vector3(37.0, 0.05, 66.0), Vector3(37.0, 0.0, 70.0), 220, "z", 69.3, true)
	# z=49 is the aisle between pods 1253 (z=47.4) and 1254 (z=50.8). Same feature,
	# retargeted onto pod 1254's centreline (placement 132.4, 0, 50.8).
	await _wall("vr_pod", Vector3(128.5, 0.05, 50.8), Vector3(136.0, 0.0, 50.8), 280, "x", 133.5, true)
	await _wall("court_pane_x58.5", Vector3(58.5, 0.05, 24.5), Vector3(58.5, 0.0, 30.5), 220, "z", 28.5, true)
	await _wall("restroom_1008_wetwall", Vector3(100.0, 0.05, 4.0), Vector3(107.0, 0.0, 4.0), 220, "x", 104.0, true)
	await _wall("rink_board", Vector3(72.0, 6.15, 22.0), Vector3(72.0, 6.1, 30.0), 220, "z", 26.0, true)
	print("[TT] floor_max_angle_deg=%.2f" % rad_to_deg(ppa._player_body.floor_max_angle))
	await _turn_check()
	await _guards()
	await _courts()
	await _pairs()
	await _rink_gate()
	await _slide_climb()
	if ppa._tower != null:
		_FB.leak_stats(ppa._tower)
	print("QA_TOWER_COLLIDE DONE failures=%d" % _failures)
	get_tree().quit(0 if _failures == 0 else 1)


func _wall(label: String, a: Vector3, b: Vector3, frames: int, axis: String, limit: float, less_is_blocked: bool) -> void:
	var r: Dictionary = await _go(label, a, b, frames)
	var q: Vector3 = r["q"]
	var coord: float = q.x if axis == "x" else q.z
	var held: bool = coord < limit if less_is_blocked else coord > limit
	var y_ok: bool = q.y > float(a.y) - 1.2
	if label.begins_with("lift_982"):
		y_ok = q.y > 5.5
	elif label.begins_with("lift_983"):
		y_ok = q.y > 11.5
	elif label == "rink_board":
		y_ok = q.y > 5.4
	var ok: bool = (not bool(r["arrived"])) and held and y_ok
	_line(label, ok, "arrived=%s q=(%.2f,%.2f,%.2f) max_air=%d held=%s" % [str(r["arrived"]), q.x, q.y, q.z, int(r["max_air"]), str(held)])


func _guards() -> void:
	# Fixed repros. A pass means the player did not fall, whether Rook's guard
	# or ours is what stopped them. A spawn that never moves is a bad point.
	await _nofall("guard_track_stairwell", Vector3(61.0, 12.30, 12.4), Vector3(61.0, 12.2, 8.0), 11.6, 220)
	await _nofall("guard_gallery_edge", Vector3(-9.0, 6.25, 66.2), Vector3(-9.0, 6.1, 71.5), 5.6, 200)
	# +6.1 is the tower N2 landing (world x 20.2..22.4). +7.0 is the deck
	# (west edge x 22.47). z=56.5 is the notch between the two towers.
	await _nofall("guard_f2_brg_bridge", Vector3(21.3, 6.18, 55.25), Vector3(19.5, 6.1, 55.25), 5.5, 200)
	await _nofall("guard_f2_brg_deck7", Vector3(23.3, 7.08, 53.5), Vector3(21.2, 7.0, 53.5), 6.4, 200)
	await _nofall("guard_slab_f2_arc", Vector3(130.2, 6.25, 66.6), Vector3(130.2, 6.1, 74.0), 5.5, 240)
	await _nofall("guard_slab_f3_play", Vector3(130.2, 12.35, 66.6), Vector3(130.2, 12.2, 74.0), 11.6, 240)
	# Rook infilled X 57..58. Crossing that slab without falling is the pass.
	await _nofall("guard_slab_b977", Vector3(55.2, 6.25, 6.0), Vector3(57.6, 6.1, 6.0), 5.5, 220, true)


func _nofall(label: String, a: Vector3, b: Vector3, min_y: float, frames: int, allow_cross: bool = false) -> void:
	var r: Dictionary = await _go(label, a, b, frames)
	var q: Vector3 = r["q"]
	var moved: float = Vector2(q.x - a.x, q.z - a.z).length()
	var y_ok: bool = q.y > min_y
	var held: bool = allow_cross or not bool(r["arrived"])
	var ok: bool = held and y_ok and int(r["max_air"]) <= 24 and moved > 0.35
	_line(label, ok, "arrived=%s q=(%.2f,%.2f,%.2f) min_y=%.2f max_air=%d moved=%.2f" % [
		str(r["arrived"]), q.x, q.y, q.z, min_y, int(r["max_air"]), moved])


func _turn_check() -> void:
	# Faces +X, goal is +Z. The court aisle at (50, 40) dead-ends in glass.
	# West foyer run between bays 19.5 and 39.5 is open. Headless steer needs _qa_hand.
	var a: Vector3 = Vector3(-6.0, 0.08, 26.0)
	var b: Vector3 = Vector3(-6.0, 0.0, 34.0)
	var xf: Transform3D = ppa._tower_xf
	ppa._qa_tower_place(xf * a, ppa._tower_up, xf * Vector3(2.0, 0.0, 26.0))
	await ppa._qa_frames(12)
	var r: Dictionary = await ppa._qa_tower_walk_leg("turn_check", b, 240)
	var q: Vector3 = r["q"]
	var ok: bool = bool(r["arrived"]) and q.y > -0.4 and absf(q.x - a.x) < 1.6
	_line("turn_check", ok, "arrived=%s q=(%.2f,%.2f,%.2f) max_air=%d" % [str(r["arrived"]), q.x, q.y, q.z, int(r["max_air"])])


func _courts() -> void:
	var centres: Array[Vector3] = [
		Vector3(64.0, 0.0, 32.0), Vector3(64.0, 0.0, 47.0),
		Vector3(90.0, 0.0, 32.0), Vector3(90.0, 0.0, 47.0),
	]
	var doors: Array[Node3D] = []
	var stack: Array[Node] = [ppa._tower]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for ch: Node in n.get_children():
			stack.append(ch)
		if n is Node3D and String(n.name).begins_with("tt_court_partition_door_closed"):
			doors.append(n as Node3D)
	if doors.size() != 8:
		_line("court_doors", false, "found=%d" % doors.size())
		return
	doors.sort_custom(func(a: Node3D, b: Node3D) -> bool: return String(a.name) < String(b.name))
	for door: Node3D in doors:
		var opening_w: Vector3 = door.global_transform * Vector3(0.47, 0.08, 0.0)
		var opening_q: Vector3 = ppa._tower_inv * opening_w
		var centre: Vector3 = centres[0]
		var best: float = INF
		for c: Vector3 in centres:
			var d: float = Vector2(c.x - opening_q.x, c.z - opening_q.z).length()
			if d < best:
				best = d
				centre = c
		# Stay on the opening centreline. A diagonal into the court centre clips
		# Leaf_R after the ±0.50 slide (clear gap is about x -0.03..0.97).
		var centre_local: Vector3 = door.global_transform.affine_inverse() * (ppa._tower_xf * centre)
		var z_sign: float = 1.0 if centre_local.z >= 0.0 else -1.0
		var out_q: Vector3 = ppa._tower_inv * (door.global_transform * Vector3(0.47, 0.08, -z_sign * 2.8))
		var in_q: Vector3 = ppa._tower_inv * (door.global_transform * Vector3(0.47, 0.08, z_sign * 2.0))
		out_q.y = 0.08
		in_q.y = 0.05
		var label: String = "court_in_%s" % String(door.name).trim_prefix("tt_court_partition_door_closed_")
		var r: Dictionary = await _go(label, out_q, in_q, 320)
		var q: Vector3 = r["q"]
		var entered: bool = bool(r["arrived"]) and q.y > -0.4
		_line(label, entered, "arrived=%s q=(%.2f,%.2f,%.2f) max_air=%d" % [str(r["arrived"]), q.x, q.y, q.z, int(r["max_air"])])
		if not entered:
			continue
		var back: Dictionary = await _go(label + "_out", q, out_q, 280)
		var qb: Vector3 = back["q"]
		var left: bool = bool(back["arrived"]) and qb.y > -0.4
		_line(label + "_out", left, "arrived=%s q=(%.2f,%.2f,%.2f) max_air=%d" % [str(back["arrived"]), qb.x, qb.y, qb.z, int(back["max_air"])])


func _one_guard(reason: String, segs: Array) -> void:
	var best: Dictionary = {}
	var best_l: float = -1.0
	for s_v in segs:
		var s: Dictionary = s_v
		if String(s.get("reason", "")) != reason:
			continue
		var l: float = Vector2(float(s["x1"]) - float(s["x0"]), float(s["z1"]) - float(s["z0"])).length()
		if l > best_l:
			best_l = l
			best = s
	if best.is_empty():
		_line("guard_" + reason, false, "no segment")
		return
	var y: float = float(best["y"])
	var mid: Vector3 = Vector3((float(best["x0"]) + float(best["x1"])) * 0.5, y, (float(best["z0"]) + float(best["z1"])) * 0.5)
	var nrm: Vector3 = Vector3(float(best["nx"]), 0.0, float(best["nz"]))
	if nrm.length_squared() < 0.01:
		nrm = Vector3.RIGHT
	nrm = nrm.normalized()
	var start: Vector3 = mid + nrm * 0.9
	start.y = y + 0.1
	var goal: Vector3 = mid - nrm * 1.4
	goal.y = y
	var r: Dictionary = await _go("guard_" + reason, start, goal, 200)
	var q: Vector3 = r["q"]
	var ok: bool = (not bool(r["arrived"])) and q.y > y - 0.45 and int(r["max_air"]) <= 20
	_line("guard_" + reason, ok, "arrived=%s q=(%.2f,%.2f,%.2f) floor_y=%.2f max_air=%d len=%.1f id=%s" % [
		str(r["arrived"]), q.x, q.y, q.z, y, int(r["max_air"]), best_l, String(best.get("id", ""))])


func _pairs() -> void:
	var doors: Array[Node3D] = _named("tt_door_pair_18")
	if doors.size() != 4:
		_line("pair_doors", false, "found=%d" % doors.size())
		return
	doors.sort_custom(func(a: Node3D, b: Node3D) -> bool: return String(a.name) < String(b.name))
	for door: Node3D in doors:
		var y: float = (ppa._tower_inv * door.global_position).y
		# ±1.15 clears the swung leaves (~0.9 m) and stays short of the stair-core
		# wall just past the F1/F2 Z64 pair (the body stopped at about +1.29 m).
		var neg_w: Vector3 = door.global_transform * Vector3(0.0, 0.12, -1.15)
		var pos_w: Vector3 = door.global_transform * Vector3(0.0, 0.12, 1.15)
		var neg_q: Vector3 = ppa._tower_inv * neg_w
		var pos_q: Vector3 = ppa._tower_inv * pos_w
		neg_q.y = y + 0.1
		pos_q.y = y + 0.1
		var label: String = "pair_%s" % String(door.name).trim_prefix("tt_door_pair_18_")
		var go: Dictionary = await _go(label + "_pz", neg_q, pos_q, 280)
		var q: Vector3 = go["q"]
		var ok: bool = bool(go["arrived"]) and q.y > y - 0.5
		_line(label + "_pz", ok, "arrived=%s q=(%.2f,%.2f,%.2f) max_air=%d" % [str(go["arrived"]), q.x, q.y, q.z, int(go["max_air"])])
		if not ok:
			continue
		var back: Dictionary = await _go(label + "_nz", q, neg_q, 280)
		var qb: Vector3 = back["q"]
		var back_ok: bool = bool(back["arrived"]) and qb.y > y - 0.5
		_line(label + "_nz", back_ok, "arrived=%s q=(%.2f,%.2f,%.2f) max_air=%d" % [str(back["arrived"]), qb.x, qb.y, qb.z, int(back["max_air"])])


func _rink_gate() -> void:
	var doors: Array[Node3D] = _named("tt_rink_board_gate_open")
	if doors.is_empty():
		_line("rink_gate", false, "found=0")
		return
	var door: Node3D = doors[0]
	var y: float = (ppa._tower_inv * door.global_position).y
	var a_q: Vector3 = ppa._tower_inv * (door.global_transform * Vector3(0.0, 0.2, -1.7))
	var b_q: Vector3 = ppa._tower_inv * (door.global_transform * Vector3(0.0, 0.2, 1.7))
	a_q.y = y + 0.12
	b_q.y = y + 0.08
	var r: Dictionary = await _go("rink_gate", a_q, b_q, 260)
	var q: Vector3 = r["q"]
	var ok: bool = bool(r["arrived"]) and q.y > y - 0.45
	_line("rink_gate", ok, "arrived=%s q=(%.2f,%.2f,%.2f) max_air=%d" % [str(r["arrived"]), q.x, q.y, q.z, int(r["max_air"])])


func _slide_climb() -> void:
	var tubes: Array[Node3D] = _named("tt_leisure_slide_tubes")
	if tubes.is_empty():
		_line("slide_climb", false, "found=0")
		return
	var space: PhysicsDirectSpaceState3D = ppa._player_body.get_world_3d().direct_space_state
	var low_y: float = INF
	var high_y: float = -INF
	var low_q: Vector3 = Vector3.ZERO
	var high_q: Vector3 = Vector3.ZERO
	var hits: int = 0
	for tube: Node3D in tubes:
		var origin: Vector3 = tube.global_position
		for ix: int in range(-5, 6):
			for iz: int in range(-5, 6):
				var from: Vector3 = origin + Vector3(float(ix) * 0.45, 7.0, float(iz) * 0.45)
				var to: Vector3 = origin + Vector3(float(ix) * 0.45, -1.5, float(iz) * 0.45)
				var rq: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(from, to, 1)
				rq.hit_back_faces = true
				var hit: Dictionary = space.intersect_ray(rq)
				if hit.is_empty() or not ppa._tt_is_slide_collider(hit.get("collider")):
					continue
				var qh: Vector3 = ppa._tower_inv * (hit["position"] as Vector3)
				hits += 1
				if qh.y < low_y:
					low_y = qh.y
					low_q = qh
				if qh.y > high_y:
					high_y = qh.y
					high_q = qh
	if hits < 4 or high_y < low_y + 0.8:
		_line("slide_climb", false, "hits=%d low=%.2f high=%.2f" % [hits, low_y, high_y])
		return
	var away: Vector3 = low_q - high_q
	away.y = 0.0
	if away.length_squared() < 0.04:
		away = Vector3(1.0, 0.0, 0.0)
	away = away.normalized()
	var start: Vector3 = low_q + away * 0.55
	start.y = low_y + 0.12
	var goal: Vector3 = high_q
	goal.y = high_y
	var r: Dictionary = await _go("slide_climb", start, goal, 280)
	var q: Vector3 = r["q"]
	var gained: float = q.y - start.y
	var ok: bool = (not bool(r["arrived"])) and gained < 0.40 and q.y > start.y - 2.0
	_line("slide_climb", ok, "arrived=%s q=(%.2f,%.2f,%.2f) gained=%.2f low=%.2f high=%.2f" % [
		str(r["arrived"]), q.x, q.y, q.z, gained, low_y, high_y])


func _named(prefix: String) -> Array[Node3D]:
	var out: Array[Node3D] = []
	var stack: Array[Node] = [ppa._tower]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for ch: Node in n.get_children():
			stack.append(ch)
		if n is Node3D and String(n.name).begins_with(prefix):
			out.append(n as Node3D)
	return out


func _go(label: String, a: Vector3, b: Vector3, frames: int) -> Dictionary:
	var xf: Transform3D = ppa._tower_xf
	ppa._qa_tower_place(xf * a, ppa._tower_up, xf * b)
	await ppa._qa_frames(18)
	return await ppa._qa_tower_walk_leg(label, b, frames)


func _line(label: String, ok: bool, detail: String) -> void:
	print("QA_TOWER_COLLIDE %s | %s | %s" % ["PASS" if ok else "FAIL", label, detail])
	if not ok:
		_failures += 1
