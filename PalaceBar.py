#!/usr/bin/python
__author__ = 'madsens'
#Runs the Palace Bar Plants. When Triggered:
# -- If Human: Sounds of sdreaming and running. Someone shouts "Oh No! It Got Joey! Plants move.
# -- If Alien: Audrey Sings "Suppertime"

from ISStreamer.Streamer import Streamer
import time, sys, urllib2, random, logging, argparse,logging.handlers, os, socket
import StepperController as SC
import Logging
from termios import tcflush, TCIOFLUSH

# --------- User Settings ---------
# Initial State settings
BUCKET_NAME = ":computer: Processes"
BUCKET_KEY = "5S3HHKBXM9Y8"
ACCESS_KEY = "ibegrAmoZM9X8QQQY3j4BDA0FdZXGSqe"
PROCESS_NAME = "PalaceBar"
# Set the time between checks
MINUTES_BETWEEN_READS = 15
# ---------------------------------

# Deafults
LOG_FILENAME = "/home/pi/Python/magiccastle.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="Template Program")
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

# Tentacles
tencacle1 = []
tencacle2 = []
tencacle3 = []
tencacle4 = []

# Vines
vine1 = SC.MotorControl(motorid="BD17") # Not working
vine2 = SC.MotorControl(motorid="BD6")
vine3 = SC.MotorControl(motorid="BD10") # Not working
vine4 = SC.MotorControl(motorid="BD18")

# Set up Motors for Tentacles
motor3 = SC.MotorControl(motorid="BD3")
motor4 = SC.MotorControl(motorid="BD4")
motor5 = SC.MotorControl(motorid="BD5")
motor7 = SC.MotorControl(motorid="BD7")
motor8 = SC.MotorControl(motorid="BD8")
motor9 = SC.MotorControl(motorid="BD9")
motor11 = SC.MotorControl(motorid="BD11")
motor12 = SC.MotorControl(motorid="BD12")
motor14 = SC.MotorControl(motorid="BD14")
motor15 = SC.MotorControl(motorid="BD15")

# Assign Motors to Tentacles
tencacle1.append(motor3)
tencacle1.append(motor4)
tencacle1.append(motor5)
tencacle2.append(motor7)
tencacle2.append(motor8)
tencacle2.append(motor9)
tencacle3.append(motor11)
tencacle3.append(motor12)
tencacle4.append(motor14)
tencacle4.append(motor15)

# Tentacle List
tentacles = []
tentacles.append(tencacle1)
tentacles.append(tencacle2)
tentacles.append(tencacle3)
tentacles.append(tencacle4)

# Wriggling Vines
vines = []
# vines.append(vine1)
vines.append(vine2)
vines.append(vine3)
vines.append(vine4)

# Helper Library to determine if we have internet before logging things.
def internet_on():
    try:
        urllib2.urlopen('http://www.cnn.com', timeout=1)
        return True
    except urllib2.URLError as err:
        return False
    except socket.timeout, e:
        return False
# Moves a Random tentacle on a random axis.
def Movement():
    for tentacle in tentacles:
        print "Moving Tentacle"
        motor = random.choice(tentacle)
        motor.moveRelative(-1600)
        time.sleep(3)
        motor.moveRelative(1600)
        time.sleep(3)

def vineRotate():
    for x in range(0,3):
        for vine in vines:
            vine.moveRelative(200)
        time.sleep(2)



# Instantiate Logging and GPIO Classes
if internet_on():
    dbConn = Logging.Logging()
    dbConn.logBoot()
    streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)
    streamer.log("Activity","Palace Bar - Startup")
    streamer.flush()

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")

    if n == "STOP":
        if internet_on():
            streamer.log("Activity", "Palace Bar - Stop")
            streamer.flush()
        break  # stops the loop
    else:
        # Default "Name"
        name = "Unknown User"
        if internet_on():
            streamer.log("ID Usage", n)
            streamer.log("Activity", "Palace Bar - Scan")
            streamer.flush()
            dbConn.logAccess(n)

        time.sleep(2)

        # Raw Input Gives us a String. We need it as an Int
        try:
            n = int(n)
        except:  # Default to 1
            n = 1

        if n % 3 == 0: #Alien
            print "Alien"
            # Play Audio
            os.system('mpg321 /home/pi/Python/Assets/AlienTriffid.mp3 -q &')

            # Move Either Vine or Tentacle
            action = random.randint(1,2)
            if action == 1:
                Movement()
            else:
                vineRotate()
            time.sleep(5)

        else: #Human
            print "Human"
            os.system('mpg321 /home/pi/Python/Assets/HumanTriffid.mp3 -q &')

            # Move Either Vine or Tentacle
            action = random.randint(1, 2)
            if action == 1:
                Movement()
            else:
                vineRotate()
            time.sleep(5)

        # Flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)