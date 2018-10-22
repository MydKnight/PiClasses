import sys

sys.path.insert(0, '/home/pi/Python')
import GPIOLib, time, sys, os, Logger, logging
from termios import tcflush, TCIOFLUSH

# Pin 11 (Board) is used to trigger projector, 12 is blacklight, 13 is air pump.
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [11, 12, 13])

# Add Logging Code
script = os.path.basename(__file__)
stdout_logger = logging.getLogger(script + '_Out')
sl = Logger.StreamToLogger(stdout_logger, logging.INFO)
# sys.stdout = sl #For Headless Operations

stderr_logger = logging.getLogger(script + '_Err')
sl = Logger.StreamToLogger(stderr_logger, logging.ERROR)
# sys.stderr = sl

# Log Bootup
stdout_logger.info("Bootup")

# Listen for Scan
while True:  # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else:
        stdout_logger.info("Activation||" + n)

        # Pump on
        gpio.on([13])
        time.sleep(1.5)
        # Light and Projector on
        gpio.on([11, 12])
        time.sleep(10)
        # All off
        gpio.off([11, 12, 13])
        time.sleep(1)

        # flush keyboard buffer
        sys.stdout.flush();
        tcflush(sys.stdin, TCIOFLUSH)
