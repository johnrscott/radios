# LC circuit impedance as a function of frequency
#
# This file models the series combination of a parallel
# LC circuit with a sense resistor Rs (for measuring
# current through LC circuit). 
#
import matplotlib.pyplot as plt
import numpy as np

L = 30e-6
C = 303e-12

Rs = 22

print(f"L = {L} H, C = {C} F, Rs = {Rs} Ohms")
fc = 1/(2*np.pi*np.sqrt(L*C))
print(f"Resonant frequency fc = {fc} Hz")

def impedance(f):
    '''
    Impedance of LC-Rs series combinatio
    '''
    w = 2*np.pi*f
    wc = 2*np.pi*fc
    return w / (1j*C*(w*w - wc*wc)) + Rs


# Base frequency range
f = np.geomspace(1e3, 1e8, 100000)

# Impedance
z = impedance(f)

# Transfer function (Vout/Vin), where
# Vout is measured across Rs
h = Rs/z


plt.plot(f, abs(h))
plt.loglog()
plt.xlim([0.99*fc, 1.01*fc])
plt.show()
    
