from multiprocessing import Pool, Pipe, Process
from chassis.motor import PCA_Motor

class Chassis:
    """Class for basic motor motion and keyboard control behaviour. """
    
    def __init__(self, PCA):
        self.left_channels = {"channel_clockwise":0, "channel_anti_clockwise":1}
        self.right_channels = {"channel_clockwise":2, "channel_anti_clockwise":3}
        
        self.left_motor = PCA_Motor(PCA, self.left_channels)
        self.right_motor = PCA_Motor(PCA, self.right_channels)
        
        self.gear_speed_map_f = {1: 0.8, 2: 0.9, 3: 1}
        self.gear_speed_map_b = {-1: -0.8, -2: -1}
        self.gear_speed_map = self.gear_speed_map_f | self.gear_speed_map_b
        
        self.left_move = None
        self.right_move = None
        
        self.process_pool = Pool(2)
        self.parent_conn_left, self.child_conn_left = Pipe()
        self.parent_conn_right, self.child_conn_right = Pipe()
        
    def move(self, gear):
        if gear not in self.gear_speed_map:
            raise ValueError("invalid gear '%d'" %gear)
        
        speed = self.gear_speed_map[gear]
            
        self.left_move = Process(target=self.left_motor.rotate, args=(-speed, self.child_conn_left))    # left motor moves anti-clockwise when chassis move forward and vice versa
        self.right_move = Process(target=self.right_motor.rotate, args=(speed, self.child_conn_right))
        self.left_move.start()
        self.right_move.start()
        
        self.left_motor.rotation = self.parent_conn_left.recv()
        self.right_motor.rotation = self.parent_conn_right.recv()
        
    def turn_right(self, gear):
        if gear == 0:
            self.spin_clockwise()
            
        elif gear in self.gear_speed_map_f:
            speed_left = self.gear_speed_map_f[gear]
            speed_right = 0.8*self.gear_speed_map_f[gear]
            
            self.left_motor.rotate(-speed_left)
            self.right_motor.rotate(speed_right)
            
        elif gear in self.gear_speed_map_b:
            speed_left = 0.8*self.gear_speed_map_b[gear]
            speed_right = self.gear_speed_map_b[gear]
            
            self.left_motor.rotate(-speed_left)
            self.right_motor.rotate(speed_right)
        
    def turn_left(self, gear):
        if gear == 0:
            self.spin_anti_clockwise()
            
        elif gear in self.gear_speed_map_f:
            speed_left = 0.8*self.gear_speed_map_f[gear]
            speed_right = self.gear_speed_map_f[gear]
            
            self.left_motor.rotate(-speed_left)
            self.right_motor.rotate(speed_right)
            
        elif gear in self.gear_speed_map_b:
            speed_left = self.gear_speed_map_b[gear]
            speed_right = 0.8*self.gear_speed_map_b[gear]
            
            self.left_motor.rotate(-speed_left)
            self.right_motor.rotate(speed_right)
    
    def spin_clockwise(self):
        speed_left = 1
        speed_right = -1
        self.left_motor.rotate(-speed_left)
        self.right_motor.rotate(speed_right)
    
    def spin_anti_clockwise(self):
        speed_left = -1
        speed_right = 1
        self.left_motor.rotate(-speed_left)
        self.right_motor.rotate(speed_right)
    
    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()