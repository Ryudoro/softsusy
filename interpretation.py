import os
import subprocess
from pathlib import Path
import pyslha

def lire_fichier(fichier):
	return pyslha.read(fichier)

def afficher_masses(data):
	print("Masses des particules")
	for pid, masses in data.blocks["MASS"].items():
		nom = data.pdg.name(pid)
		print(f"{nom} ({pid}): {masses} GeV")

def main():
	
	param_ranges = {
	"M_1(MX)": (100, 1000, 100),
	"M_2(MX)": (100, 1000, 100),
	}

	for m1 in range(*param_ranges["M_1(MX)"]):
		for m2 in range(*param_ranges["M_2(MX)"]):

			output_filename = f"output_files/output_m1_{m1}_m2_{m2}.slha"
			data = lire_fichier(output_filename)
			afficher_masses(data)         
main()
