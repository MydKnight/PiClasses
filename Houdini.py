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
# Make pin 11 low and 13 to high for antenna to work
gpio.off([11, 13])

# gag = 1
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
            os.system('mpg321 /home/pi/Assets/chains.mp3 -q &')

            #Trigger GPIO Pin to break Chains and set back to low.
            gpio.on([13])

            #Wait 14 seconds, then trigger chain reform
            time.sleep(14)
            gpio.off([13])

            # Play Chain Break mp3
            os.system('mpg321 /home/pi/Assets/chains.mp3 -q &')
            time.sleep(5)

            #flush keyboard buffer
            sys.stdout.flush();
            tcflush(sys.stdin, TCIOFLUSH)
        elif gag == 2:
            # Ball
            dbConn.logAccess(n)

            # Trigger GPIO Pins for crystal ball activation
            gpio.off([15])
            time.sleep(1)
            gpio.on([15])

            # Play one of two rosabelle sound clips
            clip = randint(1, 2)
            if clip == 1:
                os.system('mpg321 -g 20 /home/pi/Assets/rosabelle-lyrics.mp3 -q')
            else:
                os.system('mpg321 -g 40 /home/pi/Assets/rosabelle-organ.mp3 -q')

            # flush keyboard buffer
            sys.stdout.flush();
            tcflush(sys.stdin, TCIOFLUSH)
        elif gag == 3:
            # Houdini Recording
            os.system('mpg321 -g 10 /home/pi/Assets/houdini-voice.mp3 -q')
        else:
            # Houdini Obit
            os.system('mpg321 -g 10 /home/pi/Assets/houdini-voice.mp3 -q')