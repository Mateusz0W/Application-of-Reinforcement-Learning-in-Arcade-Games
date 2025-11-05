from CustomEnvs.Shooter.entity import Entity
import pygame

class Obstacle(Entity):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)

        self.color = color
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))



