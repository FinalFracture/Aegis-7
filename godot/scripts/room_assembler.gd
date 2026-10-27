class_name RoomAssembler
extends Node3D
## RoomAssembler for Cylinder Hab-7: Living Quarters (4.0m W x 5.0m D x 3.0m H)
## Assembles Rook's medium-detail contoured .glb models from res://../assets/glb/
## and binds Sloane's PBR & emissive textures from res://../assets/textures/.
## Also constructs the curved 800m x 400m (R=200m) O'Neill Cylinder exterior vista arc outside the North viewport.

const EXTERNAL_GLB_DIR := "res://../assets/glb"
const RES_GLB_DIR := "res://../assets/glb"
const DESIGN_SPEC_PATH := "res://../design/living_quarters_spec.md"

const ROOM_WIDTH := 4.0   # X: -2.0 to +2.0
const ROOM_DEPTH := 5.0   # Z: -2.5 to +2.5
const ROOM_HEIGHT := 3.0  # Y:  0.0 to +3.0

var material_loader: MaterialLoader
var _shell_container: Node3D
var _props_container: Node3D
var _vista_container: Node3D
var _loaded_glb_files: Array[String] = []

const PROP_PLACEMENTS := {
	"room_shell": {
		"file": "room_shell.glb",
		"keywords": ["room_shell", "shell", "living_quarters_shell"],
		"pos": Vector3(0.0, 0.0, 0.0),
		"rot_y_deg": 0.0,
		"is_shell": true
	},
	"bunk_bed": {
		"file": "bunk_bed.glb",
		"keywords": ["bunk_bed", "bunk", "bed", "sleep_pod"],
		"pos": Vector3(-1.32, 0.0, -0.55),
		"rot_y_deg": 90.0,
		"is_shell": false
	},
	"retro_desk_crt": {
		"file": "retro_desk_crt.glb",
		"keywords": ["retro_desk_crt", "desk", "workstation", "crt"],
		"pos": Vector3(1.22, 0.0, -1.65),
		"rot_y_deg": -90.0,
		"is_shell": false
	},
	"wardrobe_locker": {
		"file": "wardrobe_locker.glb",
		"keywords": ["wardrobe_locker", "wardrobe", "locker", "storage"],
		"pos": Vector3(-1.52, 0.0, 1.45),
		"rot_y_deg": 90.0,
		"is_shell": false
	},
	"lounge_chair": {
		"file": "lounge_chair.glb",
		"keywords": ["lounge_chair", "armchair", "chair"],
		"pos": Vector3(1.18, 0.0, 0.65),
		"rot_y_deg": -125.0,
		"is_shell": false
	},
	"coffee_table": {
		"file": "coffee_table.glb",
		"keywords": ["coffee_table", "table"],
		"pos": Vector3(0.32, 0.0, 0.55),
		"rot_y_deg": 0.0,
		"is_shell": false
	},
	"floor_lamp": {
		"file": "floor_lamp.glb",
		"keywords": ["floor_lamp", "lamp"],
		"pos": Vector3(1.55, 0.0, 1.55),
		"rot_y_deg": -45.0,
		"is_shell": false
	},
	"area_rug": {
		"file": "area_rug.glb",
		"keywords": ["area_rug", "rug", "carpet"],
		"pos": Vector3(0.10, 0.006, 0.15),
		"rot_y_deg": 0.0,
		"is_shell": false
	},
	"hydro_planter": {
		"file": "hydro_planter.glb",
		"keywords": ["hydro_planter", "planter", "plant", "hydro"],
		"pos": Vector3(-0.65, 0.0, -2.05),
		"rot_y_deg": 15.0,
		"is_shell": false
	}
}


