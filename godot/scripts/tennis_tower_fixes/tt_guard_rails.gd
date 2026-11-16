extends RefCounted
## Deterministic guard-rail list (tt_guard_rails.json) plus the runtime mesh.
## Rails are 1.07 m, one merged mesh and one body per floor. No shadows.

const JSON_PATH := "res://scripts/tennis_tower_fixes/tt_guard_rails.json"
const LAYER := 1 | (1 << 18)
const HEIGHT := 1.07
const OFFSET := 0.06
const INSET := 0.20
const MIN_LEN := 0.40

static var _skip: RegEx


static func _ensure() -> void:
	if _skip != null:
		return
	_skip = RegEx.new()
	# Pools, stands, play towers and rink/axe boards stay out of this pass
	# (pools are pass C; rink/axe openings are Vance's).
	_skip.compile("(?i)(pool|leisure_river|leisure_deck|leisure_foot|leisure_splash|dive|splash|bleach|play_tower|toddler|swing|stand|tier|rink|axe_)")


static func compile(drops: Array) -> Array:
	_ensure()
	var groups: Dictionary = {}
	for e_v in drops:
		var e: Array = e_v as Array
		if not _keep(e):
			continue
		var x: float = float(e[0])
		var z: float = float(e[1])
		var y: float = float(e[2])
		var dx: int = int(e[3])
		var dz: int = int(e[4])
		var yb: float = snapped(y, 0.05)
		var piece: Dictionary
		var key: String
		if dx != 0:
			var xr: float = snapped(x + float(dx) * 0.25, 0.001)
			key = "Z|%.3f|%.2f|%d" % [xr, yb, 1 if dx > 0 else 0]
			piece = {"t0": z - 0.25, "t1": z + 0.25, "rail": xr, "axis": "z", "y": y,
				"nx": -dx, "nz": 0, "sup": String(e[7]), "low": String(e[8]), "drop": float(e[5]), "x": x, "z": z}
		else:
			var zr: float = snapped(z + float(dz) * 0.25, 0.001)
			key = "X|%.3f|%.2f|%d" % [zr, yb, 1 if dz > 0 else 0]
			piece = {"t0": x - 0.25, "t1": x + 0.25, "rail": zr, "axis": "x", "y": y,
				"nx": 0, "nz": -dz, "sup": String(e[7]), "low": String(e[8]), "drop": float(e[5]), "x": x, "z": z}
		if not groups.has(key):
			groups[key] = []
		(groups[key] as Array).append(piece)
	var merged: Array = []
	var keys: Array = groups.keys()
	keys.sort()
	for k_v in keys:
		var arr: Array = groups[k_v]
		arr.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return float(a["t0"]) < float(b["t0"]))
		var cur: Dictionary = (arr[0] as Dictionary).duplicate()
		for i: int in range(1, arr.size()):
			var p: Dictionary = arr[i]
			if float(p["t0"]) <= float(cur["t1"]) + 0.05:
				cur["t1"] = maxf(float(cur["t1"]), float(p["t1"]))
				if float(p["drop"]) > float(cur["drop"]):
					cur["drop"] = p["drop"]
					cur["sup"] = p["sup"]
					cur["low"] = p["low"]
					cur["y"] = p["y"]
					cur["x"] = p["x"]
					cur["z"] = p["z"]
			else:
				merged.append(cur)
				cur = p.duplicate()
		merged.append(cur)
	var out: Array = []
	var reasons: Dictionary = {}
	var reason_m: Dictionary = {}
	for m_v in merged:
		var m: Dictionary = m_v
		var spans: Array = _clip(float(m["t0"]), float(m["t1"]), m)
		for sp_v in spans:
			var sp: Array = sp_v
			var a: float = float(sp[0]) + INSET
			var b: float = float(sp[1]) - INSET
			if b - a < MIN_LEN:
				continue
			var y: float = float(m["y"])
			var x0: float
			var z0: float
			var x1: float
			var z1: float
			var mx: float
			var mz: float
			if String(m["axis"]) == "z":
				x0 = float(m["rail"])
				x1 = x0
				z0 = a
				z1 = b
				mx = x0
				mz = (a + b) * 0.5
			else:
				z0 = float(m["rail"])
				z1 = z0
				x0 = a
				x1 = b
				mx = (a + b) * 0.5
				mz = z0
			var reason: String = _reason(mx, mz, y, String(m["sup"]), String(m.get("low", "")), float(m["drop"]))
			if reason == "":
				continue
			var seg_l: float = Vector2(x1 - x0, z1 - z0).length()
			reasons[reason] = int(reasons.get(reason, 0)) + 1
			reason_m[reason] = float(reason_m.get(reason, 0.0)) + seg_l
			out.append({
				"floor": _floor_of(y),
				"x0": snapped(x0, 0.001), "z0": snapped(z0, 0.001),
				"x1": snapped(x1, 0.001), "z1": snapped(z1, 0.001),
				"y": snapped(y, 0.001), "height": HEIGHT,
				"nx": int(m["nx"]), "nz": int(m["nz"]),
				"reason": reason,
			})
	out.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
		if int(a["floor"]) != int(b["floor"]):
			return int(a["floor"]) < int(b["floor"])
		if float(a["y"]) != float(b["y"]):
			return float(a["y"]) < float(b["y"])
		if float(a["x0"]) != float(b["x0"]):
			return float(a["x0"]) < float(b["x0"])
		if float(a["z0"]) != float(b["z0"]):
			return float(a["z0"]) < float(b["z0"])
		if float(a["x1"]) != float(b["x1"]):
			return float(a["x1"]) < float(b["x1"])
		return float(a["z1"]) < float(b["z1"])
	)
	for i2: int in range(out.size()):
		(out[i2] as Dictionary)["id"] = "c%04d" % (i2 + 1)
	print("[TT] guard gen reasons %s metres %s" % [str(reasons), str(reason_m)])
	return out


