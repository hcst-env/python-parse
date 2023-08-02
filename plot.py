import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime


def plot(data):
    # convert strings to floats
    for sensor in data:
        for metric in data[sensor]:
            data[sensor][metric] = [float(i) for i in data[sensor][metric]]

    # Convert epoch timestamps to datetime objects( human readable)
    for sensor in data:
        timestamp_list = data[sensor]["timestamp"]
        print(data[sensor]["timestamp"][0])

        data[sensor]["timestamp"] = [
            datetime.fromtimestamp(int(timestamp)) for timestamp in timestamp_list
        ]
        print(data[sensor]["timestamp"][0])

    # Create subplots for each metric
    fig, axs = plt.subplots(3)

    # Plot each sensor
    for sensor in data:
        # Plot temperature
        axs[0].plot(
            data[sensor]["timestamp"], data[sensor]["temperature"], label=sensor
        )
        # Plot pressure
        axs[1].plot(data[sensor]["timestamp"], data[sensor]["pressure"], label=sensor)
        # Plot humidity
        axs[2].plot(data[sensor]["timestamp"], data[sensor]["pressure"], label=sensor)

    # Format the x-axis and make the dates include min/seocnds
    for ax in axs:
        ax.format_xdata = mdates.DateFormatter("%Y-%m-%d %H:%M:%S")
        ax.xaxis.set_major_formatter(ax.format_xdata)

        
    # add titles and legends
    axs[0].set_title("Temperature (C)")
    axs[0].legend()

    axs[1].set_title("Pressure (kPa)")
    axs[1].legend()

    axs[2].set_title("Humidity")
    axs[2].legend()

    # Rotate and align the tick labels so they look better
    plt.gcf().autofmt_xdate()

    # Display the plot
    plt.show()
