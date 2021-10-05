import pygame

import constants
from unit import Unit
from unit import unit_constructors

class Building:
    RADIUS = 20
    CAPTURE_RADIUS = 50
    CAPTURE_POINTS = 60 * 5
    def __init__(self, pos, grid, team=None):
        self.grid = grid # grid is for colision detection
        self.team = team
        
        # should never change
        self.pos = pos
        self.rect = pygame.Rect(pos.x - self.RADIUS, pos.y - self.RADIUS, self.RADIUS * 2, self.RADIUS * 2)

        self.capture = 0
        self.messages = {}

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255, 200), self.pos, self.CAPTURE_RADIUS, 2)
        color = constants.team_colors[self.team]
        pygame.draw.rect(screen,color,self.rect,0)



        # draw messages
        messages = sorted(self.messages.keys())
        for i, message in enumerate(messages):
            text = self.messages[message]
            text = constants.font.render(text, True, (255,255,255))
            screen.blit(text, (self.rect.x, self.rect.y - i * 20))

    def step(self):
        # check surrounding area for units
        # if all units are on the same team, 
        # count the number of units, 
        # each second, add the number of units to the capture count
        # if the capture count is greater than 20, capture the building by setting the team to the capturing team
        # if the building is already captured, decrement the capture count instead, 
        # if the capture count is 0, set the building to unoccupied
        objects_around = self.grid.query_circle(self.pos, self.CAPTURE_RADIUS)
        units_around = [obj for obj in objects_around if isinstance(obj, Unit)]
        teams_around = set([u.team for u in units_around])
        if len(teams_around) == 2:
            self.messages["contested"] = "contested"
        elif len(teams_around) == 1:
            team_around = teams_around.pop()
            if self.team is None:
                self.capture += len(units_around)
                self.messages["capture"] = f"capture: {self.capture}"
                if self.capture >= self.CAPTURE_POINTS:
                    self.team = team_around
                    self.capture = self.CAPTURE_POINTS
            elif not self.team == team_around:
                self.capture -= len(units_around)
                self.messages["capture"] = f"capture: {self.capture}"
                if self.capture <= 0:
                    self.team = None
        return None
