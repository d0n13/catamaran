from time import sleep
from machine import Pin
from machine import PWM
import sys
import os

Pin(0, Pin.OUT)
pwm = PWM(Pin(0))
pwm.freq(50)

#Function to set an angle
#The position is expected as a parameter

def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def speed(speed):
    speed = map(speed, 0,100, 1000,2000)
    pwm.duty_ns(speed * 1000) # in nanoseconds
    
def arm():
    print("UP")
    speed(100)
    sleep(2)
    print("DOWN")
    speed(0)
    sleep(2)
    print("READY")

arm()

while True:
    
    speed(0)
    sleep(1)