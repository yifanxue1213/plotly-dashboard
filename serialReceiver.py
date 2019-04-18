import serial
import datetime
import time
import pymysql.cursors
from enum import Enum

numOfTempSensors = 24
numOfVoltageSensors = 28
voltageTableName = 'voltage'
tempratureTableName = 'temporature'
motorTableName = 'motor'
workConditionTableName = 'workCondition'
DBHost = 'localhost'
DBPort = 8889
DBName = 'uscsolarcar'
DBUser = 'uscsolar'
DBPasswd = 'solarcar'

DEBUG = 1 # 2 for verbose, 1 for simple debug put, 0 for non debug info


# still need to change to update database in a less frequency
if __name__ == '__main__':
    # use `ls /dev/tty.usb*` to find the proper port for current experiment
    serialPort = '/dev/tty.usbserial-1460'
    # connect to DB
    connection = pymysql.connect(host=DBHost,
                                 port= DBPort,
                                 user=DBUser,
                                 password=DBPasswd,
                                 db=DBName,
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor)
    with serial.Serial(port=serialPort,
                       baudrate = 9600,
                       parity=serial.PARITY_NONE,
                       stopbits=serial.STOPBITS_ONE,
                       bytesize=serial.EIGHTBITS,
                       timeout=1) as ser:
        ser.flushInput()
        print("Serial " + ser.name + " set up with port " + serialPort + "!")

        voltageArray = [0.0] * numOfVoltageSensors
        tempratureArray = [0.0] * numOfTempSensors
        sql = ""

        # loop for read serial data and store into MySQL
        while True:
            try:
                line = ser.readline().decode("utf-8")  # decode byte array into string  # readline(timeout=1)
                if DEBUG > 1:  #1
                    print("DEBUG: " + line)
                if line.rstrip() == "":
                    continue
                tokens = line.split(" ")
                table=sqlDriver(numOfTempSensors, numOfVoltageSensors,
                                 voltageTableName, tempratureTableName, motorTableName,
                                    workConditionTableName,tokens,sql)
                if tokens[0] == "voltage":
                    # generate SQL query
                    table.voltage()
                elif tokens[0] == "temperature":
                    table.temperature()
                elif tokens[0] == "motor":
                    table.motor()
                elif tokens[0] == "condition":
                    table.condition()

                connection.commit()

                # debug print
                if DEBUG > 1:
                    with connection.cursor() as cursor:
                        # Read a single record
                        sql = "SELECT `*` FROM `" + voltageTableName + "` ORDER BY `id` DESC LIMIT 1"
                        cursor.execute(sql)
                        result = cursor.fetchone()
                        print("DEBUG: \n" + result)
                        sql = "SELECT `*` FROM `" + tempratureTableName + "` ORDER BY `id` DESC LIMIT 1"
                        cursor.execute(sql)
                        result = cursor.fetchone()
                        print("DEBUG: \n" + result)
                        sql = "SELECT `*` FROM `" + motorTableName + "` ORDER BY `id` DESC LIMIT 1"
                        cursor.execute(sql)
                        result = cursor.fetchone()
                        print("DEBUG: \n" + result)
                        sql = "SELECT `*` FROM `" + workConditionTableName + "` ORDER BY `id` DESC LIMIT 1"
                        cursor.execute(sql)
                        result = cursor.fetchone()
                        print("DEBUG: \n" + result)
            except KeyboardInterrupt:
                ser.close()
                break

    connection.close()