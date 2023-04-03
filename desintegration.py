import are_files
import numpy as np
import pyslha
import pandas as pd
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display
from matplotlib.widgets import Slider
import os

particle_names = {
    1: "d",
    2: "u",
    3: "s",
    4: "c",
    5: "b",
    6: "t",
    11: "e-",
    12: "nu_e",
    13: "mu-",
    14: "nu_mu",
    15: "tau-",
    16: "nu_tau",
    21: "g",
    22: "gamma",
    23: "Z",
    24: "W+",
    25: "h0",
    35: "H0",
    36: "A0",
    37: "H+",
    1000001: "~d_L",
    1000002: "~u_L",
    1000003: "~s_L",
    1000004: "~c_L",
    1000005: "~b_1",
    1000006: "~t_1",
    1000011: "~e_L",
    1000012: "~nu_eL",
    1000013: "~mu_L",
    1000014: "~nu_muL",
    1000015: "~tau_1",
    1000016: "~nu_tauL",
    1000021: "~g",
    1000022: "~chi_10",
    1000023: "~chi_20",
    1000024: "~chi_1+",
    1000025: "~chi_30",
    1000035: "~chi_40",
    1000037: "~chi_2+",
    2000001: "~d_R",
    2000002: "~u_R",
    2000003: "~s_R",
    2000004: "~c_R",
    2000005: "~b_2",
    2000006: "~t_2",
    2000011: "~e_R",
    2000013: "~mu_R",
    2000015: "~tau_2",
    1000016: "~nu_tauL",
    1000021: "~g",
    1000022: "~chi_10",
    1000023: "~chi_20",
    1000024: "~chi_1+",
    1000025: "~chi_30",
    1000035: "~chi_40",
    1000037: "~chi_2+",
    2000001: "~d_R",
    2000002: "~u_R",
    2000003: "~s_R",
    2000004: "~c_R",
    2000005: "~b_2",
    2000006: "~t_2",
    2000011: "~e_R",
    2000013: "~mu_R",
    2000015: "~tau_2",
    -1000001: "~d_L*",
    -1000002: "~u_L*",
    -1000003: "~s_L*",
    -1000004: "~c_L*",
    -1000005: "~b_1*",
    -1000006: "~t_1*",
    -1000011: "~e_L*",
    -1000012: "~nu_eL*",
    -1000013: "~mu_L*",
    -1000014: "~nu_muL*",
    -1000015: "~tau_1*",
    -1000016: "~nu_tauL*",
    -1000021: "~g*",
    -1000022: "~chi_10*",
    -1000023: "~chi_20*",
    -1000024: "~chi_1-",
    -1000025: "~chi_30*",
    -1000035: "~chi_40*",
    -1000037: "~chi_2-",
    -2000001: "~d_R*",
    -2000002: "~u_R*",
    -2000003: "~s_R*",
    -2000004: "~c_R*",
    -2000005: "~b_2*"
}

def extract_m1_m2_mu(file_path):
     
     data = pyslha.read(file_path)

     m1 = data.blocks['EXTPAR'][1]
     m2 = data.blocks['EXTPAR'][2]
     mu = data.blocks['EXTPAR'][23]

     result = {
          'M_1(MX)': m1,
          'M_2(MX)': m2,
          'mu(MX)' : mu
     }

     return result

def slha_to_dataframe_desin(slha_file):
    data = pyslha.read(slha_file)
	
    decay_data = []

    for particle_id, particle_info in data.decays.items():
        if particle_id in (-1000024, 1000024, -1000037, 1000037, 1000022, 1000023, 1000025, 1000035):
            for decay in particle_info.decays:
                decay_data.append({
				    'particle_id': particle_id,
				    'branching_ratio' : decay.br,
				    'decay_products': tuple(sorted(decay.ids))
                })
			    
    df = pd.DataFrame(decay_data, columns = ['particle_id', 'branching_ratio', 'decay_products'])

    return df

