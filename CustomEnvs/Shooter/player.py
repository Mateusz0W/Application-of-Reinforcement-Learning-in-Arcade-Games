from CustomEnvs.Shooter.config import Direction, GameConfig, Colors, BulletConfig, PlayerConfig
import pygame
from CustomEnvs.Shooter.entity import Entity
from CustomEnvs.Shooter.bullet import Bullet
import time
import math

class Player(Entity):
    def __init__(self,x: float, y: float, width: float, height: float, speed: float, color: Colors, id: int) -> None:
        super().__init__(x, y, width, height)
        self.speed = speed
        self.color = color
        self.hit_by_bullet = False
        self.read_to_shoot = True
        self.last_shoot_time = time.time()
        self.health = PlayerConfig.health
        self.id = id
        self.hit_by_own_bullet = False
        self.last_position = (x, y)
        self.bullet_hits = 0
        self.own_bullet_hits = 0

    def update_position(self, direction: Direction) -> None:
        self.last_position = (self.x, self.y)
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
        
    def draw(self, screen) -> None:
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def shoot(self, angle: int, current_time: float) -> None:
        bullet_x, bullet_y = self._set_bullet_starting_position(angle) 
        self.read_to_shoot = False
        self.last_shoot_time = time.time()
        return Bullet(bullet_x, bullet_y, BulletConfig.radius, Colors.Orange, BulletConfig.speed, angle, BulletConfig.life, id=self.id)

    def reload(self, time: float) -> bool:
        if not self.read_to_shoot and (time - self.last_shoot_time) > PlayerConfig.reload_time:
            self.read_to_shoot = True
            
        return self.read_to_shoot
    
    def _set_bullet_starting_position(self, angle: int) -> tuple[float, float]:
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        angle_radians = math.radians(angle)
        r = self.width * 2 ** 0.5 + 0.1
        bullet_x = center_x + r * math.cos(angle_radians)
        bullet_y = center_y + r * math.sin(angle_radians)

        return bullet_x, bullet_y
    
    def reduce_health(self) -> None:
        if self.hit_by_bullet:
            self.health -= BulletConfig.damage
            self.hit_by_bullet = False
            self.hit_by_own_bullet = False
    
    def reset_counters(self) -> None:
        self.bullet_hits = 0
        self.own_bullet_hits = 0
            
        