func _ready() -> void:
	material_loader = MaterialLoader.new()
	var tex_files: Array[String] = material_loader.get_discovered_files()
	print("[RoomAssembler] Discovered ", tex_files.size(), " texture(s) in assets/textures: ", tex_files)

	_shell_container = get_node_or_null("RoomShell") as Node3D
	if _shell_container == null:
		_shell_container = Node3D.new()
		_shell_container.name = "RoomShell"
		add_child(_shell_container)

	_props_container = get_node_or_null("FurnitureAndProps") as Node3D
	if _props_container == null:
		_props_container = Node3D.new()
		_props_container.name = "FurnitureAndProps"
		add_child(_props_container)

	_vista_container = get_node_or_null("ONeillExteriorVista") as Node3D
	if _vista_container == null:
		_vista_container = Node3D.new()
		_vista_container.name = "ONeillExteriorVista"
		add_child(_vista_container)

	# 1. Build the curved 800m x 400m (200m radius) O'Neill Cylinder Exterior Vista outside the North viewport (Z = -2.5m)
	_build_curved_oneill_vista()

	# 2. Check Sloane's design spec if present for any coordinate/lighting overrides
	var spec_overrides: Dictionary = _parse_design_spec()
	if not spec_overrides.is_empty():
		print("[RoomAssembler] Loaded layout overrides from design spec: ", spec_overrides.keys())

	# 3. Assemble or refresh all .glb models from res://../assets/glb/
	_assemble_glb_models(spec_overrides)


func _discover_glb_files() -> Array[String]:
	var glb_files: Array[String] = []
	for dir_path: String in [EXTERNAL_GLB_DIR, RES_GLB_DIR]:
		var dir: DirAccess = DirAccess.open(dir_path)
		if dir == null:
			continue
		dir.list_dir_begin()
		var fname: String = dir.get_next()
		while fname != "":
			if not dir.current_is_dir():
				var lower: String = fname.to_lower()
				if lower.ends_with(".glb") or lower.ends_with(".gltf"):
					if not glb_files.has(fname):
						glb_files.append(fname)
			fname = dir.get_next()
		dir.list_dir_end()
	glb_files.sort()
	return glb_files


func _load_glb_scene(filename: String) -> Node3D:
	var res_path: String = RES_GLB_DIR + "/" + filename
	var abs_path: String = EXTERNAL_GLB_DIR + "/" + filename

	# Prefer ResourceLoader when imported so Godot instantiates native ArrayMesh MeshInstance3D nodes
	if ResourceLoader.exists(res_path):
		var packed: Resource = ResourceLoader.load(res_path)
		if packed is PackedScene:
			var inst: Node = (packed as PackedScene).instantiate()
			if inst is Node3D:
				return inst as Node3D

	# Fallback to runtime GLTFDocument for unimported .glb files
	if FileAccess.file_exists(abs_path):
		var doc: GLTFDocument = GLTFDocument.new()
		var state: GLTFState = GLTFState.new()
		var err: Error = doc.append_from_file(abs_path, state)
		if err == OK:
			var generated: Node = doc.generate_scene(state)
			if generated is Node3D:
				return generated as Node3D

	return null


