from render.sprite_helper import get_bird_sprite, rotate_sprite
import pygame

class Bird:
    position_x: int
    position_y: int
    acceleration: float
    
    def __init__(self, scale_ratio: int):
        self.position_x = 8 * scale_ratio
        self.position_y = 50 * scale_ratio
        self.acceleration = 0.0
        self.sprite = get_bird_sprite(scale_ratio)

    def flap(self):
        self.acceleration = -10.0
        if self.acceleration < -15.0:
            self.acceleration = -15.0
        
    def update(self, dt):
        self.position_y += self.acceleration * dt * 60
        if self.position_y <= 0:
            self.position_y = 0
            self.acceleration = 0.0
        self.acceleration += 1.0 * dt * 60
        if self.acceleration > 15.0:
            self.acceleration = 15.0
        
    def render(self, screen):
        rotated_sprite, rect = rotate_sprite(self.sprite, -self.acceleration * 2, (self.position_x + self.sprite.get_width() // 2, self.position_y + self.sprite.get_height() // 2))
        screen.blit(rotated_sprite, rect.topleft)