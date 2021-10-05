import pygame

import constants
from unit import Unit
from unit import unit_constructors
from building import Building

class Factory(Building):
    def __init__(self, pos, grid, team=None):
        super().__init__(pos, grid, team)
        self.production_timer = 0
        self.now_producing = "unit"

    def step(self):
        ''' returns a unit if one is produced'''
        super().step()
        produced_unit = None
        if self.team and self.now_producing:
            self.production_timer -= 1
            if self.production_timer <= 0:
                constructor = unit_constructors[self.now_producing]
                produced_unit = constructor(self.team, pygame.Vector2(self.pos.x + self.RADIUS * 2, self.pos.y))
                self.production_timer = constants.production_times[self.now_producing]
        return produced_unit

    def draw(self, screen):
        if self.team and self.now_producing:
            self.messages["prod"] = f"prod: {self.production_timer}"
        super().draw(screen)
        