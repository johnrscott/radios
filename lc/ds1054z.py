import pyvisa

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
        self.dev = rm.open_resource(rm.list_resources()[0])
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
        
    def set_channel(self, n, on):
        '''
        Turn a channel on or off, and set the vertical properties
        of the channel. 
        '''
        if on:
            self.dev.write(f":CHANNEL{n}:DISPLAY ON")
        else:
            self.dev.write(f":CHANNEL{n}:DISPLAY OFF")            
        self.wait_for_completion()
            
    def read_average_vpp(self, n):
        '''
        Read the average peak-to-peak voltage on a channel
        '''
        vpp = self.dev.query(f":MEASURE:STATISTIC:ITEM? AVERAGES,VPP,CHANNEL{n}")
        print(f"Obtained average Vpp = {vpp} V on channel {n}")
        return vpp

    def wait_for_completion(self):
        self.dev.query("*OPC?")
    
    def __del__(self):
        self.dev.close()        
        

