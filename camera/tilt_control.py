import RPi.GPIO as GPIO
import sys
import time
import pigpio

# Set GPIO Pins to be referred in Broadcom SOC channel
GPIO.setmode(GPIO.BCM)

# Set Up Pan Tilt Servo HardwarePWM Pins
