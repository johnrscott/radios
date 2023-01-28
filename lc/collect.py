import usbtmc as ut

class DS1054Z:
    '''
    Rigol DS1054z oscilloscope connection. Use to set timebase, control vertical
    range, and make measurements of waveforms.
    '''
    def __init__(self, vender_id, product_id):
        '''
        Create a new oscilloscope object
        '''
        self.dev = ut.Instrument(vender_id, product_id)
        id = self.dev.ask("*IDN?")
        print(f"Connected to '{id}'")

    def __del__(self):
        self.dev.close()        
        