static func write_segments(segs: Array) -> void:
	var payload: Dictionary = {"generated": "tt_guard_gen", "segments": segs}
	var f: FileAccess = FileAccess.open(JSON_PATH, FileAccess.WRITE)
	if f == null:
		push_error("[TT] cannot write " + JSON_PATH)
		return
	f.store_string(JSON.stringify(payload, "\t"))
	f.close()
	print("[TT] guard gen wrote %s segments=%d" % [JSON_PATH, segs.size()])


static func run(tower: Node3D) -> Dictionary:
	var segs: Array = _load()
	var old: Node = tower.get_node_or_null("TTFix_Guards")
	if old != null:
		old.free()
	var length: float = 0.0
	if not segs.is_empty():
		var root: Node3D = Node3D.new()
		root.name = "TTFix_Guards"
		tower.add_child(root)
		var by: Dictionary = {1: [], 2: [], 3: []}
		for s_v in segs:
			var s: Dictionary = s_v
			var fl: int = int(s.get("floor", 1))
			if not by.has(fl):
				by[fl] = []
			(by[fl] as Array).append(s)
			length += Vector2(float(s["x1"]) - float(s["x0"]), float(s["z1"]) - float(s["z0"])).length()
		for fl2: int in [1, 2, 3]:
			var list: Array = by[fl2]
			if list.is_empty():
				continue
			_build_floor(root, fl2, list)
	print("[TT] guard rails segments=%d length_m=%.1f" % [segs.size(), length])
	return {"segments": segs.size(), "length_m": length}


static func _load() -> Array:
	if not FileAccess.file_exists(JSON_PATH):
		push_warning("[TT] guard rail json missing")
		return []
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(JSON_PATH))
	if typeof(parsed) != TYPE_DICTIONARY:
		return []
	var segs: Variant = (parsed as Dictionary).get("segments", [])
	return segs if segs is Array else []


