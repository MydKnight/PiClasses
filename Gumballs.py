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

        # Trigger GPIO Pin to dispense candy.
        # We only want one candy dispense per RFID, so first read access of this pi for a given RFID. If not 0, do not dispense
        if (dbConn.getAccess(n) > 1):
            print "Sorry, you have already retrieved your Halloween candy for this year"
        else:
            gpio.on([11])
            time.sleep(1)
            #Candy Dispense GPIO Off
            gpio.off([11])

        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)