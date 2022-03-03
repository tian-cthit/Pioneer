from chassis.motor import PCA_Motor


class Chassis:
    """Class for basic motor motion and keyboard control behaviour. """
    
    def __init__(self):
        self.left_channels = {"channel_clockwise":0, "channel_anti_clockwise":1}
        self.right_channels = {"channel_clockwise":2, "channel_anti_clockwise":3}
        self.left_motor = PCA_Motor(self.left_channels)
        self.right_motor = PCA_Motor(self.right_channels)
        self.gear_speed_map_f = {1: 0.4, 2: 0.7, 3: 1}
        self.gear_speed_map_b = {-1: -0.25, -2: -0.5}
        
    def forward(self, gear):
        if gear not in self.gear_speed_map_f:
            raise ValueError("invalid gear '%d'" %gear)
        
        speed = self.gear_speed_map_f[gear]
        self.left_motor.rotate(-speed)
        self.right_motor.rotate(speed)
    
    def backward(self, gear):
        if gear not in self.gear_speed_map_b:
            raise ValueError("invalid gear '%d'" %gear)
        
        speed = self.gear_speed_map_b[gear]
        self.left_motor.rotate(-speed)
        self.right_motor.rotate(speed)
        
    def turn_right(self, gear):
        if gear in self.gear_speed_map_f:
            speed_left = self.gear_speed_map_f[gear]
            speed_right = 0.5*self.gear_speed_map_f[gear]
            
            self.left_motor.rotate(-speed_left)
            self.right_motor.rotate(speed_right)
            
        elif gear in gear_speed_map_b:
            speed_left = 0.5*self.gear_speed_map_b[gear]
            speed_right = self.gear_speed_map_b[gear]
            
            self.left_motor.rotate(-speed_left)
            self.right_motor.rotate(speed_right)
        
    def turn_left(self, gear):
        if gear in self.gear_speed_map_f:
            speed_left = 0.5*self.gear_speed_map_f[gear]
            speed_right = self.gear_speed_map_f[gear]
            
            self.left_motor.rotate(-speed_left)
            self.right_motor.rotate(speed_right)
            
        elif gear in self.gear_speed_map_b:
            speed_left = self.gear_speed_map_b[gear]
            speed_right = 0.5*self.gear_speed_map_b[gear]
            
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