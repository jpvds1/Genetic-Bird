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
        self.controller = None

        # Single-agent
        self.game: Game = None

        # Multi-agent
        self.games: list[Game] = []
        self.alive_mask: list[bool] = []
        self.generation_scores: list[int] = []

        self.visible = False
        self.parallel = False
        
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
            return NaiveController(self.scale_ratio, self.unscaled_height)
        elif controller_name == "Genetic Algorithm":
            return GeneticController(self.scale_ratio)
        elif controller_name == "Human":
            return HumanController()
        else:
            return None

    # ----------------------------------------------
    # Start methods
    # ----------------------------------------------
    
    def start_human_game(self):
        self.game = self._create_game()
        self.controller = HumanController()
        self.state = OrchestratorState.PLAYING
        self.visible = True
        self.parallel = False
        self.current_controller_name = "Human"

    def start_ai_view(self, model_name: str):
        self.game = self._create_game()
        self.controller = self.build_controller(model_name)
        self.state = OrchestratorState.VIEWING
        self.visible = True
        self.parallel = False
        self.current_controller_name = model_name

    def _start_training_common(self, model_name: str):
        self.controller = self.build_controller(model_name)
        self.state = OrchestratorState.TRAINING
        self.current_controller_name = model_name
        self.iteration = 0
        self.start_time = time.time()
        self.results.clear()
        self.best_score = 0

        self.parallel = self.controller.population_size > 1

        if self.parallel:
            n = self.controller.population_size
            self.games = [self._create_game() for _ in range(n)]
            self.alive_mask = [True] * n
            self.generation_scores = [0] * n
            self.visible = True
            self.game = None
        else:
            self.game = self._create_game()
            self.games = []
            self.visible = False

    def start_training_iterations(self, model_name: str, iteration_limit: int):
        self._start_training_common(model_name)
        self.train_limit_type = TrainLimitType.ITERATIONS
        self.iteration_limit = max(1, iteration_limit)
        self.time_limit = 0.0

        print(f"Started training {model_name}")
        print(f"Iterations limit {self.iteration_limit}")

    def start_training_time(self, model_name: str, time_limit: float):
        self._start_training_common(model_name)
        self.current_controller_name = model_name
        self.train_limit_type = TrainLimitType.TIME
        self.time_limit = max(0.01, time_limit)
        self.iteration_limit = 0

        print(f"Started training {model_name}")
        print(f"Time limit: {self.time_limit}")

    # ----------------------------------------------
    # State queries
    # ----------------------------------------------

    def stop_training_early(self):
        if self.state == OrchestratorState.TRAINING:
            self.state = OrchestratorState.FINISHED

    def stop(self):
        self.state = OrchestratorState.IDLE
        self.game = None
        self.games = []
        self.controller = None
        self.visible = False
        self.parallel = False

    def get_visible_game(self) -> Game | None:
        if not self.visible:
            return None
        if self.parallel:
            best = None
            best_score = -1
            for i, (game, alive) in enumerate(zip(self.games, self.alive_mask)):
                if alive and game.score > best_score:
                    best_score = game.score
                    best = game
            return best or next((g for g, a in zip(self.games, self.alive_mask) if a), self.games[0] if self.games else None)
        return self.game

    def get_training_status(self) -> dict:
        elapsed = time.time() - self.start_time

        return {
            "model": self.current_controller_name,
            "iteration": self.iteration,
            "best_score": self.best_score,
            "elapsed_time": elapsed,
            "limit_type": self.train_limit_type.name,
            "iteration_limit": self.iteration_limit,
            "time_limit": self.time_limit,
            "parallel": self.parallel,
            "alive_count": sum(self.alive_mask) if self.parallel else 1,
            "population_size": self.controller.population_size if self.controller else 1
        }

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

    def _training_should_stop(self) -> bool:
        if self.train_limit_type == TrainLimitType.ITERATIONS:
            return self.iteration >= self.iteration_limit
        
        if self.train_limit_type == TrainLimitType.TIME:
            elapsed = time.time() - self.start_time
            return elapsed >= self.time_limit

        return True

    # ----------------------------------------------
    # Update
    # ----------------------------------------------

    def update(self, dt: float, input_state: dict | None = None):
        if self.state == OrchestratorState.IDLE:
            return False

        if self.controller is None:
            self.state = OrchestratorState.FINISHED
            return False

        if not self.parallel and self.game is None:
            self.state = OrchestratorState.FINISHED
            return False

        if self.parallel:
            return self._update_parallel(dt)
        else:
            return self._update_single(dt, input_state)

    def _update_single(self, dt: float, input_state: dict | None) -> bool:
        if self.game is None:
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
            score = self.game.score
            self.results.append(score)
            self.best_score = max(self.best_score, score)
            self.iteration += 1
            self.controller.on_episode_end(score)

            if self._training_should_stop():
                self.state = OrchestratorState.FINISHED
                return False

            self.game = self._create_game()
            return True

        self.state = OrchestratorState.FINISHED
        return False

    def _update_parallel(self, dt: float) -> bool:
        any_alive = False

        for i, (game, alive) in enumerate(zip(self.games, self.alive_mask)):
            if not alive:
                continue

            game_state = game.get_game_state()
            flap = self.controller.decide_flap(game_state, None, agent_index=i)
            still_alive = game.update(dt, flap)

            if still_alive:
                any_alive = True
            else:
                self.alive_mask[i] = False
                self.generation_scores[i] = game.score

        if any_alive:
            return True

        # All agents dead -> end of generation
        gen_best = max(self.generation_scores)
        self.results.extend(self.generation_scores)
        self.best_score = max(self.best_score, gen_best)
        self.iteration += 1
        self.controller.on_generation_end(self.generation_scores)

        if self._training_should_stop():
            self.state = OrchestratorState.FINISHED
            return False

        # Reset for next generation
        n = self.controller.population_size
        self.games = [self._create_game() for _ in range(n)]
        self.alive_mask = [True] * n
        self.generation_scores = [0] * n
        return True