#!/bin/bash
set -e
# Ensure native toolchain present (needed by NumPy/SciPy/etc.)
dnf -y install gcc-c++ make libgomp
