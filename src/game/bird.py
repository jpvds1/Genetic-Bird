

class Bird:
    position_x: int
    position_y: int
    acceleration: float
    
    def __init__(self):
        self.position_x = 0
        self.position_y = 0
        self.acceleration = 0.0
        
    def flap(self):
        self.acceleration = -5.0
        
    def update(self):
        self.position_y += self.acceleration
        self.acceleration += 0.5
        
    def render(self):
        print(f"Bird at ({self.position_x}, {self.position_y}) with acceleration {self.acceleration}")