def slha_to_dataframe_mass(slha_file):
	data = pyslha.readSLHAFile(slha_file)
	mass_dict = data.blocks["MASS"].entries
	
	particle_data = {}
	for pid,mass in mass_dict.items():
		name = particle_names.get(pid, f"Unknown ({pid})")
		particle_data[name] = {'mass': mass, 'pid': pid}

	df = pd.DataFrame.from_dict(particle_data, orient='index')
	return df

def extract_mixing_matrices(file_path):
     
     data = pyslha.read(file_path)

     nmix = data.blocks['NMIX']
     umix = data.blocks['UMIX']

     return nmix, umix

def slha_to_dataframe_mod(file_path, particle_type):
     
    data = pyslha.read(file_path)

    if particle_type == 'neutralino':
         particle_ids = [1000023, 1000025, 1000035]
    elif particle_type == 'chargino':
         particle_ids = [1000024, 1000037]
    else:
         raise ValueError('Invalid particle_type')
    
    df_data = []
    for particle_id in particle_ids:
         decay_data = data.decays[particle_id]

    for decay in decay_data.decays:
         df_data.append({'decay_products' : tuple(sorted(decay.ids)), 'branching_ratio' : decay.br, 'particle_id' : particle_id})

    df = pd.DataFrame(df_data, columns = ['decay_products', 'branching_ratio', particle_id])
    return df

liste = are_files.are_output()
liste_df_desin = []
liste_df_mass = []
liste_input = []
for i in liste:
    liste_df_desin.append(slha_to_dataframe_desin(i))
    liste_df_mass.append(slha_to_dataframe_mass(i))
    liste_input.append(extract_m1_m2_mu(i))


def plot_branching_ratios(neutralino_df, chargino_df, nmix, umix):
    fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)

    for ax, df, mix_matrix, title in zip(axes, [neutralino_df, chargino_df], [nmix, umix], ['Neutralinos', 'Charginos']):
        decay_products = df['decay_products'].unique()
        num_decay_products = len(decay_products)

        if num_decay_products == 0:
            print("Aucun produit de désintégration trouvé. Le graphique ne peut pas être généré.")
            return

        bar_width = 0.8 / num_decay_products
        bar_positions = np.arange(len(mix_matrix))

        for i, decay_product in enumerate(decay_products):
            mask = df['decay_products'] == decay_product
            branching_ratios = df[mask]['branching_ratio'].values
            
            if len(branching_ratios) != len(mix_matrix):
                branching_ratios = np.pad(branching_ratios, (0, len(mix_matrix) - len(branching_ratios)), 'constant', constant_values=(0, 0))

            ax.bar(bar_positions + i * bar_width, branching_ratios, width=bar_width, label=str(decay_product))

        ax.set_xticks(bar_positions + 0.5 * (num_decay_products - 1) * bar_width)
        ax.set_xticklabels(['{:.2f}'.format(val) for val in bar_positions])
        ax.set_xlabel('Mixing Parameter')
        ax.set_ylabel('Branching Ratio')
        ax.set_title(title)
        ax.legend()

    plt.show()
     


# file_path = liste[0]

# df = slha_to_dataframe_desin(file_path)

# neutralino_df = slha_to_dataframe_mod(file_path, 'neutralino')
# chargino_df = slha_to_dataframe_mod(file_path, 'chargino')
# nmix, umix = extract_mixing_matrices(file_path)

# plot_branching_ratios(neutralino_df, chargino_df, nmix, umix)

