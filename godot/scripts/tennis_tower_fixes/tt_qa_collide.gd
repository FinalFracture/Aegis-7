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
	await _slide_link()
	await _courts()
	await _pairs()
	await _rink_gate()
	await _slide_climb()
	if ppa._tower != null:
		_FB.leak_stats(ppa._tower)
	_core_band()
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
	# (west edge x 22.47). The old mid-air start (22.5, 6.15, 56.5) is retired:
	# that notch between T1 and T2 has no floor. The link walk is _slide_link.
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
	var listed := ""
	for door0: Node3D in doors:
		var qd: Vector3 = ppa._tower_inv * door0.global_position
		listed += " %s=(%.2f,%.2f,%.2f)" % [String(door0.name), qd.x, qd.y, qd.z]
	print("QA_TOWER_COLLIDE info | pair_doors | n=%d%s" % [doors.size(), listed])
	if doors.size() != 5:
		_line("pair_doors", false, "found=%d" % doors.size())
		return
	doors.sort_custom(func(a: Node3D, b: Node3D) -> bool: return String(a.name) < String(b.name))
	for door: Node3D in doors:
		var y: float = (ppa._tower_inv * door.global_position).y
		# ±1.15 clears the swung leaves (~0.9 m). Pull in only when that stand
		# overlaps a wall (the F2 Z14.85 pocket is tight against ST+S2).
		var neg_z: float = _pair_stand(door, -1.0, y)
		var pos_z: float = _pair_stand(door, 1.0, y)
		var neg_w: Vector3 = door.global_transform * Vector3(0.0, 0.12, neg_z)
		var pos_w: Vector3 = door.global_transform * Vector3(0.0, 0.12, pos_z)
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


func _pair_stand(door: Node3D, sign: float, y: float) -> float:
	var z: float = sign * 1.15
	if not _pair_stand_hits(door, z, y):
		return z
	var z2: float = z
	while absf(z2) > 1.001:
		z2 -= sign * 0.1
		if not _pair_stand_hits(door, z2, y):
			print("QA_TOWER_COLLIDE info | pair_stand | %s z=%.2f" % [String(door.name), z2])
			return z2
	print("QA_TOWER_COLLIDE info | pair_stand | %s kept z=%.2f" % [String(door.name), z])
	return z


func _pair_stand_hits(door: Node3D, z_local: float, y: float) -> bool:
	var q: Vector3 = ppa._tower_inv * (door.global_transform * Vector3(0.0, 0.12, z_local))
	var cap := CapsuleShape3D.new()
	cap.radius = 0.35
	cap.height = 1.75
	var sq := PhysicsShapeQueryParameters3D.new()
	sq.shape = cap
	sq.collision_mask = 1 | (1 << 18)
	sq.margin = 0.0
	sq.exclude = [ppa._player_body.get_rid()]
	var centre := Vector3(q.x, y + 0.1 + 0.995, q.z)
	sq.transform = Transform3D(ppa._tower.global_transform.basis, ppa._tower.global_transform * centre)
	return not ppa._player_body.get_world_3d().direct_space_state.intersect_shape(sq, 1).is_empty()


## Link deck (24.15, 7.05, 56.5). Screens must stop a walk and a jump.
func _slide_link() -> void:
	var start := Vector3(24.15, 7.05, 56.5)
	await _link_blocked("slide_link_west", start, Vector3(18.0, 7.0, 56.5))
	await _link_blocked("slide_link_east", start, Vector3(27.0, 7.0, 56.5))
	await _qa_link_jump()
	var gate: Dictionary = await _go("slide_gate_threshold", Vector3(18.5, 6.1, 58.7), Vector3(21.0, 6.1, 58.7), 180)
	var qg: Vector3 = gate["q"]
	var gate_ok: bool = bool(gate["arrived"]) and qg.y > 5.85 and int(gate["max_air"]) <= 8
	_line("slide_gate_threshold", gate_ok, "arrived=%s q=(%.2f,%.2f,%.2f) max_air=%d" % [str(gate["arrived"]), qg.x, qg.y, qg.z, int(gate["max_air"])])