static func _keep(e: Array) -> bool:
	return _region(float(e[0]), float(e[1]), float(e[2]), String(e[7]), String(e[8]), float(e[5])) != ""


static func _reason(x: float, z: float, y: float, sup: String, low: String, drop: float) -> String:
	return _region(x, z, y, sup, low, drop)


## Rails only on the audit drops Rook/Vance have not already raised to 1.0 m.
## The generic furniture/terrace "drop" set is not a rail.
static func _region(x: float, z: float, y: float, sup: String, low: String, drop: float) -> String:
	var s: String = sup.to_lower()
	var lo: String = low.to_lower()
	var blob: String = s + "|" + lo
	if _skip.search(blob) != null:
		return ""
	# Exterior drum ramps and grand stairs stay clear. Their own cheeks guard them.
	if blob.contains("struct_stair") or blob.contains("struct_ramp") or blob.contains("ramp_sw") or blob.contains("ramp_nw") or blob.contains("ramp_e"):
		return ""
	if drop < 0.5:
		return ""
	# TTQA-051: cccb5fd infilled F2 X 57..58 beside b977. That slot is floor, not a drop.
	if y >= 5.5 and y <= 6.8 and x >= 56.7 and x <= 58.05 and z >= 2.5 and z <= 13.3:
		return ""
	var reason: String = ""
	if y > 11.0 and z >= 1.8 and z <= 11.2 and ((x >= 56.5 and x <= 64.5) or (x >= 85.0 and x <= 92.5)):
		reason = "track_stairwell"
	elif y >= 5.2 and y <= 7.6 and x >= -12.2 and x <= -5.8 and z >= 64.0 and z <= 71.5:
		reason = "gallery_edge"
	elif y >= 5.2 and y <= 8.4 and x >= 18.0 and x <= 27.0 and z >= 49.5 and z <= 63.5:
		reason = "f2_brg_bridge"
	elif y >= 5.4 and y <= 7.2 and x >= 55.4 and x <= 58.8 and z >= 2.2 and z <= 13.8:
		reason = "slab_b977"
	elif x >= 126.0 and x <= 135.0 and z >= 67.0 and z <= 80.0 and y >= 5.2 and y <= 7.8:
		reason = "slab_opening"
	elif x >= 126.0 and x <= 135.0 and z >= 67.0 and z <= 80.0 and y >= 11.2 and y <= 13.6:
		reason = "slab_opening"
	elif blob.contains("feature_stair") and y < 8.5 and drop >= 1.0:
		reason = "arcade_feature_stair"
	elif (s.contains("stair") or lo.contains("stair")) and not s.contains("struct_stair"):
		reason = "stair_landing"
	if reason == "":
		return ""
	if reason == "stair_landing" or reason == "arcade_feature_stair":
		if drop < 1.0:
			return ""
		if drop < 1.25 and (lo.contains("ramp") or lo.contains("flight") or lo.contains("landing") or lo.contains("tread")):
			return ""
	return reason


static func _floor_of(y: float) -> int:
	if y < 4.0:
		return 1
	if y < 10.0:
		return 2
	return 3


static func _gaps() -> Array:
	# S threshold rail sits at z=-1.25 (x 69.45..74.55, y 0.02), 5 cm south of
	# the old z=-1.2 cut, and blocks the door walk. Side returns at x=68.25
	# and x=75.75 stay, so the drop beside the opening is still guarded.
	return [
		[68.5, 75.5, -1.60, 1.5, -0.5, 2.5],
		[68.5, 75.5, 78.3, 81.2, -0.5, 2.5],
		[139.5, 142.5, 34.5, 40.5, -0.5, 2.5],
		[-15.0, -11.0, 17.0, 62.0, -0.5, 2.5],
		[30.5, 32.6, 15.6, 19.7, -1.0, 20.0],
		[37.6, 39.8, 15.6, 19.7, -1.0, 20.0],
		# NE plant-stack staff door (locked, but the opening must stay a door).
		[131.15, 132.85, 68.55, 69.55, 5.0, 13.8],
		# Rink player gates and the zamboni gate. Leaves park open.
		[65.6, 67.4, 51.6, 53.4, 5.0, 8.0],
		[76.6, 78.4, 51.6, 53.4, 5.0, 8.0],
		[101.8, 103.2, 34.5, 38.2, 5.0, 8.0],
	]


