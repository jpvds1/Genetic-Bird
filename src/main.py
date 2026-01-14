from app import App
from dotenv import load_dotenv
import time
import os
import pygame

load_dotenv()

FRAME_RATE = int(os.getenv("FRAME_RATE", 60))
SCREEN_WIDTH = int(os.getenv("SCREEN_WIDTH", 800))
SCREEN_HEIGHT = int(os.getenv("SCREEN_HEIGHT", 600))
FRAME_TIME = 1.0 / FRAME_RATE

def handle_events(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Genetic Bird")
    clock = pygame.time.Clock()
    running = True

    app = App(screen, clock, SCREEN_WIDTH, SCREEN_HEIGHT, FRAME_TIME)

    while running:
        app.update()
        running = app.is_running()

    pygame.quit()
    
if __name__ == "__main__":
    main()