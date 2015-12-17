#!/usr/bin/python
 
import RPi.GPIO as GPIO
import time

IN_NO = 26
OUT_NO = 20
 
print "press ^C to exit program ...\n"
 
GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)
 
GPIO.setup(IN_NO, GPIO.IN)
GPIO.setup(OUT_NO, GPIO.OUT)
 
try:
 while True:
  GPIO.output(OUT_NO, True)
  if GPIO.input(IN_NO):
    print
  print GPIO.input(IN_NO)
except KeyboardInterrupt:
 print "detect key interrupt\n"
 
GPIO.cleanup()
print "Program exit\n"
