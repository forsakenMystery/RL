import numpy as np
from graphics import *
import time


class Wampus:
    GOLD = 2
    ME = 1
    EMPTY = 0
    VAMPIRE = 3
    ARROW = 4
    HOLE = 5
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    MAP_UP = 0
    MAP_DOWN = 1
    MAP_LEFT = 2
    MAP_RIGHT = 3
    ACTIONS = {MAP_UP: UP, MAP_DOWN: DOWN, MAP_LEFT: LEFT, MAP_RIGHT: RIGHT}
    ACTION_NUMBERS = 4
    AMMO = 0
    WAMPUS_PRIZE = 250
    DEAD_PRIZE = -150
    WINNING_PRIZE = 150
    COLLECTING_PRIZE = 50
    MOVING_PRIZE = -25

    @classmethod
    def start_desired_world(cls, width, height, holes_positions, adventurer_position, vampires_positions, gold_position, arrows_positions):
        return cls(width, height, holes_positions, adventurer_position, vampires_positions, gold_position, arrows_positions)

    @classmethod
    def start_random_world(cls, width, height, number_of_holes, number_of_vampires, number_of_arrows):
        # random this shit, nevermind it can be unsolvable
        return None

    def create_state_action_dictionary(self, policy):
        Q = {}
        for key in policy.keys():
            Q[key] = {action_map: 0.0 for action_map in self.ACTIONS}
        # print(Q)
        return Q

    def create_trajectory(self, policy):
        self.reset()
        # print("lol")
        episode = []
        finish = False
        end_please = 0
        endless = False
        while not finish and not endless:
            # print(self)
            x, y = self.me
            time_step = []
            time_step.append(self.me)
            # print(policy[self.me].values())
            random = np.random.uniform(high=sum(policy[self.me].values()))
            # print("random is ", random)
            ranging = 0
            for probability in policy[self.me].items():
                # because if we don't random and instead use a random.choice we cannot continue to search in infinity
                # print(probability)
                ranging += probability[1]
                # print("ranging", ranging)
                # print("random", random)
                if random < ranging:
                    phase = probability[0]
                    break
            finish, reward = self.move(self.ACTIONS[phase])
            time_step.append(phase)
            time_step.append(reward)
            episode.append(time_step)
            end_please += 1
            if end_please > 500:
                endless = True
        return episode

    def create_random_uniform_policy(self):
        policy = {}
        for key1 in range(0, self.width):
            for key2 in range(0, self.height):
                p = {}
                for action_map in self.ACTIONS:
                    # print(int(np.random.rand()*100))
                    p[action_map] = 1 / self.ACTION_NUMBERS
                policy[(key1, key2)] = p
        # print(policy)
        # print(policy[(0, 0)])
        return policy

    def create_random_policy(self):
        policy = {}
        for key1 in range(0, self.width):
            for key2 in range(0, self.height):
                p = {}
                sum = 0
                for action_map in self.ACTIONS:
                    # print(action_map)
                    p[action_map] = int(np.random.rand()*100)
                    sum += p[action_map]
                for action_map in self.ACTIONS:
                    p[action_map] = p[action_map]/sum
                policy[(key1, key2)] = p
        # print(policy)
        # print(policy[(0, 0)])
        return policy

    def reset(self):
        self.check_arrows = self.arrows[:]
        self.check_vampires = self.vampires[:]
        self.check_obstacles = self.obstacles[:]
        self.me = self.me_original+tuple()

        self.world = np.zeros((self.width, self.height), dtype=np.int8)
        x, y = self.me
        self.world[x, y] = self.ME
        x, y = self.gold
        self.world[x, y] = self.GOLD
        for point in self.obstacles:
            x, y = point
            self.world[x, y] = self.HOLE
        for point in self.vampires:
            x, y = point
            self.world[x, y] = self.VAMPIRE
        for point in self.arrows:
            x, y = point
            self.world[x, y] = self.ARROW

    def __init__(self, width, height, obstacles, me, vampires, gold, arrows):
        self.width = width
        self.height = height
        self.me = me+tuple()
        self.me_original = me
        self.arrows = arrows
        self.check_arrows = arrows[:]
        self.gold = gold
        self.vampires = vampires
        self.check_vampires = vampires[:]
        self.obstacles = obstacles
        self.check_obstacles = obstacles[:]
        self.world = np.zeros((width, height), dtype=np.int8)
        x, y = me
        self.world[x, y] = self.ME
        x, y = gold
        self.world[x, y] = self.GOLD
        for point in obstacles:
            x, y = point
            self.world[x, y] = self.HOLE
        for point in vampires:
            x, y = point
            self.world[x, y] = self.VAMPIRE
        for point in arrows:
            x, y = point
            self.world[x, y] = self.ARROW

    def move(self, action):
        dx, dy = action
        x, y = self.me
        reward = self.MOVING_PRIZE
        new_me_x = x+dx
        new_me_y = y+dy
        finish = False
        gold_x, gold_y = self.gold
        if x == self.width-1 or x == 0 or y == 0 or y == self.height-1:
            if x == 0 and dx == -1:
                reward = -2
                new_me_x = 0
            elif x == self.width-1 and dx == 1:
                reward = -2
                new_me_x = self.width-1
            if y == 0 and dy == -1:
                reward = -2
                new_me_y = 0
            elif y == self.height-1 and dy == 1:
                reward = -2
                new_me_y = self.height-1
        if new_me_x == gold_x and new_me_y == gold_y:
            finish = True
            reward = self.WINNING_PRIZE
        for vampire in self.check_vampires:
            vampire_x, vampire_y = vampire
            if vampire_x == new_me_x and vampire_y == new_me_y:
                if self.AMMO is 0:
                    finish = True
                    reward = self.DEAD_PRIZE
                else:
                    self.AMMO -= 1
                    reward = self.WAMPUS_PRIZE
        for hole in self.check_obstacles:
            hole_x, hole_y = hole
            if hole_x == new_me_x and hole_y == new_me_y:
                finish = True
                reward = self.DEAD_PRIZE
        for arrow in self.check_arrows:
            arrow_x, arrow_y = arrow
            if arrow_x == new_me_x and arrow_y == new_me_y:
                reward = self.COLLECTING_PRIZE
                self.AMMO += 1
        if not finish:
            self.world[x, y] = self.EMPTY
            self.world[new_me_x, new_me_y] = self.ME
            self.me = (new_me_x, new_me_y)
            if reward is self.COLLECTING_PRIZE:
                self.check_arrows.remove(self.me)
            elif reward is self.WAMPUS_PRIZE:
                self.check_vampires.remove(self.me)
        elif finish and reward == self.WINNING_PRIZE:
            self.world[x, y] = self.EMPTY
            self.world[new_me_x, new_me_y] = self.ME
            self.me = (new_me_x, new_me_y)
        return finish, reward

    def __str__(self):
        return self.world.__str__()+"\n********************\n********************\n"


