from aicup2019.utils import env
from aicup2019 import model


class BaseAgent(object):
    def __init__(self):
        self.destination = None
        self.enemy = None

    def get_action(self, unit, game, debug):
        # parsing
        env.parse_frame(unit, game)

        # decision making
        weapon = env.nearest_weapon
        enemy = env.nearest_enemy
        if env.ego.weapon is None and weapon is not None:
            destination = weapon
        self.destination = destination
        self.enemy = enemy

        # micro
        action = self.micro(destination, enemy)

        # logging
        self.log(debug, action)
        return action

    def micro(self, dest, enemy):
        # velocity
        ego_pos = env.ego.position
        target_pos = dest.position
        vel = target_pos.x - ego_pos.x
        vel = [-30., 30.][vel > 0]

        # jump
        ego_tile = env.ego.tile_pos
        jump = target_pos.y > ego_pos.y
        if target_pos.x > ego_pos.x and \
                env.tiles[ego_tile[0] + 1][ego_tile[1]] == model.Tile.WALL:
            jump = True
        if target_pos.x < ego_pos.x and \
                env.tiles[ego_tile[0] - 1][ego_tile[1]] == model.Tile.WALL:
            jump = True
        # TODO: check if above platform
        jump_down = not jump

        # attack
        # TODO: check wall in the front
        shoot = True
        reload = False  # TODO
        # TODO: prediction
        aim = model.Vec2Double(0, 0)
        if enemy is not None:
            aim = model.Vec2Double(
                enemy.position.x - ego_pos.x,
                enemy.position.y - ego_pos.y)

        return model.UnitAction(
            velocity=vel,
            jump=jump,
            jump_down=jump_down,
            aim=aim,
            shoot=shoot,
            reload=reload,
            swap_weapon=False,
            plant_mine=False
        )

    def log(self, logger, action):
        logger.draw(model.CustomData.Log(
            "Target pos: {}\nVelocity: {}\n".format(self.destination, action.velocity)
        ))
