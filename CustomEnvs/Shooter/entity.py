from CustomEnvs.Shooter.config import Direction

class Entity:
    def __init__(self, x: float, y: float, width: float, height: float, radius: float = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.collision = False
        self.collision_side = None
        self.radius = radius

    def _check_box_collision(self, other: "Entity") -> bool:
        return (
            self.x  < other.x + other.width and 
            self.x + self.width > other.x and
            self.y < other.y + other.height and
            self.y + self.height > other.y
        )
        
    def _check_side_of_collision(self, other: "Entity") -> Direction:
        #circrle and square
        if self.radius is not None:
            closest_x = max(other.x, min(self.x, other.x + other.width))
            closest_y = max(other.y, min(self.y, other.y + other.height))

            dx = self.x - closest_x
            dy = self.y - closest_y

            if abs(dx) > abs(dy):
                if dx > 0:
                    return Direction.LEFT   
                else:
                    return Direction.RIGHT
            else:
                if dy > 0:
                    return Direction.UP
                else:
                    return Direction.DOWN

        #square and square
        else:
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
        
    def _check_circle_collision(self, other: "Entity") -> bool:
        clamp = lambda value, min_value, max_value: max(min_value, min(max_value, value))
        
        d_vector = (self.x - (other.x + other.width / 2), self.y - (other.y + other.height / 2))
        aabb_half_extents = (other.width / 2, other.height / 2)
        clamped_x = clamp(d_vector[0], -aabb_half_extents[0], aabb_half_extents[0])
        clamped_y = clamp(d_vector[1], -aabb_half_extents[1], aabb_half_extents[1])
        closest_point = ((other.x + other.width / 2) + clamped_x, (other.y + other.height / 2) +clamped_y)
        new_d_vector = (closest_point[0] - self.x, closest_point[1] - self.y)

        diff = (new_d_vector[0] **2 + new_d_vector[1] ** 2) ** 0.5

        return diff <= self.radius

    def check_collision(self, other: "Entity") -> None:
        if self.radius is None:
            if self._check_box_collision(other):     
                self.collision = True
                self.collision_side = self._check_side_of_collision(other)
        else:
            if self._check_circle_collision(other):
                self.collision = True
                self.collision_side = self._check_side_of_collision(other)

    def reset_collision_flags(self) -> None:
        self.collision = False
        self.collision_side = None