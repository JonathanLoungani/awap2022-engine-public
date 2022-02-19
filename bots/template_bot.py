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
        return [], 0, 0

    '''
    Returns best path and estimated reward of path starting from location A
    
    Params
        - locA: Tile
        - budget: Float
    
    Returns
        - path: List[Tile]
        - reward: Float
    '''
    def get_best_move(self, locA, budget):
        max_reward = -math.inf
        max_path = None
        for tower in self.get_cell_towers(self.map):
            path, reward, cost = self.get_reward(locA, tower)
            if reward > max_reward and cost <= budget:
                max_path = path

        assert max_path is not None
        return max_path, max_reward

    '''
    Returns best paths to build given map and cost
    
    Params:
        - map: List[List[Tile]]
        - cost: Float (TODO: currently not used in algo)
        
    Returns:
        - paths: List[(List[Tile], reward)]
          currently only the best two paths/rewards
    '''
    def get_best_path(self, map, cost):
        pass



    def play_turn(self, turn_num, map, player_info):
        self.map = map
        return
