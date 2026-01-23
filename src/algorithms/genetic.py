class GeneticPlayer:
    def __init__(self, scale_ratio: int):
        self.scale_ratio = scale_ratio
        self.margin = 15 * scale_ratio
        self.flap_cooldown = 0.2  # seconds
        self.time_since_last_flap = 0.0

    def decide_flap(self, game_state):
        bird_y = game_state['bird_y']
        bird_x = game_state['bird_x']
        bird_velocity = game_state['bird_velocity']
        pipe_x = game_state['pipe_x']
        pipe_gap_y = game_state['pipe_gap_y']
        pipe_gap_height = game_state['pipe_gap_height']
        pipe_speed = game_state['pipe_speed']

        if pipe_x is None:
            return False

        dx = pipe_x - bird_x
        t = dx / pipe_speed # time to reach the pipe
        y_pred = bird_y + bird_velocity * t

        if y_pred < pipe_gap_y + self.margin:
            return True
        return False