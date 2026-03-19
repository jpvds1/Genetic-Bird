from enum import Enum, auto
import time

from game.game import Game
from controllers.naive import NaiveController
from controllers.genetic import GeneticController
from controllers.human import HumanController

class OrchestratorState(Enum):
    IDLE     = auto()
    PLAYING  = auto()
    TRAINING = auto()
    VIEWING  = auto()
    FINISHED = auto()

class TrainLimitType(Enum):
    TIME       = auto()
    ITERATIONS = auto()

class Orchestrator:
    def __init__(self, unscaled_height: int, unscaled_width: int, scale_ratio: int, frame_time: float):
        self.unscaled_width = unscaled_width
        self.unscaled_height = unscaled_height
        self.scale_ratio = scale_ratio
        self.frame_time = frame_time

        self.state = OrchestratorState.IDLE
        self.game: Game = None
        self.controller = None

        self.visible = False
        
        self.iteration_limit = 0
        self.time_limit = 0.0
        self.iteration = 0
        self.start_time = 0.0

        self.best_score = 0
        self.results = []

        self.current_controller_name = None
        self.train_limit_type = None

    def _create_game(self):
        return Game(
            self.unscaled_height,
            self.unscaled_width,
            self.scale_ratio,
            self.frame_time
        )

    def build_controller(self, controller_name):
        if controller_name == "Naive":
            return NaiveController(self.scale_ratio)
        elif controller_name == "Genetic Algorithm":
            return GeneticController(self.scale_ratio)
        elif controller_name == "Human":
            return HumanController()
        else:
            return None

    def start_human_game(self):
        self.game = self._create_game()
        self.controller = HumanController()
        self.state = OrchestratorState.PLAYING
        self.visible = True
        self.current_controller_name = "Human"

    def start_ai_view(self, model_name: str):
        self.game = self._create_game()
        self.controller = self.build_controller(model_name)
        self.state = OrchestratorState.VIEWING
        self.visible = True
        self.current_controller_name = model_name

    def start_training_iterations(self, model_name: str, iteration_limit: int):
        self.game = self._create_game()
        self.controller = self.build_controller(model_name)
        self.state = OrchestratorState.TRAINING
        self.visible = False

        self.current_controller_name = model_name
        self.train_limit_type = TrainLimitType.ITERATIONS
        self.iteration_limit = max(1, iteration_limit)
        self.time_limit = 0.0
        self.iteration = 0
        self.start_time = time.time()
        self.results.clear()
        self.best_score = 0

        print(f"Started training {model_name}")
        print(f"Iterations limit {self.iteration_limit}")

    def start_training_time(self, model_name: str, time_limit: float):
        self.game = self._create_game()
        self.controller = self.build_controller(model_name)
        self.state = OrchestratorState.TRAINING
        self.visible = False

        self.current_controller_name = model_name
        self.train_limit_type = TrainLimitType.TIME
        self.time_limit = max(0.01, time_limit)
        self.iteration_limit = 0
        self.iteration = 0
        self.start_time = time.time()
        self.results.clear()
        self.best_score = 0

        print(f"Started training {model_name}")
        print(f"Time limit: {self.time_limit}")

    def stop(self):
        self.state = OrchestratorState.IDLE
        self.game = None
        self.controller = None
        self.visible = False

    def is_running(self) -> bool:
        return self.state in {
            OrchestratorState.PLAYING,
            OrchestratorState.VIEWING,
            OrchestratorState.TRAINING,
        }

    def is_finished(self) -> bool:
        return self.state == OrchestratorState.FINISHED

    def get_visible_game(self) -> Game | None:
        if self.visible:
            return self.game
        return None

    def get_training_summary(self) -> dict:
        elapsed = 0.0
        if self.start_time > 0:
            elapsed = time.time() - self.start_time

        avg_score = sum(self.results) / len(self.results) if self.results else 0.0

        return {
            "iterations": self.iteration,
            "elapsed_time": elapsed,
            "best_score": self.best_score,
            "average_score": avg_score,
            "results_count": len(self.results),
            "model": self.current_controller_name
        }

    def _finish_episode(self):
        if self.game is None:
            return

        score = self.game.score
        self.results.append(score)
        self.best_score = max(self.best_score, score)
        self.iteration += 1

    def _training_should_stop(self) -> bool:
        if self.train_limit_type == TrainLimitType.ITERATIONS:
            return self.iteration >= self.iteration_limit
        
        if self.train_limit_type == TrainLimitType.TIME:
            elapsed = time.time() - self.start_time
            return elapsed >= self.time_limit

        return True

    def _restart_training_episode(self):
        print(f"Restarting training episode. Iteration: {self.iteration}")
        self.game = self._create_game()

    # Return True while current session still active
    # Return False when current session has ended
    def update(self, dt: float, input_state: dict | None = None):
        if self.state == OrchestratorState.IDLE:
            return False

        if self.game is None or self.controller is None:
            self.state = OrchestratorState.FINISHED
            return False

        game_state = self.game.get_game_state()
        flap = self.controller.decide_flap(game_state, input_state)
        alive = self.game.update(dt, flap)

        if alive:
            return True

        if self.state in (OrchestratorState.PLAYING, OrchestratorState.VIEWING):
            self.state = OrchestratorState.FINISHED
            return False

        if self.state == OrchestratorState.TRAINING:
            self._finish_episode()

            if self._training_should_stop():
                print("Reached the end of the training.")
                self.state = OrchestratorState.FINISHED
                return False

            self._restart_training_episode()
            return True

        self.state = OrchestratorState.FINISHED
        return False