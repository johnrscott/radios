import usbtmc as ut

dev = ut.Instrument(0x1ab1, 0x04ce)
print(dev.ask("*IDN?"))

dev.close()
