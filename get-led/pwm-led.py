import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

led = 26
fot = 6

state = 0
period = 1.0

GPIO.setup(led, GPIO.OUT)

pwm = GPIO.PWM(led, 200)
duty = 0.0
pwm.start(duty)

while True:
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.05)
    duty += 1.0
    if duty > 100.0:
        duty = 0.0