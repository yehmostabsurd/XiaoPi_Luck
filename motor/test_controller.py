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
count = 0
run_time = time.time()

controller.set_control(vel, omega)
time.sleep(2)
#while count < 10000:
    #try:
        #controller.set_control(vel, omega)
	#count += 1
        ##time.sleep(0.03)
    #except KeyboardInterrupt:
        #controller.clean()
        #print("clean speed controller")
		
print("the average run time is ",(time.time()-run_time))
