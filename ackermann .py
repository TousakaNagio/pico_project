from servo2 import Servo2
import math

class Ackermann:
    def __init__(self, pin_left = 1, pin_right = 2):
        
        self.left = Servo2(pin = pin_left)
        self.right = Servo2(pin = pin_right)
        self.left.zero()
        self.right.zero()
        
        self.K = 140
        self.L = 220
        self.left_ang = 95
        self.right_ang = 95
        
    def zero(self):
        self.left.zero()
        self.right.zero()
    
    def turn_left(self, beta = 0):
        if beta == 0:
            self.zero()
        else:
            alpha = math.degrees(math.atan(1 / (1 / math.tan(math.radians(beta)) - self.K / self.L)))
            self.left.left(add = alpha)
            self.right.left(add = beta)
    
    def turn_right(self, beta = 0):
        if beta == 0:
            self.zero()
        else:
            alpha = math.degrees(math.atan(1 / (1 / math.tan(math.radians(beta)) - self.K / self.L)))
            self.left.right(add = beta)
            self.right.right(add = alpha)
                
        
        
        