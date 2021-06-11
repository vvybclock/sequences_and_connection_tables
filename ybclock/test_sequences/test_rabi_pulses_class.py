from labscript import start, stop
from labscriptlib.ybclock.connection_table import define_connection_table
from labscriptlib.ybclock.classes import *

if __name__ == '__main__':
	define_connection_table()

	print("Test Spinor Class...")

	atom = Spinor(w_larmor = 10e3)

	atom.prepare_atom_unitary(t=0)


	print(f"Atom Unitary\n {atom.unitary}")
	print(f"Evolution Unitary\n {atom.U_V([200000000*pi])}")
	print(f"tlast: {atom.t_last}")
	print(f"Net Unitary\n {atom.rabi_pulse(t=0.1, duration=0)}")
	start()
	
	stop(1)
