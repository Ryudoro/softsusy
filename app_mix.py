import app
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import are_files
import mixing

class MixingWindows(tk.Toplevel):
    def __init__(self, app,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        self.title("Plot mixing")
        self.app = app
        self.fenetre()
        self.create_mass_widgets()
        self.index = 0
        self.param = {}
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row = 0, column = 0, rowspan = 3, columnspan=3)
        self.neutralino = 'N1'
        
        for i in range(5):
            self.columnconfigure(i,weight=1)
        for i in range(8):
            self.rowconfigure(i,weight=1)

    def create_mass_widgets(self):
        
        

        self.M1_ent = tk.Entry(self)
        self.M1_ent.grid(row = 0, column = 4, padx=5, pady=5)

        self.M1_button = tk.Button(self, text = "choice M_1(MX)", command=lambda :self.update_M1(self.M1_ent))
        self.M1_button.grid(row = 0, column = 5, padx=5, pady=5)

        self.M2_ent = tk.Entry(self)
        self.M2_ent.grid(row = 1, column = 4, padx=5, pady=5)

        self.M2_button = tk.Button(self, text = "choice M_2(MX)", command=lambda :self.update_M2(self.M2_ent))
        self.M2_button.grid(row = 1, column = 5, padx=5, pady=5)

        self.mu_ent = tk.Entry(self)
        self.mu_ent.grid(row = 2, column = 4, padx=5, pady=5)

        self.mu_button = tk.Button(self, text = "choice mu(MX)", command=lambda :self.update_mu(self.mu_ent))
        self.mu_button.grid(row = 2, column = 5, padx=5, pady=5)
        
        self.plote = tk.Button(self, text = "plot", command=self.plot)
        self.plote.grid(row = 3, column = 5, padx=5, pady=5)


    def update_plot(self, neut):

        self.neutralino = str(neut.get())

        self.ax.clear()
        #masses.plot_masses(self.app.parameters, self.app.param_mass,self.neutralino, self.fig, self.ax, self.app.options)
        
        self.ax.plot([0,1,2,3],[4,5,6,7], marker = 'o', linestyle = '-')
        self.canvas.draw()

    def update_M1(self, truc):
        self.param['M_1(MX)'] = float(truc.get())
        self.ax.clear()

    def update_M2(self, truc):
        self.param['M_2(MX)'] = float(truc.get())
        self.ax.clear()

    def update_mu(self, truc):
        self.param['mu(MX)'] = float(truc.get())
        self.ax.clear()

    def fenetre(self):
        largeur_screen = self.winfo_screenwidth()
        hauteur_screen = self.winfo_screenheight()

        largeur_fenetre= int(largeur_screen*0.8)
        hauteur_fenetre = int(largeur_fenetre*0.8)
        
        x_position = int((largeur_screen-largeur_fenetre)/2)
        y_position = int((hauteur_screen-hauteur_fenetre)/2)

        self.geometry(f"{largeur_fenetre}x{hauteur_fenetre}+{x_position}+{y_position}")

    def plot(self):
        mixing.plot(self.param,self.ax)
        self.canvas.draw()
