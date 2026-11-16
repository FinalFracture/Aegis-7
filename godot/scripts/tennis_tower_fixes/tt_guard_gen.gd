extends Node
## Offline grid: walk area before fallback, fallback + lift seals, walk area
## after, then drop edges -> tt_guard_rails.json. Standalone tower or PPA.

const _FB := preload("res://scripts/tennis_tower_fixes/tt_collider_fallback.gd")
const _GR := preload("res://scripts/tennis_tower_fixes/tt_guard_rails.gd")
const _WG := preload("res://scripts/tennis_tower_fixes/tt_walk_grid.gd")

var ppa: PrefacePlayableArea


func _ready() -> void:
	_run.call_deferred()


func _run() -> void:
	var tower: Node3D
	var mask: int = 1
	if ppa != null:
		var guard: int = 0
		while not ppa.has_meta("exterior_spawned") and guard < 4000:
			await get_tree().physics_frame
			guard += 1
		tower = ppa._tower
		mask = 1 << 18
	else:
		tower = (load("res://scenes/tennis_tower/tennis_tower.tscn") as PackedScene).instantiate() as Node3D
		add_child(tower)
	await get_tree().physics_frame
	await get_tree().physics_frame
	var space: PhysicsDirectSpaceState3D = tower.get_world_3d().direct_space_state
	print("[TT] walk grid BEFORE")
	var before: Array = _WG.collect(tower, space, mask)
	var ba: Dictionary = _WG.analyze(before)
	_WG.report("before", ba)
	_FB.run(tower)
	await get_tree().physics_frame
	await get_tree().physics_frame
	space = tower.get_world_3d().direct_space_state
	_rays(space, tower, mask)
	print("[TT] walk grid AFTER")
	var after: Array = _WG.collect(tower, space, mask)
	var aa: Dictionary = _WG.analyze(after)
	_WG.report("after", aa)
	_WG.diff(ba, aa)
	var floor_nodes: Array = _WG.player_floor_nodes(after, aa)
	var drops: Array = _WG.drops(tower, space, floor_nodes, mask)
	var segs: Array = _GR.compile(drops)
	_GR.write_segments(segs)
	print("[TT] GUARD_GEN DONE segments=%d" % segs.size())
	get_tree().quit(0)


func _rays(space: PhysicsDirectSpaceState3D, tower: Node3D, mask: int) -> void:
	var tests: Array = [
		["lift_981", Vector3(63.5, 1.0, 13.0), Vector3(68.5, 1.0, 13.0)],
		["lift_982", Vector3(68.5, 7.0, 18.0), Vector3(68.5, 7.0, 12.0)],
		["lift_983", Vector3(68.5, 13.1, 18.0), Vector3(68.5, 13.1, 12.0)],
		["stair_b", Vector3(55.0, 1.0, 6.0), Vector3(62.0, 1.0, 6.0)],
		["stair_a", Vector3(73.5, 1.0, 6.5), Vector3(73.5, 1.0, 13.5)],
		["court_x", Vector3(61.5, 1.0, 24.5), Vector3(61.5, 1.0, 30.5)],
		["court_z", Vector3(71.5, 1.0, 33.0), Vector3(77.5, 1.0, 33.0)],
		["restroom", Vector3(37.0, 1.0, 66.0), Vector3(37.0, 1.0, 70.0)],
		["vr", Vector3(128.5, 1.0, 50.8), Vector3(136.0, 1.0, 50.8)],
	]
	for t: Array in tests:
		var a: Vector3 = t[1]
		var b: Vector3 = t[2]
		var rq: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(tower.global_transform * a, tower.global_transform * b, mask)
		rq.hit_back_faces = true
		var hit: Dictionary = space.intersect_ray(rq)
		if not hit.has("position"):
			print("[TT] ray %s MISS" % String(t[0]))
			continue
		var q: Vector3 = tower.global_transform.affine_inverse() * (hit["position"] as Vector3)
		var cn: Node = hit.get("collider") as Node
		print("[TT] ray %s hit q=(%.2f,%.2f,%.2f) %s" % [String(t[0]), q.x, q.y, q.z, String(cn.name) if cn != null else "?"])
