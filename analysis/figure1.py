import os
import pyslha
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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
    liste_N2_ff = []
    liste_N2_h = []
    liste_N2_Z = []
    liste_C1_ff = []
    liste_C1_W = []
    
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
        
        for particle_id, particle_info in data.decays.items():
            if particle_id ==1000023:
                fermion_br = 0
                h_br = 0
                z_br = 0
                for decay in particle_info.decays:
                    if 25 in decay.ids and 1000022 in decay.ids:
                        h_br+=decay.br
                    if 23 in decay.ids and 1000022 in decay.ids:
                        z_br+=decay.br
                    if 23 not in decay.ids and 25 not in decay.ids:
                        if 1000022 in decay.ids:
                            fermion_br+=decay.br
                            z_br+=decay.br

                liste_N2_ff.append(fermion_br)
                liste_N2_h.append(h_br)
                liste_N2_Z.append(z_br)
            
            if particle_id ==1000024:
                f_br = 0
                w_br = 0
                for decay in particle_info.decays:
                    if (24 in decay.ids or -24 in decay.ids) and 1000022 in decay.ids:
                        w_br+=decay.br
                    if 24 not in decay.ids and -24 not in decay.ids:
                        if 1000022 in decay.ids:
                            f_br+=decay.br
                liste_C1_ff.append(f_br)
                liste_C1_W.append(w_br)
            # if particle_id in (-1000024, 1000024, 1000023):
            #     for decay in particle_info.decays:
            #         decay_data.append({
            #             'M_1' : m1,
            #             'M_2' : m2,
            #             'mu' : mu,
            #             'particle_id': particle_id,
            #             'branching_ratio' : decay.br,
            #             'decay_products': tuple(sorted(decay.ids))
            #         })
                
    result = {
        'M_1' : liste_m1,
        'M_2' : liste_m2,
        'mu' : liste_mu,
        'Neut1' : liste_N1,
        'Neut2' : liste_N2,
        'Neut3' : liste_N3,
        'Char1' : liste_C1,
        'Char1' : liste_C2,
        'BR(N2->N1+Z)' : liste_N2_Z,
        'BR(N2->N1+h)' : liste_N2_h,
        'BR(N2->N1+ff)' : liste_N2_ff,
        'BR(C1->N1+ff)' : liste_C1_ff,
        'BR(C1->N1+W)' : liste_C1_W
    }


    return result

