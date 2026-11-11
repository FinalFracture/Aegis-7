## Rook r7: headless check for the Tennis Tower drop scene.
## godot --headless --path godot -s res://scripts/tennis_tower/tennis_tower_check.gd
## Instances res://scenes/tennis_tower/tennis_tower.tscn, prints placed / missing / meshes / tris / colliders,
## then ray-casts the floor at spawn-critical points (ramp tops, decks, F1, F2, F3) and fails on any miss.
extends SceneTree

const TTL = preload("res://scripts/tennis_tower/tennis_tower_loader.gd")

const PROBES: Array = [
	["F1 foyer", Vector3(-6.0, 3.0, 30.0), 0.0], ["F2 W gallery", Vector3(-5.0, 9.0, 40.0), 6.1], ["F2 E", Vector3(130.0, 9.0, 40.0), 6.1],
	["F3 deck", Vector3(70.0, 15.0, 4.0), 12.2], ["pool ramp top landing", Vector3(9.95, 4.0, 26.7), 2.012],
	["pool deck past exit", Vector3(10.2, 4.0, 26.7), 2.012], ["leisure ramp top", Vector3(15.25, 3.0, 45.5), 1.012],
	["leisure deck past exit", Vector3(15.4, 3.0, 45.5), 1.012], ["W terrace (deck top = F1)", Vector3(-30.0, 3.0, 40.0), 0.0],
]
var _n: Node3D
var _frames: int = 0


func _initialize() -> void:
	var ps: PackedScene = load("res://scenes/tennis_tower/tennis_tower.tscn") as PackedScene
	if ps == null:
		print("TT_CHECK FAIL scene did not load")
		quit(1)
		return
	_n = ps.instantiate() as Node3D
	root.add_child(_n)


func _physics_process(_d: float) -> bool:
	_frames += 1
	if _frames < 3:
		return false
	var st: Dictionary = _n.get("stats")
	print("TT_CHECK stats placed=%d glbs=%d missing=%d meshes(surfaces)=%d tris=%d colliders=%d ms=%d" % [
		int(st["placed"]), int(st["glbs"]), (st["missing"] as Array).size(), int(st["meshes"]), int(st["tris"]), int(st["colliders"]), int(st.get("ms", 0))])
	for m: Variant in st["missing"]:
		print("TT_CHECK missing ", m)
	var space: PhysicsDirectSpaceState3D = _n.get_world_3d().direct_space_state
	var bad: int = (st["missing"] as Array).size()
	for pr: Array in PROBES:
		var from: Vector3 = pr[1]
		var q: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(from, from + Vector3(0, -8.0, 0))
		var hit: Dictionary = space.intersect_ray(q)
		var y: float = (hit["position"] as Vector3).y if hit.has("position") else -999.0
		var ok: bool = absf(y - float(pr[2])) <= 0.02
		if not ok:
			bad += 1
		print("TT_CHECK probe %-24s floor y=%.4f expect %.3f %s" % [pr[0], y, float(pr[2]), "OK" if ok else "FAIL"])
	var xf: Transform3D = TTL.drop_transform()
	var o: Vector3 = xf.origin - Vector3(xf.origin.x, 200.12, -1.25)
	print("TT_CHECK drop origin=%s basis_y=%s r_from_axis=%.4f" % [str(xf.origin), str(xf.basis.y), o.length()])
	print("TT_CHECK ", "PASS" if bad == 0 else "FAIL (%d)" % bad)
	quit(0 if bad == 0 else 1)
	return true
