## Rook r7 (2026-11-11): Tennis Tower (Strip 5) cylinder-drop loader.
## Builds the whole tower under this node from res://assets/models/tt_tower_manifest.json, in BUILDING coords
## (X axial, Z across, Y up; origin = SW corner, F1 floor top = y 0). Same runtime GLTFDocument path as
## preface_playable_area.gd (_load_glb_scene), so no .import files are needed. *-colonly / *-convcolonly mesh nodes
## become hidden-mesh StaticBody3D trimesh / convex colliders (layer 1). One cached template per GLB, duplicated per instance.
## Placing it in the drum: see design/tennis_tower_handoff/CYLINDER_DROP.md (drop_transform() below gives the Strip 5 pose).
class_name TennisTowerLoader
extends Node3D

@export var manifest_path: String = "res://assets/models/tt_tower_manifest.json"
@export var build_on_ready: bool = true
@export var build_colliders: bool = true
## Optional: apply the Strip 5 drum pose on ready (otherwise the parent supplies it).
@export var apply_drop_transform: bool = false
@export var axial_offset: float = -100.0

signal tower_built(stats: Dictionary)

var stats: Dictionary = {}
var _tmpl: Dictionary = {}
var _tag_roots: Dictionary = {}


## World pose of the building origin for the walkable drum in preface_playable_area.gd
## (DRUM_FLOOR_R 200, DRUM_AXIS_Y 200.12, DRUM_AXIS_Z -1.25, strip k at alpha (k - 4) * 36 deg).
## Strip 5 local: x = 60 + X (axial), z = -40 + Z (across), F1 above the strip-centreline hull. f1_hd 4.0408 = R - sqrt(R^2 - 40^2):
## the true-circle value that keeps the S threshold flush (the spec parabola p(Z) gives 4.0, which leaves the S door 40.8 mm under the floor).
static func drop_transform(axis_y: float = 200.12, axis_z: float = -1.25, r: float = 200.0, strip: int = 5,
		axial_off: float = -100.0, strip_x0: float = 60.0, strip_z0: float = -40.0, f1_hd: float = 4.0408) -> Transform3D:
	var a: float = deg_to_rad(float(strip - 4) * 36.0)
	var up: Vector3 = Vector3(0.0, cos(a), -sin(a))
	var tan_v: Vector3 = Vector3(0.0, sin(a), cos(a))
	var centre: Vector3 = Vector3(strip_x0 + axial_off, axis_y - r * cos(a), axis_z + r * sin(a))
	return Transform3D(Basis(Vector3.RIGHT, up, tan_v), centre + tan_v * strip_z0 + up * f1_hd)


func _ready() -> void:
	if apply_drop_transform:
		transform = drop_transform(200.12, -1.25, 200.0, 5, axial_offset)
	if build_on_ready:
		build()


func build() -> Dictionary:
	var t0: int = Time.get_ticks_msec()
	var txt: String = FileAccess.get_file_as_string(manifest_path)
	var man: Variant = JSON.parse_string(txt)
	stats = {"placed": 0, "missing": [], "glbs": 0, "meshes": 0, "tris": 0, "colliders": 0}
	if typeof(man) != TYPE_DICTIONARY:
		push_error("tennis_tower_loader: cannot read " + manifest_path)
		return stats
	for rec: Variant in (man as Dictionary)["placements"]:
		var d: Dictionary = rec as Dictionary
		var path: String = String(d["glb"])
		var tm: Node3D = _template(path)
		if tm == null:
			if not (stats["missing"] as Array).has(path):
				(stats["missing"] as Array).append(path)
			continue
		var inst: Node3D = tm.duplicate() as Node3D
		var pa: Array = d["p"] as Array
		inst.position = Vector3(float(pa[0]), float(pa[1]), float(pa[2]))
		inst.rotation_degrees = Vector3(0.0, float(d["yaw"]), 0.0)
		inst.name = "%s_%d" % [String(d["asset"]), int(stats["placed"])]
		_tag_root(String(d["tag"])).add_child(inst)
		stats["placed"] = int(stats["placed"]) + 1
	_count(self)
	stats["ms"] = Time.get_ticks_msec() - t0
	tower_built.emit(stats)
	return stats


