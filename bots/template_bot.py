import sys

import random

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
    def get_population(self, tile):
        return

    '''
    Computes the estimated utility of building a path from location A to location B.
    '''
    def get_reward(self, locA, locB):
        return


    def play_turn(self, turn_num, map, player_info):

        return
