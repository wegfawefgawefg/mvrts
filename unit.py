import random

import pygame
from pygame.math import Vector2

import constants

class Unit:
    SPEED = 2
    RADIUS = 6
    PERSONAL_SPACE = 15
    TARGET_RADIUS = 20
    def __init__(self, team, pos):
        self.team = team
        self.last_pos = pos
        self.pos = pos
        self.target = None
        self.vel = (0,0)
        self.hp = 10

    def attack(self, other):
        other.hp -= 1

    def space_out(self, others):
        for other in others:
            if self.pos.distance_to(other.pos) < self.PERSONAL_SPACE:
                self.pos += self.pos - other.pos
            if self.pos == other.pos:
                # random vector
                self.pos += Vector2(random.random(), random.random())

    def constrain_to_screen(self):
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.x > constants.WIDTH:
            self.pos.x = constants.WIDTH
        if self.pos.y > constants.HEIGHT:
            self.pos.y = constants.HEIGHT
            
    def step(self):
        self.last_pos = self.pos
        if self.target:
            to_target = self.target - self.pos
            if to_target.length() <= self.TARGET_RADIUS:
                self.vel = Vector2(0,0)
            else:
                self.vel = to_target.normalize() * self.SPEED
        else:
            self.vel = (0,0)
        self.pos += self.vel
    
    def draw(self, screen):
        pygame.draw.circle(screen, constants.team_colors[self.team], self.pos, self.RADIUS)
        if self.target:
            pygame.draw.line(screen, (255,255,255, 100), self.pos, self.target, 1)

unit_constructors = {
    "unit": Unit,
}