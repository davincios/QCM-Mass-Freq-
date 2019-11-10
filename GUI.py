import tkinter
from tkinter import W
import pandas as pd
import plotly
import plotly.express as px
from ScatterPlot import ScatterPlot

print(plotly.__version__)


# Read the data table of the last experiment. 
df = pd.read_csv('./test1.csv')

fig = px.line(df, x = 'Time', y = 'Frequency', title='Frequency Over Time')
fig.show()

# Setting up the root for the GUI program. 
root = tkinter.Tk()
root.title("Mass Frequency Shift")
root.geometry("500x500")

# Initializing the plot. 
aPlot = ScatterPlot(60, 'Frequency shifts scatter plot')

def windowCallBack():
        print( "The window callBack function", "Hello World") 

# Adding a start calculation button.
tkinter.Label(root, text = "The Best QCM program in the world!").pack()
B = tkinter.Button(root, text ="Calculate mass frequency shift", command=aPlot.show_plot)
B.pack()

# Adding a close button. 
tkinter.Button(master=root, text='Quit', command=root.destroy).pack()

# Start the root 
root.mainloop()