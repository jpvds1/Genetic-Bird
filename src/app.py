from game.game import Game
from render.renderer import Renderer
import pygame


class App:
    def __init__(self, screen, clock, screen_width: int, screen_height: int, frame_time: float):
        self.screen = screen
        self.clock = clock
        self.running = True

        self.game = Game(screen_width, screen_height, frame_time)
        self.renderer = Renderer(screen_width, screen_height, screen, clock)
        self.renderer.set_vars(self.game.bird, self.game.pipes)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.running = False

    def is_running(self) -> bool:
        return self.running
    
    def update(self):
        if not self.game.loop(): 
            self.running = False
        
        self.handle_events()
        self.renderer.render()