from game.bird import Bird
from game.pipe import Pipe
from render.sprite_helper import get_grass_sprite, get_background_sprite
from enum import Enum
import pygame

BUTTON_COLOR = (209, 0, 0)
BUTTON_HOVER_COLOR = (255, 0, 0)

class MenuSelection(Enum):
    MENU = 0
    PLAY = 1
    GA = 2
    QUIT = 4

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

    def draw_button(self, text, x, y, width, height, mouse_pos, click):
        if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR, (x, y, width, height))
            if click[0] == 1:
                return True
        else:
            pygame.draw.rect(self.screen, BUTTON_COLOR, (x, y, width, height))

        font = pygame.font.Font(None, 10 * self.scale_ratio)
        text_surface = font.render(text, True, "black")
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)


    def menu(self):
        self.screen.fill("black")

        self.screen.blit(self.background_sprite, (0, 0))
        self.screen.blit(self.grass_sprite, (0, self.height - self.grass_sprite.get_height()))

        if self.draw_button("Start Game", self.width // 2 - 40 * self.scale_ratio, self.height // 2 - 10 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio, pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
            return MenuSelection.PLAY

        if self.draw_button("Quit", self.width // 2 - 40 * self.scale_ratio, self.height // 2 + 20 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio, pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
            return MenuSelection.QUIT

        pygame.display.flip()

        return MenuSelection.MENU