class_name MaterialLoader
extends RefCounted
## MaterialLoader for Cylinder Hab-7: Living Quarters
## Dynamically loads PNG/JPG textures from res://../assets/textures/
## (or res://assets/textures/) and builds Godot 4 StandardMaterial3D resources.

const EXTERNAL_TEXTURE_DIR := "res://../assets/textures"
const RES_TEXTURE_DIR := "res://assets/textures"

var _texture_cache: Dictionary = {}
var _material_cache: Dictionary = {}
var _discovered_files: Array[String] = []


func _init() -> void:
	refresh_discovered_files()


func refresh_discovered_files() -> Array[String]:
	_discovered_files.clear()
	for dir_path: String in [EXTERNAL_TEXTURE_DIR, RES_TEXTURE_DIR]:
		var dir: DirAccess = DirAccess.open(dir_path)
		if dir == null:
			continue
		dir.list_dir_begin()
		var fname: String = dir.get_next()
		while fname != "":
			if not dir.current_is_dir():
				var lower: String = fname.to_lower()
				if lower.ends_with(".png") or lower.ends_with(".jpg") or lower.ends_with(".jpeg") or lower.ends_with(".webp"):
					if not _discovered_files.has(fname):
						_discovered_files.append(fname)
			fname = dir.get_next()
		dir.list_dir_end()
	_discovered_files.sort()
	return _discovered_files


func get_discovered_files() -> Array[String]:
	return _discovered_files


func load_texture_file(filename_or_path: String) -> Texture2D:
	if _texture_cache.has(filename_or_path):
		return _texture_cache[filename_or_path] as Texture2D

	var candidate_paths: Array[String] = []
	if filename_or_path.begins_with("/") or filename_or_path.begins_with("res://"):
		candidate_paths.append(filename_or_path)
	else:
		candidate_paths.append(EXTERNAL_TEXTURE_DIR + "/" + filename_or_path)
		candidate_paths.append(RES_TEXTURE_DIR + "/" + filename_or_path)

	for path: String in candidate_paths:
		var abs_path: String = path
		if path.begins_with("res://"):
			abs_path = ProjectSettings.globalize_path(path)
		if FileAccess.file_exists(abs_path):
			var img: Image = Image.new()
			var err: Error = img.load(abs_path)
			if err == OK and not img.is_empty():
				img.generate_mipmaps()
				var tex: ImageTexture = ImageTexture.create_from_image(img)
				_texture_cache[filename_or_path] = tex
				return tex
		if path.begins_with("res://") and ResourceLoader.exists(path):
			var res: Resource = ResourceLoader.load(path)
			if res is Texture2D:
				_texture_cache[filename_or_path] = res
				return res as Texture2D

	return null


func find_texture_by_keywords(keywords: Array[String], map_type: String = "albedo") -> String:
	var aux_suffixes: Array[String] = ["_normal", "_norm", "_n.", "_rough", "_roughness", "_metal", "_metallic", "_orm", "_ao", "_emit", "_emission", "_height"]
	for kw: String in keywords:
		for fname: String in _discovered_files:
			var lower: String = fname.to_lower()
			var is_aux: bool = false
			for suf: String in aux_suffixes:
				if lower.contains(suf):
					is_aux = true
					break
			if map_type == "albedo" and is_aux:
				continue
			if map_type != "albedo" and not lower.contains(map_type):
				continue
			if lower.contains(kw.to_lower()):
				return fname
	return ""


