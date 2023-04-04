import pyslha
import math
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import concurrent.futures
import are_files
import numpy as np
from scipy.interpolate import griddata

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


def slha_to_dataframe(slha_file):
	data = pyslha.readSLHAFile(slha_file)
	mass_dict = data.blocks["MASS"].entries
	
	particle_data = {}
	for pid,mass in mass_dict.items():
		name = particle_names.get(pid, f"Unknown ({pid})")
		particle_data[name] = {'mass': mass, 'pid': pid}

	df = pd.DataFrame.from_dict(particle_data, orient='index')
	return df

# def main(param_ranges, param_mass):

#     param_values = {}

#     for param_name, (min_value, max_value, step) in param_ranges.items():
#         values = list(range(min_value, max_value+1, step))
#         param_values[param_name] = values

#     combinations = list(itertools.product(*param_values.values()))
#     print(combinations)


#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         result = list(executor.map(perform_calculations_mass, combinations))

#     liste_mass = [x[0] for x in result]
#     liste_input = [x[1] for x in result]

#     plot_mass(liste_mass,liste_input, param_mass)



def plot_masses(param_ranges, param_mass, neutralino, fig, ax, options):

    output_list = are_files.are_output()
    param_list = list(param_mass.keys())
    var_list = list(param_ranges.keys())

    liste_mass = []
    liste_input = []

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
                if float(dict_file[elem]) != float(param_mass[elem]):
                    bad = True
        if bad:
            continue
                    
        # if 'M_1(MX)' in param_list:
        #     if temp2[0] != str(param_mass['M_1(MX)']):
        #         continue
        # if 'M_2(MX)' in param_list:
        #     if temp3[0] != str(param_mass['M_2(MX)']):
        #         continue
        # if 'mu(MX)' in param_list:
        #     if temp4[0] != str(param_mass['mu(MX)']):
        #         continue

        for elem in var_list:
            min,max,step = param_ranges[elem]
            rang = range(min,max,step)
            if int(dict_file[elem]) in rang:
                df = slha_to_dataframe(file)
                tup = ()
                for i in elements:
                    tup += tuple([float(dict_file[i])])
                liste_mass.append(df)
                liste_input.append(tup)

        # if 'M_1(MX)' in var_list and neutralino == 'N1':
        #     min,max,step = param_ranges['M_1(MX)']
        #     rang = range(min,max,step)
        #     if int(temp2[0]) in rang:
        #         df = slha_to_dataframe(file)
        #         tup = (float(temp2[0]),float(temp3[0]),float(temp4[0]))
        #         liste_mass.append(df)
        #         liste_input.append(tup)


        # if 'M_2(MX)' in var_list and neutralino == 'N2':
        #     min,max,step = param_ranges['M_2(MX)']
        #     rang = range(min,max,step)
        #     if int(temp3[0]) in rang:
        #         df = slha_to_dataframe(file)
        #         tup = (float(temp2[0]),float(temp3[0]),float(temp4[0]))
        #         liste_mass.append(df)
        #         liste_input.append(tup)

        # if 'mu(MX)' in var_list and neutralino == 'no':
        #     min,max,step = param_ranges['mu(MX)']
        #     rang = range(min,max,step)
        #     if int(temp4[0]) in rang:
        #         df = slha_to_dataframe(file)
        #         tup = (float(temp2[0]),float(temp3[0]),float(temp4[0]))
        #         liste_mass.append(df)
        #         liste_input.append(tup)



    plot_mass(liste_mass,liste_input,param_mass,param_ranges, neutralino, fig, ax)




def plot_mass(liste_mass, liste_input, param_mass, param_ranges, neutralino, fig, ax):

    neutralino_1 = []
    neutralino_2 = []
    neutralino_3 = []
    neutralino_4 = []

    for i in range(len(liste_mass)):
        neutralino_1.append(float(liste_mass[i][liste_mass[i]['pid'] == 1000022]['mass']))
        neutralino_2.append(float(liste_mass[i][liste_mass[i]['pid'] == 1000023]['mass']))
        neutralino_3.append(float(liste_mass[i][liste_mass[i]['pid'] == 1000025]['mass']))
        neutralino_4.append(float(liste_mass[i][liste_mass[i]['pid'] == 1000035]['mass']))

    x_m1,x_m2,x_mu = [],[],[]
    y_m1_1,y_m1_2,y_m1_3,y_m1_4 = [],[],[],[]
    y_m2_1,y_m2_2,y_m2_3,y_m2_4 = [],[],[],[]
    y_mu_1,y_mu_2,y_mu_3,y_mu_4 = [],[],[],[]

    for i in range(len(liste_input)):
        # if liste_input[i][0] == 100:
        #     if liste_input[i][2] == 100:
        #y_m1_1.append()
        x_m2.append(math.fabs(liste_input[i][1]))
        x_m1.append(math.fabs(liste_input[i][0]))
        y_m2_1.append(math.fabs(neutralino_1[i]))
        y_m2_2.append(math.fabs(neutralino_2[i]))
        y_m2_3.append(math.fabs(neutralino_3[i]))
        y_m2_4.append(math.fabs(neutralino_4[i]))

    if neutralino == 'M1':
        plot_M1(x_m1,y_m2_1,y_m2_2, fig, ax, param_ranges, param_mass, neutralino)
    if neutralino == 'M2':
        plot_M2(x_m2,y_m2_1,y_m2_2, fig, ax, param_ranges, param_mass, neutralino)
    if neutralino == 'map':
        plots(x_m1, x_m2, y_m2_1, y_m2_2, fig, ax, param_ranges, param_mass) 
    # #plt.plot(x_mu,y_mu_2, label = "mu(MX)")
    # plt.legend()

    # plt.ylabel("Masses du neutralino 1 en GeV")
    # plt.xlabel("Masse M_1(MX) en GeV")
    # #print(liste_input)
    # plt.savefig("neutralino_2")
    # plt.show()

