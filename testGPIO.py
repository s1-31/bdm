#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import subprocess

IN_NO = 26
OUT_NO = 21

print "press ^C to exit program ...\n"

GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)

GPIO.setup(IN_NO, GPIO.IN)
GPIO.setup(OUT_NO, GPIO.OUT)

n=0

try:
    while True:
        GPIO.output(OUT_NO, True)
	if GPIO.input(IN_NO):
	    if n == 0:
		process = subprocess.Popen('toggle-timer.sh')
		print 'OK'
		n+=1
	    elif n == 2:
		process = subprocess.Popen('sudo killall python')
		#process = subprocess.Popen('toggle-timer.sh')
		print 'Close'
		n+=1
	else:
	    if n == 1:
		n+=1
	    elif n == 3:
		n = 0
	#print GPIO.input(IN_NO)
        #if GPIO.input(IN_NO):
            #print process.poll()

except KeyboardInterrupt:
            print "detect key interrupt\n"

GPIO.cleanup()
print "Program exit\n"
