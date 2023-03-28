import pyslha
import math
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import concurrent.futures
import are_files

def slha_to_dataframe(slha_file):
    data = pyslha.readSLHAFile(slha_file)
    mixing_dict = data.blocks["NMIX"].entries
    particle_data = {}

    for pid,mixing in mixing_dict.items():
        particle_data[(pid)] = math.fabs(mixing)
    #print(particle_data)
    df = pd.DataFrame(list(particle_data.items()), columns = ['Coordinates', 'Mixing'])
    df[['x', 'y']] = pd.DataFrame(df['Coordinates'].tolist(), index=df.index)
    df = df.drop('Coordinates', axis = 1).set_index(['x', 'y']).sort_index(ascending = False)
    return df

#output_filename = f"output_dir/output_m1_{1500}_m2_{100}_mu_{800}.slha"

#df = slha_to_dataframe(output_filename)

def transform_to_matrix(df):
    return df.unstack().values

def colormap_mixing(df,matrix):
    _ = plt.imshow(matrix, cmap = 'cividis', origin = 'upper', extent = [0,len(matrix[0]), len(matrix),0 ])
    __ = plt.colorbar(_,label = 'Mixing Value')

    plt.xticks(range(len(matrix[0])), df.index.levels[0])
    plt.yticks(range(len(matrix[1])), df.index.levels[1])
    plt.xlabel('Neutralino mixing (1,2,3,4)')
    plt.ylabel('Neutralino mixing (1,2,3,4)')
    plt.title('Colormap of Mixing Value')

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix[i,j]
            plt.text(j+0.5, i+0.5, f"{value:.2f}", ha = "center", va = "center", color = 'w', fontsize = 12)
    plt.show()

def draw(df,ax):
    matrix = df.unstack().values
    #fig,ax = plt.subplots()

    _ = plt.imshow(matrix, cmap = 'cividis', origin = 'upper', extent = [0,len(matrix[0]), len(matrix),0 ])
    __ = plt.colorbar(_,label = 'Mixing Value')

    plt.xticks(range(len(matrix[0])), df.index.levels[0])
    plt.yticks(range(len(matrix[1])), df.index.levels[1])
    plt.xlabel('Neutralino mixing (1,2,3,4)')
    plt.ylabel('Neutralino mixing (1,2,3,4)')
    plt.title('Colormap of Mixing Value')

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            value = matrix[i,j]
            plt.text(j+0.5, i+0.5, f"{value:.2f}", ha = "center", va = "center", color = 'w', fontsize = 12)
            plt.text(j+0.5, i+0.2, str((i+1,j+1)), ha = "center", va = "center", color = 'w', fontsize = 8)
    plt.show()
    #print(df.head())

def plot(param,ax):
    output_list = are_files.are_output()
    param_list = list(param.keys())

    liste_mass = []
    liste_input = []
    options = ["M_1(MX)", "M_2(MX)", "mu(MX)", "tan(beta)"]
    output_interest_list = []
    M1 = []
    M2 = []
    mu = []

    for file in output_list:
        # temp = file.split('m1_')
        # temp2 = temp[1].split('_m2_')
        # temp3 = temp2[1].split('_mu_')
        # temp4 = temp3[1].split('.')

        dict_file = are_files.file_infos(file, options)
        elements = list(dict_file.keys())
        # for option in options:
        #     if option in param_list:
        #         a=1= are_files.file_infos(file, options)
        # for option in options:
        #     if option in param_list:
        #         a=1
        bad = False
        for elem in param_list:
            if elem in elements:
                #print(float(dict_file[elem]),float(param_mass[elem]))
                if float(dict_file[elem]) != float(param[elem]):
                    bad = True
        if bad:
            continue

        df = slha_to_dataframe(file)

        draw(df,ax)