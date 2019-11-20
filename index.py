import tkinter
import pandas as pd
from tkinter import W
from AlanDeviation import AlanDeviation
import plotly
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np


# Setting up the main loop.
def main():
    # Setup variable for the seperate tests
    test_data = collect_frequency_data(
        'tube droplet 20-11.txt', False).values

    # plot data
    plot_data(test_data)

    # Frequency shift.
    min_value = min(test_data)
    max_value = max(test_data)

    # Frequency shift not always correct, due to settling. 
    frequency_shift = max_value - min_value

    print("The min value is", min_value)
    print("The max value is", max_value)
    print("The frequency shift", frequency_shift)

    # q_factor_normal_dist(test_data, False)
    # q_factor_normal_dist(test_data, True)


# Helper functions.
def get_standard_metrics(data, print_metrics=False):
    mu = np.median(data)
    sigma = np.std(data)
    avg = np.average(data)
    n_samples = len(data)

    if print_metrics:
        print('The standard deviation is...', sigma)
        print('The median is...', mu)
        print('The average is...', avg)
        print('The amount of samples is...', n_samples)

    return mu, sigma, n_samples


# Plot data function.
def plot_data(y_data, title='Frequency over Time', y_label='Frequency (Hz)', x_label='Time (s)'):
    plt.plot(y_data)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.title(title)
    plt.show()


# Returns the data of the last experiment (38 000 seconds / samples).
def collect_data(data_file_name, show_fig=False, is_open_qcm_file=False):
    _data = pd.read_fwf('./data/{}'.format(data_file_name), sep=" ",
                        header=None, index=False)
    if is_open_qcm_file:
        _data.columns = ["Date", "Time", "Frequency", "Temperature"]

    if show_fig:
        _data.columns = ["Frequency"]
        plot_data(_data, title=data_file_name)

    return _data

# Returns the data of the last experiment (38 000 seconds / samples).


def collect_temperature_data(data_file_name, show_fig=True, is_open_qcm_file=False):
    data_temperature = collect_data(data_file_name)
    if is_open_qcm_file:
        data_temperature = data_temperature["Temperature"]

    if show_fig:
        plot_data(data_temperature, title=data_file_name)

    return data_temperature

# Returns the frequency data only. Data standard value is data of last experiment.


def collect_frequency_data(data_file_name, show_fig=False, print_metrics=False, is_open_qcm_file=False):
    data_frequency = collect_data(data_file_name)

    if is_open_qcm_file:
        data_frequency = data_frequency["Frequency"]

    if print_metrics:
        print('Frequency standard metrics:')
        get_standard_metrics(data_frequency)

    if show_fig:
        plot_data(data_frequency, title=data_file_name)

    return data_frequency

# Returns data of the environmnent box.


def get_temperature_box_data(show_fig=False, print_metrics=False):
    _data = pd.read_fwf('./data/Arduino control box.txt', sep=" ",
                        header=None, index=False).head(3000)
    _data.columns = ["Temperature"]
    data_temperature = _data["Temperature"]

    if print_metrics:
        print('Temperature standard metrics:')
        get_standard_metrics(data_temperature)

    if show_fig:
        plt.plot(data_temperature)
        plt.show()

    return data_temperature


# Calculates the Q value, based on creating a normal distriubtion(standard deviation, mean) of the 38 000 test.
def q_factor_normal_dist(data, is_alan_dev=False, show_fig=False):
    # Normal distribution.
    (mu, sigma, n_samples) = get_standard_metrics(data)
    # s = np.random.normal(mu, sigma, n_samples)

    if is_alan_dev:
        # If we want the q factor with the alan deviation, we switch the sigma for the rest of the calcualtion for the alan deviation
        # Calculate alan deviation to use for calculations
        a_dev = get_alan_deviation(data)
        sigma = a_dev

    # Take not the calculated values but the Alan deviation
    s = np.random.normal(mu, sigma, n_samples)

    # Convert the normal distribution into a histogram.
    bin_amount = 100
    count, bins, ignored = plt.hist(s, bin_amount, normed=True)

    # Create a plot.
    if show_fig:
        # plt.plot(s)
        plt.xlabel("Frequency buckets")
        plt.ylabel("Intensity")
        plt.title("Normal distribution model of Frequency response")
        plt.show()

    # Height of the normal dist@ check the formula for the
    y = 1/(sigma * np.sqrt(2 * np.pi)) * \
        np.exp(- (bins - mu)**2 / (2 * sigma**2))
    amplitude = max(y)
    y_3db = amplitude/np.sqrt(2)

    # In what bucket value falls the 3db cutoff?
    y_sorted = sorted(y)
    y_sorted_index_3db = np.digitize(
        np.array(y_3db), y_sorted, right=True)
    y_3db_bin = y_sorted[y_sorted_index_3db]

    # At what index is the bin value in the unsorted normal distribution?
    bin_3db_index = np.where(y == y_3db_bin)[0][0]

    # What is the frequency (x value) at the 3db cutoff?
    frequency_3db = bins[bin_3db_index]

    # What is the delta frequency?
    delta = abs(mu-frequency_3db)
    q_factor = (mu/(2*delta))

    if is_alan_dev:
        print('[Q Factor]: {}K [ADEV]: {}'.format(
            round(q_factor/1000, 0), round(sigma, 2)))
    else:
        print('[Q Factor]: {}K [SDEV]: {}'.format(
            round(q_factor/1000, 0), round(sigma, 2)))

    return q_factor


def get_alan_deviation(data, show_fig=False):
    # Read values out of measurement file.
    # Setup alan deviation and pass data.
    a = AlanDeviation()
    a.reset_data()
    # Alternative, if the changes are small over time, a.logspace_tau()
    a.add_data(data)
    # a.logspace_tau()
    if show_fig:
        a.show_plot()

    return a.avg_adev


def print_introduction():
    print("\n------------------------WELCOME TO THE ULTIMATE QCM ANALYZER) ----------------------------------\n")
    print("Today we'll discover which QCM Device will have the most spice!")
    print("Standard Deviation varies around 4.58")
    print("Alan Deviation varies between 0.03 and 0.15, depending on the tau")
    print("\n-----------------------END OF INTRODUCTION----------------------------\n")


# Run the main loop
main()


'''
Todos: 
- Put the helper functions into a seperate file. 




'''


# def get_q_factors_first_experiments():
#     water_test_19_nov = collect_frequency_data('WaterTest-19-Nov.txt', True)
#     first_test_11_nov = collect_frequency_data('Roomtemp.txt', True)

#     # Get q factor with standard deviation.
#     q1 = q_factor_normal_dist(water_test_19_nov, False)
#     q2 = q_factor_normal_dist(first_test_11_nov, False)
#     # Get q factor with alan deviation.
#     q1 = q_factor_normal_dist(water_test_19_nov, True)
#     q2 = q_factor_normal_dist(first_test_11_nov, True)
