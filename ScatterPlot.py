import numpy as np
import matplotlib.pyplot as plt

# Create data
class ScatterPlot: 
    def __init__(self, N, title):
        plt.title(title)
        plt.legend(loc=2)

        self._g1 = (0.6 + 0.6 * np.random.rand(N), np.random.rand(N))
        self._g2 = (0.4+0.3 * np.random.rand(N), 0.5*np.random.rand(N))
        self._g3 = (0.3*np.random.rand(N), 0.3*np.random.rand(N))
        self._data = (self._g1, self._g2, self._g3)
        self._colors = ("red", "green", "blue")
        self._groups = ("coffe", "tea", "water")
        self.populate_plot()

    def zip_data(self):
        _zipped = zip(self._data, self._colors, self._groups)
        self._zipped = _zipped

    def populate_plot(self): 
        self.zip_data()
        for data, color, group in self._zipped:
            x, y = data
            plt.scatter(x, y, alpha=0.8, c=color, edgecolors='none', s=30, label=group)


    def show_plot(self):
        plt.show()

