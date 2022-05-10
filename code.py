#Title: Task 7.3D Raspberry Pi PWM
#Author: Matthew Murrell - 218296335
#Date: 8/05/2022
#Purpose: Increases the light level of an LED as a proximity sensor detects closer objects.
#Developed using information from the following tutorials:
    #Electronic Wings: https://www.electronicwings.com/raspberry-pi/raspberry-pi-pwm-generation-using-python-and-c
    #ThePiHut: https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi 

#LIBRARIES
import RPi.GPIO as GPIO
import time

#PINOUT
LED = 12    #The pin connected to the LED
#GND = 34
TRIG = 16   #The pin connected to the TRIG pin on the HC-SR04
ECHO = 18   #The pin connected to the ECHO pin on the HC-SR04
#VCC = 2

MAX_DIST = 25

#GPIO Setup
GPIO.setmode(GPIO.BOARD)	#Sets the pins to GPIO mode
GPIO.setup(LED,GPIO.OUT)    #Sets the LED pin to output
GPIO.setup (TRIG,GPIO.OUT)  #Sets the TRIG pin to output
GPIO.setup (ECHO, GPIO.IN)  #Sets the ECHO pin to input

led_pwm = GPIO.PWM(LED,1000)	#create PWM instance with frequency
led_pwm.start(0)				#start PWM of required Duty Cycle

    
#Allowing the sensor to settle
GPIO.output (TRIG, False)
time.sleep(2)

#Emits a pulse from the HC-SR04 and returns the time that it takes to return to the sensor
def get_pulse_duration():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while (GPIO.input(ECHO)== 0):
        pulse_start = time.time()
    
    while GPIO.input (ECHO) == 1:
        pulse_end = time.time()
        
    return (pulse_end - pulse_start)

#Returns the distance detected by the HC-SR04
def get_distance():
    
    duration = get_pulse_duration()
    #Converts the duration into distance
    distance = duration * 17150
    #Returns the distance rounded to 2 deciman places
    return round (distance, 2)

#Uses PWM to light up the LED proportionally to it's proximity to the sensor
def light_pwm_led(distance):
    if distance <= MAX_DIST:
        #If something is detected within 25cm, the LED is lit up at a level inversely proportionate to the distance 
        led_pwm.ChangeDutyCycle((MAX_DIST - distance) * (100/MAX_DIST))
    
    else:
        #If nothing is detected within 25cm, the LED is turned off
        led_pwm.ChangeDutyCycle(0)
    time.sleep(0.1)   

#The main loop of the program. Loops until interrupted
try:
    while True:
        distance = get_distance()
        light_pwm_led(distance)

#Cleans up GPIO pins when exiting the program
except KeyboardInterrupt:
    GPIO.cleanup()
    
