import random

from game.bird import Bird
from game.pipe import Pipe, RewardState

class Game:

    def __init__(self, unscaled_height: int, unscaled_width: int, scale_ratio: int, frame_time: float, model=None):
        self.screen_width = unscaled_width * scale_ratio
        self.screen_height = unscaled_height * scale_ratio
        self.scale_ratio = scale_ratio
        self.frame_time = frame_time

        self.bird = Bird(scale_ratio)
        self.pipes = []
        self.score = 0
        self.alive = True

    def update(self, dt: float, flap: bool = False) -> bool:
        if not self.alive:
            return False

        if flap:
            self.bird.flap()

        self.bird.update(dt)
        if self.bird.check_collision(self.screen_height):
            self.alive = False
            return False
        
        updated_pipes = []
        for pipe in self.pipes:
            pipe.update(dt)

            if pipe.offscreen:
                continue

            if pipe.state == RewardState.AVAILABLE:
                self.score += 1
                pipe.state = RewardState.COLLECTED

            if pipe.check_collision(self.bird.hitbox()):
                self.alive = False
                return False

            updated_pipes.append(pipe)
            
        self.pipes = updated_pipes
        self.generate_pipe()
        return True
    
    # check the position of the last pipe and generate a new one if needed
    def generate_pipe(self):
        if len(self.pipes) == 0:
            gap_y = random.randint(int(self.screen_height*0.1), int(self.screen_height*0.4))
            new_pipe = Pipe(gap_y, self.screen_width, self.screen_height, self.scale_ratio)
            self.pipes.append(new_pipe)
            return

        last_position = self.pipes[-1].position_x
        if last_position < self.screen_width * 0.5:
            gap_y = random.randint(int(self.screen_height*0.1), int(self.screen_height*0.4))
            new_pipe = Pipe(gap_y, self.screen_width, self.screen_height, self.scale_ratio)
            self.pipes.append(new_pipe)

    def get_game_state(self):
        next_pipe = None
        for pipe in self.pipes:
            if pipe.position_x + pipe.top_sprite.get_width() >= self.bird.position_x:
                next_pipe = pipe
                break

        if next_pipe is None:
            return {
                'bird_y': self.bird.position_y,
                'bird_velocity': self.bird.acceleration,
                'bird_x': self.bird.position_x,
                'pipe_x': None,
                'pipe_gap_y': None,
                'pipe_gap_height': None,
                'pipe_speed': None
            }

        return {
            'bird_y': self.bird.position_y,
            'bird_velocity': self.bird.acceleration,
            'bird_x': self.bird.position_x,
            'pipe_x': next_pipe.position_x,
            'pipe_gap_y': next_pipe.gap_y,
            'pipe_gap_height': next_pipe.gap_height,
            'pipe_speed': next_pipe.speed
        }