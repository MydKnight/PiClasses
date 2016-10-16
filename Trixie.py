#!/usr/bin/python
__author__ = 'madsens'

import sys, time, os, subprocess
sys.path.append("/home/pi/PiClasses")
import GPIOLib
import Logging
from termios import tcflush, TCIOFLUSH

dbConn = Logging.Logging()

# We're doing multiple things now. Pepper Flip = 11, Blue Light = 13, Fan = 15, Air Blast = 7
gpio = GPIOLib.GPIOLib("BOARD", "HIGH", [7, 11, 13, 15])

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else :
        dbConn.logAccess(n)

        # Trigger Peppers Ghost, Fan, Blue Light - 11, 13, 15
        gpio.on([11, 13, 15])
        time.sleep(1)

        if (n == '0005784121'):
            # Play My Sharona Sound - If shiloh scans
            os.system('mpg321 -k 1600 /media/usb0/Assets/sharona.mp3 -q &')
        else:
            os.system('mpg321 /media/usb0/Assets/wraith.mp3 -q &')
        # Fire Air Burst - 7
        gpio.on([7])
        time.sleep(1)
        gpio.off([7])

        time.sleep(10)

        #Trixie Turn off Pepper, Light, Fan
        gpio.off([11, 13, 15])

        # Kill MPG321
        subprocess.Popen(['sudo', 'pkill', 'mpg321'])

        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)