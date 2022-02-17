import RPi.GPIO as GPIO          
from time import sleep

leftin1 = 24
leftin2 = 23
leften = 25

rightin1 = 27
rightin2 = 22
righten = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(leftin1,GPIO.OUT)
GPIO.setup(leftin2,GPIO.OUT)
GPIO.setup(leften,GPIO.OUT)
GPIO.output(leftin1,GPIO.LOW)
GPIO.output(leftin2,GPIO.LOW)
lpwm=GPIO.PWM(leften,1000)
lpwm.start(25)

GPIO.setmode(GPIO.BCM)
GPIO.setup(rightin1,GPIO.OUT)
GPIO.setup(rightin2,GPIO.OUT)
GPIO.setup(righten,GPIO.OUT)
GPIO.output(rightin1,GPIO.LOW)
GPIO.output(rightin2,GPIO.LOW)
rpwm=GPIO.PWM(righten,1000)
rpwm.start(25)
