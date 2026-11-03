# NAV-13 egress capsule sweep (Rook, 2026-11-03). Headless; QA placement mode is required or the scene quits early:
#   godot --headless --path godot -s res://tools/qa/rook_nav13_probe.gd -- --qa-placement
# Loads preface_playable_area.tscn, disables FieldCollider door shapes (doors treated as open), then sweeps a
# 0.35 x 1.75 m capsule in 0.1 m steps (floor ray each step) along each route. Prints `NAV13|<route>|PASS/FAIL`
# plus the blocking collider path + normal, or NO FLOOR. QA_OLD_gallery_z1.8 is the stale pre-Rev C route and is
# expected to FAIL on the 201|202 partition; REVC_spawn_to_exit is the real egress (needs the stair glbs placed).
extends SceneTree
func _initialize() -> void:
	var inst = (load("res://scenes/preface/preface_playable_area.tscn") as PackedScene).instantiate()
	root.add_child(inst)
	for _i in 30: await process_frame
	for _i in 10: await physics_frame
	var space = root.get_world_3d().direct_space_state
	for n in root.find_children("FieldCollider*_Shape", "CollisionShape3D", true, false): n.disabled = true
	for _i in 3: await physics_frame
	var cap := CapsuleShape3D.new(); cap.radius = 0.35; cap.height = 1.75
	var routes = {
		"QA_OLD_gallery_z1.8": [Vector3(-9.35,0,6.2), Vector3(-3.0,0,1.8), Vector3(7.0,0,1.8)],
		"REVC_spawn_to_exit": [Vector3(-9.35,0,6.2), Vector3(-3.0,0,2.0), Vector3(-3.0,0,0.0), Vector3(1.15,0,0.0), Vector3(1.15,0,-4.7), Vector3(1.15,0,-8.1), Vector3(-1.15,0,-8.1), Vector3(-1.15,0,-2.7), Vector3(-1.15,0,-0.3), Vector3(1.15,0,-0.3), Vector3(1.15,0,-8.2), Vector3(0.0,0,-8.6), Vector3(0.0,0,-10.0)]}
	for rn in routes.keys():
		var pts: Array = routes[rn]; var y := 4.25; var ok := true
		for i in range(pts.size() - 1):
			var a: Vector3 = pts[i]; var b: Vector3 = pts[i + 1]
			var n := int(ceil(a.distance_to(b) / 0.1))
			for k in range(n):
				var p := a.lerp(b, float(k) / n); var q := a.lerp(b, float(k + 1) / n)
				var rq := PhysicsRayQueryParameters3D.create(Vector3(p.x, y + 0.3, p.z), Vector3(p.x, y - 1.5, p.z))
				var h := space.intersect_ray(rq)
				if h.is_empty():
					print("NAV13|%s|NO FLOOR at %s (y %.2f)" % [rn, str(p), y]); ok = false; break
				var fy: float = (h["position"] as Vector3).y
				y = fy
				var sp := PhysicsShapeQueryParameters3D.new(); sp.shape = cap; sp.margin = 0.0
				sp.transform = Transform3D(Basis.IDENTITY, Vector3(p.x, fy + 0.3 + 0.875, p.z)); sp.motion = Vector3(q.x - p.x, 0, q.z - p.z)
				var fr = space.cast_motion(sp)
				if fr[0] < 1.0:
					sp.transform.origin += sp.motion * fr[1]
					var info = space.get_rest_info(sp); var cid = info.get("collider_id", 0)
					var o = instance_from_id(cid) if cid else null
					print("NAV13|%s|BLOCK at %s floor %.3f by %s n%s (floor %s)" % [rn, str(p), fy, (str(o.get_path()) if o else "?"), str(info.get("normal","")), str((h["collider"] as Node).get_path())])
					ok = false; break
			if not ok: break
		print("NAV13|%s|%s|last y %.3f" % [rn, "PASS" if ok else "FAIL", y])
	quit()
