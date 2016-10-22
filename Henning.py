#!/usr/bin/python
__author__ = 'madsens'
# Runs the Doug Henning Altar effect. When triggered spins a wheel with sounds.

import time, sys
sys.path.append("/home/pi/PiClasses")
import Logging
import GPIOLib
from termios import tcflush, TCIOFLUSH

# Instantiate Logging and GPIO Classes
dbConn = Logging.Logging()
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [11])

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else:
        dbConn.logAccess(n)

        # Trigger GPIO Pins. Henning gag just uses one pin
        gpio.on([11])
        time.sleep(10)

        # Spinner GPIO Off
        gpio.off([11])
        time.sleep(1)

        # Flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)