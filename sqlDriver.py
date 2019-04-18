import datetime
import time
from enum import Enum

class sqlDriver:
    def __init__(self, numOfTempSensors, numOfVoltageSensors,
                 voltageTableName, tempratureTableName, motorTableName,
                 workConditionTableName,tokens,sql):
        self.sqlValues =""
        self.numOfTempSensors =numOfTempSensors
        self.numOfVoltageSensors = numOfVoltageSensors
        self.voltageTableName = voltageTableName
        self.tempratureTableName = tempratureTableName
        self.motorTableName = motorTableName
        self.workConditionTableName = workConditionTableName
        self.voltageArray = [0.0] * numOfVoltageSensors
        self.tempratureArray = [0.0] * numOfTempSensors
        self.tokens=tokens
        self.sql=sql

    def voltage(self):
        sql = "INSERT INTO `" + self.voltageTableName + "` ("
        # parse value
        for i in range(0, self.numOfVoltageSensors ):
            print(self.tokens[i+1])
            self.voltageArray[i] = float(self.tokens[i + 1])
            self.sql = self.sql + "`voltage" + str(i + 1) + "`, "
            self.sqlValues = self.sqlValues + "%s, "
        self.sql = self.sql[:-2] + ") VALUES (" + self.sqlValues[:-2] + ")"
        if DEBUG > 1:#1
            print("DEBUG: " + self.sql)
        # execute query
        with connection.cursor() as cursor:
                        cursor.execute(self.sql, self.voltageArray)

        def temperature(self):
            sql = "INSERT INTO `" + self.temperatureTableName + "` ("
            # parse value
            for i in range(0, self.numOfTempSensors ):
                print(self.tokens[i+1])
                self.temperatureArray[i] = float(self.tokens[i + 1])
                self.sql = self.sql + "`temp" + str(i + 1) + "`, "
                self.sqlValues = self.sqlValues + "%s, "
            self.sql = self.sql[:-2] + ") VALUES (" + self.sqlValues[:-2] + ")"
            if DEBUG > 1:#1
                print("DEBUG: " + self.sql)
            # execute query
            with connection.cursor() as cursor:
                            cursor.execute(self.sql, self.temperatureArray)

        def motor(self):
            self.motorOpCurrent = float(self.tokens[1])
            rpm = int(self.tokens[2])
            sql = "INSERT INTO `" + self.motorTableName + \
                  "` (`current`, `rpm`) VALUES (%s, %s)"
            if DEBUG > 1:
                print("DEBUG: " + sql)
            with connection.cursor() as cursor:
                        cursor.execute(self.sql, (self.motorOpCurrent, rpm))

        def condition():
            opCurrent = float(tokens[2])
            outputVoltage = float(tokens[3])
            self.sql = "INSERT INTO `" + self.workConditionTableName + \
                  "` (`current`, ``outputVoltage`) VALUES (%s, %s)"
            if DEBUG > 1:
                print("DEBUG: " + self.sql)
            with connection.cursor() as cursor:
                        cursor.execute(self.sql, (opCurrent, outputVoltage))

      