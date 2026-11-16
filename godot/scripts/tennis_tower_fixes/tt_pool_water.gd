extends RefCounted
## TTQA-009. Water volumes and ladder climb areas for Rook's pools.
## Walk-out stairs, ladders, river entries and the splash basin are already
## built (a7e7d35). This script does not add a second set of steps.
## Splash stays dry when the basin tile is already at the raised deck.
## Areas live in building coords. sample() tests those same boxes at the
## body origin so a one-frame teleport still counts; overlaps_body is logged
## only as a mismatch. Deck walking stays outside every box.


var _tower: Node3D
var _areas: Array[Area3D] = []
var _vols: Array[Dictionary] = []
var _excludes: Array[Dictionary] = []
var _climbs: Array[Dictionary] = []
var splash_top: float = -999.0
var splash_ray: float = -999.0
var splash_infill: bool = false
var overlap_mismatches: int = 0


func setup(tower: Node3D) -> void:
	_tower = tower
	_areas.clear()
	_vols.clear()
	_excludes.clear()
	_climbs.clear()
	var root := Node3D.new()
	root.name = "TT_PoolWater"
	tower.add_child(root)
	# Lap tank. Surface 1.92, tile ~0.035. The alcove extension covers the
	# recessed east stair so a swimmer can reach a tread before step-up.
	var lap_main := _box(2.70, 27.35, -0.20, 1.92, 0.70, 21.30, 0.035, 1.92, true)
	var lap_alcove := _box(27.15, 29.45, -0.20, 1.92, 0.75, 3.65, 0.035, 1.92, true)
	_add_area(root, "TT_Water_Lap", [lap_main, lap_alcove])
	# Diving well. Surface 1.92, tile ~-2.465. Stair XZ stays inside; standing
	# on a tread cancels swim in the player hook.
	var dive := _box(15.15, 27.95, -2.70, 1.92, 22.15, 33.85, -2.465, 1.92, true)
	_add_area(root, "TT_Water_Dive", [dive])
	# Lazy river. Four channels, surface 0.85, shallow enough to wade.
	var river: Array[Dictionary] = [
		_box(1.15, 28.85, -0.15, 0.85, 47.15, 49.85, 0.035, 0.85, false),
		_box(1.15, 28.85, -0.15, 0.85, 72.15, 74.85, 0.035, 0.85, false),
		_box(1.15, 3.85, -0.15, 0.85, 50.05, 71.95, 0.035, 0.85, false),
		_box(26.15, 28.85, -0.15, 0.85, 50.05, 71.95, 0.035, 0.85, false),
	]
	_add_area(root, "TT_Water_River", river)
	# Slide runout. Surface 0.92, wade, stair at the west end.
	var runout := _box(5.15, 22.85, -0.05, 0.92, 64.15, 70.85, 0.035, 0.92, false)
	_add_area(root, "TT_Water_Runout", [runout])
	# Bank entries and the runout stair. Swim turns off on the treads even
	# before the feet register a floor, so the 0.16 m risers walk normally.
	_exclude(20.85, 22.55, 46.55, 48.70) # S outer, xc 21.7
	_exclude(15.45, 17.15, 48.35, 50.45) # S island, xc 16.3
	_exclude(10.45, 12.15, 73.35, 75.50) # N outer, xc 11.3
	_exclude(5.85, 7.55, 71.50, 73.65) # N island, xc 6.7
	_exclude(4.85, 6.65, 69.05, 71.55) # runout west stair
	# Ladders. Approach is ~0.70 m into the water so the capsule clears the
	# 0.06 m rungs. The exit point is outside the box.
	_climb("lap_n", 11.85, 13.15, -0.30, 3.20, 20.35, 21.55, 12.5, 20.74, 12.5, 22.45, 2.012)
	_climb("lap_w", 2.55, 3.70, -0.30, 3.20, 20.15, 21.45, 3.26, 20.8, 1.60, 20.8, 2.012)
	_climb("lap_e", 26.25, 27.55, -0.30, 3.20, 18.85, 20.15, 26.74, 19.5, 28.55, 19.5, 2.012)
	_climb("dive_e", 26.85, 28.05, -3.10, 3.20, 22.35, 23.65, 27.24, 23.0, 28.95, 23.0, 2.012)
	_climb("dive_w", 14.85, 16.25, -3.10, 3.20, 22.35, 23.65, 15.76, 23.0, 14.05, 23.0, 2.012)
	_measure_splash(tower)
	print("[TT] pool volumes=%d climbs=%d excludes=%d areas=%d splash_mesh=%.3f splash_ray=%.3f infill=%s" % [
		_vols.size(), _climbs.size(), _excludes.size(), _areas.size(), splash_top, splash_ray, str(splash_infill)])


