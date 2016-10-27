#!/usr/bin/python
__author__ = 'madsens'
#Runs the Museum Skeleton.

import time, sys, os
sys.path.append("/home/pi/PiClasses")
import Logging
import GPIOLib
from termios import tcflush, TCIOFLUSH

#Instantiate Logging and GPIO Classes
dbConn = Logging.Logging()
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [11,13])

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else :
        dbConn.logAccess(n)

        #Trigger "up" GPIO Pin.
        gpio.on([11])
        time.sleep(1)
        gpio.off([11])

        time.sleep (10)

        # Trigger "down" GPIO Pin.
        gpio.on([13])
        time.sleep(1)
        gpio.off([13])

        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)