#!/usr/bin/python
__author__ = 'madsens'
# Runs Houdini Gag. On trigger, chains wrapping picture break, crystal ball activates and sound file plays.
# Chains Break. Remain Broken for 6 seconds. Then Reset. Leave sound placeholder in.
# Crystal ball runs for 10 seconds with ten second song as well
# No Timeout

import time, sys, os, subprocess
sys.path.append("/home/pi/PiClasses")
import Logging
import GPIOLib
from random import randint
from termios import tcflush, TCIOFLUSH

#Instantiate Logging and GPIO Classes
dbConn = Logging.Logging()
gpio = GPIOLib.GPIOLib("BOARD", "HIGH", [11, 13, 15])

#Houdini does two effects. This var tracks what the current trick to play is.
gag = "chain"

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else :
        gag = randint(1,4)
        if gag == 1:
            #Chains
            dbConn.logAccess(n)

            # Play Chain Break mp3
            os.system('mpg321 /media/usb0/Assets/ChainDropped.mp3 -q &')

            #Trigger GPIO Pin to break Chains and set back to low.
            gpio.on([11])
            time.sleep(1)
            gpio.off([11])

            #Wait 6 seconds, then trigger chain reform
            time.sleep(6)
            gpio.on([13])
            time.sleep(1)
            gpio.off([13])

            #flush keyboard buffer
            sys.stdout.flush();
            tcflush(sys.stdin, TCIOFLUSH)
        elif gag == 2:
            # Ball
            dbConn.logAccess(n)

            # Play one of two rosabelle sound clips
            clip = randint(1,2)
            if clip == 1:
                os.system('mpg321 -k 1000 /media/usb0/Assets/1.mp3 -q &')
            else:
                os.system('mpg321 -k 1000 /media/usb0/Assets/2.mp3 -q &')

            # Trigger GPIO Pins for crystal ball activation
            gpio.on([15])
            time.sleep(1)
            gpio.off([15])

            # Play song for 15 seconds, then kill song and trigger gpio for ball again to stop its effect
            time.sleep(15)
            gpio.on([15])
            time.sleep(1)
            gpio.off([15])

            # flush keyboard buffer
            sys.stdout.flush();
            tcflush(sys.stdin, TCIOFLUSH)
        elif gag == 3:
            # Houdini Recording
            os.system('mpg321 -k 1000 /media/usb0/Assets/3.mp3 -q &')
        else:
            # Houdini Obit
            os.system('mpg321 -k 1000 /media/usb0/Assets/4.mp3 -q &')

'''
Chain:
Trigger Chain Break Pin + Play Chain Break MP3
Wait 6 Seconds
Trigger Chain Reform
Wait 5 seconds
Clear Buffer

Ball:
Trigger Ball + Play Ball Audio
Wait 10 seconds
Trigger Ball again to stop
Clear Buffer
'''