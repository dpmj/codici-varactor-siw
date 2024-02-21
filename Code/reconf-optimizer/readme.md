# optimizer using R&S ZNB VNA 

- **Author:** Juan del Pino Mena
- **Version:** v01
- **Date:** 2024-02-21


# Introduction 

## Requirements

- An updated version of Python 3
- `RPi.GPIO`: For accessing the GPIO on the Raspberry Pi
- `numpy`: For vector manipulation
- `scipy`: For the optimization algorithms
- `socketscpi`: For communication with SCPI commands over sockets.
    - docs: https://socketscpi.readthedocs.io/en/latest/index.html
    - original repo: https://github.com/morgan-at-keysight/socketscpi
    - backup fork in case it's unavailable: https://github.com/dpmj/socketscpi

Execute this code on a virtual environment for safety. In the root folder of this code (reconf-optimizer, where `main.py` is):
```bash
python -m venv venv  # creates the virtual environment named venv on folder ./venv/
source venv/bin/activate  # activates the virtual environment
pip install -r requirements.txt  # automatically installs any required dependencies
```

# Network configuration

## Remote access to the Raspberry Pi

The Raspberry Pi will automatically boot headless (with no graphical interface). The SSH service is enabled, VNC is disabled. To transfer files from your computer to the Raspberry Pi, you can use the SFTP transfer protocol with a FTP client such as Filezilla. 

The Raspberry Pi should be configured to auto-connect to a wifi named `lcafwifi` with password `lcafgam12`. Create this wifi hotspot with a laptop or smartphone. 

Once connected, access the Raspberry Pi command line with:
```bash
ssh pi@raspberrypi.local
```
Password for user `pi` is `raspberry`. In case the `raspberrypi.local` name is not resolved, you must find out the Raspberry Pi's IP address manually.


## Connection between the Raspi and the VNA.  

Once with remote access to the Pi, you must configure the network between the VNA and the Raspberry.

By default, the VNA has fixed address 10.10.0.152 with mask /8. This is tedious to change, so the easier way is to configure the Raspi's interface instead. 
Physically connect the VNA and the Raspberry Pi together with an Ethernet cable. Then, execute the script:
```bash
sh ./change_ip.sh
```
This script changes ip address of the interface eth0 to one in the same network as the VNA (`10.10.0.150/8`) and performs a connectivity check with `ping`. You should see that the pings are successful.


# Usage

## Calibration

Ensure the VNA is properly calibrated before measuring. There shall be a calibration file already available and suitable on the VNA. Go to CAL >> USE CAL >> CAL MANAGER. In the Pool (right window), select "Reconf-Filter-2-6G-201". Contains the calibration data for a 2-to-6 GHz bandwidth with 201 points per trace using the Agilent 85052C calibration kit. Once selected, click "Apply" on the center of the screen.

If you need another measurement range and/or another number of points per trace, you'll need to apply a different calibration or calibrate manually. Save the calibration in the calibration manager in case you'll need it again.





