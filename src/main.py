from dotenv import load_dotenv
from game import Game
import time
import os

load_dotenv()

FRAME_RATE = int(os.getenv("FRAME_RATE", 60))
SCREEN_WIDTH = int(os.getenv("SCREEN_WIDTH", 800))
SCREEN_HEIGHT = int(os.getenv("SCREEN_HEIGHT", 600))
FRAME_TIME = 1.0 / FRAME_RATE

def main():
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    last_frame = 0.0
    while True:
        elapsed = time.time() - last_frame
        if elapsed < FRAME_TIME:
            continue
        last_frame = time.time()
        
        game.update()
        game.render()
    
if __name__ == "__main__":
    main()