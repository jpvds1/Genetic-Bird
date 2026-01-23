import random
import time

from game.bird import Bird
from game.pipe import Pipe, RewardState
from algorithms.naive import NaivePlayer
from algorithms.genetic import GeneticPlayer

class Game:
    bird: Bird
    pipes: list[Pipe]
    screen_width: int
    screen_height: int
    frame_time: float
    last_frame: float = 0.0

    def __init__(self, unscaled_height: int, unscaled_width: int, scale_ratio: int, frame_time: float, model=None):
        self.screen_width = unscaled_width * scale_ratio
        self.screen_height = unscaled_height * scale_ratio
        self.scale_ratio = scale_ratio
        self.frame_time = frame_time
        self.bird = Bird(scale_ratio)
        self.pipes = []
        self.score = 0
        
        # AI variables
        self.use_ai = model is not None
        if self.use_ai:
            self.get_model(model)

    def get_model(self):
        if self.model == "Naive":
            self.model = NaivePlayer(self.scale_ratio)
        elif self.model == "Genetic":
            self.model = GeneticPlayer(self.scale_ratio)

    def update(self, dt: float) -> bool:

        self.bird.update(dt)
        if self.bird.check_collision(self.screen_height):
            return False
        
        for pipe in self.pipes:
            pipe.update(dt)
            if pipe.offscreen:
                self.pipes.remove(pipe)
            if pipe.state == RewardState.AVAILABLE:
                self.score += 1
                pipe.state = RewardState.COLLECTED
            if pipe.check_collision(self.bird.hitbox()):
                return False
            
        self.generate_pipe()

        if self.use_ai:
            game_state = self.get_game_state()
            if self.model.decide_flap(game_state):
                self.bird.flap()

        return True
    
    # check the position of the last pipe and generate a new one if needed
    def generate_pipe(self):
        if len(self.pipes) == 0:
            gap_y = random.randint(self.screen_height*0.1, self.screen_height*0.4)
            new_pipe = Pipe(gap_y, self.screen_width, self.screen_height, self.scale_ratio)
            self.pipes.append(new_pipe)
            return
        last_position = self.pipes[-1].position_x
        if last_position < self.screen_width * 0.5:
            gap_y = random.randint(self.screen_height*0.1, self.screen_height*0.4)
            new_pipe = Pipe(gap_y, self.screen_width, self.screen_height, self.scale_ratio)
            self.pipes.append(new_pipe)

    def get_game_state(self):
        # return relevant game state information for AI decision making
        next_pipe = None
        for pipe in self.pipes:
            if pipe.position_x + pipe.top_sprite.get_width() >= self.bird.position_x:
                next_pipe = pipe
                break
        
        state = {
            'bird_y': self.bird.position_y,
            'bird_velocity': self.bird.acceleration,
            'bird_x': self.bird.position_x,
            'pipe_x': next_pipe.position_x,
            'pipe_gap_y': next_pipe.gap_y,
            'pipe_gap_height': next_pipe.gap_height,
            'pipe_speed': next_pipe.speed
        }
        return state
