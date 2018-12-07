from multiprocessing import Process, Queue, Value, Lock, Array
import time
import numpy as np
import cv2
from datetime import datetime
from motor_controller import motor_controller
import RPi.GPIO as GPIO
import sys
import subprocess
import pigpio

from motor_controller import motor_controller

#set fro broadcom numbering not board numbers
GPIO.setmode(GPIO.BCM)
# Set Up Pan Tilt Servo HardwarePWM Pins
motorPinT = 12
# connect to pi gpio Daemon
pi_hw = pigpio.pi()

currentDutyCycleT = 115000 # look at forward 

#Control the wheels
def control_wheels():
	# print("control_wheels Funtion :  change the wheels\n")
	pass
	

#Rotate the camera to make the balloon in the center of the image
def rotate_camera(dir, strength):
	global currentDutyCycleT
	full_up = 65000 # 1.3ms -> up
	full_down = 115000 # 2.3ms -> forward
	increment = (full_down - full_up) / 200  #200
	#camera up
	if dir == 1: 
		currentDutyCycleT = currentDutyCycleT - strength * increment
		if currentDutyCycleT < full_up:
			currentDutyCycleT = full_up
	
	elif dir == 0: 
		pi_hw.hardware_PWM(motorPinR, 50, 0) #50 Hz Freq. 0% duty cycle
		pi_hw.hardware_PWM(motorPinT, 50, 0) #50 Hz Freq. 0% duty cycle
		currentDutyCycleT = currentDutyCycleT - strength * increment
		if currentDutyCycleT < full_up:
			currentDutyCycleT = full_down
	#camera down
	else: 
		currentDutyCycleT = currentDutyCycleT + strength * increment *2
		if currentDutyCycleT > full_down:
			currentDutyCycleT = full_down
	pi_hw.hardware_PWM(motorPinT, 50, currentDutyCycleT) #50 Hz Freq.
	##print("rotate_camera Function :  change the camera\n")


tilt_time = time.time() # record the length of giving order to tilt
#Master Process --- recognize the red balloon
def recognize_balloon(send_frame_queue, p_start_turn, p_end_turn, p_start_lock, p_end_lock): 
	global run_flag
	last_contour_receive_time = 0
	start_queue = datetime.now()
	count_put = 0
	time_total_run = time.time()
	waiting_threshold = 10
	calibration = False
	#print(run_flag.value)
	
	while(run_flag.value): 
		try:
			run_time = time.time()
			#1. get a frame and show ret, 
			_, frame = cap.read() 
			# height 480; width 640; channel 3
			#cv2.imshow('Capture', frame)
			#2. change to hsv model 
			hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
			#3. Threshold the HSV image to get only red colors and get mask 
			mask = cv2.inRange(hsv, lower_red, upper_red) #lower than 
			# #print(mask)
			# cv2.imshow('Mask_first', mask)			
			cur_time = datetime.now()
			delta_time = cur_time - start_queue
			delta_time_tol_ms = delta_time.total_seconds()*1000
		
			if (calibration): 
				#print("Calibration the camera")
				pass
				
			else: 
				#only put the mask in queue if it has past 10ms and there are less than 4 masks in queue
				if (delta_time_tol_ms > waiting_threshold) and (send_frame_queue.qsize() < 2) :
					start_queue = cur_time # Update last send to queue time
					send_frame_queue.put(mask)  # put mask in queue
					# print("send_frame_queue", send_frame_queue.qsize())
					count_put += 1
					#print("put the mask to queue\n")

			if cv2.waitKey(1) & 0xFF == ord('q'):
				run_flag.value = 0	
				time_total_run = time.time() - time_total_run
				print('count_put %d' % count_put)
				#print('count_#print_x %d' % count_#print_x)
				print('Total running time' , time_total_run)
				print("Time to process", time_total_run/count_put)
		except KeyboardInterrupt:
			run_flag.value = 0	
			time_total_run = time.time() - time_total_run
			print('count_put %d' % count_put)
			#print('count_#print_x %d' % count_#print_x)
			print('Total running time' , time_total_run)
			print("Time to process", time_total_run/count_put)
	print(run_flag.value)
	print("Quit Processor 0")
	
def process_contour_1(send_frame_queue, receive_contour_queue, 	p_start_turn, p_end_turn, p_start_lock, p_end_lock):
	global run_flag
	while (run_flag.value):
		try:
			run_time = time.time()
			# startTime = datetime.now()
			# startTime_ms = startTime.second *1000 + startTime.microsecond/1000
			# If frame queue not empty and it is Worker Process 1's turn
			if ((not send_frame_queue.empty()) and (p_start_turn.value == 1)):
				# print("1 send_frame_queue  ", send_frame_queue.qsize())
				mask = send_frame_queue.get() # Grab a frame
				p_start_turn.value = 1 # and change it to worker process 2's turn
				#find contours
				contours,h=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
				
				receive_contour_queue.put(contours) # Put contour back 
				
			else:
				##print("Processor 1 Didn't Receive Frame, sleep for 10ms")
				time.sleep(0.01)
			currentTime = datetime.now()
			currentTime_ms = currentTime.second *1000 + currentTime.microsecond/1000
			# print("processor 1 time \n\n\n\n ", time.time() - run_time)
			##print ("Processor 1 Processing Time: " + str(currentTime_ms-startTime_ms))
		except KeyboardInterrupt:
			run_flag.value = 0	
	print(run_flag.value)
	print("Quiting Processor 1")

