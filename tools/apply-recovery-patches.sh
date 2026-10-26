#!/bin/sh
set -eu
device_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
recovery_dir=${1:-bootable/recovery}
patch="$device_dir/patches/0001-settings-storage-and-slot-errors.patch"
if git -C "$recovery_dir" apply --reverse --check "$patch" 2>/dev/null; then
    echo "Recovery settings/slot patch already applied"
else
    git -C "$recovery_dir" apply --check "$patch"
    git -C "$recovery_dir" apply "$patch"
fi
