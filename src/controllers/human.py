from game.controller import Controller

class HumanController(Controller):
    def decide_flap(self, game_state: dict, input_state: dict | None):
        if input_state is None:
            return False
        return bool(input_state.get("flap", False))