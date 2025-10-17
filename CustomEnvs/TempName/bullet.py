from entity import Entity
from config import GameConfig, Direction
import math
import pygame

class Bullet(Entity):
    
    def __init__(self, x: float, y: float, radius: float, color: tuple[int, int, int], speed: float, angle: float, width: float = None, height: float = None):
        super().__init__(x, y, width, height, radius)
        self.color = color
        self.speed_x = speed
        self.speed_y = speed
        self.angle = angle

    def update_position(self) -> None:
        self.x += self.speed_x * math.cos(math.radians(self.angle))
        self.y -= self.speed_y * math.sin(math.radians(self.angle))

    def draw(self, screen) -> None:
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def update(self,others) -> None:
        for other in others:
            self.check_collision(other)
            if self.collision:
                print(self.collision_side)
                if self.collision_side in (Direction.RIGHT, Direction.LEFT):
                    self.speed_x *= -1
                else:
                    self.speed_y *= -1
                break
        
        if not 0 <= self.x <= GameConfig.screen_width:
            self.speed_x *= -1

        if not 0 <= self.y <= GameConfig.screen_height:
            self.speed_y *= -1

        self.update_position()

        

