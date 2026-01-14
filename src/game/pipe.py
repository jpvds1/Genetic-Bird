from render.sprite_helper import get_pipe_sprites
from enum import Enum
import pygame

class RewardState(Enum):
    NONE = 0
    AVAILABLE = 1
    COLLECTED = 2

class Pipe:
    position_x: int
    gap_y: int
    gap_height: int
    offscreen: bool = False
    
    def __init__(self, gap_y: int, screen_width: int, scale_ratio: int):
        self.scale_ratio = scale_ratio
        self.position_x = screen_width
        self.gap_y = gap_y
        self.gap_height = 50 * scale_ratio
        self.top_sprite, self.bottom_sprite = get_pipe_sprites(scale_ratio)
        self.state = RewardState.NONE

    def update(self, dt):
        self.position_x -= 10 * dt * 60
        if self.position_x < 8 * self.scale_ratio and self.state == RewardState.NONE:
            self.state = RewardState.AVAILABLE
        if self.position_x < -self.top_sprite.get_width():
            self.offscreen = True
        
    def render(self, screen):
        screen.blit(self.top_sprite, (self.position_x, self.gap_y - self.top_sprite.get_height()))
        screen.blit(self.bottom_sprite, (self.position_x, self.gap_height + self.gap_y))

    def collect_reward(self):
        if self.state == RewardState.AVAILABLE:
            self.state = RewardState.COLLECTED
            return 1
        return 0