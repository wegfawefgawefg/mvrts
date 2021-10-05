''' this is a spatial indexing datastructure to make collision detection more efficient '''
import pygame
from pygame.rect import Rect

class Grid:
    def __init__(self, cell_size):
        self.positions = {}
        self.grid = {}
        self.cell_size = cell_size
    
    def cell_pos(self, p):
        return p // self.cell_size

    def get_cell_index(self, x, y):
        return (self.cell_pos(x), self.cell_pos(y))

    def update(self, obj):
        self.remove(obj)
        self.add(obj)

    def add(self, obj):
        cell_index = self.get_cell_index(obj.pos.x, obj.pos.y)
        if cell_index not in self.grid:
            self.grid[cell_index] = []
        self.grid[cell_index].append(obj)
        self.positions[obj] = cell_index
    
    def remove(self, obj):
        cell_index = self.positions[obj]
        if cell_index in self.grid:
            self.grid[cell_index].remove(obj)
            del self.positions[obj]

    def query_circle(self, pos, radius):
        objects = []
        rect = Rect(pos.x - radius, pos.y - radius, radius * 2, radius * 2)
        for unit in self.query_rect(rect):
            if unit.pos.distance_to(pos) < radius:
                objects.append(unit)
        return objects

    def query_rect(self, rect):
        objects = []
        for x in range( self.cell_pos(rect.left), self.cell_pos(rect.right) + 1 ):
            for y in range( self.cell_pos(rect.top), self.cell_pos(rect.bottom) + 1 ):
                if (x, y) in self.grid:
                    for obj in self.grid[(x, y)]:
                        if rect.collidepoint(obj.pos.x, obj.pos.y):
                            objects.append(obj)
        return objects


    def draw(self, screen):
        for cell in self.grid:
            #transparent with thin outline
            pygame.draw.rect(screen, (255, 255, 255, 20), Rect(cell[0] * self.cell_size, cell[1] * self.cell_size, self.cell_size, self.cell_size), 1)




