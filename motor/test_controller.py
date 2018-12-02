import time
from motor_controller import motor_controller
import sys

if (len(sys.argv) > 1):
    vel = float(sys.argv[1])
    omega = float(sys.argv[2])
else:
    vel = 1000.
    omega = 0.
controller = motor_controller()
controller.set_control(vel, omega)
time.sleep(3)
controller.clean()
