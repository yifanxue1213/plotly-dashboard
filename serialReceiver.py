import serial
import datetime
import time

numOfTempSensors = 3

if __name__ == '__main__':
    serialPort = '/dev/ttyUSB0'
    with serial.Serial(port=serialPort,
                       baudrate = 9600,
                       parity=serial.PARITY_NONE,
                       stopbits=serial.STOPBITS_ONE,
                       bytesize=serial.EIGHTBITS,
                       timeout=1) as ser:
        ser.flush()
        print("Serial " + ser.name + " set up with port " + serialPort + "!")
        line = ser.readline(timeout=1)
        curVal = int.from_bytes(line, byteorder='big', signed=False)

        print(datetime.datetime.now() + ": " + line)
        ser.close()
