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
    a.logspace_tau()
    # a.show_plot()


# Read the data table of the last experiment.
def collect_data():
    # fwf stands for 'fixed with formatted lines'
    _data = pd.read_fwf('./data/Roomtemp.txt', sep=" ",
                        header=None, index=False)
    _data.columns = ["Date", "Time", "Frequency", "Temperature"]
    data_frequency = _data["Frequency"].values
    fig = px.line(_data, x='Time', y='Frequency',
                  title='Frequency Over Time')

    # Regular frequency graph.
    fig.show()

    print('The standard deviation is...', np.std(data_frequency))
    print('The standard median is...', np.median(data_frequency))
    print('The standard average is...', np.average(data_frequency))

    mu = 4953184
    sigma = 4.58
    # sigma = 0.12
    n_samples = len(data_frequency)

    # Normal distribution.
    s = np.random.normal(mu, sigma, n_samples)

    # Create the bins and histogram
    # set to 10 for accurate results.
    count, bins, ignored = plt.hist(s, 40, normed=True)

    # Determine the height of the normal distribution. According to the bins.
    height_normal_dist = 1/(sigma * np.sqrt(2 * np.pi)) * \
        np.exp(- (bins - mu)**2 / (2 * sigma**2))
    max_height = max(height_normal_dist)
    cutoff_3db_height = max_height/np.sqrt(2)

    # What is the value of the correct bin?
    sorted_height_dist = sorted(height_normal_dist)
    cutoff_bin_index = np.digitize(
        np.array(cutoff_3db_height), sorted_height_dist, right=True)
    bin_value = sorted_height_dist[cutoff_bin_index]
    index_cutoff_in_dist = np.where(height_normal_dist == bin_value)[0][0]
    element = height_normal_dist[index_cutoff_in_dist]

    # The bin value of the frequency @ cut off position.
    frequency_cutoff = bins[index_cutoff_in_dist]
    delta_frequency = abs(mu - frequency_cutoff)
    q_factor = mu/(2*delta_frequency)

    print('THE Q FACTOR!!!!', q_factor)
    print('Delta frequency cutoff', delta_frequency)
    print('Frequency cutoff', frequency_cutoff)
    print('bin value', bin_value)
    print('index_of_cutoff_in_dist',  index_cutoff_in_dist)
    print('Element cut height normal dist', element)

    # To which bin does the cut off height belong?
    # height_bin_index = height_normal_dist[cutoff_bin_value]
    # print('height_bin_index', height_bin_index)

    # Print values
    print('Height_normal_dist', height_normal_dist)
    print('Max value of height normal list', max_height)

    # Plot the distribution curve
    plt.plot(bins, height_normal_dist, linewidth=3, color='y')
    plt.title('Frequency with Normal distribution, Sigma = {}'.format(sigma))
    plt.xlabel('Frequency (zoomed in)')
    plt.show()

    return data_frequency


# Run main
main()
