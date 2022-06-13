import time 
from time import sleep
from machine import ADC, Pin, PWM

# Use pin #0 and # 1 for ESC controller 1 and 2
trusterRight = PWM(Pin(0)); trusterRight.freq(50)
trusterLeft = PWM(Pin(1)); trusterLeft.freq(50)
steering = PWM(Pin(3)); steering.freq(50)

# Joystick x axis
joyX = ADC(27)

# Joystick y axis
joyY = ADC(26)

# Joystick input switch
joySw = Pin(28, Pin.IN, Pin.PULL_UP)

masterArm = 0
masterArmTime = time.time()

lastSteerPosition = 50

# map function
def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Set speeds to be same on both ESC controllers
# Map the value from 0-100% to a pulse from 1ms to 2ms
def speed(speed):
    speed = map(speed, 0,100, 1000,2000) #ESC
    trusterRight.duty_ns(speed * 1000) # in nanoseconds
    trusterLeft.duty_ns(speed * 1000) # in nanoseconds
    
# Steering 0 - 100. 50 is straight
def steer(direction): 
    dir = map(direction, 0,100, 700,2300)
    steering.duty_ns(dir * 1000) # in nanoseconds

# Turn off the outputs
def escOff():
    trusterRight.duty_ns(0)
    trusterLeft.duty_ns(0)

# Arm the ESC controllers, not sure if this is correct yet as it depends on the state of the controller
# and I need to test this under the conditions that it's in effect
def arm():
    print("Arming")
    speed(0)
    sleep(2)
    print("Ready")

# trigger the arming
#arm()

# Steering
def joystickToSteer():
    global lastSteerPosition

    if masterArm:
        x = joyX.read_u16()                 # Read the joystick
        mappedX = map(x, 0,65535, 0,100)    # Map to a range 0-100. Center position is 50

        if (lastSteerPosition - 2) > mappedX:
            lastSteerPosition = mappedX
            steer(mappedX)
        if (lastSteerPosition + 2) < mappedX:
            lastSteerPosition = mappedX
            steer(mappedX)

# Steering
def joystickToTrottle():
    y = joyY.read_u16()                 # Read the joystick
    mappedY = map(y, 0,65535, 0,100)    # Map to a range 0-100. Center position is 50
    speed(mappedY)

def checkIfArmed():
    global masterArmTime
    global masterArm

    arm = joySw.value()
    if not arm:
        pressTime = time.time()
        # print("pressTime: " + str(pressTime))
        # print("masterTime: " + str(masterArmTime))

        if pressTime - 2  > masterArmTime:
            
            masterArmTime = pressTime
            masterArm = not masterArm
            print("Arming: " + str(masterArm)) # need to latch the value between on and off as sw is momentary
    
    
    
# Main Loop
while True:
    joystickToSteer()
    joystickToTrottle()
    checkIfArmed()