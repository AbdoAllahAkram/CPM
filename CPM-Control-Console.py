import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

pin1 = 23
pin2 = 24
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
freq = int(input("put frequancy: "))



try:
    while(1):
        direction = input("put direction: ")
        speed = int(input("put speed: "))

        if direction == 'f':
            my_pwd = GPIO.PWM(pin2, freq)
            my_pwd.start(0)
            my_pwd.ChangeDutyCycle(speed)
            GPIO.output(pin1, 0)
        elif direction == 'b':
            my_pwd = GPIO.PWM(pin1, freq)
            my_pwd.start(0)
            my_pwd.ChangeDutyCycle(speed)
            GPIO.output(pin2, 0)


except KeyboardInterrupt:
    pass

#my_pwd.stop()
GPIO.cleanup()
