extends Node
## --qa-tower-entry. Real PlayerBody, every entrance from the drum floor.
## ENTERED only when the body ends on F1 inside the building footprint
## (X -12..140, Z 0..79, q.y ~ 0). Walk, then the same routes sprinting.
## Stair failures stay in the count and are also printed as KNOWN-ROOK TTQA-052.

const L2 := -1.118
const ARRIVE := 0.8

var ppa: PrefacePlayableArea
var _failures: int = 0


func _ready() -> void:
	_run.call_deferred()


func _drum_y(z: float) -> float:
	return 195.9592 - sqrt(maxf(0.0, 40000.0 - (z - 40.0) * (z - 40.0)))


func _run() -> void:
	var guard := 0
	while (ppa == null or not ppa.has_meta("exterior_spawned")) and guard < 4000:
		await get_tree().physics_frame
		guard += 1
	if ppa == null or ppa._player_body == null or ppa._tower == null:
		print("QA_TOWER_ENTRY FAIL | setup | player=%s tower=%s" % [str(ppa != null and ppa._player_body != null), str(ppa != null and ppa._tower != null)])
		print("QA_TOWER_ENTRY DONE failures=1")
		get_tree().quit(1)
		return
	var routes := _routes()
	for sprint in [false, true]:
		var mode := "sprint" if sprint else "walk"
		for spec in routes:
			await _qa_one(spec, sprint, mode)
	ppa._qa_ring_release()
	print("QA_TOWER_ENTRY DONE failures=%d" % _failures)
	get_tree().quit(0 if _failures == 0 else 1)


func _routes() -> Array:
	var lf := _drum_y(8.3) + 0.003
	var xe := -41.92 + (L2 - lf) * 12.0
	var xf := xe + 1.5
	var lfil := maxf((lf - _drum_y(9.05) - 0.003) * 20.0, 0.2)
	var approach := xf + lfil + 2.4
	# Lane B centre is Z 9.35. The median's west end is X -41.9, so a 0.35 m
	# capsule crossing there must be near X -42.65 (turn landing is -43.42..-41.9).
	# Points sit back on that line so the cross-fall does not walk the body into the wall.
	var sw_ramp: Array = [
		Vector2(xf - 0.4, 9.05),
		Vector2(-39.5, 9.05),
		Vector2(-42.65, 9.05),
		Vector2(-42.65, 10.3),
		Vector2(-42.65, 11.40),
		Vector2(-38.5, 11.40),
		Vector2(-34.8, 11.40),
		Vector2(-31.0, 11.40),
		Vector2(-27.4, 11.40),
		Vector2(-26.0, 11.40),
		Vector2(-26.0, 13.4),
		Vector2(-26.0, 16.0),
		Vector2(-20.0, 19.005),
		Vector2(-14.0, 19.005),
		Vector2(-8.0, 19.005),
	]
	var nw: Array = []
	var er: Array = []
	for p_v in sw_ramp:
		var p: Vector2 = p_v
		if p.y < 17.0:
			nw.append(Vector2(p.x, 80.0 - p.y))
			er.append(Vector2(128.0 - p.x, p.y))
	nw.append(Vector2(-20.0, 60.045))
	nw.append(Vector2(-14.0, 60.045))
	nw.append(Vector2(-8.0, 60.045))
	er.append(Vector2(154.0, 22.0))
	er.append(Vector2(154.0, 30.0))
	er.append(Vector2(148.0, 36.415))
	er.append(Vector2(140.0, 36.415))
	er.append(Vector2(134.0, 36.415))
	return [
		{"name": "SW_ramp", "stair": false, "start": Vector2(approach, 9.05), "goals": sw_ramp},
		{"name": "NW_ramp", "stair": false, "start": Vector2(approach, 70.95), "goals": nw},
		{"name": "W_stair", "stair": true, "start": Vector2(-76.2, 38.0), "goals": [
			Vector2(-70.5, 38.0), Vector2(-64.2, 38.0), Vector2(-59.5, 38.4),
			Vector2(-30.0, 39.005), Vector2(-16.0, 39.005), Vector2(-6.0, 39.005)]},
		{"name": "E_ramp", "stair": false, "start": Vector2(128.0 - approach, 9.05), "goals": er},
		{"name": "E_stair", "stair": true, "start": Vector2(184.0, 38.0), "goals": [
			Vector2(176.0, 38.0), Vector2(168.5, 38.0), Vector2(155.0, 38.2),
			Vector2(146.0, 38.585), Vector2(134.0, 38.585)]},
		{"name": "S_door", "stair": false, "start": Vector2(70.915, -14.0), "goals": [
			Vector2(70.915, -3.0), Vector2(70.915, 1.6), Vector2(70.915, 8.0)]},
		{"name": "N_door", "stair": false, "start": Vector2(70.915, 93.0), "goals": [
			Vector2(70.915, 82.5), Vector2(70.915, 77.2), Vector2(70.915, 70.0)]},
	]


