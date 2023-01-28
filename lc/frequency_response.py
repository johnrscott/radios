from ds1054z import DS1054Z
from time import sleep

osc = DS1054Z()
osc.reset()
osc.unlock_autoscale()
osc.autoscale()

osc.average_vpp(1)
osc.average_phase_difference(1,2)