func sample(world_pos: Vector3, climb_intent: bool, body: Node = null) -> Dictionary:
	var q := _to_local(world_pos)
	var hit := {
		"in_water": false, "climb": false, "climb_i": -1, "out": false,
		"q_y": q.y, "floor_q": -999.0, "deep": false, "float_q": 0.0, "surface": 0.0,
	}
	if q.x < -2.0 or q.x > 34.0 or q.z < -2.0 or q.z > 80.0 or q.y < -5.0 or q.y > 8.0:
		return hit
	if climb_intent:
		for i: int in range(_climbs.size()):
			if _contains(_climbs[i], q):
				hit["climb"] = true
				hit["climb_i"] = i
				hit["in_water"] = true
				hit["deep"] = true
				hit["floor_q"] = float(_climbs[i]["floor_q"])
				hit["surface"] = float(_climbs[i]["surface"])
				hit["float_q"] = float(_climbs[i]["surface"]) - 1.52
				return hit
	if _excluded(q):
		return hit
	for v: Dictionary in _vols:
		if _contains(v, q):
			hit["in_water"] = true
			hit["deep"] = bool(v["deep"])
			hit["floor_q"] = float(v["floor_q"])
			hit["surface"] = float(v["surface"])
			hit["float_q"] = float(v["surface"]) - 1.52
			break
	if body is CollisionObject3D and not _areas.is_empty():
		var overlapped := false
		for area: Area3D in _areas:
			if area.overlaps_body(body):
				overlapped = true
				break
		if overlapped != bool(hit["in_water"]):
			overlap_mismatches += 1
	return hit


func begin_climb(body: CharacterBody3D, hit: Dictionary, _delta: float) -> void:
	var idx := int(hit.get("climb_i", -1))
	if idx < 0 or idx >= _climbs.size():
		return
	var c: Dictionary = _climbs[idx]
	var q := _to_local(body.global_position)
	var deck := float(c["deck"])
	if q.y >= deck - 0.16:
		body.global_position = _tower.global_transform * Vector3(float(c["ex"]), deck - 0.10, float(c["ez"]))
		body.velocity = Vector3.ZERO
		hit["out"] = true
		hit["in_water"] = false
		hit["climb"] = false
		hit["deep"] = false
		return
	var ax := float(c["ax"])
	var az := float(c["az"])
	var dx := ax - q.x
	var dz := az - q.z
	var dist := sqrt(dx * dx + dz * dz)
	if dist > 0.02:
		var step := minf(0.40, dist)
		q.x += dx / dist * step
		q.z += dz / dist * step
		body.global_position = _tower.global_transform * q


## Deep water: hold the body at float_q (eye just above the surface) and clamp
## a dive so a board landing never reaches the tank floor. Shallow water keeps
## the gravity result; a fresh jump is a short hop, not a 4.8 m/s launch.
func swim_up(hit: Dictionary, v_up: float, _delta: float, jump_held: bool, jump_just: bool) -> float:
	if not bool(hit.get("deep", false)):
		if jump_just:
			return maxf(v_up, 2.2)
		return v_up
	# Jump holds just under the surface instead of launching out of the volume.
	# A dive is clamped so the body cannot reach a deep tank floor.
	var surface := float(hit.get("surface", 0.0))
	var target := float(hit.get("float_q", 0.0))
	if jump_held:
		target = surface - 0.08
	var err := target - float(hit.get("q_y", 0.0))
	return clampf(err * 3.2, -1.35, 2.6)


func _to_local(world_pos: Vector3) -> Vector3:
	if _tower == null:
		return world_pos
	return _tower.global_transform.affine_inverse() * world_pos


func _box(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float, floor_q: float, surface: float, deep: bool) -> Dictionary:
	var box := {
		"x0": x0, "x1": x1, "y0": y0, "y1": y1, "z0": z0, "z1": z1,
		"floor_q": floor_q, "surface": surface, "deep": deep,
	}
	_vols.append(box)
	return box


func _exclude(x0: float, x1: float, z0: float, z1: float) -> void:
	_excludes.append({"x0": x0, "x1": x1, "y0": -1.0, "y1": 2.4, "z0": z0, "z1": z1})


func _climb(nm: String, x0: float, x1: float, y0: float, y1: float, z0: float, z1: float, ax: float, az: float, ex: float, ez: float, deck: float) -> void:
	_climbs.append({
		"name": nm, "x0": x0, "x1": x1, "y0": y0, "y1": y1, "z0": z0, "z1": z1,
		"ax": ax, "az": az, "ex": ex, "ez": ez, "deck": deck,
		"floor_q": -2.465 if nm.begins_with("dive") else 0.035,
		"surface": 1.92,
	})