static func _clip(t0: float, t1: float, m: Dictionary) -> Array:
	var spans: Array = [[t0, t1]]
	var y: float = float(m["y"])
	var axis: String = String(m["axis"])
	var rail: float = float(m["rail"])
	for g_v in _gaps():
		var g: Array = g_v
		if y < float(g[4]) or y > float(g[5]):
			continue
		var cut0: float
		var cut1: float
		if axis == "x":
			if rail < float(g[2]) or rail > float(g[3]):
				continue
			cut0 = float(g[0])
			cut1 = float(g[1])
		else:
			if rail < float(g[0]) or rail > float(g[1]):
				continue
			cut0 = float(g[2])
			cut1 = float(g[3])
		var next: Array = []
		for sp_v in spans:
			var sp: Array = sp_v
			var a: float = float(sp[0])
			var b: float = float(sp[1])
			if cut1 <= a or cut0 >= b:
				next.append([a, b])
			else:
				if cut0 > a:
					next.append([a, cut0])
				if cut1 < b:
					next.append([cut1, b])
		spans = next
	return spans


static func _build_floor(root: Node3D, floor_n: int, segs: Array) -> void:
	var glass: SurfaceTool = SurfaceTool.new()
	var metal: SurfaceTool = SurfaceTool.new()
	var cyan: SurfaceTool = SurfaceTool.new()
	glass.begin(Mesh.PRIMITIVE_TRIANGLES)
	metal.begin(Mesh.PRIMITIVE_TRIANGLES)
	cyan.begin(Mesh.PRIMITIVE_TRIANGLES)
	var ng: int = 0
	var nm: int = 0
	var nc: int = 0
	var body: StaticBody3D = StaticBody3D.new()
	body.name = "Guards_F%d" % floor_n
	body.collision_layer = LAYER
	body.collision_mask = 1
	for s_v in segs:
		var s: Dictionary = s_v
		var p0: Vector3 = Vector3(float(s["x0"]), float(s["y"]), float(s["z0"]))
		var p1: Vector3 = Vector3(float(s["x1"]), float(s["y"]), float(s["z1"]))
		var delta: Vector3 = p1 - p0
		var length: float = delta.length()
		if length < 0.05:
			continue
		var along: Vector3 = delta / length
		var normal: Vector3 = Vector3(float(s["nx"]), 0.0, float(s["nz"]))
		if normal.length_squared() < 0.01:
			normal = Vector3(-along.z, 0.0, along.x)
		normal = normal.normalized()
		along = along - normal * along.dot(normal)
		if along.length_squared() < 0.0001:
			continue
		along = along.normalized()
		var mid: Vector3 = (p0 + p1) * 0.5 + normal * OFFSET
		var up: Vector3 = Vector3.UP
		_emit_box(glass, mid + up * 0.55, along, up, normal, length, 0.90, 0.015)
		ng += 1
		_emit_box(metal, mid + up * 1.04, along, up, normal, length, 0.06, 0.045)
		_emit_box(metal, mid + up * 0.05, along, up, normal, length, 0.10, 0.06)
		nm += 2
		_emit_box(cyan, mid + up * 1.062 + normal * 0.012, along, up, normal, length, 0.014, 0.012)
		nc += 1
		var cs: CollisionShape3D = CollisionShape3D.new()
		var box: BoxShape3D = BoxShape3D.new()
		box.size = Vector3(length, HEIGHT, 0.08)
		cs.shape = box
		var basis: Basis = Basis()
		basis.x = along
		basis.y = up
		basis.z = normal
		cs.transform = Transform3D(basis, mid + up * (HEIGHT * 0.5))
		body.add_child(cs)
	if ng == 0:
		return
	var mesh: ArrayMesh = ArrayMesh.new()
	_add_surface(mesh, glass, _mat_glass())
	if nm > 0:
		_add_surface(mesh, metal, _mat_metal())
	if nc > 0:
		_add_surface(mesh, cyan, _mat_cyan())
	var mi: MeshInstance3D = MeshInstance3D.new()
	mi.name = "GuardMesh_F%d" % floor_n
	mi.mesh = mesh
	mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	mi.set_meta("tt_no_batch", true)
	root.add_child(mi)
	root.add_child(body)


