#!/usr/bin/python
__author__ = 'madsens'
#Runs the RFID Tester in the lobby. When triggered spins a wheel with sounds.

import time, sys
sys.path.append("/home/pi/PiClasses")
import Logging
import RPi.GPIO as GPIO
from termios import tcflush, TCIOFLUSH

# Instantiate Logging and GPIO Classes
dbConn = Logging.Logging()

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    # Manual setup of GPIO pins
    GPIO.setmode(GPIO.BOARD)

    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else:
        dbConn.logAccess(n)

        GPIO.setup(11, GPIO.OUT)
        time.sleep(1)

        GPIO.cleanup()
        time.sleep(1)

        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)