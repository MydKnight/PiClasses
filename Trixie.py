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
        time.sleep(2)
        # Trigger Peppers Ghost - 13
        gpio.on([13])

        #Trixie Turn off Pepper
        gpio.off([13])
        time.sleep(12)

        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)