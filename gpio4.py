import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT)
GPIO.output(4, GPIO.HIGH)

time.sleep(30)

GPIO.output(4, GPIO.LOW)
GPIO.cleanup()