func _add_area(root: Node3D, nm: String, boxes: Array) -> void:
	var area := Area3D.new()
	area.name = nm
	area.collision_layer = 0
	area.collision_mask = 1
	area.monitoring = true
	area.monitorable = false
	for box: Dictionary in boxes:
		var shape := CollisionShape3D.new()
		var sh := BoxShape3D.new()
		sh.size = Vector3(float(box["x1"]) - float(box["x0"]), float(box["y1"]) - float(box["y0"]), float(box["z1"]) - float(box["z0"]))
		shape.shape = sh
		shape.position = Vector3(
			(float(box["x0"]) + float(box["x1"])) * 0.5,
			(float(box["y0"]) + float(box["y1"])) * 0.5,
			(float(box["z0"]) + float(box["z1"])) * 0.5)
		area.add_child(shape)
	root.add_child(area)
	_areas.append(area)


func _contains(box: Dictionary, q: Vector3) -> bool:
	return q.x >= float(box["x0"]) and q.x <= float(box["x1"]) and q.y >= float(box["y0"]) and q.y <= float(box["y1"]) and q.z >= float(box["z0"]) and q.z <= float(box["z1"])


func _excluded(q: Vector3) -> bool:
	for box: Dictionary in _excludes:
		if _contains(box, q):
			return true
	return false


func _measure_splash(tower: Node3D) -> void:
	tower.force_update_transform()
	var best := -999.0
	var stack: Array[Node] = [tower]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for ch: Node in n.get_children():
			stack.append(ch)
		if not (n is MeshInstance3D):
			continue
		if not _under_named(n, "splash") or _under_named(n, "spray"):
			continue
		var mi := n as MeshInstance3D
		if mi.mesh == null:
			continue
		var ab: AABB = tower.global_transform.affine_inverse() * (mi.global_transform * mi.get_aabb())
		var cx := ab.position.x + ab.size.x * 0.5
		var cz := ab.position.z + ab.size.z * 0.5
		if cx < 4.0 or cx > 18.0 or cz < 50.0 or cz > 63.0:
			continue
		if ab.size.y > 1.2:
			continue
		best = maxf(best, ab.position.y + ab.size.y)
	splash_top = best
	splash_ray = _ray_y(tower, 11.0, 56.5)
	var top := best
	if top < -100.0:
		top = splash_ray
	# Basin tile is specified at +1.015, flush with the +1.012 leisure deck.
	# A second slab would z-fight that tile. Add one only if the floor is low.
	if top < 0.90:
		_add_infill(tower, top)
		splash_infill = true
		print("[TT] splash infill added (measured %.3f)" % top)
	else:
		print("[TT] splash already raised y=%.3f (ray %.3f); no water volume" % [best, splash_ray])


func _under_named(n: Node, token: String) -> bool:
	var p: Node = n
	while p != null:
		if String(p.name).to_lower().contains(token):
			return true
		p = p.get_parent()
	return false


func _ray_y(tower: Node3D, x: float, z: float) -> float:
	var world := tower.get_world_3d()
	if world == null:
		return -999.0
	var xf := tower.global_transform
	var rq := PhysicsRayQueryParameters3D.create(xf * Vector3(x, 4.0, z), xf * Vector3(x, -1.0, z), 1)
	var hit := world.direct_space_state.intersect_ray(rq)
	if hit.is_empty():
		return -999.0
	return (xf.affine_inverse() * (hit["position"] as Vector3)).y


func _add_infill(tower: Node3D, from_y: float) -> void:
	var y0 := 0.90 if from_y < 0.0 else from_y
	var y1 := 1.015
	if y1 - y0 < 0.02:
		y1 = y0 + 0.04
	var body := StaticBody3D.new()
	body.name = "TT_SplashDeckInfill"
	body.collision_layer = 1
	body.collision_mask = 1
	var shape := CollisionShape3D.new()
	var sh := BoxShape3D.new()
	sh.size = Vector3(11.6, y1 - y0, 10.6)
	shape.shape = sh
	shape.position = Vector3(11.0, (y0 + y1) * 0.5, 56.5)
	body.add_child(shape)
	var mi := MeshInstance3D.new()
	var mesh := BoxMesh.new()
	mesh.size = sh.size
	mi.mesh = mesh
	mi.position = shape.position
	var mat := StandardMaterial3D.new()
	mat.albedo_color = Color(0.74, 0.73, 0.70)
	mat.roughness = 0.82
	mi.material_override = mat
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mi.set_meta("tt_no_batch", true)
	body.add_child(mi)
	tower.add_child(body)
