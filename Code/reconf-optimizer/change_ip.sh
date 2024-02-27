#!/bin/bash

# The VNA has fixed address 10.10.0.152 with mask /8 by default
# This script changes ip address of the interface eth0 to one in the same network as the VNA
# Before running this script, connect the raspberry pi and the VNA together with the same ethernet cable

sudo ip addr add 10.10.0.150/8 dev eth0  # change ip addr
sleep 1  # wait for a moment
ping -c 2 10.10.0.152  # check connectivity

source venv/bin/activate  # activate the virtual environment
