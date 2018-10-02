#!/usr/bin/python
__author__ = 'madsens'
#Runs the Robot Voice. Will be triggered by GPIO Input:


from ISStreamer.Streamer import Streamer
import time, urllib2, sys, socket
import Logging
import GPIOLib
import os
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

def internet_on():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib2.URLError as err:
        return False
    except socket.timeout, e:
        return False

#Instantiate Logging and GPIO Classes
if internet_on():
    dbConn = Logging.Logging()
    dbConn.logBoot()
    streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)
    streamer.log("Activity","Robot Voice - Startup")
    streamer.flush()
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [11,12])

UDP_IP = "192.168.40.89"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                 socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
# Wait till about 4.5 secs through the play
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    if data == "0270906975":
        time.sleep(7)
        os.system('mpg321 /home/pi/Python/Assets/dangeralan.mp3 -q &')
    else:
        time.sleep(7)
        os.system('mpg321 /home/pi/Python/Assets/Danger.mp3 -q &')
    print "received message:", data