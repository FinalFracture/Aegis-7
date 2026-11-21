"""Rook door_lab QA for the bi-parting pocket slider (pass C): thin wrapper over door_lab_passC.py (clip at key poses, leaf / panel /
solenoid sweeps, tri budget, renders to /workspace/renders/doorlab_passC/). The pass B checks used the old node names."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import door_lab_passC as pc
if __name__ == "__main__":
    pc.main(["biparting_slide"], "--no-render" not in sys.argv)
