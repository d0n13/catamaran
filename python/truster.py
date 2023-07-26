from machine import Pin, PWM
import util

MAXPCM = 1900
MINPCM = 1100
OFFPCM = 1500
DEAD_ZONE = 50  # Ignore values lower than this
STEER_DIFF = 200 # How much the steering effect has on truster

class PowerManager:

    def __init__(self, display):
        
        self.display = display
        
        # Use pin #0 and # 1 for ESC controller 1 and 2
        self.trusterRight = PWM(Pin(16, mode=Pin.OUT));
        self.trusterRight.freq(50)
        self.trusterLeft = PWM(Pin(17, mode=Pin.OUT));
        self.trusterLeft.freq(50)

    def killTrusters(self):

        self.trusterRight.duty_ns(OFFPCM * 1000)  # in nanoseconds
        self.trusterLeft.duty_ns(OFFPCM * 1000)  # in nanoseconds
        
    def calculateTrusterPCM(self, position):

        # Set speeds to be same on both ESC controllers
        # Map the value from 0-100% to a pulse from 1100ms to 1900ms for high speed
        # Map the value from 0-100% to a pulse from 1400ms to 1600ms for low speed

        x, y = position
        #print(f"{x:3},{y:3}")
        # 1100 1200 1300 1400 1500 1600 1700 1800 1900
        left = util.map(y, 0, 100, MINPCM, MAXPCM)
        right = util.map(y, 0, 100, MINPCM, MAXPCM)
        
        steer = util.map(x, 0, 100, -STEER_DIFF, STEER_DIFF)

        # for forward direction
        if (y > DEAD_ZONE):
            # steering to left
            if (steer < DEAD_ZONE):
                right = right - steer
                if (right > MAXPCM):
                    right = MAXPCM

                left = left + steer
                if (left < MINPCM):
                    left = MINPCM

            # steering to right
            if (steer > DEAD_ZONE):
                right = right - steer
                if (right < MINPCM):
                    right = MINPCM

                left = left + steer
                if (left > MAXPCM):
                    left = MAXPCM

        # for backward direction
        if (y < 50):
            # steering to left
            if (steer > DEAD_ZONE):
                right = right + steer
                if (right < MINPCM):
                    right = MINPCM

                left = left - steer
                if (left < MINPCM):
                    left = MINPCM

            # steering to right
            if (steer < DEAD_ZONE):
                right = right + steer
                if (right < MINPCM):
                    right = MINPCM

                left = left - steer
                if (left < MINPCM):
                    left = MINPCM
                    
        # Update power for display
        self.display.leftPower = left
        self.display.rightPower = right

        self.trusterRight.duty_ns(right * 1000)  # in nanoseconds
        self.trusterLeft.duty_ns(left * 1000)  # in nanoseconds
