import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685

from chassis.chassis import Chassis
from turret.turret import Turret, MainGun
from remote_control.remote_controller import RemoteController
# from state_machine import StateMachine

class Pioneer:
    """main class for Pioneer. """
    def __init__(self):
#         self.state_machine = StateMachine()
        self.i2c_bus = busio.I2C(SCL, SDA)
        self.pca = PCA9685(self.i2c_bus)
        self.pca.frequency = 50
        
        self.chassis = Chassis(self.pca)
        self.turret = Turret(self.pca)
        self.main_gun = MainGun(self.pca)
        
        self.remote_controller = RemoteController(self.chassis, self.turret, self.main_gun)
        self.remote_controller.show()
        
        
def main():
    pioneer = Pioneer()    

if __name__ == "__main__":
    main()