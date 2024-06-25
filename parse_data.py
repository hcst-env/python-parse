import json
import numpy as np


def parse(index, sdate, edate, datapath):

    out = {}
    sensors = askSensor(getSensors(index, sdate, edate))
    days = index.keys()
    print(sensors)
    count = 0
    for day in days:

        if (int(day) >= sdate and int(day) <= edate) or (sdate == 0 and edate == 0):
            for sensor in index[day]:
                if sensor not in sensors:
                    continue
                filepath = datapath + day + "/" + sensor + ".json"
                with open(filepath, "r") as f:
                    data = json.loads(f.read())
                    if sensor not in out:
                        out[sensor] = {}
                    flattened_data = []
                    sensorData = {}
                    # Flatten the data
                    for reading in data.values():
                        flattened_data.append(reading)

                    values = flattened_data[0].keys()
                    print(values)
                    for col in values:
                        if col not in out[sensor]:
                            out[sensor][col] = []
                    for row in flattened_data:
                        if (
                            (sdate == 0 and edate == 0)
                            or int(row["timestamp"]) >= sdate
                            and int(row["timestamp"]) <= edate
                        ):
                            for col in values:
                                out[sensor][col].append(row[col])

                        else:
                            pass

    # Get the data for each sensor

    # for sensor in sensors:
    #     if sensor == "Sensors":
    #         continue
    #     cont = input("Would you like to include sensor " + sensor + "? (y/n)")
    #     if cont == "n":
    #         continue

    #     readings = data[sensor]["readings"]
    #     flattened_data = []
    #     sensorData = {}
    #     # Flatten the data
    #     for reading in readings.values():
    #         flattened_data.append(reading)

    #     # get the variable names  (temp/pressure/humidity)
    #     values = flattened_data[0].keys()
    #     # create an array for each variable to store information
    #     for col in values:
    #         sensorData[col] = []

    #     # add the data to the arrays
    #     for row in flattened_data:
    #         if sdate == 0 and edate == 0:  # if no dates are specified, get all data
    #             for col in values:
    #                 sensorData[col].append(row[col])
    #         elif (
    #             int(row["timestamp"]) >= sdate and int(row["timestamp"]) <= edate
    #         ):  # verify data is within range
    #             for col in values:
    #                 sensorData[col].append(row[col])
    #         else:
    #             pass
    #     out[sensor] = sensorData  # add the data to the output dictionary

    return out


def askSensor(sensors):
    for sensor in sensors:
        cont = input("Would you like to include sensor " + sensor + "? (y/n)")
        if cont == "n":
            sensors.remove(sensor)
    return sensors


def getSensors(index, s, e):
    out = []
    for time in index:
        if (int(time) >= s and int(time) <= e) or (s == 0 and e == 0):
            out += index[time]
    out = list(set(out))
    return out
