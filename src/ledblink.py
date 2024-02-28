import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) #disable annoying warning messages
GPIO.setup(17,GPIO.OUT)

#initially is off
#GPIO.output(7,GPIO.LOW)

def relay_on(gpio):
        GPIO.output(gpio,GPIO.HIGH)

def relay_off(gpio):
        GPIO.output(gpio,GPIO.LOW)
        
while True:
        relay_on(17)
        time.sleep(4)
        relay_off(17)
        time.sleep(4)