func _assemble_glb_models(spec_overrides: Dictionary) -> void:
	var glb_files: Array[String] = _discover_glb_files()
	print("[RoomAssembler] Discovered ", glb_files.size(), " .glb model(s) in assets/glb: ", glb_files)

	if glb_files.is_empty():
		push_warning("[RoomAssembler] No .glb files found in " + EXTERNAL_GLB_DIR)
		return

	# Check if the scene tree already has the GLB nodes from living_quarters.tscn
	var existing_nodes: Dictionary = {}
	for ch: Node in _shell_container.get_children():
		if ch is Node3D:
			existing_nodes[ch.name] = ch
	for ch: Node in _props_container.get_children():
		if ch is Node3D:
			existing_nodes[ch.name] = ch

	for fname: String in glb_files:
		var stem: String = fname.get_basename().to_lower()
		var node_name: String = "GLB_" + fname.get_basename()
		var matched_slot: String = _match_slot_for_stem(stem)
		var pos: Vector3 = Vector3.ZERO
		var rot_y: float = 0.0
		var is_shell: bool = false

		if matched_slot != "" and PROP_PLACEMENTS.has(matched_slot):
			var slot_info: Dictionary = PROP_PLACEMENTS[matched_slot]
			pos = slot_info["pos"] as Vector3
			rot_y = float(slot_info["rot_y_deg"])
			is_shell = bool(slot_info["is_shell"])

		if spec_overrides.has(stem):
			var ov: Dictionary = spec_overrides[stem]
			pos = ov.get("pos", pos) as Vector3
			rot_y = float(ov.get("rot_y_deg", rot_y))

		var node: Node3D = null
		if existing_nodes.has(node_name):
			node = existing_nodes[node_name] as Node3D
		else:
			node = _load_glb_scene(fname)
			if node == null:
				push_warning("[RoomAssembler] Failed to load GLB: " + fname)
				continue
			node.name = node_name
			if is_shell:
				_shell_container.add_child(node)
			else:
				_props_container.add_child(node)

		_loaded_glb_files.append(fname)
		node.position = pos
		node.rotation_degrees = Vector3(0.0, rot_y, 0.0)
		_bind_and_enhance_materials(node, stem, is_shell)

		if is_shell:
			print("[RoomAssembler] Ready Room Shell GLB: ", fname, " at ", pos)
		else:
			print("[RoomAssembler] Ready Prop GLB: ", fname, " -> slot '", matched_slot, "' at pos=", pos, " rot_y=", rot_y)


func _match_slot_for_stem(stem: String) -> String:
	var priority_order: Array[String] = [
		"room_shell",
		"bunk_bed",
		"retro_desk_crt",
		"wardrobe_locker",
		"lounge_chair",
		"coffee_table",
		"floor_lamp",
		"area_rug",
		"hydro_planter"
	]
	for slot: String in priority_order:
		var slot_dict: Dictionary = PROP_PLACEMENTS[slot]
		var kws: Array = slot_dict["keywords"] as Array
		for kw_var: Variant in kws:
			var kw: String = String(kw_var)
			if stem.contains(kw):
				return slot
	return ""


func _bind_and_enhance_materials(root: Node3D, _stem: String, is_shell: bool) -> void:
	var stack: Array[Node] = [root]
	while not stack.is_empty():
		var curr: Node = stack.pop_back()
		if curr is MeshInstance3D:
			var mi: MeshInstance3D = curr as MeshInstance3D
			var mname_lower: String = mi.name.to_lower()
			# Ensure structural collision slab underneath floor doesn't occlude Floor_ParquetDecking or area_rug
			if mname_lower.contains("structuralslab"):
				mi.position.y = -0.022
			if mi.mesh != null:
				mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_ON
				for s_idx: int in range(mi.mesh.get_surface_count()):
					var active_mat: Material = mi.get_active_material(s_idx)
					if active_mat is StandardMaterial3D:
						var smat: StandardMaterial3D = (active_mat as StandardMaterial3D).duplicate() as StandardMaterial3D
						var mat_name: String = smat.resource_name.to_lower()
						_upgrade_standard_material(smat, mat_name, mname_lower, is_shell)
						mi.set_surface_override_material(s_idx, smat)
		for ch: Node in curr.get_children():
			stack.append(ch)


