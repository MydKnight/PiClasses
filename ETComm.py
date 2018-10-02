#!/usr/bin/python
__author__ = 'madsens'
# Runs the ET Communicator Gag. When Triggered:
# If Human: Play ET Separating and Dying Clip. Trigger Communication device
# If Alien: Play ET Phone Home Clip. Trigger Communication Device

from ISStreamer.Streamer import Streamer
import time, sys, os, urllib2,logging, argparse,logging.handlers, socket
sys.path.append("/home/pi/PiClasses")
import Logging
import GPIOLib
from termios import tcflush, TCIOFLUSH

# --------- User Settings ---------
# Initial State settings
BUCKET_NAME = ":computer: Processes"
BUCKET_KEY = "5S3HHKBXM9Y8"
ACCESS_KEY = "ibegrAmoZM9X8QQQY3j4BDA0FdZXGSqe"
PROCESS_NAME = "ETComm"
# Set the time between checks
MINUTES_BETWEEN_READS = 15

# Local Log Defaults
LOG_FILENAME = "/home/pi/Python/magiccastle.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"
# Define and parse command line arguments for local log
parser = argparse.ArgumentParser(description="My simple Python service")
parser.add_argument("-l", "--log", help="file to write log to (default " + LOG_FILENAME + "')")
# ---------------------------------

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

# Helper Library to determine if we have internet before logging things.
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
    streamer.log("Activity","ET Communicator - Startup")
    streamer.flush()
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [11])

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        if internet_on():
            streamer.log("Activity", "ET Communicator - Stop")
            streamer.flush()
        break  # stops the loop
    else:
        if internet_on():
            streamer.log("ID Usage", n)
            streamer.log("Activity", "Communicator - Scan")
            streamer.flush()
            dbConn.logAccess(n)

        try:
            n = int(n)
        except:  # Default to 1
            n = 1

        if n % 3 == 0: #Alien
            print "Alien"
            # Play Alien Audio
            os.system('mpg321 /home/pi/Python/Assets/ETAlien.mp3 -g 10 -q &')

            # ET  Rig Pulse
            for x in range(0,40):
                gpio.on([11])
                time.sleep(.1)
                gpio.off([11])
                time.sleep(.5)

        else: #Human
            print "Human"
            # Rachael
            print "Number: " + str(n)
            if str(n) == "270900574":
                os.system('mpg321 /home/pi/Python/Assets/shark.mp3 -q &')
            # Play Human Audio
            else:
                os.system('mpg321 /home/pi/Python/Assets/ETHuman.mp3 -g 100 -q &')

            # ET  Rig Pulse
            for x in range(0, 30):
                gpio.on([11])
                time.sleep(.1)
                gpio.off([11])
                time.sleep(.5)

        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)