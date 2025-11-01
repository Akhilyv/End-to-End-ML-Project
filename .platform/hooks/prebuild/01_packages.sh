#!/bin/bash
set -e
# Install build toolchain for heavy ML packages
dnf install -y gcc gcc-c++ make libgomp
