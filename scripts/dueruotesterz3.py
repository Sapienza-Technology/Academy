import RPi.GPIO as GPIO
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from math import*
from time import sleep

factory=PiGPIOFactory()


class Ruote:
    def __init__(self, pin):
        self.servo_ruote=AngularServo(pin, min_pulse_width=(0.5)/1000, max_pulse_width=(2.5)/1000, pin_factory=factory)

    def inclinazione(self, x):
        if x==1:
            self.servo_ruote.max()
        elif x==-1:
            self.servo_ruote.min()
        elif (x==0):
            self.servo_ruote.mid()
        else:
            self.servo_ruote.value = x

class Motore:
    def __init__(self, input1, input2, ena):
        self.in1 = input1
        self.in2 = input2
        self.ena = ena

        self.acceso = GPIO.HIGH
        self.spento = GPIO.LOW

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        GPIO.setup(self.ena,GPIO.OUT)
        GPIO.output(self.in1,self.spento)
        GPIO.output(self.in2,self.spento)
        self.pwm=GPIO.PWM(self.ena,1000)
        self.pwm.start(25)



    def avanti_dietro(self, y):
        if y>0.15 and GPIO.input(self.in1)==0:
            GPIO.output(self.in1,self.acceso)
            GPIO.output(self.in2,self.spento)
            #print((GPIO.input(self.in1), GPIO.input(self.in2)))
            #print("va indietro!")
        elif y<-0.15 and GPIO.input(self.in2)==0:
            GPIO.output(self.in1,self.spento)
            GPIO.output(self.in2,self.acceso)
            #print((GPIO.input(self.in1), GPIO.input(self.in2)))
            #print("va avanti!")
        elif y>-0.15 and y<0.15:
            GPIO.output(self.in1,self.spento)
            GPIO.output(self.in2,self.spento)
            #print((GPIO.input(self.in1), GPIO.input(self.in2)))

    def velocity(self, y):
        velocity=((500/17)*abs(y))+(1200/17)
        self.pwm.ChangeDutyCycle(velocity)
        #print(velocity)

    def spegnimento_motori(self):
        GPIO.output(self.in1, self.spento)
        GPIO.output(self.in2, self.spento)

    def shutdown(self):
        print("shutdown")
        GPIO.cleanup()

class Bottoni():
    def run(self, dizionario_eventi):
        bottoni=dizionario_eventi["bottoni"]
        for i in range(len(bottoni)):
             if bottoni[i] ==1:
                 if i ==0:
                     print("A")
                     componenti['Servo_braccio_mid'][1]=True
                     componenti['Servo_braccio_low'][1]=False
                 elif i ==1:
                     print("B")
                     componenti['Servo_braccio_mid'][1]=False
                     componenti['Servo_braccio_low'][1]=True
                 elif i ==2:
                     print("X")
                 elif i ==3:
                     print("Y")
                 elif i ==4:
                     print("LEFT_BUMP")
                 elif i ==5:
                     print("RIGHT_BUMP")
                 elif i ==6:
                     print("SELECT")
                 elif i ==7:
                     print("START")
                 elif i ==8:
                     print("LEFT_STICK_BTN")
                 elif i ==9:
                     print("RIGHT_STICK_BTN")

class Pad():

    def run(self, dizionario_eventi):
        for i in range(len(self.pad)):
             if self.pad[i] ==1:
                 if i ==0:
                     k=0
                     for k in range(100):
                         componenti["Servo_braccio_mid"][0].value = k/100
                         k+=5
                 elif i ==1:
                     print("pad_right")
                 elif i ==2:
                     j=0
                     for j in range(100):
                         componenti["Servo_braccio_mid"][0].value = -j/100
                         j+=5
                         print(componenti["Servo_braccio_mid"].pulse_width)
                 elif i ==3:
                     print("pad_left")
