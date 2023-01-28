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

def set_frequency(f):
    '''
    Set the frequency of the signal generator 
    to f, and update the timebase of the oscilloscope
    to target one full period in 6 divisions. Next,
    the system is left to settle for one second, and
    then the statistic data is reset ready for 
    measurements.
    '''
    gen.set_frequency(f)    
    period = 1/f
    num_divs = 6
    seconds_per_div = period/num_divs
    osc.set_timebase(seconds_per_div)
    sleep(1)
    osc.reset_statistic_data()

target_voltage = 1
gen_max_voltage = 5
gen_min_voltage = 0

def set_amplitude(v):
    '''
    Set the amplitude of the signal generator voltage to
    v. In addition, the oscilloscope is autoscaled so that
    the new amplitude fits on the screen
    '''
    gen.set_amplitude(v)
    osc.autoscale()

def adjust_voltage_to(target):
    '''
    Adjust the signal generator voltage
    to obtain the target voltage on the oscilloscope
    channel. This function uses interval bisection to
    obtain the correct input voltage. The function 
    returns the input voltage that was required to 
    obtain the target output voltage
    ''' 
    v_tol = 0.01
    max_iter = 5
    
    # Initial state
    v_upper = gen_max_voltage
    v_lower = gen_min_voltage
    n = 0
    
    while n < max_iter:
        v_try = (v_lower + v_upper) / 2
        set_amplitude(v_try)
        sleep(1)
        v_meas = osc.average_vpp(1)
        if abs(v_meas - target) < v_tol:
            return v_try
        if v_meas > target:
            v_upper = v_try
        else:
            v_lower = v_try
        n += 1

    raise RuntimeError(f"Voltage adjustment did not converge within {max_iter} iterations")
        
for f in freq:

    set_frequency(f)
    sleep(5)

    v_in = adjust_voltage_to(1.0)
    print(v_in)
    exit()
    
    osc.average_vpp(1)
    osc.average_vpp(2)
    osc.average_phase_difference(1,2)
    
    
exit()


