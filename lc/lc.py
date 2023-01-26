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
# The effect of R is to damp the resonance of the LC tank,
# and thereby reduce its impedance from infinity. This
# smooths the phase change across fc, and increase Vout
# from 0 to some finite level at resonance. For low values
# of R, its effect is not visible above Vlim.
#
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

# AM channel bandwidth
bw_kHz = 10

# Particular AM channel
fc_bbc_somerset_kHz = 1566

# Intermediate frequency
f_if_kHz = 455

# 

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
fc_kHz = fc/1e3
f_lo_kHz = fc_kHz - f_if_kHz

axes[0].axhline(y=Vin, color='black', linestyle='-', label = f"|Vin| = {Vin} V")
axes[0].loglog(f_kHz, abs(Vout_with_R), label = f"|Vout|, R = {R} Ohms")
axes[0].loglog(f_kHz, abs(Vout_without_R), label = f"|Vout|, R = 0 Ohms")
axes[0].set_ylabel("Peak-to-peak voltage / V")
axes[0].grid(which="both")
axes[0].xaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))
axes[0].yaxis.set_major_formatter(StrMethodFormatter("{x:.0g}"))
axes[0].axvspan(fc_kHz - bw_kHz/2, fc_kHz + bw_kHz/2,
                alpha=0.7, color="blue", label = f"Tuned AM Channel, fc={fc_kHz:.0f} kHz")
axes[0].axvline(x=f_if_kHz, color='black', linestyle='-',
                label = f"Intermediate Frequency = {f_if_kHz} kHz")
axes[0].axvline(x=f_lo_kHz, color='purple', linestyle='-',
                label = f"Local Oscillator = {f_lo_kHz:.0f} kHz")
axes[0].axvspan(fc_bbc_somerset_kHz - bw_kHz/2, fc_bbc_somerset_kHz + bw_kHz/2,
                alpha=0.7, color="green",
                label = f"BBC Radio Somerset, fc = {fc_bbc_somerset_kHz:.0f} kHz")
axes[0].fill_between(f_kHz, Vlim, facecolor='red',
                     alpha=0.3, label = "Oscilloscope Measurement Limit")
axes[0].legend()

scale = 360/(2*np.pi)
axes[1].plot(f_kHz, scale*np.angle(Vout_with_R), label = f"Phase(Vout), R = {R} Ohms")
axes[1].plot(f_kHz, scale*np.angle(Vout_without_R), label = f"Phase(Vout), R = 0 Ohms")
axes[1].set_xlabel("Frequency, kHz")
axes[1].set_ylabel("Angle / Degrees")
axes[1].grid(which="both")
axes[1].legend()

fig.suptitle(f"Frequency response of parallel LC circuit")

plt.show()
    
