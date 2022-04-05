from machine import Pin, PWM
import utime, time
from servo import Servo
from servo2 import Servo2
from bldc import BLDC
from PID import PID
        
    
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
    setpoint = 5.8
    pid = PID(0.9, 0.1, 0.05, setpoint=setpoint)
#     fan.turn()
#     start()
    v = fan.update()
    while True:
        control = pid(v)
        v = fan.update(control)
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
