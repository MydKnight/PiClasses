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
        if (gag == "chain"):
            #Set gag to Crystal Ball
            gag = "ball"

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
        else:
            #Set gag to Chain
            gag = "chain"

            dbConn.logAccess(n)

            # Play Rosalie Sound Clip - 1000 frames in seems a good number
            os.system('mpg321 -k 1000 /media/usb0/Assets/Rosabelle\ Believe.mp3 -q &')

            # Trigger GPIO Pins for crystal ball activation
            gpio.on([15])
            time.sleep(1)
            gpio.off([15])

            # Play song for 15 seconds, then kill song and trigger gpio for ball again to stop its effect
            time.sleep(15)
            gpio.on([15])
            time.sleep(1)
            gpio.off([15])
            subprocess.Popen(['sudo', 'pkill', 'mpg321'])

            # flush keyboard buffer
            sys.stdout.flush();
            tcflush(sys.stdin, TCIOFLUSH)

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