def plot_branching_ratios_on_ax(ax_neutralino, ax_chargino, neutralino_df, chargino_df, title_neutralino, title_chargino):
    # Neutralinos
    decay_products_neutralino = neutralino_df['decay_products'].unique()
    num_decay_products_neutralino = len(decay_products_neutralino)
    bar_positions_neutralino = np.arange(num_decay_products_neutralino)

    for i, decay_product in enumerate(decay_products_neutralino):
        ax_neutralino.bar(bar_positions_neutralino[i], neutralino_df[neutralino_df['decay_products'] == decay_product]['branching_ratio'].mean(), label=decay_product)

    ax_neutralino.set_xticks(bar_positions_neutralino)
    ax_neutralino.set_xticklabels(decay_products_neutralino, rotation=45, ha='right')
    ax_neutralino.set_ylabel('Branching Ratio')
    ax_neutralino.set_title(title_neutralino)
    ax_neutralino.legend()

    # Charginos
    decay_products_chargino = chargino_df['decay_products'].unique()
    num_decay_products_chargino = len(decay_products_chargino)
    bar_positions_chargino = np.arange(num_decay_products_chargino)

    for i, decay_product in enumerate(decay_products_chargino):
        ax_chargino.bar(bar_positions_chargino[i], chargino_df[chargino_df['decay_products'] == decay_product]['branching_ratio'].mean(), label=decay_product)

    ax_chargino.set_xticks(bar_positions_chargino)
    ax_chargino.set_xticklabels(decay_products_chargino, rotation=45, ha='right')
    ax_chargino.set_ylabel('Branching Ratio')
    ax_chargino.set_title(title_chargino)
    ax_chargino.legend()

def plot_mixing_and_branching_ratios(nmix, umix, neutralino_df, chargino_df):
     fig, axes = plt.subplots(1,3, figsize = (12,6), sharey = False)

     im1 = axes[0].imshow(nmix, cmap = 'viridis', vmin = 0, vmax = 1)
     axes[0].set_title('Neutralino Mixing Matrice')
     fig.colorbar(im1, ax = axes[0])

     plot_branching_ratios_on_ax(neutralino_df, chargino_df, nmix, umix, ax=axes[1])
     #plt.show()

def plot_mixing_matrix_on_ax(ax, mixing_matrix, title):
    im = ax.imshow(mixing_matrix, cmap='viridis', vmin=-1, vmax=1)
    ax.figure.colorbar(im, ax=ax)
    
    # Affichez les valeurs de la matrice de mixage dans chaque cellule
    for i in range(mixing_matrix.shape[0]):
        for j in range(mixing_matrix.shape[1]):
            ax.text(j, i, f"{mixing_matrix[i, j]:.2f}", ha="center", va="center", color="w" if mixing_matrix[i, j] > 0.5 else "k")

    ax.set_xticks(np.arange(mixing_matrix.shape[1]))
    ax.set_yticks(np.arange(mixing_matrix.shape[0]))
    ax.set_xticklabels([f"{i+1}" for i in range(mixing_matrix.shape[1])])
    ax.set_yticklabels([f"{i+1}" for i in range(mixing_matrix.shape[0])])
    
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")
    ax.set_title(title)
    
def update_graph(m1_value, m2_value, mu_value, tan_beta_value):
    nmix, umix, neutralino_df, chargino_df = load_data_from_files(m1_value, m2_value, mu_value, tan_beta_value)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 12))

    plot_mixing_matrix_on_ax(ax1, nmix, "Neutralino Mixing Matrix")
    plot_mixing_matrix_on_ax(ax2, umix, "Chargino Mixing Matrix")
    plot_branching_ratios_on_ax(ax3, ax4, neutralino_df, chargino_df, "Neutralino Decay Branching Ratios", "Chargino Decay Branching Ratios")

    plt.tight_layout()
    plt.show()

