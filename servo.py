from machine import Pin, PWM
from utime import sleep
import utime

class Servo:
    def __init__(self, pin = 15, freq = 50, step = 20):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(freq)
        self.step = step
        
        self.MIN = 1040000
        self.MAX = 1540000#2370000
        self.turn = (self.MAX - self.MIN)//self.step
        
    
    def test_mode(self):
        while True:
            for i in range(self.step):
                self.pwm.duty_ns(self.MIN + self.turn*i)
                utime.sleep(0.05)
                
            for i in range(self.step):
                self.pwm.duty_ns(self.MAX - self.turn*i)
                utime.sleep(0.05)
                
    def zero(self):
        self.pwm.duty_ns(self.MIN)
        utime.sleep(2)
        
    def __del__(self):
        self.pwm.duty_ns(0)
