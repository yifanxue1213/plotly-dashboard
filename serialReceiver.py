import serial
import datetime
import time
import pymysql.cursors
from enum import Enum

numOfTempSensors = 3
tableName = 'test_table'
DBPort = 8889


if __name__ == '__main__':
    # serialPort = '/dev/ttyUSB0'
    serialPort = '/dev/tty.usbserial-1410'
    # connect to DB
    connection = pymysql.connect(host='localhost',
                                 port= DBPort,
                                 user='uscsolar',
                                 password='solarcar',
                                 db='uscsolarcar',
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

        dataArray = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] # t1 t2 t3 voltage power speed

        # loop for read serial data and store into MySQL
        while True:
            try:
                i = 0
                while i < 6:
                    # assume reading from line is byte for string, this string is the string form of double value
                    line = ser.readline().decode("utf-8")  # decode byte array into string  # readline(timeout=1)
                    print(line)
                    if line.rstrip() == "":
                        i = 0
                        continue
                    curVal = float(line)
                    # curVal = int.from_bytes(line, byteorder='big', signed=False) # parse byte int into int
                    dataArray[i] = curVal
                    i += 1

                with connection.cursor() as cursor:
                    sql = "INSERT INTO `" + tableName + \
                          "` (`t1`, `t2`, `t3`, `voltage`, `power`, `speed`) VALUES (%s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql,
                                   (dataArray[0], dataArray[1], dataArray[2], dataArray[3], dataArray[4], dataArray[5]))

                connection.commit()

                # debug print
                with connection.cursor() as cursor:
                    # Read a single record
                    sql = "SELECT `*` FROM `" + tableName + "` ORDER BY `id` DESC LIMIT 1"
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    print(result)

                # print(datetime.datetime.now() + ": " + line)
            except KeyboardInterrupt:
                ser.close()
                break

    connection.close()