def zplot_branching_ratios_on_ax(neutralino_df, chargino_df, nmix, umix, ax=None):
    
    if ax is None:
         fig,ax = plt.subplots()
     
    for df, mix_matrix, title in zip([neutralino_df, chargino_df], [nmix, umix], ['Neutralinos', 'Charginos']):
        decay_products = df['decay_products'].unique()
        num_decay_products = len(decay_products)
          
        if num_decay_products == 0:
             print('rien')
             return
        
        bar_width = 0.8/num_decay_products

        bar_positions = np.arange(len(mix_matrix))

        for i, decay_product in enumerate(decay_products):
             mask = df['decay_products'] == decay_product
             branching_ratios = df[mask]['branching_ratio'].values
             if len(branching_ratios) != len(mix_matrix):
                  branching_ratios = np.pad(branching_ratios, (0,len(mix_matrix)-len(branching_ratios)), 'constant', constant_values = (0,0))
               
             ax.bar(bar_positions+i*bar_width, branching_ratios, width= bar_width, label=str(decay_product))

        ax.set_xticks(bar_positions+0.5*(num_decay_products-1)*bar_width)
        ax.set_xticklabels([':.2f'.format(val) for val in bar_positions])
        ax.set_xlabel('Mixing parameter')
        ax.set_ylabel('Branching_ratio')
        ax.set_title(title)
        ax.legend()

def zupdate_graph(m1_value, m2_value, mu_value, tan_beta_value):
     
     nmix, umix, neutralino_df, chargino_df = load_data_from_files(m1_value, m2_value,mu_value, tan_beta_value)
     
     plot_mixing_and_branching_ratios(nmix, umix, neutralino_df, chargino_df)
     

def load_data_from_files(m1_value, m2_value, mu_value, tan_beta_value):
     
     filename = get_filename(m1_value, m2_value, mu_value, tan_beta_value)

     if filename != None:
          data = pyslha.read(filename)
     else:
          return

     neutralino_df = slha_to_dataframe_mod(filename, particle_type = 'neutralino')
     chargino_df = slha_to_dataframe_mod(filename, particle_type = 'chargino')

     nmix = np.zeros((4,4))
     umix = np.zeros((2,2))

     for i in range(1,5):
          for j in range(1,5):
               if (i,j) in data.blocks['NMIX']:
                    nmix[i-1, j-1] = data.blocks['NMIX'][i,j]

     for i in range(1,3):
          for j in range(1,3):
               if (i,j) in data.blocks['UMIX']:
                    umix[i-1,j-1] = data.blocks['UMIX'][i,j]

     return nmix, umix, neutralino_df, chargino_df

def get_filename(m1_value, m2_value, mu_value, tan_beta_value, folder = 'output_dir'):
     
     for root, dirs, files in os.walk(folder):
          for file in files:
               if file.endswith('.slha'):
                    filepath = os.path.join(root, file)
                    try:
                         data = pyslha.read(filepath)
                    except Exception as e:
                         print(f"Erreur lors de la lecture du fichier {filepath}: {str(e)}")
                         continue
                    # if 'EXTPAR' not in data.blocks.keys():
                    #      #print('EXTPAR' not in data.blocks.keys())
                    #      continue
                    
                    extpar = data.blocks['EXTPAR']
                    m1 = extpar.get(1, None)
                    m2 = extpar.get(2, None)
                    mu = extpar.get(23, None)
                    tan_beta = extpar.get(25, None)
                    if (m1 == m1_value and m2 == m2_value and mu == mu_value and tan_beta == tan_beta_value):
                         return filepath
                    
     return None
          
m1_slider = widgets.FloatSlider(min = 100, max=1500, step = 100, value = 100, description = 'M_1(MX)')
m2_slider = widgets.FloatSlider(min = 100, max=1500, step = 100, value = 200, description = 'M_2(MX)')
mu_slider = widgets.FloatSlider(min = 100, max=1500, step = 100, value = 800, description = 'mu(MX)')
tan_beta_slider = widgets.FloatSlider(min = 0, max=50, step = 0.1, value = 10, description = 'tan(beta)')

interactive_plot = widgets.interactive(
     update_graph,
     m1_value = m1_slider,
     m2_value = m2_slider,
     mu_value = mu_slider,
     tan_beta_value = tan_beta_slider
)

display(widgets.HBox([m1_slider, m2_slider, mu_slider, tan_beta_slider]))

display(interactive_plot.children[-1])

plt.show()

