#!/bin/bash
set -euo pipefail

# Ensure disk-backed temp area
mkdir -p /var/tmp
chmod 1777 /var/tmp

# If /tmp is a tmpfs (RAM), replace it with a bind to /var/tmp
if mount | grep -E ' on /tmp type tmpfs' > /dev/null; then
  echo "EB prebuild: Rebinding /tmp from tmpfs to /var/tmp ..."
  # copy anything already in /tmp to /var/tmp (best-effort)
  cp -a /tmp/. /var/tmp/ 2>/dev/null || true

  # Try normal unmount; if busy, do a lazy unmount
  umount /tmp 2>/dev/null || umount -l /tmp

  # Bind-mount disk-backed /var/tmp onto /tmp
  mount --bind /var/tmp /tmp
fi

echo "EB prebuild: /tmp now points to:"
mount | grep ' /tmp '
df -h /tmp /var/tmp /
