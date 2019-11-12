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
        self.tau = np.linspace(0, 100, 1000)
        # self.tau = np.linspace(0, 5, 10)

        self.tau_result = []

    def generate_noise(self, N=10000):
        # generate some frequency noise data with N data points.
        self.y = allantools.noise.white(N)

    def logspace_tau(self):
        self.tau = np.logspace(0, 3, 50)

    def add_data(self, data):
        self.y = data

    def calculate_adev(self, sample_rate=1):
        (t2, ad, ade, adn) = allantools.adev(
            self.y, rate=sample_rate, data_type="freq", taus=self.tau)

        self.tau_result = t2                    # tau values
        self.alan_dev_result = ad               # Alan deviations per tau
        self.error = ade                        # errors of alan adeviations
        self.data_points = adn                  # values of N for t
        return ad

    def show_plot(self):
        self.calculate_adev()
        plt.plot(self.tau_result, self.alan_dev_result)  # Plot the results || Alternatively = plt.loglog
        plt.xlabel("Tau (s)")
        plt.ylabel("Alan deviation")
        plt.title("Alan deviation with varying Tau values (x-axis)")
        plt.grid()
        plt.show()
