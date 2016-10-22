#!/usr/bin/python
__author__ = 'madsens'
#Runs Sanctuary candles. 1/10 triggers causes evil laugh w all candles go out, then reset back to normal 30 seconds later.

import time, sys, os
sys.path.append("/home/pi/PiClasses")
import Logging
import serial
from termios import tcflush, TCIOFLUSH
from random import randint

#Instantiate Logging and serial
dbConn = Logging.Logging()
port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=3.0)

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else:
        effect = randint(1, 10)
        dbConn.logAccess(n)

        if (effect == 1):
            # Laugh/Lights Out
            os.system('mpg321 /media/usb0/Assets/audio1.mp3 -q &')
            time.sleep (2)
            port.write("\r\n0")
            rcv = port.read(10)
            time.sleep(30)
            port.write("\r\n1")
        else:
            # Crying/Candle Light
            os.system('mpg321 /media/usb0/Assets/audio2.mp3 -q &')
            time.sleep(5)
            port.write("\r\n2")
            rcv = port.read(10)
            time.sleep(20)

        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)