import mcp3021
import util
import math

XAXIS = 0x48  # Address of x-axis on mcp3021 chip
YAXIS = 0x4d  # Address of y-axis on mcp3021 chip

class Joystick:

    def __init__(self, i2c=None):
        self.i2c = i2c
        self.adc = mcp3021.mcp3021()

    def readAxis(self):
        x = self.adc.read(self.i2c, XAXIS)  # x-axis
        y = self.adc.read(self.i2c, YAXIS)  # y-axis

        mapx = util.map(x, 0, 1023, -100, 100)  # Map to a range 0-100. Center position is 50
        mapy = util.map(y, 0, 1023, 100, -100)

        return float(mapx / 100), float(mapy / 100)

    # See https://electronics.stackexchange.com/questions/19669/algorithm-for-mixing-2-axis-analog-input-to-control-a-differential-motor-drive
    def steering(self, axis):
        x, y = axis
        # convert to polar
        r = math.sqrt(x ** 2 + y ** 2)
        t = math.atan2(x, y)

        # rotate by 45 degrees
        t += math.pi / 4

        # back to cartesian
        left = r * math.cos(t)
        right = r * math.sin(t)

        # rescale the new coords
        left = left * math.sqrt(2)
        right = right * math.sqrt(2)
        # print(f"{left:4.1f} {right:4.1f}")
        # clamp to -1/+1
        left = max(-1, min(left, 1))
        right = max(-1, min(right, 1))

        return left, right
