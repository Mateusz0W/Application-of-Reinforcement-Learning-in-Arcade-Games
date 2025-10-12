from entity import Entity
import math
import pygame

class Bullet(Entity):
    
    def __init__(self, x: float, y: float, radius: float, color: tuple[int, int, int], speed: float, angle: float, width: float = None, height: float = None):
        super().__init__(x, y, width, height, radius)
        self.color = color
        self.speed = speed
        self.angle = angle

    def update_position(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

