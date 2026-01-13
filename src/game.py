import random
import time

from bird import Bird
from pipe import Pipe

class Game:
    bird: Bird
    pipes: list[Pipe]
    screen_width: int
    screen_height: int
    frame_time: float
    last_frame: float = 0.0
    
    def __init__(self, screen_width: int, screen_height: int, frame_time: float):
        self.bird = Bird()
        self.pipes = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.frame_time = frame_time
        
    def update(self):
        self.bird.update()
        for pipe in self.pipes:
            pipe.update()
            if pipe.offscreen:
                self.pipes.remove(pipe)
            
        self.generate_pipe()
            
    def render(self):
        self.bird.render()
        for pipe in self.pipes:
            pipe.render()
            
    # check the position of the last pipe and generate a new one if needed
    def generate_pipe(self):
        last_position = self.pipes[-1].position_x if self.pipes else self.screen_width - 300
        if last_position < self.screen_width - 200:
            chance = random.randint(1, last_position)
            if chance > 150:
                gap_y = random.randint(50, 250)
                gap_height = 100
                new_pipe = Pipe(gap_y, gap_height, self.screen_width)
                self.pipes.append(new_pipe)
                
    def loop(self):
        elapsed = time.time() - self.last_frame
        if elapsed < self.frame_time:
            return True
        self.last_frame = time.time()

        self.update()
        self.render()
        
        return True