from machine import ADC
import ssd1306 as ssd1306
import util as util

class OLED:

    def __init__(self, i2c):

        # store last reading from battery
        self.batteryVoltage = 0
        self.flash = False
        self.leftPower = 1500
        self.rightPower = 1500

        # setup display
        self.i2c = i2c
        self.frame = ssd1306.SSD1306_I2C(128, 32, i2c)
        self.display = ssd1306.SSD1306_I2C(128, 32, i2c)

        # Bounding box for battery display
        self.display.rect(0, 24, 128, 8, 1)

        # bounding circles for buttons
        self.display.ellipse(6, 6, 6, 6, 1)
        self.display.ellipse(22, 6, 6, 6, 1)
        self.display.ellipse(38, 6, 6, 6, 1)

        self.display.show()

    def showSafety(self, safetyOn):

        self.display.rect(109, 2, 2, 9, 1, 1)
        self.display.rect(122, 2, 2, 9, 1, 1)

        self.display.rect(112, 2, 9, 9, 0, 1)
        self.display.rect(112, 2, 9, 9, 1, safetyOn)

        if not safetyOn:
            self.showText('ATTACH')

    def showButtons(self, buttons):

        one, two, three = buttons
        r = 4
        self.display.ellipse(6, 6, r, r, 0, 1)
        self.display.ellipse(22, 6, r, r, 0, 1)
        self.display.ellipse(38, 6, r, r, 0, 1)

        if one:
            self.display.ellipse(6, 6, r, r, 1, one)
        if two:
            self.display.ellipse(22, 6, r, r, 1, two)
        if three:
            self.display.ellipse(38, 6, r, r, 1, three)

    def updateBattery(self):

        batteryVolts = ADC(26)
        volts = batteryVolts.read_u16()

        volts = (self.batteryVoltage + volts) / 2
        self.batteryVoltage = volts

        # print(f"voltage {volts}")
        # 20.75 - full
        # 15v - empty

        # map the power to the graph
        width = util.map(volts, 44300, 60800, 0, 122)
        #width = 40
        if width > 122:
            width = 122

        # Blank out the display before updating frame
        self.display.fill_rect(3, 26, 124, 4, 0)
        self.display.fill_rect(3, 26, width, 4, 1)

        power = util.map(width, 0, 122, 0, 100)
        if power <= 10:
            self.flash = not self.flash
            self.display.rect(0, 24, 128, 8, self.flash)
            self.display.rect(0, 24, 16, 8, self.flash)
            # print(f"{width}%")
        else:
            self.display.rect(0, 24, 128, 8, 1)
            self.display.rect(0, 24, 16, 8, 1)

    def setCruise(self, state):

        if state:
            self.showText('CRUISE')
        else:
            self.showText('MAN')

    def showText(self, text):

        self.display.rect(48, 2, 52, 8, 0, 1)
        if(len(text) <= 3):
            self.display.text(text, 66, 2)
        else:
            self.display.text(text, 54, 2)

    def showTrusterPower(self):

        # map the power values
        left = util.map(self.leftPower, 1100, 1900, -20, 20)
        right = util.map(self.rightPower, 1100, 1900, -20, 20)
        #print(f"D {left:3},{right:3}")
        x = 78
        self.display.rect(x-22, 13, 44, 8, 1, 0)
        self.display.rect(x-20, 14, 40, 6, 0, 1)
        self.display.line(x, 15, x + left, 15, 1)
        self.display.line(x, 17, x + right, 17, 1)

    def updateDisplay(self):
        self.frame.blit(self.display, 0, 0)
        self.frame.show()

