from game.bird import Bird
from game.pipe import Pipe
from render.sprite_helper import get_grass_sprite, get_background_sprite
from enum import Enum
import pygame

BUTTON_COLOR = (209, 0, 0)
BUTTON_HOVER_COLOR = (255, 0, 0)

class MenuState(Enum):
    MAIN = 0
    AI = 1
    SELECT = 2

class MenuSelection(Enum):
    MENU = 0
    PLAY = 1
    AI = 2
    QUIT = 4

class Menu:
    def __init__(self, unscaled_height, unscaled_width, scale_ratio, screen, clock):
        self.scale_ratio = scale_ratio
        self.height = unscaled_height * scale_ratio
        self.width = unscaled_width * scale_ratio
        self.screen = screen
        self.clock = clock
        self.background_sprite = get_background_sprite(scale_ratio)
        self.grass_sprite = get_grass_sprite(scale_ratio)
        self.state = MenuState.MAIN
        self.chosen_ai = None

    def render(self):
        if self.state == MenuState.MAIN:
            return self.render_main_menu()
        elif self.state == MenuState.AI:
            return self.render_ai_menu()
        elif self.state == MenuState.SELECT:
            return self.render_select_menu()

    def wait_for_mouse_release(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False

    def draw_button(self, text, x, y, width, height):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR, (x, y, width, height))
            if click[0] == 1:
                self.wait_for_mouse_release()
                return True
        else:
            pygame.draw.rect(self.screen, BUTTON_COLOR, (x, y, width, height))

        font = pygame.font.Font(None, 10 * self.scale_ratio)
        text_surface = font.render(text, True, "black")
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(text_surface, text_rect)


    def render_main_menu(self):
        self.screen.fill("black")

        self.screen.blit(self.background_sprite, (0, 0))
        self.screen.blit(self.grass_sprite, (0, self.height - self.grass_sprite.get_height()))

        if self.draw_button("Start Game", self.width // 2 - 40 * self.scale_ratio, self.height // 2 - 40 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio):
            return MenuSelection.PLAY
        
        if self.draw_button("AI", self.width // 2 - 40 * self.scale_ratio, self.height // 2 - 10 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio):
            self.state = MenuState.AI

        if self.draw_button("Quit", self.width // 2 - 40 * self.scale_ratio, self.height // 2 + 20 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio):
            return MenuSelection.QUIT

        pygame.display.flip()

        return MenuSelection.MENU
    
    def render_ai_menu(self):
        self.screen.fill("black")

        self.screen.blit(self.background_sprite, (0, 0))
        self.screen.blit(self.grass_sprite, (0, self.height - self.grass_sprite.get_height()))

        if self.draw_button("Naive", self.width // 2 - 40 * self.scale_ratio, self.height // 2 - 20 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio):
            self.chosen_ai = "Naive"
            self.state = MenuState.SELECT
        
        if self.draw_button("Genetic Algorithm", self.width // 2 - 40 * self.scale_ratio, self.height // 2 + 10 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio):
            self.chosen_ai = "Genetic Algorithm"
            self.state = MenuState.SELECT

        pygame.display.flip()

        return MenuSelection.MENU
    
    def render_select_menu(self):
        self.screen.fill("black")

        self.screen.blit(self.background_sprite, (0, 0))
        self.screen.blit(self.grass_sprite, (0, self.height - self.grass_sprite.get_height()))

        font = pygame.font.Font(None, 10 * self.scale_ratio)
        text = font.render(f"Selected AI: {self.chosen_ai}", True, (255, 255, 255))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - 50 * self.scale_ratio))

        if self.draw_button("Train", self.width // 2 - 40 * self.scale_ratio, self.height // 2 - 20 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio):
            return MenuSelection.AI

        if self.draw_button("View", self.width // 2 - 40 * self.scale_ratio, self.height // 2 + 10 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio):
            return MenuSelection.AI

        pygame.display.flip()

        return MenuSelection.MENU