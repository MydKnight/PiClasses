__author__ = 'madsens'
import sys

sys.path.insert(0, '/home/pi/Python')
import RPi.GPIO as GPIO, os, Logger, logging

# Add Logging Code
script = os.path.basename(__file__)
stdout_logger = logging.getLogger(script + '_Out')
sl = Logger.StreamToLogger(stdout_logger, logging.INFO)
# sys.stdout = sl #For Headless Operations

stderr_logger = logging.getLogger(script + '_Err')
sl = Logger.StreamToLogger(stderr_logger, logging.ERROR)


# sys.stderr = sl

class GPIOLib:
    'Common base class for all GPIO Access'
    # <editor-fold desc="Global Variables">

    # </editor-fold>

    def __init__(self, boardType, pinState, pins=[], inout='out'):
        '''
        :param type: GPIO pinout type (BOARD or BCM)
        :param state: Whether the pins are initialized HIGH or LOW
        :param pins: An array of pins to initialize on the GPIO board
        :return:
        '''
        # Attempt to Initialize GPIO
        if (boardType == "BOARD"):
            GPIO.setmode(GPIO.BOARD)
        else:
            GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for pin in pins:
            if inout == "out":
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH) if pinState == "HIGH" else GPIO.setup(pin, GPIO.OUT,
                                                                                                   initial=GPIO.LOW)
            elif inout == "in":
                GPIO.setup(pin, GPIO.IN) if pinState == "HIGH" else GPIO.setup(pin, GPIO.IN)

    def on (self, pinArray):
        '''
        This function is called to trigger the activation of particular pins on the GPIO header
        :param pinArray: An array of pins to act on
        :return:
        '''
        for pin in pinArray:
            GPIO.output(pin, GPIO.HIGH)
            # print "Set " + str(pin) + " to On. \n"


    def off(self, pinArray):
        '''
        This function is called to trigger the deactivation of particular pins on the GPIO header
        :param pinArray: An array of pins to act on
        :return:
        '''
        for pin in pinArray:
            GPIO.output(pin, GPIO.LOW)
            # print "Set " + str(pin) + " to Off. \n"
