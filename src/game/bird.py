from render.sprite_helper import get_bird_sprite
import pygame

class Bird:
    position_x: int
    position_y: int
    acceleration: float
    
    def __init__(self, scale_ratio: int):
        self.position_x = 50
        self.position_y = 100
        self.acceleration = 0.0
        self.sprite = get_bird_sprite(scale_ratio)

    def flap(self):
        self.acceleration = -10.0
        
    def update(self, dt):
        self.position_y += self.acceleration * dt * 60
        if self.position_y <= 0:
            self.position_y = 0
            self.acceleration = 0.0
        self.acceleration += 1.0 * dt * 60
        if self.acceleration > 15.0:
            self.acceleration = 15.0
        
    def render(self, screen):
        screen.blit(self.sprite, (self.position_x, self.position_y))