func get_surface_material(role: String) -> StandardMaterial3D:
	if _material_cache.has(role):
		return _material_cache[role] as StandardMaterial3D

	var mat: StandardMaterial3D = StandardMaterial3D.new()
	mat.resource_name = "Mat_" + role

	match role:
		"wallpaper":
			var matched: String = find_texture_by_keywords(["wallpaper_retro_geometric", "wallpaper", "wall_upper", "wall_pattern", "wall"])
			if matched != "":
				mat.albedo_texture = load_texture_file(matched)
			mat.roughness = 0.78
			mat.metallic = 0.02
			mat.uv1_scale = Vector3(3.0, 1.5, 1.0)
			_bind_companion_maps(mat, matched)

		"wainscoting":
			var matched: String = find_texture_by_keywords(["bulkhead_wainscoting", "wainscot", "wood_panel", "panel", "laminate"])
			if matched != "":
				mat.albedo_texture = load_texture_file(matched)
			mat.roughness = 0.48
			mat.metallic = 0.14
			mat.uv1_scale = Vector3(4.0, 1.0, 1.0)
			_bind_companion_maps(mat, matched)

		"floor":
			var matched: String = find_texture_by_keywords(["wood_parquet_warm", "floor", "parquet", "deck", "tile"])
			if matched != "":
				mat.albedo_texture = load_texture_file(matched)
			mat.roughness = 0.44
			mat.metallic = 0.04
			mat.uv1_scale = Vector3(3.0, 4.0, 1.0)
			_bind_companion_maps(mat, matched)

		"ceiling":
			var matched: String = find_texture_by_keywords(["ceiling", "overhead", "acoustic"])
			if matched != "":
				mat.albedo_texture = load_texture_file(matched)
			else:
				mat.albedo_color = Color(0.84, 0.80, 0.73)
			mat.roughness = 0.55
			mat.metallic = 0.15

		"brass_trim":
			var matched: String = find_texture_by_keywords(["metal_brushed_brass", "brass", "trim", "gold", "copper"])
			if matched != "":
				mat.albedo_texture = load_texture_file(matched)
			mat.albedo_color = Color(0.95, 0.82, 0.55)
			mat.metallic = 0.82
			mat.roughness = 0.28
			_bind_companion_maps(mat, matched)

		"oneill_vista":
			var matched: String = find_texture_by_keywords(["oneill_exterior_vista", "vista", "oneill", "cylinder", "exterior", "landscape"])
			if matched != "":
				mat.albedo_texture = load_texture_file(matched)
			mat.albedo_color = Color(0.92, 0.95, 0.90)
			mat.emission_enabled = false
			mat.roughness = 1.0
			mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
			mat.cull_mode = BaseMaterial3D.CULL_DISABLED

		"viewport_glass":
			mat.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
			mat.albedo_color = Color(0.82, 0.92, 0.96, 0.06)
			mat.metallic = 0.85
			mat.roughness = 0.06
			mat.cull_mode = BaseMaterial3D.CULL_DISABLED

		"rug":
			var matched: String = find_texture_by_keywords(["rug_retro_woven", "rug", "carpet", "mat"])
			if matched != "":
				mat.albedo_texture = load_texture_file(matched)
			mat.roughness = 0.90
			mat.metallic = 0.0

		"crt_screen":
			var matched: String = find_texture_by_keywords(["crt_screen_telemetry", "crt", "screen", "terminal_display", "monitor"])
			if matched != "":
				mat.albedo_texture = load_texture_file(matched)
			mat.albedo_color = Color(1.0, 0.96, 0.88)
			mat.emission_enabled = false
			mat.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
			mat.roughness = 0.15

		"warm_fabric":
			var matched: String = find_texture_by_keywords(["fabric_terracotta_cushion", "fabric", "upholstery", "cushion"])
			if matched != "":
				mat.albedo_texture = load_texture_file(matched)
			mat.roughness = 0.84

		_:
			var matched: String = find_texture_by_keywords([role])
			if matched != "":
				mat.albedo_texture = load_texture_file(matched)
			else:
				mat.albedo_color = Color(0.65, 0.62, 0.56)
			mat.roughness = 0.6

	_material_cache[role] = mat
	return mat


func _bind_companion_maps(mat: StandardMaterial3D, albedo_filename: String) -> void:
	if albedo_filename == "":
		return
	var stem: String = albedo_filename.get_basename()
	var suffixes: Array[String] = ["_normal", "_norm", "_roughness", "_rough", "_metallic", "_metal", "_emission", "_emit"]
	var kinds: Array[String] = ["normal", "normal", "roughness", "roughness", "metallic", "metallic", "emission", "emission"]
	for i: int in range(suffixes.size()):
		var suffix: String = suffixes[i]
		var map_kind: String = kinds[i]
		for ext: String in [".png", ".jpg"]:
			var candidate: String = stem + suffix + ext
			if _discovered_files.has(candidate):
				var tex: Texture2D = load_texture_file(candidate)
				if tex == null:
					continue
				match map_kind:
					"normal":
						mat.normal_enabled = true
						mat.normal_texture = tex
					"roughness":
						mat.roughness_texture = tex
					"metallic":
						mat.metallic_texture = tex
					"emission":
						mat.emission_enabled = true
						mat.emission_texture = tex
