from enum import Enum
from dataclasses import dataclass

class Direction(Enum):
    LEFT = "Left"
    RIGHT = "Right"
    UP = "Up"
    DOWN = "Down"

@dataclass(frozen=True)
class GameConfig:
    screen_width: int = 800
    screen_height: int = 600
    fps: int = 60
    num_of_obstacles: int = 12

@dataclass(frozen=True)
class Colors:
    Red = (255, 0, 0)
    Blue = (0, 0, 255)
    Black = (0, 0, 0)
    Green = (0, 255, 0)
    Orange = (255, 165, 0)

@dataclass(frozen=True)
class ObstacleConfig:
    min_width: int = 10
    max_width: int = 70
    max_height: int = 70
    min_height: int = 10

@dataclass(frozen=True)
class BulletConfig:
    radius: int = 10
    speed: int = 5
    life: int = 4
    damage: int = 40

@dataclass(frozen=True)
class PlayerConfig:
    reload_time: int = 1
    health: int = 100