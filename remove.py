import os
import subprocess
from pathlib import Path
import pyslha


def lire_fichier(fichier):
	return pyslha.read(fichier)

def remove_files():
    output_dir = "output_dir"
    input_dir = "input_dir"
    for name in os.listdir(output_dir):
        path_file = os.path.join(output_dir, name)

        if os.path.isfile(path_file):
            os.remove(path_file)

    for name in os.listdir(input_dir):
        path_file = os.path.join(input_dir, name)

        if os.path.isfile(path_file):
            os.remove(path_file)
# param_ranges = {
#     "M_1(MX)": (100, 10000, 100),
#     "M_2(MX)": (100, 10000, 100),
# 	"mu(MX)": (100,10000,100)
#     }



# for i in os.listdir('output_files'):
#     i_name = os.path.join('output_files', i)

#     if "mu_100" not in i_name:
#         os.remove(i_name)