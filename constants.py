import pygame

pygame.font.init()
font = pygame.font.SysFont("Arial", 20)

HEIGHT, WIDTH = 900, 900

unit_types = set("unit")
production_times = {
    'unit': 60 * 3
}
team_colors = {
    None: (255, 255, 255, 100),
    "red": (255, 0, 0, 255),
    "blue": (0, 0, 255, 255),
    "green": (0, 255, 0, 255),
    "yellow": (255, 255, 0, 255),
    "purple": (255, 0, 255, 255),
    "orange": (255, 165, 0, 255),
}