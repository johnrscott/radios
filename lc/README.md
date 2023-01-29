# Automatic frequency response measurement

This folder contains the calculation of the impedance of a parallel LC circuit. The current through the LC circuit is determined by measuring the voltage across a sense resistor in series with the circuit. the amplitude and phase of this voltage is measured automatically as a function of the input sinusoidal voltage across the LC-circuit-sense-resistor combination using a FeelTech FY6600 signal generator and a Rigol DS1054Z oscilloscope. The measured results and plotted along with the theoretical impedance curve at the end of the script.

The data for the theoretical impedance calculation came from the measured value of inductance and capacitance in the LC circuit, using a standard component tester (based on the one by Karl-Heinz Kubbeler). The experiment was partially to test how accurately this device measures inductance. The results show that the measured inductance (30uH according to the tester) must correspond reasonably closely to the true value of the inductor. 

A capacitor was chosen to make the resonant frequency of the LC circuit as close as possible to BBC Radio Somerset. The target capacitance was 330pF, but the measured capacitance was 303pF, slightly shifting the resonant frequency.

## Running the script

Connect the signal generator and oscillosope to the circuit under test as shown in the comments in lc.py and frequency_response.py. Ensure that the appropriate libraries for serial communication with the signal generator and oscilloscpe are installed (see the sections below for some notes). Then run:

```bash
python3 lc.py
```

The script will write an output file `meas.csv` containing the results of the measurements (there is an example in this folder). After obtaining this file, subsequent runs of the script will ask if you want to simply plot the data in `meas.csv` or rerun the experiment.

Expect the script to take about 20 minutes with 100 frequency points.

## Frequency response measurement

The frequency response measured contains automatic adjustment of the signal generator amplitude level to maintain a given input amplitude level to the circuit under test (greatly reducing the effect of the source impedance of the generator). For each frequency, the timebase and vertical scale of the oscilloscope are automatically adjusted to maintain one cycle of the waveform in the centre of the oscilloscope display. Performing this operation manually was found to be significantly faster than using the autoscale function in the Rigol DS1054 model. 

You can use the FrequencyResponse class in a generic way, provided you write appropriate functions for your oscilloscope and signal generator. The signal generator must be able to set the output amplitude and frequency. 

The oscilloscope must:
* have two channels
* be able to set and retrieve the vertical scale (volts per division)
* be able to set the horizontal scale (seconds per division)
* be able to measure of the peak-to-peak amplitude of each channel waveform
* be able to measure the phase difference between each channel waveform

In addition, it is important to be able to tell when the vertical scale is too small (i.e. the waveform is off the screen). In the DS1054, the amplitude measurement returns nonsense in this case, which is used as the test. If your oscilloscope has an automatic way to adjust the horizontal and vertical scales only (or if the auto mode is sufficiently fast), use that instead of performing the interval bisection to adjust the signal generator voltage.

The phase measurement is particularly noisy, so several samples are taken, with delays in between, in an attempt to average out the noise. Experimentation is required to find the optimimum values of the delay and number of samples.

See the `ds1054.py` and `fy6600.py` for example implementations for these devices.

## Dependencies

Install the `visa` and `serial` libraries

```bash
python3 -m pip install pyvisa pyvisa-py pyserial
```

## Permissions problems accessing usbtmc device

If you find permissions issues when attempting to run Create `/etc/udev/rules.d/usbtmc.rules` and add

```conf
# USBTMC instruments

# Rigol DS1054z
SUBSYSTEMS=="usb", ACTION=="add", ATTRS{idVendor}=="1ab1", ATTRS{idProduct}=="04ce", GROUP="usbtmc", MODE="0660"
```

Save and close. Next create the `usbtmc` group and add yourself to it:

```bash
sudo addgroup usbtmc
sudo usermod -aG usbtmc <your-username>
```

Reboot the computer (for the udev rules), and ensure that `/dev/usbtmc1` has the correct permissions (owner root, group usbtmc):

```bash
ls -la /dev/ | grep usbtmc
# crw-rw----   1 root usbtmc    180,   1 Jan 28 14:24 usbtmc1
```

You should now be able to write to the device (assuming your user is a member of `usbtmc`).

