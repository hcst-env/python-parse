from datetime import datetime
import requests
import json
from parse_data import parse
from plot import plot

# API url:
# url = "http://131.215.193.162:4445/jsonbrowser"
datapath = "./out/"
indexpath = "./out/index.json"


# Function to get the data from the API:
def get_data():
    # Get the data from the API:

    # Convert the response to JSON:
    with open(indexpath) as f:

        data = json.loads(f.read())

    # Return the data:
    return data


def date_picker():
    custom_date = input("Do you want a custom date?(Default is all time) (yes/no): ")
    if custom_date.lower() != "yes":
        return (0, 0)

    now = datetime.now()
    print("Press enter to continue with default")
    year = input(f"Enter the start year (default is {now.year}): ")
    year = int(year) if year else now.year

    month = input(f"Enter the start month (default is {now.month}): ")
    month = int(month) if month else now.month

    day = input(f"Enter the start day (default is {now.day}): ")
    day = int(day) if day else now.day

    hour = input(f"Enter the start hour (default is {now.hour}): ")
    hour = int(hour) if hour else now.hour

    start_date = datetime(year, month, day, hour)
    start_date_epoch = int(start_date.timestamp())

    custom_end_date = input(
        "Do you want a custom end date? (default is now) (yes/no): "
    )
    if custom_end_date.lower() == "yes":
        year = input(f"Enter the end year (default is {now.year}): ")
        year = int(year) if year else now.year

        month = input(f"Enter the end month (default is {now.month}): ")
        month = int(month) if month else now.month

        day = input(f"Enter the end day (default is {now.day}): ")
        day = int(day) if day else now.day

        hour = input(f"Enter the end hour (default is {now.hour}): ")
        hour = int(hour) if hour else now.hour

        end_date = datetime(year, month, day, hour)
    else:
        end_date = now

    end_date_epoch = int(end_date.timestamp())

    return (start_date_epoch, end_date_epoch)


if __name__ == "__main__":
    # Get the data:
    data = get_data()
    # Parse the data:
    s, e = date_picker()
    data = parse(data, s, e, datapath)
    # Plot the data:
    plot(data)