def plot_M1(x_m1,y_m2_1,y_m2_2, fig, ax, param_ranges, param_mass, neutralino):

    xy_sorted = sorted(zip(x_m1,y_m2_1, y_m2_2), key = lambda triplet: triplet[0])
    x_m1, y_m2_1, y_m2_2 = zip(*xy_sorted)
    x_m1 = list(x_m1)
    y_m2_1 = list(y_m2_1)
    y_m2_2 = list(y_m2_2)
    ax.plot(x_m1,y_m2_1, label = "Variation du neutralino_1 en fonction de M_1(MX)")
    ax.plot(x_m1,y_m2_2, label = "Variation du neutralino_2 en fonction de M_1(MX)")
    #plt.plot(x_mu,y_mu_2, label = "mu(MX)")
    plt.legend()

    ax.set_ylabel("Masses du neutralino en GeV")
    ax.set_xlabel("Masse " + str(list(param_ranges.keys())) +" en GeV")
    #print(liste_input)
    plt.savefig("neutralino_"+neutralino)

def plot_M2(x_m1,y_m2_1,y_m2_2, fig, ax, param_ranges, param_mass, neutralino):
    xy_sorted = sorted(zip(x_m1,y_m2_1, y_m2_2), key = lambda triplet: triplet[0])
    x_m1, y_m2_1, y_m2_2 = zip(*xy_sorted)
    x_m1 = list(x_m1)
    y_m2_1 = list(y_m2_1)
    y_m2_2 = list(y_m2_2)
    ax.plot(x_m1,y_m2_1, label = "Variation du neutralino_1 en fonction de M_2(MX)")
    ax.plot(x_m1,y_m2_2, label = "Variation du neutralino_2 en fonction de M_2(MX)")
    #plt.plot(x_mu,y_mu_2, label = "mu(MX)")
    plt.legend()

    ax.set_ylabel("Masses du neutralino en GeV")
    ax.set_xlabel("Masse " + str(list(param_ranges.keys())) +" en GeV")
    #print(liste_input)
    plt.savefig("neutralino_"+neutralino)


def plots(x_m1,x_m2,y_m2_1,y_m2_2, fig, ax, param_ranges, param_mass):
    x_m1 = list(x_m1)
    x_m2 = list(x_m2)
    y_m2_1 = list(y_m2_1)
    y_m2_2 = list(y_m2_2)
    
    scatter = ax.scatter(x_m1, x_m2, c = y_m2_1, cmap = 'viridis')

    cbar = fig.colorbar(scatter, ax=ax, label = 'Neutralino 1')
    x_m1_grid, x_m2_grid = np.meshgrid(np.linspace(min(x_m1), max(x_m1), 100), np.linspace(min(x_m2), max(x_m2), 100))
    points = np.vstack((x_m1, x_m2)).T
    y_m2_1_grid = griddata(points, y_m2_1, (x_m1_grid, x_m2_grid), method = 'cubic')
    ax.contour(x_m1_grid, x_m2_grid, y_m2_1_grid, cmap = 'viridis', alpha = 0.5)

    ax.set_xlabel('M_1(MX)')
    ax.set_ylabel('M_2(MX)')

# def perform_calculations_mass(combi):

#     try:
#         M1 = combi[0]
#     except IndexError:
#         M1 = True

#     try:
#         M2 = combi[1]
#     except IndexError:
#         M2 = True

#     try:
#         mu = combi[2]
#     except IndexError:
#         mu = True

#     output_filename = f"output_dir/output_m1_{M1}_m2_{M2}_mu_{mu}.slha"

#     with open(output_filename, "r") as f:
#         lines = f.readlines()
    
#     if M1 == True or M2 == True or mu == True:
#         for i, line in enumerate(lines):
#             if line.startswith("M_1(MX)", -8):
#                 if M1 == True:
#                     line.split(" ")
#                     M1 = line[1]
#             if line.startswith("M_2(MX)", -8):
#                 if M2 == True:
#                     line.split(" ")
#                     M2 = line[1]
#             if line.startswith("mu(MX)", -7):
#                 if mu == True:
#                     line.split(" ")
#                     mu = line[1]
#     df = slha_to_dataframe(output_filename)
#     tup = (M1,M2,mu)
#     return df, tup