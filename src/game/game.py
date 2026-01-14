import random
import time

from game.bird import Bird
from game.pipe import Pipe

class Game:
    bird: Bird
    pipes: list[Pipe]
    screen_width: int
    screen_height: int
    frame_time: float
    last_frame: float = 0.0

    def __init__(self, unscaled_height: int, unscaled_width: int, scale_ratio: int, frame_time: float):
        self.bird = Bird()
        self.pipes = []
        self.screen_width = unscaled_width * scale_ratio
        self.screen_height = unscaled_height * scale_ratio
        self.frame_time = frame_time
        
    def update(self, dt: float) -> bool:
        self.bird.update(dt)
        for pipe in self.pipes:
            pipe.update(dt)
            if pipe.offscreen:
                self.pipes.remove(pipe)
            
        self.generate_pipe()

        return True
    
    # check the position of the last pipe and generate a new one if needed
    def generate_pipe(self):
        last_position = self.pipes[-1].position_x if self.pipes else self.screen_width - 300
        if last_position < self.screen_width - 200:
            chance = random.randint(1, int(last_position))
            if chance > 150:
                gap_y = random.randint(50, 250)
                gap_height = random.randint(125, 200)
                new_pipe = Pipe(gap_y, gap_height, self.screen_width)
                self.pipes.append(new_pipe)

    def get_state(self) -> dict:
        return {
            "bird": self.bird,
            "pipes": self.pipes
        }