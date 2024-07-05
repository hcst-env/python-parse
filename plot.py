import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from scipy.optimize import curve_fit
import numpy as np


def exponential_decay(t, N0, k):
    return N0 * np.exp(-k * t)


def plot(data):
    # convert strings to floats
    for sensor in data:
        for metric in data[sensor]:
            data[sensor][metric] = [float(i) for i in data[sensor][metric]]

    # Convert epoch timestamps to datetime objects (human-readable)
    for sensor in data:
        timestamp_list = data[sensor]["timestamp"]
        data[sensor]["timestamp"] = [
            datetime.fromtimestamp(int(timestamp)) for timestamp in timestamp_list
        ]

    # Create subplots for each metric
    fig, axs = plt.subplots(3, figsize=(12, 8))

    # Peak detection parameters
    peak_params = {
        "distance": 80,  # Minimum distance between peaks
        "prominence": 0.5,  # Minimum prominence of peaks
    }

    # Plot each sensor and find peaks
    for sensor in data:
        # Plot temperature and find peaks
        axs[1].plot(
            data[sensor]["timestamp"], data[sensor]["temperature"], label=sensor
        )
        # Plot humidity and find peaks
        axs[0].plot(data[sensor]["timestamp"], data[sensor]["humidity"], label=sensor)

        axs[2].plot(data[sensor]["timestamp"], data[sensor]["pressure"], label=sensor)

    # Extract LAB1 sensor data for exponential decay fitting
    # FitSensor = "d"
    # if FitSensor in data:
    #     timestamps = np.array([ts.timestamp() for ts in data[FitSensor]["timestamp"]])
    #     temperatures = np.array(data[FitSensor]["temperature"])

    #     # Normalize timestamps for fitting
    #     normalized_timestamps = timestamps - timestamps[0]

    #     # Fit the exponential decay model to the data
    #     initial_guess = [temperatures[0], 0.01]
    #     popt, pcov = curve_fit(
    #         exponential_decay, normalized_timestamps, temperatures, p0=initial_guess
    #     )
    #     fitted_temperatures_exp = exponential_decay(normalized_timestamps, *popt)

    #     # Print the equation of the fitted exponential decay
    #     N0, k = popt
    #     print(
    #         f"Fitted Exponential Decay Equation: Temperature(t) = {N0:.2f} * exp(-{k:.4f} * t)"
    #     )

    #     # Fit quadratic and cubic polynomials to the data
    #     coeffs_quad = np.polyfit(normalized_timestamps, temperatures, 2)
    #     coeffs_cubic = np.polyfit(normalized_timestamps, temperatures, 3)

    #     # # Generate fitted data for quadratic and cubic models
    #     fitted_temperatures_quad = np.polyval(coeffs_quad, normalized_timestamps)
    #     # fitted_temperatures_cubic = np.polyval(coeffs_cubic, normalized_timestamps)

    #     # # Print the equations of the fitted polynomials
    #     print(
    #         f"Fitted Quadratic Equation: Temperature(t) = {coeffs_quad[0]:.4e} * t^2 + {coeffs_quad[1]:.4e} * t + {coeffs_quad[2]:.4e}"
    #     )
    #     # print(
    #     #     f"Fitted Cubic Equation: Temperature(t) = {coeffs_cubic[0]:.4e} * t^3 + {coeffs_cubic[1]:.4e} * t^2 + {coeffs_cubic[2]:.4e} * t + {coeffs_cubic[3]:.4e}"
    #     # )

    #     # Overlay the fitted curves on the temperature plot
    #     # axs[1].plot(
    #     #     data[FitSensor]["timestamp"],
    #     #     fitted_temperatures_exp,
    #     #     label="FitSensor Exp Fit",
    #     #     linestyle="--",
    #     # )
    #     axs[1].plot(
    #         data[FitSensor]["timestamp"],
    #         fitted_temperatures_quad,
    #         label="fitSensor Quad Fit",
    #         linestyle="-.",
    #     )
    #     # axs[1].plot(
    #     #     data["LAB1"]["timestamp"],
    #     #     fitted_temperatures_cubic,
    #     #     label="LAB1 Cubic Fit",
    #     #     linestyle=":",
    #     # )

    # Format the x-axis and make the dates include min/seconds
    for ax in axs:
        ax.format_xdata = mdates.DateFormatter("%Y-%m-%d %H:%M:%S")
        ax.xaxis.set_major_formatter(ax.format_xdata)

    # Add titles and legends
    axs[1].set_title("Temperature (C)")
    axs[1].legend()

    axs[0].set_title("Humidity")
    axs[0].legend()

    axs[2].set_title("Pressure")
    axs[2].legend()

    # Rotate and align the tick labels so they look better
    plt.gcf().autofmt_xdate()

    # Display the plot
    plt.show()


def find_settle(data, peaks, threshold=0.03, numpoints=10):
    # goes throught he peaks, and finds the settle point
    # settle point is found by going through and finding the point where the value starts to increase

    # find the settle point
    settle_points = []

    for peak in peaks:
        for i in range(peak + numpoints, len(data) - numpoints):
            if ((data[i + numpoints] - data[i - numpoints]) / numpoints) > threshold:
                settle_points.append(i)
                print(
                    ((data[i + numpoints] - data[i - numpoints]) / numpoints),
                    data[i + numpoints],
                    data[i - numpoints],
                )
                break

            # last_value = data[i]

    return settle_points
