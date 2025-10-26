from config import GameConfig, Colors
import pygame
import cv2
import numpy as np
import os

class Renderer:
    def __init__(self, rendering: bool) -> None:
        os.environ["SDL_VIDEODRIVER"] = "dummy" if not rendering else os.environ.get("SDL_VIDEODRIVER", "")
        pygame.init()
        if rendering:
            self.screen = pygame.display.set_mode((GameConfig.screen_width, GameConfig.screen_height)) 
        else:
            self.screen = pygame.Surface((GameConfig.screen_width, GameConfig.screen_height))
        pygame.display.set_caption("game title")
        self.clock = pygame.time.Clock()
        self.rendering = rendering

    def render(self, sim, running: bool) -> tuple[bool, np.ndarray]: 
        if not running:
            return 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        self.screen.fill(Colors.Black)
        self.draw(sim)
        if self.rendering:
            pygame.display.flip()
        self.clock.tick(GameConfig.fps)

        return running, self.save_image()
    
    def draw(self, sim) -> None:
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



        

        
        
