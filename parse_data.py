import json

# empyt directory


def parse(data, sdate, edate):
    out = {}
    sensors = []
    for sensor in list(data["Sensors"].keys()):
        if data["Sensors"][sensor]["type"] == "BME680":
            sensors.append(sensor)

    for sensor in sensors:
        readings = data[sensor]["readings"]
        flattened_data = []
        sensorData = {}
        for reading in readings.values():
            flattened_data.append(reading)
        values = flattened_data[0].keys()
        for col in values:
            sensorData[col] = []
        for row in flattened_data:
            if sdate == 0 and edate == 0:
                for col in values:
                    sensorData[col].append(row[col])
            elif int(row["timestamp"]) >= sdate and int(row["timestamp"]) <= edate:
                for col in values:
                    sensorData[col].append(row[col])
            else:
                pass
        out[sensor] = sensorData
    with open("files.json", "w") as output_file:
        json.dump(out, output_file)
    return out
