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
        print(f"Connected to '{id}'")

    def set_channel(self, n, on):
        '''
        Turn a channel on or off, and set the vertical properties
        of the channel
        '''
        if on:
            self.dev.write(f":CHANNEL{n}:DISPLAY ON")
        else:
            self.dev.write(f":CHANNEL{n}:DISPLAY OFF")            
        
    def __del__(self):
        self.dev.close()        
        

