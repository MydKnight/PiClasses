#!/usr/bin/python
__author__ = 'madsens'
#Runs singing skulls

import time, sys, os
sys.path.append("/home/pi/PiClasses")
import Logging
import GPIOLib
from termios import tcflush, TCIOFLUSH

#Instantiate Logging and GPIO Classes
dbConn = Logging.Logging()
gpio = GPIOLib.GPIOLib("BOARD", "HIGH", [11])

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else :
        dbConn.logAccess(n)

        #Trigger GPIO Pins. The skulls are only started by the tap of a space bar. As a result, we just need to turn the pin on, then off
        gpio.on([11])
        time.sleep(1)
        #Keyboard hit GPIO Off
        gpio.off([11])

        #Don't allow a new trigger for the length of the song
        time.sleep(5)

        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)