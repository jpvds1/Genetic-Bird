from game.game import Game
from render.renderer import Renderer, MenuSelection
from enum import Enum
import pygame

class AppState(Enum):
    MENU = 0
    PLAYING = 1
    TRAINING = 2
    GAME_OVER = 3
    OFF = 4

class App:
    def __init__(self, screen, clock, unscaled_height, unscaled_width, scale_ratio: int, frame_time: float):
        self.screen = screen
        self.clock = clock
        self.state = AppState.MENU

        self.game = Game(unscaled_height, unscaled_width, scale_ratio, frame_time)
        self.renderer = Renderer(unscaled_height, unscaled_width, scale_ratio, screen, clock)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = AppState.OFF

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.state = AppState.OFF
        if keys[pygame.K_SPACE]:
            self.game.bird.flap()
    
    def update(self):
        dt = self.clock.tick() / 1000.0

        if not self.game.update(dt): 
            self.state = AppState.GAME_OVER        

    def render(self):
        if self.state == AppState.MENU:
            selection = self.renderer.menu()

            if selection == MenuSelection.PLAY:
                self.game = Game(self.game.screen_height // self.game.scale_ratio, self.game.screen_width // self.game.scale_ratio, self.game.scale_ratio, self.game.frame_time)
                self.renderer.set_vars(self.game.bird, self.game.pipes)
                self.state = AppState.PLAYING
            elif selection == MenuSelection.QUIT:
                self.state = AppState.OFF
            else:
                self.state = AppState.MENU
        elif self.state == AppState.PLAYING:
            self.renderer.render(self.game.score)
        elif self.state == AppState.GAME_OVER:
            selection = self.renderer.render_game_over(self.game.score)
            if selection == MenuSelection.MENU:
                self.state = AppState.MENU
    
    def run(self):
        while self.state != AppState.OFF:
            self.handle_events()

            if self.state == AppState.PLAYING:
                self.update()

            self.render()
