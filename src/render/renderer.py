from game.bird import Bird
from game.pipe import Pipe
from render.sprite_helper import get_grass_sprite, get_background_sprite
from enum import Enum
from render.menu import MenuSelection, Menu
import pygame

BUTTON_COLOR = (209, 0, 0)
BUTTON_HOVER_COLOR = (255, 0, 0)


class Renderer:
    def __init__(self, unscaled_height, unscaled_width, scale_ratio, screen, clock):
        self.scale_ratio = scale_ratio
        self.height = unscaled_height * scale_ratio
        self.width = unscaled_width * scale_ratio
        self.screen = screen
        self.clock = clock
        self.background_sprite = get_background_sprite(scale_ratio)
        self.grass_sprite = get_grass_sprite(scale_ratio)
        self.menu = Menu(unscaled_height, unscaled_width, scale_ratio, screen, clock)

        self.bird = None
        self.pipes = []

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

    def render_game_over(self, score):
        self.screen.fill("black")

        self.screen.blit(self.background_sprite, (0, 0))

        self.bird.render(self.screen)
        for pipe in self.pipes:
            pipe.render(self.screen)

        self.screen.blit(self.grass_sprite, (0, self.height - self.grass_sprite.get_height()))

        self.draw_final_score(score)
        if self.draw_button("Menu", self.width // 2 - 40 * self.scale_ratio, self.height // 2 + 20 * self.scale_ratio, 80 * self.scale_ratio, 20 * self.scale_ratio):
            return MenuSelection.MENU

        pygame.display.flip()

    def render_training(self, status: dict):
        self.screen.fill("black")
        self.screen.blit(self.background_sprite, (0, 0))
        self.screen.blit(self.grass_sprite, (0, self.height - self.grass_sprite.get_height()))

        title_font = pygame.font.Font(None, 12 * self.scale_ratio)
        font = pygame.font.Font(None, 10 * self.scale_ratio)

        title = title_font.render("Training", True, (255, 255, 255))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 15 * self.scale_ratio))

        model_text = font.render(f"Model: {status['model']}", True, (255, 255, 255))
        self.screen.blit(model_text, (20 * self.scale_ratio, 40 * self.scale_ratio))

        iteration_text = font.render(f"Current iteration: {status['iteration']}", True, (255, 255, 255))
        self.screen.blit(iteration_text, (20 * self.scale_ratio, 55 * self.scale_ratio))

        if status["limit_type"] == "TIME":
            limit_value = f"{status['time_limit']:.1f}s"
            limit_label = "Time limit"
        else:
            limit_value = str(status["iteration_limit"])
            limit_label = "Iteration limit"

        limit_text = font.render(f"{limit_label}: {limit_value}", True, (255, 255, 255))
        self.screen.blit(limit_text, (20 * self.scale_ratio, 70 * self.scale_ratio))

        elapsed_text = font.render(f"Elapsed time: {status['elapsed_time']:.1f}", True, (255, 255, 255))
        self.screen.blit(elapsed_text, (20 * self.scale_ratio, 85 * self.scale_ratio))

        best_text = font.render(f"Best score: {status['best_score']}", True, (255, 255, 255))
        self.screen.blit(best_text, (20 * self.scale_ratio, 100 * self.scale_ratio))

        if self.draw_button(
            "Stop Early",
            self.width // 2 - 50 * self.scale_ratio,
            self.height // 2 + 35 * self.scale_ratio,
            100 * self.scale_ratio,
            20 * self.scale_ratio
        ):
            pygame.display.flip()
            return MenuSelection.QUIT

        pygame.display.flip()
        return None

    def render_training_results(self, summary: dict):
        self.screen.fill("black")
        self.screen.blit(self.background_sprite, (0, 0))
        self.screen.blit(self.grass_sprite, (0, self.height - self.grass_sprite.get_height()))

        title_font = pygame.font.Font(None, 12 * self.scale_ratio)
        font = pygame.font.Font(None, 10 * self.scale_ratio)

        title = title_font.render("Training Results", True, (255, 255, 255))
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 15 * self.scale_ratio))

        model_text = font.render(f"Model: {summary['model']}", True, (255, 255, 255))
        self.screen.blit(model_text, (20 * self.scale_ratio, 40 * self.scale_ratio))

        iterations_text = font.render(f"Iterations: {summary['iterations']}", True, (255, 255, 255))
        self.screen.blit(iterations_text, (20 * self.scale_ratio, 55 * self.scale_ratio))

        elapsed_text = font.render(f"Elapsed time: {summary['elapsed_time']:.1f}s", True, (255, 255, 255))
        self.screen.blit(elapsed_text, (20 * self.scale_ratio, 70 * self.scale_ratio))

        best_text = font.render(f"Best score: {summary['best_score']}", True, (255, 255, 255))
        self.screen.blit(best_text, (20 * self.scale_ratio, 85 * self.scale_ratio))

        avg_text = font.render(f"Average score: {summary['average_score']:.2f}", True, (255, 255, 255))
        self.screen.blit(avg_text, (20 * self.scale_ratio, 100 * self.scale_ratio))

        if self.draw_button(
            "Menu",
            self.width // 2 - 40 * self.scale_ratio,
            self.height // 2 + 35 * self.scale_ratio,
            80 * self.scale_ratio,
            20 * self.scale_ratio
        ):
            pygame.display.flip()
            return MenuSelection.MENU

        pygame.display.flip()
        return None

    def draw_score(self, score):
        font = pygame.font.Font(None, 10 * self.scale_ratio)
        text = font.render(str(score), True, (255, 255, 255))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, 3 * self.scale_ratio))

    def draw_final_score(self, score):
        font = pygame.font.Font(None, 10 * self.scale_ratio)
        text = font.render(f"Final Score: {score}", True, (255, 255, 255))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height() // 2))

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

    def render_menu(self):
        return self.menu.render()