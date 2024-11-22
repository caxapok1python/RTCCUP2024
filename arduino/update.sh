#!/bin/sh

git pull
arduino-cli compile -b arduino:avr:mega && arduino-cli upload -b arduino:avr:mega -p /dev/ttyUSB0 && arduino-cli monitor --timestamp --config baudrate=115200 -b arduino:avr:mega -p /dev/ttyUSB0