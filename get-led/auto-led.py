import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led = 26
fot = 6

state = 0
period = 1.0

GPIO.setup(led, GPIO.OUT)
GPIO.setup(fot, GPIO.IN)

while True:
    if GPIO.input(fot):
        state = 0
    else:
        state = 1
    time.sleep(0.2)
    GPIO.output(led, state)
