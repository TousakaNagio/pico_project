from PiicoDev_MPU6050 import PiicoDev_MPU6050
from PiicoDev_Unified import sleep_ms # Cross-platform compatible sleep function
from machine import Pin
from kalman import KalmanAngle
import time
import math
from servo2 import Servo2

motion = PiicoDev_MPU6050(bus = 0, freq = 400000, sda = Pin(8), scl = Pin(9))

count = 0
timer = time.time()
gyroScale = 131

while True:
    count += 1
    if count > 300:
        break
    
    #Read Accelerometer raw value
    accel = motion.read_accel_data() # read the accelerometer [ms^-2]
    accX = accel["x"]
    accY = accel["y"]
    accZ = accel["z"]

    #Read Gyroscope raw value
    gyro = motion.read_gyro_data()   # read the gyro [deg/s]
    gyroX = gyro["x"]
    gyroY = gyro["y"]
    gyroZ = gyro["z"]

    dt = time.time() - timer
    timer = time.time()
    
    gsx = gyroX/gyroScale
    gsy = gyroY/gyroScale
    gsz = gyroZ/gyroScale
    
    arx = (180/3.141592) * math.atan(accX / math.sqrt(accY**2 + accZ**2)); 
    ary = (180/3.141592) * math.atan(accY / math.sqrt(accX**2 + accZ**2));
    arz = (180/3.141592) * math.atan(accZ / accY);
    
    if count == 1:
        grx = arx;
        gry = ary;
        grz = arz;
        
    else:
        grx = grx + (dt * gsx);
        gry = gry + (dt * gsy);
        grz = grz + (dt * gsz);
        
    rx = (0.96 * arx) + (0.04 * grx);
    ry = (0.96 * ary) + (0.04 * gry);
    rz = (0.96 * arz) + (0.04 * grz);
    
    #print(rx, ry, rx)
    print(ary, gry, ry)
    time.sleep(0.05)
    
    
    
    