func _link_blocked(label: String, a: Vector3, b: Vector3) -> void:
	var r: Dictionary = await _go(label, a, b, 100)
	var q: Vector3 = r["q"]
	var moved: float = Vector2(q.x - a.x, q.z - a.z).length()
	var on_deck: bool = q.x > 23.50 and q.x < 24.90 and q.z > 55.85 and q.z < 57.20 and q.y > 6.4
	var ok: bool = (not bool(r["arrived"])) and on_deck and int(r["max_air"]) <= 2 and moved > 0.05
	_line(label, ok, "arrived=%s q=(%.2f,%.2f,%.2f) max_air=%d moved=%.2f" % [str(r["arrived"]), q.x, q.y, q.z, int(r["max_air"]), moved])


func _qa_link_jump() -> void:
	var start := Vector3(24.15, 7.05, 56.5)
	var goal := Vector3(23.2, 7.0, 56.5)
	await _go("slide_link_rail", start, goal, 100)
	var prev: int = Engine.max_physics_steps_per_frame
	Engine.max_physics_steps_per_frame = 1
	ppa._qa_key(KEY_W, true)
	await ppa._qa_idle(2)
	var y0: float = (ppa._tower_inv * ppa._player_body.global_position).y
	ppa._qa_key(KEY_SPACE, true)
	await ppa._qa_idle(1)
	ppa._qa_key(KEY_SPACE, false)
	var peak: float = y0
	var min_y: float = y0
	for _i: int in range(90):
		var qf: Vector3 = ppa._tower_inv * ppa._player_body.global_position
		peak = maxf(peak, qf.y)
		min_y = minf(min_y, qf.y)
		await ppa.get_tree().physics_frame
	ppa._qa_key(KEY_W, false)
	await ppa._qa_frames(12)
	Engine.max_physics_steps_per_frame = prev
	var q: Vector3 = ppa._tower_inv * ppa._player_body.global_position
	var on_link: bool = q.x > 23.55 and q.x < 24.85 and q.z > 55.85 and q.z < 57.15 and q.y > 6.4 and min_y > 6.4
	var jumped: bool = peak > y0 + 0.45
	_line("slide_link_jump", jumped and on_link, "peak=%.2f y0=%.2f min_y=%.2f q=(%.2f,%.2f,%.2f)" % [peak, y0, min_y, q.x, q.y, q.z])


