import tkinter
import pandas as pd
from tkinter import W
from AlanDeviation import AlanDeviation
import plotly
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np


# Helper functions.
def get_standard_metrics(data):
    mu = np.median(data)
    sigma = np.std(data)
    avg = np.average(data)
    n_samples = len(data)

    print('The standard deviation is...', sigma)
    print('The median is...', mu)
    print('The average is...', avg)
    print('The amount of samples is...', n_samples)

    return mu, sigma, n_samples


# Setting up the main loop.
def main():
    print("\n------------------------WELCOME TO THE ULTIMATE QCM ANALYZER) ----------------------------------\n")
    print("Today we'll discover which QCM Device will have the most spice!")
    print("Standard Deviation varies around 4.58")
    print("Alan Deviation varies between 0.03 and 0.15, depending on the tau")
    print("\n-----------------------END OF INTRODUCTION----------------------------\n")

    # Read values out of measurement file.
    data = collect_data()
    # Setup alan deviation and pass data.
    a = AlanDeviation()
    # Alternative, if the changes are small over time, a.logspace_tau()
    a.add_data(data)
    # a.logspace_tau()
    # a.show_plot()


# Returns the data of the last experiment (38 000 seconds / samples).
def collect_data(show_fig=False):
    _data = pd.read_fwf('./data/Roomtemp.txt', sep=" ",
                        header=None, index=False)
    _data.columns = ["Date", "Time", "Frequency", "Temperature"]
    if show_fig:
        fig = px.line(_data, x='Time', y='Frequency',
                      title='Frequency Over Time')
        fig.show()

    return _data

# Returns the frequency data only. Data standard value is data of last experiment.


def collect_frequency_data(data=collect_data(), show_fig=False, print_metrics=False):
    data_frequency = data["Frequency"].values

    if print_metrics:
        print('Frequency standard metrics:')
        get_standard_metrics(data_frequency)

    if show_fig:
        fig = px.line(data, x='Time', y='Frequency',
                      title='Frequency Over Time')
        fig.show()

    return data_frequency

# Returns data of the environmnent box.


def get_temperature_box_data(show_fig=False, print_metrics=False):
    _data = pd.read_fwf('./data/Arduino control box.txt', sep=" ",
                        header=None, index=False)
    _data.columns = ["Temperature"]
    data_temperature = _data["Temperature"].values

    if print_metrics:
        print('Temperature standard metrics:')
        get_standard_metrics(data_temperature)

    if show_fig:
        plt.plot(data_temperature, title='Temperature over time')
        plt.show()

    return data_temperature


# Calculates the Q value, based on creating a normal distriubtion(standard deviation, mean) of the 38 000 test.
def q_factor_normal_dist(data=collect_frequency_data()):
    (mu, sigma, n_samples) = get_standard_metrics(data)
    # Normal distribution.
    s = np.random.normal(mu, sigma, n_samples)

    # Convert the normal distribution into a histogram.
    bin_amount = 100
    count, bins, ignored = plt.hist(s, bin_amount, normed=True)
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
    q_factor = mu/(2*delta)
    print('The Q factor for the normal distributino is:', q_factor)

    return q_factor


# Calculates the Q value, based on creating a normal distriubtion(standard deviation, mean) of the 38 000 test.
# Run main
main()
q_factor_normal_dist()
