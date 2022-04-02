# Example code for PiicoDev Motion Sensor MPU6050
from PiicoDev_MPU6050 import PiicoDev_MPU6050
from PiicoDev_Unified import sleep_ms # Cross-platform compatible sleep function
from machine import Pin
from kalman import KalmanAngle
import time
import math
from servo2 import Servo2

motion = PiicoDev_MPU6050(bus = 0, freq = 400000, sda = Pin(8), scl = Pin(9))

time.sleep(1)
accel = motion.read_accel_data() # read the accelerometer [ms^-2]
accX = accel["x"]
accY = accel["y"]
accZ = accel["z"]

kalmanX = KalmanAngle()
kalmanY = KalmanAngle()
kalmanZ = KalmanAngle()

RestrictPitch = True  #Comment out to restrict roll to ±90deg instead - please read: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf
radToDeg = 57.2957786
kalAngleX = 0
kalAngleY = 0
kalAngleZ = 0

if (RestrictPitch):
    roll = math.atan2(accY,accZ) * radToDeg
    pitch = math.atan(-accX/math.sqrt((accY**2)+(accZ**2))) * radToDeg
    yaw = math.atan(math.sqrt((accX**2)+(accY**2))/accZ) * radToDeg 
else:
    roll = math.atan(accY/math.sqrt((accX**2)+(accZ**2))) * radToDeg
    pitch = math.atan2(-accX,accZ) * radToDeg
    yaw = math.atan(math.sqrt((accX**2)+(accY**2))/accZ) * radToDeg 


print(roll)
kalmanX.setAngle(roll)
kalmanY.setAngle(pitch)
kalmanZ.setAngle(yaw)
gyroXAngle = roll;
gyroYAngle = pitch;
gyroZAngle = yaw;
compAngleX = roll;
compAngleY = pitch;
compAngleZ = yaw;

timer = time.time()
flag = 0

servo = Servo2()
servo.zero()

count = 0

while True:
    count += 1
    if count == 300:
        break
    if(flag >100): #Problem with the connection
        print("There is a problem with the connection")
        flag=0
        continue
    try:
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

        if (RestrictPitch):
            roll = math.atan2(accY,accZ) * radToDeg
            pitch = math.atan(-accX/math.sqrt((accY**2)+(accZ**2))) * radToDeg
            yaw = math.atan(math.sqrt((accX**2)+(accY**2))/accZ) * radToDeg 
        else:
            roll = math.atan(accY/math.sqrt((accX**2)+(accZ**2))) * radToDeg
            pitch = math.atan2(-accX,accZ) * radToDeg
            yaw = math.atan(math.sqrt((accX**2)+(accY**2))/accZ) * radToDeg 

        #print(roll, pitch, yaw, 'debug') #-0.7612836 -1.890975 2.038414 debug
        gyroXRate = gyroX/131
        gyroYRate = gyroY/131
        gyroZRate = gyroZ/131
        #print(gyroXRate, gyroYRate, gyroZRate, 'debug') #-0.8975001 1.609114 0.3924014 debug

        if (RestrictPitch):

            if((roll < -90 and kalAngleX >90) or (roll > 90 and kalAngleX < -90)):
                kalmanX.setAngle(roll)
                complAngleX = roll
                kalAngleX   = roll
                gyroXAngle  = roll
                kalAngleZ  = kalmanZ.getAngle(yaw,gyroZRate,dt)
            else:
                kalAngleX = kalmanX.getAngle(roll,gyroXRate,dt)
                kalAngleZ  = kalmanZ.getAngle(yaw,gyroZRate,dt)
                

            if(abs(kalAngleX)>90):
                gyroYRate  = -gyroYRate
                kalAngleY  = kalmanY.getAngle(pitch,gyroYRate,dt)
                
                
                
        else:

            if((pitch < -90 and kalAngleY >90) or (pitch > 90 and kalAngleY < -90)):
                kalmanY.setAngle(pitch)
                complAngleY = pitch
                kalAngleY   = pitch
                gyroYAngle  = pitch
                kalAngleZ  = kalmanZ.getAngle(yaw,gyroZRate,dt)
            else:
                kalAngleY = kalmanY.getAngle(pitch,gyroYRate,dt)
                kalAngleZ  = kalmanZ.getAngle(yaw,gyroZRate,dt)
                

            if(abs(kalAngleY)>90):
                gyroXRate  = -gyroXRate
                kalAngleX = kalmanX.getAngle(roll,gyroXRate,dt)


        #angle = (rate of change of angle) * change in time
        gyroXAngle = gyroXRate * dt
        gyroYAngle = gyroYAngle * dt
        gyroZAngle = gyroZAngle * dt

        #compAngle = constant * (old_compAngle + angle_obtained_from_gyro) + constant * angle_obtained from accelerometer
        compAngleX = 0.93 * (compAngleX + gyroXRate * dt) + 0.07 * roll
        compAngleY = 0.93 * (compAngleY + gyroYRate * dt) + 0.07 * pitch
        compAngleZ = 0.93 * (compAngleZ + gyroZRate * dt) + 0.07 * yaw

        if ((gyroXAngle < -180) or (gyroXAngle > 180)):
            gyroXAngle = kalAngleX
        if ((gyroYAngle < -180) or (gyroYAngle > 180)):
            gyroYAngle = kalAngleY
        if ((gyroZAngle < -180) or (gyroZAngle > 180)):
            gyroZAngle = kalAngleZ

        print("Angle X: " + str(kalAngleX)+"   " +"Angle Y: " + str(kalAngleY)+"   " +"Angle Z: " + str(kalAngleZ))
        #print("Angle X: " + str(compAngleX)+"   " +"Angle Y: " + str(compAngleY)+"   " +"Angle Z: " + str(compAngleZ))
        #print(str(roll)+"  "+str(gyroXAngle)+"  "+str(compAngleX)+"  "+str(kalAngleX)+"  "+str(pitch)+"  "+str(gyroYAngle)+"  "+str(compAngleY)+"  "+str(kalAngleY))
        time.sleep(0.05)
        #ervo.target(kalAngleY)
    
    except Exception as exc:
        flag += 1

