import machine
import time
import utime
import util as util

# Define the I2C bus
I2C_SDA_PIN = 20
I2C_SCL_PIN = 21
i2c = machine.I2C(0, sda=machine.Pin(I2C_SDA_PIN), scl=machine.Pin(I2C_SCL_PIN), freq=100000)

# MCP3021 I2C address
xaxis = 0x48
yaxis = 0x49

battery = machine.ADC(26)
print(battery.read_u16())


# Read ADC value
def read_adc_value(axis):
    # Start a new conversion
    i2c.writeto(axis, b'\x00')

    # Wait for the conversion to complete
    time.sleep_ms(1)

    # Read the ADC value
    data = i2c.readfrom(axis, 2)
    value = (data[0] << 6) | (data[1] >> 2)
    return value

# Main program
# while True:
#     x = read_adc_value(xaxis)
#     y = read_adc_value(yaxis)
#     print("X:", x, " Y:", y)
#     #print("Battery: ", battery.read_u16())
#     time.sleep_ms(10)
#     util.flashLED()

