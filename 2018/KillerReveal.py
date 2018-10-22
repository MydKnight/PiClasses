import sys

sys.path.insert(0, '/home/pi/Python')
import time, sys, os, Logger, logging, Movies, RPi.GPIO as GPIO, GPIOLib

# Add Logging Code
script = os.path.basename(__file__)
stdout_logger = logging.getLogger(script + '_Out')
sl = Logger.StreamToLogger(stdout_logger, logging.INFO)
sys.stdout = sl  # For Headless Operations

stderr_logger = logging.getLogger(script + '_Err')
sl = Logger.StreamToLogger(stderr_logger, logging.ERROR)
sys.stderr = sl

# Log Bootup
stdout_logger.info("Bootup")

# Pin 18 (Board) - Blue LED
# Pin 26 (Board) - Red LED
# Pin 40 (Board) - Green LED
GPIO.setmode(GPIO.BOARD)
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [18, 26, 40])

# GPIO class doesnt exactly work for GPIO inputs. Setting these up manually
# Pin 16 - Blue Button
# Pin 24 - Red Button
# Pin 38 - Green Button
GPIO.setup(16, GPIO.IN)
GPIO.setup(24, GPIO.IN)
GPIO.setup(38, GPIO.IN)

# Start Movie Loop
Movies.StartLoop('/home/pi/Python/2018/Assets')

# Listen for Scan
while True:  # Runs until break is encountered. We want to set it to break on a particular ID.
    if GPIO.input(16) or GPIO.input(24) or GPIO.input(38):
        currentScan = time.time()

        if GPIO.input(16):
            stdout_logger.info("Activation||" + str(1))

            # Play Blue Video
            Movies.PlayMovie('vid2.mp4')
            for x in range(20):
                gpio.on([18])
                time.sleep(.5)
                gpio.off([18])
                time.sleep(.5)

        elif GPIO.input(24):
            stdout_logger.info("Activation||" + str(2))

            # Play Video 2
            Movies.PlayMovie('vid1.mp4')
            for x in range(20):
                gpio.on([26])
                time.sleep(.5)
                gpio.off([26])
                time.sleep(.5)

        elif GPIO.input(38):
            stdout_logger.info("Activation||" + str(3))

            # Play Video 3
            Movies.PlayMovie('vid3.mp4')
            for x in range(20):
                gpio.on([40])
                time.sleep(.5)
                gpio.off([40])
                time.sleep(.5)

        else:
            stdout_logger.info("Activation||" + str(0))

        Movies.PlayLoop()
