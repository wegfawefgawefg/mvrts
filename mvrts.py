'''
we are going to make a real time strategy game
where you make unit dots and move them around with the mouse
select the unit dots with a rectangle

unit dots have target points that they move to.
use pygame and pygame vectors
'''

import random
import math

import pygame
from pygame.locals import *
from pygame.color import *
from pygame.math import Vector2

from unit import Unit
from factory import Factory
from hq import HQ
from grid import Grid

def handle_input():
    pass

def main():
    pygame.init()
    # loop here
    WIDTH, HEIGHT = 900, 900
    main_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen = main_screen.convert_alpha()

    pygame.display.set_caption('MVRTS')
    clock = pygame.time.Clock()
    running = True

    TEAM = "red"
    grid = Grid(cell_size=32)

    units = []
    buildings = []
    # selection state
    selected_units = []
    selection_start = None
    selection_end = None
    selecting = False

    hqs = {}
    hq = HQ(pos=Vector2(WIDTH/2, HEIGHT/4 * 3), grid=grid, team="red")
    hqs["red"] = hq
    buildings.append(hq)
    hq = HQ(pos=Vector2(WIDTH/2, HEIGHT/4 * 1), grid=grid, team="blue")
    hqs["blue"] = hq
    buildings.append(hq)

    for i in range(3):
        factory = Factory(
            pos=Vector2(i * WIDTH // 4 + WIDTH // 4, HEIGHT * 0.1),
            grid=grid,
            team="blue" if i == 1 else None)
        buildings.append(factory)
        grid.add(factory)
    for i in range(3):
        factory = Factory(
            pos=Vector2( i * WIDTH // 4 + WIDTH // 4, HEIGHT * 0.9),
            grid=grid,
            team="red" if i == 1 else None)
        buildings.append(factory)
        grid.add(factory)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            # on right click, set target for all selected units
            if event.type == MOUSEBUTTONDOWN and event.button == 3:
                for s in selected_units:
                    s.target = Vector2(event.pos)
            '''
            on left click start a rectangle
            on release click, end the rectangle
            select all units in the rectangle
            '''
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    selecting = True
                    selection_start = Vector2(event.pos)
                    selection_end = Vector2(event.pos)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    selecting = False
                    selected_units = []
                    less_x = min(selection_start.x, selection_end.x)
                    less_y = min(selection_start.y, selection_end.y)
                    more_x = max(selection_start.x, selection_end.x)
                    more_y = max(selection_start.y, selection_end.y)
                    sel_low = Vector2(less_x, less_y)
                    sel_high = Vector2(more_x, more_y)
                    selection_rect = pygame.Rect(sel_low, sel_high - sel_low)
                    selected_units = grid.query_rect(selection_rect)
                    selected_units = [u for u in selected_units if isinstance(u, Unit)]
                    selected_units = [u for u in selected_units if u.team == TEAM]
            elif event.type == MOUSEMOTION:
                if selecting:
                    selection_end = Vector2(event.pos)
            # if hit q clear all selected units targets
            if event.type == KEYDOWN and event.key == K_q:
                for s in selected_units:
                    s.target = None
            # team red if press a
            if event.type == KEYDOWN and event.key == K_a:
                TEAM = "red"
            # team blue if press s
            if event.type == KEYDOWN and event.key == K_s:
                TEAM = "blue"

        ''' UPDATE ZONE '''            
        screen.fill((0,0,0,0))
        # check for loss conditions
        teams = ["red", "blue"]
        for team, op in zip(teams, reversed(teams)):
            if not hqs[team].team == team:
                font = pygame.font.SysFont("Arial", 72)
                text = font.render(f"{op} Team Wins!", True, (0,0,255))
                text_rect = text.get_rect()
                text_rect.center = (WIDTH/2, HEIGHT/2)
                screen.blit(text, text_rect)

        for building in buildings:
            new_unit = building.step()
            if new_unit:
                units.append(new_unit)
                grid.add(new_unit)
        for i, unit in enumerate(units):
            unit.step()
            in_range = grid.query_circle(unit.pos, Unit.PERSONAL_SPACE)
            not_me = [u for u in in_range if u != unit]
            unit.space_out(not_me)
            unit.constrain_to_screen()
            grid.update(unit)

        ''' RENDER ZONE '''
        grid.draw(screen)
        for building in buildings:
            building.draw(screen)
        for unit in units:
            unit.draw(screen)
        for unit in selected_units:
            pygame.draw.circle(screen, (255,255,255), unit.pos, unit.RADIUS+5, 1)
        if selecting:
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(selection_start, selection_end -   selection_start), 1)

        main_screen.fill((0,0,0))
        main_screen.blit(screen, (0,0))
        pygame.display.flip()
        clock.tick(60)

main()


