#!/usr/bin/python
__author__ = 'madsens'
# Hall of Fame gag. Will run laser show, 10 DJ lights and play sound.

import urllib2
import time, sys, os, logging, argparse,logging.handlers, socket
sys.path.append("/home/pi/PiClasses")
import Logging, GPIOLib
from ISStreamer.Streamer import Streamer
from termios import tcflush, TCIOFLUSH
from DmxPy import DmxPy
from random import randint

# --------- User Settings ---------
# Initial State settings
BUCKET_NAME = ":computer: Processes"
BUCKET_KEY = "5S3HHKBXM9Y8"
ACCESS_KEY = "ibegrAmoZM9X8QQQY3j4BDA0FdZXGSqe"
PROCESS_NAME = "HallCore"
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

#Instantiate Logging, GPIO and DMX Classes
dbConn = Logging.Logging()
dbConn.logBoot()
streamer = Streamer(bucket_name=BUCKET_NAME, bucket_key=BUCKET_KEY, access_key=ACCESS_KEY)

def internet_on():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=1)
        return True
    except urllib2.URLError as err:
        return False
    except socket.timeout, e:
        return False

if (internet_on()):
    streamer.log("Activity","HallCore - Startup")
    streamer.flush()
dmx = DmxPy('/dev/ttyUSB0')
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [13])

def standby():
    global dmx
    # Set Baseline
    for x in [1, 2, 4, 5, 6, 7, 8, 11, 12, 14, 15, 16, 17, 18, 21, 22, 24, 25, 26, 27, 28]:
        dmx.setChannel(x, 0)
    for x in [7, 17, 27]:
        dmx.setChannel(x, 255)
    dmx.render()

    # Fade up to blue from nothing
    for x in range(0, 255):
        for y in [3, 13, 23]:
            dmx.setChannel(y, x)
            dmx.render()
            time.sleep(.01)

    # Play Looping Audio
    os.system('mpg321 /home/pi/Python/Assets/loop.mp3 -l 0 -q &')

    # Begin to pulse
    dmx.setChannel(8, 157)
    dmx.setChannel(18, 158)
    dmx.setChannel(28, 159)
    dmx.render()

def meltdown():
    global dmx

    red = [1, 11, 21]
    green = [2, 12, 22]
    blue = [3, 13, 23]
    effect = [8, 18, 28]
    dimmer = [7, 17, 27]
    dimToggle = 0
    dimValue = 255

    for x in effect:
        dmx.setChannel(x, 224)
        dmx.render()

    # Increasing pulse, increasing fade from blue to yellow to red.
    # Blue to Yellow
    print "Blue to Yellow"
    for x in range(0,255, 2):
        for b in blue:
            dmx.setChannel(b, 255-(x))
        for r in red:
            dmx.setChannel(r, (x))
        for g in green:
            dmx.setChannel(g, (x))
        dmx.render();

        # Run four cycles of fade up/down
        for f in range (0,4):
            for d in dimmer:
                dmx.setChannel(d, dimValue)
                dmx.render()
                time.sleep(.005)

            # Increment or decrement the counter based on the toggle.
            if dimToggle == 0:
                # We're fading down because toggle is at 0
                dimValue -= 10
                # Check if we hit the floor of 0. If so, Flip the toggle for the next loop
                if dimValue < 1:
                    dimToggle = 1
            else:
                # We're fading up because toggle is at 1
                dimValue += 10
                if dimValue > 254:
                    dimToggle = 0

    # Yellow to Orange
    print "Yellow to Orange"
    for x in range(255, 165, -1):
        for g in green:
            dmx.setChannel(g, x)
        dmx.render();

        # Run four cycles of fade up/down
        for f in range(0, 4):
            for d in dimmer:
                dmx.setChannel(d, dimValue)
                dmx.render()
                time.sleep(.01)

            # Increment or decrement the counter based on the toggle.
            if dimToggle == 0:
                # We're fading down because toggle is at 0
                dimValue -= 20
                # Check if we hit the floor of 0. If so, Flip the toggle for the next loop
                if dimValue < 1:
                    dimToggle = 1
            else:
                # We're fading up because toggle is at 1
                dimValue += 20
                if dimValue > 254:
                    dimToggle = 0

    # Orange to Red
    print "Orange to Red"
    gpio.on([13])
    for x in range(165, 0, -2):
        for g in green:
            dmx.setChannel(g, x)
        dmx.render();

        # Run four cycles of fade up/down
        for f in range(0, 4):
            for d in dimmer:
                dmx.setChannel(d, dimValue)
                dmx.render()
                time.sleep(.01)

            # Increment or decrement the counter based on the toggle.
            if dimToggle == 0:
                # We're fading down because toggle is at 0
                dimValue -= 30
                # Check if we hit the floor of 0. If so, Flip the toggle for the next loop
                if dimValue < 1:
                    dimToggle = 1
            else:
                # We're fading up because toggle is at 1
                dimValue += 30
                if dimValue > 254:
                    dimToggle = 0

    # Hold Red
    print "Hold Red."
    for f in range(0, 400):
        for d in dimmer:
            dmx.setChannel(d, dimValue)
            dmx.render()
            time.sleep(.01)

        # Increment or decrement the counter based on the toggle.
        if dimToggle == 0:
            # We're fading down because toggle is at 0
            dimValue -= 40+f
            # Check if we hit the floor of 0. If so, Flip the toggle for the next loop
            if dimValue < 1:
                dimToggle = 1
        else:
            # We're fading up because toggle is at 1
            dimValue += 40+f
            if dimValue > 254:
                dimToggle = 0
    for d in dimmer:
        dmx.setChannel(d, 255)
        dmx.render()
        time.sleep(.5)

    # Blackout
    for x in range(255, 0, -5):
        for d in dimmer:
            dmx.setChannel (d, x)
            dmx.render()
            time.sleep(.05)
    print "Blackout"

    gpio.off([13])
    print "Reboot"

while True:    # Runs until break is encountered. We want to set it to break on a particular ID.
    standby()
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        if (internet_on):
            streamer.log("Activity", "HallCore - Stop")
            streamer.flush()
        break  # stops the loop
    else :
        dbConn.logAccess(n)
        if (internet_on()):
            streamer.log("ID Usage", n)
            streamer.log("Activity", "HallCore - Activation")
            streamer.flush()

        # Kill Looping Audio
        os.system('sudo pkill mpg321')

        #MIB
        if n == "0009183669":
            os.system('mpg321 /home/pi/Python/Assets/mib.mp3 -q &')
        # Play Meltdown Audio
        else:
            os.system('mpg321 /home/pi/Python/Assets/trigger.mp3 -q &')
        meltdown()

        #flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)