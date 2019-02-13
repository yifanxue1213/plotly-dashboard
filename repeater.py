#!/usr/bin/env python

import time
import serial
import struct

DEBUG = 2

if __name__ == '__main__':


    bmsArduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)
    #bmsArduino.write(9)
    #bmsArduino.write(struct.pack('>B', 9))
    # canArduino = serial.Serial(port='/dev/ttyUSB2', baudrate=115200)

    xBeeOut = serial.Serial(port='/dev/ttyUSB1', baudrate=9600)

    bmsData = bmsArduino.readline()
    # canData = canArduino.readline()

    # while bmsData is not None or canData is not None:
    while bmsData is not None:
        print(bmsData.decode("UTF-8"))
        tokens = str(bmsData.decode("UTF-8")).split(" ")
        # print(tokens[0])
        if tokens[0] == "voltage":
            if DEBUG > 0:
                print("DEBUG: BMS: " + bmsData.decode("UTF-8"), end="")
            xBeeOut.write(bmsData)
        elif tokens[0] == "temperature":
            if DEBUG > 0:
                print("DEBUG: BMS: " + bmsData.decode("UTF-8"), end="")
            xBeeOut.write(bmsData)

        # bmsDataToWrite = str(bmsData)
        # canDataToWrite = str(canData)
        # xBeeOut.write(bmsData)
        # xBeeOut.write(canData)
        bmsData = bmsArduino.readline()
        # canArduino = canArduino.readline()
