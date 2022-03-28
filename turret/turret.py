import time
from multiprocessing import Pipe, Process
from chassis.motor import PCA_Motor
from adafruit_motor import servo


class Turret:
    def __init__(self, PCA):
        self.pca_channels = {"channel_clockwise":4, "channel_anti_clockwise":5}
        self.motor = PCA_Motor(PCA, self.pca_channels)
            
    def rotate(self, direction):
        """
        Args:
            direction:  -1 for left/anti-clockwise, 1 for right.
        """
        valid_direction = [1, -1]
        if direction in valid_direction:
            self.motor.rotate(direction)
        else:
            raise ValueError("Invalid value for direction.")
        
    def stop(self):
        self.motor.stop()
        
class MainGun:
    def __init__(self, PCA):
        self.pca_channels = {"channel_clockwise":6, "channel_anti_clockwise":7}
        self.servo_channel = 8
        
        self.motor = PCA_Motor(PCA, self.pca_channels)   
        self.servo = servo.Servo(PCA.channels[self.servo_channel], min_pulse=500, max_pulse=2500)    # servo.angle = 180 for smallest pitch(downward), 0 for largest(upward)
        
        self.time_pitch_sleep = 0.01
        self.pitch_init()
        self.current_pitch = self.servo.angle
        self.flag_pitch_stop = 1
            # parameter to make pitch change smoothly
            
        self.parent_conn_up, self.child_conn_up = Pipe()
        self.parent_conn_down, self.child_conn_down = Pipe()
        
        self.move_up = None
    
    def pitch_init(self):
        target_angle = 130    # 0 pitch 
        while not target_angle-0.5 < self.servo.angle < target_angle+0.5:    #servo angle can't be precisly controlled, so a range is defined.
            if self.servo.angle < target_angle:
                self.servo.angle += 1
            else:
                self.servo.angle -= 1
            print(self.servo.angle, target_angle)
            time.sleep(self.time_pitch_sleep)
            
        
    def pitch_up(self):
        self.parent_conn_up.send(0)
        self.move_up = Process(target=self.servo_clockwise, args=(self.child_conn_up,))
        self.move_up.start()
        
    def pitch_down(self):
        self.parent_conn_down.send(0)
        self.move_up = Process(target=self.servo_anti_clockwise, args=(self.child_conn_down,))
        self.move_up.start()
        
    def servo_clockwise(self, *argv):
        while True:
            a = argv[0].recv()
            if a == 'stop':
                print("break")
                argv[0].send(self.current_pitch)
                break
                
            elif self.servo.angle > 0:
                self.servo.angle = max(self.servo.angle-1, 0)
                self.current_pitch = self.servo.angle
                
                time.sleep(self.time_pitch_sleep)
                
                self.parent_conn_up.send(0)
            else:
                break
        
    def servo_anti_clockwise(self, *argv):
        while True:
            a = argv[0].recv()
            if a == 'stop':
                print("break")
                argv[0].send(self.current_pitch)
                break
            
            if self.servo.angle < 180:
                self.servo.angle = min(self.servo.angle+1, 180)
                self.current_pitch = self.servo.angle
                
                time.sleep(self.time_pitch_sleep)
                
                self.parent_conn_down.send(0)
            else:
                break
            
    def pitch_up_stop(self):
        self.parent_conn_up.send('stop')
        
        print('pitch_up_stop', self.servo.angle)
        self.current_pitch = self.parent_conn_up.recv()
        self.servo.angle = self.current_pitch
        
    def pitch_down_stop(self):
        self.parent_conn_down.send('stop')
        
        print('pitch_down_stop', self.servo.angle)
        self.current_pitch = self.parent_conn_down.recv()
        self.servo.angle = self.current_pitch
    
        
    def fire(self):
        self.motor.rotate(-1)
        
    def cease_fire(self):
        self.motor.stop()