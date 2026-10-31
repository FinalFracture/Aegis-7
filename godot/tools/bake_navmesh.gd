extends SceneTree
## Bake the preface playable-area navmesh (D670-05).
## Covers interior + exterior walk: ramp, platform, hatch, walkways.
##   xvfb-run -a godot --path godot --rendering-driver opengl3 -s res://tools/bake_navmesh.gd -- --qa-placement
## --qa-placement is a user arg so preface_playable_area keeps interior streaming off.
## The scene skips PlayableNavRegion while this script is on the command line.
## Closed force-field door colliders are baked as obstacles, so doorways are cut.
## A 0.2 m BakeDoorObstacle on each door plane also extends 0.3 m below the pivot.
## Field-gated openings (D-204 hatch, service-field and closed-hatch colliders) get the same
## obstacle, 0.1 m larger than the opening on each side. The Apt201 slab seam at z 6.20 is a
## bake-only wall: that slab covers the Room1A spool, so a closed-field path was ending on it.
## Baking AABB is x -50..60, y -1..12, z -60..40 (apartments near y 4.25, and the hatch).
## Furniture and roof are name/group exclusions of that node's own colliders, not floors.
## Polygons with any vertex x > 100 (gravity ring) are dropped after the bake.
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
	# 0.25 is 5 x cell_size, so the radius lands on the voxel grid. Height and climb stay.
	navmesh.agent_radius = 0.25
	navmesh.agent_height = 1.75
	navmesh.agent_max_climb = 0.3
	navmesh.cell_size = 0.05
	navmesh.cell_height = 0.05
	navmesh.geometry_parsed_geometry_type = NavigationMesh.PARSED_GEOMETRY_STATIC_COLLIDERS
	# x -50..60, y -1..12, z -60..40. Tall enough for the apartments (y ~4.25) and the hatch.
	# Do not clip y at 7.2: that rejected interior meshes that also reach the roof.
	navmesh.filter_baking_aabb = AABB(Vector3(-50.0, -1.0, -60.0), Vector3(110.0, 13.0, 100.0))
	_block_force_field_doors()
	_block_field_gated_openings()
	_block_apt201_slab_seam()
	_exclude_furniture_and_roof()
	var source := NavigationMeshSourceGeometryData3D.new()
	NavigationServer3D.parse_source_geometry_data(navmesh, source, _scene)
	NavigationServer3D.bake_from_source_geometry_data(navmesh, source)
	_drop_far_x_polygons(navmesh)
	_compact_navmesh(navmesh)
	DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path("res://assets/nav"))
	var err := ResourceSaver.save(navmesh, NAV_PATH)
	var n := navmesh.get_polygon_count()
	var v := navmesh.get_vertices().size()
	var islands := _count_islands(navmesh)
	print("NAVMESH_BAKE polygons=%d vertices=%d islands=%d" % [n, v, islands])
	quit(0 if err == OK and n > 0 else 1)


func _block_force_field_doors() -> void:
	# Keep the closed FieldCollider bodies in the parsed tree. They are the doorway walls.
	# Also drop a 0.2 m box through the opening, 0.3 m below the pivot, so an L2 floor crack
	# (pivot y 4.32, floor near 4.20) cannot stay walkable. Jambs and the header stay.
	if _scene == null:
		return
	if _scene.get("_rfid_doors") is Array:
		for entry: Variant in _scene.get("_rfid_doors"):
			if not (entry is Dictionary):
				continue
			var door: Dictionary = entry
			for key: String in ["field_collider", "col_a", "col_b"]:
				_enable_field_shape(door.get(key) as CollisionShape3D)
	var stack: Array[Node] = [_scene]
	var fields: Array[StaticBody3D] = []
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		var nm := String(n.name)
		if (nm == "FieldCollider" or nm.begins_with("FieldCollider_")) and n is StaticBody3D:
			fields.append(n as StaticBody3D)
		for ch: Node in n.get_children():
			stack.append(ch)
	for field: StaticBody3D in fields:
		_enable_field_body(field)
		_add_bake_door_box(field)


func _enable_field_shape(cs: CollisionShape3D) -> void:
	if cs == null or not is_instance_valid(cs):
		return
	cs.disabled = false
	var body := cs.get_parent()
	if body is CollisionObject3D:
		_enable_field_body(body as CollisionObject3D)


