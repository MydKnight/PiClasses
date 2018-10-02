#!/usr/bin/env python
__author__ = 'madsens'
#Runs the Alien gag. When Triggered:
# -- If Human: Play Robot Voice: Please Hold While Sxanning. Activate Green Lights GPIO 11. Play Human DNA Confirmed. Proceed.
# -- If Alien: Play Robot Voice: Please Hold While Scanning. Activate Red Light. Play Siren Effect. Warning, Alien DNA Detected. Please Proceed in for further Evaluation.

from ISStreamer.Streamer import Streamer
import time, sys, urllib2, speake, os, logging, logging.handlers, argparse, talkey, socket
sys.path.append("/home/pi/PiClasses")
import Logging
import GPIOLib
from termios import tcflush, TCIOFLUSH

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

i = 0

# --------- User Settings ---------
# Initial State settings
BUCKET_NAME = ":computer: Processes"
BUCKET_KEY = "5S3HHKBXM9Y8"
ACCESS_KEY = "ibegrAmoZM9X8QQQY3j4BDA0FdZXGSqe"
PROCESS_NAME = "AlienDetector"
# Set the time between checks
MINUTES_BETWEEN_READS = 15
# ---------------------------------

# Helper Library to determine if we have internet before logging things.
def internet_on():
    try:
        urllib2.urlopen('http://www.cnn.com', timeout=1)
        return True
    except urllib2.URLError as err:
        return False
    except socket.timeout, e:
        return False

# Instantiate Logging and GPIO Classes
if internet_on():
    dbConn = Logging.Logging()
    dbConn.logBoot()
    streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)
    streamer.log("Activity","Alien Detector - Startup")
    streamer.flush()

# Initilize our Red/Green GPIO Pins
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [11]) # Red Strobe
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [12]) # Green Strobe
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [13]) # Flashing Lights and Rotating Hoop
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [15]) # Extra Channel

# Initialize talkey
tts = talkey.Talkey(
    engine_preference=['espeak']
)

# tts.say("Voila! In view, a humble vaudevillian veteran cast vicariously as both victim and villain by the vicissitudes of Fate. This visage, no mere veneer of vanity, is a vestige of the vox populi, now vacant, vanished. However, this valourous visitation of a bygone vexation stands vivified and has vowed to vanquish these venal and virulent vermin vanguarding vice and vouchsafing the violently vicious and voracious violation of volition! The only verdict is vengeance; a vendetta held as a votive, not in vain, for the value and veracity of such shall one day vindicate the vigilant and the virtuous. Verily, this vichyssoise of verbiage veers most verbose, so let me simply add that it's my very good honour to meet you and you may call me V.")

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")

    if n == "STOP":
        if internet_on():
            streamer.log("Activity", "Alien Detector - Stop")
            streamer.flush()
        break  # stops the loop
    else:
        #engine = speake.Speake()  # Initialize the speake engine
        #engine.set('voice', 'en')
        #engine.set('speed', '130')
        #engine.set('pitch', '150')

        # Default "Name"
        name = "Unknown User"

        # Inform the user they are being scanned.
        tts.say("Attention! User scan of: %s Commencing. Please Wait." % name)

        # MIB
        if n == "0009183669":
            os.system('mpg321 /home/pi/Python/Assets/mib.mp3 -q &')
        else:
            os.system('mpg321 /home/pi/Python/Assets/scanner.mp3 -q &')

        # Trigger Flashy lightshow
        gpio.on([13])
        time.sleep(7)
        gpio.off([13])

        # Raw Input Gives us a String. We need it as an Int
        try:
            n = int(n)
        except:  # Default to 1
            n = 1

        if internet_on():
            streamer.log("ID Usage", n)
            streamer.log("Activity", "Alien Detector - Scan")
            streamer.flush()
            dbConn.logAccess(n)
            # Get the User
            name = dbConn.getName(n)

        if n % 3 == 0: #Alien
            print "Alien"

            #Trigger Red Pin
            gpio.on([11])
            tts.say("Warning! Warning! Alien DNA Detected in user: %s. Security forces inbound" % name)
            time.sleep(5)

            #Red GPIO Off
            gpio.off([11])
            time.sleep(1)
        else: #Human
            print "Human"

            # Trigger Green Pin
            gpio.on([12])
            tts.say("Human DNA detected in user: %s. Please proceed." % name)
            time.sleep(3)

            # Spinner GPIO Off
            gpio.off([12])
            time.sleep(1)


        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)