def extract_slha_2(folder_path):

    liste_path = os.listdir(folder_path)

    liste_m1 = []
    liste_m2 = []
    liste_mu = []
    liste_N1 = []
    liste_N2 = []
    liste_N3 = []
    liste_C1 = []
    liste_C2 = []
    liste_N3_ff = []
    liste_N3_N1_h = []
    liste_N3_N2_h = []
    liste_N3_N1_Z = []
    liste_N3_N2_Z = []
    liste_N3_W = []
    liste_C2_ff = []
    liste_C2__N1_W = []
    liste_C2__N2_W = []
    liste_C2_C1_Z = []
    liste_C2_C1_h = []
    
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
        
        for particle_id, particle_info in data.decays.items():
            if particle_id ==1000025:
                fermion_br = 0
                h_br = 0
                z_br = 0
                N2_h_br = 0
                N2_z_br = 0
                w_br = 0
                for decay in particle_info.decays:
                    if 25 in decay.ids and 1000022 in decay.ids:
                        h_br+=decay.br
                    if 23 in decay.ids and 1000022 in decay.ids:
                        z_br+=decay.br
                    if 25 in decay.ids and 1000023 in decay.ids:
                        N2_h_br+=decay.br
                    if 23 in decay.ids and 1000023 in decay.ids:
                        N2_z_br+=decay.br
                    if (24 in decay.ids or -24 in decay.ids) and (1000024 in decay.ids or -1000024 in decay.ids):
                        w_br += decay.br
                    
                    if 23 not in decay.ids and 25 not in decay.ids:
                        if 1000022 in decay.ids:
                            fermion_br+=decay.br

                liste_N3_ff.append(fermion_br)
                liste_N3_N1_h.append(h_br)
                liste_N3_N1_Z.append(z_br)
                liste_N3_N2_h.append(N2_h_br)
                liste_N3_N2_Z.append(N2_z_br)
                liste_N3_W.append(w_br)
            
            if particle_id ==1000037:
                f_br = 0
                N1w_br = 0
                N2w_br = 0
                C1z_br = 0
                C1h_br = 0
                for decay in particle_info.decays:
                    if (24 in decay.ids or -24 in decay.ids) and 1000022 in decay.ids:
                        N1w_br+=decay.br
                    if (24 in decay.ids or -24 in decay.ids) and 1000023 in decay.ids:
                        N2w_br+=decay.br
                    if 23 in decay.ids and ((1000024 in decay.ids) or (-1000024 in decay.ids)):
                        C1z_br+=decay.br
                    if 25 in decay.ids and ((1000024 in decay.ids) or (-1000024 in decay.ids)):
                        C1h_br+=decay.br
                    if 24 not in decay.ids and -24 not in decay.ids:
                        if 1000022 in decay.ids:
                            f_br+=decay.br
                liste_C2_ff.append(f_br)
                liste_C2__N1_W.append(N1w_br)
                liste_C2__N2_W.append(N2w_br)
                liste_C2_C1_Z.append(C1z_br)
                liste_C2_C1_h.append(C1h_br)
            # if particle_id in (-1000024, 1000024, 1000023):
            #     for decay in particle_info.decays:
            #         decay_data.append({
            #             'M_1' : m1,
            #             'M_2' : m2,
            #             'mu' : mu,
            #             'particle_id': particle_id,
            #             'branching_ratio' : decay.br,
            #             'decay_products': tuple(sorted(decay.ids))
            #         })
                
    result = {
        'M_1' : liste_m1,
        'M_2' : liste_m2,
        'mu' : liste_mu,
        'Neut1' : liste_N1,
        'Neut2' : liste_N2,
        'Neut3' : liste_N3,
        'Char1' : liste_C1,
        'Char1' : liste_C2,
        'BR(N3->N1+Z)' : liste_N3_N1_Z,
        'BR(N3->N1+h)' : liste_N3_N1_h,
        'BR(N3->N2+Z)' : liste_N3_N2_Z,
        'BR(N3->N2+h)' : liste_N3_N2_h,
        'BR(N3->C1+W)' : liste_N3_W,
        'BR(N3->N1+ff)' : liste_N3_ff,
        'BR(C2->N1+ff)' : liste_C2_ff,
        'BR(C2->N1+W)' : liste_C2__N1_W,
        'BR(C2->N2+W)' : liste_C2__N2_W,
        'BR(C2->C1+Z)' : liste_C2_C1_Z,
        'BR(C2->C1+h)' : liste_C2_C1_h
    }


    return result

#extract_slha_2("M2from0to1200M12000mu100")
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

    sorted_columns = sorted(df.columns, key=lambda col: min([particle_weight(str(pid)) for pid in col]))
    sorted_latex_columns = [latex_decay_products_to_names(str(col)) for col in sorted_columns]
    df.columns = [latex_decay_products_to_names(str(col)) for col in sorted_columns]
    print(sorted_columns)

    moitie = len(sorted_columns) // 2
    colormap_viridis = plt.cm.Set1
    colormap_jet = plt.cm.viridis

    couleurs_viridis = [colormap_viridis(i) for i in np.linspace(0, 1, moitie)]
    couleurs_jet = [colormap_jet(i) for i in np.linspace(0, 1, len(sorted_columns) - moitie)]


    couleurs = couleurs_viridis + couleurs_jet
    couleurs_vives = [
    "#FF0000",  # Rouge
    "#00FF00",  # Vert
    "#0000FF",  # Bleu
    "#FFFF00",  # Jaune
    "#FF00FF",  # Magenta
    "#00FFFF",  # Cyan
    "#FF4500",  # Orange
    "#8A2BE2",  # Bleu-violet
    "#7FFF00",  # Vert chartreuse
    "#D2691E",  # Chocolat
    "#DC143C",  # Cramoisi
    "#00FA9A",  # Vert moyen printemps
    "#FF69B4",  # Rose vif
    "#8B008B",  # Magenta foncé
    "#1E90FF",  # Bleu Dodger
    "#FFD700",  # Or
    "#4B0082",  # Indigo
    "#FF4500",  # Orange-rouge
    "#2E8B57",  # Vert de mer
    "#ADFF2F",  # Vert jaune
    "#32CD32",  # Vert lime
    "#FA8072",  # Saumon
    "#6A5ACD",  # Bleu ardoise
    "#FFA500",  # Orange
    "#FF6347",  # Tomate
    "#3CB371",  # Vert menthe moyen
    "#F08080",  # Rose clair
    "#20B2AA",  # Vert clair de mer
    "#8B4513",  # Brun de selle
    "#B22222"   # Rouge brique
]
    couleurs =couleurs_vives
    fig = plt.figure(figsize=(14, 8))
    for i, column in enumerate(sorted_latex_columns):
        #print(np.array(df[column]).max(), f"${column[0]} {column[1]}$")
        if np.array(df[column]).max() < 0.05:
            continue
        if len(column) == 2:
            plt.plot(df.index, df[column], label=f"${column[0]}, {column[1]}$", color = couleurs[i])
        if len(column) == 3:
            plt.plot(df.index, df[column], label=f"${column[0]}, {column[1]}, {column[2]}$", color = couleurs[i])
    plt.text(10,0.9,f'$M_1 = {M1}$ GeV' + '\n'+r'$\tan\beta=$' +f'{tanb}' +f'\n $\\mu =$ {mu} GeV', fontsize=10, bbox=dict(facecolor='skyblue', alpha=0.5, edgecolor='black', boxstyle='round,pad=0.5'))
    plt.title(title, fontsize = 14)
    plt.xlabel('$M_2$ [GeV]', fontsize= 14)
    plt.ylabel('Branching ratio', fontsize= 14)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.tick_params(which='major', length=5, direction='in', bottom = True, top = True, left = True, right=True)
    plt.xlim(0,1200)
    plt.ylim(0,1.005)
    plt.show()

