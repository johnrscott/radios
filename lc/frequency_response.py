from ds1054z import DS1054Z
from fy6600 import FY6600
from time import sleep
import numpy as np

gen = FY6600()

osc = DS1054Z()
osc.reset()
osc.unlock_autoscale()

freq = np.geomspace(1e3, 1e4, 11)
print(freq)

gen.set_amplitude(1.0)
gen.set_frequency(freq[0])
osc.autoscale()

for f in freq:
    gen.set_frequency(f)
    sleep(1)
    osc.reset_statistic_data()
    sleep(3)
    osc.average_vpp(1)
    osc.average_phase_difference(1,2)
    
    
exit()


