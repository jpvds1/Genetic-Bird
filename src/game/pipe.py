import pygame

class Pipe:
    position_x: int
    gap_y: int
    gap_height: int
    offscreen: bool = False
    
    def __init__(self, gap_y: int, gap_height: int, screen_width: int):
        self.position_x = screen_width
        self.gap_y = gap_y
        self.gap_height = gap_height
        
    def update(self, dt):
        self.position_x -= 2 * dt * 60
        if self.position_x < -50:
            self.offscreen = True
        
    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(self.position_x, 0, 50, self.gap_y))
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(self.position_x, self.gap_y + self.gap_height, 50, screen.get_height() - (self.gap_y + self.gap_height)))