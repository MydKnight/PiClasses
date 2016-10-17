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

# Gag flip bit. Controls which gag to play
gag = 0

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else:
        dbConn.logAccess(n)

        if (gag == 0):
            # Trigger Hand
            gpio.on([11])
            time.sleep(1)
            gpio.off([11])
            time.sleep(15)

            # Set bit for Dust Gag
            gag = 1

            #flush keyboard buffer
            sys.stdout.flush();
            tcflush(sys.stdin, TCIOFLUSH)
        else:
            # Trigger Dust
            gpio.on([13])
            time.sleep(1)
            gpio.off([13])
            time.sleep(15)

            # Set bit for Hand Gag
            gag = 0

            # flush keyboard buffer
            sys.stdout.flush();
            tcflush(sys.stdin, TCIOFLUSH)