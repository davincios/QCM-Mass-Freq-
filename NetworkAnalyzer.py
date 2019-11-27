import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

'''
Network analyzer todos: 
1) first clean the data with pandas
    - Remove head for rows 1,2,3. 
    - Remove third collumn.
    - Add headers to first two collumns: frequency and s11.
    - Convert scientific notation to numpy / number. 

2) Calculate Z(f) and store in new y array.
3) Plot f-z graph. 
--------------------------------------------
4.1) Get all file names from folder n-analyzer.
4.2) Store all file names into one array. 
5) Loop through all filenames and store the resulting graphs into a new folder. 
'''

# Returns the data of the last experiment (38 000 seconds / samples).


def collect_data(data_file_name):
    data = pd.read_csv('./data/network_analyzer_data/{}'.format(data_file_name),
                       header=None, sep=",", skiprows=3)
    data.columns = ["Frequency", "S11", "-"]
    data = data[["Frequency", "S11"]]

    return data


# Calculate Z.
def calculate_z(s11, z0=20):
    z = z0*(1+s11)/(1-s11)

    return z

# Plot data function.


def plot_data(x_data, y_data, title='Impedance over Frequency', x_label='Frequency (Hz)', y_label='Impedance (Ohm)' , file_name=False):
    plt.plot(x_data, y_data)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.title(title)
    plt.show()

# Run it.

# Execute functions.


def execute(file_name):
    data = collect_data(file_name)
    frequency_data = data['Frequency']
    s11_data = data['S11']

    title_string = "S11 over Frequency - {}".format(file_name)
    plot_data(x_data=frequency_data, y_data=s11_data, title=title_string, x_label='Frequency (Hz)', y_label='S11 (Ohm)' )


# Execute file functions. 
execute('SETUP5 - D WATER TUBE - M3 M.CSV')


