#!/bin/bash
set -e
# Force pip to use disk-backed temp/cache (NOT the tiny /tmp tmpfs)
export TMPDIR=/var/tmp
export PIP_CACHE_DIR=/var/tmp/pipcache
mkdir -p "$PIP_CACHE_DIR"

# Reduce footprint further (safe)
export PIP_NO_CACHE_DIR=1

echo "EB prebuild: TMPDIR=$TMPDIR, PIP_CACHE_DIR=$PIP_CACHE_DIR, PIP_NO_CACHE_DIR=$PIP_NO_CACHE_DIR"
df -h / /tmp /var/tmp || true
