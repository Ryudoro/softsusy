import app
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import are_files
import masses

class MassWindows(tk.Toplevel):
    def __init__(self, app,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.title("Plot masses")
        self.app = app
        self.index = 0
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, expand=1)
        self.neutralino = 'N1'

        self.create_mass_widgets()

    def create_mass_widgets(self):
        

        neut = tk.Entry(self)
        neut.pack(side = tk.LEFT)

        self.update_button = tk.Button(self, text = "choice neutralino", command=lambda :self.update_plot(neut))
        self.update_button.pack(side = tk.LEFT)
    def update_plot(self, neut):

        self.neutralino = str(neut.get())

        self.ax.clear()
        masses.plot_masses(self.app.parameters, self.app.param_mass,self.neutralino, self.fig, self.ax, self.app.options)
        
        self.canvas.draw()
        
        
        