from ds1054z import DS1054Z
from fy6600 import FY6600
from time import sleep

gen = FY6600()
exit()

osc = DS1054Z()
osc.reset()
osc.unlock_autoscale()
osc.autoscale()

osc.average_vpp(1)
osc.average_phase_difference(1,2)