func _qa_one(spec: Dictionary, sprint: bool, mode: String) -> void:
	var name := String(spec["name"])
	var start: Vector2 = spec["start"]
	var goals: Array = spec["goals"]
	await _place_drum(start, goals[0])
	var q0: Vector3 = ppa._tower_inv * ppa._player_body.global_position
	var outside := not _inside_f1(q0)
	if sprint:
		ppa._qa_key(KEY_SHIFT, true)
		await ppa._qa_idle(2)
	var frames := 0
	var samples: Array[Vector3] = []
	var min_y := q0.y
	var max_y := q0.y
	var path_m := 0.0
	var prev := Vector2(q0.x, q0.z)
	var widths: Array[float] = []
	var stuck := ""
	var entered := false
	for gi in range(goals.size()):
		var goal: Vector2 = goals[gi]
		await ppa._qa_tower_face(Vector3(goal.x, 0.0, goal.y))
		var leg: Dictionary = await _qa_leg(goal, 900)
		frames += int(leg["frames"])
		var chunk: Array = leg["samples"]
		for s_v in chunk:
			var s: Vector3 = s_v
			samples.append(s)
			min_y = minf(min_y, s.y)
			max_y = maxf(max_y, s.y)
			var step := Vector2(s.x, s.z).distance_to(prev)
			if step < 2.0:
				path_m += step
			prev = Vector2(s.x, s.z)
		if float(leg.get("width", -1.0)) > 0.2:
			widths.append(float(leg["width"]))
		if bool(leg["inside"]):
			entered = true
			break
		if not bool(leg["arrived"]):
			stuck = String(leg["blocker"])
			break
	ppa._qa_key(KEY_W, false)
	if sprint:
		ppa._qa_key(KEY_SHIFT, false)
	await ppa._qa_frames(20)
	var q: Vector3 = ppa._tower_inv * ppa._player_body.global_position
	if _inside_f1(q):
		entered = true
	var climb := maxf(max_y - min_y, 0.001)
	var grade := path_m / climb
	var width := _min_pos(widths)
	var state := "ENTERED" if entered else "BLOCKED"
	print("QA_TOWER_ENTRY route=%s mode=%s %s frames=%d q=(%.2f,%.3f,%.2f) start_out=%s rise=%.3f run=%.2f grade=1:%.2f width=%.2f min_y=%.3f max_y=%.3f" % [
		name, mode, state, frames, q.x, q.y, q.z, str(outside), max_y - min_y, path_m, grade, width, min_y, max_y])
	if not entered:
		print("QA_TOWER_ENTRY BLOCK %s %s | %s" % [name, mode, stuck])
		_failures += 1
		if bool(spec["stair"]):
			print("KNOWN-ROOK TTQA-052 | %s %s | q=(%.2f,%.3f,%.2f) %s" % [name, mode, q.x, q.y, q.z, stuck])


func _min_pos(xs: Array[float]) -> float:
	var m := -1.0
	for v in xs:
		if v > 0.2 and (m < 0.0 or v < m):
			m = v
	return m


func _place_drum(xz: Vector2, look: Vector2) -> void:
	var feet: Vector3 = ppa._tt_floor_feet(Vector3(xz.x, 0.0, xz.y))
	ppa._qa_tower_place(feet, ppa._drum_up_at(feet), ppa._tower_xf * Vector3(look.x, 0.0, look.y))
	await ppa._qa_frames(30)
	if not ppa._player_body.is_on_floor():
		await ppa._qa_frames(20)


