from ds1054z import DS1054Z
from time import sleep

osc = DS1054Z()

while True:
    osc.set_channel(1, True)
    sleep(1)
    osc.set_channel(1, False)
    sleep(1)
    
