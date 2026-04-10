import json
import numpy as np
import random
from pathlib import Path
from game.controller import Controller

_SCHEMA_VERSION = 1

class NeuralNetwork:
    def __init__(self, layer_sizes: list[int]):
        self.layer_sizes = layer_sizes
        self.weights = []
        self.biases = []
        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i + 1]) * 0.5
            b = np.zeros(layer_sizes[i + 1])
            self.weights.append(w)
            self.biases.append(b)

    def forward(self, x: np.ndarray) -> float:
        for i, (w, b) in enumerate(zip(self.weights, self.biases)):
            x = x @ w + b
            if i < len(self.weights) - 1:
                x = np.tanh(x)
            else:
                x = 1.0 / (1.0 + np.exp(-x))
        return float(x.item())

    def get_flat(self) -> np.ndarray:
        parts = [w.flatten() for w in self.weights] + [b.flatten() for b in self.biases]
        return np.concatenate(parts)

    def set_flat(self, flat: np.ndarray):
        idx = 0
        for w in self.weights:
            size = w.size
            w[:] = flat[idx:idx + size].reshape(w.shape)
            idx += size
        for b in self.biases:
            size = b.size
            b[:] = flat[idx:idx + size]
            idx += size

    def clone(self) -> "NeuralNetwork":
        child = NeuralNetwork(self.layer_sizes)
        child.set_flat(self.get_flat().copy())
        return child

    def to_dict(self) -> dict:
        return {
            "layer_sizes": self.layer_sizes,
            "weights": [w.tolist() for w in self.weights],
            "biases": [b.tolist() for b in self.biases]
        }

    @classmethod
    def from_dict(cls, data: dict) -> "NeuralNetwork":
        nn = cls(data["layer_sizes"])
        nn.weights = [np.array(w, dtype=np.float64) for w in data["weights"]]
        nn.biases = [np.array(b, dtype=np.float64) for b in data["biases"]]
        return nn


class GeneticController(Controller):
    SCREEN_H = 195
    SCREEN_W = 143

    def __init__(
        self,
        scale_ratio: int,
        pop_size: int = 30,
        elite_count: int = 4,
        mutation_rate: float = 0.15,
        mutation_strength: float = 0.4,
        tournament_size: int = 4,
    ):
        self.scale_ratio = scale_ratio
        self.pop_size = pop_size
        self.elite_count = elite_count
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength
        self.tournament_size = tournament_size
        self.layer_sizes = [5, 10, 6, 1]
        self.generation = 0
        self.population: list[NeuralNetwork] = [
            NeuralNetwork(self.layer_sizes) for _ in range(pop_size)
        ]

    @property
    def population_size(self) -> int:
        return self.pop_size

    def _normalise(self, game_state: dict) -> np.ndarray:
        sh = self.SCREEN_H * self.scale_ratio
        sw = self.SCREEN_W * self.scale_ratio

        bird_y   = game_state["bird_y"] / sh
        bird_vel = np.clip(game_state["bird_velocity"] / (600 * self.scale_ratio), -1.0, 1.0)

        if game_state["pipe_x"] is None:
            dx, dy, gap_h = 1.0, 0.0, 0.5
        else:
            dx = (game_state["pipe_x"] - game_state["bird_x"]) / sw
            target_y = game_state["pipe_gap_y"] + game_state["pipe_gap_height"] / 2
            dy = (game_state["bird_y"] - target_y) / sh
            gap_h = game_state["pipe_gap_height"] / sh

        return np.array([bird_y, bird_vel, dx, dy, gap_h], dtype=np.float32)

    def decide_flap(self, game_state: dict, input_state: dict | None = None, agent_index: int = 0) -> bool:
        inputs = self._normalise(game_state)
        return self.population[agent_index].forward(inputs) > 0.5

    def on_generation_end(self, scores: list[int]):
        best = max(scores)
        avg  = sum(scores) / len(scores)
        print(f"Gen {self.generation:>4} | best={best:>5} | avg={avg:>6.1f}")

        ranked = sorted(zip(scores, self.population), key=lambda x: x[0], reverse=True)

        new_population: list[NeuralNetwork] = []

        for _, nn in ranked[:self.elite_count]:
            new_population.append(nn.clone())

        while len(new_population) < self.pop_size:
            p1 = self._tournament_select(ranked)
            p2 = self._tournament_select(ranked)
            child = self._crossover(p1, p2)
            self._mutate(child)
            new_population.append(child)

        self.population = new_population
        self.generation += 1

    def _tournament_select(self, ranked: list) -> NeuralNetwork:
        contestants = random.sample(ranked, min(self.tournament_size, len(ranked)))
        return max(contestants, key=lambda x: x[0])[1]

    def _crossover(self, p1: NeuralNetwork, p2: NeuralNetwork) -> NeuralNetwork:
        child = NeuralNetwork(self.layer_sizes)
        f1, f2 = p1.get_flat(), p2.get_flat()
        mask = np.random.rand(len(f1)) > 0.5
        child.set_flat(np.where(mask, f1, f2))
        return child

    def _mutate(self, nn: NeuralNetwork):
        flat = nn.get_flat()
        mask = np.random.rand(len(flat)) < self.mutation_rate
        flat[mask] += np.random.randn(int(mask.sum())) * self.mutation_strength
        nn.set_flat(flat)

    # ----------------------------------------------
    # Persistance
    # ----------------------------------------------

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "controller_type": "GeneticController",
            "version": _SCHEMA_VERSION,
            "generation": self.generation,
            "hyperparameters": {
                "pop_size":          self.pop_size,
                "elite_count":       self.elite_count,
                "mutation_rate":     self.mutation_rate,
                "mutation_strength": self.mutation_strength,
                "tournament_size":   self.tournament_size,
                "layer_sizes":       self.layer_sizes
            },
            "population": [nn.to_dict() for nn in self.population]
        }

        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        tmp.replace(path)

        print(f"Checkpoint saved -> {path} (gen {self.generation})")

    def load(self, path: str | Path) -> None:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"No checkpoint found at '{path}'")

        payload = json.loads(path.read_text(encoding="utf-8"))

        if payload.get("controller_type") != "GeneticController":
            raise ValueError("Checkpoint controller missmatch")
        if payload.get("version", 0) != _SCHEMA_VERSION:
            raise ValueError("Checkpoint schema version missmatch")

        hp = payload.get("hyperparameters", {})
        self.pop_size = hp.get("pop_size", self.pop_size)
        self.elite_count = hp.get("elite_count", self.elite_count)
        self.mutation_rate = hp.get("mutation_rate", self.mutation_rate)
        self.mutation_strength = hp.get("mutation_strength", self.mutation_strength)
        self.tournament_size = hp.get("tournament_size", self.tournament_size)
        self.layer_sizes = hp.get("layer_sizes", self.layer_sizes)

        self.generation = payload.get("generation", 0)
        self.population = [NeuralNetwork.from_dict(d) for d in payload["population"]]

        print(f"Checkpoint loaded (gen {self.generation})")