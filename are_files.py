import os
import pyslha

def are_input():
    input_dir = "input_dir"

    liste_files = []

    for name in os.listdir(input_dir):
        path_file = os.path.join(input_dir, name)

        if os.path.isfile(path_file):
            liste_files.append(path_file)
    return liste_files

def are_output():
    output_dir = "output_dir"
    liste_files = []

    for name in os.listdir(output_dir):
        path_file = os.path.join(output_dir, name)

        if os.path.isfile(path_file):
            liste_files.append(path_file)
    return liste_files

def change_name():
    liste_output_file = are_output()
    liste_input_file = are_output()

    
    return True

def file_infos(file,options):

    data = pyslha.read(file)

    m1 = data.blocks['EXTPAR'][1]
    m2 = data.blocks['EXTPAR'][2]
    mu = data.blocks['EXTPAR'][23]

    result = {
          'M_1(MX)': m1,
          'M_2(MX)': m2,
          'mu(MX)' : mu
    }

    return result
    # split = file.split(':')

    # elements = {}
    # for i in range(len(split)):
    #     if split[i]+'(MX)' in options:
    #         elements[split[i]+'(MX)'] = float(split[i+1])
    # return elements

# file = "output:M_1(MX):100:M_2(MX):100:mu(MX):800:.slha"

# options = ["M_1(MX)", "M_2(MX)", "mu(MX)", "tan(beta)"]

# a = file_infos(file,options)
# print(a)