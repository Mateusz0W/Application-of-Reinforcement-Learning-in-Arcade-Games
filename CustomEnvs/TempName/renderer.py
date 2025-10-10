from config import GameConfig, Colors
import pygame
from simulation import Simulation

class Renderer:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((GameConfig.screen_width, GameConfig.screen_height))
        pygame.display.set_caption("game title")
        self.clock = pygame.time.Clock()

    def render(self, sim: Simulation, running: bool) -> bool: 
        if not running:
            return 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        self.screen.fill(Colors.Black)
        self.draw(sim)
        pygame.display.update()
        self.clock.tick(GameConfig.fps)

        return running
    
    def draw(self, sim: Simulation) -> None:
        for player in sim.players:
            player.draw(self.screen)

        
        
