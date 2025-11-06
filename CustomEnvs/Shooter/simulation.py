from CustomEnvs.Shooter.player import Player
from CustomEnvs.Shooter.config import Colors
from CustomEnvs.Shooter.obstacle import Obstacle
from CustomEnvs.Shooter.config import GameConfig, ObstacleConfig, Colors, Direction
import random
import pygame
import time
from CustomEnvs.Shooter.renderer import  Renderer

class Simulation:
    def __init__(self, render: bool=False, debuging: bool=False) -> None: 
        self.players = [
            Player(500,250,20,20,5,Colors.Blue, id=1),
            Player(500,750,20,20,5,Colors.Red, id=2)
        ]
        self.obstacles = self._set_obstacles()
        self.bullets = []
        self.game_over = True
        self.renderer = Renderer(render)
        self.running = True
        self.image = None
        self.debuging = debuging

    def run(self, action: int) -> bool:
        self.update(action)
        self.reset_collision_flags()
        if self.debuging:
            self.restart_game()
        self.running, self.image = self.renderer.render(self,self.running)
        self.delete_bullets()
        return self.running

    def update(self, action: int) -> None:
        current_time = time.time()
        for player in self.players:
            player.reset_counters()
        if self.debuging:
            direction, space_pressed = self._keyboard_input()
            angle = 120
        else:
            if isinstance(action, Direction):
                direction = action
                space_pressed = False
            else:
                direction = None
                space_pressed = True
                angle = action
        self.players[1].check_collision(self.players[0])
        for obstacle in self.obstacles:
            self.players[1].check_collision(obstacle)
        if direction:
            self.players[1].update_position(direction)
        if self.players[1].reload(current_time):
            if space_pressed:
                self.bullets.append(self.players[1].shoot(angle, current_time))
        for bullet in self.bullets:
            bullet.update(self.players + self.obstacles)
            for player in self.players:
                player.reduce_health()
            if any(player.health <= 0 for player in self.players):
                self.game_over = True
                break
    

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
            Player(500,250,20,20,5,Colors.Blue, id=1),
            Player(500,750,20,20,5,Colors.Red, id=2)
        ]
        self.bullets.clear()
        self.game_over = False
        self.running, self.image = self.renderer.render(self,self.running)

    def _keyboard_input(self) -> tuple:
        keys = pygame.key.get_pressed()
        direction = Player.keyboard_input()
        space_pressed = True if keys[pygame.K_SPACE] else False

        return direction, space_pressed



