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
---------------------------------------------
5) Calculate Q-factors from file and store somewhere (into a new csv file)
---------------------------------------------
6) Loop through all filenames and store the resulting graphs into a new folder.

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


def plot_data(x_data, y_data, title, x_label='Frequency (Hz)', y_label='Impedance (Ohm)'):
    plt.plot(x_data, y_data)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.title(title)
    plt.show()

# Function to determine q factor


def get_q_factor(g, frequency_array):
    # Determine 3dB cutoff height.
    amplitude = max(g)
    g_3db = amplitude/np.sqrt(2)

    # Find number closest to y_3db.
    g_3db_closest = min(g, key=lambda x: abs(x-g_3db))

    # Determine frequency index @ 3dB cutoff height.
    index_3db = [index for index in range(
        len(g)) if g[index] == g_3db_closest][0]
    frequency_3db = frequency_array[index_3db]

    # Determine the resonance frequency.
    index_resonance_max = [index for index in range(
        len(g)) if g[index] == amplitude][0]
    frequency_resonance = frequency_array[index_resonance_max]

    # Determine the q factor
    delta = abs(frequency_resonance-frequency_3db)
    q_factor = frequency_resonance/(2*delta)
    q_factor = round(q_factor, 0)

    # return the q factor. 
    return q_factor

    # print('The index of 3db cutoff is...', index_3db)
    # print('The resonance frequency is...', frequency_resonance)
    # print('The q factor is...', q_factor)


# Execute functions.


def execute(file_name):
    data = collect_data(file_name)
    frequency_data = data['Frequency']
    s11_data = data['S11']

    # Create title string for labling.
    title_string = "Impedance over Frequency - {}".format(file_name)

    # Calculate Z / Impedance and store in new array
    z_array = [calculate_z(s) for s in s11_data]

    # Convert Impedance to Conductance (G) and also store in array.
    g_array = [1/z for z in z_array]

    get_q_factor(g_array, frequency_data)

    # plot_data(x_data=frequency_data, y_data=g_array, title=title_string,
    #           x_label='Frequency (Hz)', y_label='Impedance (Ohm)')


# Execute file functions.
execute('SETUP5 - D WATER TUBE - M3 M.CSV')


# def plot_s11():
#     title_string = "S11 over Frequency - {}".format(file_name)
#     plot_data(x_data=frequency_data, y_data=s11_data, title=title_string,
#               x_label='Frequency (Hz)', y_label='S11 (Ohm)')
