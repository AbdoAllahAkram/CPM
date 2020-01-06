import RPi.GPIO as GPIO
import time
from tkinter import *
import datetime
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pin1 = 23
pin2 = 24
end = 0.0
start = 0.0
elapsed = 0.0
flag = 1
GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
my_pwm_f = GPIO.PWM(pin1, 1000)
my_pwm_b = GPIO.PWM(pin2, 1000)


def treatment():
    speed_final = int(speed.get())
    angle_frist = int(angle.get())
    angle_secound = angle_frist / 4.2
    angle_3 = (100 - speed_final)/25
    angle_final =  angle_secound + angle_3* angle_secound
    num_treatment = int(Etreatment.get())
    global start 
    global  elapsed
    start = time.time()
    global flag
    flag = 1

    while flag == 1:

        for x in range (num_treatment):
            if flag == 0:
                break
            my_pwm_b.stop()
            my_pwm_f.start(50)
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

def motorF():

    speed_final = int(speed.get())
    angle_frist = int(angle.get())
    angle_secound = angle_frist / 4.2
    angle_3 = (100 - speed_final)/25
    angle_final =  angle_secound + angle_3* angle_secound
    global start 
    global  elapsed
    start = time.time()
    global flag
    flag = 1

    while angle_final >= elapsed and flag == 1:
        my_pwm_b.stop()
        my_pwm_f.start(50)
        my_pwm_f.ChangeDutyCycle(speed_final)
        end = time.time()
        elapsed = end - start
    my_pwm_f.stop()
    

def motorB():

    speed_final = int(speed.get())
    angle_frist = int(angle.get())
    angle_secound = angle_frist / 4.2
    angle_3 = (100 - speed_final)/25
    angle_final =  angle_secound + angle_3* angle_secound
    global start 
    global  elapsed
    start = time.time()
    global flag
    flag = 1

    while angle_final >= elapsed and flag == 1:
        my_pwm_f.stop()
        my_pwm_b.start(50)
        my_pwm_b.ChangeDutyCycle(speed_final)
        end = time.time()
        elapsed = end - start
    my_pwm_b.stop()

def motorStop():
    global flag
    flag = 0
    end = time.time()
    my_pwm_f.stop()
    my_pwm_b.stop()
    elapsed = end - start
    print(elapsed)

def setFreq(event):
    freq_final = int(freq.get())
    my_pwm_f = GPIO.PWM(pin1, freq_final)
    my_pwm_b = GPIO.PWM(pin2, freq_final)

def treatmentUp(event):
    treat_final = int(Etreatment.get())
    treat_final += 1
    Etreatment.delete(0, 'end')
    Etreatment.insert(10, str(treat_final)) 

def treatmentDown(event):
    treat_final = int(Etreatment.get())
    treat_final -= 1
    Etreatment.delete(0, 'end')
    Etreatment.insert(10, str(treat_final)) 

def tTreatment(event):
    t1 = threading.Thread(target=treatment, args=())
    t1.start()

def tMotorF(event):
    t2 = threading.Thread(target=motorF, args=())
    t2.start()

def tMotorB(event):
    t3 = threading.Thread(target=motorB, args=())
    t3.start()

def tMotorStop(event):
    t4 = threading.Thread(target=motorStop, args=())
    t4.start()


root = Tk()
frame = Frame(root)
frame.pack()
label_freq = Label(frame, text="Frequancy")
label_speed = Label(frame, text="Speed")
label_angle = Label(frame, text="Angle")

label_freq.grid(row=0)
label_speed.grid(row=1, column=0)
label_angle.grid(row=2, column=0)

freq = Entry(frame)
speed = Entry(frame)
angle = Entry(frame)
Etreatment = Entry(frame)

freq.grid(row=0, column=1)
speed.grid(row=1, column=1)
angle.grid(row=2, column=1)
Etreatment.grid(row=3, column=1)

freq.insert(10,"1000")
speed.insert(10, "100")
angle.insert(10, "30")
Etreatment.insert(10, "3")

freq_final = int(freq.get())


buttonTreatment = Button(frame, text="Treatment", height=2)
button1 = Button(frame, text="Forword", height=2)
button2 = Button(frame, text="Back", height=2)
button3 = Button(frame, text="STOP", height=2)
button4 = Button(frame, text="SET Frequance", fg="red", height=2)
button5 = Button(frame, text="▲", width=5, fg="red", height=2)
button6 = Button(frame, text="▼", width=5, fg="red", height=2)

buttonTreatment.bind("<Button-1>", tTreatment)
button1.bind("<Button-1>", tMotorF)
button2.bind("<Button-1>", tMotorB)
button3.bind("<Button-1>", tMotorStop)
button4.bind("<Button-1>", setFreq)
button5.bind("<Button-1>", treatmentUp)
button6.bind("<Button-1>", treatmentDown)

buttonTreatment.grid(row=3)
button1.grid(row=4)
button2.grid(row=5)
button3.grid(row=6)
button4.grid(row=7)
button5.grid(row=4, column=1)
button6.grid(row=5, column=1)

frame.mainloop()