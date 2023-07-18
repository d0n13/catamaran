import time 
from time import sleep
from machine import ADC, Pin, PWM, ADC, I2C
import ssd1306 as ssd1306
import oleddisplay as oleddisplay
import util as util
import mcp3021 as Joystick
import mcp23009 as Controls

# Init MCP23009 to control buttons and lights
controls = Controls.mcp23009()
controls.setupIODIR()
# controls.setAsInput(0)  # Joystick button
# controls.setAsInput(1)  # Kill switch
# controls.setAsInput(2)  # Switch 3
# controls.setAsInput(3)  # Switch 2
# controls.setAsInput(4)  # Switch 1
# controls.setAsOutput(5) # Switch 3 light
# controls.setAsOutput(6) # Switch 2 light
# controls.setAsOutput(7) # Switch 1 light

# Min and max pcm values
MAXPCM = 1900
MINPCM = 1100
OFFPCM = 1500
DEAD_ZONE = 50 # Ignore values lower than this

# How much the steering effect has on truster
STEER_DIFF = 200 

# init display
#display = oleddisplay.OLED()
#display.updateBattery(100)

util.flashLED()

# Use pin #0 and # 1 for ESC controller 1 and 2
trusterRight = PWM(Pin(16, mode=Pin.OUT)); trusterRight.freq(50)
trusterLeft = PWM(Pin(17, mode=Pin.OUT)); trusterLeft.freq(50)

speedProfile = 0
speedProfileLastTime = time.time()
masterArm = 0
masterArmTime = time.time()
lastSteerPosition = 50

def speedProfileCallback(swValue):
    global speedProfile
    global speedProfileLastTime

    pressTime = time.time()
    if pressTime - 2  > speedProfileLastTime:  
        if joySw.value() == 0:
            if speedProfile == 0:
                print("High power")
                speedProfile = 1
            else:
                print("Low power")
                speedProfile = 0
        speedProfileLastTime = time.time()
    # else:
    #     print("ignored")

# Joystick input switch
joySw = Pin(28, Pin.IN, Pin.PULL_UP)
joySw.irq(trigger=Pin.IRQ_FALLING, handler=speedProfileCallback)

# map function
def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Set speeds to be same on both ESC controllers
# Map the value from 0-100% to a pulse from 1100ms to 1900ms for high speed
# Map the value from 0-100% to a pulse from 1400ms to 1600ms for low speed
def speed(x, y):
    
    # 1100 1200 1300 1400 1500 1600 1700 1800 1900 
    left = map(y, 0,100, MINPCM,MAXPCM)
    right = map(y, 0,100, MINPCM,MAXPCM)

    steer = map(x, 0,100, -STEER_DIFF, STEER_DIFF)

    # for forward direction
    if(y > DEAD_ZONE):
        # steering to left
        if(steer < DEAD_ZONE):
            right = right - steer
            if(right > MAXPCM):
                right = MAXPCM
            
            left = left + steer
            if(left < MINPCM):
                left = MINPCM

        # steering to right    
        if(steer > DEAD_ZONE):
            right = right - steer
            if(right < MINPCM):
                right = MINPCM
            
            left = left + steer
            if(left > MAXPCM):
                left = MAXPCM
    
    # for backward direction
    if(y < 50):
        # steering to left
        if(steer > DEAD_ZONE):
            right = right + steer
            if(right < MINPCM):
                right = MINPCM
            
            left = left - steer
            if(left < MINPCM):
                left = MINPCM

        # steering to right    
        if(steer < DEAD_ZONE):
            right = right + steer
            if(right < MINPCM):
                right = MINPCM
            
            left = left - steer
            if(left < MINPCM):
                left = MINPCM
    # print("left: ", left ," right: ", right, " steer: ", steer)
    
    trusterRight.duty_ns(right * 1000) # in nanoseconds
    trusterLeft.duty_ns(left * 1000) # in nanoseconds
    print("left: ", left ," right: ", right)
    # print(speed)
        
# Turn off the outputs
def escOff():
    trusterRight.duty_ns(0)
    trusterLeft.duty_ns(0)

# Arm the ESC controllers, not sure if this is correct yet as it depends on the state of the controller
# and I need to test this under the conditions that it's in effect
def arm():
    print("Arming")
    speed(0, 0)
    sleep(2)
    print("Ready")

# Steering
def joystickToTrottle():
    x = Joystick.read_adc_value(Joystick.xaxis) # x-axis
    y = Joystick.read_adc_value(Joystick.yaxis) # x-axis
    
    mapx = map(x, 0,1023, 0,100)    # Map to a range 0-100. Center position is 50
    mapy = map(y, 0,1023, 100,0)
    # print("x: ", mapx ," y: ", mapy)
    speed(mapx, mapy)


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
    # joystickToTrottle()
    util.flashLED()