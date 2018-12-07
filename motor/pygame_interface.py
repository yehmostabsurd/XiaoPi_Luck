#########################################################
### Yanling Wu (yw996), Yeh Dawei(ty359)			   ##
### This is the code to build the pygame interface     ##
### to control the different modes.			 	       ##
#########################################################

import time
from pygame.locals import *
import pygame
import os

#initilization pygame
pygame.init()
pygame.mouse.set_visible(True)
WHITE = 255, 255, 255
BLACK = 0,0,0
Red = 255,0,0
Green = 0,255,0
screen = pygame.display.set_mode((480, 360))
my_font = pygame.font.Font(None, 40)
run_buttons = {'Play':(240,180), 'Calibration':(90,280), 'Celebration':(390,280), "Quit":(240,330)}
stop_buttons = {'RESUME':(240,180), 'Calibration':(90,280), 'Celebration':(390,280), "Quit":(240,330)}
background_image = pygame.image.load("img3.jpg").convert()

#Define the function of building the buttons
def build_buttons(buttons):
	screen.fill(BLACK) # Erase the Work space	
	screen.blit(background_image, [0, 0])
	for my_text, text_pos in buttons.items():
		if(my_text == 'Play'):
			pygame.draw.circle(screen, Red, text_pos, 50, 0)
		text_surface = my_font.render(my_text, True, WHITE)
		rect = text_surface.get_rect(center=text_pos)
		screen.blit(text_surface, rect)
	pygame.display.flip()
	
#Some variables
elapse_time = 0 	
start_time = time.time()

#build original buttons
build_buttons(run_buttons)
#Main loop
while elapse_time < 1200:
	elapse_time = time.time() - start_time
	time.sleep(0.2) 
	#touching the buttons on the screen
	for event in pygame.event.get():
		if(event.type is MOUSEBUTTONDOWN):
            #get touch position
			pos = pygame.mouse.get_pos()
		elif(event.type is MOUSEBUTTONUP):
			pos = pygame.mouse.get_pos()
			x,y = pos
			#judge whether touch the area of 'Play'
			if(x > 190 and x < 290 and y >130 and y < 230):
				#press the play button	
				text = "I am trying to pop the balloon"
				run_buttons.clear()
				run_buttons = {'Play':(240,180), 'Calibration':(90,280), 'Celebration':(390,280), "Quit":(240,330), text:(240,50)}
				build_buttons(run_buttons)
				#open the another file of main code
				os.system("python wheel_tilt_four_cores.py")
				
				text = "I have poped a balloon"
				run_buttons.clear()
				run_buttons = {'Play':(240,180), 'Calibration':(90,280), 'Celebration':(390,280), "Quit":(240,330), text:(240,50)}
				build_buttons(run_buttons)
			
			#judge whether touch the area of 'Calibration'
			if(x > 20 and x < 160 and y > 250 and 300 > y):
				#press the Calibration button
				text = "I am looking for a balloon"
				run_buttons.clear()
				run_buttons = {'Play':(240,180), 'Calibration':(90,280), 'Celebration':(390,280), "Quit":(240,330), text:(240,50)}
				build_buttons(run_buttons)
				#open the another file of "Calibration"
				os.system("python try_calibration.py")
				
				text = "I have calibrated, ready to play"
				run_buttons.clear()
				run_buttons = {'Play':(240,180), 'Calibration':(90,280), 'Celebration':(390,280), "Quit":(240,330), text:(240,50)}
				build_buttons(run_buttons)
				
			#judge whether touch the area of 'Celebration'
			if (y > 250 and 300 > y and x < 460 and 300 < x):
				text = "Yeah~ Let's celebrate~~~~"
				run_buttons.clear()
				run_buttons = {'Play':(240,180), 'Calibration':(90,280), 'Celebration':(390,280), "Quit":(240,330), text:(240,50)}
				build_buttons(run_buttons)
				#open the another file of "Celebration"
				os.system("python celebration.py")
				
			if(x > 210 and x < 270 and y > 300 and 360 > y):
				text = "ByeBye~ Have A Good Day!!!"
				run_buttons.clear()
				run_buttons = {'Play':(240,180), 'Calibration':(90,280), 'Celebration':(390,280), "Quit":(240,330), text:(240,50)}
				build_buttons(run_buttons)
				exit()
	
	
