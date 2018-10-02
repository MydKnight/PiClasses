#!/usr/bin/python
__author__ = 'madsens'
#Runs the Geiger Counter gag. When Triggered:
# -- If Human: Audio plays that the alien blood is radioactive, blood glows, sounds of panic, Geiger noises go crazy
# -- If Alien: Alien voice gives dying comments, then "blood" glows and geiger goes crazy

from ISStreamer.Streamer import Streamer
import time, sys
sys.path.append("/home/pi/PiClasses")
import Logging
import GPIOLib
from termios import tcflush, TCIOFLUSH

# --------- User Settings ---------
# Initial State settings
BUCKET_NAME = ":computer: Processes"
BUCKET_KEY = "5S3HHKBXM9Y8"
ACCESS_KEY = "ibegrAmoZM9X8QQQY3j4BDA0FdZXGSqe"
PROCESS_NAME = "GeigerCounter"
# Set the time between checks
MINUTES_BETWEEN_READS = 15
# ---------------------------------

#Instantiate Logging and GPIO Classes
dbConn = Logging.Logging()
dbConn.logBoot()
streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)
streamer.log("Activity","RFID Tester - Startup")
streamer.flush()
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [11])

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        streamer.log("Activity", "RFID Tester - Stop")
        streamer.flush()
        break  # stops the loop
    else:
        streamer.log("ID Usage", n)
        streamer.log("Activity", "RFID Tester - Scan")
        streamer.flush()
        dbConn.logAccess(n)

        #Trigger GPIO Pins. Spinner just uses one pin
        gpio.off([11])
        time.sleep(1)

        #Spinner GPIO Off
        gpio.on([11])
        time.sleep(1)

        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)