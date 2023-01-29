import pyvisa
import re
from time import sleep

def open_rigol_resource(rm):
    '''
    Search for the Rigol DS1054z oscilloscope in the VISA
    resource list, and return the opened resource
    '''
    # Rigol DS1054z
    vender_id = "6833"
    product_id = "1230"

    resources = rm.list_resources()
    matches = [i for i, elem in enumerate(resources) if
               re.search(vender_id, elem) and
               re.search(product_id, elem)]
    if len(matches) != 1:
        raise RuntimeError("Unable to open connection to DS1054z")
    else:
        return rm.open_resource(resources[matches[0]])

class DS1054Z:
    '''
    Rigol DS1054z oscilloscope connection. Use to set timebase, control vertical
    range, and make measurements of waveforms.
    '''
    def __init__(self, timeout_seconds = 1):
        '''
        Create a new oscilloscope object
        '''
        rm = pyvisa.ResourceManager()
        self.dev = open_rigol_resource(rm)
        id = self.dev.query("*IDN?")
        print(f"Connected to: {id}")
        self.dev.timeout = timeout_seconds * 1e3
        print(f"Set device timeout to {self.dev.timeout} ms")

    def reset(self):
        '''
        Reset the device
        '''
        print("Resetting the device")
        self.dev.write("*RST")
        self.wait_for_completion()
            

    def enable_channel(self, n):
        '''
        Turn on the specified channel, set the vertical
        scale to 0.2V/div and zero the vertical offset.
        '''
        self.dev.write(f":CHANNEL{n}:DISPLAY ON")
        self.set_vertical_scale(n, 0.2)
        self.dev.write(f":CHANNEL{n}:OFFSET 0")
        self.wait_for_completion()
        
    def reset_statistic_data(self):
        '''
        Clear the data being used to calculate a statistic,
        ready for a new statistic.
        '''
        self.dev.write(f":MEASURE:STATISTIC:RESET")
        self.wait_for_completion()
        
    def average_vpp(self, n, max_attempts = 10):
        '''
        Read the average peak-to-peak voltage on a channel. If
        the measurement fails, make repeated attempts up to
        max_attempts, separated by 0.1 second. RuntimeError is
        raised if measured fails after max_attempts.
        '''
        # Wait until the command returns sensible numbers
        # (when the statistic is first turned on, it prints
        # ***** to the screen, and returns 9.9E37 here. The check
        # for validity is whether vpp < 1e6 (1 MV)
        cmd = f":MEASURE:STATISTIC:ITEM? AVERAGES,VPP,CHANNEL{n}"
        for n in range(max_attempts):
            print(f"Reading Vpp, attempt {n}")
            vpp = float(self.dev.query(cmd))
            if abs(vpp) < 1e6:
                return vpp
            sleep(0.1)
        raise RuntimeError("Reached maximum attempts while reading Vpp")
    
    def average_phase_difference(self, n1, n2):
        '''
        Read the average peak-to-peak voltage on a channel
        '''
        # Wait until the command returns sensible numbers
        # (when the statistic is first turned on, it prints
        # ***** to the screen, and returns 9.9E37 here
        cmd = f":MEASURE:STATISTIC:ITEM? AVERAGES,RPHASE,CHANNEL{n1},CHANNEL{n2}"
        phase = 9.9e37
        while abs(phase) > 1e6:
            phase = float(self.dev.query(cmd))
        print(f"Obtained average phase = {phase} deg between channels {n1} and {n2}")
        return phase

    def set_timebase(self, seconds_per_div):
        '''
        Set the timebase of the oscilloscope. The timebase nearest to
        the specified seconds per division is picked.
        '''
        print(f"Setting main timebase to {seconds_per_div} s/div")
        self.dev.write(f":TIMEBASE:MAIN:SCALE {seconds_per_div}")
        self.wait_for_completion()        

    def set_vertical_scale(self, n, volts_per_div):
        '''
        Set the vertical scale of channel n to the specified volts
        per division (or the closest valid scale)
        '''
        print(f"Setting vertical scale {volts_per_div}")
        self.dev.write(f":CHANNEL{n}:SCALE {volts_per_div}")
        self.wait_for_completion()                

    def vertical_scale(self, n):
        '''
        Set the vertical scale of channel n to the specified volts
        per division (or the closest valid scale)
        '''
        v_scale = float(self.dev.query(f":CHANNEL{n}:SCALE?"))
        print(f"Obtained vertical scale {v_scale}")
        return v_scale
        
    def set_trigger(self, n, level):
        '''
        Set the trigger source to channel n with a specified
        trigger level. The type of triggering is set to rising
        edge. The 
        '''
        self.dev.write(f":TRIGGER:EDGE:SOURCE CHANNEL{n}")
        self.dev.write(f":TRIGGER:EDGE:SLOPE POSITIVE")
        self.dev.write(f":TRIGGER:EDGE:LEVEL {level}")        
        self.wait_for_completion()
        
    def wait_for_completion(self, max_timeouts = 10):
        '''
        Wait for the completetion of a previous command, allowing
        multiple timeouts to occur in the waiting command (*OPC?). 
        By setting the number of timeouts, the maximum allowed time
        can be controlled by the caller. If the maximum number of 
        timeouts is reached, a runtime error is thrown.
        '''
        for n in range(max_timeouts):
            try:
                self.dev.query("*OPC?")
                return
            except pyvisa.errors.VisaIOError as e:
                if e.error_code == pyvisa.constants.VI_ERROR_TMO:
                    print(f"Got timeout {n}; trying again")
                else:
                    raise e
        raise RuntimeError("Reached maximum timeouts waiting for completion")
                
    def __del__(self):
        self.dev.close()        
        

