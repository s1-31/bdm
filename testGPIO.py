#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import subprocess

IN_NO = 20 #電気ショックボタンが押されたか検出用
OUT_NO = 21 #モーター回転用電源
OUT_NO2 = 26 #スイッチ導通検出用電源


print "press ^C to exit program ...\n"

GPIO.setmode(GPIO.BCM)
#GPIO.setmode(GPIO.BOARD)

GPIO.setup(IN_NO, GPIO.IN)
#GPIO.setup(OUT_NO, GPIO.OUT)
GPIO.setup(OUT_NO2, GPIO.OUT)

try:
    while True:
        #GPIO.output(OUT_NO, True)
	GPIO.output(OUT_NO2, True)
	print GPIO.input(IN_NO)
except KeyboardInterrupt:
            print "detect key interrupt\n"

GPIO.cleanup()
print "Program exit\n"
