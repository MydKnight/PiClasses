#!/usr/bin/python
__author__ = 'madsens'
#Runs the Geiger Counter gag. When Triggered:
# -- If Human: Audio plays that the alien blood is radioactive, blood glows, sounds of panic, Geiger noises go crazy
# -- If Alien: Alien voice gives dying comments, then "blood" glows and geiger goes crazy

from ISStreamer.Streamer import Streamer
import time, urllib2, sys, socket, logging, argparse, logging.handlers, socket
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


# Deafults
LOG_FILENAME = "/home/pi/Python/magiccastle.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="My simple Python service")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")

# If the log file is specified on the command line then override the default
args = parser.parse_args()
if args.log:
        LOG_FILENAME = args.log

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
        def __init__(self, logger, level):
                """Needs a logger and a logger level."""
                self.logger = logger
                self.level = level

        def write(self, message):
                # Only log if there is a message (not just a new line)
                if message.rstrip() != "":
                        self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO level -- May not need this. Only want errors
# sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)


def internet_on():
    try:
        urllib2.urlopen('http://www.cnn.com', timeout=1)
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
    streamer.log("Activity","Geiger Counter - Startup")
    streamer.flush()
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [11,12])

UDP_IP = "192.168.40.89"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        if internet_on():
            streamer.log("Activity", "Geiger Counter - Stop")
            streamer.flush()
        break  # stops the loop
    else:
        if internet_on():
            streamer.log("ID Usage", n)
            streamer.log("Activity", "Geiger Counter - Scan")
            streamer.flush()
            dbConn.logAccess(n)

        # MIB
        if n == "0009183669":
            os.system('mpg321 /home/pi/Python/Assets/mib.mp3 -q &')
        # Rachael
        elif n == "0270900574":
            os.system('mpg321 /home/pi/Python/Assets/gimme.mp3 -q &')
        #Default
        else:
        # Play Geiger Counter Sounds
            os.system('mpg321 /home/pi/Python/Assets/geigerfix.mp3 -q &')

        # Talk to Robot Voice Pi
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(n, (UDP_IP, UDP_PORT))

        #Trigger GPIO Pin for wand and needle
        gpio.on([11])
        time.sleep(11)

        #Spinner GPIO Off
        gpio.off([11])
        time.sleep(1)

        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)