from machine import Pin, I2C
import ssd1306 as ssd1306
import util as util

class OLED:

    def __init__(self):
        # setup display
        led = Pin(25,Pin.OUT)
        i2c = I2C(0, sda=Pin(20), scl=Pin(21))
        self.frame = ssd1306.SSD1306_I2C(128, 32, i2c)
        self.display = ssd1306.SSD1306_I2C(128, 32, i2c)
        self.display.text('Demo', 0, 0)
        self.display.text('Bat:', 0, 19)
        self.display.show()

    def updateBattery(self, power):

        # map the power to the graph
        width = util.map(power, 0, 100, 0, 128)

        # Blank out the dispplay before updating frame
        self.display.fill_rect(0, 28, 128, 4, 0)
        self.display.fill_rect(0, 28, width, 4, 1)
        self.frame.blit(self.display, 0, 0)
        self.frame.show()
