import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG = 3
ECHO = 18

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)

time.sleep(0.1)

x = 0
while x < 30:

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == False:
        start = time.time()

    while GPIO.input(ECHO) == True:
        end = time.time()

    signal_time = end - start

    distance = signal_time / 0.000058 # in cm

    print('Distance: {} cm'.format(distance))
    time.sleep(1)
    x += 1

GPIO.cleanup()
