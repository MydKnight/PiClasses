#!/usr/bin/python
__author__ = 'madsens'

import sys, time, os, subprocess
sys.path.append("/home/pi/PiClasses")
import GPIOLib
import Logging
from termios import tcflush, TCIOFLUSH

dbConn = Logging.Logging()

# We're doing multiple things now. Pepper Flip = 11, Blue Light = 13, Fan = 15, Air Blast = 7
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [11, 13, 15])

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else :
        dbConn.logAccess(n)

        os.system('mpg321 /home/pi/Python/Assets/chimes.mp3 -q &')
        time.sleep(4)
        # Trigger Peppers Ghost, Fan, Blue Light - 13, 15
        gpio.on([13,15])

        if (n == '0006701791'):
            # Play My Sharona Sound - If shiloh scans
            os.system('mpg321 -k 1600 /home/pi/Python/Assets/sharona.mp3 -q &')
        else:
            os.system('mpg321 /home/pi/Python/Assets/screams.mp3 -q &')

        # Fire Air Burst - 7
        gpio.on([11])
        time.sleep(1)
        gpio.off([11])
        time.sleep(.5)

        gpio.on([11])
        time.sleep(1)
        gpio.off([11])
        time.sleep(.5)

        gpio.on([11])
        time.sleep(1)
        gpio.off([11])

        time.sleep(5.5)

        #Trixie Turn off Pepper, Light, Fan
        gpio.off([13, 15])
        time.sleep(.1)

        # Kill MPG321
        subprocess.Popen(['sudo', 'pkill', 'mpg321'])

        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)