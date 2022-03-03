import busio
import time
from board import SCL, SDA
from adafruit_pca9685 import PCA9685

speed_hex_max = 0xFFFF
clock_wise = "clock_wise"
anti_clock_wise = "anti_clock_wise"

class PCA_Motor:
    """ Basic motor behaviours. """
    
    def __init__(self, channels, frequency=60):
        self.i2c_bus = busio.I2C(SCL, SDA)
        self.pca = PCA9685(i2c_bus)
        self.pca.frequency = frequency
        self.channels = channels
        self.rotation = None
        
    def rotate(self, speed):
        if speed < -1 or speed > 1:
            raise ValueError("invalid speed '%d', should between 0 and 1" %speed)
        
        self.safe_check(speed)
        
        if speed >= 0:
            speed = int(speed*speed_hex_max)
            pca.channels[self.channels["channel_clockwise"]].duty_cycle = speed
            self.rotation = clock_wise
        elif speed < 0:
            speed = int(abs(speed)*speed_hex_max)
            pca.channels[self.channels["channel_anti_clockwise"]].duty_cycle = speed
            self.rotation = anti_clock_wise
        
    def stop(self):
        for channel in self.channels:
            pca.channels[self.channels[channel]].duty_cycle = 0
        self.rotation = None
        
    def safe_check(self, speed):
        if (speed > 0 and self.rotation == anti_clock_wise) or (speed < 0 and self.rotation == clock_wise):
            self.stop()
            time.sleep(1)