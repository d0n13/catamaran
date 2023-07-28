from machine import Pin, PWM
import util

MAXPCM = 1900
MINPCM = 1100
OFFPCM = 1500


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

    def setTrusterPCM(self, position):
        # Set speeds to be same on both ESC controllers
        # Map the value from -1 to +1 to a pulse from 1100ms to 1900ms
        l, r = position
        left = util.map(l, -1, 1, MINPCM, MAXPCM)
        right = util.map(r, -1, 1, MINPCM, MAXPCM)

        # Update power for display
        self.display.leftPower = left
        self.display.rightPower = right

        # Send it
        self.trusterLeft.duty_ns(left * 1000)  # in nanoseconds
        self.trusterRight.duty_ns(right * 1000)  # in nanoseconds
