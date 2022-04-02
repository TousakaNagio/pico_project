from machine import Pin, PWM
from utime import sleep
import utime

class Servo2:
    def __init__(self, pin = 14, freq = 50, step = 36):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(freq)
        self.step = step
        
        self.MIN = 1350
        self.MAX = 8200
        self.turn = (self.MAX - self.MIN)//self.step
        self.CUR = (self.MIN+self.MAX)//2
        
    
    def test_mode(self):
        while True:
            for i in range(self.step//2):
                self.pwm.duty_u16(self.MIN + self.turn*i)
                utime.sleep(0.05)
                
            for i in range(self.step):
                #self.pwm.duty_u16(self.MAX - self.turn*i)
                utime.sleep(0.05)
                
    def zero(self):
        self.CUR = (self.MIN+self.MAX)//2
        self.pwm.duty_u16(self.CUR)
        utime.sleep(2)
    
    def target(self, tar):
        
        print(tar)
        
        if tar < 0:
            self.CUR = self.MIN
            self.pwm.duty_u16(self.CUR)
            utime.sleep(0.005)
        elif (tar > 180):
            self.CUR = self.MAX
            self.pwm.duty_u16(self.CUR)
            utime.sleep(0.005)
        else:
            tar = tar // 5
            print(tar)
            self.CUR = self.MIN + self.turn * tar
            print(self.CUR)
            self.pwm.duty_u16(int(self.CUR))
            utime.sleep(0.005)
            
        
    def __del__(self):
        self.pwm.duty_ns(0)