func _upgrade_standard_material(smat: StandardMaterial3D, mname: String, mesh_name: String, is_shell: bool) -> void:
	if mname.contains("wallpaper") or mesh_name.contains("wallpaper"):
		var wall_mat: StandardMaterial3D = material_loader.get_surface_material("wallpaper")
		smat.albedo_texture = wall_mat.albedo_texture
		smat.roughness = 0.78
		smat.metallic = 0.02
		smat.cull_mode = BaseMaterial3D.CULL_DISABLED
		if is_shell:
			smat.uv1_scale = Vector3(3.0, 1.5, 1.0)
	elif mname.contains("wainscot") or mesh_name.contains("wainscot"):
		var wain_mat: StandardMaterial3D = material_loader.get_surface_material("wainscoting")
		smat.albedo_texture = wain_mat.albedo_texture
		smat.roughness = 0.48
		smat.metallic = 0.14
		smat.cull_mode = BaseMaterial3D.CULL_DISABLED
		if is_shell:
			smat.uv1_scale = Vector3(4.0, 1.0, 1.0)
	elif mname.contains("parquet") or mesh_name.contains("parquet"):
		var floor_mat: StandardMaterial3D = material_loader.get_surface_material("floor")
		smat.albedo_texture = floor_mat.albedo_texture
		smat.roughness = 0.42
		smat.metallic = 0.04
		smat.cull_mode = BaseMaterial3D.CULL_DISABLED
		if is_shell:
			smat.uv1_scale = Vector3(3.0, 4.0, 1.0)
	elif mname.contains("walnut"):
		var wood_mat: StandardMaterial3D = material_loader.get_surface_material("floor")
		smat.albedo_texture = wood_mat.albedo_texture
		smat.albedo_color = Color(0.86, 0.72, 0.58)
		smat.roughness = 0.40
		smat.metallic = 0.05
	elif mname.contains("brass"):
		var brass_mat: StandardMaterial3D = material_loader.get_surface_material("brass_trim")
		smat.albedo_texture = brass_mat.albedo_texture
		smat.albedo_color = Color(0.95, 0.82, 0.55)
		smat.metallic = 0.82
		smat.roughness = 0.28
	elif mname.contains("terracotta") or mname.contains("boucle"):
		var fab_mat: StandardMaterial3D = material_loader.get_surface_material("warm_fabric")
		smat.albedo_texture = fab_mat.albedo_texture
		smat.roughness = 0.84
	elif mname.contains("rug") or mesh_name.contains("wovenpatterntop"):
		var rug_mat: StandardMaterial3D = material_loader.get_surface_material("rug")
		smat.albedo_texture = rug_mat.albedo_texture
		smat.roughness = 0.90
		smat.cull_mode = BaseMaterial3D.CULL_DISABLED
	elif mname.contains("crt") or mname.contains("phosphor"):
		var crt_mat: StandardMaterial3D = material_loader.get_surface_material("crt_screen")
		smat.albedo_texture = crt_mat.albedo_texture
		smat.albedo_color = Color(1.0, 0.96, 0.88)
		smat.emission_enabled = false
		smat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
		smat.cull_mode = BaseMaterial3D.CULL_DISABLED
	elif mname.contains("emissive_warm") or mname.contains("warmamberlight"):
		smat.emission_enabled = true
		smat.emission = Color(1.0, 0.82, 0.52)
		smat.emission_energy_multiplier = 1.25
	elif mname.contains("mushroomshade"):
		smat.emission_enabled = true
		smat.emission = Color(1.0, 0.78, 0.44)
		smat.emission_energy_multiplier = 1.15
		smat.roughness = 0.30
	elif mname.contains("hydrogrowbar"):
		smat.emission_enabled = true
		smat.emission = Color(0.95, 0.96, 0.78)
		smat.emission_energy_multiplier = 1.25
	elif mname.contains("smokedamber"):
		smat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
		smat.albedo_color = Color(0.82, 0.48, 0.18, 0.78)
		smat.roughness = 0.14
		smat.metallic = 0.12


