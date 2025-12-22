from CustomEnvs.Shooter.player import Player
from CustomEnvs.Shooter.config import Colors
from CustomEnvs.Shooter.obstacle import Obstacle
from CustomEnvs.Shooter.config import GameConfig, ObstacleConfig, Colors, Direction, PlayerConfig
import random
import pygame
import time
import json
from CustomEnvs.Shooter.renderer import  Renderer

class Simulation:
    def __init__(self, render: bool=False, debuging: bool=False) -> None: 
        self.players = [
            Player(GameConfig.screen_width // 2,50,PlayerConfig.width,PlayerConfig.height,5,Colors.Blue, id=1),
            Player(GameConfig.screen_width // 2,GameConfig.screen_height - 50,PlayerConfig.width,PlayerConfig.height,5,Colors.Red, id=2)
        ]
        self.obstacles = self._set_obstacles()
        self.bullets = []
        self.game_over = True
        self.renderer = Renderer(render)
        self.running = True
        self.image = None
        self.debuging = debuging

    def run(self, actions: list[int]) -> bool:
        self.update(actions)
        self.reset_collision_flags()
        if self.debuging:
            self.restart_game()
        self.running, self.image = self.renderer.render(self,self.running)
        self.delete_bullets()
        return self.running

    def update(self, actions: list[int]) -> None:
        current_time = time.time()
        players_actions = []
        for player in self.players:
            player.reset_counters()
        if self.debuging:
            direction, space_pressed = self._keyboard_input()
            angle = 120
        else:
            for action in actions:
                if isinstance(action, Direction):
                    direction = action
                    space_pressed = False
                    angle = None
                else:
                    direction = None
                    space_pressed = True
                    angle = action
                players_actions.append((direction, space_pressed, angle))

        self.players[0].check_collision(self.players[1])
        self.players[1].check_collision(self.players[0])

        for obstacle in self.obstacles:
            self.players[0].check_collision(obstacle)
            self.players[1].check_collision(obstacle)
        
        for idx, (direction, space_pressed, angle) in enumerate(players_actions):
            if direction:
                self.players[idx].update_position(direction)
            if self.players[idx].reload(current_time):
                if space_pressed:
                    self.bullets.append(self.players[idx].shoot(angle, current_time))

        for bullet in self.bullets:
            bullet.update(self.players + self.obstacles)
        for player in self.players:
            player.reduce_health()
        if any(player.health <= 0 for player in self.players):
            self.game_over = True

        self._count_missed_shots()

    def _set_obstacles(self) -> list[Obstacle]:
        with open("CustomEnvs/Shooter/map.json" ,'r') as file:
            data = json.load(file)
        
        obstacle_data = data["Obstacles"]
        obstacles = [Obstacle(obs['x'], obs['y'], obs['width'], obs['height'], Colors.Green) for obs in obstacle_data]
  
        return obstacles
    
    def reset_collision_flags(self) -> None:
        for obj in self.players + self.bullets:
            obj.reset_collision_flags()

    def delete_bullets(self) -> None:
        self.bullets = [b for b in self.bullets if b.life > 0]

    def restart_game(self) -> None:
        if not self.game_over:
            return
        
        self.players = [
            Player(GameConfig.screen_width // 2,50,PlayerConfig.width,PlayerConfig.height,5,Colors.Blue, id=1),
            Player(GameConfig.screen_width // 2,GameConfig.screen_height - 50,PlayerConfig.width, PlayerConfig.height,5,Colors.Red, id=2)
        ]
        self.bullets.clear()
        self.game_over = False
        self.running, self.image = self.renderer.render(self,self.running)

    def _keyboard_input(self) -> tuple:
        keys = pygame.key.get_pressed()
        direction = Player.keyboard_input()
        space_pressed = True if keys[pygame.K_SPACE] else False

        return direction, space_pressed
    
    def _count_missed_shots(self):
        for player in self.players:
            for bullet in self.bullets:
                if player.id == bullet.id and bullet.hit_wall:
                    player.missed_shots += 1




