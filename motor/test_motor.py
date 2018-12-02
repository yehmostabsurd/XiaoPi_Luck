from rrb3 import *
from random import randint

BATTERY_VOLTS = 8
MOTOR_VOLTS = 5

rr = RRB3(BATTERY_VOLTS, MOTOR_VOLTS)

i = 0
speedl = 0.1
speedr = 0.1
while True:
    try:
      dl = 1 #randint(0, 1)
      dr = 1 #randint(0, 1)
      rr.set_motors(speedl, dl, speedr, dr)
      print( "{} has speedl {} with {} dr, speedr {} with {} dr".format(i, speedl, dl, speedr, dr) )
      #speedl -= 0.09
      # speedr -= 0.09
      time.sleep(3)
      i += 1
    except KeyboardInterrupt:
      print("Exiting")
      rr.cleanup()