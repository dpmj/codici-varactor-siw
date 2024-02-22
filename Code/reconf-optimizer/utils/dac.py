#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Docstring
Manages the SPI communication with the AD5504 DAC
Authors: Jose Vicente Martínez Sánchez de Rojas, Juan Del Pino Mena 
"""

import RPi.GPIO as GPIO  # GPIOs
import spidev  # SPI bus


# Defines

DEFAULT_LDAC_PIN = 25  # GPIO pin for LDAC. Default = 25
DEFAULT_CLR_PIN = 5  # GPIO pin for CLR. Default = 5

DEFAULT_SPI_DEV = 1  # SPI device number. Default = 1
DEFAULT_SPI_FREQ = int(16e6)  # SPI clk frequency. Default = int(16e9)

spi = None


def init_GPIO(LDAC=DEFAULT_LDAC_PIN, CLR=DEFAULT_CLR_PIN):  
    """
    Initializes DAC GPIO ports
    :param LDAC: port number for LDAC
    :param CLR: port number for CLR
    """
    GPIO.setmode(GPIO.BCM)

    # Set a LDAC pulse
    GPIO.setup(LDAC, GPIO.OUT)
    GPIO.output(LDAC, 0)

    # Set a CLR level
    GPIO.setup(CLR, GPIO.OUT)
    GPIO.output(CLR, 1)


def close_GPIO():
    """
    Resets GPIOs
    """
    GPIO.cleanup()


def init_SPI(device=DEFAULT_SPI_DEV, freq=DEFAULT_SPI_FREQ):
    """
    Initializes SPI device at specified frequency
    :param device: SPI device number, integer
    :param freq: SPI clock frequency (Hz), integer
    """
    global spi  # dirty but works
    spi = spidev.SpiDev()  # Redefining SPI object -- Not pretty but works
    bus = 0
    spi.open(bus,device)
    spi.max_speed_hz = freq


def close_SPI():
    """
    Closes SPI connection and resets GPIOs
    """
    spi.close()


def power_up_DAC():
    """
    Writes configuration to AD5504 control register. See AD5504 datasheet, page 16
    0x70 : 0111 0000 : RW=0, A1=1,A2=1,A3=1 (writing to the control register)
    0x38 : 0011 1000 : ChB,ChC,ChD power up (ChA power down)
    """

    # xfer2: Performs an SPI transaction. Chip-select should be held active between blocks
    spi.xfer2([0x70, 0x38])  


def power_down_DAC():
    """
    Writes configuration to AD5504 control register. See AD5504 datasheet, page 16
    0x70 : 0111 0000 : RW=0, A1=1,A2=1,A3=1 (writing to the control register)
    0x38 : 0000 0000 : All channels power down
    """

    spi.xfer2([0x70, 0x00])


def set_voltage(vector):
    """
    Sets a voltage in the DACs
    :param vector: 3-position vector of voltages to set according to each channel
    """

    for j, voltage in enumerate(vector):

        # clips voltages to the maximum=30 and minimum=0, for safety
        if voltage < 0:
            voltage = 0
        elif voltage > 30:
            voltage = 30

        # transforms the digit into a 12-bit range
        # // : floor division
        digit = int((voltage * 4095) // 30)  # important! 4095, not 4096!

        digit_bytes = digit & 0x0FFF  # mask : put 0's in the leftmost part
        digit_bytes = digit_bytes | ((int(j + 2)) << 12)  # select channel

        # Divide the 2 bytes in two bytes: 8 MSB (high part) and 8 LSB (low part)
        b = digit_bytes  # it's going to be clipped at its 8 LSB by the function
        a = digit_bytes >> 8  # high part

        spi.xfer2([a, b])