func _enable_field_body(body: CollisionObject3D) -> void:
	if body == null or not is_instance_valid(body):
		return
	body.collision_layer = 1
	body.collision_mask = 1
	for ch: Node in body.get_children():
		if ch is CollisionShape3D:
			(ch as CollisionShape3D).disabled = false


func _add_bake_door_box(field_body: StaticBody3D) -> void:
	var parent := field_body.get_parent() as Node3D
	if parent == null or parent.get_node_or_null("BakeDoorObstacle") != null:
		return
	var x0 := INF
	var x1 := -INF
	var y0 := INF
	var y1 := -INF
	var any := false
	for sib: Node in parent.get_children():
		if not (sib is StaticBody3D):
			continue
		var sn := String(sib.name)
		if sn != "FieldCollider" and not sn.begins_with("FieldCollider_") and not sn.begins_with("PortalJambCollider") and sn != "PortalHeaderCollider":
			continue
		var body := sib as StaticBody3D
		for ch: Node in body.get_children():
			if not (ch is CollisionShape3D):
				continue
			var shape: Shape3D = (ch as CollisionShape3D).shape
			if not (shape is BoxShape3D):
				continue
			var bsz: Vector3 = (shape as BoxShape3D).size
			var c: Vector3 = body.position
			x0 = minf(x0, c.x - bsz.x * 0.5)
			x1 = maxf(x1, c.x + bsz.x * 0.5)
			y0 = minf(y0, c.y - bsz.y * 0.5)
			y1 = maxf(y1, c.y + bsz.y * 0.5)
			any = true
	if not any:
		return
	# 0.3 m below the lowest portal collider (the pivot) so the slab bites the floor.
	y0 -= 0.30
	var body_box := StaticBody3D.new()
	body_box.name = "BakeDoorObstacle"
	body_box.position = Vector3((x0 + x1) * 0.5, (y0 + y1) * 0.5, field_body.position.z)
	parent.add_child(body_box)
	var cs := CollisionShape3D.new()
	cs.name = "BakeDoorObstacle_Shape"
	var bs := BoxShape3D.new()
	bs.size = Vector3(maxf(x1 - x0, 0.20), maxf(y1 - y0, 0.20), 0.20)
	cs.shape = bs
	body_box.add_child(cs)


func _block_field_gated_openings() -> void:
	# Door FieldCollider bodies already have a BakeDoorObstacle. This pass catches every other
	# field-gated opening: the D-204 hatch, a service field, or a closed hatch collider.
	if _scene == null:
		return
	var stack: Array[Node] = [_scene]
	var hits: Array[Node] = []
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if _is_gated_opening_node(n) and not _ancestor_has_bake_obstacle(n):
			hits.append(n)
		for ch: Node in n.get_children():
			stack.append(ch)
	for node: Node in hits:
		_add_gated_opening_obstacle(node)


func _is_gated_opening_node(n: Node) -> bool:
	var nm := String(n.name).to_lower()
	if nm == "bakedoorobstacle" or nm.begins_with("bakedoorobstacle") or nm.begins_with("bakeslab"):
		return false
	var named := nm.contains("hatch") or nm.contains("d204") or nm.contains("servicefield")
	named = named or (nm.contains("closed") and (nm.contains("hatch") or nm.contains("field")))
	if named:
		return true
	# "Field" only on a collider. FieldPlane meshes and the door model are not openings.
	if not (n is CollisionObject3D or n is CollisionShape3D):
		return false
	return nm.contains("field") or nm.contains("forcefield")


func _ancestor_has_bake_obstacle(n: Node) -> bool:
	var c: Node = n
	while c != null:
		if c.get_node_or_null("BakeDoorObstacle") != null:
			return true
		c = c.get_parent()
	return false


func _add_gated_opening_obstacle(node: Node) -> void:
	var aabb := _opening_world_aabb(node)
	if aabb.size.length_squared() <= 0.0001:
		return
	# 0.1 m past the opening on each side, and 0.3 m lower so the box bites the floor.
	aabb.position -= Vector3(0.1, 0.4, 0.1)
	aabb.size += Vector3(0.2, 0.5, 0.2)
	var body := StaticBody3D.new()
	var nm := String(node.name)
	body.name = "BakeDoorObstacle_" + nm
	body.collision_layer = 1
	body.collision_mask = 1
	body.position = aabb.get_center()
	_scene.add_child(body)
	var cs := CollisionShape3D.new()
	cs.name = "BakeDoorObstacle_Shape"
	var bs := BoxShape3D.new()
	bs.size = Vector3(maxf(aabb.size.x, 0.20), maxf(aabb.size.y, 0.20), maxf(aabb.size.z, 0.20))
	cs.shape = bs
	body.add_child(cs)


