import RPi.GPIO as GPIO
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from math import*
from time import sleep

factory=PiGPIOFactory()


class Motore:
    def __init__(self, input1, input2):
        self.in1 = input1
        self.in2 = input2
        #self.ena = ena

        self.acceso = GPIO.HIGH
        self.spento = GPIO.LOW

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        #GPIO.setup(self.ena,GPIO.OUT)
        GPIO.output(self.in1,self.spento)
        GPIO.output(self.in2,self.spento)
        #self.pwm=GPIO.PWM(self.ena,1000)
        #self.pwm.start(25)


    def direzione(self, avant):

        if avant:
            GPIO.output(self.in1,self.spento)
            GPIO.output(self.in2,self.acceso)
            print("va avanti!")

        else:
            GPIO.output(self.in1,self.acceso)
            GPIO.output(self.in2,self.spento)
            print("va indietro!")


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
        #self.pwm.ChangeDutyCycle(velocity)
        #print(velocity)

    def velocity_right(self, x, y): #metodo che chiamo nella callback
        if -0.15 <= x <= 0.15:
            x = 0
        a = 1.91
        L = 0.42 #in metri
        velocity = y + x*a*L/2
        velocity=((500/17)*abs(velocity))+(1200/17) #converto la velocità da [-1, 1] a [0, 1]
        #self.pwm.ChangeDutyCycle(velocity)
        #print(velocity)

    def spegnimento_motori(self):
        GPIO.output(self.in1, self.spento)
        GPIO.output(self.in2, self.spento)

    def shutdown(self):
        print("shutdown")
        GPIO.cleanup()


if __name__ == '__main__':
    factory=PiGPIOFactory()
    motoreFront_Right=Motore(26, 19)
    motoreFront_Left=Motore(21, 20)
    motoreBack_Right=Motore(17, 27)
    motoreBack_Left=Motore(2, 3)

    print("avanti")

    motoreFront_Right.direzione(1)
    motoreFront_Left.direzione(1)
    motoreBack_Right.direzione(1)
    motoreBack_Left.direzione(1)

    motoreFront_Right.velocity_right(1,1)
    motoreFront_Left.velocity_left(1,1)
    motoreBack_Right.velocity_right(1,1)
    motoreBack_Left.velocity_left(1,1)

    sleep(5)

    print("Spin")

    motoreFront_Right.direzione(1)
    motoreFront_Left.direzione(0)
    motoreBack_Right.direzione(1)
    motoreBack_Left.direzione(0)

    #motoreFront_Right.avanti_dietro(1)
    #motoreFront_Left.avanti_dietro(1)
    #motoreBack_Right.avanti_dietro(1)
    #motoreBack_Left.avanti_dietro(1)

    motoreFront_Right.velocity_right(1,1)
    motoreFront_Left.velocity_left(1,1)
    motoreBack_Right.velocity_right(1,1)
    motoreBack_Left.velocity_left(1,1)

    sleep(2.88)

    print("avanti")

    motoreFront_Right.direzione(1)
    motoreFront_Left.direzione(1)
    motoreBack_Right.direzione(1)
    motoreBack_Left.direzione(1)

    motoreFront_Right.velocity_right(1,1)
    motoreFront_Left.velocity_left(1,1)
    motoreBack_Right.velocity_right(1,1)
    motoreBack_Left.velocity_left(1,1)

    sleep(5)

    print("Spengo")
    motoreFront_Right.spegnimento_motori()
    motoreFront_Left.spegnimento_motori()
    motoreBack_Right.spegnimento_motori()
    motoreBack_Left.spegnimento_motori()

    motoreFront_Right.shutdown()
    motoreFront_Left.shutdown()
    motoreBack_Right.shutdown()
    motoreBack_Left.shutdown()

    motoreFront_Right=None
    motoreFront_Left=None
    motoreBack_Right=None
    motoreBack_Left=None
