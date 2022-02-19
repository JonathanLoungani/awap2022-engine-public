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
                if map[x][y].structure and (map[x][y].structure.team == self.team):
                    locAs.append(map[x][y])

        return locAs 

    '''
    Returns best path and estimated reward of path starting from location A
    
    Params
        - locA: Tile
    
    Returns
        - path: List[Tile]
        - bid: float
        - reward: Float
    '''
    def get_best_move(self, locA, player_info):
        max_reward = -math.inf
        max_path = None
        max_bid = 0
        sec_max_cost = -1
        for tower in self.get_cell_towers(self.map):
            path, reward, cost = self.get_reward(locA, tower)
            if reward > max_reward and cost <= player_info.money:
                max_path = path
                max_reward = reward
                max_bid = (cost - sec_max_cost) if sec_max_cost == -1 else (player_info.money - cost)
                sec_max_cost = cost

        return max_path, max_bid, max_reward

    '''
    Returns best paths to build given map and cost
    
    Params:
        - map: List[List[Tile]]
        - player_info
        
    Returns:
        - paths: List[(List[Tile], reward)]
        - bid: Float
    '''
    def get_best_path(self, map, player_info):
        best_path = None
        best_reward = -math.inf
        best_bid = None
        for locA in self.get_locAs(map):
            path, bid, reward = self.get_best_move(locA, player_info)
            if path and reward > best_reward:
                best_path = path
                best_reward = reward
                best_bid = bid 

        return best_path, best_bid

    '''
    Compute ideal bid amount
    '''
    def get_bid(self, best_paths):
        if best_paths is None or len(best_paths) <= 1:
            return 0

        best = best_paths[0]
        second_best = best_paths[1]

        best_reward = best[1]
        second_reward = second_best[1]

        return best_reward - second_reward


    def play_turn(self, turn_num, map, player_info):
        self.map = map
        return