#extract_slha("M2from0to1200M15000mu1000and5000")


def particle_weight(decay_products):
    # Liste des particules dans l'ordre spécifié par l'utilisateur
    order = [1000022, 1000024, -1000024, 1000023]
    
    # Parcourir l'ordre pour trouver la particule correspondante
    for idx, particle in enumerate(order):
        if str(particle) in decay_products:
            return idx
    
    # Si aucune des particules n'est trouvée, retourner une valeur plus grande pour mettre à la fin
    return len(order)

def plot2(liste_plot,M2, M1, mu, tanb,liste_label,  title = '', linestyle = '-'):


    fig = plt.figure(figsize=(14, 8))
    for i, column in enumerate(liste_plot):

        plt.plot(M2, column, label=liste_label[i])

    plt.text(10,0.9,f'$M_1 = {M1}$ GeV' + '\n'+r'$\tan\beta=$' +f'{tanb}' +f'\n $\\mu =$ {mu} GeV', fontsize=10, bbox=dict(facecolor='skyblue', alpha=0.5, edgecolor='black', boxstyle='round,pad=0.5'))
    plt.title(title, fontsize = 14)
    plt.xlabel('$M_2$ [GeV]', fontsize= 14)
    plt.ylabel('Branching ratio', fontsize= 14)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.tick_params(which='major', length=5, direction='in', bottom = True, top = True, left = True, right=True)
    plt.xlim(99,1200)
    plt.ylim(0,1.005)
    plt.show()


