from player import Player
from config import Colors
from obstacle import Obstacle
from config import GameConfig, ObstacleConfig, Colors
import random

class Simulation:
    def __init__(self) -> None: 
        self.players = [
            Player(500,250,20,20,5,Colors.Blue),
            Player(500,750,20,20,5,Colors.Red)
        ]
        self.obstacles = self._set_obstacles()
        self.bullets = []

    def run(self) -> None:
        self.update()
        self.reset()

    def update(self) -> None:
        direction = Player.keyboard_input()
        self.players[1].check_collision(self.players[0])
        for obstacle in self.obstacles:
            self.players[1].check_collision(obstacle)
        if direction:
            self.players[1].update_position(direction)
        self.bullets.append(self.players[1].shoot(90))
        for bullet in self.bullets:
            bullet.update_position()

    def _set_obstacles(self) -> list[Obstacle]:
        obstacles = []
        for _ in range(GameConfig.num_of_obstacles):
            x = random.randint(0, GameConfig.screen_width)
            y = random.randint(0, GameConfig.screen_height)

            width = random.randint(ObstacleConfig.min_width, ObstacleConfig.max_width)
            height = random.randint(ObstacleConfig.min_height, ObstacleConfig.max_height)

            obstacles.append(Obstacle(x, y, width, height, Colors.Green))
        
        return obstacles
    
    def reset(self) -> None:
        for player in self.players:
            player.reset()

