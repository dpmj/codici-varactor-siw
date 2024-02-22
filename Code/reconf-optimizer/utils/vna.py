#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Docstring
Manages the SPI communication with the Rohde-Schwarz ZNB20 VNA using socketscpi
IDN: Rohde-Schwarz,ZNB20-2Port,1311601062101657,3.32
Author: Juan Del Pino Mena 
"""


import socketscpi
import numpy as np


# Defines

DEFAULT_VNA_HOST = "10.10.0.152"  # [str] Instrument IP address.
DEFAULT_VNA_PORT = 5025  # [int] Instrument listening port.
DEFAULT_VNA_TIMEOUT = 10  # [s] How many seconds to wait for a response.

vna = None


def open(host=DEFAULT_VNA_HOST, port=DEFAULT_VNA_PORT, timeout=DEFAULT_VNA_TIMEOUT, 
         verboseErrCheck=False):
    """
    Opens communication with the VNA
    :param host: str, IP address
    :param port: int, port number. Default: 5025
    :param timeout: int, default 10 s
    :param verboseErrCheck: whether the instrument should explain errors. Default: false.
    """
    global vna  # to overwrite the vna object without having to declare a whole ass class

    vna = socketscpi.SocketInstrument(ipAddress=host,
                                      port=port,
                                      timeout=timeout,
                                      verboseErrCheck=verboseErrCheck)


def close():
    """
    Closes communication with the VNA
    """
    vna.close()


def error_check():
    """
    Retrieves errors in the VNA
    """
    vna.err_check()


def identify():
    """
    Identifies the device
    """
    return vna.instId


def setup(sweep_config):
    """
    Performs a reset and setups the VNA with default known parameters. 
    Connection must be opened first.
    :param f_min: lower frequency limit
    :param f_max: upper frequency limit
    :param n_points: number of points for each trace
    """

    # Unpack sweep config for convenience
    f_min = sweep_config["f_min"]
    f_max = sweep_config["f_max"]
    n_points = sweep_config["n_points"]
    
    # ####################################################################################
    # Reset

    vna.write("*RST")  # Reset
    vna.write("INIT:CONT:ALL OFF")  # Disables continuous mode even for new traces
    vna.write("CALC:PAR:DEL:ALL")  # Delete all traces, blanks screen
    vna.write("*WAI")  # Waits until completed before proceeding with next command

    # ####################################################################################
    # Establishes start, stop and number of points
    
    vna.write('SENS:FREQ:STAR ' + str(f_min))  # Set lower frequency bound
    vna.write('SENS:FREQ:STOP ' + str(f_max))  # Set upper frequency bound
    vna.write('SENS:SWE:POIN ' + str(n_points))  # Set number of points per trace
    vna.write("*WAI")  # Waits until completed before proceeding with next command

    # ####################################################################################
    # Creates new traces and measurements. Pag 864
    # Channel 1 (CALC1, number omitted). Measures magnitude in dB and phase in degrees
    # Data will be retrieved in this order
    
    # S11
    vna.write("CALC:PAR:SDEF 'Trc1_mlog', 'S11'")
    vna.write("CALC:PAR:SEL 'Trc1_mlog'")
    vna.write("CALC:FORM MLOG")  # MLOG: Magnitude,dB. Pag 807
    
    vna.write("CALC:PAR:SDEF 'Trc1_phas', 'S11'")
    vna.write("CALC:PAR:SEL 'Trc1_phas'")
    vna.write("CALC:FORM PHAS")  # PHAS: Phase,deg. Pag 807
    
    # S21
    vna.write("CALC:PAR:SDEF 'Trc2_mlog', 'S21'")
    vna.write("CALC:PAR:SEL 'Trc2_mlog'")
    vna.write("CALC:FORM MLOG")
    
    vna.write("CALC:PAR:SDEF 'Trc2_phas', 'S21'")
    vna.write("CALC:PAR:SEL 'Trc2_phas'")
    vna.write("CALC:FORM PHAS")
    
    # S12
    vna.write("CALC:PAR:SDEF 'Trc3_mlog', 'S12'")
    vna.write("CALC:PAR:SEL 'Trc3_mlog'")
    vna.write("CALC:FORM MLOG")
    
    vna.write("CALC:PAR:SDEF 'Trc3_phas', 'S12'")
    vna.write("CALC:PAR:SEL 'Trc3_phas'")
    vna.write("CALC:FORM PHAS")
    
    # S22
    vna.write("CALC:PAR:SDEF 'Trc4_mlog', 'S22'")
    vna.write("CALC:PAR:SEL 'Trc4_mlog'")
    vna.write("CALC:FORM MLOG")
    
    vna.write("CALC:PAR:SDEF 'Trc4_phas', 'S22'")
    vna.write("CALC:PAR:SEL 'Trc4_phas'")
    vna.write("CALC:FORM PHAS")
    
    vna.write("*WAI")  # Waits until completed before proceeding with next command
    
    # ####################################################################################
    # Display traces on the screen. Single sweep (only one measurement)
    
    vna.write("DISP:WIND1:STAT ON")  # Turn on window 1
    
    vna.write("DISP:WIND1:TRAC1:FEED 'Trc1_mlog'")  # Add traces
    vna.write("DISP:WIND1:TRAC2:FEED 'Trc2_mlog'")
    vna.write("DISP:WIND1:TRAC3:FEED 'Trc3_mlog'")
    vna.write("DISP:WIND1:TRAC4:FEED 'Trc4_mlog'")
    
    vna.write("DISP:WIND1:TRAC5:FEED 'Trc1_phas'")
    vna.write("DISP:WIND1:TRAC6:FEED 'Trc2_phas'")
    vna.write("DISP:WIND1:TRAC7:FEED 'Trc3_phas'")
    vna.write("DISP:WIND1:TRAC8:FEED 'Trc4_phas'")
    
    vna.write("INIT:IMM; *WAI")  # Perform a single sweep and wait until completed

    # ####################################################################################
    # Set data format - Swapped byte order, float32.
    
    vna.write('format:border swap')  # Swapped byte order
    vna.write('format real,32')  # 32-bit precision float
    vna.write("*WAI")  # Waits until completed before proceeding with next command

    # ####################################################################################
    # Check errors
    
    vna.err_check()


def measure_once(sweep_config):
    """
    Performs a sweep and measure all data. Returns the measurement as a matrix.
    Connection must be opened first and setup done.

    mat format:
    Npoints rows
    9 cols: f[Hz], s11(mag,pha)[dB], s21 (mag,pha)[dB], s12(mag,pha)[dB], s22(mag,pha)[dB]
    """
        
    # Unpack sweep config
    n_points = sweep_config["n_points"]
    freq = np.array([sweep_config["freq"]]).T  # modify freq so it can be concatenated

    vna.write("INIT:IMM; *WAI")  # Perform a single sweep and wait until completed
    
    vna.write('format:border swap')  # Swapped byte order
    vna.write('format real,32')  # 32-bit precision float
    vna.write("*WAI")  # Waits until completed before proceeding with next command
    
    data = vna.query_binary_values('CALC:DATA:ALL? FDAT', datatype='f')
    
    meas = data.reshape(8, n_points)  # Reshape: 8 columns, of N_POINTS rows.
    meas = meas.T  # traspose

    mat = np.concatenate((freq, meas), axis=1)  # build the measurement s2p matrix
    
    return mat
