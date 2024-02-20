#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Docstring
Filter optimizer
Authors: 
Juan Del Pino Mena <jdelpin@iteam.upv.es>
Jose Vicente Martínez Sánchez de Rojas <josevmart@iteam.upv.es>
"""


import numpy as np
from scipy.optimize import minimize


def addwindow(sparam, orientation, value, flow, fhigh, weight):
    """
    Defines an optimization window
    :param sparam: S-parameter to optimize: S11, S12, S21, S22. String.
    :param orientation: orientation: greater than, less than ('<','>')
    :param value: value to compare to in the opt, in dB: e.g.: S11 < -20 (dB)
    :param freq_lim_low: Lower frequency limit of the window, in GHz
    :param freq_lim_high: Upper frequency limit of the window, in GHz
    :param weight: Weight in the optimization algorithm. Scalar.
    :return a standardized dict with the above parameters
    """
    
    return {'sparam': sparam,  # parameter to optimize
            'orientation': orientation,  # orientation: greater than, less than ('<','>')
            'value': value,  # value to compare to in the opt.: e.g.: S11 < -20 (dB)
            'flow': freq_lim_low,  # Lower frequency limit, in GHz
            'fhigh': freq_lim_high,  # Upper frequency limit, in GHz
            'weight': weight}  # Weight in the optimization algorithm


def checkmasks(masks, f_min, f_max):
    """
    Checks mask in a masks list
    :param masks: optimization mask (list of dicts, format: see addwindow() func.)
    :param mat: s2p data matrix,
    """

    valid_sparam = ("S11", "S12", "S21", "S22")
    valid_orientation = ("<", ">")

    for mask in masks:
        
        flow = mask['flow']
        fhigh = mask['fhigh']
        sparam = mask['sparam']
        orientation = mask['orientation']
        
        if flow < f_min:
            raise Exception(f"flow cannnot be lower than F_MIN.\nMask: {mask}")
        if fhigh > f_max:
            raise Exception(f"fhigh cannnot be greater than F_MAX.\nMask: {mask}")
        if flow > fhigh:
            raise Exception(f"flow cannnot be greater than fhigh.\nMask: {mask}")
        if sparam not in valid_sparam:
            raise Exception(f"Unvalid S-param. Allowed: {valid_sparam}\nMask: {mask}")
        if orientation not in valid_orientation:
            raise Exception(f"Unvalid orientation. Allowed: {valid_orientation}\nMask: {mask}")


def evalerror(mat, masks):
    """
    Evaluates the error, comparing the filter response to the windows. 

    :param mat: 2-port S-parameter matrix
    :param masks: optimization mask (list of dicts, format: see addwindow() func.)

    mat format:
    Npoints rows
    9 cols: f[Hz], s11(mag,pha)[dB], s21 (mag,pha)[dB], s12(mag,pha)[dB], s22(mag,pha)[dB]
    """

    # indicates the column index in the s2p matrix where the mangitude of each s-param is. 
    sparam_mag_col = {"S11": 1,
                      "S21": 3,
                      "S12": 5,
                      "S22": 7}
    
    # checkmasks(masks)  # Check masks. This should be done only once at the beginning, but whatever
    
    # check matrix dimensions
    valid_shape = (N_POINTS, 9)
    shape = np.shape(mat)
    if (shape != valid_shape):  # check number of rows and cols
        raise Exception(f"Unexpected matrix shape: {shape}. Expected: {valid_shape}\n")
    
    error = 0  # total error, added in every iteration of mask check
    
    # Calculate the error
    for mask in masks:
        mask_error = 0  # per-mask error. 
    
        sparam = mask['sparam']
        value = mask['value']
        weight = mask['weight']
        orientation = mask['orientation']
        flow = mask['flow'] * 1e9
        fhigh = mask['fhigh'] * 1e9
    
        # Search the low and high frequency indexes that define the window inside the 
        # s2p-matrix, that we will use to calculate the error. If it doesn't match, it'll
        # use the most restrictive case (immediately lower or higher)
    
        # Find the index of the first value that is lower/greater or equal than the 
        # objective frequency. In the argmax() search, the FREQ array is flipped to ensure
        # that the found index does not narrow the defined window.
        
        flow_index = (len(FREQ) - 1) - np.argmax(FREQ[::-1] <= flow)
        fhigh_index = np.argmax(FREQ >= fhigh)

        # extracts sub-matrix of relevant s-param values from mat
        s_param_values = mat[flow_index:fhigh_index + 1, sparam_mag_col[sparam]]
        diff = value - s_param_values  # difference vector (how far from value?)
    
        if orientation == '>':  # 'greater than' the 'value'
            mask_error = weight * np.sum(diff[diff > 0])  # only sum them if diff > 0
        
        else:  # 'smaller than' the 'value'
            mask_error = weight * np.abs(np.sum(diff[diff < 0]))  # only sum them if diff < 0

        error += mask_error

    return error


def optfunc(x, vna, dac, masks):
    """
    Implements the function to optimize.
    Measures from the VNA and sets DAC voltages
    :param x: 3-pos vector which sets the status of the DACs (variables to optimize)
    """

    dac.set_voltage(x)  # Sets DAC channel voltages according to the optimizer
    mat = vna.measure_once()  # Measures the filter response and gets the s2p matrix
    return evalerror(mat=mat, masks=masks)  # Evaluates the error with current config


def optimize(vna, dac, masks):
    """
    Calls the optimizer on the 
    """

    bounds = Bounds([0, 30],  # ChB limits (volts)
                    [0, 30],  # ChC limits (volts)
                    [0, 30])  # ChD limits (volts)

    x0 = [0, 0, 0]  # initial state

    res = minimize(optfunc,  # variable to optimize
                   x0=x0,  # vector of variables
                   args=[vna, dac, masks],
                   method='nelder-mead', 
                   options={'xatol': 1e-4,  # Accepted error for convergence
                            'disp': True},  # Print convergence messages
                   bounds=bounds)  # variable limits

    return res


