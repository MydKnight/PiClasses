#!/usr/bin/python
from ISStreamer.Streamer import Streamer
import urllib2, sys, datetime, logging, argparse,logging.handlers
sys.path.append("/home/pi/Python")
import PMP
import Logging
from RPi import GPIO
from time import sleep

# --------- User Settings:InitialState ---------
# Initial State settings
BUCKET_NAME = ":computer: Processes"
BUCKET_KEY = "5S3HHKBXM9Y8"
ACCESS_KEY = "ibegrAmoZM9X8QQQY3j4BDA0FdZXGSqe"
PROCESS_NAME = "LauraRadio"
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

# Define our click and direction vars
clk = 17
dt = 18

# Set up the GPIO pins that the click and direction communicate over
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Set up media player
client = PMP.mpc(volume=50, playlist=['InvasionCellar1.m4a', 'EmergencySoundEffect.m4a', 'InvasionCellar2.m4a', 'InvasionStatic.m4a', 'InvasionCellar3.m4a', 'MoreStaticAndRadioDials.m4a', 'InvasionCellar4.m4a', 'EmergencySoundEffect.m4a', 'InvasionCellar5.m4a'])

# Initialize Tuner Variables
counter = 0
clkLastState = GPIO.input(clk)

# Helper Library to determine if we have internet before logging things.
def internet_on():
    try:
        urllib2.urlopen('http://www.cnn.com', timeout=1)
        return True
    except urllib2.URLError as err:
        return False

# Now that we've initialized, let both the DB and InitialState know we're alive
streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)
if internet_on():
    streamer.log("Activity","Laura's Radio - Startup")
    streamer.flush()
    dbConn = Logging.Logging()
    dbConn.logBoot()

hbValue = 0

# Begin listening for turning dial.
try:
    while True:
        if internet_on():
            # Heartbeat (no dials have been turned...just let us know you're still alive)
            now = datetime.datetime.now()
            if now.minute % 5 == 0 and now.minute != hbValue:
                print "heartbeat"
                hbValue = now.minute
                dbConn.logHeartbeat()

        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        if clkState != clkLastState:
            if dtState != clkState:
                counter += 1
                # If our counter is divisible by 10 and we're turning clockwise, play the next track
                if counter % 10 == 0:
                    client.next()
            else:
                counter -= 1
                # If our counter is divisible by 10 and we're turning counterclockwise, play the previous track
                if counter % 10 == 0:
                    client.prev()
            print counter
        clkLastState = clkState
        # print client.getSong()
        sleep(.01)
finally:
    GPIO.cleanup()

