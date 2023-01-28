from ds1054z import DS1054Z
from time import sleep

osc = DS1054Z()
osc.reset()
osc.unlock_autoscale()
osc.autoscale()

osc.read_average_vpp(1)
sleep(2)
osc.read_average_vpp(1)
sleep(2)
osc.read_average_vpp(1)
sleep(2)
osc.read_average_vpp(1)
sleep(2)

