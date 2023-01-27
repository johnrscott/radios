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

# Measured data
f_meas_kHz = np.array([1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1650,1700,1800,1900,2000,3000,4000,5000,6000,7000,8000,9000,10000,20000,30000,40000,50000,60000])
Vin_mag_V = 1.01
Vout_mag_mV_1 = np.array([984,984,984,984,976,976,984,984,984,984,968,952,920,896,856,824,792,760,728,480,344,260,208,168,134,114,94,78,64,54,42,32.8,24.8,15.2,12.4,12,21,24,32,88.8,132,172,210,248,282,310,344,600,728,832,984,976])
Vout_angle_1 = np.array([2.16,-1.44,2.622,3.6,3.52,3.894,4.513,4.025,5.827,5.02,9.38,14.01,21.6,27,29.1,31.77,35.08,38.2,41.04,61.2,67.9,75.6,78.3,80.48,85.55,87.9,82.33,81.2,80.52,77.88,72,70,68,19,-51,-84,-68,-93,-92.36,-81.2,-75,-77.4,-71.14,-71.59,-68,-66,-67,-41.2,-36,-23.04,-16.4,-6.8])
Vout_mag_mV_2 = np.array([992,992,992,984,984,984,976,976,976,976,960,950,912,888,856,824,792,760,736,488,344,256,212,172,138,118,98,84,66,56,44,33.6,25.2,18,11,15,19,25,29,90.4,136,174,212,252,280,314,348,604,712,840,994,994])
print(len(Vout_mag_mV_2))
Vout_mag_mV = (Vout_mag_mV_1 + Vout_mag_mV_2) / 2
Vout_angle_2 = np.array([-0.72,-1.428,1.622,2.160,2.520,3.021,3.529,5.176,4.532,6.480,10.80,16.26,18.72,23.40,26.95,32.68,34.04,39.50,40.88,58.76,68.11,71.28,78.20,80.25,80.52,86.20,85.97,82.08,78.19,81.15,77,74,67,-5,74,-46,-82,-97,-88,-77.6,-86,-81,-73.73,-70,-67,-68.04,-64,-47.56,-38.76,-24.60,-18,-8.6])
Vout_angle = (Vout_angle_1 + Vout_angle_2) / 2

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
f_image_kHz = f_lo_kHz + 2*f_if_kHz

axes[0].axhline(y=Vin, color='black', linestyle='-', label = f"|Vin| = {Vin} V")
axes[0].loglog(f_kHz, abs(Vout_with_R), label = f"|Vout|, R = {R} Ohms")
axes[0].scatter(f_meas_kHz, (Vin_mag_V / Vin) * Vout_mag_mV / 1000)
axes[0].loglog(f_kHz, abs(Vout_without_R), label = f"|Vout|, R = 0 Ohms")
axes[0].set_ylabel("Peak-to-peak voltage / V")
axes[0].grid(which="both")
axes[0].xaxis.set_major_formatter(StrMethodFormatter("{x:.0f}"))
axes[0].yaxis.set_major_formatter(StrMethodFormatter("{x:.0g}"))
axes[0].axvspan(fc_kHz - bw_kHz/2, fc_kHz + bw_kHz/2,
                alpha=0.1, color="blue", label = f"Tuned AM Channel, fc={fc_kHz:.0f} kHz")
axes[0].axvline(x=f_if_kHz, color='black', linestyle='-',
                label = f"Intermediate Frequency = {f_if_kHz} kHz")
axes[0].axvline(x=f_lo_kHz, color='purple', linestyle='-',
                label = f"Local Oscillator = {f_lo_kHz:.0f} kHz")
axes[0].axvspan(fc_bbc_somerset_kHz - bw_kHz/2, fc_bbc_somerset_kHz + bw_kHz/2,
                alpha=0.1, color="green",
                label = f"BBC Radio Somerset, fc = {fc_bbc_somerset_kHz:.0f} kHz")
axes[0].fill_between(f_kHz, Vlim, facecolor='red',
                     alpha=0.1, label = "Oscilloscope Measurement Limit")
axes[0].axvspan(f_image_kHz - bw_kHz/2, f_image_kHz + bw_kHz/2,
                alpha=0.1, color="red", label = f"Image AM Channel, fc={fc_kHz:.0f} kHz")
axes[0].legend()

scale = 360/(2*np.pi)
axes[1].plot(f_kHz, scale*np.angle(Vout_with_R), label = f"Phase(Vout), R = {R} Ohms")
axes[1].plot(f_kHz, scale*np.angle(Vout_without_R), label = f"Phase(Vout), R = 0 Ohms")
axes[1].scatter(f_meas_kHz, -Vout_angle)
axes[1].set_xlabel("Frequency, kHz")
axes[1].set_ylabel("Angle / Degrees")
axes[1].grid(which="both")
axes[1].legend()

fig.suptitle(f"Frequency response of parallel LC circuit")

plt.show()
    
