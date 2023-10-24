import os
import pyslha
import pandas as pd
import matplotlib.pyplot as plt

def extract_slha(folder_path):

    liste_path = os.listdir(folder_path)

    liste_m1 = []
    liste_m2 = []
    liste_mu = []
    liste_N1 = []
    liste_N2 = []
    liste_N3 = []
    liste_C1 = []
    liste_C2 = []

    for slha in liste_path:
        data = pyslha.read(f'{folder_path}/' +slha)

        liste_m1.append(data.blocks['EXTPAR'][1])
        liste_m2.append(data.blocks['EXTPAR'][2])
        liste_mu.append(data.blocks['EXTPAR'][23])
        liste_N1.append(data.blocks['MASS'][1000022])
        liste_N2.append(data.blocks['MASS'][1000023])
        liste_N3.append(data.blocks['MASS'][1000025])
        liste_C1.append(data.blocks['MASS'][1000024])
        liste_C2.append(data.blocks['MASS'][1000037])

    result = {
        'M_1' : liste_m1,
        'M_2' : liste_m2,
        'mu' : liste_mu,
        'Neut1' : liste_N1,
        'Neut2' : liste_N2,
        'Neut3' : liste_N3,
        'Char1' : liste_C1,
        'Char1' : liste_C2,
    }

    return result

def slha_to_dataframe_desin(slha_file):
    data = pyslha.read(slha_file)
    m1 = data.blocks['EXTPAR'][1]
    m2 = data.blocks['EXTPAR'][2]
    mu = data.blocks['EXTPAR'][23]
    decay_data = []

    for particle_id, particle_info in data.decays.items():
        if particle_id in (-1000024, 1000024, -1000037, 1000037, 1000022, 1000023, 1000025, 1000035):
            for decay in particle_info.decays:
                decay_data.append({
                    'M_1' : m1,
                    'M_2' : m2,
                    'mu' : mu,
				    'particle_id': particle_id,
				    'branching_ratio' : decay.br,
				    'decay_products': tuple(sorted(decay.ids))
                })
			    
    df = pd.DataFrame(decay_data, columns = ['M_1', 'M_2', 'mu', 'particle_id', 'branching_ratio', 'decay_products'])

    return df

def slha_folder(slha_folder):
    liste = os.listdir(slha_folder)
    df = slha_to_dataframe_desin(slha_folder+'/' +liste[0])
    for slha in liste[1:]:
        slha_path = slha_folder+'/'+slha
        df = pd.concat([df, slha_to_dataframe_desin(slha_path)], ignore_index=True)

    return df

# dicto = slha_to_dataframe_desin('output_dir/outputM_1100M_20mu1000.slha')

# it = slha_folder('output_dir')

# print(it.head())

from particle_name import particles_names
particles_name = particles_names()

def latex_decay_products_to_names(decay_tuple_str):
    return tuple(particles_name.get(int(pid.strip()), pid.strip()) for pid in decay_tuple_str.strip('()').split(','))

def plot(df2, M1, mu, tanb, title = '', linestyle = '-'):
    df = df2.copy(deep = True)
    df.columns = [latex_decay_products_to_names(str(col)) for col in df.columns]
    fig = plt.figure(figsize=(14, 8))
    for column in df.columns:
        if len(column) == 2:
            plt.plot(df.index, df[column], label=f"${column[0]}, {column[1]}$")
        if len(column) == 3:
            plt.plot(df.index, df[column], label=f"${column[0]}, {column[1]}, {column[2]}$")
    plt.text(10,0.9,f'$M_1 = {M1}$ GeV' + '\n'+r'$\tan\beta=$' +f'{tanb}' +f'\n \\mu = {mu} GeV', fontsize=10, bbox=dict(facecolor='skyblue', alpha=0.5, edgecolor='black', boxstyle='round,pad=0.5'))
    plt.title(title, fontsize = 14)
    plt.xlabel('$M_2$ [GeV]', fontsize= 14)
    plt.ylabel('Branching ratio', fontsize= 14)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.tick_params(which='major', length=5, direction='in', bottom = True, top = True, left = True, right=True)
    plt.xlim(0,1200)
    plt.ylim(0,1)
    plt.show()

#extract_slha("M2from0to1200M15000mu1000and5000")
