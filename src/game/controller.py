from __future__ import annotations
from abc import ABC, abstractmethod


class Controller(ABC):
    @abstractmethod
    def decide_flap(self, game_state: dict, input_state: dict | None = None) -> bool:
        raise NotImplementedError