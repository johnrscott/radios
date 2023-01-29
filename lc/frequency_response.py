from ds1054z import DS1054Z
from fy6600 import FY6600
from time import sleep
import numpy as np
import pandas as pd

class FrequencyResponse:
    '''
    This class obtains frequency response data. A signal
    generator is directed to sweep over a range of frequencies,
    and the magnitude and phase response of the circuit under
    test is measured at each frequency. The results are stored
    in a pandas data frame.
    
    To use the class, connect the signal generator and oscilloscope
    to the device under test in the following way:
    
     _________          ___________
    | Gen     |        |    DUT    |          ________
    |      OUT|---+----|IN      OUT|---------|2       |
    |         |   |    |           |         |   OSC  |
     ^^^^^^^^^    |     ^^^^^^^^^^^          |        |
                  +--------------------------|1       |
                                              ^^^^^^^^
    The class was developed and tested using a FeelTech FY660 signal
    generator and a Rigol DS1054 oscilloscope. It is assumed that the
    signal generator is capable of generating sinusoids of known 
    amplitude. The class automatically adjusts the output amplitude
    of the signal generator to maintain vin_amplitude at port 1 of
    the oscilloscope, which takes account of the source impedance of
    the generator. The class automatically adjusts the vertical and
    horizontal scales of the oscilloscope in order to maintain the
    two signals (IN and OUT) in the centre of the screen; one period
    occupies four horizontal divisions and the peak-to-peak signal
    occupies four vertical divisions.

    This class is generic (but untested), and can in principle be 
    extended to other signal generators and oscilloscopes, provided
    they expose the required functionality.

    Creating the classes initialises the signal generator and
    oscilloscope in their starting states ready for the frequency
    sweep. Call run() to begin the sweep.
    '''
    def __init__(self, freq_low, freq_high, freq_steps,
                 vin_amplitude, input_channel = 1,
                 output_channel = 2):
        self.gen = FY6600()
        self.osc = DS1054Z()
        self.input_channel = 1
        self.output_channel = 2
        self.target_input_amplitude = vin_amplitude
        self.gen_max_voltage = 5
        self.gen_min_voltage = 0
        
        self.osc.reset()
        self.osc.enable_channel(self.input_channel)
        self.osc.enable_channel(self.output_channel)
        self.osc.set_trigger(self.input_channel, 0.0)
        
        self.freq = np.geomspace(freq_low, freq_high, freq_steps)
        
    def set_frequency(self,f):
        '''
        Set the frequency of the signal generator 
        to f, and update the timebase of the oscilloscope
        to target one full period in 6 divisions. Next,
        the system is left to settle for one second, and
        then the statistic data is reset ready for 
        measurements.
        '''
        self.gen.set_frequency(f)    
        period = 1/f
        num_divs = 6
        seconds_per_div = period/num_divs
        self.osc.set_timebase(seconds_per_div)
        sleep(0.5)
        self.osc.reset_statistic_data()

    def update_vertical_scale(self, channel, volts_per_div):
        '''
        Update the vertical scale on channel to v_scale,
        unless the current vertical scale is within 5%
        of the requested value (in which case do nothing).
        '''
        current = self.osc.vertical_scale(channel)
        if abs(current - volts_per_div) / current > 0.05:
            self.osc.set_vertical_scale(channel, volts_per_div)
        return 

    def auto_vertical_scale(self, channel, max_adjustments = 5):
        '''
        Adjust the channel vertical scale to fit the signal
        on the middle four divisions. Raises a RuntimeError
        if max_adjustments are made and the signal amplitude
        cannot be read.
        '''
        for n in range(max_adjustments):
            try:
                v_meas = self.osc.average_vpp(channel) / 2
                num_divs = 2
                volts_per_div = v_meas / num_divs
                self.update_vertical_scale(channel, volts_per_div)
                return
            except RuntimeError:
                print(f"Performing vertical adjustment {n}")
                volts_per_div = self.osc.vertical_scale(channel)
                self.update_vertical_scale(channel, 2 * volts_per_div)
        raise RuntimeError("Reached maximum vertical adjustments")

    def channel_amplitude(self, channel):
        '''
        Make a measurement of the amplitude on a channel.
        The function also adjusts the vertical scale to 
        attempt to place the signal across the middle
        four divisions.
        '''
        self.auto_vertical_scale(channel)
        return self.osc.average_vpp(channel) / 2

    def input_amplitude(self):
        '''
        Get the amplitude of the input channel
        (the one connected to the signal generator),
        which is the input port to the device under
        test. Result in volts.
        '''
        return self.channel_amplitude(self.input_channel)

    def output_amplitude(self):
        '''
        Get the amplitude of the output channel,
        the one connected to the output port of the
        device under test. An initial measurement is 
        made, which is used to scale the axis appropriately for
        a more accurate measurement. Result in volts.
        '''
        return self.channel_amplitude(self.output_channel)    

    def phase_difference(self, num_samples = 10, delay = 0.75):
        '''
        Get the phase difference between the input and the
        output channels. The result is in degrees. The
        num_samples determines how many readings are taken
        (separated by delay seconds) and averaged (the average
        phase measurement appears highly variable).
        '''
        # Reset the statistics and wait for average to stabilise
        self.osc.reset_statistic_data()
        sleep(5)        
        total = 0
        for n in range(num_samples):
            total += self.osc.average_phase_difference(self.input_channel,
                                                       self.output_channel)        
            sleep(0.75)
        return total / num_samples

    def set_gen_amplitude(self, v):
        '''
        Set the amplitude of the signal generator voltage to
        v. In addition, the oscilloscope channel 1 is measured,
        and the signal is scaled to fit on two vertical divisions.
        '''
        self.gen.set_amplitude(v)
        self.auto_vertical_scale(self.input_channel)
        sleep(0.5)
        self.osc.reset_statistic_data()
        sleep(0.5)
        return

    def set_input_amplitude(self, target):
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
        v_meas = self.input_amplitude()
        if abs(v_meas - target) < v_tol:
            print("No need for amplitude adjustment")
            return 0

        print("Amplitude adjustment required")

        # Initial state
        v_low = self.gen_min_voltage
        v_high = self.gen_max_voltage

        for n in range(max_iter):
            v_mid = (v_low + v_high) / 2
            self.set_gen_amplitude(v_mid)
            v_meas = self.input_amplitude()
            print(f"n={n}, v_low={v_low}, v_mid={v_mid}, v_high={v_high}: v_meas={v_meas}")
            if abs(v_meas - target) < v_tol:
                return v_mid
            if v_meas > target:
                v_high = v_mid
            else:
                v_low = v_mid

        raise RuntimeError(f"Voltage adjustment did not converge within {max_iter} iterations")

    def run(self, savefile = "meas.csv"):
        '''
        Run the frequency sweep and return the frequency response 
        data as a dataframe. The function also saves the file as
        meas
        '''
    
        v_gen = []
        v_in = []
        v_out = []
        phase_in_out = []

        for n, f in enumerate(self.freq):
            print(f"Measuring frequency {f} Hz ({n}/{len(self.freq)})")
            self.set_frequency(f)
            v_gen.append(self.set_input_amplitude(self.target_input_amplitude))
            v_in.append(self.input_amplitude())
            v_out.append(self.output_amplitude())
            phase_in_out.append(self.phase_difference())

        df = pd.DataFrame({
            "f": self.freq,
            "v_gen": v_gen,
            "v_in": v_in,
            "v_out": v_out,
            "phase": phase_in_out
        })

        df.to_csv(savefile)
        return df
