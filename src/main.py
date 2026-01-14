from app import App
from dotenv import load_dotenv
import time
import os
import pygame

load_dotenv()

FRAME_RATE = int(os.getenv("FRAME_RATE", 60))
SCALE_RATIO = int(os.getenv("SCALE_RATIO", 3))
FRAME_TIME = 1.0 / FRAME_RATE
SCREEN_WIDTH = 143
SCREEN_HEIGHT = 195

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH * SCALE_RATIO, SCREEN_HEIGHT * SCALE_RATIO))
    pygame.display.set_caption("Genetic Bird")
    clock = pygame.time.Clock()
    running = True

    app = App(screen, clock, SCREEN_HEIGHT, SCREEN_WIDTH, SCALE_RATIO, FRAME_TIME)

    while running:
        app.update()
        running = app.is_running()

    pygame.quit()
    
if __name__ == "__main__":
    main()