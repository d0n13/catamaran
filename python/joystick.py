import util

XAXIS = 0x48
YAXIS = 0x4d

class Joystick:
    
    def __init__(self, i2c):
        self.i2c  = i2c

    def readAxis(self):
        x = self.adc.read(self.i2c, XAXIS)  # x-axis
        y = self.adc.read(self.i2c, YAXIS)  # y-axis

        mapx = util.map(x, 0, 1023, 0, 100)  # Map to a range 0-100. Center position is 50
        mapy = util.map(y, 0, 1023, 100, 0)
        #print(f"{mapx:3},{mapy:3}")
        return (mapx, mapy)
    