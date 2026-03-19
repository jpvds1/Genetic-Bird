from enum import Enum, auto
import time

from game.game import Game
from algorithms.naive import NaivePlayer
from algorithms.genetic import GeneticPlayer

class OrchestratorState(Enum):
    IDLE     = auto()
    PLAYING  = auto()
    TRAINING = auto()
    VIEWING  = auto()
    FINISHED = auto()

class Orchestrator:
    def __init__(self, unscaled_height: int, unscaled_width: int, scale_ratio: int, frame_time: float):
        self.unscaled_width = unscaled_width
        self.unscaled_height = unscaled_height
        self.scale_ratio = scale_ratio
        self.frame_time = frame_time

        self.state = OrchestratorState.IDLE
        self.game = None
        self.controller = None
        
        self.iteration_limit = 0
        self.time_limit = 0
        self.iteration = 0
        self.start_time = 0

        self.best_score = 0
        self.results = []

    def build_controller(self, model_name):
        if model_name == "Naive":
            return NaivePlayer(self.scale_ratio)
        elif movel_name == "Genetic Algorithm":
            return GeneticPlayer(self.scale_ratio)
        else:
            return None

    def request_game(self):
        self.game = Game(self.unscaled_height, self.unscaled_width, self.scale_ratio, self.frame_time)
        self.state = OrchestratorState.PLAYING

    def request_train(self, model, iteration, time):
        self.game = Game(self.unscaled_height, self.unscaled_width, self.scale_ratio, self.frame_time, self.model)
        self.state = OrchestratorState.TRAINING
        self.start_time = time.now()
        self.iteration = 0
        self.iteration_limit = iteration
        self.time_limit = time

    def update(self):
        if self.state == OrchestratorState.PLAYING:
            self.game.update()
        elif self.state == OrchestratorState.TRAINING:
            elapsed_time = time.now() - self.start_time
            if elapsed_time >= self.time_limit:
                self.game.early_stop()
                self.state = OrchestratorState.IDLE
                return False
            
            game_state = game.update()

            if game_state == False:
                if self.iteration_limit > self.iteration:
                    self.iteration += 1
                    self.game = Game(self.unscaled_height, self.unscaled_width, self.scale_ratio, self.frame_time, self.model)
                else:
                    return False
