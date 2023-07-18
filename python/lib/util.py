from machine import Pin
import utime

# map function
def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def flashLED():
    delay = 0.05

    led = Pin(25,Pin.OUT)
    led.high()
    utime.sleep(delay)
    led.low()
    utime.sleep(delay)