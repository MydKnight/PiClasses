#!/usr/bin/python
__author__ = 'madsens'
# Runs Dai Vernon gag. Alternates between a pin to make the hand come out and show cards and a puff of "dust"

import time, sys
sys.path.append("/home/pi/PiClasses")
import Logging
import GPIOLib
from termios import tcflush, TCIOFLUSH

#Instantiate Logging and GPIO Classes
dbConn = Logging.Logging()
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [11, 13])

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else:
        dbConn.logAccess(n)

        # Trigger Hand
        gpio.on([11])
        time.sleep(1)
        gpio.off([11])
        time.sleep(15)

        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)