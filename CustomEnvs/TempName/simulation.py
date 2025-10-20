from player import Player
from config import Colors
from obstacle import Obstacle
from config import GameConfig, ObstacleConfig, Colors
import random
import pygame

class Simulation:
    def __init__(self) -> None: 
        self.players = [
            Player(500,250,20,20,5,Colors.Blue),
            Player(500,750,20,20,5,Colors.Red)
        ]
        self.obstacles = self._set_obstacles()
        self.bullets = []
        self.game_over = False

    def run(self) -> None:
        self.update()
        self.reset_collision_flags()
        self.restart_game()

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        direction = Player.keyboard_input()
        self.players[1].check_collision(self.players[0])
        for obstacle in self.obstacles:
            self.players[1].check_collision(obstacle)
        if direction:
            self.players[1].update_position(direction)
        if keys[pygame.K_SPACE]:
            self.bullets.append(self.players[1].shoot(120))
        for bullet in self.bullets:
            bullet.update(self.players + self.obstacles)
            if any(player.hit_by_bullet for player in self.players):
                self.game_over = True
                break
    
        self.delete_bullets()

    def _set_obstacles(self) -> list[Obstacle]:
        obstacles = []
        for _ in range(GameConfig.num_of_obstacles):
            x = random.randint(0, GameConfig.screen_width)
            y = random.randint(0, GameConfig.screen_height)

            width = random.randint(ObstacleConfig.min_width, ObstacleConfig.max_width)
            height = random.randint(ObstacleConfig.min_height, ObstacleConfig.max_height)

            obstacles.append(Obstacle(x, y, width, height, Colors.Green))
        
        return obstacles
    
    def reset_collision_flags(self) -> None:
        for obj in self.players + self.bullets:
            obj.reset_collision_flags()

    def delete_bullets(self) -> None:
        for idx, bullet in enumerate(self.bullets):
            if bullet.life <= 0:
                del self.bullets[idx]

    def restart_game(self) -> None:
        if not self.game_over:
            return
        
        self.players = [
            Player(500,250,20,20,5,Colors.Blue),
            Player(500,750,20,20,5,Colors.Red)
        ]
        self.bullets.clear()
        self.game_over = False