func _qa_leg(goal: Vector2, budget: int) -> Dictionary:
	var goal_w: Vector3 = ppa._tower_xf * Vector3(goal.x, 0.0, goal.y)
	var frames := 0
	var samples: Array[Vector3] = []
	var width := -1.0
	var best := INF
	var stall := 0
	var arrived := false
	var inside := false
	var prev_p: Vector3 = ppa._player_body.global_position
	ppa._qa_key(KEY_W, true)
	await ppa._qa_idle(2)
	while frames < budget:
		var p: Vector3 = ppa._player_body.global_position
		var q: Vector3 = ppa._tower_inv * p
		if frames % 4 == 0:
			samples.append(q)
		if frames % 15 == 0 and ppa._player_body.is_on_floor() and q.y < -0.25:
			var w := _width_here(prev_p, p)
			if w > 0.2:
				width = w if width < 0.0 else minf(width, w)
		prev_p = p
		if _inside_f1(q):
			inside = true
			arrived = true
			break
		var dist := Vector2(q.x - goal.x, q.z - goal.y).length()
		if dist < ARRIVE:
			arrived = true
			ppa._player_body.velocity = Vector3.ZERO
			break
		if dist + 0.15 < best:
			best = dist
			stall = 0
		else:
			stall += 1
		# A rail rub at the breadcrumb counts. Farther than 1.5 m is not there.
		if stall > 50 and dist < 1.5:
			arrived = true
			ppa._player_body.velocity = Vector3.ZERO
			break
		if stall > 70:
			break
		ppa._qa_ring_steer(goal_w - p)
		await get_tree().physics_frame
		frames += 1
	ppa._qa_key(KEY_W, false)
	var blocker := ""
	if not arrived and not inside:
		blocker = _ahead()
	return {"arrived": arrived, "inside": inside, "frames": frames, "samples": samples, "width": width, "blocker": blocker}


func _inside_f1(q: Vector3) -> bool:
	if ppa._player_body == null or not ppa._player_body.is_on_floor():
		return false
	return q.x > -11.6 and q.x < 139.6 and q.z > 0.45 and q.z < 78.55 and absf(q.y) < 0.45


func _width_here(prev: Vector3, p: Vector3) -> float:
	var up: Vector3 = ppa._player_body.up_direction
	var dir := p - prev
	dir -= up * dir.dot(up)
	if dir.length() < 0.02:
		return -1.0
	dir = dir.normalized()
	var side := up.cross(dir).normalized()
	var origin := ppa._player_body.global_position + up * 0.45
	return _ray(origin, side, 3.0) + _ray(origin, -side, 3.0)


func _ray(from: Vector3, dir: Vector3, dist: float) -> float:
	var rq := PhysicsRayQueryParameters3D.create(from, from + dir * dist)
	rq.exclude = [ppa._player_body.get_rid()]
	var hit: Dictionary = ppa.get_world_3d().direct_space_state.intersect_ray(rq)
	if not hit.has("position"):
		return dist
	return from.distance_to(hit["position"])


func _ahead() -> String:
	var b: CharacterBody3D = ppa._player_body
	var q: Vector3 = ppa._tower_inv * b.global_position
	var blk := "q=(%.2f,%.2f,%.2f) slide=" % [q.x, q.y, q.z]
	for sc in range(b.get_slide_collision_count()):
		var kc := b.get_slide_collision(sc)
		var cn: Node = kc.get_collider() as Node
		var n: Vector3 = ppa._tower_xf.basis.inverse() * kc.get_normal()
		blk += "%s n=%s; " % [str(cn.name) if cn != null else "?", str(n.snapped(Vector3.ONE * 0.01))]
	var fwd := -b.global_transform.basis.z
	var up := b.up_direction
	fwd -= up * fwd.dot(up)
	if fwd.length() > 0.01:
		fwd = fwd.normalized()
		for h_v in [0.2, 0.6, 1.2]:
			var h := float(h_v)
			var from: Vector3 = b.global_position + up * h
			var rq := PhysicsRayQueryParameters3D.create(from, from + fwd * 1.6)
			rq.exclude = [b.get_rid()]
			var hit: Dictionary = ppa.get_world_3d().direct_space_state.intersect_ray(rq)
			if hit.has("position"):
				var cn2: Node = hit["collider"] as Node
				blk += "h%.1f:%s@%.2f " % [h, str(cn2.name) if cn2 != null else "?", from.distance_to(hit["position"])]
	return blk
