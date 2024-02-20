#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Docstring
Reconfigurable SIW Filter optimizer.
Authors: 
Juan Del Pino Mena <jdelpin@iteam.upv.es>
Jose Vicente Martínez Sánchez de Rojas <josevmart@iteam.upv.es>
"""


__author__ = "Juan Del Pino Mena"
__copyright__ = ""
__credits__ = ["Juan Del Pino Mena", "Jose Vicente Martínez Sánchez de Rojas"]
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "Juan Del Pino Mena"
__email__ = "jdelpin@iteam.upv.es"
__status__ = ""


import logging as log
from datetime import datetime

import numpy as np

import utils.dac as DAC
import utils.s2p as S2P
import utils.vna as VNA
import utils.opt as OPT


# ########################################################################################
# LOGGING CONFIGURATION

logfile = datetime.now().strftime("logs/reconf-%Y-%m-%d-%H-%M.log")
logging.basicConfig(filename=logfile, 
                    filemode='a', 
                    format='%(name)s - %(levelname)s - %(message)s')


# ########################################################################################
# VNA & SWEEP CONFIGURATION

HOST = "10.10.0.152"  # [str] Instrument IP address. Default: "10.10.0.152"
PORT = 5025  # [int] Instrument listening port. Default: 5025
TIMEOUT = 10  # [s] How many seconds to wait for a response. Default: 10

F_MIN = 2e9  # [Hz] Default: 2e9 (2 GHz)
F_MAX = 6e9  # [Hz] Default: 6e9 (6 GHz)
N_POINTS = 201  # Number of measurement points. Default: 201


VNA.open(host=HOST, port=PORT, timeout=TIMEOUT)  # Open connection with the VNA
VNA.setup(f_min=F_MIN, f_max=F_MAX, n_points=N_POINTS)  # Reset and setup the instrument.


# ########################################################################################
# DAC CONFIGURATION

DAC.init_GPIO()  # Init GPIOs
DAC.init_SPI()  # Init SPI device
DAC.powerup_DAC()  # Set registers in the DAC, power up channels B,C,D


# ########################################################################################
# OPTIMIZER CONFIGURATION

# Set goals - masks

MASKS = [] # List of masks (goal windows)
MASKS.append(OPT.addwindow('S11', '<', -20, 3, 3.1, 20))
MASKS.append(OPT.addwindow('S21', '>',  -2, 3, 3.1, 20))
MASKS.append(OPT.addwindow('S21', '<', -15, 1, 2.5, 1))
MASKS.append(OPT.addwindow('S21', '<', -15, 3.9, 5.5, 1))

OPT.checkmasks(masks=MASKS, f_min=F_MIN, f_max=F_MAX)  # Checks if masks are correcly defined


# Optimizer loop

res = OPT.optimize(vna=VNA, dac=DAC, masks=MASKS)  # Optimize

print(res.x)



# ########################################################################################
# Shutdown everything

VNA.close()
DAC.powerdown_DAC()
DAC.close_SPI()
DAC.close_GPIO()


