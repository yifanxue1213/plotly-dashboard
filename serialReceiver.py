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
                if DEBUG > 1:
                    print("DEBUG: " + line)
                if line.rstrip() == "":
                    continue
                tokens = line.split(" ")
                if tokens[0] == "voltage":
                    # generate SQL query
                    sql = "INSERT INTO `" + voltageTableName + "` ("
                    sqlValues = ""
                    # parse value
                    for i in range(0, numOfVoltageSensors):
                        print(tokens[i+1])
                        voltageArray[i] = float(tokens[i + 1])
                        sql = sql + "`voltage" + str(i + 1) + "`, "
                        sqlValues = sqlValues + "%s, "
                    sql = sql[:-2] + ") VALUES (" + sqlValues[:-2] + ")"
                    if DEBUG > 1:
                        print("DEBUG: " + sql)
                    # execute query
                    with connection.cursor() as cursor:
                        cursor.execute(sql, voltageArray)
                elif tokens[0] == "temperature":
                    sql = "INSERT INTO `" + tempratureTableName + "` ("
                    sqlValues = ""
                    for i in range(0, numOfTempSensors):
                        tempratureArray[i] = float(tokens[i + 1])
                        sql = sql + "`temp" + str(i + 1) + "`, "
                        sqlValues = sqlValues + "%s, "
                    sql = sql[:-2] + ") VALUES (" + sqlValues[:-2] + ")"
                    if DEBUG > 1:
                        print("DEBUG: " + sql)
                    with connection.cursor() as cursor:
                        cursor.execute(sql, tempratureArray)
                elif tokens[0] == "motor":
                    motorOpCurrent = float(tokens[1])
                    rpm = int(tokens[2])
                    sql = "INSERT INTO `" + motorTableName + \
                          "` (`current`, `rpm`) VALUES (%s, %s)"
                    if DEBUG > 1:
                        print("DEBUG: " + sql)
                    with connection.cursor() as cursor:
                        cursor.execute(sql, (motorOpCurrent, rpm))
                elif tokens[0] == "condition":
                    opCurrent = float(tokens[2])
                    outputVoltage = float(tokens[3])
                    sql = "INSERT INTO `" + workConditionTableName + \
                          "` (`current`, ``outputVoltage`) VALUES (%s, %s)"
                    if DEBUG > 1:
                        print("DEBUG: " + sql)
                    with connection.cursor() as cursor:
                        cursor.execute(sql, (opCurrent, outputVoltage))

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