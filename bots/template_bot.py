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
        min_path, min_cost = self.min_road_cost(locA, locB)
        reward = self.get_utility(locB) - min_cost - 250

        return min_path, reward, (min_cost + 250)

    '''
    Returns all possible starting locations
    '''
    def get_locAs(self, map):
        self.MAP_WIDTH = len(map)
        self.MAP_HEIGHT = len(map[0])

        locAs = []
        for x in range(self.MAP_WIDTH):
            for y in range(self.MAP_HEIGHT):
                if map[x][y].structure.team == self.team:
                    locAs.append(map[x][y])

        return locAs 

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
        
    Returns:
        - paths: List[(List[Tile], reward)]
        - bid: Float
    '''
    def get_best_path(self, map):
        best_path = None
        best_reward = -math.inf
        best_bid = None
        for locA in self.get_locAs(map):
            path, bid, reward = self.get_best_move(locA)
            if path and reward > best_reward:
                best_path = path
                best_reward = reward
                best_bid = bid 

        return best_path, best_bid



    def play_turn(self, turn_num, map, player_info):
        self.map = map
        return
