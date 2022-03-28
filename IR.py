from machine import Pin, PWM
import utime

def main():
    #switch = Pin(0, Pin.IN, Pin.PULL_DOWN)
    sensor = Pin(15, Pin.IN, Pin.PULL_DOWN)
    
    while True:
        print(sensor.value())
        utime.sleep(0.05)
        
main()