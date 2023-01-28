# Automatic frequency response measurement

## Install the python library

Install `visa` as follows

```bash
python3 -m pip install pyvisa pyvisa-py
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

