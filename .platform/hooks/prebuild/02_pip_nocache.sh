#!/bin/bash
set -e
# Reduce disk footprint during pip install
export PIP_NO_CACHE_DIR=1
# Make sure it's visible to the EB pip step
echo 'export PIP_NO_CACHE_DIR=1' >> /etc/profile.d/pip_nocache.sh