static func _add_surface(mesh: ArrayMesh, st: SurfaceTool, mat: Material) -> void:
	st.generate_normals()
	var tmp: ArrayMesh = st.commit()
	if tmp == null or tmp.get_surface_count() == 0:
		return
	mesh.add_surface_from_arrays(Mesh.PRIMITIVE_TRIANGLES, tmp.surface_get_arrays(0))
	mesh.surface_set_material(mesh.get_surface_count() - 1, mat)


static func _emit_box(st: SurfaceTool, center: Vector3, ax: Vector3, ay: Vector3, az: Vector3, sx: float, sy: float, sz: float) -> void:
	var hx: Vector3 = ax * (sx * 0.5)
	var hy: Vector3 = ay * (sy * 0.5)
	var hz: Vector3 = az * (sz * 0.5)
	var p: Array[Vector3] = []
	p.resize(8)
	for i: int in range(8):
		var sxn: float = 1.0 if (i & 1) != 0 else -1.0
		var syn: float = 1.0 if (i & 2) != 0 else -1.0
		var szn: float = 1.0 if (i & 4) != 0 else -1.0
		p[i] = center + hx * sxn + hy * syn + hz * szn
	_quad(st, p[1], p[5], p[7], p[3])
	_quad(st, p[4], p[0], p[2], p[6])
	_quad(st, p[2], p[3], p[7], p[6])
	_quad(st, p[0], p[4], p[5], p[1])
	_quad(st, p[5], p[4], p[6], p[7])
	_quad(st, p[0], p[1], p[3], p[2])


static func _quad(st: SurfaceTool, a: Vector3, b: Vector3, c: Vector3, d: Vector3) -> void:
	st.add_vertex(a)
	st.add_vertex(b)
	st.add_vertex(c)
	st.add_vertex(a)
	st.add_vertex(c)
	st.add_vertex(d)


static func _mat_glass() -> StandardMaterial3D:
	var m: StandardMaterial3D = StandardMaterial3D.new()
	m.albedo_color = Color(0.75, 0.86, 0.90, 0.35)
	m.roughness = 0.15
	m.metallic = 0.0
	m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	m.cull_mode = BaseMaterial3D.CULL_DISABLED
	return m


static func _mat_metal() -> StandardMaterial3D:
	var m: StandardMaterial3D = StandardMaterial3D.new()
	m.albedo_color = Color(0.78, 0.80, 0.82, 1.0)
	m.metallic = 0.85
	m.roughness = 0.35
	m.cull_mode = BaseMaterial3D.CULL_DISABLED
	return m


static func _mat_cyan() -> StandardMaterial3D:
	var m: StandardMaterial3D = StandardMaterial3D.new()
	m.albedo_color = Color(0.25, 0.85, 0.95, 1.0)
	m.emission_enabled = true
	m.emission = Color(0.20, 0.90, 1.0, 1.0)
	m.emission_energy_multiplier = 0.35
	m.roughness = 0.25
	m.metallic = 0.4
	m.cull_mode = BaseMaterial3D.CULL_DISABLED
	return m
