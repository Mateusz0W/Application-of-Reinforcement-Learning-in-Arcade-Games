from config import Direction, GameConfig, Colors
import pygame
from entity import Entity

class Player(Entity):
    def __init__(self,x: float, y: float, width: float, height: float, speed: float, color: Colors) -> None:
        super().__init__(x, y, width, height)
        self.speed = speed
        self.color = color

    def update_position(self, direction: Direction) -> None:
        if direction == Direction.RIGHT and direction != self.collision_side:
            self.x += self.speed
        elif direction == Direction.LEFT and direction != self.collision_side:
            self.x -= self.speed
        elif direction == Direction.UP and direction != self.collision_side:
            self.y -= self.speed
        elif direction == Direction.DOWN and direction != self.collision_side:
            self.y += self.speed

        self.x = max(0, min(self.x, GameConfig.screen_width - self.width))
        self.y = max(0, min(self.y, GameConfig.screen_height - self.height))

    @staticmethod
    def keyboard_input() -> Direction | None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            return Direction.UP
        elif keys[pygame.K_s]:
            return Direction.DOWN
        elif keys[pygame.K_a]:
            return Direction.LEFT
        elif keys[pygame.K_d]:
            return Direction.RIGHT
        else:
            return None
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def reset(self) -> None:
        self.collision = False
        self.collision_side = None

