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

    def set_frequency(self, n, f):
        ''' 
        Set the frequency of channel n to f (in Hertz)
        '''
        # The argument is passed in micro-Hertz, padded
        # to a fourteen digit integer
        f_uHz = f"{(f/1e-6):014.0f}"
        print(f_uHz)
        self.ser.write(f"WMF{f_uHz}\n".encode())


    def __del__(self):
        self.ser.close()

        
