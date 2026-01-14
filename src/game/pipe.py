

class Pipe:
    position_x: int
    gap_y: int
    gap_height: int
    offscreen: bool = False
    
    def __init__(self, gap_y: int, gap_height: int, screen_width: int):
        self.position_x = screen_width
        self.gap_y = gap_y
        self.gap_height = gap_height
        
    def update(self):
        self.position_x -= 2
        if self.position_x < -50:
            self.offscreen = True
        
    def render(self):
        print(f"Pipe at x={self.position_x} with gap from y={self.gap_y} to y={self.gap_y + self.gap_height}")