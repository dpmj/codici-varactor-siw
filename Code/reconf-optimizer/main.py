#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Docstring
Reconfigurable SIW Filter optimizer for Raspberry Pi + R&S ZNB20 2-Port VNA

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


import csv
import os
import logging as log
from datetime import datetime

import numpy as np

import utils.dac as DAC
import utils.s2p as S2P
import utils.vna as VNA
import utils.opt as OPT


# ########################################################################################
# CONFIGURATION

HOST = "10.10.0.152"  # [str] Instrument IP address. Default: "10.10.0.152"
PORT = 5025  # [int] Instrument listening port. Default: 5025
TIMEOUT = 10  # [s] How many seconds to wait for a response. Default: 10

F_MIN = 2e9  # [Hz] Default: 2e9 (2 GHz)
F_MAX = 6e9  # [Hz] Default: 6e9 (6 GHz)
N_POINTS = 201  # Number of measurement points. Default: 201

# dictionary that contains the sweep configuration
SWEEP_CONFIG = {
    "f_min": F_MIN,  # minimum frequency
    "f_max": F_MAX,  # maximum frequency
    "n_points": N_POINTS,  # number of points
    "freq": np.linspace(F_MIN, F_MAX, N_POINTS)  # freq vector
}


# ########################################################################################
# TIMESTAMP AND OUTPUT FILES
# Identifies results with the date and time they were ran. 
# Results are saved in a folder named 'outputs/{timestamp}/'
# containing: logs, historic and last-iteration, optimized (or best-effort) s2p parameters

timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

base_folder = f"./output"
folder = f"{base_folder}/{timestamp}"

try:
   os.mkdir(base_folder)
except FileExistsError:
   pass

try:
   os.mkdir(folder)
except FileExistsError:
   pass

log_file = f"{folder}/messages-{timestamp}.log"
s2p_file = f"{folder}/response-{timestamp}.s2p"
csv_file = f"{folder}/historic-{timestamp}.csv"


# ########################################################################################
# LOGGING

logging.basicConfig(filename=logfile, 
                    filemode='a', 
                    format='%(name)s - %(levelname)s - %(message)s')


# ########################################################################################
# WELCOME

print("Reconfigurable SIW Filter optimizer for Raspberry Pi + R&S ZNB20 2-Port VNA")
print(f"Version: {__version__}")
print(f"Author: {__author__} <{__email__}>")
print(f"GAM - iTEAM - UPV - 2024\n\n")
print("----------------------------------------------------------------------")
print(f"TIMESTAMP: {timestamp}")
print(f"SESSION OUTPUTS: {folder}")
print("----------------------------------------------------------------------")

log.info("Reconfigurable SIW Filter optimizer for Raspberry Pi + R&S ZNB20 2-Port VNA")
log.info(f"Version {__version__}")
log.info(f"Author: {__author__} <{__email__}>")
log.info(f"GAM - iTEAM - UPV - 2024")
log.info(f"TIMESTAMP: {timestamp}")
log.info(f"SESSION OUTPUTS: {folder}")
log.info(f"SESSION CONFIG: host={HOST}:{PORT}, timeout={TIMEOUT}, sweep=[{F_MIN}, {F_MAX}, {N_POINTS}]")


# ########################################################################################
# VNA SETUP

print("\n\nVNA SETUP ------------------------------------------------------------")

DEV_IDN = ""

try:
    VNA.open(host=HOST, port=PORT, timeout=TIMEOUT)  # Open connection with the VNA
    print(f"Connection opened with {HOST}:{PORT}, timeout: {TIMEOUT} s")
    log.info(f"Connection opened with {HOST}:{PORT}, timeout: {TIMEOUT} s")

    DEV_IDN = VNA.identify()  # Identifies the instrument
    print(f"Device IDN:\n{DEV_IDN}")
    log.info(f"Device IDN: {DEV_IDN}")

    VNA.setup(SWEEP_CONFIG)  # Reset and setup the instrument to a known base state
    print(f"Sweep configuration set")
    log.info(f"Sweep configuration set")

