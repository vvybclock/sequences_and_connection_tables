from labscript import start, stop
from labscriptlib.ybclock_v0_1.connection_table import define_connection_table

def repeat_p7888_start_triggers(ti, tf, dt):
	t = ti
	while t < tf:
		p7888_start_trigger.enable(t)
		t += dt/2
		p7888_start_trigger.disable(t)
		t += dt/2

def send_fake_photons(ti,tf,dt):
	t = ti
	while t < tf:
		p7888_flushing_channel.enable(t)
		t += dt/2
		p7888_flushing_channel.disable(t)
		t += dt/2


if __name__ == '__main__':
	define_connection_table()
	# Begin issuing labscript primitives
	# start() elicits the commencement of the shot
	start()

	repeat_p7888_start_triggers(
		ti = 5.1,
		tf = 10,
		dt = 1
	)

	send_fake_photons(
		ti = 5.1,
		tf = 10,
		dt = 0.0001
	 )

	
	stop(11)