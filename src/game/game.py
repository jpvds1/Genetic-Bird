import random
import time

from game.bird import Bird
from game.pipe import Pipe, RewardState

class Game:
    bird: Bird
    pipes: list[Pipe]
    screen_width: int
    screen_height: int
    frame_time: float
    last_frame: float = 0.0

    def __init__(self, unscaled_height: int, unscaled_width: int, scale_ratio: int, frame_time: float):
        self.screen_width = unscaled_width * scale_ratio
        self.screen_height = unscaled_height * scale_ratio
        self.scale_ratio = scale_ratio
        self.frame_time = frame_time
        self.bird = Bird(scale_ratio)
        self.pipes = []
        self.pipes.append(Pipe(random.randint(self.screen_height*0.1, self.screen_height*0.4), self.screen_width, scale_ratio))
        self.score = 0

    def update(self, dt: float) -> bool:
        self.bird.update(dt)
        for pipe in self.pipes:
            pipe.update(dt)
            if pipe.offscreen:
                self.pipes.remove(pipe)
            if pipe.state == RewardState.AVAILABLE:
                self.score += 1
                pipe.state = RewardState.COLLECTED
            
        self.generate_pipe()

        return True
    
    # check the position of the last pipe and generate a new one if needed
    def generate_pipe(self):
        last_position = self.pipes[-1].position_x
        if last_position < self.screen_width * 0.5:
            gap_y = random.randint(self.screen_height*0.1, self.screen_height*0.4)
            new_pipe = Pipe(gap_y, self.screen_width, self.scale_ratio)
            self.pipes.append(new_pipe)
