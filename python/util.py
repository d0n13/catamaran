import utime
import machine


# map function
def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def flashLED():
    led = machine.Pin("LED", machine.Pin.OUT)
    delay = 0.04
    led.on()
    utime.sleep(delay)
    led.off()
    utime.sleep(delay)
