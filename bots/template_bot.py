import sys

import math
import random

from src.player import *
from src.structure import *
from src.game_constants import GameConstants as GC

class MyPlayer(Player):

    def __init__(self):
        print("Init")
        self.turn = 0
        self.map = None

        return

    '''
    Calculate the minimum cost to build roads from locA to locB.
    '''
    def min_road_cost(self, map, locA, locB):
        return

    '''
    Generator to yield optimal cell tower locations.
    '''
    def get_cell_towers(self, map):
        for row in map:
            for tile in row:
                if tile.structure is not None and tile.population > 0:
                    yield tile

    '''
    Get population at tile
    '''
    def get_population(self, tile):
        return

    '''
    Computes the estimated utility of building a path from location A to location B.
    '''
    def get_reward(self, locA, locB):
        return [], 0

    '''
    Returns best path and estimated reward of path starting from location A
    
    Params
        - locA: Tile
    
    Returns
        - path: List[Tile]
        - reward: Float
    '''
    def get_best_move(self, locA):
        max_reward = -math.inf
        max_path = None
        for tower in self.get_cell_towers(self.map):
            path, reward = self.get_reward(locA, tower)
            if reward > max_reward:
                max_path = path

        assert max_path is not None
        return max_path, max_reward


    def play_turn(self, turn_num, map, player_info):
        self.map = map
        return
