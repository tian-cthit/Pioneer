import time
from vispy import app, io, scene
from vispy.scene.widgets.viewbox import ViewBox
from chassis.chassis import Chassis

padel_forward = 3
padel_backward = -2

class RemoteController:
    def __init__(self, chassis, turret, main_gun):
        self.camera_view = None
        
        self.chassis = chassis
        self.turret = turret
        self.main_gun = main_gun
        
        self._func_keys_press = {}
        self._func_keys_release = {}
        
        self.flag_remote_control = 0
        self.flag_fire = 0
        
        self.gear = 0
        self.padel = 0
        self.time = None
        self.gear_up_time = time.time()
        self.gear_up_flag = 0
        self.gear_down_time = time.time()
        self.gear_down_flag = 0
        
        self._canvas = scene.SceneCanvas(keys="interactive", bgcolor="black", size=(800, 600))
        self._grid = self._canvas.central_widget.add_grid()
        
        self.add_event("key_press", self.key_press_handler)
        self.add_event("key_release", self.key_release_handler)
        self.list_hotkeys()

        self._views = dict(widgets={})

        self.add_camera()
        self.add_map()
        self.add_motion_indicator()

    def show(self):
        self._canvas.show(visible=True, run=True)

    def add_map(self):
        self._grid.add_widget(row=0, col=1, col_span=2, bgcolor="green")

    def add_motion_indicator(self):
        self._grid.add_widget(row=1, col=0, col_span=2, bgcolor="red")

    def add_camera(self):
        camera_view = ViewBox()
        camera_view.camera.rect = (0, 0, 400, 300)
        # camera_view.add()

        postion = (0, 1, 1, 1)
        self._grid.add_widget(camera_view, *postion)

    def list_hotkeys(self):
        self._func_keys_press["escape"] = {"func": "_close_ui", "desc": "Close UI"}
        self._func_keys_press["o"] = {"func": "remote_control_mode", "desc": "Switch to remote control mode"}
        self._func_keys_press["p"] = {"func": "autonomous_mode", "desc": "Switch to autonomous mode"}
        
        self._func_keys_press["w"] = {"func": "padel_forward", "desc": "Move forward with full speed"}
        self._func_keys_press["s"] = {"func": "padel_backward", "desc": "Move backward with full speed"}
        self._func_keys_press["a"] = {"func": "turn_left", "desc": "Turn left"}
        self._func_keys_press["d"] = {"func": "turn_right", "desc": "Turn right"}
        
        self._func_keys_press["r"] = {"func": "gear_puls_one", "desc": "switch to a higher gear"}
        self._func_keys_press["f"] = {"func": "gear_minus_one", "desc": "switch to a lower gear"}
        
        self._func_keys_press["up"] = {"func": "main_gun_up", "desc": "Main gun up"}
        self._func_keys_press["down"] = {"func": "main_gun_down", "desc": "Main gun down"}
        self._func_keys_press["left"] = {"func": "turret_rotate_left", "desc": "Turret turns left"}
        self._func_keys_press["right"] = {"func": "turret_rotate_right", "desc": "Turret turns right"}
        
        self._func_keys_press["space"] = {"func": "fire", "desc": "Fire/Cease fire"}

        self._func_keys_release["w"] = {"func": "padel_release", "desc": "Release padel"}
        self._func_keys_release["s"] = {"func": "padel_release", "desc": "Release padel"}
        self._func_keys_release["a"] = {"func": "stop_turning", "desc": "Stop turning"}
        self._func_keys_release["d"] = {"func": "stop_turning", "desc": "Stop turning"}
        
        self._func_keys_release["up"] = {"func": "main_gun_up_stop", "desc": "Main gun stop moving"}
        self._func_keys_release["down"] = {"func": "main_gun_down_stop", "desc": "Main gun stop moving"}
        self._func_keys_release["left"] = {"func": "turret_stop", "desc": "Turret stop moving"}
        self._func_keys_release["right"] = {"func": "turret_stop", "desc": "Turret stop moving"}
        
        self._func_keys_release["p"] = {"func": "stop_all", "desc": "Stop all acuators"}

        for key, action in self._func_keys_press.items():
            print("{}{}".format(key.ljust(15, "."), " ".join(action["desc"].split("_"))))

    def key_press_handler(self, event):
        key_string = event.key.name.lower()
        if key_string in self._func_keys_press.keys():
            getattr(self, self._func_keys_press[key_string]["func"])()
        else:
            print(f"You pressed: {key_string} which is not a valid key.")

    def key_release_handler(self, event):
        key_string = event.key.name.lower()
        if key_string in self._func_keys_release.keys():
            getattr(self, self._func_keys_release[key_string]["func"])()

    def add_event(self, event_name, event_handle):
        if event_name in self._canvas.events:
            getattr(self._canvas.events, event_name).connect(event_handle)
            
    def _close_ui(self):
        print("Closing UI...")
        self._canvas.close()
            
    def remote_control_mode(self):
        if self.flag_remote_control == 0:
            self.flag_remote_control = 1
