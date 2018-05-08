import RPi.GPIO as GPIO
import time



# Pin Def

R= 17
G=27
B=22


# SETUP

GPIO.setmode(GPIO.BCM)

GPIO.setup(R,GPIO.OUT)
GPIO.setup(G,GPIO.OUT)
GPIO.setup(B,GPIO.OUT)


i = range(5)

for z in i:
    GPIO.output(R,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(G,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(B,GPIO.HIGH)

    time.sleep(1)

    GPIO.output(R,GPIO.LOW)
    GPIO.output(G,GPIO.LOW)
    GPIO.output(B,GPIO.LOW)

    time.sleep(1)


