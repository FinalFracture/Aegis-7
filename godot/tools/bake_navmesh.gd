extends SceneTree
## Bake the preface playable-area navmesh (D670-05).
## Covers interior + exterior walk: ramp, platform, hatch, walkways.
##   xvfb-run -a godot --path godot --rendering-driver opengl3 -s res://tools/bake_navmesh.gd -- --qa-placement
## --qa-placement is a user arg so preface_playable_area keeps interior streaming off.
## The scene skips PlayableNavRegion while this script is on the command line.
## Force-field door fields are excluded so doorways stay open in the mesh.
## Furniture tops, the roof slab, and geometry outside x -50..60 are excluded.
## Exit 0 when the baked mesh has at least one polygon, else 1.

const SCENE_PATH := "res://scenes/preface/preface_playable_area.tscn"
const NAV_PATH := "res://assets/nav/preface_navmesh.tres"
const SETTLE_FRAMES := 30
const _SKIP_NAME_BITS: PackedStringArray = [
	"furniture", "bunk", "workbench", "planter", "bench", "roof",
	"counter", "desk", "shelf", "cabinet", "locker", "armchair", "sofa", "table"
]

var _scene: Node = null
var _frames: int = 0
var _done: bool = false


func _initialize() -> void:
	var packed: PackedScene = load(SCENE_PATH) as PackedScene
	if packed == null:
		print("NAVMESH_BAKE polygons=0 vertices=0 islands=0")
		quit(1)
		return
	var inst: Node = packed.instantiate()
	if inst == null:
		print("NAVMESH_BAKE polygons=0 vertices=0 islands=0")
		quit(1)
		return
	# Before add_child so _ready sees it even when --qa-placement is omitted.
	# Headless boot otherwise sets _validate_only and quits the tree at frame 4.
	inst.set("_qa_placement", true)
	if "_validate_only" in inst:
		inst.set("_validate_only", false)
	root.add_child(inst)
	_scene = inst


func _process(_delta: float) -> bool:
	if _done:
		return true
	_frames += 1
	if _frames < SETTLE_FRAMES:
		return false
	_done = true
	_bake()
	return true


func _bake() -> void:
	var navmesh := NavigationMesh.new()
	navmesh.agent_radius = 0.35
	navmesh.agent_height = 1.75
	navmesh.agent_max_climb = 0.3
	navmesh.cell_size = 0.1
	navmesh.cell_height = 0.05
	navmesh.geometry_parsed_geometry_type = NavigationMesh.PARSED_GEOMETRY_STATIC_COLLIDERS
	# Residential playable only. x -50..60 drops the gravity-ring islands at x 143..157.
	# y tops out at 7.2 so the roof slab at y 8.95 is outside the bake.
	navmesh.filter_baking_aabb = AABB(Vector3(-50.0, -1.0, -50.0), Vector3(110.0, 8.2, 70.0))
	_exclude_force_field_doors()
	_exclude_furniture_and_roof()
	var source := NavigationMeshSourceGeometryData3D.new()
	NavigationServer3D.parse_source_geometry_data(navmesh, source, _scene)
	NavigationServer3D.bake_from_source_geometry_data(navmesh, source)
	_drop_stray_flat_islands(navmesh)
	_compact_navmesh(navmesh)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://assets/nav"))
	var err := ResourceSaver.save(navmesh, NAV_PATH)
	var n := navmesh.get_polygon_count()
	var v := navmesh.get_vertices().size()
	var islands := _count_islands(navmesh)
	print("NAVMESH_BAKE polygons=%d vertices=%d islands=%d" % [n, v, islands])
	quit(0 if err == OK and n > 0 else 1)


func _exclude_force_field_doors() -> void:
	# Door registry in preface_playable_area.gd (_rfid_doors): field_collider / col_a / col_b.
	if _scene != null and _scene.get("_rfid_doors") is Array:
		for entry: Variant in _scene.get("_rfid_doors"):
			if not (entry is Dictionary):
				continue
			var door: Dictionary = entry
			for key: String in ["field_collider", "col_a", "col_b"]:
				_disable_field_shape(door.get(key) as CollisionShape3D)
	if _scene == null:
		return
	var stack: Array[Node] = [_scene]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		var nm := String(n.name)
		if nm == "FieldCollider" or nm.begins_with("FieldCollider_"):
			_drop_collision_node(n)
		for ch: Node in n.get_children():
			stack.append(ch)


func _disable_field_shape(cs: CollisionShape3D) -> void:
	if cs == null or not is_instance_valid(cs):
		return
	cs.disabled = true
	var body := cs.get_parent()
	if body is CollisionObject3D:
		_drop_collision_node(body)


func _exclude_furniture_and_roof() -> void:
	if _scene == null:
		return
	var stack: Array[Node] = [_scene]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if _is_furniture_or_roof(n):
			_strip_collision_under(n)
			continue
		for ch: Node in n.get_children():
			stack.append(ch)


func _is_furniture_or_roof(n: Node) -> bool:
	if n.is_in_group("furniture") or n.is_in_group("roof") or n.is_in_group("navmesh_exclude"):
		return true
	var nm := String(n.name).to_lower()
	for bit: String in _SKIP_NAME_BITS:
		if nm.contains(bit):
			return true
	return false


