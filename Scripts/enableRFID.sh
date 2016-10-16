#!/bin/bash
# Disables the USB port the RFID reader is on

echo '1-1.4' |sudo tee /sys/bus/usb/drivers/usb/bind