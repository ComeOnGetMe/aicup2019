import sys
from aicup2019 import model


def distance(vec1, vec2):
    return (vec1.x - vec2.x) ** 2 + (vec1.y - vec2.y) ** 2


def unit_distance(u1, u2):
    return distance(u1.position, u2.position)


class _Env(object):
    def __init__(self):
        self.frame = None
        self.ego = None

    @property
    def tiles(self):
        return self.frame.level.tiles

    @property
    def tile_pos(self):
        return int(self.ego.position.x), int(self.ego.position.y)

    @property
    def units(self):
        return [u for u in self.frame.units if
                u.player_id != self.ego.player_id]

    @property
    def weapons(self):
        return [b for b in self.frame.loot_boxes if
                isinstance(b, model.Item.Weapon)]

    @property
    def nearest_weapon(self):
        return min(self.weapons, key=lambda w: unit_distance(self.ego, w), default=None)

    @property
    def nearest_enemy(self):
        return min(self.units, key=lambda u: unit_distance(self.ego, u), default=None)

    def parse_frame(self, unit, game):
        self.ego = unit
        self.frame = game


sys.modules[__name__] = _Env()
