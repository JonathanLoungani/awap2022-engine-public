import sys

import math
import random
import heapq
from collections import defaultdict

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
    def min_road_cost(self, map, source, target):
        class Node(object):
            def __init__(self, val: int, data):
                self.val = val
                self.data = data

            def __repr__(self):
                return f'Node value: {self.val}'

            def __lt__(self, other):
                return self.val < other.val

        def get_neighbors(location):
            neighbors = []
            for (dx, dy) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                x = location.x + dx
                y = location.y + dy
                if x < 0 or y < 0 or x >= len(map) or y >= len(map[0]):
                    continue

                neighbor = map[x][y]
                if neighbor.structure is None:
                    neighbors.append(neighbor)
            return neighbors

        # if source.structure is not None:
        #     raise Exception('min_road_cost called starting from non-empty tile')
        if target.structure is not None:
            raise Exception('min_road_cost called ending on non-empty tile')

        dist = defaultdict(lambda: float('inf'))
        prev = defaultdict(lambda: None)
        visited = set()

        frontier = [Node(source.passability, source)]
        dist[source] = source.passability
        heapq.heapify(frontier)

        # print('source:', source.x, source.y, 'target:', target.x, target.y)
        while len(frontier) != 0:

            tile = heapq.heappop(frontier).data
            if tile == target: break
            if (tile.x, tile.y) in visited: continue

            visited.add((tile.x, tile.y))

            for neighbor in get_neighbors(tile):
                if (neighbor.x, neighbor.y) not in visited:
                    alt = dist[tile] + neighbor.passability
                    if alt < dist[neighbor]:
                        dist[neighbor] = alt
                        prev[neighbor] = tile
                    heapq.heappush(frontier, Node(dist[neighbor], neighbor))

            # print(tile.x, tile.y, "\n", [(n.data.x, n.data.y) for n in frontier], "\n", visited, "\n" + "="*20)


        path = []
        u = target
        if prev[u] is None:
            # raise Exception('No path possible')
            return path, float('inf')

        while u is not None:
            path.insert(0, u)
            u = prev[u]

        return path, dist[target]

    '''
    Generator to yield optimal cell tower locations.
    '''
    def get_cell_towers(self, map):
        for row in map:
            for tile in row:
                if tile.structure is None and tile.population > 0:
                    yield tile

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
    Computes the estimated utility of building a path from location A to location B.
    '''
    def get_reward(self, locA, locB):
        min_path, min_cost = self.min_road_cost(self.map, locA, locB)
        reward = self.get_population(locB, self.map) - min_cost - 250

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
            # print(f"Reward: {reward}, Cost: {cost}")
            # if reward > max_reward and cost <= player_info.money:
            if reward > max_reward:
                max_path = path
                max_reward = reward
                max_bid = (cost - sec_max_cost) if sec_max_cost == -1 else (player_info.money - cost)
                sec_max_cost = cost

        # print(f"Reward: {max_reward}, Max path: {len(max_path)}")
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


    def play_turn(self, turn_num, map, player_info):
        self.map = map

        # Get List[(path, reward)] where path is List of Tiles
        best_path, best_bid = self.get_best_path(map, player_info)

        if best_path is None:
            return

        # Set the bid
        self.set_bid(best_bid)

        for i, tile in enumerate(best_path):
            # Build road
            if i < len(best_path) - 1:
                self.build(StructureType.ROAD, tile.x, tile.y)
            # Build tower at the end of the path
            else:
                self.build(StructureType.TOWER, tile.x, tile.y)
