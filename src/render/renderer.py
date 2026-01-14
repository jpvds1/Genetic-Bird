from game.bird import Bird
from game.pipe import Pipe
import pygame

class Renderer:
    def __init__(self, unscaled_height, unscaled_width, scale_ratio, screen, clock):
        self.scale_ratio = scale_ratio
        self.height = unscaled_height * scale_ratio
        self.width = unscaled_width * scale_ratio
        self.screen = screen
        self.clock = clock
        self.create_sprites()

    def set_vars(self, bird, pipes):
        self.bird = bird
        self.pipes = pipes

    def render(self):
        self.screen.fill("black")

        self.screen.blit(self.background_sprite, (0, 0))
        self.screen.blit(self.grass_sprite, (0, self.height - self.grass_sprite.get_height()))

        self.bird.render(self.screen)
        for pipe in self.pipes:
            pipe.render(self.screen)

        pygame.display.flip()

    def load_spritesheet(self):
        return pygame.image.load("assets/spritesheet.png").convert_alpha()
    
    def cut_sprite(self, sheet, rect):
        sprite = sheet.subsurface(rect)
        return sprite
    
    def create_sprites(self):
        sheet = self.load_spritesheet()
        self.bird_sprite = self.cut_sprite(sheet, pygame.Rect(0, 0, 34, 24))
        self.pipe_sprite = self.cut_sprite(sheet, pygame.Rect(34, 0, 52, 320))
        self.grass_sprite = self.cut_sprite(sheet, pygame.Rect(292, 0, 459 - 292, 30))
        self.background_sprite = self.cut_sprite(sheet, pygame.Rect(0, 70, 143, 155))

        self.background_sprite = pygame.transform.scale_by(self.background_sprite, self.scale_ratio)
        self.grass_sprite = pygame.transform.scale_by(self.grass_sprite, self.scale_ratio)