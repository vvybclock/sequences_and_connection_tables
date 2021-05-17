from lyse import *

try:
	run = Run(path)
	Neta_fits = run.get_result("atoms_in_cavity_helper", "Neta_fit")
	Neta = sum(Neta_fits)/len(Neta_fits)
	run.save_result(name="Neta", value=Neta)
except Exception as e:
	print(f"Error: {e}")