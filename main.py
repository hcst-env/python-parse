import requests
import json
from parse_data import parse
from plot import plot

# API url:
url = "http://131.215.193.162:4445/jsonbrowser"


# Function to get the data from the API:
def get_data():
    # Get the data from the API:
    response = requests.get(url)
    # Convert the response to JSON:
    data = json.loads(response.text)
    # Return the data:
    return data


if __name__ == "__main__":
    # Get the data:
    data = get_data()
    # Parse the data:
    data = parse(data, 0, 0)
    # Plot the data:
    plot(data)