def plot2_ATLAS_style(liste_plot, M2, M1, mu, tanb, liste_label, title='', linestyle='-', ncol=1, ylim = 1.005, yaxis = '', labelpos = 'upper right', textposx=0.7, textposy=0.9, save = ''):
    # Création de la figure
    fig, ax = plt.subplots(figsize=(8, 7))
    
    color_hot = ['red', 'orange', 'pink', 'firebrick']
    color_cold = ['blue','cyan', 'green', 'blueviolet', 'lime']
    
    W_color = ['blue', 'cyan']
    Z_color = ['green', 'line']
    h_color = ['red', 'orange']
    h_num = 0
    W_num = 0
    Z_num = 0
    # others_labels = liste_label
    dict_label = {'h' : 0,'Z':0, 'W' : 0}
    # Tracé des données
    for i, column in enumerate(liste_plot):
        
        
        # del(others_labels[i])
        if 'h+' in liste_label[i]:
            
            if dict_label['h'] ==1:
                ax.plot(M2, column, label=liste_label[i], linestyle='--', linewidth=2, color = dict_label['hcolor'])
            else:
                ax.plot(M2, column, label=liste_label[i], linestyle=linestyle, linewidth=2, color = h_color[h_num])
                dict_label['hcolor'] = h_color[h_num]
                h_num+=1
            
            dict_label['h'] = 1
        if 'W+' in liste_label[i]:
            print(liste_label[i])
            if dict_label['W'] ==1:
                ax.plot(M2, column, label=liste_label[i], linestyle='--', linewidth=2, color = dict_label['wcolor'])
                
            elif dict_label['W'] ==2:
                ax.plot(M2, column, label=liste_label[i], linestyle=':', linewidth=2, color = dict_label['wcolor'])
            elif dict_label['W'] ==3:
                ax.plot(M2, column, label=liste_label[i], linestyle='-.', linewidth=2, color = dict_label['wcolor'])
            else:
                ax.plot(M2, column, label=liste_label[i], linestyle=linestyle, linewidth=2, color = W_color[W_num])
                dict_label['wcolor'] = W_color[W_num]
                W_num+=1
                
            dict_label['W'] += 1
        if 'Z+' in liste_label[i]:
            
            if dict_label['Z'] ==1:
                ax.plot(M2, column, label=liste_label[i], linestyle='--', linewidth=2, color = dict_label['zcolor'])
            else:
                ax.plot(M2, column, label=liste_label[i], linestyle=linestyle, linewidth=2, color = Z_color[Z_num])
                dict_label['zcolor'] = Z_color[Z_num]
                Z_num+=1
            dict_label['Z'] = 1
            
        # if liste_label[i] in others_labels:
        #     ax.plot(M2, column, label=liste_label[i], linestyle=linestyle, linewidth=2, color = color_hot[hot])
        #     dict_label[color_hot[hot]
        # else:
        #     ax.plot(M2, column, label=liste_label[i], linestyle='--', linewidth=2, color = color_hot[hot])
        
        # if  r'\tilde{\chi}_1^\pm' in liste_label[i]:
            
        #     ax.plot(M2, column, label=liste_label[i], linestyle=linestyle, linewidth=2, color = color_hot[hot])
        #     hot+=1
        # else:
        #     ax.plot(M2, column, label=liste_label[i], linestyle=linestyle, linewidth=2, color = color_cold[cold])
        #     cold+=1
    
    
    
    # Ajout du label "ATLAS Work In Progress"
    #ax.text(0.42, 0.6, 'Work In Progress', transform=ax.transAxes, fontsize=16, verticalalignment='top', weight='bold', style='italic')
    
    # Titre et labels
    ax.set_title(title, fontsize=14, loc='right', pad=0)
    ax.text(0, 1.05, 'SOFTSUSY-4.1.19', transform=ax.transAxes, fontsize=14, verticalalignment='top', horizontalalignment='left')
    
    ax.set_xlabel('$M_2$ [GeV]', fontsize=16)
    ax.set_ylabel(f'BR({yaxis})', fontsize=16)
    
    # Légende avec un style spécifique
    leg = ax.legend(loc=labelpos, fontsize=12, frameon=True, edgecolor='black', handlelength=1.5, labelspacing=0.5, ncol=ncol)
    leg.get_frame().set_linewidth(1)
    
    # Grille, limites et autres réglages
    ax.grid(True, which='major', linestyle='--', linewidth=0.5)
    
    # leg_x = leg.get_window_extent().x0 / fig.dpi
    # leg_y = leg.get_window_extent().y1 / fig.dpi
    
    # Ajout du texte avec les paramètres
    ax.text(textposx, textposy, f'$M_1 = {M1}$ GeV\n$\\mu = {mu}$ GeV\n$tan \\, \\beta = {tanb}$', 
            transform=ax.transAxes, fontsize=14, verticalalignment='top', horizontalalignment='right', bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
    
    
    
    ax.set_xlim(100, 1200)
    ax.set_ylim(0, ylim)
    
    ax.set_yticks(np.arange(0, ylim, 0.2))  # Ticks majeurs tous les 200
    ax.set_yticks(np.arange(0, ylim, 0.05), minor=True)  # Ticks mineurs tous les 100

    ax.set_xticks(np.arange(200, 1201, 200))  # Ticks majeurs tous les 200
    ax.set_xticks(np.arange(100, 1201, 50), minor=True)  # Ticks mineurs tous les 100
    ax.tick_params(which='major', length=7, direction='in', bottom=True, top=True, left=True, right=True, labelsize=14)
    ax.tick_params(which='minor', length=4, direction='in', bottom=True, top=True, left=True, right=True)
    
    # Affichage de la figure
    plt.tight_layout()
    plt.savefig(f"{save}.png",facecolor='white', transparent=False)
    plt.show()
    
    
def plot2_ATLAS_style_double(liste_plot,liste_plot2, M2, M1, mu,mu2, tanb, liste_label, title='', linestyle='-', ncol=1, ylim = 1.005, yaxis = '', labelpos = 'upper right', textposx=0.7, textposy=0.9, save = ''):
    # Création de la figure
    fig, ax = plt.subplots(figsize=(8, 7))
    color_hot = ['red', 'orange', 'pink', 'firebrick']
    color_cold = ['blue','cyan', 'green', 'blueviolet', 'lime']
    hot = 0
    cold = 0
    # Tracé des données
    for i, column in enumerate(liste_plot):
        if  r'\tilde{\chi}_1^\pm' in liste_label[i]:
            
            ax.plot(M2, column, label=liste_label[i], linestyle=linestyle, linewidth=2, color = color_hot[hot])
            hot+=1
        else:
            ax.plot(M2, column, label=liste_label[i], linestyle=linestyle, linewidth=2, color = color_cold[cold])
            cold+=1
    hot = 0
    cold = 0
    
    for i, column in enumerate(liste_plot2):
        if  r'\tilde{\chi}_1^\pm' in liste_label[i]:
            
            ax.plot(M2, column, linestyle='--', linewidth=2, color = color_hot[hot])
            hot+=1
        else:
            ax.plot(M2, column, linestyle='--', linewidth=2, color = color_cold[cold])
            cold+=1
    
    # Ajout du label "ATLAS Work In Progress"
    #ax.text(0.42, 0.6, 'Work In Progress', transform=ax.transAxes, fontsize=16, verticalalignment='top', weight='bold', style='italic')
    
    # Titre et labels
    ax.set_title(title, fontsize=14, loc='right', pad=0)
    ax.text(0, 1.05, 'SOFTSUSY-4.1.19', transform=ax.transAxes, fontsize=14, verticalalignment='top', horizontalalignment='left')
    
    ax.set_xlabel('$M_2$ [GeV]', fontsize=16)
    ax.set_ylabel(f'BR({yaxis})', fontsize=16)
    
    # Légende avec un style spécifique
    leg = ax.legend(loc=labelpos, fontsize=12, frameon=True, edgecolor='black', handlelength=1.5, labelspacing=0.5, ncol=ncol)
    leg.get_frame().set_linewidth(1)
    
    # Grille, limites et autres réglages
    ax.grid(True, which='major', linestyle='--', linewidth=0.5)
    
    # leg_x = leg.get_window_extent().x0 / fig.dpi
    # leg_y = leg.get_window_extent().y1 / fig.dpi
    
    # Ajout du texte avec les paramètres
    ax.text(textposx, textposy, f'$M_1 = {M1}$ GeV\n$\\mu = {mu}$ GeV (solid)\n$\\mu = {mu2}$ GeV (dashed)\n$tan \\, \\beta = {tanb}$', 
            transform=ax.transAxes, fontsize=14, verticalalignment='top', horizontalalignment='right', bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
    
    
    
    ax.set_xlim(100, 1200)
    ax.set_ylim(0, ylim)
    
    ax.set_yticks(np.arange(0, ylim, 0.2))  # Ticks majeurs tous les 200
    ax.set_yticks(np.arange(0, ylim, 0.05), minor=True)  # Ticks mineurs tous les 100

    ax.set_xticks(np.arange(200, 1201, 200))  # Ticks majeurs tous les 200
    ax.set_xticks(np.arange(100, 1201, 50), minor=True)  # Ticks mineurs tous les 100
    ax.tick_params(which='major', length=7, direction='in', bottom=True, top=True, left=True, right=True, labelsize=14)
    ax.tick_params(which='minor', length=4, direction='in', bottom=True, top=True, left=True, right=True)
    
    # Affichage de la figure
    plt.tight_layout()
    plt.savefig(f"{save}.png",facecolor='white', transparent=False)
    plt.show()