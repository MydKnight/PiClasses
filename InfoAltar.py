#!/usr/bin/python
__author__ = 'madsens'
# Runs the Informational Altar

import time, sys, os
sys.path.append("/home/pi/PiClasses")
import Logging
import GPIOLib
from termios import tcflush, TCIOFLUSH

# Instantiate Logging and GPIO Classes
dbConn = Logging.Logging()
gpio = GPIOLib.GPIOLib("BOARD", "HIGH", [7, 11, 13, 21, 29])

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else :
        dbConn.logAccess(n)

        # Trigger first element/info bar.
        gpio.off([7])
        time.sleep(6)
        gpio.on([7])

        time.sleep (2)

        # Trigger second element/info bar.
        gpio.off([11])
        time.sleep(6)
        gpio.on([11])

        time.sleep(2)

        # Trigger third element/info bar.
        gpio.off([13])
        time.sleep(6)
        gpio.on([13])

        time.sleep(2)

        # Trigger fourth element/info bar.
        gpio.off([21])
        time.sleep(6)
        gpio.on([21])

        time.sleep(2)

        # Trigger fifth element/info bar.
        gpio.off([29])
        time.sleep(6)
        gpio.on([29])

        time.sleep(2)

        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)