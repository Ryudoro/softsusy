import tkinter as tk
from tkinter import filedialog, messagebox
import input_generator
import masses
import remove
import app_mass
import app_mix
import extended_entry
import verif
# Vos fonctions de génération de fichiers de sortie et d'analyse doivent être importées ici.

class SoftsusyApp:
    def __init__(self, root,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root
        self.root.title("Softsusy Analysis")
        self.root.configure(bg = "#f0f0f0")
        self.title_font = ('Arial', 16, 'bold')
        self.label_font = ('Arial', 8)
        self.fenetre()
        self.parameters = {}
        self.param_enlever = []
        self.entry_name = ''
        self.param_mass = {}
        self.label_param = 1
        self.stock_param = {}
        self.fix_parameters_widgets = []
        self.create_widgets()
        # Créez les éléments de l'interface utilisateur ici (labels, boutons, etc.)

    # Ajoutez des fonctions pour gérer les actions de l'utilisateur, telles que la génération de fichiers,
    # l'ouverture de fichiers et l'exécution des analyses.

    def create_widgets(self):

        num_params = 3

        self.choice_of_parameters(0)

        
        self.mass_choice()
        self.generate_button = tk.Button(self.root, text = "Generate Output_files",font = self.label_font,bg = "#4CAF50", fg = 'white', relief = 'raised', command = self.generate_output)
        self.generate_button.grid(row = num_params, column = 2, padx=5, pady=5, sticky = "ew")

        self.button = tk.Button(self.root,font = self.label_font, text = "Calculation of Mass",bg = '#ED7F10', fg = 'white', relief = 'raised', command = self.masses)
        self.button.grid(row = num_params-1, column = 2, padx=5, pady=5, sticky = "ew")

        self.button = tk.Button(self.root,font = self.label_font, text = "Calculation of Mixing",bg = '#ED7F10', fg = 'white', relief = 'raised', command = self.mix)
        self.button.grid(row = num_params-1, column = 3, padx=5, pady=5, sticky = "ew")

        for i in range(4):
            self.root.columnconfigure(i,weight=1)
        for i in range(10):
            self.root.rowconfigure(i,weight=1)

        self.remo = tk.Button(self.root, text = "remove_files",bg = '#f44336', fg = 'white', relief = 'raised', command = self.remove_all)
        self.remo.grid(row = num_params+1, column = 3, padx=5, pady=5, sticky = "ew")

        self.debuge = tk.Button(self.root, text = "debug", fg = 'white', relief = 'raised', command = self.debug)
        self.debuge.grid(row = num_params, column = 5, padx=5, pady=5, sticky = "ew")

        self.clear = tk.Button(self.root, text = "Clear", fg = 'white', relief = 'raised', command = self.restart)
        self.clear.grid(row = num_params+1, column = 5, padx=5, pady=5, sticky = "ew")
    def fenetre(self):
        largeur_screen = self.root.winfo_screenwidth()
        hauteur_screen = self.root.winfo_screenheight()

        largeur_fenetre= int(largeur_screen*0.8)
        hauteur_fenetre = int(largeur_fenetre*0.8)
        
        x_position = int((largeur_screen-largeur_fenetre)/2)
        y_position = int((hauteur_screen-hauteur_fenetre)/2)

        self.root.geometry(f"{largeur_fenetre}x{hauteur_fenetre}+{x_position}+{y_position}")

    def full_screen(self):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

        #self.root.maxsize(largeur_fenetre, hauteur_fenetre)
    def choice_of_parameters(self,index):

        #label = tk.Label(self.root, text=f"Paramètre {index+1}: ")
        #label.grid(row=index, column = 0, padx=5, pady=5, sticky = "ew")

        #entry_name = tk.Entry(self.root)
        #entry_name.grid(row = index, column = 1, padx=5, pady=5, sticky = "ew")

        self.liste = tk.Listbox(self.root, selectmode = tk.SINGLE, height = 4)
        self.options = ["M_1(MX)", "M_2(MX)", "mu(MX)", "tan(beta)"]
        for option in self.options:
            self.liste.insert(tk.END, option)

        self.liste.grid(row = 0, column = 0, padx=5, pady=5, sticky = "ew")

             
        self.liste.bind('<ButtonRelease-1>', self.clic)
        

        entry_min = extended_entry.EntryWithPlaceholder(self.root, placeholder = 'min')
        entry_min.grid(row = index, column = 1, padx=5, pady=5, sticky = "ew")

        entry_max = extended_entry.EntryWithPlaceholder(self.root, placeholder = 'max')
        entry_max.grid(row = index, column = 2, padx=5, pady=5, sticky = "ew")

        entry_step = extended_entry.EntryWithPlaceholder(self.root, placeholder = 'step')
        entry_step.grid(row = index, column = 3, padx=5, pady=5, sticky = "ew")


        submit_button = tk.Button(self.root, text = "Submit",bg = '#0F9DE8', fg = 'white', relief = 'raised', command = lambda: self.submit_data(index, entry_min, entry_max, entry_step, self.entry_name))
        submit_button.grid(row = index, column = 4, padx=5, pady=5, sticky = "ew")


    def clic(self, liste):

        for index in self.liste.curselection():
            self.entry_name = self.liste.get(index)

    def mass_choice(self):

        label = tk.Label(self.root, text="Paramètre choice: ", font = ('Arial', 10),bg = "#f0f0f0")
        label.grid(row=5, column = 0, padx=5, pady=5, sticky = "ew")

        mass = extended_entry.EntryWithPlaceholder(self.root, placeholder = 'name')
        mass.grid(row = 5, column = 1, padx=5, pady=5, sticky = "ew")

        value = extended_entry.EntryWithPlaceholder(self.root, placeholder = 'value')
        value.grid(row = 5, column = 2, padx=5, pady=5, sticky = "ew")

        submit_button = tk.Button(self.root, text = "Submit",bg = '#0F9DE8', fg = 'white', relief = 'raised', command = lambda: self.fix_parameters(mass,value))
        submit_button.grid(row = 5, column = 3, padx=5, pady=5, sticky = "ew")
        m = str(mass.get())

        
        
    def fix_parameters(self, mass, value):
        try:
            val = int(value.get())
            m = str(mass.get())
        except ValueError:
            messagebox.showerror("Error", "Pas une bonne valeur")

        next_row = max([widget.grid_info()['row'] for widget in self.fix_parameters_widgets], default = 0)+1

        label_texte = tk.Label(self.root, text = m+f" : {val}", bg = "#f0f0f0")
        
        if m not in self.param_mass:
    
            self.stock_param[m] = self.label_param
            remove_button = tk.Button(self.root, text = "remove", fg = 'white',bg = '#850606', relief = 'raised', command = lambda: self.remove_param(m))
            label_texte.grid(row = 5+self.stock_param[m], column = 2, padx=5, pady=5, sticky = "ew")
            self.param_enlever.append(5+self.stock_param[m])
            remove_button.grid(row = 5+self.stock_param[m], column = 3, padx=5, pady=5, sticky = "ew")
            self.fix_parameters_widgets.append(remove_button)
            self.label_param+=1
        elif m in self.param_mass:
            label_texte.grid(row = 5+self.stock_param[m], column = 2, padx=5, pady=5, sticky = "ew")
        self.fix_parameters_widgets.append(label_texte)
        self.param_mass[str(mass.get())] = int(value.get())
        print(self.param_mass)
        
        
    def submit_data(self, index, entry_min, entry_max, entry_step, entry_name):
        param_min = int(entry_min.get())
        param_max = int(entry_max.get())
        param_step = int(entry_step.get())
        param_name = entry_name

        ok, name_ok = verif.verification_input(entry_name, [param_min, param_max, param_step])

        if ok:
            messagebox.showerror("Error", name_ok)
            return

        self.parameters[param_name] = (param_min, param_max, param_step)
        # if index == 0:
        #     self.parameters["M1(MX)"] = (param_min, param_max, param_step)
        # if index == 1:
        #     self.parameters["M2(MX)"] = (param_min, param_max, param_step)
        # if index == 2:
        #     self.parameters["mu(MX)"] = (param_min, param_max, param_step)
        res = ' '
        for item in self.parameters:
            res += item +str(self.parameters[item])

        label = tk.Label(self.root, text=res, font = ('Arial', 10), bg = "#f0f0f0")
        label.grid(row=1, column = 1, padx=5, pady=5, sticky = "ew", columnspan = 2)
        self.param_enlever.append(1)
        self.fix_parameters_widgets.append(label)
        print(self.parameters)


    def generate_output(self):
        # Votre fonction de génération de fichiers de sortie doit être appelée ici.
        # Par exemple:
        #result = input_generator()
        input_generator.inputs_generator(self.parameters, self.param_mass)
        result = True
        if result:
            messagebox.showinfo("Success", "Output generated successfully.")
        else:
            messagebox.showerror("Error", "An error occurred while generating the output.")

    def masses(self):
        app_mass.MassWindows(self)
        #masses.plot_masses(self.parameters, self.param_mass)

    def mix(self):
        app_mix.MixingWindows(self)
        #masses.plot_masses(self.parameters, self.param_mass)

    def remove_all(self):
        remove.remove_files()
    
    def remove_param(self, m):
        try:
            self.param_mass.pop(m)
        except KeyError:
            print("not here ")
        widget_to_destroy = [widget for widget in self.fix_parameters_widgets if widget.grid_info()['row'] == 5+self.stock_param[m]]
        for widget in widget_to_destroy:
            widget.destroy()
            self.fix_parameters_widgets.remove(widget)
        self.label_param = 0
    def restart(self):
        self.parameters.clear()
        self.param_mass.clear()

        for i in self.param_enlever:
            widget_to_destroy = [widget for widget in self.fix_parameters_widgets if widget.grid_info()['row'] == i]
            for widget in widget_to_destroy:
                widget.destroy()
                self.fix_parameters_widgets.remove(widget)

        
    def debug(self):
        self.parameters['M_2(MX)'] = (100,1500,100)
        self.parameters['M_1(MX)'] = (100,1500,100)
        self.param_mass['mu(MX)'] = 800

def main():
    root = tk.Tk()
    app = SoftsusyApp(root)
    #app.create_widgets()
    root.mainloop()

if __name__ == "__main__":
    main()