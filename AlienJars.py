#!/usr/bin/python
__author__ = 'madsens'
#Runs the Alien Jars. When Triggered:
# -- Bubble loop cuts to bubbles dying off video, exposing alien heads in jars. Perhaps audio associated with this video to increase intensity, but it will be bound to the audio file.

from ISStreamer.Streamer import Streamer
import sys, urllib2, time
sys.path.append("/home/pi/PiClasses")
import Logging
from termios import tcflush, TCIOFLUSH

# --------- User Settings ---------
# Initial State settings
BUCKET_NAME = ":computer: Processes"
BUCKET_KEY = "5S3HHKBXM9Y8"
ACCESS_KEY = "ibegrAmoZM9X8QQQY3j4BDA0FdZXGSqe"
PROCESS_NAME = "AlienJars"
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
    streamer.log("Activity","AlienJars - Startup")
    streamer.flush()
    dbConn = Logging.Logging()
    dbConn.logBoot()

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")

    if n == "STOP":
        Movies.StopLoop()
        if internet_on():
            streamer.log("Activity", "AlienJars - Stop")
            streamer.flush()
        #print "Stopping."
        break  # stops the loop
    else :
        # We're only logging access if there is a connection to the DB. if not, we dont do this.
        if internet_on():
            streamer.log("ID Usage", n)
            streamer.log("Activity", "AlienJars - Scan")
            streamer.flush()
            if dbConn:
                dbConn.logAccess(n)



        # flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)