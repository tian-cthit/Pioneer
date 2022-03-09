from chassis.chassis import Chassis
from remote_control.remote_controller import RemoteController
# from state_machine import StateMachine

class Pioneer:
    """main class for Pioneer. """
    def __init__(self):
#         self.state_machine = StateMachine()
        self.chassis = Chassis()
        self.remote_controller = RemoteController(self.chassis)
        self.remote_controller.show()
        
        
def main():
    pioneer = Pioneer()    

if __name__ == "__main__":
    main()