# Function for the Worker Process 2
def calculate_contour_2(receive_contour_queue, send_motor_queue, p_start_lock, p_end_lock):
	global run_flag
	global currentDutyCycleT
	global p0,p1,p2,p3
	x_diff = 0
	y_diff = 0
	area_diff = 0
	last_areaDiff = 0
	area = 0
	last_xdiff = 0
	last_ydiff = 0
	start_time = 0
	waiting_threshold = 10
	#print("I am here1")
	tilt_lst = [0,0]
	global controller
	controller = motor_controller()
	while (run_flag.value):
		try:
			if ((not receive_contour_queue.empty())):
				#last_contour_receive_time = time.time()
				contours = receive_contour_queue.get() # Extract contour
				print("Main Processor 2: Get the processed contour from queue\n")
				print("2 receive_contour_queue  ", receive_contour_queue.qsize())
				Area_list = []
				if 0 == len(contours):
					print("Calibration --- finding balloon\n\n\n\n\n")
					# controller.set_control( 0, 0)
					controller.set_control( 0, 10)
					#time.sleep(waiting_threshold/1000.)
				else:
					run_flag.value = 0
					controller.clean()
					if run_flag.value == 0:
						p0.terminate()
						p1.terminate()
						p2.terminate()
						p3.terminate()

					# print("processor 2 time ", time.time() - run_time)
					# print("\n\n\n\n")
			else:
				#print("Processor 2 Didn't Receive Frame, sleep for 10ms")
				time.sleep(0.01)
		except KeyboardInterrupt:
			run_flag.value = 0	
			controller.clean()
			pi_hw.stop()
	print(run_flag.value)
	print("Quiting Processor 2")
	
# Function for the Worker Process 3
def process_motor_3(send_motor_queue, p_start_lock, p_end_lock):
	#print("you are there!")
	global run_flag
	while (run_flag.value):
		run_time = time.time()
		try: 
			if (not send_motor_queue.empty()):
				tilt_lst = send_motor_queue.get()
				#print("get motor queue successfully")
				for i in range(1,2):
					rotate_camera(tilt_lst[0],tilt_lst[1]/i)
					if (not send_motor_queue.empty()):
						break
					time.sleep(10/1000.)
			else: 
				#print("Processor 3 didnt receive the tilt list\n")
				time.sleep(0.01)
			# print("processor 3 send command")
			# print("processor 3 time\n\n\n\n ", time.time() - run_time)
		except KeyboardInterrupt:
			run_flag.value = 0	
	print(run_flag.value)
	print("Quiting Processor 3")
	
def __del__():
	print("del python")
	global pi_hw
	pi_hw.stop()
	controller.clean()

# set red thresh 
lower_red = np.array([156,100,40])
#156, 100, 40

upper_red = np.array([180,255,255])

x_res = 640 #320 
y_res = 480 #240 
resolution = x_res*y_res
center_x = x_res/2
center_y = y_res/2
area_ref = resolution*4/5
tolerance = 5 / 100.
x_tlr = x_res * tolerance
y_tlr = y_res * tolerance
area_tlr = resolution * tolerance
# Setting Kernel Convolution Parameters
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

cap = cv2.VideoCapture(0) 

count1 = 0
count2 = 0
count3 = 0

if __name__ == '__main__':
	# run_flag is used to safely exit all processes
	run_flag = Value('i',1)
	# p_start_turn is used to keep worker processes process in order
	p_start_turn = Value('i', 1)
	p_end_turn = Value('i', 1)
	send_frame_queue = Queue()#send frame to queue 
	receive_contour_queue = Queue()# send the processed contour to the queue
	send_motor_queue = Queue()
	p_start_lock = Lock() #Safety lock, but didnt use
	p_end_lock = Lock() #Safety lock, but didnt use
	
	p0 = Process(target=recognize_balloon, args=(send_frame_queue, p_start_turn, p_end_turn, p_start_lock, p_end_lock))
	
	p1 = Process(target=process_contour_1, args=(send_frame_queue, receive_contour_queue, p_start_turn, p_end_turn, p_start_lock, p_end_lock))
		
	p2 = Process(target=calculate_contour_2, args=(receive_contour_queue, send_motor_queue, p_start_lock, p_end_lock))
		
	p3 = Process(target=process_motor_3, args=(send_motor_queue, p_start_lock, p_end_lock))
		
	p0.start()
	p1.start()
	p2.start()
	p3.start()
	# Wait for four processes to safely exit
	print("I am here")
	print(run_flag.value)
	# if run_flag.value == 0:
		# p0.terminate()
		# p1.terminate()
		# p2.terminate()
		# p3.terminate()
		
		
	p0.join()
	print("finish the multi-processors 0\n")
	p1.join()
	print("finish the multi-processors 1\n")
	p2.join()
	print("finish the multi-processors2\n")
	p3.join()
	print("finish the multi-processors 3\n")
	#Turn off cv2 window
	pi_hw.hardware_PWM(motorPinT, 0, 0) # 0hz, 0% duty cycle -- stop the motor!
	
	pi_hw.stop() # close pi gpio DMA resources
	cap.release()
cv2.destroyAllWindows() 
			
