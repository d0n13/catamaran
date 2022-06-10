from time import sleep
from machine import Pin
from machine import PWM

# Use pin #0 for ESC controller 1
# Use pin #1 for ESC controller 2
Pin(0, Pin.OUT)
Pin(1, Pin.OUT)

pwm1 = PWM(Pin(0))
pwm2 = PWM(Pin(1))

pwm1.freq(50) # Freq must be 50Hz for both controllers
pwm1.freq(50)

# map function
def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Set speeds to be same on both ESC controllers
# Map the value from 0-100% to a pulse from 1ms to 2ms
def speed(speed):
    speed = map(speed, 0,100, 1000,2000)
    pwm1.duty_ns(speed * 1000) # in nanoseconds
    pwm2.duty_ns(speed * 1000) # in nanoseconds
    
# Turn off the outputs
def escOff():
    pwm1.duty_ns(0)
    pwm2.duty_ns(0)

# Arm the ESC controllers, not sure if this is correct yet as it depends on 
def arm():
    print("Arming")
    speed(0)
    sleep(2)
    print("Ready")

# trigger the arming
arm()

# TODO: Need to add joystick and servo for steering and attach trottles to stick
while True:
    speed(0)
    sleep(1)