## Read-only. Counts unguarded drops inside tower_plan cores. Does not fail the probe.
func _core_band() -> void:
	var cores: Array = [
		[30.0, 40.2, 15.0, 20.5], [102.8, 113.0, 15.0, 20.5], [30.0, 40.2, 58.5, 64.0], [102.8, 113.0, 58.5, 64.0],
		[71.0, 76.5, 9.5, 19.7], [71.0, 76.5, 59.3, 69.5], [24.5, 34.7, 39.0, 44.5], [108.3, 118.5, 39.0, 44.5],
		[57.0, 64.0, 2.6, 13.2], [86.0, 92.0, 2.6, 13.2], [58.0, 64.0, 65.8, 76.4], [86.0, 92.0, 65.8, 76.4],
		[119.5, 125.5, 50.0, 60.6], [-6.0, 0.0, 10.0, 20.6], [-6.0, 0.0, 58.4, 69.0],
		[134.0, 140.0, 10.0, 20.6], [134.0, 140.0, 58.4, 69.0],
	]
	var space: PhysicsDirectSpaceState3D = ppa._player_body.get_world_3d().direct_space_state
	var mask: int = 1 | (1 << 18)
	var tower: Node3D = ppa._tower
	var floors: Dictionary = {}
	var inside: Dictionary = {}
	for rect_v in cores:
		var rect: Array = rect_v
		var x: float = float(rect[0]) + 0.25
		while x <= float(rect[1]) - 0.25 + 0.001:
			var z: float = float(rect[2]) + 0.25
			while z <= float(rect[3]) - 0.25 + 0.001:
				var key := Vector2i(int(round((x - 0.25) / 0.5)), int(round((z - 0.25) / 0.5)))
				inside[key] = true
				var ys: Array = _core_floors(space, tower, x, z, mask)
				if not ys.is_empty():
					floors[key] = ys
				z += 0.5
			x += 0.5
	var edges: int = 0
	var band: int = 0
	var low_guard: int = 0
	var samples: PackedStringArray = PackedStringArray()
	var dirs: Array[Vector2i] = [Vector2i(1, 0), Vector2i(-1, 0), Vector2i(0, 1), Vector2i(0, -1)]
	var box := BoxShape3D.new()
	var bq := PhysicsShapeQueryParameters3D.new()
	bq.shape = box
	bq.collision_mask = mask
	bq.margin = 0.0
	bq.exclude = [ppa._player_body.get_rid()]
	var basis: Basis = tower.global_transform.basis
	for key_v in floors.keys():
		var key: Vector2i = key_v
		var x0: float = float(key.x) * 0.5 + 0.25
		var z0: float = float(key.y) * 0.5 + 0.25
		var ys0: Array = floors[key]
		for y_v in ys0:
			var y: float = float(y_v)
			for dv: Vector2i in dirs:
				var k2 := Vector2i(key.x + dv.x, key.y + dv.y)
				if not inside.has(k2):
					continue
				var close := false
				if floors.has(k2):
					for oy_v in floors[k2]:
						if absf(float(oy_v) - y) <= 0.36:
							close = true
							break
				if close:
					continue
				var nx: float = x0 + float(dv.x) * 0.5
				var nz: float = z0 + float(dv.y) * 0.5
				var hd: Dictionary = _core_ray(space, tower, Vector3(nx, y + 0.3, nz), Vector3(nx, y - 30.0, nz), mask)
				var drop: float = 30.0
				if hd.has("position"):
					drop = y - (tower.global_transform.affine_inverse() * (hd["position"] as Vector3)).y
				if drop < 0.5:
					continue
				box.size = Vector3(0.4 if dv.x != 0 else 0.3, 0.85, 0.3 if dv.x != 0 else 0.4)
				var mid := Vector3(x0 + float(dv.x) * 0.25, y + 0.575, z0 + float(dv.y) * 0.25)
				bq.transform = Transform3D(basis, tower.global_transform * mid)
				var guard_h: float = 0.0
				if not space.intersect_shape(bq, 1).is_empty():
					var hb: Dictionary = _core_ray(space, tower, Vector3(mid.x, y + 1.6, mid.z), Vector3(mid.x, y, mid.z), mask)
					guard_h = ((tower.global_transform.affine_inverse() * (hb["position"] as Vector3)).y - y) if hb.has("position") else 1.0
					if guard_h >= 1.0:
						continue
				edges += 1
				var in_band: bool = y >= 3.9 and y <= 4.8
				if in_band:
					band += 1
					if guard_h < 0.50:
						low_guard += 1
				if samples.size() < 6 and (in_band or samples.size() < 2):
					samples.append("(%.2f,%.2f,%.2f) drop=%.2f guard=%.2f" % [x0, z0, y, drop, guard_h])
	print("QA_TOWER_COLLIDE info | core_band | cells=%d floors=%d edges=%d band_edges=%d low_guard=%d" % [inside.size(), floors.size(), edges, band, low_guard])
	print("QA_TOWER_COLLIDE info | core_band | samples %s" % (" | ".join(samples) if samples.size() > 0 else "none"))


func _core_floors(space: PhysicsDirectSpaceState3D, tower: Node3D, x: float, z: float, mask: int) -> Array:
	var ys: Array = []
	var top := 18.0
	for _g: int in range(8):
		var hit: Dictionary = _core_ray(space, tower, Vector3(x, top, z), Vector3(x, -2.0, z), mask)
		if not hit.has("position"):
			break
		var hp: Vector3 = tower.global_transform.affine_inverse() * (hit["position"] as Vector3)
		if hp.y >= top - 0.01:
			break
		var nrm: Vector3 = (tower.global_transform.basis.inverse() * (hit["normal"] as Vector3)).normalized()
		if rad_to_deg(acos(clampf(nrm.dot(Vector3.UP), -1.0, 1.0))) < 50.0:
			ys.append(hp.y)
		top = hp.y - 0.05
	return ys


func _core_ray(space: PhysicsDirectSpaceState3D, tower: Node3D, a: Vector3, b: Vector3, mask: int) -> Dictionary:
	var rq: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(tower.global_transform * a, tower.global_transform * b, mask)
	rq.hit_back_faces = true
	rq.exclude = [ppa._player_body.get_rid()]
	return space.intersect_ray(rq)


func _go(label: String, a: Vector3, b: Vector3, frames: int) -> Dictionary:
	var xf: Transform3D = ppa._tower_xf
	ppa._qa_tower_place(xf * a, ppa._tower_up, xf * b)
	await ppa._qa_frames(18)
	return await ppa._qa_tower_walk_leg(label, b, frames)


func _line(label: String, ok: bool, detail: String) -> void:
	print("QA_TOWER_COLLIDE %s | %s | %s" % ["PASS" if ok else "FAIL", label, detail])
	if not ok:
		_failures += 1
