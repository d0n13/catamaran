import _thread
import machine

I2C_SDA_PIN = 20
I2C_SCL_PIN = 21

class i2c:

    def __init__(self):

        self.mutex = _thread.allocate_lock()
        self.i2c = machine.I2C(0, sda=machine.Pin(I2C_SDA_PIN), scl=machine.Pin(I2C_SCL_PIN), freq=400000)
        
    def writeto(self, addr, buf):

        self.mutex.acquire()
        self.i2c.writeto(addr, buf)
        self.mutex.release()
        
    def writevto(self, addr, buf):

        self.mutex.acquire()
        self.i2c.writevto(addr, buf)
        self.mutex.release()
    
    def readfrom(self, addr, numBytes):
        
        self.mutex.acquire()
        ret = self.i2c.readfrom(addr, numBytes)
        self.mutex.release()
        return ret