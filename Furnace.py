__author__ = 'madsens'
from ISStreamer.Streamer import Streamer
import sys
import urllib2
sys.path.append("/home/pi/PiClasses")
import Logging
import os
import Movies
import time
from termios import tcflush, TCIOFLUSH

# --------- User Settings ---------
# Initial State settings
BUCKET_NAME = ":computer: Processes"
BUCKET_KEY = "5S3HHKBXM9Y8"
ACCESS_KEY = "ibegrAmoZM9X8QQQY3j4BDA0FdZXGSqe"
PROCESS_NAME = "Furnace"
# Set the time between checks
MINUTES_BETWEEN_READS = 15
# ---------------------------------

def internet_on():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib2.URLError as err:
        return False

streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)
if internet_on():
    streamer.log("Activity","Furnace - Startup")
    streamer.flush()
    dbConn = Logging.Logging()
    dbConn.logBoot()

Movies.StartLoop('/home/pi/Python/Assets/')

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    # Logging.HeartBeat()
    n = raw_input("Scanned ID: ")
    if n == "STOP":
        Movies.StopLoop()
        if internet_on():
            streamer.log("Activity", "Furnace - Stop")
            streamer.flush()
        #print "Stopping."
        break  # stops the loop
    else :
        # We're only logging access if there is a connection to the DB. if not, we dont do this.
        if internet_on():
            streamer.log("ID Usage", n)
            streamer.log("Activity", "Furnace - Scan")
            streamer.flush()
        if dbConn:
            dbConn.logAccess(n)

        time.sleep(.5)

        # print "Playing."
        Movies.PlayMovie()
        time.sleep(25)

        Movies.PlayLoop()

        # flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)