#!/usr/bin/env python
## Recognize the objects with specific color

import cv2 
import time
import numpy as np 
from rrb3 import *

cap = cv2.VideoCapture(0) 
# set red thresh 
lower_red = np.array([156,100,80])
upper_red = np.array([180,255,255])

x_res = 640 #320 
y_res = 480 #240 
center_x = x_res/2
center_y = y_res/2
x_diff = 0
y_diff = 0

# Setting Kernel Convolution Parameters
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

BATTERY_VOLTS = 8
MOTOR_VOLTS = 5

rr = RRB3(BATTERY_VOLTS, MOTOR_VOLTS)
speedl = 0.5
speedr = 0.5
dl = 1 #randint(0, 1)
dr = 0 #randint(0, 1)

#time.sleep(1)
while(1): 
	# get a frame and show ret, 
	_, frame = cap.read() 
	# height 480; width 640; channel 3
	cv2.imshow('Capture', frame)
	# change to hsv model 
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
	# get mask 
	mask = cv2.inRange(hsv, lower_red, upper_red) #lower than 
	# print(mask)
	cv2.imshow('Mask', mask) 
	
	start_time = time.time()
	# maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
	# maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
	# contours,h=cv2.findContours(maskClose.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	contours,h=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	#contours,hierarchy = cv2.findContours(mask, 1, 2)
	
	area = []
	if 0 == len(contours):
		rr.set_motors(speedl, dl, speedr, dr)
		time.sleep(0.2)
	else:
		#for c in contours:
		#	area.append(cv2.contourArea(c) )
		area = [ cv2.contourArea(c) for c in contours ]
		#print area
		maxindex = area.index(max(area))
		#print maxindex
		cnt = contours[maxindex]#Get the first contour 
		#print (contours[0])
		M = cv2.moments(cnt)#Calculat M of the first contour
		# print (M)
		#calcualte the center coordinate
		if M['m00'] != 0:	
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			x_diff = abs(cx - center_x)
			y_diff = abs(cy - center_y)
			print("x_bar=%f, y_bar= %f" % (cx,cy))
			print("x_diff= %f, y_diff= %f" % (x_diff,y_diff))
			#area = cv2.contourArea(cnt)
			print("Area = %f" %M['m00'])
			cv2.circle(frame, (cx, cy), 7, (255, 255, 255), -1) #Draw center of object
			cv2.drawContours(frame,contours,-1,(255,0,0),3) #Draw contour of object
			cv2.circle(frame, (center_x, center_y), 2, (0, 0, 255), -1) #Draw center of camera
			cv2.imshow('frame',frame) #Display Frame
		
	cal_time = time.time() - start_time
	print("Running time = ", cal_time)
	#text = "(x_bar,y_bar)"
	#font = cv2.FONT_HERSHEY_SUPLEX 
	# font=cv2.InitFont(cv.CV_FONT_HERSHEY_SCRIPT_SIMPLEX, 1, 1, 0, 3, 8)
	#cv2.putText(mask,text, (300,300),font,2,(0,0,255), 1)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		rr.cleanup()
		break

cap.release()
cv2.destroyAllWindows()
