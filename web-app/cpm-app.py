import RPi.GPIO as GPIO
import time
import datetime
import thread
import threading
from flask import Flask, render_template, request, url_for
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pin1 = 23
pin2 = 24
end = 0.0
start = 0.0
elapsed = 0.0
flag = True
speed=100
angle=20

GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)

my_pwm_f = GPIO.PWM(pin1, 1000)
my_pwm_b = GPIO.PWM(pin2, 1000)


def motorF(speed, angle):
   speed_final = speed
   angle_frist = angle
   angle_secound = angle_frist / 4.2
   angle_3 = (100 - speed_final)/25
   angle_final =  angle_secound + angle_3* angle_secound
   start =0
   elapsed =0
   start = time.time()
   global flag
   flag = 1

   while angle_final >= elapsed and flag:
      my_pwm_b.stop()
      my_pwm_f.start(1)
      my_pwm_f.ChangeDutyCycle(speed_final)
      end = time.time()
      elapsed = end - start
   my_pwm_f.stop()

   """ my_pwm_b.stop()
   my_pwm_f.start(50)
   my_pwm_f.ChangeDutyCycle(speed) """


def motorB(speed, angle):
   speed_final = speed
   angle_frist = angle
   angle_secound = angle_frist / 4.2
   angle_3 = (100 - speed_final)/25
   angle_final =  angle_secound + angle_3* angle_secound
   start =0
   elapsed =0
   start = time.time()
   global flag
   flag = 1

   while angle_final >= elapsed and flag:
      my_pwm_f.stop()
      my_pwm_b.start(1)
      my_pwm_b.ChangeDutyCycle(speed_final)
      end = time.time()
      elapsed = end - start
   my_pwm_b.stop()

   """ my_pwm_f.stop()
   my_pwm_b.start(50)
   my_pwm_b.ChangeDutyCycle(speed) """


def motorStop():
   global flag
   flag = False 
   end = time.time()
   my_pwm_f.stop()
   my_pwm_b.stop()


def treatment(speed, angle, num_treatment):
   speed_final = speed
   angle_frist = angle
   angle_secound = angle_frist / 4.2
   angle_3 = (100 - speed_final)/25
   angle_final =  angle_secound + angle_3* angle_secound
   start =0
   elapsed=0
   start = time.time()
   global flag
   flag = 1

   while flag == 1:

      for x in range (num_treatment):
         if flag == 0:
               break
         my_pwm_b.stop()
         my_pwm_f.start(1)
         my_pwm_f.ChangeDutyCycle(speed_final)
         time.sleep(angle_final)
         my_pwm_f.stop()
         time.sleep(1)
         if flag == 0:
               break
         my_pwm_b.start(1)
         my_pwm_b.ChangeDutyCycle(speed_final)
         time.sleep(angle_final)
         my_pwm_b.stop()
         time.sleep(1)
      flag = 0


    

@app.route("/")
def main():
   
   return render_template('cpm-main.html')

@app.route("/", methods=['GET', 'POST'])
def action():
   action = request.form['action']
   speed = int(request.form['speed']) 
   angle = int(request.form['angle']) 
   num_treatment = int(request.form['num_treatment'])

   """ speed = 100
   angle = 20 """
   
   if action == 'treatment':
      treatment(speed, angle, num_treatment)
   if action == "motorF":
      motorF(speed, angle)
      """ t1 = threading.Thread(target=motorF, args=(speed,angle))
      t1.start() """
   if action == "motorB":
      motorB(speed, angle)
      """ t2 = threading.Thread(target=motorB, args=(speed, angle))
      t2.start() """
   if action == "motorStop":
      motorStop()
      """ t3 = threading.Thread(target=motorStop, args=())
      t3.start() """

   return render_template('cpm-main.html', action = action, speed=speed, angle=angle, num_treatment=num_treatment)


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True) 