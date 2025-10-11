from config import Direction

class Entity:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.collision = False
        self.collision_side = None

    def _check_box_collision(self, other: "Entity") -> bool:
        return (
            self.x  < other.x + other.width and 
            self.x + self.width > other.x and
            self.y < other.y + other.height and
            self.y + self.height > other.y
        )
        
    def _check_side_of_collision(self, other: "Entity") -> Direction:
        right = abs((self.x + self.width) - other.x)
        left = abs(self.x - (other.x + other.width))
        down = abs((self.y + self.height) - other.y)
        up = abs(self.y - (other.y + other.height))

        collision_side =  min(right, left, up, down)

        if collision_side == right:
            return Direction.RIGHT
        elif collision_side == left:
            return Direction.LEFT
        elif collision_side == up:
            return Direction.UP
        elif collision_side == down:
            return Direction.DOWN
        
    def check_collision(self, other) -> None:
        if self._check_box_collision(other):     
            self.collision = True
            self.collision_side = self._check_side_of_collision(other)