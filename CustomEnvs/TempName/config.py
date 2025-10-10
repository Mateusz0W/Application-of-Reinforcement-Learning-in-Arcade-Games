from enum import Enum
from dataclasses import dataclass

class Direction(Enum):
    LEFT = "Left"
    RIGHT = "Right"
    UP = "Up"
    DOWN = "Down"

@dataclass(frozen=True)
class GameConfig:
    screen_width: int = 1000
    screen_height: int = 800
    fps: int = 60

@dataclass(frozen=True)
class Colors:
    Red = (255, 0, 0)
    Blue = (0, 0, 255)
    Black = (0, 0, 0)

