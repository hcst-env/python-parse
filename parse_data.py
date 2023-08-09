import json



def parse(data, sdate, edate):

    out = {}
    sensors = []
    # Get the sensors that are BME680s
    for sensor in list(data["Sensors"].keys()):
        if data["Sensors"][sensor]["type"] == "BME680":
            sensors.append(sensor)

    # Get the data for each sensor
    
    for sensor in sensors:
        cont=input("Would you like to include sensor "+sensor+"? (y/n)")
        if cont == "n":
            continue

        readings = data[sensor]["readings"]
        flattened_data = []
        sensorData = {}
        # Flatten the data
        for reading in readings.values():
            flattened_data.append(reading)

        #get the variable names  (temp/pressure/humidity)  
        values = flattened_data[0].keys()
        #create an array for each variable to store information
        for col in values:
            sensorData[col] = []

        #add the data to the arrays    
        for row in flattened_data:
            if sdate == 0 and edate == 0:#if no dates are specified, get all data
                for col in values:
                    sensorData[col].append(row[col])
            elif int(row["timestamp"]) >= sdate and int(row["timestamp"]) <= edate:#verify data is within range
                for col in values:
                    sensorData[col].append(row[col])
            else:
                pass
        out[sensor] = sensorData#add the data to the output dictionary

    return out
