extends Node3D
## Door lab root. Builds the rig for every launch, including the placement probe.
## The long QA and the shot pass run only when their flags are on the command line.

func _ready() -> void:
	# Lab viewport only. project.godot stays at the project default.
	# 4x MSAA is for the shot pass (bay3 frit alpha-to-coverage). The numeric
	# QA does not read pixels, and 4x on this GPU blows the 15 minute window.
	var user := OS.get_cmdline_user_args()
	if _flag(user, "--qa-door-lab-shots"):
		get_viewport().msaa_3d = Viewport.MSAA_4X
	ProjectSettings.set_setting("rendering/textures/anisotropic_filter_level", 16)
	var info: Dictionary = DoorLabRig.build(self)
	set_meta("lab_info", info)
	if _flag(user, "--qa-door-lab-shots"):
		var shots: Node = load("res://tools/qa/door_lab_shots.gd").new()
		shots.name = "ShotPass"
		add_child(shots)
		shots.call("start", self)
	elif _flag(user, "--qa-door-lab"):
		var qa: Node = load("res://tools/qa/door_lab_qa.gd").new()
		qa.name = "LabPass"
		add_child(qa)
		qa.call("start", self)
	elif _flag(user, "--qa-door-lab-build"):
		print("[door_lab] build-ok")
		get_tree().quit(0)


func _flag(args: PackedStringArray, name: String) -> bool:
	return args.has(name)