def run(width, height, obstacles, me, vampires, gold, arrows):
    game = Wampus.start_desired_world(width, height, obstacles, me, vampires, gold, arrows)
    uni = game.create_random_uniform_policy()
    game.create_random_policy()
    game.create_state_action_dictionary(uni)
    print(game.create_trajectory(uni))
    print(game.create_trajectory(uni))
    # print(game)
    # print(game.move(game.ACTIONS[game.MAP_UP]))
    # print(game)
    # print(game.move(game.ACTIONS[game.MAP_LEFT]))
    # print(game)
    # print(game.move(game.ACTIONS[game.MAP_LEFT]))
    # print(game)
    # print(game.move(game.ACTIONS[game.MAP_LEFT]))
    # print(game)
    # print(game.move(game.ACTIONS[game.MAP_RIGHT]))
    # print(game)
    # print(game.move(game.ACTIONS[game.MAP_LEFT]))
    # print(game)
    # print(game.move(game.ACTIONS[game.MAP_LEFT]))
    # print(game)


def main():
    width = 5
    height = width
    obstacles = [(2, 3), (2, 2)]
    me = (4, 4)
    vampires = [(3, 1)]
    arrows = [(3, 2), (3, 3)]
    gold = (0, 0)
    run(width, height, obstacles, me, vampires, gold, arrows)


if __name__ == '__main__':
    main()
