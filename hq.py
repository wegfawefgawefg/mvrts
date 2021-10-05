import pygame

import constants
from unit import Unit
from unit import unit_constructors
from building import Building

class HQ(Building):
    CAPTURE_POINTS = 60 * 10
    def __init__(self, pos, grid, team=None):
        super().__init__(pos, grid, team)

    def step(self):
        if self.capture 
        