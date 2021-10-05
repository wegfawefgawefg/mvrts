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


    team = "red"
    grid = Grid(cell_size=32)

    # selection state
    selected_units = []
    selection_start = None
    selection_end = None
    selecting = False

    units = []
    for i in range(1):
        unit = Unit(
            team=team, 
            pos=Vector2(random.randrange(WIDTH), random.randrange(HEIGHT)))
        units.append(unit)
        grid.add(unit)

    factories = []
    for i in range(3):
        factory = Factory(
            pos=Vector2(i * WIDTH // 4 + WIDTH // 4, HEIGHT * 0.1),
            grid=grid)
        factories.append(factory)
        grid.add(factory)
    for i in range(3):
        factory = Factory(
            pos=Vector2( i * WIDTH // 4 + WIDTH // 4, HEIGHT * 0.9),
            grid=grid)
        factories.append(factory)
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
                    
            elif event.type == MOUSEMOTION:
                if selecting:
                    selection_end = Vector2(event.pos)
            # if hit q clear all selected units targets
            if event.type == KEYDOWN and event.key == K_q:
                for s in selected_units:
                    s.target = None

        ''' UPDATE ZONE '''            
        screen.fill((0,0,0,0))
        for factory in factories:
            new_unit = factory.step()
            if new_unit:
                units.append(new_unit)
                grid.add(new_unit)
        for i, unit in enumerate(units):
            unit.step()
            in_range = grid.query_circle(unit.pos, Unit.PERSONAL_SPACE)
            not_me = [u for u in in_range if u != unit]
            unit.space_out(not_me)
            grid.update(unit)

        ''' RENDER ZONE '''
        grid.draw(screen)
        for factory in factories:
            factory.draw(screen)
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


