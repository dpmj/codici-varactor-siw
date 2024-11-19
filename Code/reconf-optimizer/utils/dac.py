#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Docstring
Manages the SPI communication with the AD5504 DAC
Authors: Jose Vicente Martínez Sánchez de Rojas, Juan Del Pino Mena 
"""

import RPi.GPIO as GPIO  # GPIOs
import spidev  # SPI bus


# Defines

DEFAULT_ENABLE_PIN = 18  # GPIO pin for DC/DC ENABLE

DEFAULT_LDAC_PIN = 25  # GPIO pin for LDAC. integer. Default = 25
DEFAULT_CLR_PIN = 5  # GPIO pin for CLR. integer. Default = 5

DEFAULT_SPI_BUS = 0  # SPI bus. integer. Default = 0
DEFAULT_SPI_DEV = 1  # SPI device number. integer. Default = 1
DEFAULT_SPI_FREQ = 1000000  # SPI clk frequency. integer. Max. (read operation) = 9 MHz
DEFAULT_SPI_MODE = 1  # spi mode: https://pypi.org/project/spidev/ https://picockpit.com/raspberry-pi/spi-the-serial-peripheral-interface/

spi = None


def init_GPIO(LDAC=DEFAULT_LDAC_PIN, CLR=DEFAULT_CLR_PIN, ENABLE=DEFAULT_ENABLE_PIN):  
    """
    Initializes DAC GPIO ports
    :param LDAC: port number for LDAC
    :param CLR: port number for CLR
    """
    GPIO.setmode(GPIO.BCM)

    # Set a LDAC pulse
    # LDAC PIN: Load DAC Input. Pulsing this pin low allows any or all DAC registers to be
    # updated if the input registers have new data. This allows all DAC outputs to update
    # simultaneously. Alternatively, this pin can be tied permanently low.
    GPIO.setup(LDAC, GPIO.OUT)
    GPIO.output(LDAC, 0)

    # Set a CLR level
    # Asynchronous Clear Input. The CLR input is falling edge sensitive. When CLR is low,
    # all LDAC pulses are ignored. When CLR is high, the input register and the DAC
    # register are set to 0x000 and the outputs to zero scale.
    GPIO.setup(CLR, GPIO.OUT)
    GPIO.output(CLR, 1)

    # Enable DC/DC converter
    # Power on the Raspi HAT
    GPIO.setup(ENABLE, GPIO.OUT)
    GPIO.output(ENABLE, 1)


def close_GPIO(LDAC=DEFAULT_LDAC_PIN, CLR=DEFAULT_CLR_PIN, ENABLE=DEFAULT_ENABLE_PIN):
    """
    Resets GPIOs. SPI should be closed first (close_SPI())
    """
    GPIO.output(CLR, 1)  # Clear registers
    GPIO.output(ENABLE, 0) # Power down the Raspi HAT
    GPIO.cleanup()  # Deactivate GPIOs. 


def init_SPI(bus=DEFAULT_SPI_BUS, device=DEFAULT_SPI_DEV, freq=DEFAULT_SPI_FREQ, mode=DEFAULT_SPI_MODE):
    """
    Initializes SPI device at specified frequency
    :param device: SPI device number, integer
    :param freq: SPI clock frequency (Hz), integer
    """
    global spi  # Not pretty but works

    spi = spidev.SpiDev()  # Redefining SPI object

    spi.open(bus, device)  # bus 0, device 1
    spi.max_speed_hz = freq  # 16 MHz 
    spi.mode = mode  # mode = 1
    spi.lsbfirst = False
    # spi.bits_per_word = 8
    # spi.cshigh = True
    # spi.loop = False
    # spi.threewire = False
    # spi.read0 = False


def close_SPI():
    """
    Closes SPI connection.
    """
    spi.close()


def power_up_DAC():
    """
    Writes configuration to AD5504 control register. 
    """
    # See AD5504 datasheet, page 16, 17
    # HIGH PART = 0x70 : 0111 0000 : RW=0, A1=1, A2=1, A3=1: writing to the control reg
    # LOW PART  = 0x38 : 0011 1000 : ChA power down; ChB, ChC, ChD power up,
    #                                outputs connected to AGND through a 20 kOhm resistor

    spi.xfer2([0x70, 0x38])  # Write to the control reg
    # xfer2: Performs an SPI transaction. Chip-select should be held active between blocks

    # A write to the control register must be followed by another write operation. The
    # second write operation can be a write to a DAC input register or a NOP write
    spi.xfer2([0x00])  # No Operation (NOP) write


def read_control_reg_DAC():
    """
    Reads the control register of the AD5504 DAC
    """
    return spi.xfer2([0xF0, 0x00])


def read_channel_regs_DAC():
    """
    Reads a channel registers of the AD5504 DAC
    """
    values = []
    values.append(spi.xfer2([0x90, 0x00]))
    values.append(spi.xfer2([0xA0, 0x00]))
    values.append(spi.xfer2([0xB0, 0x00]))
    values.append(spi.xfer2([0xC0, 0x00]))

    return values


def transfer(data):
    """
    spi.xfer2() wrapper
    """
    return spi.xfer2(data)


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
        b = digit_bytes  # Low part -- it's going to be clipped at 8 LSB by the xfer2 function
        a = digit_bytes >> 8  # high part

        spi.xfer2([a, b])
