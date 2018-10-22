import sys

sys.path.insert(0, '/home/pi/Python')
import time, sys, os, Logger, logging, Movies
from termios import tcflush, TCIOFLUSH

# Add Logging Code
script = os.path.basename(__file__)
stdout_logger = logging.getLogger(script + '_Out')
sl = Logger.StreamToLogger(stdout_logger, logging.INFO)
# sys.stdout = sl #For Headless Operations

stderr_logger = logging.getLogger(script + '_Err')
sl = Logger.StreamToLogger(stderr_logger, logging.ERROR)
sys.stderr = sl

# Log Bootup
stdout_logger.info("Bootup")

# Start Movie Loop
Movies.StartLoop('/home/pi/Python/2018/Assets')

# Listen for Scan
while True:  # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        Movies.StopLoop()
        break  # stops the loop
    else:
        stdout_logger.info("Activation||" + n)

        # Play Movie
        Movies.PlayMovie()
        time.sleep(10)

        Movies.PlayLoop()

        # flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)
