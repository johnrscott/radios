import serial

class FY6600:
    def __init__(self, device = "/dev/ttyUSB1"):
        '''
        Create a new FY6600 signal generator object.
        '''
        self.ser = serial.Serial(device)
        self.ser.baudrate = 115200
        # self.ser.write(b"RMA\n")
        # print(self.ser.readline())

    def set_frequency(self, f):
        ''' 
        Set the frequency of channel n to f (in Hertz)
        '''
        # The argument is passed in micro-Hertz, padded
        # to a fourteen digit integer
        val = f"{(f/1e-6):014.0f}"
        self.ser.write(f"WMF{val}\n".encode())

    def set_amplitude(self, v):
        ''' 
        Set the amplitude of channel n to f (in Volts)
        '''
        # The argument is passed in Volts, formatted
        # as xx.xx (note 5 characters required)
        val = f"{v:05.2f}"
        print(val)
        self.ser.write(f"WMA{val}\n".encode())

        

    def __del__(self):
        self.ser.close()

        