func _build_curved_oneill_vista() -> void:
	for ch: Node in _vista_container.get_children():
		ch.free()

	var mat_vista: StandardMaterial3D = material_loader.get_surface_material("oneill_vista")
	var mat_glass: StandardMaterial3D = material_loader.get_surface_material("viewport_glass")

	var st: SurfaceTool = SurfaceTool.new()
	st.begin(Mesh.PRIMITIVE_TRIANGLES)

	var cols: int = 24
	var rows: int = 16
	var width: float = 7.2

	for r: int in range(rows):
		var v0: float = float(r) / float(rows)
		var v1: float = float(r + 1) / float(rows)
		for c: int in range(cols):
			var u0: float = float(c) / float(cols)
			var u1: float = float(c + 1) / float(cols)

			var p00: Vector3 = _vista_cylinder_point(u0, v0, width)
			var p10: Vector3 = _vista_cylinder_point(u1, v0, width)
			var p11: Vector3 = _vista_cylinder_point(u1, v1, width)
			var p01: Vector3 = _vista_cylinder_point(u0, v1, width)

			st.set_normal(Vector3(0.0, 0.0, 1.0))
			st.set_uv(Vector2(u0, 1.0 - v0))
			st.add_vertex(p00)
			st.set_uv(Vector2(u1, 1.0 - v0))
			st.add_vertex(p10)
			st.set_uv(Vector2(u1, 1.0 - v1))
			st.add_vertex(p11)

			st.set_uv(Vector2(u0, 1.0 - v0))
			st.add_vertex(p00)
			st.set_uv(Vector2(u1, 1.0 - v1))
			st.add_vertex(p11)
			st.set_uv(Vector2(u0, 1.0 - v1))
			st.add_vertex(p01)

	var vista_mesh: ArrayMesh = st.commit()
	var vista_mi: MeshInstance3D = MeshInstance3D.new()
	vista_mi.name = "ONeillCylinderCurvedVista"
	vista_mi.mesh = vista_mesh
	vista_mi.material_override = mat_vista
	vista_mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_vista_container.add_child(vista_mi)

	var glass_mi: MeshInstance3D = MeshInstance3D.new()
	glass_mi.name = "NorthViewportGlassPane"
	var qmesh: QuadMesh = QuadMesh.new()
	qmesh.size = Vector2(2.48, 1.48)
	glass_mi.mesh = qmesh
	glass_mi.position = Vector3(0.0, 1.60, -2.44)
	glass_mi.material_override = mat_glass
	glass_mi.cast_shadow = GeometryInstance3D.SHADOW_CASTING_SETTING_OFF
	_vista_container.add_child(glass_mi)


func _vista_cylinder_point(u: float, v: float, width: float) -> Vector3:
	var x: float = (u - 0.5) * width
	var theta: float = (u - 0.5) * 0.65
	var cyl_lift: float = (1.0 - cos(theta)) * 2.2
	var pitch_angle: float = v * 0.88
	var y: float = -0.15 + sin(pitch_angle) * 4.4 + cyl_lift
	var z: float = -3.15 - (1.0 - cos(pitch_angle)) * 2.4 - abs(u - 0.5) * 0.4
	return Vector3(x, y, z)


func _parse_design_spec() -> Dictionary:
	var overrides: Dictionary = {}
	if not FileAccess.file_exists(DESIGN_SPEC_PATH):
		return overrides
	var file: FileAccess = FileAccess.open(DESIGN_SPEC_PATH, FileAccess.READ)
	if file == null:
		return overrides
	var text: String = file.get_as_text()
	var regex: RegEx = RegEx.new()
	regex.compile("([a-zA-Z0-9_\\-]+)\\.glb[^\\n]*?\\(([\\-0-9\\.]+)\\s*,\\s*([\\-0-9\\.]+)\\s*,\\s*([\\-0-9\\.]+)\\)")
	for m: RegExMatch in regex.search_all(text):
		var stem: String = m.get_string(1).to_lower()
		var x: float = m.get_string(2).to_float()
		var y: float = m.get_string(3).to_float()
		var z: float = m.get_string(4).to_float()
		overrides[stem] = {
			"pos": Vector3(x, y, z),
			"rot_y_deg": PROP_PLACEMENTS.get(stem, {}).get("rot_y_deg", 0.0)
		}
	return overrides
