from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path

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

    def save(self, path: str | Path) -> None:
        """Persists the controller's state to *path*."""
        pass

    def load(self, path: str | Path) -> None:
        """Restore the controller's state from *path*."""
        pass

    @property
    def supports_checkpointing(self) -> bool:
        """Return True if this controller has overridden save/load."""
        return (
            type(self).save is not Controller.save
            or type(self).load is not Controller.load
        )

    def get_parallel_tasks(self) -> list:
        """Retuns a list of opaque task data to be distributed to workers."""
        pass

    @staticmethod
    def evaluate_task(task_data, game_params: dict, seed: int) -> int:
        """"Runs a single simulation. Returns score."""
        return NotImplementedError