#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)
num = 0;
while num < 1000000:
    GPIO.output(18, True)
    num += 1
print "End"
GPIO.cleanup()
