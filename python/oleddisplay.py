from machine import ADC, I2C, Pin
import ssd1306 as ssd1306
import util as util
from array import *


class OLED:

    def __init__(self):

        #  store last reading from battery
        self.batteryVoltage = 0
        self.flash = False;

        # setup display
        led = Pin(25, Pin.OUT)
        i2c = I2C(0, sda=Pin(20), scl=Pin(21))
        self.frame = ssd1306.SSD1306_I2C(128, 32, i2c)
        self.display = ssd1306.SSD1306_I2C(128, 32, i2c)
        # self.display.text('Demo', 0, 0)

        #  bounding box for battery display
        self.display.rect(0, 24, 128, 8, 1)

        # bounding circles for buttons
        self.display.ellipse(6, 6, 6, 6, 1)
        self.display.ellipse(22, 6, 6, 6, 1)
        self.display.ellipse(38, 6, 6, 6, 1)

        self.display.show()

    def showSafety(self, safetyOn):
        # self.display.poly(110, 0, array('h', [0,0, 0, 8, -5, 4]), 1, 1)
        # self.display.poly(122, 0, array('h', [0,0, 0, 8, 5, 4]), 1, 1)

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
        if width > 122:
            width = 122

        # Blank out the dispplay before updating frame
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
            self.showText('MANN')

    def showText(self, text):
        self.display.rect(48, 3, 52, 8, 0, 1)
        self.display.text(text, 52, 3)

    def updateDisplay(self):
        self.frame.blit(self.display, 0, 0)
        self.frame.show()

