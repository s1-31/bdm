import Rhi.GPIO as GPIO
import commands
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(18)
    input_state2 = GPIO.input(23)
    if input_state == False:
        #print(commands.getstatusoutput('toggle-timer.sh'))
        print(commands.getstatusoutput('toggle-xstroke.sh'))
	#print(commands.getstatusoutput('ls -l'))
	time.sleep(0.2)

    if input_state2 == False:
        #print(commands.getstatusoutput('sudo killall xstroke'))
        print(commands.getstatusoutput('ls -l'))
        time.sleep(0.2)
