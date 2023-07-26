import machine
import time
import utime
import util as util

# MCP3021 I2C address
xaxis = 0x48
yaxis = 0x4d

class mcp3021:
    
    # Read ADC value
    def read(self, i2c, axis):
        # Start a new conversion
        i2c.writeto(axis, b'\x00')

        # Wait for the conversion to complete
        time.sleep_ms(1)

        # Read the ADC value
        data = i2c.readfrom(axis, 2)
        value = (data[0] << 6) | (data[1] >> 2)
        return value
