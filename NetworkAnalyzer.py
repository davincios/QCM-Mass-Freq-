import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


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


def plot_data(x_data, y_data, title, x_label='Frequency (Hz)', y_label='Conductance (S)'):
    plt.plot(x_data, y_data)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.title(title)
    # plt.show()
    plt.savefig('./data/network_analyzer_figures/{}'.format(title[:-3]))


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
    if delta == 0:
        return 0
    q_factor = frequency_resonance/(2*delta)
    q_factor = round(q_factor, 0)

    # return the q factor.
    return q_factor

    # print('The index of 3db cutoff is...', index_3db)
    # print('The resonance frequency is...', frequency_resonance)
    # print('Delta in the q factor calculation is.....', delta)
    # print('The q factor is...', q_factor)


# Execute functions.


def execute_data_set(file_name):
    data = collect_data(file_name)
    frequency_data, s11_data = data['Frequency'], data['S11']

    # Calculate Z-Impedance and convert to Conductance (G) and also store in array.
    g_array = [1/z for z in [calculate_z(s) for s in s11_data]]
    q_factor = get_q_factor(g_array, frequency_data)

 
    # Error handling. Show graph if error value 0 is returned.
    if q_factor == 0:
        q_factor = 'error'
        result = 'error - {}'.format(file_name)

    else:
        result = round(q_factor)


    # Create title string to label the resulting calculations.
    title_string = "Q-factor = {} for {}".format(
        q_factor, file_name)

    
    # Save the figure
    plot_data(x_data=frequency_data, y_data=g_array, title=title_string,
              x_label='Frequency (Hz)', y_label='Conductance (S)')

    



    # Return the results
    return result

    # print(title_string)


# Execute tests.---------------------------
# execute_data_set('SETUP5 - D WATER TUBE - M3 M.CSV')
# execute_data_set('SETUP5 - EMPTY TUBE - M2 P.CSV')

def get_file_names():
    arr = os.listdir('./data/network_analyzer_data')
    return arr


def calculate_and_save():
    q_results = []
    file_names = get_file_names()
    # string_result
    # remove (phase graphs from filenames)
    file_names = [x for x in file_names if '(P)' not in x and 'P.CSV' not in x]

    for file_name in file_names:
        result = execute_data_set(file_name)
        q_results.append(result)
        print('FILE NAME: {} QFACTOR: {}'.format(file_name, result))

    # np.savetxt('qfactor_results.csv', file_names, delimiter=',')


    # print(q_results)
# Save the data.
# np.savetxt('qfactor_results.csv', (col1_array, col2_array, col3_array), delimiter=',')
calculate_and_save()


# def plot_s11():
#     title_string = "S11 over Frequency - {}".format(file_name)
#     plot_data(x_data=frequency_data, y_data=s11_data, title=title_string,
#               x_label='Frequency (Hz)', y_label='S11 (Ohm)')


#  plot_data(x_data=frequency_data, y_data=g_array, title=title_string,
#               x_label='Frequency (Hz)', y_label='Conductance (S)')
