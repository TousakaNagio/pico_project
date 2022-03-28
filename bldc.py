from machine import Pin, PWM
from utime import sleep
import utime

class BLDC:
    def __init__(self, pin = 15, freq = 50, step = 20, Min = 1040000, Max = 2370000):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(freq)
        self.step = step
        
        self.MIN = Min
        self.MAX = Max
        self.turn = (self.MAX - self.MIN)//self.step
        
    
    def test_mode(self):
        while True:
            print("start")
            for i in range(self.step):
                print(self.MIN + self.turn*i)
                self.pwm.duty_ns(self.MIN + self.turn*i)
                utime.sleep(5)
            print("end")
            
    def __del__(self):
        self.pwm.duty_ns(0)
    

