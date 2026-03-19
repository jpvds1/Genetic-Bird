from game.orchestrator import Orchestrator
from render.renderer import Renderer, MenuSelection

from enum import Enum, auto
import pygame

class AppState(Enum):
    MENU = auto()
    RUNNING = auto()
    TRAINING = auto()
    GAME_OVER = auto()
    OFF = auto()

class App:
    def __init__(self, screen, clock, unscaled_height, unscaled_width, scale_ratio: int, frame_time: float):
        self.screen = screen
        self.clock = clock
        self.frame_time = frame_time
        self.state = AppState.MENU

        self.orchestrator = Orchestrator(
            unscaled_height, 
            unscaled_width, 
            scale_ratio, 
            frame_time
        )

        self.renderer = Renderer(
            unscaled_height, 
            unscaled_width, 
            scale_ratio, 
            screen, 
            clock
        )

    def _collect_input_state(self) -> dict:
        input_state = {
            "quit": False,
            "escape": False,
            "flap": False
        }

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                input_state["quit"] = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    input_state["escape"] = True
                elif event.key == pygame.K_SPACE:
                    input_state["flap"] = True

        return input_state

    def _sync_renderer_with_game(self):
        visible_game = self.orchestrator.get_visible_game()
        if visible_game is not None:
            self.renderer.set_vars(visible_game.bird, visible_game.pipes)

    def _handle_menu(self):
        selection = self.renderer.render_menu()

        if selection == MenuSelection.PLAY:
            self.orchestrator.start_human_game()
            self._sync_renderer_with_game()
            self.state = AppState.RUNNING
            return

        if selection == MenuSelection.VIEW:
            model_name = self.renderer.menu.chosen_ai or "Naive"
            self.orchestrator.start_ai_view(model_name)
            self._sync_renderer_with_game()
            self.state = AppState.RUNNING
            return

        if selection == MenuSelection.TRAIN:
            model_name = self.renderer.menu.chosen_ai or "Naive"
            menu = self.renderer.menu

            if menu.train_mode.name == "TIME":
                self.orchestrator.start_training_time(model_name, menu.train_time)
            else:
                self.orchestrator.start_training_iterations(model_name, menu.train_it)

            self.state = AppState.TRAINING
            return
        
        if selection == MenuSelection.QUIT:
            self.state = AppState.OFF

    def _handle_running(self, dt: float, input_state: dict):
        active = self.orchestrator.update(dt, input_state)
        self._sync_renderer_with_game()

        if not active:
            self.state = AppState.GAME_OVER

    def _handle_training(self, dt: float, input_state: dict):
        active = self.orchestrator.update(dt, input_state)

        if not active:
            summary = self.orchestrator.get_training_summary()
            print("Training finished:", summary)
            self.state = AppState.MENU

    def _render_running(self):
        visible_game = self.orchestrator.get_visible_game()
        if visible_game is not None:
            self.renderer.render(visible_game.score)

    def _render_game_over(self):
        visible_game = self.orchestrator.get_visible_game()
        if visible_game is None:
            self.state = AppState.MENU
            return

        self.renderer.set_vars(visible_game.bird, visible_game.pipes)
        selection = self.renderer.render_game_over(visible_game.score)

        if selection == MenuSelection.MENU:
            self.orchestrator.stop()
            self.state = AppState.MENU

    def run(self):
        while self.state != AppState.OFF:
            dt = self.clock.tick() / 1000.0
            input_state = self._collect_input_state()

            if input_state["quit"] or input_state["escape"]:
                self.state = AppState.OFF
                continue

            if self.state == AppState.MENU:
                self._handle_menu()

            elif self.state == AppState.RUNNING:
                self._handle_running(dt, input_state)
                self._render_running()

            elif self.state == AppState.TRAINING:
                self._handle_training(dt, input_state)

            elif self.state == AppState.GAME_OVER:
                self._render_game_over()