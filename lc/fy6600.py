import serial

class FY6600:
    def __init__(self, device = "/dev/ttyUSB1"):
        self.ser = serial.Serial(device)
        self.ser.baudrate = 115200
        self.ser.write(b"RMA\n")
        print(self.ser.readline())
