#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import subprocess

IN_NO = 12
IN_NO2 = 13
IN_NO3 = 19
OUT_NO = 16 


print "press ^C to exit program ...\n"

GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)

GPIO.setup(IN_NO, GPIO.IN)
GPIO.setup(IN_NO2, GPIO.IN)
GPIO.setup(IN_NO3, GPIO.IN)
GPIO.setup(OUT_NO, GPIO.OUT)

try:
    while True:
        GPIO.output(OUT_NO, True)
	print "{0}:{1}".format(IN_NO, GPIO.input(IN_NO))
        print "{0}:{1}".format(IN_NO2, GPIO.input(IN_NO2))
	print "{0}:{1}".format(IN_NO3, GPIO.input(IN_NO3))
except KeyboardInterrupt:
            print "detect key interrupt\n"

GPIO.cleanup()
print "Program exit\n"
