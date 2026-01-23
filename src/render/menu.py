from game.bird import Bird
from game.pipe import Pipe
from render.sprite_helper import get_grass_sprite, get_background_sprite
from enum import Enum, auto
import pygame

BUTTON_COLOR = (209, 0, 0)
BUTTON_HOVER_COLOR = (255, 0, 0)

class MenuState(Enum):
    MAIN = auto()
    AI = auto()
    SELECT = auto()
    TRAIN = auto()

class MenuSelection(Enum):
    MENU = auto()
    PLAY = auto()
    TRAIN = auto()
    VIEW = auto()
    QUIT = auto()

class TrainMode(Enum):
    TIME = auto()
    ITERATIONS = auto()

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

        self.train_mode = TrainMode.TIME
        self.train_time = 60 # seconds
        self.train_it = 1000 # iterations
        self.train_time_step = 5
        self.train_time_min = 5
        self.train_time_max = 7200
        self.train_it_step = 50
        self.train_it_min = 50
        self.train_it_max = 50000

    def render(self):
        if self.state == MenuState.MAIN:
            return self.render_main_menu()
        elif self.state == MenuState.AI:
            return self.render_ai_menu()
        elif self.state == MenuState.SELECT:
            return self.render_select_menu()
        elif self.state == MenuState.TRAIN:
            return self.render_train_menu()

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
    
    # Render Menu to choose AI type
    def render_ai_menu(self):
        self.screen.fill("black")

        self.screen.blit(self.background_sprite, (0, 0))
        self.screen.blit(self.grass_sprite, (0, self.height - self.grass_sprite.get_height()))

        if self.draw_button("Naive", self.width // 2 - 40 * self.scale_ratio, self.height // 2 - 40 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio):
            self.chosen_ai = "Naive"
            self.state = MenuState.SELECT
        
        if self.draw_button("Genetic Algorithm", self.width // 2 - 40 * self.scale_ratio, self.height // 2 - 10 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio):
            self.chosen_ai = "Genetic Algorithm"
            self.state = MenuState.SELECT

        if self.draw_button("Back", self.width // 2 - 40 * self.scale_ratio, self.height // 2 + 20 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio):
            self.state = MenuState.MAIN

        pygame.display.flip()

        return MenuSelection.MENU
    
    # Render Menu to select Train or View for chosen AI
    def render_select_menu(self):
        self.screen.fill("black")

        self.screen.blit(self.background_sprite, (0, 0))
        self.screen.blit(self.grass_sprite, (0, self.height - self.grass_sprite.get_height()))

        font = pygame.font.Font(None, 10 * self.scale_ratio)
        text = font.render(f"Selected AI: {self.chosen_ai}", True, (255, 255, 255))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - 60 * self.scale_ratio))

        if self.draw_button("Train", self.width // 2 - 40 * self.scale_ratio, self.height // 2 - 40 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio):
            self.state = MenuState.TRAIN

        if self.draw_button("View", self.width // 2 - 40 * self.scale_ratio, self.height // 2 - 10 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio):
            return MenuSelection.VIEW
        
        if self.draw_button("Back", self.width // 2 - 40 * self.scale_ratio, self.height // 2 + 20 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio):
            self.state = MenuState.AI

        pygame.display.flip()

        return MenuSelection.MENU
    
    # Render Menu to modify time/iterations for training
    def render_train_menu(self):
        self.screen.fill("black")

        self.screen.blit(self.background_sprite, (0, 0))
        self.screen.blit(self.grass_sprite, (0, self.height - self.grass_sprite.get_height()))

        font = pygame.font.Font(None, 10 * self.scale_ratio)
        text = font.render(f"Selected AI: {self.chosen_ai}", True, (255, 255, 255))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - 60 * self.scale_ratio))

        mode_label = "TIME" if self.train_mode == TrainMode.TIME else "ITERATIONS"
        mode_text = font.render(f"Mode: {mode_label}", True, (255, 255, 255))
        self.screen.blit(mode_text, (self.width // 2 - mode_text.get_width() // 2, self.height // 2 - 80 * self.scale_ratio))

        if self.draw_button("Toggle Mode", self.width // 2 - 40 * self.scale_ratio, self.height // 2 - 40 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio):
            if self.train_mode == TrainMode.TIME:
                self.train_mode = TrainMode.ITERATIONS
            else:
                self.train_mode = TrainMode.TIME

        value_text = font.render(f"{self.train_time if self.train_mode == TrainMode.TIME else self.train_it}", True, (0, 0, 0))

        pygame.draw.rect(self.screen, BUTTON_COLOR, (self.width // 2 - 20 * self.scale_ratio, self.height // 2 - 10 * self.scale_ratio, 40 * self.scale_ratio, 20 * self.scale_ratio))
        self.screen.blit(value_text, (self.width // 2 - value_text.get_width() // 2, self.height // 2 - 3 * self.scale_ratio))

        if self.draw_button("-", self.width // 2 - 40 * self.scale_ratio, self.height // 2 - 10 * self.scale_ratio, 20 * self.scale_ratio, 20 * self.scale_ratio):
            if self.train_mode == TrainMode.TIME:
                self.train_time = max(self.train_time_min, self.train_time - self.train_time_step)
            else:
                self.train_it = max(self.train_it_min, self.train_it - self.train_it_step)

        if self.draw_button("+", self.width // 2 + 20 * self.scale_ratio, self.height // 2 - 10 * self.scale_ratio, 20 * self.scale_ratio, 20 * self.scale_ratio):
            if self.train_mode == TrainMode.TIME:
                self.train_time = min(self.train_time_max, self.train_time + self.train_time_step)
            else:
                self.train_it = min(self.train_it_max, self.train_it + self.train_it_step)

        if self.draw_button("Train", self.width // 2 - 40 * self.scale_ratio, self.height // 2 + 20 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio):
            return MenuSelection.TRAIN
        
        if self.draw_button("Back", self.width // 2 - 40 * self.scale_ratio, self.height // 2 + 50 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio):
            self.state = MenuState.SELECT

        pygame.display.flip()

        return MenuSelection.MENU