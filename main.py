from machine import Pin, PWM
import utime
from servo import Servo
from servo2 import Servo2
from bldc import BLDC
        
    
def init():
    global servo
    servo = Servo()
    servo.zero()
    
    #global switch
    #switch = Pin(0, Pin.IN, Pin.PULL_DOWN)
    

def start():
    while not switch.value():
        continue
    pass

def main():
    init()
    
    #start()
    #motor = BLDC(Min = 1190250, Max = 1297500)
    #motor.test_mode()
    #servo = Servo2()
    servo.test_mode()
    #servo.zero()
     
main()
