import math

class Odometry:
    def __init__(self, left_vel = 0, right_vel = 0):
        self.x = 0
        self.y = 0
        self.theta = 0
        self.L = 140
        
    def update(self, d_left = 0, d_right = 0):
        d_center = (d_left + d_right) / 2
        phi = (d_right - d_left) / self.L
        self.x += d_center * math.cos(self.theta + phi / 2)
        self.y += d_center * math.sin(self.theta + phi / 2)
        self.theta = phi
        return self.x, self.y, self.theta