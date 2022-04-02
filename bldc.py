from machine import Pin, PWM
from utime import sleep
import utime

#setting: 5.5 start: 5.65

class BLDC:
    def __init__(self, pin = 15, freq = 50, step = 20, Min = 5.5*65025/100, Max = 8.5*65025/100): #1040000/2370000
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(freq)
        self.step = step
        
        self.MIN = int(Min)
        self.MAX = int(Max)
        self.turn = (self.MAX - self.MIN)//self.step
        
    
    def test_mode(self):
        while True:
            duty = float(input('Input duty cycle: '))
            chrust = int(duty*65025/100)
            print(chrust)
            self.pwm.duty_u16(chrust)
            utime.sleep(5)
#             print("start")
#             for i in range(self.step):
#                 print(self.MIN + self.turn*i)
#                 self.pwm.duty_u16(int(self.MIN + self.turn*i))
#                 utime.sleep(5)
#             print("end")
            
    def __del__(self):
        self.pwm.duty_u16(self.MIN)
        
    def zero(self):
        self.pwm.duty_u16(self.MIN)
    

