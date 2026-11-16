extends Node

const _FB := preload("res://scripts/tennis_tower_fixes/tt_collider_fallback.gd")


func _ready() -> void:
	_run.call_deferred()


func _run() -> void:
	var tower: Node3D = (load("res://scenes/tennis_tower/tennis_tower.tscn") as PackedScene).instantiate() as Node3D
	add_child(tower)
	_FB.run(tower)
	_FB.leak_stats(tower)
	print("[TT] LEAK DONE")
	get_tree().quit(0)
