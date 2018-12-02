from rrb3 import *
from random import randint

class motor_controller():
    
    def __init__(self):
        BATTERY_VOLTS = 8
        MOTOR_VOLTS = 5
        
	self.rr = RRB3(BATTERY_VOLTS, MOTOR_VOLTS)
		
	# speed should be any number between 0 and 1
        self.speedl = 0.
        self.speedr = 0.
	# direction should be an integer either 0 or 1
	self.dl = 0.
	self.dr = 0.
	
	self.b = 150. # unit in millimeter
	self.maxspeed = 2000. # 2m/s => 2000 mm/s
        
    def set_control(self, vel, omega):
	try:
		vl = vel - (self.b * omega) / 2
		vr = vel + (self.b * omega) / 2
		
		speedl = abs(vl) / self.maxspeed
		speedr = abs(vr) / self.maxspeed
	
                if speedl > 1.: print("speedl {} exceed maximum value 1.0".format(speedl) )        
                speedl = 1. if speedl > 1. else speedl
                if speedl < 0.: print("speedl {} is below minimum value 0.".format(speedl) )
                speedl = 0. if speedl < 0. else speedl

                if speedr > 1.: print("speedr {} exceed maximum value 1.0".format(speedr) )
                speedr = 1. if speedr > 1. else speedr
                if speedr < 0.: print("speedr {} is below minimum value 0.".format(speedr)) 
                speedr = 0. if speedr < 0. else speedr


		dl = 1 if vl > 0 else 0
		dr = 1 if vr > 0 else 0
                print("sending motor control speedl {} in {} dir, speedr {} in {} dir".format(speedl, dl, speedr, dr) )
                self.rr.set_motors(speedl, dl, speedr, dr)
	except KeyboardInterrupt:
		print("Exiting speed controller!!")
		self.rr.cleanup()
		
    def clean(self):
	self.rr.cleanup()
