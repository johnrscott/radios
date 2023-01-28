# Automatic frequency response measurement

## Accessing a shell for testing usbtmc commands

The `universal_usbtmc` python library provides a shell for accessing the usbtmc instrument.

```bash
# Install the universal usbtmc (USB test and measurement class) library
python3 -m pip install universal_usbtmc

# Test the connection (plug the DS1054z in via usb first, and check /dev/usbtmc1 is present)
usbtmc-shell /dev/usbtmc1
``

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

## Install the python library

To use the usbtmc device in python, install `python-usbtmc`:

```bash
sudo apt install libusb-1.0-0
python3 -m pip install python-usbtmc pyusb
```
