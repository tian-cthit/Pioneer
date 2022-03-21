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
        self.pca = PCA9685(self.i2c_bus)
        self.pca.frequency = frequency
        self.channels = channels
        self.rotation = None
        self.last_rotation = None
        
    def rotate(self, speed, *argv):
        """
        Args:
            speed: value in [0, 1], 0 for stop and 1 for full speed.
            *argv: for multi processing, takes the 2nd return value of Pipe().
        """
        
        if speed < -1 or speed > 1:
            raise ValueError("invalid speed '%d', should between 0 and 1" %speed)
        
        self.safe_check(speed)
        
        if speed >= 0:
            speed = int(speed*speed_hex_max)
            self.pca.channels[self.channels["channel_clockwise"]].duty_cycle = speed
            self.rotation = clock_wise
        elif speed < 0:
            speed = int(abs(speed)*speed_hex_max)
            self.pca.channels[self.channels["channel_anti_clockwise"]].duty_cycle = speed
            self.rotation = anti_clock_wise
        
        if argv:
            argv[0].send(self.rotation)
        
    def stop(self):
        for channel in self.channels:
            self.pca.channels[self.channels[channel]].duty_cycle = 0
        self.rotation = None
        self.stop_time = time.time()
        print("Motor stop")
        
    def safe_check(self, speed):
        if (speed > 0 and self.rotation == anti_clock_wise) or (speed < 0 and self.rotation == clock_wise):
            self.stop()
            print("Safe pause")
            time.sleep(1)