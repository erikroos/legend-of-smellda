import pygame
from constants import ROCK_COLOR, WATER_COLOR, TREE_COLOR

class Obstacle:
    def __init__(self, x, y, width, height, obstacle_type='rock'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = obstacle_type
        self.rect = pygame.Rect(x, y, width, height)

        # Kleuren gebaseerd op type
        if obstacle_type == 'rock':
            self.color = ROCK_COLOR
        elif obstacle_type == 'water':
            self.color = WATER_COLOR
        elif obstacle_type == 'tree':
            self.color = TREE_COLOR

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
