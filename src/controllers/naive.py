from game.controller import Controller

class NaiveController(Controller):
    def __init__(self, scale_ratio: int, unscaled_height: int):
        self.scale_ratio = scale_ratio
        self.screen_height = unscaled_height * scale_ratio
        self.margin = 10 * scale_ratio
        self.gravity = 1.0 / 6.0 * scale_ratio
        self.max_lookahead = 0.6
        self.bird_size = 14 * scale_ratio

    def decide_flap(self, game_state: dict, input_state: dict | None):
        bird_y = game_state['bird_y']
        bird_x = game_state['bird_x']
        bird_velocity = game_state['bird_velocity']
        pipe_x = game_state['pipe_x']
        pipe_gap_y = game_state['pipe_gap_y']
        pipe_gap_height = game_state['pipe_gap_height']
        pipe_speed = game_state['pipe_speed']

        # No pipe, maintain vertical center
        if pipe_x is None or pipe_speed is None or pipe_speed <= 0:
            target_y = self.screen_height * 0.5
            return bird_y > target_y and bird_velocity > 0

        dx = pipe_x - bird_x
        t = min(dx / pipe_speed, self.max_lookahead)

        y_pred = bird_y + bird_velocity * t + 0.5 * self.gravity * t * t - self.bird_size // 2
        target_y = pipe_gap_y + pipe_gap_height / 2

        return y_pred > target_y - self.margin