import tkinter
import pandas as pd
from tkinter import W
from AlanDeviation import AlanDeviation
import plotly
import plotly.express as px
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
    a.show_plot()


# Read the data table of the last experiment.
def collect_data():
    # fwf stands for 'fixed with formatted lines'
    _data = pd.read_fwf('./data/Roomtemp.txt', sep=" ",
                        header=None, index=False)
    _data.columns = ["Date", "Time", "Frequency", "Temperature"]
    data_frequency = _data["Frequency"].values
    fig = px.line(_data, x='Time', y='Frequency',
                  title='Frequency Over Time')
    fig.show()

    print('The standard deviation is...', np.std(data_frequency))

    return data_frequency


# Run main
main()
