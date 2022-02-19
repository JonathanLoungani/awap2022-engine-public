import sys

import math
import random

import numpy as np

from src.player import *
from src.structure import *
from src.game_constants import GameConstants as GC

class MyPlayer(Player):

    def __init__(self):
        print("Init")
        self.turn = 0
        self.map = None
        self.cell_towers = None
        self.team = None
        self.prev_dest = None

        return

    '''
    Calculate the minimum cost to build roads from locA to locB.
    '''
    def min_road_cost(self, map, locA, locB):
        dx = abs(locB.x - locA.x)
        dy = abs(locB.y - locA.y)

        cost = 0

        path = []
        # Path along x
        low_x = locB.x if locB.x < locA.x else locA.x
        high_x = locB.x if locB.x > locA.x else locA.x
        y = locB.y if low_x == locB.x else locA.y
        for i in range(low_x, high_x + 1):
            path.append(map[i][y])
            cost += 10 * map[i][y].passability

        # Path along y
        target_y = locB.y if y == locB.x else locA.y
        while y != target_y:
            if y < target_y:
                path.append(map[high_x][y + 1])
                y += 1
            else:
                path.append(map[high_x][y - 1])
                y -= 1
            cost += 10 * map[high_x][y].passability

        return path, cost

    '''
    Generator to yield optimal cell tower locations.
    '''
    def get_cell_towers(self):
        for tower in self.cell_towers:
            yield tower

    '''
    Returns true if tile is profitable to us
    '''
    def is_profitable(self, tile):
        if tile.structure is not None:
            return False

        tiles = self.get_neighbors(tile)
        unoccupied = False
        for tile in tiles:
            if tile.structure is None:
                unoccupied = True
            elif tile.structure.team == self.team and tile.structure is StructureType.TOWER:
                return False
        return unoccupied

    '''
    Get population at tile
    '''
    def get_population(self, tile, map):
        x = tile.x
        y = tile.y
        rows = len(map)
        cols = len(map[0])
        pop = tile.population
        if(x>=2):
            pop += (map[x-2][y]).population
        if((x>=1) and (y>=1)):
            pop += (map[x-1][y-1]).population
        if(x>=1):
            pop += (map[x-1][y]).population
        if((x>=1) and (y<cols-1)):
            pop += (map[x-1][y+1]).population
        if(y>=2):
            pop += (map[x][y-2]).population
        if(y>=1):
            pop += (map[x][y-1]).population
        if(y<cols-1):
            pop += (map[x][y+1]).population
        if(y<cols-2):
            pop += (map[x][y+2]).population
        if((x<rows-1) and (y>=1)):
            pop += (map[x+1][y-1]).population
        if(x<rows-1):
            pop += (map[x+1][y]).population
        if((x<rows-1) and (y<cols-1)):
            pop += (map[x+1][y+1]).population
        if(x<rows-2):
            pop += (map[x+2][y]).population

        return pop

    '''
    Gets neighboring tiles
    '''
    def get_neighbors(self, tile):
        x = tile.x
        y = tile.y
        map = self.map
        rows = len(map)
        cols = len(map[0])
        n = []
        n.append(tile)
        if(x>=2):
            n.append(map[x-2][y])
        if((x>=1) and (y>=1)):
            n.append((map[x-1][y-1]))
        if(x>=1):
            n.append((map[x-1][y]))
        if((x>=1) and (y<cols-1)):
            n.append((map[x-1][y+1]))
        if(y>=2):
            n.append((map[x][y-2]))
        if(y>=1):
            n.append((map[x][y-1]))
        if(y<cols-1):
            n.append((map[x][y+1]))
        if(y<cols-2):
            n.append((map[x][y+2]))
        if((x<rows-1) and (y>=1)):
            n.append((map[x+1][y-1]))
        if(x<rows-1):
            n.append((map[x+1][y]))
        if((x<rows-1) and (y<cols-1)):
            n.append((map[x+1][y+1]))
        if(x<rows-2):
            n.append((map[x+2][y]))

        return n



    '''
    Gets tiles the have a population at or around it
    '''
    def init_cell_towers(self, map):
        self.cell_towers = set()
        for row in map:
            for tile in row:
                if self.get_population(tile, map) > 0:
                    self.cell_towers.add(tile)

    '''
    Computes the estimated utility of building a path from location A to location B.
    '''
    def get_reward(self, locA, locB):
        min_path, min_cost = self.min_road_cost(self.map, locA, locB)
        reward = self.get_population(locB, self.map)**2 - min_cost - 250

        return min_path, reward, (min_cost + 250)

    '''
    Returns all possible starting locations
    '''
    def get_locAs(self, map, player_info):
        self.MAP_WIDTH = len(map)
        self.MAP_HEIGHT = len(map[0])

        locAs = []
        for x in range(self.MAP_WIDTH):
            for y in range(self.MAP_HEIGHT):
                if map[x][y].structure and (map[x][y].structure.team == player_info.team):
                    print(map[x][y].x, map[x][y].y)
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

        for tower in self.get_cell_towers():
            path, reward, cost = self.get_reward(locA, tower)
            # if reward > max_reward and cost <= player_info.money:
            if reward > max_reward:
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
        for locA in self.get_locAs(map, player_info):
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

    '''
    Removes cell towers from set for consideration
    '''
    def remove_neighbors(self, prev_dest, map, player_info):
        x = prev_dest.x
        y = prev_dest.y
        rows = len(map)
        cols = len(map[0])

        #remove the dest from consideration if controlled by anyone
        if not map[x][y].structure:
            return

        if prev_dest in self.cell_towers:
            self.cell_towers.remove(map[x][y])
        if map[x][y].structure.team != player_info.team:
            return 

        #remove neighbors from consideration
        if(x>=2) and map[x-2][y] in self.cell_towers:
            self.cell_towers.remove(map[x-2][y])
        if((x>=1) and (y>=1)) and map[x-1][y-1] in self.cell_towers:
            self.cell_towers.remove(map[x-1][y-1])
        if(x>=1) and map[x-1][y] in self.cell_towers:
            self.cell_towers.remove(map[x-1][y])
        if((x>=1) and (y<cols-1)) and map[x-1][y+1] in self.cell_towers:
            self.cell_towers.remove(map[x-1][y+1])
        if(y>=2) and map[x][y-2] in self.cell_towers:
            self.cell_towers.remove(map[x][y-2])
        if(y>=1) and map[x][y-1] in self.cell_towers:
            self.cell_towers.remove(map[x][y-1])
        if(y<cols-1) and map[x][y+1] in self.cell_towers:
            self.cell_towers.remove(map[x][y+1])
        if(y<cols-2) and map[x][y+2] in self.cell_towers:
            self.cell_towers.remove(map[x][y+2])
        if((x<rows-1) and (y>=1)) and map[x+1][y-1] in self.cell_towers:
            self.cell_towers.remove(map[x+1][y-1])
        if(x<rows-1) and map[x+1][y] in self.cell_towers:
            self.cell_towers.remove(map[x+1][y])
        if((x<rows-1) and (y<cols-1)) and map[x+1][y+1] in self.cell_towers:
            self.cell_towers.remove(map[x+1][y+1])
        if(x<rows-2) and map[x+2][y] in self.cell_towers:
            self.cell_towers.remove(map[x+2][y])


    def play_turn(self, turn_num, map, player_info):
        if self.cell_towers is None:
            self.init_cell_towers(map)
            self.team = player_info.team

        self.map = map

        if self.prev_dest:
            self.remove_neighbors(self.prev_dest, map, player_info)

        # Get List[(path, reward)] where path is List of Tiles
        best_path, best_bid = self.get_best_path(map, player_info)

        if best_path is None:
            print("No path found")
            return

        # Set the bid
        self.set_bid(best_bid)

        for i, tile in enumerate(best_path):
            # Build road
            if i < (len(best_path) - 1):
                self.build(StructureType.ROAD, tile.x, tile.y)
            # Build tower at the end of the path
            else:
                self.build(StructureType.TOWER, tile.x, tile.y)
                self.prev_dest = tile
