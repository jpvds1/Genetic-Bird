from game.bird import Bird
from game.pipe import Pipe
from render.sprite_helper import get_grass_sprite, get_background_sprite
import pygame

class Renderer:
    def __init__(self, unscaled_height, unscaled_width, scale_ratio, screen, clock):
        self.scale_ratio = scale_ratio
        self.height = unscaled_height * scale_ratio
        self.width = unscaled_width * scale_ratio
        self.screen = screen
        self.clock = clock
        self.background_sprite = get_background_sprite(scale_ratio)
        self.grass_sprite = get_grass_sprite(scale_ratio)

    def set_vars(self, bird, pipes):
        self.bird = bird
        self.pipes = pipes

    def render(self, score):
        self.screen.fill("black")

        self.screen.blit(self.background_sprite, (0, 0))

        self.bird.render(self.screen)
        for pipe in self.pipes:
            pipe.render(self.screen)

        self.screen.blit(self.grass_sprite, (0, self.height - self.grass_sprite.get_height()))

        self.draw_score(score)

        pygame.display.flip()

    def draw_score(self, score):
        font = pygame.font.Font(None, 10 * self.scale_ratio)
        text = font.render(str(score), True, (255, 255, 255))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, 3 * self.scale_ratio))