except Exception as e:
    print(f"ERROR SETTING UP THE VNA:\n{e}")
    log.error(f"ERROR SETTING UP THE VNA:{e}")
    exit()
    

# ########################################################################################
# DAC SETUP

print("\n\nDAC SETUP ------------------------------------------------------------")

try:
    DAC.init_GPIO()  # Init GPIOs
    print("GPIO initialized")
    log.info("GPIO initialized")

    DAC.init_SPI()  # Init SPI device
    print(f"SPI initialized")
    log.info(f"SPI initialized")
    
    DAC.power_up_DAC()  # Set registers in the DAC, power up channels B,C,D
    print(f"DAC channels B,C,D powered up")
    log.info(f"DAC channels B,C,D powered up")

except Exception as e:
    print(f"ERROR SETTING UP THE DAC:\n{e}")
    log.error(f"ERROR SETTING UP THE DAC:{e}")
    exit()


# ########################################################################################
# OPTIMIZER SETUP

print("\n\nOPTIMIZER SETUP ------------------------------------------------------")

# Set goals
MASKS = [] # List of masks (goal windows)
MASKS.append(OPT.add_mask(sparam='S11', orientation='<', value=-20, flow=3, fhigh=3.1, weight=20))
MASKS.append(OPT.add_mask(sparam='S21', orientation='>', value=-2, flow=3, fhigh=3.1, weight=20))
MASKS.append(OPT.add_mask(sparam='S21', orientation='<', value=-15, flow=1, fhigh=2.5, weight=1))
MASKS.append(OPT.add_mask(sparam='S21', orientation='<', value=-15, flow=3.9, fhigh=5.5, weight=1))

# Checks if masks are correctly defined
try:
    OPT.check_masks(masks=MASKS, sweep_config=SWEEP_CONFIG)  
    print("Masks checked")
    log.info(f"Masks checked. Masks: {MASKS}")

except Exception as e:
    print(f"MASKS ARE NOT CORRECTLY SETUP:\n{e}")
    log.error(f"MASKS ARE NOT CORRECTLY SETUP:{e}")
    exit()


# ########################################################################################
# OPTIMIZER LOOP

print("\n\nOPTIMIZER LOOP -------------------------------------------------------")

res = None
historic = None

try:
    res, historic = OPT.optimize(vna=VNA, dac=DAC, masks=MASKS, sweep_config=SWEEP_CONFIG)

except Exception as e:
    print(f"ERROR DURING OPTIMIZATION:\n{e}")
    log.error(f"ERROR DURING OPTIMIZATION:{e}")
    exit()

# ########################################################################################
# SAVE RESULTS

# Write historic into a csv file
with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(historic)

# Save optimized s2p file
mat = VNA.measure_once(sweep_config=SWEEP_CONFIG)  # get optimized measurement 
S2P.mat2file(path=s2p_file, mat=mat, device_idn=DEV_IDN)  # save s2p file

# Output results
print(f"OPTIMIZATION ENDED. Results saved in folder: {folder}") 
print(f"Optimization status: Success={res.success}")
print(f"Optimized varactor voltages={res.x}")
print(f"Optimizer messages: {res.message}")

log.info(f"OPTIMIZATION ENDED. Results saved in folder: {folder}") 
log.info(f"Optimization status: Success={res.success}")
log.info(f"Optimized varactor voltages={res.x}")
log.info(f"Optimizer messages: {res.message}")


# ########################################################################################
# Shutdown everything

print("\n\nSHUTDOWN -------------------------------------------------------------")

try:
    VNA.close()
    DAC.power_down_DAC()
    DAC.close_SPI()
    DAC.close_GPIO()

except Exception as e:
    print(f"ERROR DURING SHUTDOWN:\n{e}")
    log.error(f"ERROR DURING SHUTDOWN:{e}")
    exit()

