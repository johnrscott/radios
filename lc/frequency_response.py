from ds1054z import DS1054Z
from fy6600 import FY6600
from time import sleep
import numpy as np

input_channel = 1
output_channel = 2

gen = FY6600()

osc = DS1054Z()
osc.reset()
osc.enable_channel(input_channel)
osc.enable_channel(output_channel)

freq = np.geomspace(1e3, 1e4, 11)
print(freq)

gen.set_amplitude(1.0)
gen.set_frequency(freq[0])

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

def input_amplitude():
    '''
    Get the amplitude of the input channel
    (the one connected to the signal generator),
    which is the input port to the device under
    test. Result in volts.
    '''
    return osc.average_vpp(input_channel) / 2

def output_amplitude():
    '''
    Get the amplitude of the output channel,
    the one connected to the output port of the
    device under test. Result in volts.
    '''
    return osc.average_vpp(output_channel) / 2

def phase_difference():
    '''
    Get the phase difference between the input and the
    output channels. The result is in degrees.
    '''
    return osc.average_phase_difference(input_channel,
                                        output_channel)

def set_gen_amplitude(v):
    '''
    Set the amplitude of the signal generator voltage to
    v. In addition, the oscilloscope channel 1 is measured,
    and the signal is scaled to fit on two vertical divisions.
    '''
    gen.set_amplitude(v)
    sleep(1)
    v_meas = input_amplitude()
    num_divs = 2
    volts_per_div = v_meas / num_divs
    osc.set_vertical_scale(input_channel, volts_per_div)
    
def set_input_amplitude(target):
    '''
    Adjust the signal generator voltage
    to obtain the target voltage on the oscilloscope
    channel. This function uses interval bisection to
    obtain the correct input voltage. The function 
    returns the input voltage that was required to 
    obtain the target output voltage
    '''
    
    v_tol = 0.001
    max_iter = 20
    
    # Initial state
    v_upper = gen_max_voltage
    v_lower = gen_min_voltage
    n = 0
    
    while n < max_iter:
        v_try = (v_lower + v_upper) / 2
        set_gen_amplitude(v_try)
        v_meas = input_amplitude()
        if abs(v_meas - target) < v_tol:
            return v_try
        if v_meas > target:
            print(f"{v_meas}, too high")
            v_upper = v_try
        else:
            print(f"{v_meas}, too low")
            v_lower = v_try
        n += 1

    raise RuntimeError(f"Voltage adjustment did not converge within {max_iter} iterations")

set_frequency(1e3)
v_in = set_input_amplitude(0.5)
exit()

for f in freq:

    set_frequency(f)
    sleep(5)

    print(v_in)
    exit()
    
    osc.average_vpp(1)
    osc.average_vpp(2)
    
    
exit()


