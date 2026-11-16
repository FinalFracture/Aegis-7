extends RefCounted
## TTQA-013. Added glow only: S/N door frames, drum-floor paths, and small cues
## at Rook's ramp/stair feet and the E door. No colliders, no shadowed lights.
## One merged unshaded mesh so the Intel UHD 605 pays a single extra draw.

const DRUM_K := 195.9592
const L2 := -1.118
const PATH_M := 13.0
const FZ := -0.74


static func run(tower: Node3D) -> void:
	var st := SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)
	var tris := 0
	var doors := _find_doors(tower)
	tris += _frame(st, doors.get("S"), true)
	tris += _frame(st, doors.get("N"), true)
	tris += _frame(st, doors.get("E"), false)
	tris += _path_z(st, 72.0, -3.2, -1.0)
	tris += _path_z(st, 72.0, 82.2, 1.0)
	if doors.has("E"):
		tris += _e_dots(st, doors["E"])
	tris += _foot_cues(st)
	if tris == 0:
		print("[TT] wayfinding tris=0")
		return
	st.generate_normals()
	var mesh := st.commit()
	mesh.surface_set_material(0, _material())
	var mi := MeshInstance3D.new()
	mi.name = "TT_Wayfinding_Glow"
	mi.mesh = mesh
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mi.gi_mode = GeometryInstance3D.GI_MODE_DISABLED
	mi.set_meta("tt_no_batch", true)
	var root := Node3D.new()
	root.name = "TT_Wayfinding"
	root.set_meta("tt_no_batch", true)
	root.add_child(mi)
	tower.add_child(root)
	print("[TT] wayfinding tris=%d doors=%s paths=13m cues=ramps+stairs+E (no lights, no colliders)" % [tris, str(doors.keys())])


static func _drum_y(z: float) -> float:
	return DRUM_K - sqrt(maxf(0.0, 40000.0 - (z - 40.0) * (z - 40.0)))


static func _find_doors(tower: Node3D) -> Dictionary:
	var out := {}
	var stack: Array[Node] = [tower]
	while not stack.is_empty():
		var n: Node = stack.pop_back()
		for ch in n.get_children():
			stack.append(ch)
		if not (n is Node3D):
			continue
		var nm := String(n.name)
		var side := ""
		if nm.begins_with("tt_secondary_entrance_s"):
			side = "S"
		elif nm.begins_with("tt_secondary_entrance_n"):
			side = "N"
		elif nm.begins_with("tt_secondary_entrance_e"):
			side = "E"
		if side != "":
			out[side] = n as Node3D
	return out


static func _frame(st: SurfaceTool, door: Node3D, full: bool) -> int:
	if door == null:
		return 0
	# Tag_* parents sit at the tower origin, so the instance transform is building space.
	var xf := door.transform
	var n := 0
	if full:
		n += _box(st, xf, Vector3(-3.92, 3.05, FZ), Vector3(0.10, 5.90, 0.05))
		n += _box(st, xf, Vector3(3.92, 3.05, FZ), Vector3(0.10, 5.90, 0.05))
		n += _box(st, xf, Vector3(0.0, 5.95, FZ), Vector3(7.94, 0.10, 0.05))
		n += _box(st, xf, Vector3(0.0, 2.52, FZ + 0.03), Vector3(7.50, 0.08, 0.04))
		n += _box(st, xf, Vector3(0.0, 0.025, FZ), Vector3(7.60, 0.02, 0.06))
	else:
		n += _box(st, xf, Vector3(-3.70, 1.35, FZ), Vector3(0.08, 2.40, 0.045))
		n += _box(st, xf, Vector3(3.70, 1.35, FZ), Vector3(0.08, 2.40, 0.045))
		n += _box(st, xf, Vector3(0.0, 2.52, FZ), Vector3(7.48, 0.08, 0.045))
	return n


static func _path_z(st: SurfaceTool, x: float, z0: float, dir: float) -> int:
	var n := 0
	var z := z0
	var left := PATH_M
	while left > 0.2:
		var step := minf(0.85, left)
		var z1 := z + dir * step
		var a := Vector3(x, _drum_y(z) + 0.03, z)
		var b := Vector3(x, _drum_y(z1) + 0.03, z1)
		n += _along(st, a, b, 0.09, 0.016)
		n += _box(st, Transform3D.IDENTITY, a + Vector3(0.0, 0.02, 0.0), Vector3(0.22, 0.028, 0.22))
		z = z1
		left -= step
	return n


