# LC circuit impedance as a function of frequency
#
# This file models the series combination of a parallel
# LC circuit with a sense resistor Rs (for measuring
# current through LC circuit). 
#
# The magnitude and phase of the frequency response is
# plotted. For the magnitude, the units are peak-to-peak
# voltage Vout, for a user-specified input voltage Vin.
# A line is plotted to indicate the measurement floor of
# the oscilloscope for reference (Vlim). For example, set
# Vlim = 0.5e-3 if the smallest vertical resolution is
# 1mV/div.
#
# The script aids in the measurement of the frequency
# response of the following circuit:
#
#      _____I ->_____
#     |            __|__    LC resonant circuit, with R
#     |           R     |   modelling resistance of inductor
#    Vin          |     C   leads. Current I is controlled by 
#     |           L     |   Vin, and measured indirectly across
#     |            -----    Rs (the sense resistor)
#     |              |
#     |              Rs <--- Vout = V(Rs)
#     |              |
#      -----GND------
#       
#
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import numpy as np

# Inductor with series resistance R
L = 30e-6
R = 0.6

# Capacitor
C = 303e-12

# Sense resistor
Rs = 22

# Input voltage, peak-to-peak
Vin = 1

# Set minimum measurement amplitude as 1mV
Vlim = 0.5e-3

print(f"L = {L} H, C = {C} F, Rs = {Rs} Ohms")
fc = 1/(2*np.pi*np.sqrt(L*C))
print(f"Resonant frequency fc = {fc} Hz")

def impedance(f, C, L, R, Rs):
    '''
    Impedance of LC-Rs series combinatio
    '''
    w = 2*np.pi*f
    s = 1j*w
    num = R + s*L
    denom = 1 + s*R*C + s*s*L*C
    return Rs + num / denom


# Base frequency range
f = np.geomspace(1e3, 1e8, 100000)

# Impedance
z_with_R = impedance(f, C, L, R, Rs)
z_without_R = impedance(f, C, L, 0, Rs)

# Transfer function (Vout/Vin), where
# Vout is measured across Rs
Vout_with_R = Rs/z_with_R * Vin
Vout_without_R = Rs/z_without_R * Vin

fig, axes = plt.subplots(2, 1, sharex = True)

#axes[0].set_xlim([0.99*fc, 1.01*fc])

f_kHz = f/1e3
axes[0].loglog(f_kHz, abs(Vout_with_R), label = f"R = {R} Ohms")
axes[0].loglog(f_kHz, abs(Vout_without_R), label = f"R = 0 Ohms")
axes[0].legend()
axes[0].set_ylabel("|Vout|")
axes[0].grid(which="both")
axes[0].xaxis.set_major_formatter(StrMethodFormatter(
    "{x:.0f}"
))
axes[0].yaxis.set_major_formatter(StrMethodFormatter(
    "{x:.0g}"
))
axes[0].fill_between(f_kHz, Vlim, facecolor='red', alpha=0.2)

scale = 360/(2*np.pi)
axes[1].plot(f_kHz, scale*np.angle(Vout_with_R), label = f"R = {R} Ohms")
axes[1].plot(f_kHz, scale*np.angle(Vout_without_R), label = f"R = 0 Ohms")
axes[1].legend()
axes[1].set_xlabel("Frequency, kHz")
axes[1].set_ylabel("arg(Vout), degrees")
axes[1].grid(which="both")

fig.suptitle(f"Frequency response of parallel LC circuit, Vin = {Vin} V")

plt.show()
    
