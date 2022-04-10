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
    
    global normal_speed, climbing_speed, low_speed, falling_speed
    normal_speed = 5.70 + 0.05
    climbing_speed = 5.85 + 0.05
    low_speed = 5.65 + 0.05
    falling_speed = 5.75
    
    global start_turn_distance, turn_left_distance, mid_turn_distance, end_turn_distance, falling_distance
    start_turn_distance = 100
    mid_turn_distance = 300
    turn_left_distance = 720
    end_turn_distance = 150
    falling_distance = 900
    
    global steering
    steering = Servo2(pin = 6)
    steering.zero()
    
    global brake
    brake = Servo2(pin = 4)
    brake.release()
    
    global IR_front, IR_back
    IR_front = IRs(pin1 = 11, pin2 = 12, pin3 = 13, pin4 = 14, pin5 = 15) #will change
    IR_back = IRs(pin1 = 22, pin2 = 20, pin3 = 23, pin4 = 21, pin5 = 25)
    
    

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
    photo.zero()
    while True:
        d = photo.count_distance()
        utime.sleep(0.005)
        print(d)
        if d >= start_turn_distance:
            break
    
    # Second step: Turn left
    print('Stage 2')
    fan.update(low_speed)
    for i in range(1):
        steering.turn_left()
    photo.zero()
    while True:
        d = photo.count_distance()
        utime.sleep(0.005)
        print(d)
        if d >= turn_left_distance:
            break
    
    # Third step: before track
    print('Stage 3')
    fan.update(normal_speed)
    
    while True:
        utime.sleep(0.05)
        IR_f = IR_front.values()
        if sum(IR_f) == 0:
            print('Not found')
        else:
            print('Start tracking 1')
            break
    steering.zero()
    
    # Forth step: track
    print('stage 4')
    
    fan.update(low_speed)
    brake.brake()
    steering.zero()
    utime.sleep(4.0)
    brake.release()
    fan.update(climbing_speed)
    
    while True:
        
        utime.sleep(0.001)
        
        IR_f = IR_front.values()
        
        if sum(IR_f) >= 4:
            utime.sleep(0.5)
            print('pass first line')
            break
        
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
    
    brake.brake()
    steering.zero()
    utime.sleep(0.5)
#     utime.sleep(1)
    brake.release()
        
    # 5th stage
    print('stage 5')
    fan.update(climbing_speed)
    steering.left(35)
#         utime.sleep(1)
    photo.zero()
    while True:
        d = photo.count_distance()
        utime.sleep(0.005)
        print(d)
        if d >= mid_turn_distance:
            break
    steering.zero()
#     photo.zero()
#     while True:
#         d = photo.count_distance()
#         utime.sleep(0.005)
#         print(d)
#         if d >= 50:
#             break
#     steering.right()
#     photo.zero()
#     while True:
#         d = photo.count_distance()
#         utime.sleep(0.005)
#         print(d)
#         if d >= mid_turn_distance:
#             break
    
    # 6th stage
    print('stage 6')
    fan.update(climbing_speed)
    
    while True:
        utime.sleep(0.05)
        IR_f = IR_front.values()
        if IR_f[0] == 1:
            break
        else:
            print('Not found')
    
    steering.right(35)
    utime.sleep(0.3)
    steering.zero()
    
    # 7th stage
    print('stage 7')
    count = 0
    fan.update(climbing_speed)
    photo.zero()
    while True:
        utime.sleep(0.001)
        IR_f = IR_front.values()
        
        d = photo.count_distance()
        utime.sleep(0.005)
        print(d)
        if d >= end_turn_distance:
            break
        
#         if sum(IR_f) >= 4:
#             utime.sleep(1.5)
#             print('pass third line')
#             fan.update(normal_speed)
#             brake.brake()
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
    
    
    
    # 8th stage
    print('stage 8')
    brake.brake()
    utime.sleep(2)
    brake.release()
    steering.zero()
    
    # 9th stage
    print('stage 9')
    fan.update(falling_speed)
    photo.zero()
    while True:
        utime.sleep(0.001)
        IR_f = IR_front.values()
        IR_b = IR_back.values()
        
        d = photo.count_distance()
        utime.sleep(0.005)
        print(d)
        if d >= falling_distance:
            break

#             if IR_f[2] == 1 :
#                 continue
        if sum(IR_f) >= 2:
            steering.zero()
            continue
            
            
        if IR_b[3] == 1 :
            steering.left()
            continue
        
        if IR_b[1] == 1 :
            steering.right()
            continue
        
        if IR_f[0] == 1:
            steering.left(add = 30)
            continue
        
        if IR_f[4] == 1:
            steering.right(add = 30)
            continue
#             if IR_f[4] == 1 :
#                 steering.right()
#     #             steering.right()
#                 continue
#             
#             if IR_f[0] == 1 :
#                 steering.left()
#     #             steering.left()
#                 continue
    
    # final stage
    print('final stage')
    fan.update(5.5)
    utime.sleep(1)
    brake.brake()
    utime.sleep(1)
    brake.release()
    init()
    print('Congratulation !!')
    
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
     
main()