#             self.state_machine.to(remote_mode)
            print("Switch to remote control mode")
        
    def autonomous_mode(self):
        if self.flag_remote_control == 1:
            self.flag_remote_control = 0
#             self.state_machine.to(autonomous_mode)
            print("Switch to autonomous mode")

    def padel_forward(self):
        if self.flag_remote_control == 1:
            self.gear_down_flag = 0
            self.gear_up_flag = 0
            
            self.padel = padel_forward
            self.gear = 0
            self.chassis.move(self.padel)
            print("Moving forward")

    def padel_backward(self):
        if self.flag_remote_control == 1:
            self.gear_down_flag = 0
            self.gear_up_flag = 0
            
            self.padel = padel_backward
            self.gear = 0
            self.chassis.move(self.padel)
            print("Moving backward")  

    def padel_release(self):
        if self.flag_remote_control == 1:
            self.gear_down_flag = 0
            self.gear_up_flag = 0
            
            self.padel = 0
            print("Padel released")  
            if self.gear == 0:
                self.chassis.stop()
                print("Stop")
            else:
                self.chassis.move(self.gear)
        
    def gear_puls_one(self):
        if self.flag_remote_control == 1:
            self.gear = self.gear + 1
            self.gear = min(self.gear, 3)
            print(f"Gear: {self.gear}")
            
            self.gear_down_flag = 0
            self.gear_up_flag = 1
            self.time = time.time()
            if not self.padel:
                if self.gear_up_flag == 1 and (self.time - self.gear_up_time) < 0.3:
                    self.gear = 3
                    self.chassis.move(self.gear)
                else:
                    self.chassis.stop() if self.gear == 0 else self.chassis.move(self.gear)
                self.gear_up_time = time.time()
                print(f"Moving with gear {self.gear}")
        
    def gear_minus_one(self):
        if self.flag_remote_control == 1:
            self.gear = self.gear - 1
            self.gear = max(self.gear, -2)
            print(f"Gear: {self.gear}")
            
            self.gear_up_flag = 0
            self.gear_down_flag = 1
            self.time = time.time()
            if not self.padel:
                if self.gear_down_flag == 1 and (self.time - self.gear_down_time) < 0.3:
                    self.gear = -2
                    self.chassis.move(self.gear)
                else:
                    self.chassis.stop() if self.gear == 0 else self.chassis.move(self.gear)
                self.gear_down_time = time.time()
                print(f"Moving with gear {self.gear}")
        
    def turn_left(self):
        if self.flag_remote_control == 1:
            self.gear_down_flag = 0
            self.gear_up_flag = 0
            
            self.chassis.turn_left(self.padel) if self.padel else self.chassis.turn_left(self.gear)
            print("Turning left")
            
    def turn_right(self):
        if self.flag_remote_control == 1:
            self.gear_down_flag = 0
            self.gear_up_flag = 0
            
            self.chassis.turn_right(self.padel) if self.padel else self.chassis.turn_right(self.gear)
            print("Turning right")
    
    def stop_turning(self):
        if self.flag_remote_control == 1:
            if self.padel:
                self.chassis.move(self.padel)
            elif self.gear:
                self.chassis.move(self.gear)
            else:
                self.chassis.stop()
    
    def turret_rotate_left(self):
        if self.flag_remote_control == 1:
            self.turret.rotate(-1)
    
    def turret_rotate_right(self):
        if self.flag_remote_control == 1:
            self.turret.rotate(1)
    
    def turret_stop(self):
        if self.flag_remote_control == 1:
            self.turret.stop()
            
    def main_gun_up(self):
        self.main_gun.pitch_up()
        
    def main_gun_down(self):
        self.main_gun.pitch_down()
    
    def main_gun_up_stop(self):
        self.main_gun.pitch_up_stop()
        
    def main_gun_down_stop(self):
        self.main_gun.pitch_down_stop()
        
    def fire(self):
        if self.flag_remote_control == 1:
            if self.flag_fire == 0:
                self.flag_fire = 1
                self.main_gun.fire()
            else:
                self.flag_fire = 0
                self.main_gun.cease_fire()

    def stop_all(self):
        print("Stopping all actuators...")
        self.chassis.stop()
        self.turret.stop()
        self.main_gun.pitch_stop()
        self.main_gun.cease_fire()
        

