from machine import Pin, PWM
import utime, time
from servo import Servo
from servo2 import Servo2
from bldc import BLDC
from PID import PID
from photo import Photo
from IR import IRs
from track import track
        
    
def init():
    
    global switch
    switch = Pin(0, Pin.IN, Pin.PULL_DOWN)
    
    global photo
    photo = Photo(pin = 2)
    
    global fan
    fan = BLDC(pin = 10)
    
    global start_turn_distance, normal_speed, climbing_speed
    start_turn_distance = 80
    normal_speed = 5.70
    climbing_speed = 5.83
    
    global steering
    steering = Servo2(pin = 6)
    steering.zero()
    
    global brake
    brake = Servo2(pin = 4)
    brake.release()
    
    global IR_front, IR_back
    IR_front = IRs(pin1 = 11, pin2 = 12, pin3 = 13, pin4 = 14, pin5 = 15) #will change
    IR_back = IRs(pin1 = 21, pin2 = 22, pin3 = 23, pin4 = 24, pin5 = 25)
    
    

def start():
    while not switch.value():
        print('Waiting to start')
        utime.sleep(0.005)
        continue
    pass

def main():
    
    init()
    start()
    
    # First step: Go ahead
    print('Stage 1')
    fan.update(normal_speed)
    while True:
        d = photo.count_distance()
        utime.sleep(0.005)
        print(d)
        if d >= start_turn_distance:
            break
    
    # Second step: Turn left
    print('Stage 2')
    fan.update(5.65)
    for i in range(1):
        steering.turn_left()
    utime.sleep(1.5)
    
    # Third step: before track
    print('Stage 3')
    fan.update(normal_speed)
    while True:
        IR_f = IR_front.values()
        if sum(IR_f) == 0:
            print('Not found')
            utime.sleep(0.05)
            
            continue
        else:
            steering.turn_right()
            brake.brake()
            
            utime.sleep(4)
            brake.release()
            steering.turn_left()
            fan.update(climbing_speed)
            break
    
    # Forth step: track
    print('Stage 4')
    steering.zero()
    steering.turn_left()
    fan.update(climbing_speed)
    while True:
        
        utime.sleep(0.001)
        
        IR_f = IR_front.values()
        
#         if sum(IR_f) >= 3:
#             break
        
        if IR_f[2] == 1 :
            continue
        
        if IR_f[3] == 1 :
            steering.right()
            continue
        
        if IR_f[1] == 1 :
            steering.left()
            continue
        
        if IR_f[4] == 1 :
            steering.right()
#             steering.right()
            continue
        
        if IR_f[0] == 1 :
            steering.left()
#             steering.left()
            continue
    
    
#     setpoint = 5.8
#     pid = PID(0.9, 0.1, 0.05, setpoint=setpoint)
#     fan.turn()
#     start()
#     v = fan.update()
#     while True:
#         control = pid(v)
#         v = fan.update(control)
#     while True:
#         #led.toggle()
#         #time.sleep_ms(1000)
#     motor = BLDC(Min = 1190250, Max = 1297500)
#     motor.test_mode()
#     servo = Servo2()
#     servo.test_mode()
#     print('debug')
#     servo.zero()
     
main()
