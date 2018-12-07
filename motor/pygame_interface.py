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
	
#Some important variabels
elapse_time = 0 	
	
build_buttons(run_buttons)
start_time = time.time()

while elapse_time < 80:
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
				#press the stop button	
				print("press Play button\n")
				build_buttons(run_buttons)
				print  str(pos)
				#os.system("python try_play.py")
				os.system("python wheel_tilt_four_cores.py")
			
			#judge whether touch the area of 'Start'
			if(x > 20 and x < 160 and y > 250 and 300 > y):
				#press the Start button
				start_button_press = 1
				print ("Press Calibration button")
				print  str(pos)
				os.system("python try_calibration.py")
				
			#judge whether touch the area of 'quit'
			if (y > 250 and 300 > y and x < 460 and 300 < x):
				print("press Celebration button\n")
				print  str(pos)
				os.system("python celebration.py")
				
			if(x > 210 and x < 270 and y > 300 and 360 > y):
				print "Button quit!" + str(pos)
				# quit()
				exit()
	
exit()