func _strip_collision_under(root: Node) -> void:
	var bodies: Array[Node] = []
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if n is CollisionObject3D or n is CollisionShape3D:
			bodies.append(n)
		for ch: Node in n.get_children():
			stack.append(ch)
	for b: Node in bodies:
		_drop_collision_node(b)


func _drop_collision_node(n: Node) -> void:
	if n == null or not is_instance_valid(n):
		return
	if n is CollisionObject3D:
		(n as CollisionObject3D).collision_layer = 0
		(n as CollisionObject3D).collision_mask = 0
	elif n is CollisionShape3D:
		(n as CollisionShape3D).disabled = true
		var body := n.get_parent()
		if body is CollisionObject3D:
			(body as CollisionObject3D).collision_layer = 0
			(body as CollisionObject3D).collision_mask = 0
	# Out of the parsed tree. Parser walks nodes, not orphaned bodies.
	var parent := n.get_parent()
	if parent != null and (n is CollisionObject3D or n is CollisionShape3D):
		parent.remove_child(n)


func _is_stray_nav_y(y: float) -> bool:
	# Flat islands on furniture tops (~0.8, ~1.65, ~5.1 above the floors) and the roof slab.
	if absf(y - 0.80) <= 0.20:
		return true
	if absf(y - 1.65) <= 0.20:
		return true
	if absf(y - 5.10) <= 0.20:
		return true
	if absf(y - 8.95) <= 0.30:
		return true
	return false


func _drop_stray_flat_islands(navmesh: NavigationMesh) -> void:
	var n := navmesh.get_polygon_count()
	if n == 0:
		return
	var verts := navmesh.get_vertices()
	var parent := _polygon_parents(navmesh)
	var groups: Dictionary = {}
	for i: int in n:
		var root := _uf_find(parent, i)
		var bucket: Array = groups.get(root, [])
		bucket.append(i)
		groups[root] = bucket
	var drop: Dictionary = {}
	for key: Variant in groups.keys():
		var polys: Array = groups[key]
		var ymin := INF
		var ymax := -INF
		var ysum := 0.0
		var yc := 0
		for pi: Variant in polys:
			for vi: int in navmesh.get_polygon(int(pi)):
				var y := verts[vi].y
				ymin = minf(ymin, y)
				ymax = maxf(ymax, y)
				ysum += y
				yc += 1
		if yc == 0 or ymax - ymin > 0.25:
			continue
		if _is_stray_nav_y(ysum / float(yc)):
			for pi2: Variant in polys:
				drop[int(pi2)] = true
	if drop.is_empty():
		return
	var kept: Array[PackedInt32Array] = []
	for i: int in n:
		if not drop.has(i):
			kept.append(navmesh.get_polygon(i))
	navmesh.clear_polygons()
	for poly: PackedInt32Array in kept:
		navmesh.add_polygon(poly)


func _compact_navmesh(navmesh: NavigationMesh) -> void:
	var old_verts := navmesh.get_vertices()
	var n := navmesh.get_polygon_count()
	var polys: Array[PackedInt32Array] = []
	var remap: Dictionary = {}
	var new_verts := PackedVector3Array()
	for i: int in n:
		var poly := navmesh.get_polygon(i)
		var mapped := PackedInt32Array()
		mapped.resize(poly.size())
		for k: int in poly.size():
			var vi := int(poly[k])
			if not remap.has(vi):
				remap[vi] = new_verts.size()
				new_verts.append(old_verts[vi])
			mapped[k] = int(remap[vi])
		polys.append(mapped)
	navmesh.clear_polygons()
	navmesh.set_vertices(new_verts)
	for poly: PackedInt32Array in polys:
		navmesh.add_polygon(poly)


func _count_islands(navmesh: NavigationMesh) -> int:
	var n := navmesh.get_polygon_count()
	if n == 0:
		return 0
	var parent := _polygon_parents(navmesh)
	var roots: Dictionary = {}
	for i: int in n:
		roots[_uf_find(parent, i)] = true
	return roots.size()


## Connected components over shared vertices (index or position within 5 cm) and therefore shared edges.
func _polygon_parents(navmesh: NavigationMesh) -> Array:
	var n := navmesh.get_polygon_count()
	var verts := navmesh.get_vertices()
	var parent: Array = []
	parent.resize(n)
	for i: int in n:
		parent[i] = i
	var buckets: Dictionary = {}
	for pi: int in n:
		for vi: int in navmesh.get_polygon(pi):
			var p: Vector3 = verts[vi]
			var key := Vector3i(int(round(p.x / 0.05)), int(round(p.y / 0.05)), int(round(p.z / 0.05)))
			if buckets.has(key):
				_uf_union(parent, pi, int(buckets[key]))
			else:
				buckets[key] = pi
			for ox: int in range(-1, 2):
				for oy: int in range(-1, 2):
					for oz: int in range(-1, 2):
						var nk := Vector3i(key.x + ox, key.y + oy, key.z + oz)
						if buckets.has(nk):
							_uf_union(parent, pi, int(buckets[nk]))
	return parent


func _uf_find(parent: Array, i: int) -> int:
	var root := i
	while int(parent[root]) != root:
		root = int(parent[root])
	while int(parent[i]) != root:
		var nxt := int(parent[i])
		parent[i] = root
		i = nxt
	return root


func _uf_union(parent: Array, a: int, b: int) -> void:
	var ra := _uf_find(parent, a)
	var rb := _uf_find(parent, b)
	if ra != rb:
		parent[rb] = ra
