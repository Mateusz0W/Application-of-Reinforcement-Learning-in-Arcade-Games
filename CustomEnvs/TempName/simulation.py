from player import Player
from config import Colors
class Simulation:
    def __init__(self) -> None: 
        self.players = [
            Player(500,250,20,20,5,Colors.Blue),
            Player(500,750,20,20,5,Colors.Red)
        ]
    def run(self):
        self.update()

    def update(self):
        direction = Player.keyboard_input()
        if direction:
            self.players[1].update_position(direction)