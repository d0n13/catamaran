import machine
import util

util.flashLED()

I2C_SDA_PIN = 20
I2C_SCL_PIN = 21
i2c=machine.I2C(0, sda=machine.Pin(I2C_SDA_PIN), scl=machine.Pin(I2C_SCL_PIN), freq=400000)

print('Scanning I2C bus.')
devices = i2c.scan() # this returns a list of devices

device_count = len(devices)

if device_count == 0:
    print('No i2c device found.')
else:
    print(f"{device_count} devices found.")

for device in devices:
    print(f"Decimal address: {device} Hex address: {hex(device)}")