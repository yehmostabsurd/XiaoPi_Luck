##########################################################
### Yanling Wu (yw996), Yeh Dawei(ty359) 				##
### This is for celebration mode and the car  			##
### will turn around and move forward and backward      ##
##########################################################

import time
from motor_controller import motor_controller

controller = motor_controller()

value = 1
start_time = time.time()
while 10>(time.time() - start_time):
    if value == 1:
        controller.set_control( 0., 30.)
        time.sleep(2)
        value += 1
    if value == 2:
        controller.set_control( 0., -30.)
        time.sleep(2)
        value += 1
    if value == 3:
        controller.set_control( 2000., 0.)
        time.sleep(1)
        value += 1
    if value == 4:
        controller.set_control( -2000., 0.)
        time.sleep(2)
        value = 1
