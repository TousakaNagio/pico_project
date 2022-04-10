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
    falling_speed = 5.70
    
    global start_turn_distance, turn_left_distance, mid_turn_distance, end_turn_distance, falling_distance
    start_turn_distance = 100
    mid_turn_distance = 300
    turn_left_distance = 720
    end_turn_distance = 150
    falling_distance = 1500
    
    global steering
    steering = Servo2(pin = 6)
    steering.zero()
    
    global brake
    brake = Servo2(pin = 4)
    brake.release()
    
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
    brake.brake()
    utime.sleep(2)
    brake.release()
    steering.zero()
    
    # 9th stage
    print('stage 9')
    fan.update(falling_speed)
    photo.zero()
    count = 0
    timer = time.time()
    while True:
        print(time.time() - timer)
        utime.sleep(0.001)
        IR_f = IR_front.values()
        IR_b = IR_back.values()
        
        d = photo.count_distance()
        utime.sleep(0.005)
        print(d)
        if d >= falling_distance or time.time() - timer > 18:
            break

        if d <= 400:
            if sum(IR_b) == 2 or sum(IR_f) >= 2:
                count += 1
                brake.brake()
                utime.sleep(0.5)
                brake.release()
                utime.sleep(0.5)
                continue
        else:
            if sum(IR_b)==2 or sum(IR_f) >= 2:
                fan.update(normal_speed)
            
        
        if sum(IR_f) == 0:
            brake.brake()
            utime.sleep(0.5)
#             steering.zero()
#             steering.left(add = 15)
            brake.release()
            utime.sleep(0.6)
        
        if IR_f[2] == 1:
            brake.brake()
            utime.sleep(0.5)
            steering.zero()
            brake.release()
            utime.sleep(0.6)
            
        
        if IR_f[0] == 1:
            brake.brake()
            utime.sleep(0.5)
            steering.left(add = 10)
            brake.release()
            utime.sleep(0.6)
            
        
        
        if IR_f[4] == 1:
            brake.brake()
            utime.sleep(2)
            steering.right(add = 10)
            brake.release()
            utime.sleep(0.6)
            
        
        if IR_f[1] == 1:
            brake.brake()
            utime.sleep(2)
            steering.left(add = 10)
            brake.release()
            utime.sleep(0.6)
            
        
        
        if IR_f[3] == 1:
            brake.brake()
            utime.sleep(2)
            steering.right(add = 10)
            brake.release()
            utime.sleep(0.6)
            
        if IR_b[3] == 1 :
            brake.brake()
            utime.sleep(0.5)
            steering.left(add = 10)
            brake.release()
            utime.sleep(0.50)
            
        
        if IR_b[1] == 1 :
            brake.brake()
            utime.sleep(0.5)
            steering.right(add = 10)
            brake.release()
            utime.sleep(0.50)
            
    
    # final stage
    print('final stage')
    fan.update(5.5)
    utime.sleep(1)
    init()
    print('Congratulation !!')
     
main()


