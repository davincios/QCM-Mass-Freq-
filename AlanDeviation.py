import allantools
import matplotlib.pyplot as plt
import numpy as np

'''
@Todo: switch from matplotlib to plotly (looks nicer)
import plotly
import plotly.express as px
'''

# Class to calculate and display Adam deviation. 
class AlanDeviation:
    def __init__(self, title="Alan deviation with varying Tau values (x-axis)"):
        self._title = title
        self.y = []
        self.tau = np.linspace(0, 100, 100) # self.tau = np.linspace(0, 5, 10)
        self.tau_result = []
        self.alan_dev_result = []       
        self.error = []          
        self.data_points = []         
        self.avg_adev = 0

    def generate_noise(self, N=10000):
        # generate some frequency noise data with N data points.
        self.y = allantools.noise.white(N)

    def logspace_tau(self):
        self.tau = np.logspace(0, 3, 50)

    def add_data(self, data):
        self.y = data
        self.calculate_adev()

    def calculate_adev(self, sample_rate=1):
        # x = allantools.noise.white(10000)
        # (t2, ad, ade, adn) = allantools.adev(
        #     x, rate=sample_rate, data_type="freq", taus=self.tau)
        (t2, ad, ade, adn) = allantools.adev(
            self.y, rate=sample_rate, data_type="freq", taus=self.tau)

        self.tau_result = t2                    # tau values
        self.alan_dev_result = ad               # Alan deviations per tau
        self.error = ade                        # errors of alan adeviations
        self.data_points = adn                  # values of N for t

        # Determine a tau value
        tau_index = 40
        self.avg_adev = ad[tau_index]
        # print('[TAU {}] = {}'.format(tau_index, round(self.avg_adev,2)))
        return ad

    def reset_data(self):
        self.y = []
        self.tau_result = []
        self.alan_dev_result = []       
        self.error = []          
        self.data_points = []         
        self.avg_adev = 0

    def show_plot(self):
        plt.plot(self.tau_result, self.alan_dev_result)  # Plot the results || Alternatively = plt.loglog
        plt.xlabel("Tau (s)")
        plt.ylabel("Alan deviation")
        plt.title("Alan deviation with varying Tau values (x-axis)")
        plt.grid()
        plt.show()
