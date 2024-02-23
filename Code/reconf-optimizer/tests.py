#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Docstring

******************************************************************************************
TEST FILE
******************************************************************************************

Reconfigurable SIW Filter optimizer for Raspberry Pi + R&S ZNB20 2-Port VNA

Authors: 
Juan Del Pino Mena <jdelpin@iteam.upv.es>
Jose Vicente Martínez Sánchez de Rojas <josevmart@iteam.upv.es>
"""


__author__ = "Juan Del Pino Mena"
__copyright__ = ""
__credits__ = ["Juan Del Pino Mena", "Jose Vicente Martínez Sánchez de Rojas"]
__license__ = ""
__version__ = "0.0.0"
__maintainer__ = "Juan Del Pino Mena"
__email__ = "jdelpin@iteam.upv.es"
__status__ = ""


import sys
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

TIMESTAMP = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

BASE_FOLDER = "./output"
FOLDER = f"{BASE_FOLDER}/{TIMESTAMP}"

try:
    os.mkdir(BASE_FOLDER)
except FileExistsError:
    pass

try:
    os.mkdir(FOLDER)
except FileExistsError:
    pass

log_file = f"{FOLDER}/messages-{TIMESTAMP}.log"
s2p_file = f"{FOLDER}/response-{TIMESTAMP}.s2p"
csv_file = f"{FOLDER}/historic-{TIMESTAMP}.csv"


# ########################################################################################
# LOGGING

log.basicConfig(filename=log_file, filemode='a', level=log.INFO,
                format='%(name)s - %(levelname)s - %(message)s')


# ########################################################################################
# WELCOME

print("Reconfigurable SIW Filter optimizer for Raspberry Pi + R&S ZNB20 2-Port VNA")
print("**********************************************************************")
print("TEST FILE")
print("**********************************************************************")
print(f"Version: {__version__}")
print(f"Author: {__author__} <{__email__}>")
print("GAM - iTEAM - UPV - 2024\n")
print("----------------------------------------------------------------------")
print(f"TIMESTAMP: {TIMESTAMP}")
print(f"SESSION OUTPUTS: {FOLDER}")
print("----------------------------------------------------------------------")

log.info("Reconfigurable SIW Filter optimizer for Raspberry Pi + R&S ZNB20 2-Port VNA")
log.info("TEST FILE")
log.info("Version: %s", __version__)
log.info("Author: %s <%s>", __author__, __email__)
log.info("GAM - iTEAM - UPV - 2024")
log.info("TIMESTAMP: %s", TIMESTAMP)
log.info("SESSION OUTPUTS: %s", FOLDER)
log.info("SESSION CONFIG: host=%s:%d, timeout=%d, sweep=[%e, %e, %d]",
         HOST, PORT, TIMEOUT, F_MIN, F_MAX, N_POINTS)


# ########################################################################################
# VNA SETUP

DEV_IDN = ""

def vna_setup():

    print("\nVNA SETUP ------------------------------------------------------------")

    global DEV_IDN

    try:
        VNA.open(host=HOST, port=PORT, timeout=TIMEOUT)  # Open connection with the VNA
        print(f"Connection opened with {HOST}:{PORT}, timeout: {TIMEOUT} s")
        log.info("Connection opened with %s:%d, timeout: %d s", HOST, PORT, TIMEOUT)

        DEV_IDN = VNA.identify()  # Identifies the instrument
        print(f"Device IDN:\n{DEV_IDN}")
        log.info("Device IDN: %s", DEV_IDN)

        VNA.setup(SWEEP_CONFIG)  # Reset and setup the instrument to a known base state
        print("Sweep configuration set")
        log.info("Sweep configuration set")

    except Exception as e:
        print(f"ERROR SETTING UP THE VNA:\n{str(e)}")
        log.error("ERROR SETTING UP THE VNA: %s", str(e))
        sys.exit()


# ########################################################################################
# DAC SETUP

def dac_setup():

    print("\nDAC SETUP ------------------------------------------------------------")

    try:
        DAC.init_GPIO()  # Init GPIOs
        print("GPIO initialized")
        log.info("GPIO initialized")

        DAC.init_SPI()  # Init SPI device
        print("SPI initialized")
        log.info("SPI initialized")
        
        DAC.power_up_DAC()  # Set registers in the DAC, power up channels B,C,D
        print("DAC channels B,C,D powered up")
        log.info("DAC channels B,C,D powered up")

    except Exception as e:
        print(f"ERROR SETTING UP THE DAC:\n{str(e)}")
        log.error("ERROR SETTING UP THE DAC: %s", str(e))
        sys.exit()


# ########################################################################################
# OPTIMIZER SETUP

MASKS = [] # List of masks (goal windows)

def opt_setup():

    print("\nOPTIMIZER SETUP ------------------------------------------------------")

    # Set goals
    global MASKS

    MASKS = [] # List of masks (goal windows)
    MASKS.append(OPT.add_mask(sparam='S11', orientation='<', value=-20, flow=3, fhigh=3.1, weight=20))
    MASKS.append(OPT.add_mask(sparam='S21', orientation='>', value=-2, flow=3, fhigh=3.1, weight=20))
    MASKS.append(OPT.add_mask(sparam='S21', orientation='<', value=-15, flow=2, fhigh=2.5, weight=1))
    MASKS.append(OPT.add_mask(sparam='S21', orientation='<', value=-15, flow=3.9, fhigh=5.5, weight=1))

    # Checks if masks are correctly defined
    try:
        OPT.check_masks(masks=MASKS, sweep_config=SWEEP_CONFIG)
        print("Masks checked")
        log.info("Masks checked. Masks: %s", str(MASKS))

    except AssertionError as e:
        print(f"MASKS ARE NOT CORRECTLY SETUP:\n{str(e)}")
        log.error("MASKS ARE NOT CORRECTLY SETUP: %s", str(e))
        sys.exit()


# ########################################################################################
# OPTIMIZER LOOP

res = None
historic = None

def opt_loop():

    print("\nOPTIMIZER LOOP -------------------------------------------------------")

    global res
    global historic

    res = None
    historic = None

    try:
        res, historic = OPT.optimize(vna=VNA, dac=DAC, masks=MASKS, sweep_config=SWEEP_CONFIG)

    except Exception as e:
        print(f"ERROR DURING OPTIMIZATION:\n{str(e)}")
        log.error("ERROR DURING OPTIMIZATION: %s", str(e))
        exit()


# ########################################################################################
# SAVE RESULTS

def save_results():

    # Write historic into a csv file
    with open(csv_file, 'w', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(historic)

    # Save optimized s2p file
    mat = VNA.measure_once(sweep_config=SWEEP_CONFIG)  # get optimized measurement 
    S2P.mat2file(path=s2p_file, mat=mat, device_idn=DEV_IDN)  # save s2p file

    # Output results
    print(f"OPTIMIZATION ENDED. Results saved in folder: {FOLDER}") 
    print(f"Optimization status: Success={res.success}")
    print(f"Optimized varactor voltages={res.x}")
    print(f"Optimizer messages: {res.message}")

    log.info("OPTIMIZATION ENDED. Results saved in folder: %s", FOLDER) 
    log.info("Optimization status: Success=%s", str(res.success))
    log.info("Optimized varactor voltages=%s", str(res.x))
    log.info("Optimizer messages: %s", str(res.message))


# ########################################################################################
# Shutdown everything

def shutdown():

    print("\nSHUTDOWN -------------------------------------------------------------")

    try:
        VNA.close()
    except Exception as e:
        print(f"ERROR DURING SHUTDOWN:\n{str(e)}")
        log.error("ERROR DURING SHUTDOWN: %s", str(e))

    try:
        DAC.power_down_DAC()
    except Exception as e:
        print(f"ERROR DURING SHUTDOWN:\n{str(e)}")
        log.error("ERROR DURING SHUTDOWN: %s", str(e))

    try:
        DAC.close_SPI()
    except Exception as e:
        print(f"ERROR DURING SHUTDOWN:\n{str(e)}")
        log.error("ERROR DURING SHUTDOWN: %s", str(e))

    try:
        DAC.close_GPIO()
    except Exception as e:
        print(f"ERROR DURING SHUTDOWN:\n{str(e)}")
        log.error("ERROR DURING SHUTDOWN: %s", str(e))

    sys.exit()


def dac_test():

    reg = DAC.read_control_reg_DAC()
    print(f"{reg[0]:02X} {reg[1]:02X}")

    while True:
        ch_B = int(input("ch_B="))
        ch_C = int(input("ch_C="))
        ch_D = int(input("ch_D="))

        print("Before:")
        regs = DAC.read_channel_regs_DAC()
        for reg in regs:
            print(f"{reg[0]:02X} {reg[1]:02X}")

        # set arbitrary voltages in DACs
        DAC.set_voltage(vector=[ch_B, ch_C, ch_D])

        print("After:")
        regs = DAC.read_channel_regs_DAC()
        for reg in regs:
            print(f"{reg[0]:02X} {reg[1]:02X}")

        # measure response, show in screen
        VNA.measure_once(sweep_config=SWEEP_CONFIG)

        # wait for user to confirm exit
        if input("shutdown? [y/n]") in ("y", "Y"):
            shutdown()
            break


def test():
    """
    Define tests to be executed here
    """
    vna_setup()
    dac_setup()
    dac_test()


if __name__ == "__main__":
    test()
    sys.exit()
