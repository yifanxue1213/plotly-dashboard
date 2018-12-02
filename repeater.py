#!/usr/bin/env python

import time
import serial

DEBUG = 2

if __name__ == '__main__':


    bmsArduino = serial.Serial(port='/dev/ttyUSB1', baudrate=115200)

    canArduino = serial.Serial(port='/dev/ttyUSB2', baudrate=115200)

    xBeeOut = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)

    bmsData = bmsArduino.readline()
    canData = canArduino.readline()

    while bmsData is not None or canData is not None:
        if DEBUG > 0:
            print("DEBUG: BMS: " + bmsData, end="")
            print("DEBUG: CAN: " + canData, end="")
        bmsDataToWrite = str(bmsData)
        canDataToWrite = str(canData)
        xBeeOut.write(bmsData)
        xBeeOut.write(canData)
        bmsArduino = bmsArduino.readline()
        canArduino = canArduino.readline()