func _exit_tree() -> void:
	for k: Variant in _tmpl.keys():
		var t: Variant = _tmpl[k]
		if t != null and is_instance_valid(t):
			(t as Node).free()
	_tmpl.clear()


func _tag_root(tag: String) -> Node3D:
	if not _tag_roots.has(tag):
		var n: Node3D = Node3D.new()
		n.name = "Tag_" + tag
		add_child(n)
		_tag_roots[tag] = n
	return _tag_roots[tag] as Node3D


func _template(path: String) -> Node3D:
	if _tmpl.has(path):
		return _tmpl[path] as Node3D
	var tm: Node3D = null
	if FileAccess.file_exists(path):
		var doc: GLTFDocument = GLTFDocument.new()
		var st: GLTFState = GLTFState.new()
		if doc.append_from_file(path, st) == OK:
			var n: Node = doc.generate_scene(st)
			if n is Node3D:
				tm = n as Node3D
				_make_colliders(tm)
			elif n != null:
				n.free()
	_tmpl[path] = tm
	if tm != null:
		stats["glbs"] = int(stats["glbs"]) + 1
	return tm


func _make_colliders(root_n: Node3D) -> void:
	var stack: Array[Node] = [root_n]
	var cols: Array[MeshInstance3D] = []
	while not stack.is_empty():
		var c: Node = stack.pop_back()
		if c is MeshInstance3D and String(c.name).to_lower().contains("colonly"):
			cols.append(c as MeshInstance3D)
		for ch: Node in c.get_children():
			stack.append(ch)
	for mi: MeshInstance3D in cols:
		var holder: Node = mi.get_parent()
		var nm: String = String(mi.name)
		mi.visible = false
		if not build_colliders or mi.mesh == null or holder == null:
			if holder != null:
				holder.remove_child(mi)
			mi.free()
			continue
		var faces: PackedVector3Array = mi.mesh.get_faces()
		holder.remove_child(mi)
		if faces.size() >= 3:
			var body: StaticBody3D = StaticBody3D.new()
			body.name = nm
			body.collision_layer = 1
			body.collision_mask = 1
			body.transform = mi.transform
			var cs: CollisionShape3D = CollisionShape3D.new()
			if nm.to_lower().contains("convcolonly"):
				var cv: ConvexPolygonShape3D = ConvexPolygonShape3D.new()
				cv.points = faces
				cs.shape = cv
			else:
				var cc: ConcavePolygonShape3D = ConcavePolygonShape3D.new()
				cc.data = faces
				cc.backface_collision = true
				cs.shape = cc
			body.add_child(cs)
			holder.add_child(body)
			body.owner = root_n
			cs.owner = root_n
		mi.free()


func _count(n: Node) -> void:
	if n is MeshInstance3D and (n as MeshInstance3D).visible and (n as MeshInstance3D).mesh != null:
		var m: Mesh = (n as MeshInstance3D).mesh
		stats["meshes"] = int(stats["meshes"]) + m.get_surface_count()
		for s: int in range(m.get_surface_count()):
			var a: Array = m.surface_get_arrays(s)
			var idx: Variant = a[Mesh.ARRAY_INDEX]
			if idx != null and (idx as PackedInt32Array).size() > 0:
				stats["tris"] = int(stats["tris"]) + (idx as PackedInt32Array).size() / 3
			else:
				stats["tris"] = int(stats["tris"]) + (a[Mesh.ARRAY_VERTEX] as PackedVector3Array).size() / 3
	elif n is CollisionShape3D:
		stats["colliders"] = int(stats["colliders"]) + 1
	for ch: Node in n.get_children():
		_count(ch)
