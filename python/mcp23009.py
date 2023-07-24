from machine import I2C, Pin


class mcp23009:

    def __init__(self, addr=0x27):
        self.i2c = I2C(0, sda=Pin(20), scl=Pin(21))
        self.i2caddr = addr
        self.reg = bytearray(2)
        self.gpio = 0

    def readGPIO(self):
        #  read the gpio
        self.i2c.writeto(self.i2caddr, bytes([0x09]))
        self.gpio = self.i2c.readfrom(self.i2caddr, 1)[0]
        # print(f"GPIO: {self.gpio[0]:08b}")
        return self.gpio

    def setupIO(self):
        iodir = bytearray(([0x00, 0x1f]))
        self.i2c.writeto(self.i2caddr, iodir)

        #  Set  iodir back in focus
        acks = self.i2c.writeto(self.i2caddr, bytes([0x00]))

        current = self.i2c.readfrom(self.i2caddr, 1)
        print(f"IODIR: {current[0]:08b}")

        # Set pull-up on 0-5
        gppu = bytearray(([0x06, 0x1f]))
        acks = self.i2c.writeto(self.i2caddr, gppu)
        self.i2c.writeto(self.i2caddr, bytes([0x06]))
        current = self.i2c.readfrom(self.i2caddr, 1)
        print(f"GPPU: {current[0]:08b}")

        self.readGPIO()

    def setOutput(self, bit, value=True):
        olat = bytearray(([0x0A]))
        current = self.i2c.writeto(self.i2caddr, bytes([0x0A]))

        if (value > 0):
            current = current | (1 << bit)
        else:
            current = current & (0xFF ^ (1 << bit))

        self.i2c.writeto(self.i2caddr, bytes([0x0A, current]))

        print(f"{current:08b}")

    def isSafetyON(self):
        # current = self.readGPIO()
        pattern = self.gpio & (1 << 1)
        return bool(self.gpio & pattern)
        # print(f"{current:08b} {pattern:08b} {result}")

    def isSafetyON(self):
        # current = self.readGPIO()
        pattern = self.gpio & (1 << 1)
        return bool(self.gpio & pattern)

    def readButtons(self):
        # current = self.readGPIO()
        button1 = not bool(self.gpio & 0x10)
        button2 = not bool(self.gpio & 0x08)
        button3 = not bool(self.gpio & 0x04)
        return (button1, button2, button3)

    # Set GPIO as input
    def setAsInput(self, ibit):
        reg = bytearray(1)
        reg[0] = 0
        # Read current register value
        self.i2c.writeto(self.i2caddr, reg)
        current = self.i2c.readfrom(self.i2caddr, 2)
        print("register state: " + hex(current[1]))

        # Set the bit for selected GPIO
        reg[0] = current[0] | (1 << ibit)
        # current = int.from_bytes(current|(1<<ibit))

        # Rewrite the register using new hex value
        self.i2c.writeto(self.i2caddr, reg)

        # Set GPIO as output

    def setAsOutput(self, ibit):
        reg = bytearray(1)
        reg[0] = 0

        # Read current register value
        self.i2c.writeto(self.i2caddr, reg)
        current = self.i2c.readfrom(self.i2caddr, 1)
        print("output state: " + hex(current[0]))
        # Set the bit for selected GPIO
        reg[0] = current[0] & (0xFF ^ (0 << ibit))
        print("output state mod: " + hex(current[0]))

        # Rewrite the register using new hex value
        self.i2c.writeto(self.i2caddr, reg)

        # Set value of GPIO

    def set(self, ibit, value):
        reg = 0

        # Read current register value
        current = self.i2c.read_byte(reg)

        # Set value of GPIO either high (1) or low (0)
        if (value > 0):
            current = current | (1 << ibit)
        else:
            current = current & (0xFF ^ (1 << ibit))

        # Rewrite the register using new hex value
        self.i2c.write([reg, current])

        # Set the output value of many GPIOs at once

    def setMany(self, bits, values):
        val = -1
        reg = 9
        # Loop over all bits
        for ibit in range(0, len(bits)):
            # Read register current value
            if val < 0:
                # self.iicbus.write_byte(self.i2caddr, reg)
                val = self.i2c.read_byte(reg)

            # Adjust the value
            if values[ibit] > 0:
                val = val | (1 << bits[ibit])
            else:
                val = val & (0xFF ^ (1 << bits[ibit]))

        # Write new register value
        self.i2c.write_byte(reg, val)

        # print("Setting reg {} with val {:08b}".format(reg, val))

    # Read register for I2C R/W test
    # Register chosen controls the mask value for the interupt which won't affect any behaviors
    def read(self, ibit):
        reg = 3
        # Read register
        self.i2c.write_byte(self.i2caddr, reg)
        val = self.i2c.read_byte(self.i2caddr)

        # Check value of specified bit
        if (val & (1 << ibit)):
            return 1
        else:
            return 0

    def setByte(self, value):
        reg = 3

        # Set I2C check register
        self.i2c.write_byte(reg, value)

    def readByte(self):
        reg = 3

        # Read I2C check register
        cval = self.i2c.read_byte(reg)
        # cval=self.iicbus.read_byte(self.i2caddr)
        return cval

    def readAllBytes(self):
        bytes = []
        for i in range(0, 11):
            bytes.append(self.i2c.read_byte(i))

        return bytes