func _opening_world_aabb(node: Node) -> AABB:
	var found := AABB()
	var any := false
	var stack: Array[Node] = [node]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if n is CollisionShape3D:
			var cs := n as CollisionShape3D
			var shape: Shape3D = cs.shape
			if shape is BoxShape3D and cs.global_transform != null:
				var ext: Vector3 = (shape as BoxShape3D).size * 0.5
				var xf: Transform3D = cs.global_transform
				for sx: float in [-1.0, 1.0]:
					for sy: float in [-1.0, 1.0]:
						for sz: float in [-1.0, 1.0]:
							var corner: Vector3 = xf * Vector3(ext.x * sx, ext.y * sy, ext.z * sz)
							if not any:
								found = AABB(corner, Vector3.ZERO)
								any = true
							else:
								found = found.expand(corner)
		if n != node:
			pass
		for ch: Node in n.get_children():
			stack.append(ch)
	if not any:
		return AABB()
	return found


func _block_apt201_slab_seam() -> void:
	# The leak is not a door. Spawn (-9.35, 4.25, 6.20) and the Room1A spool (-6.15, 0.98, 7.25)
	# share an XZ footprint: Tech_Apartment_Upper's slab (about x -13.6..-5.4, z 2.7..8.5, top y 4.35)
	# sits on the mezzanine deck directly above the laundry shelf. With every field link off, the
	# path stays on that slab and still ends 0.55 m away horizontally, which the QA counts as a reach.
	# There is no Hatch_D204 collider in the sector (the emitter panel is an empty marker on the
	# alcove tool wall). A thin bake-only wall across the slab, x -13.95..-5.45 at z 6.20, meets the
	# west shell and the Apt201 east wall. The reachable mesh stops south of it, more than 1 m from
	# the spool. Nothing north of the seam is an interactable.
	if _scene == null:
		return
	var body := StaticBody3D.new()
	body.name = "BakeSlabGapObstacle"
	body.collision_layer = 1
	body.collision_mask = 1
	body.position = Vector3(-9.70, 4.75, 6.20)
	_scene.add_child(body)
	var cs := CollisionShape3D.new()
	cs.name = "BakeSlabGapObstacle_Shape"
	var bs := BoxShape3D.new()
	bs.size = Vector3(8.50, 1.50, 0.10)
	cs.shape = bs
	body.add_child(cs)


func _exclude_furniture_and_roof() -> void:
	# Name or group on this node only. Do not strip a parent and take the floors with it.
	if _scene == null:
		return
	var stack: Array[Node] = [_scene]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		if _is_furniture_or_roof(n) and not _is_walkable_floor_name(n):
			if n is CollisionObject3D:
				_drop_collision_node(n)
				continue
			_drop_direct_collision_children(n)
		for ch: Node in n.get_children():
			stack.append(ch)


func _is_walkable_floor_name(n: Node) -> bool:
	var nm := String(n.name).to_lower()
	return nm.contains("floor") or nm.contains("deck") or nm.contains("promenade") or nm.contains("stair") or nm.contains("walkway") or nm.contains("ground")


func _drop_direct_collision_children(n: Node) -> void:
	var cols: Array[Node] = []
	for ch: Node in n.get_children():
		if ch is CollisionObject3D or ch is CollisionShape3D:
			cols.append(ch)
	for c: Node in cols:
		_drop_collision_node(c)


func _is_furniture_or_roof(n: Node) -> bool:
	if n.is_in_group("furniture") or n.is_in_group("roof") or n.is_in_group("navmesh_exclude"):
		return true
	var nm := String(n.name).to_lower()
	for bit: String in _SKIP_NAME_BITS:
		if nm.contains(bit):
			return true
	return false


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


func _drop_far_x_polygons(navmesh: NavigationMesh) -> void:
	# Gravity-ring islands sit around x 143..157. Drop any polygon that reaches past x 100.
	var n := navmesh.get_polygon_count()
	if n == 0:
		return
	var verts := navmesh.get_vertices()
	var kept: Array[PackedInt32Array] = []
	var dropped := false
	for i: int in n:
		var poly := navmesh.get_polygon(i)
		var far := false
		for vi: int in poly:
			if verts[vi].x > 100.0:
				far = true
				break
		if far:
			dropped = true
		else:
			kept.append(poly)
	if not dropped:
		return
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
