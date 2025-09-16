import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led = 26
button = 13

state = 0
period = 1.0

GPIO.setup(led, GPIO.OUT)
GPIO.setup(button, GPIO.IN)


while True:
    if GPIO.input(button):
        if state == 1:
            state = 0
        else:
            state = 1
        GPIO.output(led, state)
        time.sleep(0.2)
