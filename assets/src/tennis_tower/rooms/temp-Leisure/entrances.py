"""F1-FOOD N + F1-ARC E entrances: place Arrival's canonical secondary entrances (already TT_GlassScissor).
No room-local forks. Do not rebuild or replace tt_secondary_entrance_n/e."""
from lz_lib import *

def build(PL):
    # place() expects emit()-style [(asset, world_offset)] lists
    n = [('tt_secondary_entrance_n', [0, 0, 0])]
    e = [('tt_secondary_entrance_e', [0, 0, 0])]
    place(PL, n, 72, 0, 79 + .98, 0, 'facade')
    place(PL, e, 140 + .98, 0, 37.5, 90, 'facade')
    return dict(canonical=['tt_secondary_entrance_n', 'tt_secondary_entrance_e'])

if __name__ == '__main__':
    PL = []; print(build(PL))
