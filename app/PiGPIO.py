#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import subprocess

# IN_NO = 20 #電気ショックボタンが押されたか検出用
# OUT_NO = 21 #モーター回転用電源
# OUT_NO2 = 26 #スイッチ導通検出用電源

class PiGPIO():
    def __init__(self, conduction_check_no=20, conduction_power_no=26, motor_power_no=21):
        self.conduction_check_no=conduction_check_no
        self.conduction_power_no=conduction_power_no
        self.motor_power_no=motor_power_no
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.conduction_check_no, GPIO.IN)
        GPIO.setup(self.conduction_power_no, GPIO.OUT)
        GPIO.setup(self.motor_power_no, GPIO.OUT)
        GPIO.output(self.motor_power_no, False)
        GPIO.output(self.conduction_power_no, False)


    def check_conduction(self):
        return GPIO.input(self.conduction_check_no)

    def motor_power_on(self):
        GPIO.output(self.motor_power_no, True)

    def motor_power_off(self):
        GPIO.output(self.motor_power_no, False)

    def conduction_power_on(self):
        GPIO.output(self.conduction_power_no, True)

    def conduction_power_off(self):
        GPIO.output(self.conduction_power_no, True)

    def cleanup(self):
        GPIO.cleanup()


if __name__ == '__main__':
    gpio = PiGPIO()
    gpio.conduction_power_on()

    while True:
        print gpio.check_conduction()

    gpio.conduction_power_off()
    gpio.cleanup()
