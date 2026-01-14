import pygame

class Bird:
    position_x: int
    position_y: int
    acceleration: float
    
    def __init__(self):
        self.position_x = 50
        self.position_y = 100
        self.acceleration = 0.0
        
    def flap(self):
        self.acceleration = -6.0
        
    def update(self, dt):
        self.position_y += self.acceleration * dt * 60
        if self.position_y <= 0:
            self.position_y = 0
            self.acceleration = 0.0
        self.acceleration += 0.3 * dt * 60
        if self.acceleration > 15.0:
            self.acceleration = 15.0
        
    def render(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.position_x, self.position_y), 10)