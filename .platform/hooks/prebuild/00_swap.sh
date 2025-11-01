#!/bin/bash
set -e
# Create a 2GB swap file (helps big wheels compile/extract)
if ! swapon --show | grep -q "/swapfile"; then
  if command -v fallocate >/dev/null 2>&1; then
    fallocate -l 2G /swapfile
  else
    dd if=/dev/zero of=/swapfile bs=1M count=2048
  fi
  chmod 600 /swapfile
  mkswap /swapfile
  swapon /swapfile
fi
