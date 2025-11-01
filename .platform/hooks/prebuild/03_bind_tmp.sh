#!/bin/bash
set -e

# Ensure a big, disk-backed temp area exists
mkdir -p /var/tmp/pip-tmp

# If /tmp is not already a bind mount, bind it to /var/tmp so pip won't hit the small tmpfs
if ! mountpoint -q /tmp; then
  # Clean current /tmp to avoid mount failures due to open files
  rm -rf /tmp/*
  mount --bind /var/tmp /tmp
fi

# Show where /tmp now points and free space (for verification in logs)
echo "EB prebuild: /tmp is now bound to /var/tmp"
mount | grep ' /tmp '
df -h /tmp /var/tmp /
