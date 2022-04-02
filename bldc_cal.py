from bldc import BLDC
from machine import Pin, PWM
import utime, time

global fan
fan = BLDC()


fan.zero()

