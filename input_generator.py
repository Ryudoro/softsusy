import os
import subprocess
from pathlib import Path
import itertools
import concurrent.futures
import functools

# def create_input_file(base_input, output_filename, params_to_change):
# 	with open(base_input, "r") as f:
# 		lines = f.readlines()

# 	for param, value in params_to_change.items():
# 		for i, line in enumerate(lines):
# 			if line.startswith(param, -8):
# 				if param == "M_1(MX)":
# 					lines[i] = f" 1  {value} #{param}\n"
# 				if param == "M_2(MX)":
# 					lines[i] = f" 2 {value} #{param}\n"
# 				if param == "mu(MX)":
# 					lines[i] = f" 23 {value} #{param}\n"
# 				break

# 	with open(output_filename, "w") as f:
#     		f.writelines(lines)

def create_input_file(base_input, output_filename, params_to_change):
	with open(base_input, "r") as f:
		lines = f.readlines()
	
	for i, line in enumerate(lines):

		if line.startswith("M_1(MX)", -8) and params_to_change["M_1(MX)"] != True:
			M1 = params_to_change["M_1(MX)"]
			lines[i] = f"1 {M1} # M1(MX)\n"
		if line.startswith("M_2(MX)", -8) and params_to_change["M_2(MX)"] != True:
			M2 = params_to_change["M_2(MX)"]
			lines[i] = f"2 {M2} # M2(MX)\n"
		if line.startswith("mu(MX)", -7) and params_to_change["mu(MX)"] != True:
			mu = params_to_change["mu(MX)"]
			lines[i] = f"23 {mu} # mu(MX)\n"

	with open(output_filename, "w") as f:
    		f.writelines(lines)


def run_softsusy(input_filename, output_filename):

	command = f"./softsusy-4.1.13/softpoint.x leshouches < {input_filename} > output_dir/{output_filename}"
	result = subprocess.run(command, shell=True, stdout = subprocess.PIPE, stderr=subprocess.PIPE)


def inputs_generator(param_ranges,param_mass):

	input_dir = "input_dir"
	output_dir = "output_dir"
	os.makedirs(output_dir, exist_ok=True)
	os.makedirs(input_dir, exist_ok=True)

	param_values = {}
	param_name_list = []
	for param_name, (min_value, max_value, step) in param_ranges.items():
		values = list(range(min_value, max_value+1, step))
		param_values[param_name] = values
		param_name_list.append(param_name)
	
	combinations = list(itertools.product(*param_values.values()))
	
	perform_calculations_with_fixed_param = functools.partial(perform_calculations, param_mass=param_mass, name = param_name_list)

	with concurrent.futures.ProcessPoolExecutor() as executor:
		executor.map(perform_calculations_with_fixed_param, combinations)

def perform_calculations(param_values, param_mass,name):

	base_input = "softsusy_ewinos_example.in"

	try:
		M1 = param_values[name.index("M_1(MX)")]
	except (IndexError,ValueError):
		M1 = param_mass["M_1(MX)"]

	try:
		M2 = param_values[name.index("M_2(MX)")]
	except (IndexError,ValueError):
		M2 = param_mass["M_2(MX)"]

	try:
		mu = param_values[name.index("mu(MX)")]
	except (IndexError,ValueError):
		mu = param_mass["mu(MX)"]

	input_filename = f"input_dir/input:M_1:{M1}:M_2:{M2}:mu:{mu}:.slha"


	create_input_file(base_input, input_filename, {"M_1(MX)": M1, "M_2(MX)": M2, "mu(MX)" : mu})

	output_filename = f"output:M_1:{M1}:M_2:{M2}:mu:{mu}:.slha"
	run_softsusy(input_filename, output_filename)

# def main():
# 	base_input = "../softsusy_ewinos_example.in"
# 	input_dir = "../input"
# 	output_dir = "../output_files"
# 	os.makedirs(output_dir, exist_ok=True)

# 	param_ranges = {
#         "M_1(MX)": (100, 10000, 100),
#         "M_2(MX)": (100, 10000, 100),
# 		"mu(MX)": (100,1000,100)
#     	}

# 	for m1 in range(*param_ranges["M_1(MX)"]):
# 			for m2 in range(*param_ranges["M_2(MX)"]):
# 				for mu in range(*param_ranges["mu(MX)"]):
# 					input_filename = f"../input/input_M_1_{m1}_M_2_{m2}_mu_{mu}.slha"
# 					create_input_file(base_input, input_filename, {"M_1(MX)": m1, "M_2(MX)": m2, "mu(MX)" : mu})
# 					output_filename = f"output_m1_{m1}_m2_{m2}_mu_{mu}.slha"
# 					#output_filename = os.path.join(output_dir, f"output_m1_{m1}_m2_{m2}.slha")
# 					run_softsusy(input_filename, output_filename)

#main()
