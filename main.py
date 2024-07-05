from datetime import datetime
import requests
import json
from parse_data import parse
from plot import plot
from tqdm import tqdm
import math as Math


# API url:
url = "http://131.215.193.162:4445/jsonbrowser"


def dayEpoch(
    time,
):  # gets the epoch time fo the start of the day - this is ing GMT to avoid confuison with DST - so days will be brokn up based on GMT
    return Math.floor(time / 86400) * 86400


# download files with timetamps
def download_file(url, dest_path, start, end):
    print(f"{url}?start={start}&end={end}")
    response = requests.get(f"{url}?start={start}&end={end}", stream=True)
    total_size = int(response.headers.get("content-length", 0))
    chunk_size = 1024  # 1 KB
    with open(dest_path, "wb") as file, tqdm(
        desc=dest_path,
        total=total_size,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=chunk_size):
            file.write(data)
            bar.update(len(data))


# Function to get the data from the API:
def get_data():
    # Get the data from the API:
    proces = input("Do you want to get new data? (default y) (y/n): ")

    if not (proces.lower() == "n"):
        s, e = date_picker()
        print(s, e)
        print("Waiting for sam to process the data...")

        download_file(url, "data.json", s, e)
        # with open("data.json", "w") as f:
        #     json.dump(data, f)
    # Return the data:
    with open("data.json", "r") as f:
        data = json.load(f)
    return data, s, e


def date_picker():
    custom_date = input(
        "Do you want a custom date? (y/n): (It is reccomended as there is a lot of data and it may be very slow) "
    )
    if custom_date.lower() != "y":
        return (0, 0)

    now = datetime.now()

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
    print("To Proceed with Default Press Enter")
    data, s, e = get_data()
    # Parse the data:

    data = parse(data, s, e)
    # Plot the data:
    plot(data)
