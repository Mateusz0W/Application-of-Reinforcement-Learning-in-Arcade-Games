from config import GameConfig, Colors
import pygame
from simulation import Simulation
import cv2
import numpy as np

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
        pygame.display.flip()
        self.clock.tick(GameConfig.fps)
       # self.save_image()

        return running
    
    def draw(self, sim: Simulation) -> None:
        for player in sim.players:
            player.draw(self.screen)

        for obstacle in sim.obstacles:
            obstacle.draw(self.screen)

        for bulet in sim.bullets:
            bulet.draw(self.screen)

    def save_image(self) -> np.ndarray:
        image = pygame.surfarray.array3d(self.screen) 
        image = np.transpose(image, (1, 0, 2))
        image = cv2.resize(image, (250, 160), interpolation=cv2.INTER_AREA)
        return image.astype(np.uint8)



        

        
        
