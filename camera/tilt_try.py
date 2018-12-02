import time
import RPi.GPIO as GPIO
import sys
import subprocess
import pigpio
#set fro broadcom numbering not board numbers
GPIO.setmode(GPIO.BCM)

# Set Up Pan Tilt Servo HardwarePWM Pins
motorPinT = 12
# connect to pi gpio Daemon
pi_hw = pigpio.pi()
start_time = time.time()
esl_time = 0
t = 2.3
dc = t / 20 * 100 * 10000 #(1.5-2.3)
# pi_hw.hardware_PWM(motorPinT, 50, dc) # 50hz, 7.5 % duty cycle(1.5 msec)
while esl_time < 30:
	els_time = time.time() - start_time
	pi_hw.hardware_PWM(motorPinT, 50, dc) # 50hz, 7.5 % duty cycle(1.5 msec)
	t -= 0.1
	dc = t / 20 * 100 * 10000 #(1.5-2.3)
	time.sleep(1)

	
	
# pi_hw.hardware_PWM(motorPinT, 50, 75000) # 50hz, 7.5 % duty cycle(1.5 msec)
# time.sleep(2)
# pi_hw.hardware_PWM(motorPinT, 50, 80000) # 50hz, 7.5 % duty cycle(1.5 msec)
# pi_hw.hardware_PWM(motorPinT, 50, dc) # 0hz, 0% duty cycle -- stop the motor!
time.sleep(1)
pi_hw.hardware_PWM(motorPinT, 0, 0) # 0hz, 0% duty cycle -- stop the motor!

pi_hw.stop() # close pi gpio DMA resources

