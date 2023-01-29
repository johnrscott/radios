from ds1054z import DS1054Z
from fy6600 import FY6600
from time import sleep
import numpy as np
import pandas as pd

input_channel = 1
output_channel = 2

target_input_amplitude = 0.5
gen_max_voltage = 5
gen_min_voltage = 0

gen = FY6600()
osc = DS1054Z()
osc.reset()
osc.enable_channel(input_channel)
osc.enable_channel(output_channel)
osc.set_trigger(input_channel, 0.0)

freq = np.geomspace(1e3, 6e7, 11)
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
    device under test. An initial measurement is 
    made, which is used to scale the axis appropriately for
    a more accurate measurement. Result in volts.
    '''
    v_meas = osc.average_vpp(output_channel) / 2
    num_divs = 2
    volts_per_div = v_meas / num_divs
    osc.set_vertical_scale(output_channel, volts_per_div)
    return osc.average_vpp(output_channel) / 2
    
def phase_difference():
    '''
    Get the phase difference between the input and the
    output channels. The result is in degrees.
    '''
    sleep(1)
    p1 = osc.average_phase_difference(input_channel,
                                      output_channel)
    sleep(1)
    p2 = osc.average_phase_difference(input_channel,
                                      output_channel)
    sleep(1)
    p3 = osc.average_phase_difference(input_channel,
                                      output_channel)
    return (p1 + p2 + p3) / 3
    
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
    
    v_tol = 0.01
    max_iter = 20

    # Make an amplitude measurement
    # to test if any adjustment is needed
    v_meas = input_amplitude()
    if abs(v_meas - target) < v_tol:
        print("No need for amplitude adjustment")
        return 0
    
    print("Amplitude adjustment required")
    
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
            v_upper = v_try
        else:
            v_lower = v_try
        n += 1

    raise RuntimeError(f"Voltage adjustment did not converge within {max_iter} iterations")

set_frequency(1e3)
v_in = set_input_amplitude(0.5)
print(v_in)

v_gen = []
v_in = []
v_out = []
phase_in_out = []

for f in freq:
    print(f"Measuring frequency {f} Hz")
    set_frequency(f)
    v_gen.append(set_input_amplitude(target_input_amplitude))
    v_in.append(input_amplitude())
    v_out.append(output_amplitude())
    phase_in_out.append(phase_difference())
    print("")

df = pd.DataFrame({
    "f": freq,
    "v_gen": v_gen,
    "v_in": v_in,
    "v_out": v_out,
    "phase": phase_in_out
})

df.to_csv("meas.csv")
