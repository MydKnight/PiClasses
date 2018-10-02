#!/usr/bin/python
__author__ = 'madsens'
# Runs the 'Do Not Press Me' Button

from ISStreamer.Streamer import Streamer
import time, sys, os, urllib2,logging, argparse,logging.handlers
import Logging, GPIOLib
from termios import tcflush, TCIOFLUSH
import RPi.GPIO as GPIO

# --------- User Settings ---------
# Initial State settings
BUCKET_NAME = ":computer: Processes"
BUCKET_KEY = "5S3HHKBXM9Y8"
ACCESS_KEY = "ibegrAmoZM9X8QQQY3j4BDA0FdZXGSqe"
PROCESS_NAME = "Button"
# Set the time between checks
MINUTES_BETWEEN_READS = 15
# ---------------------------------

# Deafults
LOG_FILENAME = "/home/pi/Python/magiccastle.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="Button Program")
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
#sys.stderr = MyLogger(logger, logging.ERROR)

# Helper Library to determine if we have internet before logging things.
def internet_on():
    try:
        urllib2.urlopen('http://www.cnn.com', timeout=1)
        return True
    except urllib2.URLError as err:
        return False

#Instantiate Logging and GPIO Classes
if internet_on():
    dbConn = Logging.Logging()
    dbConn.logBoot()
    streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)
    streamer.log("Activity","Button - Startup")
    streamer.flush()

# Gag only runs once every 10 minutes. Variable to store last time the gag was run.
lastRun = 0

# Instantiate GPIO
gpio = GPIOLib.GPIOLib("BOARD", "HIGH", [11, 12, 13, 15])
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
LASER = 11
SMOKER = 12
ALARM = 13
BUTTON_LIGHT = 15

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    currentScan = time.time()
    input_state = GPIO.input(16)

    if input_state == False:
        # Turn Alarm On
        gpio.off([ALARM])
        print ("Alarm On")

        # Turn Fogger on. On in this case is turning the GPIO on (off) and off (on) a second cycle will turn it back off
        gpio.off([SMOKER])
        time.sleep(.1)
        gpio.on([SMOKER])
        print ("Fogger On")

        time.sleep(3)

        # Turn Fogger off. On in this case is turning the GPIO on (off) and off (on) a second cycle will turn it back off
        gpio.off([SMOKER])
        time.sleep(.1)
        gpio.on([SMOKER])
        print ("Fogger Off")

        # Flicker lasers on, then leave on
        for x in range (0,5):
            gpio.off([LASER])
            time.sleep(.5)
            gpio.on([LASER])
            time.sleep(.5)
        gpio.off([LASER])
        print ("Laser On")

        time.sleep(5)

        # Turn off Lasers, Alarm
        gpio.on([LASER, ALARM])
