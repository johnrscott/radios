from ds1054z import DS1054Z
from fy6600 import FY6600
from time import sleep
import numpy as np

#gen = FY6600()
osc = DS1054Z()

f = np.geomspace(1e3, 1e4, 11)
print(f)

#gen.set_frequency(1e3)
#gen.set_amplitude(1.5)

exit()

osc.reset()
osc.unlock_autoscale()
osc.autoscale()

osc.average_vpp(1)
osc.average_phase_difference(1,2)

