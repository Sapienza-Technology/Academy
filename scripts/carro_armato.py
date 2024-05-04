import RPi.GPIO as GPIO
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from math import*
from time import sleep

factory=PiGPIOFactory()


# class Ruote:
#     def __init__(self, pin):
#         self.servo_ruote=AngularServo(pin, min_pulse_width=(0.5)/1000, max_pulse_width=(2.5)/1000, pin_factory=factory)

#     # def inclinazione(self, x):
#     #     if x==1:
#     #         self.servo_ruote.max()
#     #     elif x==-1:
#     #         self.servo_ruote.min()
#     #     elif (x==0):
#     #         self.servo_ruote.mid()
#     #     else:
#     #         self.servo_ruote.value = x




    
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

    def velocity_left(self, x, y): #metodo che chiamo nella callback
        if -0.15 <= x <= 0.15:
            x = 0
        a = 1.91
        L = 0.42 #in metri
        # velocity=((500/17)*abs(y))+(1200/17) #converto la velocità da [-1, 1] a [0, 1]
        velocity = y - x*a*L/2 
        velocity=((500/17)*abs(velocity))+(1200/17) #converto la velocità da [-1, 1] a [0, 1]
        self.pwm.ChangeDutyCycle(velocity)
        #print(velocity)
    
    def velocity_right(self, x, y): #metodo che chiamo nella callback
        if -0.15 <= x <= 0.15:
            x = 0
        a = 1.91
        L = 0.42 #in metri 
        velocity = y + x*a*L/2 
        velocity=((500/17)*abs(velocity))+(1200/17) #converto la velocità da [-1, 1] a [0, 1]
        self.pwm.ChangeDutyCycle(velocity)
        #print(velocity)

    def spegnimento_motori(self):
        GPIO.output(self.in1, self.spento)
        GPIO.output(self.in2, self.spento)

    def shutdown(self):
        print("shutdown")
        GPIO.cleanup()




