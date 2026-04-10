from __future__ import annotations
from abc import ABC, abstractmethod

class Controller(ABC):

    @property
    def population_size(self) -> int:
        """Override to run multiple agents in parallel."""
        return 1

    @abstractmethod
    def decide_flap(self, game_state: dict, input_state: dict | None = None, agent_index: int = 0) -> bool:
        raise NotImplementedError

    def on_episode_end(self, score: int):
        """Called when a single-agent episode ends."""
        pass

    def on_generation_end(self, scores: list[int]):
        """Called when all parallel agents in a generation have died."""
        pass