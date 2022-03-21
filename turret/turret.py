from chassis.motor import PCA_Motor


class Turret:
    def __init__(self):
        self.pca_channels = {"channel_clockwise":4, "channel_anti_clockwise":5}
        self.motor = PCA_Motor(self.pca_channels)
    
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
    def __init__(self):
        self.pca_channels = {"channel_clockwise":6, "channel_anti_clockwise":7}
        self.motor = PCA_Motor(self.pca_channels)
        
    def fire(self):
        self.motor.rotate(-1)
        
    def cease_fire(self):
        self.motor.stop()