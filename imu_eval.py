# Example code for PiicoDev Motion Sensor MPU6050
from PiicoDev_MPU6050 import PiicoDev_MPU6050
from PiicoDev_Unified import sleep_ms # Cross-platform compatible sleep function
from machine import Pin

motion = PiicoDev_MPU6050(bus = 0, freq = 100000, sda = Pin(8), scl = Pin(9))
count = 0
while True:
    count += 1
    if count > 200:
        break
    # Accelerometer data
    accel = motion.read_accel_data() # read the accelerometer [ms^-2]
    aX = accel["x"]
    aY = accel["y"]
    aZ = accel["z"]
    #print("x:" + str(aX) + " y:" + str(aY) + " z:" + str(aZ))
    
    # Gyroscope Data
    gyro = motion.read_gyro_data()   # read the gyro [deg/s]
    gX = gyro["x"]
    gY = gyro["y"]
    gZ = gyro["z"]
    print("x:" + str(gX) + " y:" + str(gY) + " z:" + str(gZ))
    
    # Rough temperature
#     temp = motion.read_temperature()   # read the device temperature [degC]
#     print("Temperature: " + str(temp) + "°C")

    # G-Force
#     gforce = motion.read_accel_abs(g=True) # read the absolute acceleration magnitude
#     print("G-Force: " + str(gforce))
    
    sleep_ms(100)