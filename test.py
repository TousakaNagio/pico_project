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
    climbing_speed = 5.85 + 0
    low_speed = 5.65 + 0.05
    falling_speed = 5.72
    
    global start_turn_distance, turn_left_distance, mid_turn_distance, end_turn_distance, falling_distance
    start_turn_distance = 100
    mid_turn_distance = 300
    turn_left_distance = 720
    end_turn_distance = 150
    falling_distance = 1400
    
    global steering
    steering = Servo2(pin = 6)
    steering.zero()
    
    global brake_l, brake_r, r_ang, l_ang, r_fall, l_fall #left #right
    brake_l = Servo2(pin = 3)
    brake_l.release()
    brake_r = Servo2(pin = 4)
    brake_r.release(ang = 100)
    r_ang = 150
    l_ang = 55
    r_fall = 110
    l_fall = 65

    
    global IR_front, IR_back
    IR_front = IRs(pin1 = 11, pin2 = 12, pin3 = 13, pin4 = 14, pin5 = 15) #will change
    IR_back = IRs(pin1 = 22, pin2 = 18, pin3 = 23, pin4 = 19, pin5 = 25)
    
    

def start():
    while not switch.value():
        print('Waiting to start')
        utime.sleep(0.005)
        continue
    pass

def main():
    
    init()
    start()
    fan.update(falling_speed)
    
        # 8th stage
    print('stage 8')
    brake_l.brake(ang = l_ang)
    brake_r.brake(ang = r_ang)
    utime.sleep(2)
    brake_l.release()
    brake_r.release()
#     brake.fall()
#     brake1.fall()
    steering.zero()
    
    # 9th stage
    print('stage 9')
    fan.update(falling_speed)
    photo.zero()
    count = 0
    IR_b_mode = 0
    d1 = 0
    delta_d1 = 0
    delta_d2 = 0
    
    while True:
        utime.sleep(0.001)
        d = photo.count_distance()
        count += 1
        if count == 20.0:
            delta_d2 = d - d1
            print(delta_d2-delta_d1)
            fan_speed = falling_speed+(delta_d2-delta_d1)/50.0 
            delta_d1 = delta_d2
            if fan_speed < climbing_speed and fan_speed > low_speed:
                print(fan_speed)
                fan.update(fan_speed)
            elif fan_speed >= climbing_speed:
                print(climbing_speed)
                fan.update(climbing_speed-0.05)
            elif fan_speed <= low_speed:
                print(low_speed)
                fan.update(low_speed)
            delta_d2 = 0
            d1 = d
            count = 0
        utime.sleep(0.005)
#         print(d)
        
        if d >= falling_distance:
            fan.update(5.5)
            utime.sleep(1.5)
            brake_l.brake(ang = l_ang)
            brake_r.brake(ang = r_ang)
            utime.sleep(2)
            brake_l.release()
            brake_r.release()
            break
        
        IR_f = IR_front.values()
        IR_b = IR_back.values()

        if IR_b[1] == 1 and IR_b[3] == 0:
            IR_b_mode = 1
        elif IR_b[1] == 0 and IR_b[3] == 1:
            IR_b_mode = 3
        
        elif IR_b[3] == 1 and IR_b[1] == 1 and sum(IR_f) != 0:
            IR_b_mode = 0
#         if IR_b[3] == 1 and IR_b[1] == 1 and sum(IR_f) == 0:
#         IR_b_mode = 2
       
        if  IR_b_mode == 3 :
            if IR_f[0] == 1:
                steering.left(add = 15)
            if IR_f[1] == 1 :
                steering.left(add = 5)
            if IR_f[2] == 1:
                steering.left(add = 5)
            if IR_f[3] == 1:
                steering.right(add = 5)
            if IR_f[4] == 1:
                steering.right(add = 10)
                
        elif  IR_b_mode == 1 :
            if IR_f[0] == 1:
                steering.right(add = 10)
            if IR_f[1] == 1 :
                steering.right(add = 5)
            if IR_f[2] == 1:
                steering.left(add = 5)
            if IR_f[3] == 1:
                steering.left(add = 5)
            if IR_f[4] == 1:
                steering.left(add = 15)
        
        elif  IR_b_mode == 0 :
            if IR_f[0] == 1:
                steering.right(add = 5)
            if IR_f[1] == 1 :
                steering.right(add = 5)
            if IR_f[2] == 1:
                steering.zero()
            if IR_f[3] == 1:
                steering.left(add = 5)
            if IR_f[4] == 1:
                steering.left(add = 5)
    
    # final stage
    print('final stage')
    fan.update(5.5)
    utime.sleep(1)
    brake_l.brake(ang = l_ang)
    brake_r.brake(ang = r_ang)
    utime.sleep(2)
    brake_l.release()
    brake_r.release()
    init()
    print('Congratulation !!')
     
main()



