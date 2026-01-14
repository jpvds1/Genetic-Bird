from game.bird import Bird
from game.pipe import Pipe
import pygame

class Renderer:
    def __init__(self, width, height, screen, clock):
        self.width = width
        self.height = height
        self.screen = screen
        self.clock = clock

    def set_vars(self, bird, pipes):
        self.bird = bird
        self.pipes = pipes

    def render(self):
        self.screen.fill("black")

        self.bird.render(self.screen)
        for pipe in self.pipes:
            pipe.render(self.screen)

        pygame.display.flip()