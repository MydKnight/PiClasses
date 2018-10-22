import sys
sys.path.insert(0, '/home/pi/Python')
import GPIOLib, time, sys, os, Logger, logging
from termios import tcflush, TCIOFLUSH

# Pin 11 (Board) is used to trigger the fan.
gpio = GPIOLib.GPIOLib("BOARD", "LOW", [11])

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

def FlutterFan(seconds):
    '''
    Simulate a PWM by pulsing the GPIO pin on and off for the number of seconds passed in
    @param seconds: Number of seconds to pulse
    @return: void
    '''
    for s in range(seconds):
        for i in range(2):
            gpio.on([11])
            time.sleep(.05)
            gpio.off([11])
            time.sleep(.5)

# Listen for Scan
while True:  # Runs until break is encountered. We want to set it to break on a particular ID.
    n = raw_input("Scanned ID: ")
    currentScan = time.time()
    if n == "STOP":
        break  # stops the loop
    else:
        stdout_logger.info("Activation||" + n)
        # Trigger Sound Play
        music = os.popen('mpg321 /home/pi/Python/2018/Assets/wind.mp3')

        # Trigger Fan Blow
        FlutterFan(4)

        time.sleep(15)

        # flush keyboard buffer
        try:
            sys.stdout.flush();
            tcflush(sys.stdin, TCIOFLUSH)
        except AttributeError as e:
            stderr_logger.log(logging.ERROR, e)
