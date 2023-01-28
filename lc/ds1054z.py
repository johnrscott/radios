import pyvisa
import re

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
    def __init__(self):
        '''
        Create a new oscilloscope object
        '''
        rm = pyvisa.ResourceManager()
        self.dev = open_rigol_resource(rm)
        id = self.dev.query("*IDN?")
        print(f"Connected to: {id}")
        self.dev.timeout = 100000
        print(f"Set device timeout to {self.dev.timeout} ms")

    def reset(self):
        '''
        Reset the device
        '''
        print("Resetting the device")
        self.dev.write("*RST")
        #self.wait_for_completion()
        
    def autoscale(self):
        '''
        Autoscale the device. This will also turn
        on channels that have signals present.
        '''
        print("Autoscaling device")
        self.dev.write(":AUTOSCALE")
        self.wait_for_completion()

    def unlock_autoscale(self):
        '''
        Unlock the autoscale function on the device
        '''
        print("Unlocking the autoscale function")
        self.dev.write(":SYSTEM:AUTOSCALE ON")
        self.wait_for_completion()
        
    def reset_statistic_data(self):
        '''
        Clear the data being used to calculate a statistic,
        ready for a new statistic.
        '''
        self.dev.write(f":MEASURE:STATISTIC:RESET")
        self.wait_for_completion()
        
    def average_vpp(self, n):
        '''
        Read the average peak-to-peak voltage on a channel
        '''
        # Wait until the command returns sensible numbers
        # (when the statistic is first turned on, it prints
        # ***** to the screen, and returns 9.9E37 here
        cmd = f":MEASURE:STATISTIC:ITEM? AVERAGES,VPP,CHANNEL{n}"
        vpp = 9.9e37
        while abs(vpp) > 1e6:
            vpp = float(self.dev.query(cmd))
        print(f"Obtained average Vpp = {vpp} V on channel {n}")
        return vpp

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
    
    def wait_for_completion(self):
        self.dev.query("*OPC?")
    
    def __del__(self):
        self.dev.close()        
        

