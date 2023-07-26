from time import sleep
import oleddisplay as oleddisplay
import joystick
import mcp23009 as Controls
import truster
import thread_i2c
import _thread

# init
i2c = thread_i2c.i2c()
display = oleddisplay.OLED(i2c = i2c)
joystick = joystick.Joystick(i2c = i2c)

# Init MCP23009 to control buttons and lights
controls = Controls.mcp23009(i2c = i2c)
controls.setupIO()
t200 = truster.PowerManager(display)


def timeCrit():

    print("Starting...")
    while True:
        axis = joystick.readAxis()
        
        if not controls.isSafetyOn():
            t200.killTrusters()
        else:
            t200.calculateTrusterPCM(axis)
        
        if controls.isJoystickHatOn():
           print("HAT")
        sleep(0.1)

def displayUpdates():

    while True:
        controls.readGPIO()
        display.updateBattery()

        buttons = controls.readButtons()
        display.showButtons(buttons)
        button1, button2, button3 = buttons

        display.setCruise(button2)
        display.showSafety(controls.isSafetyOn())

        display.showTrusterPower()
        display.updateDisplay()

        sleep(0.05)


if __name__ == "__main__":

    _thread.start_new_thread(displayUpdates, ())
    timeCrit()


