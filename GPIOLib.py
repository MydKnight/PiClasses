__author__ = 'madsens'
import time
import RPi.GPIO as GPIO

class GPIOLib:
    'Common base class for all GPIO Access'
    # <editor-fold desc="Global Variables">

    # </editor-fold>

    def __init__(self, boardType, pinState, pins = []):
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

        for pin in pins:
            GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH) if pinState == "HIGH" else GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    def on (self, pinArray):
        '''
        This function is called to trigger the activation of particular pins on the GPIO header
        :param pinArray: An array of pins to act on
        :return:
        '''
        for pin in pinArray:
            GPIO.output(pin, GPIO.HIGH)
            print "Set " + str(pin) + " to On. \n"


    def off(self, pinArray):
        '''
        This function is called to trigger the deactivation of particular pins on the GPIO header
        :param pinArray: An array of pins to act on
        :return:
        '''
        for pin in pinArray:
            GPIO.output(pin, GPIO.LOW)
            print "Set " + str(pin) + " to Off. \n"