static func _e_dots(st: SurfaceTool, door: Node3D) -> int:
	var n := 0
	for i in range(5):
		var p: Vector3 = door.transform * Vector3(0.0, 0.03, 2.4 + float(i) * 0.85)
		n += _box(st, Transform3D.IDENTITY, p, Vector3(0.20, 0.025, 0.20))
	return n


static func _foot_cues(st: SurfaceTool) -> int:
	var n := 0
	var lf := _drum_y(8.3) + 0.003
	var xe := -41.92 + (L2 - lf) * 12.0
	var xf := xe + 1.5
	var lfil := maxf((lf - _drum_y(9.35) - 0.003) * 20.0, 0.2)
	var sw_x := xf + lfil + 0.7
	n += _cue_x(st, sw_x, 9.35, 1.0)
	n += _cue_x(st, sw_x, 70.65, 1.0)
	n += _cue_x(st, 128.0 - sw_x, 9.35, -1.0)
	# W stair pad ends X -73.8; E stair pad ends X 181.3. Cue sits on the drum past the pad.
	n += _cue_z(st, -74.8, 38.0)
	n += _cue_z(st, 182.3, 38.0)
	return n


static func _cue_x(st: SurfaceTool, x: float, z: float, dir: float) -> int:
	var n := 0
	for i in range(4):
		var px := x + dir * float(i) * 0.45
		n += _box(st, Transform3D.IDENTITY, Vector3(px, _drum_y(z) + 0.035, z), Vector3(0.28, 0.025, 0.16))
	return n


static func _cue_z(st: SurfaceTool, x: float, z: float) -> int:
	var n := 0
	for i in range(4):
		var pz := z - 0.7 + float(i) * 0.45
		n += _box(st, Transform3D.IDENTITY, Vector3(x, _drum_y(pz) + 0.035, pz), Vector3(0.16, 0.025, 0.28))
	return n


static func _along(st: SurfaceTool, a: Vector3, b: Vector3, width: float, thick: float) -> int:
	var along := b - a
	if along.length() < 0.05:
		return 0
	var z := along.normalized()
	var x := Vector3.UP.cross(z)
	if x.length() < 0.2:
		x = Vector3.RIGHT
	x = x.normalized()
	var y := z.cross(x).normalized()
	var xf := Transform3D(Basis(x, y, z), (a + b) * 0.5)
	return _box(st, xf, Vector3.ZERO, Vector3(width, thick, along.length()))


static func _box(st: SurfaceTool, xf: Transform3D, center: Vector3, size: Vector3) -> int:
	var hx := size.x * 0.5
	var hy := size.y * 0.5
	var hz := size.z * 0.5
	var raw: Array[Vector3] = [
		Vector3(-hx, -hy, -hz), Vector3(hx, -hy, -hz), Vector3(hx, hy, -hz), Vector3(-hx, hy, -hz),
		Vector3(-hx, -hy, hz), Vector3(hx, -hy, hz), Vector3(hx, hy, hz), Vector3(-hx, hy, hz),
	]
	var p: Array[Vector3] = []
	for v in raw:
		p.append(xf * (center + v))
	var faces: Array = [
		[0, 2, 1], [0, 3, 2],
		[4, 5, 6], [4, 6, 7],
		[0, 1, 5], [0, 5, 4],
		[1, 2, 6], [1, 6, 5],
		[2, 3, 7], [2, 7, 6],
		[3, 0, 4], [3, 4, 7],
	]
	for f in faces:
		st.add_vertex(p[int(f[0])])
		st.add_vertex(p[int(f[1])])
		st.add_vertex(p[int(f[2])])
	return 12


static func _material() -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.resource_name = "TT_Wayfinding"
	m.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
	m.albedo_color = Color(1.0, 0.78, 0.32, 1.0)
	m.emission_enabled = true
	m.emission = Color(1.0, 0.55, 0.10)
	m.emission_energy_multiplier = 3.5
	m.roughness = 0.4
	return m
