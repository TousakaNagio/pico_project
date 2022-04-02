from machine import Pin, PWM
import utime, time
from servo import Servo
from servo2 import Servo2
from bldc import BLDC
        
    
def init():
#     global servo
#     servo = Servo2()
#     servo.zero()
    
    global switch
    switch = Pin(0, Pin.IN, Pin.PULL_DOWN)
    
    global led
    led = Pin(25, Pin.OUT)
    
    global fan
    fan = BLDC()
    

def start():
    while not switch.value():
        continue
    pass

def main():
    
    init()
    start()
#     fan.test_mode()
    #while True:
        #led.toggle()
        #time.sleep_ms(1000)
    #motor = BLDC(Min = 1190250, Max = 1297500)
    #motor.test_mode()
    #servo = Servo2()
    #servo.test_mode()
    #print('debug')
    #servo.zero()
     
main()
