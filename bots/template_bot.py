import sys

import random

import numpy as np

from src.player import *
from src.structure import *
from src.game_constants import GameConstants as GC

class MyPlayer(Player):

    def __init__(self):
        print("Init")
        self.turn = 0

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
        return

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
        return


    def play_turn(self, turn_num, map, player_info):

        return
