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

# optimization setup. See docs:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html

OPT_METHOD = "nelder-mead"  # opt method. Different methods have different options. (IN DICT BELOW). string

INITIAL_STATE = [1.0, 2.0, 0.5]  # initial conditions. list
TOLERANCE = 0.5  # Accepted error for convergence. float

# Define limits (boundaries). tuple of tuples.
BOUNDS = ((0.0, 30.0),  # ChB limits (volts)
          (0.0, 30.0),  # ChC limits (volts)
          (0.0, 30.0))  # ChD limits (volts)

# dictionary to keep the optimizer config
OPT_CONFIG = {
    "initial_state": INITIAL_STATE,  # initial conditions
    "bounds": BOUNDS,  # limits
    "tolerance": TOLERANCE,  # Accepted error for convergence
    "method": OPT_METHOD,
    "opt_options": {'xatol': TOLERANCE,  # Accepted error for convergence
                    'disp': True},  # Display convergence messages
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
log.info("OPTIMIZER CONFIG: method=%s, ic=[%f, %f, %f], tolerance=%f",
         OPT_METHOD, INITIAL_STATE[0], INITIAL_STATE[1], INITIAL_STATE[2], TOLERANCE)


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
# OPTIMIZER TEST (MANUAL)

def opt_test_manual():
    """
    """

    vna_setup()
    dac_setup()
    opt_setup()

    print("\nMANUAL OPTIMIZER TESTING -------------------------------------------------------")

    while True:
        try:
            ch_B = float(input("ch_B="))
            ch_C = float(input("ch_C="))
            ch_D = float(input("ch_D="))

            print("Before:")
            regs = DAC.read_channel_regs_DAC()
            for i, reg in enumerate(regs):
                print(f"Data reg {i} = {reg16_to_str(reg)}")
                # print(f"Data reg {i} = {reg}")

            x = [ch_B, ch_C, ch_D]

            errorval = OPT.opt_func(x, vna=VNA, dac=DAC, masks=MASKS, sweep_config=SWEEP_CONFIG)

            print("After:")
            regs = DAC.read_channel_regs_DAC()
            for i, reg in enumerate(regs):
                print(f"Data reg {i} = {reg16_to_str(reg)}")

            print(f"Voltages [B,C,D] = [{ch_B}, {ch_C}, {ch_D}]\nError value      =  {errorval}")

        except KeyboardInterrupt:
            print("Exit")
            shutdown()
            break

        except Exception as e:
            print(f"Error:\n{str(e)}")
            log.error("Error: %s", str(e))

        # wait for user to confirm exit
        if input("shutdown? [y/n]") in ("y", "Y"):
            shutdown()
            break


# ########################################################################################
# OPTIMIZER LOOP (AUTOMATIC)

res = None
historic = None

def opt_loop():

    vna_setup()
    dac_setup()
    opt_setup()

    print("\nOPTIMIZER LOOP -------------------------------------------------------")

    global res
    global historic

    res = None
    historic = None

    try:
        res, historic = OPT.optimize(vna=VNA, dac=DAC, masks=MASKS, sweep_config=SWEEP_CONFIG, opt_config=OPT_CONFIG)

    except KeyboardInterrupt:
        print("Exit")

    # except Exception as e:
    #     print(f"Error:\n{str(e)}")
    #     log.error("Error: %s", str(e))



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
        print(f"ERROR IN VNA SHUTDOWN:\n{str(e)}")
        log.error("ERROR IN VNA SHUTDOWN: %s", str(e))

    try:
        DAC.power_down_DAC()
    except Exception as e:
        print(f"ERROR IN DAC SHUTDOWN:\n{str(e)}")
        log.error("ERROR IN DAC SHUTDOWN: %s", str(e))

    try:
        DAC.close_SPI()
    except Exception as e:
        print(f"ERROR IN SPI SHUTDOWN:\n{str(e)}")
        log.error("ERROR IN SPI SHUTDOWN: %s", str(e))

    try:
        DAC.close_GPIO()
    except Exception as e:
        print(f"ERROR IN GPIO SHUTDOWN:\n{str(e)}")
        log.error("ERROR IN GPIO SHUTDOWN: %s", str(e))

    print("Shutdown complete")


def reg16_to_str(reg):
    """
    prints a 16bit register
    """
    return f"0x{reg[0]:02X} 0x{reg[1]:02X} | 0b{reg[0]:08b} 0b{reg[1]:08b}"


def dac_test():
    """
    arbitrary test of the DAC
    """
    
    # Setup the DAC (from dac_setup)
    DAC.init_GPIO()  # Init GPIOs
    DAC.init_SPI()  # Init SPI device

    # Read unset control register
    try:
        reg = DAC.read_control_reg_DAC()
        print(f"Control reg, before = {reg16_to_str(reg)}")
        # print(f"Control reg, before = {reg}")
    except Exception as e:
        print(f"Error:\n{str(e)}")
        log.error("Error: %s", str(e))
    
    # DAC.power_up_DAC()  # Set registers in the DAC, power up channels B,C,D
    ctrl_msg = [0x70, 0x38]
    DAC.transfer([0x70, 0x38])
    print(f"Control reg, sent   = {reg16_to_str(ctrl_msg)}")

    # Read changed control register
    try:
        reg = DAC.read_control_reg_DAC()
        print(f"Control reg, after  = {reg16_to_str(reg)}")
        # print(f"Control reg, after  = {reg}")
    except Exception as e:
        print(f"Error:\n{str(e)}")
        log.error("Error: %s", str(e))

    while True:

        try:
            ch_B = int(input("ch_B="))
            ch_C = int(input("ch_C="))
            ch_D = int(input("ch_D="))

            print("Before:")
            regs = DAC.read_channel_regs_DAC()
            for i, reg in enumerate(regs):
                print(f"Data reg {i} = {reg16_to_str(reg)}")
                # print(f"Data reg {i} = {reg}")

            # set arbitrary voltages in DACs
            DAC.set_voltage(vector=[ch_B, ch_C, ch_D])

            print("After:")
            regs = DAC.read_channel_regs_DAC()
            for i, reg in enumerate(regs):
                print(f"Data reg {i} = {reg16_to_str(reg)}")
                # print(f"Data reg {i} = {reg}")

            # measure response, show in screen
            # VNA.measure_once(sweep_config=SWEEP_CONFIG)

        except KeyboardInterrupt:
            print("Exit")
            shutdown()
            break

        except Exception as e:
            print(f"Error:\n{str(e)}")
            log.error("Error: %s", str(e))

        # wait for user to confirm exit
        if input("shutdown? [y/n]") in ("y", "Y"):
            shutdown()
            break


def turn_on_dac():
    print("turning on")
    try:
        DAC.init_GPIO()
        print("turned on")
    except Exception as e:
        print(f"ERROR IN POWERUP:\n{str(e)}")
        log.error("ERROR IN POWERUP: %s", str(e))
        

def turn_off_dac():
    print("turning off")
    try:
        DAC.close_GPIO()
        print("shutdown")
    except Exception as e:
        print(f"ERROR IN SHUTDOWN:\n{str(e)}")
        log.error("ERROR IN SHUTDOWN: %s", str(e))


def power_on_off():
    turn_on_dac()
    input("Press enter to shutdown:")
    turn_off_dac()


def test():
    """
    Define tests to be executed here
    """
    # power_on_off()
    # dac_test()

    # vna_setup()
    # dac_setup()

    # opt_test_manual()

    opt_loop()
    save_results()
    shutdown()


if __name__ == "__main__":
    test()
    sys.exit()
