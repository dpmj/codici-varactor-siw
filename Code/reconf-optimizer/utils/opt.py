#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""Docstring
Filter optimizer
Authors: 
Juan Del Pino Mena <jdelpin@iteam.upv.es>
Jose Vicente Martínez Sánchez de Rojas <josevmart@iteam.upv.es>
"""


import numpy as np
from scipy.optimize import minimize, Bounds


def add_mask(sparam, orientation, value, flow, fhigh, weight):
    """
    Defines an optimization mask dictionary in a standard format
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
            'flow': flow,  # Lower frequency limit, in GHz
            'fhigh': fhigh,  # Upper frequency limit, in GHz
            'weight': weight}  # Weight in the optimization algorithm


def check_masks(masks, sweep_config):
    """
    Checks mask in a masks list
    :param masks: optimization mask (list of dicts, format: see addwindow() func.)
    :param mat: s2p data matrix,
    """

    # Unpack sweep config for convenience
    f_min = sweep_config["f_min"]
    f_max = sweep_config["f_max"]

    # Define valid parameters
    valid_sparam = ("S11", "S12", "S21", "S22")
    valid_orientation = ("<", ">")

    # Check masks
    for mask in masks:
        
        # unpack mask
        flow = mask['flow']
        fhigh = mask['fhigh']
        sparam = mask['sparam']
        orientation = mask['orientation']
        
        assert flow >= f_min, f"flow cannnot be lower than F_MIN.\nMask: {mask}"
        assert fhigh <= f_max, f"fhigh cannnot be greater than F_MAX.\nMask: {mask}"
        assert flow <= fhigh, f"flow cannnot be greater than fhigh.\nMask: {mask}"
        assert sparam in valid_sparam, f"Unvalid S-param. Allowed: {valid_sparam}\n \
            Mask: {mask}"
        assert orientation in valid_orientation, f"Unvalid orientation. Allowed: \
            {valid_orientation}\nMask: {mask}"


def eval_error(mat, masks, sweep_config):
    """
    Evaluates the error, comparing the filter response to the windows. 

    :param mat: 2-port S-parameter matrix
    :param masks: optimization mask (list of dicts, format: see addwindow() func.)

    mat format:
    n_points rows
    9 cols: f[Hz], s11(mag,pha)[dB], s21 (mag,pha)[dB], s12(mag,pha)[dB], s22(mag,pha)[dB]
    """

    # Unpack sweep config for convenience
    n_points = sweep_config["n_points"]
    freq = sweep_config["freq"]

    # indicates the column index in the s2p matrix where the magnitude of each s-param is. 
    sparam_mag_col = {"S11": 1, "S21": 3, "S12": 5, "S22": 7}
    
    # check matrix dimensions
    valid_shape = (n_points, 9)
    shape = np.shape(mat)

    # check number of rows and cols
    assert shape == valid_shape, f"Unexpected matrix shape: {shape}. \
        Expected: {valid_shape}\n"
    
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
        
        flow_index = (len(freq) - 1) - np.argmax(freq[::-1] <= flow)
        fhigh_index = np.argmax(freq >= fhigh)

        # extracts sub-matrix of relevant s-param values from mat
        s_param_values = mat[flow_index:fhigh_index + 1, sparam_mag_col[sparam]]
        diff = value - s_param_values  # difference vector (how far from value?)
    
        if orientation == '>':  # 'greater than' the 'value'
            mask_error = weight * np.sum(diff[diff > 0])  # only sum if diff > 0
        
        else:  # 'smaller than' the 'value'
            mask_error = weight * np.abs(np.sum(diff[diff < 0]))  # only sum if diff < 0

        error += mask_error

    return error


def opt_func(x, vna, dac, masks, sweep_config):
    """
    Implements the function to optimize.
    Measures from the VNA and sets DAC voltages
    :param x: 3-pos vector which sets the status of the DACs (variables to optimize)
    """
    dac.set_voltage(x)  # Sets DAC channel voltages according to the optimizer
    mat = vna.measure_once(sweep_config)  # Measures the filter response and gets the s2p

    # Evaluates the error with current config
    return eval_error(mat=mat, masks=masks, sweep_config=sweep_config)  


historic = []

def opt_callback(result):
    """
    A callback function which is called at the end of every iteration of the optimization. 
    Saves intermediate data in an historic
    :param intermediate_result: scipy.optimize.OptimizeResult object
    """
    # Iter number, function result, function input variables
    historic.append((result.nit, result.fun, result.x))


def optimize(vna, dac, masks, sweep_config):
    """
    Calls the optimizer on the 
    """
    bounds = Bounds([0, 30],  # ChB limits (volts)
                    [0, 30],  # ChC limits (volts)
                    [0, 30])  # ChD limits (volts)

    x0 = [0, 0, 0]  # initial state

    res = minimize(opt_func,  # variable to optimize
                   x0=x0,  # vector of variables
                   args=[vna, dac, masks, sweep_config],
                   method='nelder-mead', 
                   options={'xatol': 1e-4,  # Accepted error for convergence
                            'disp': True},  # Print convergence messages
                   bounds=bounds,
                   callback=opt_callback)  # variable limits

    return res, historic
