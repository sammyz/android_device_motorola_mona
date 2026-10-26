#!/system/bin/sh
# Persistent diagnostics for the mona recovery/decryption investigation.
# Codex implementation; keep enabled until reliable data access is established.
lock=/tmp/mona-recovery-logger.lock
mkdir "$lock" 2>/dev/null || exit 0
logcat_pid=
cleanup() {
    [ -z "$logcat_pid" ] || kill "$logcat_pid" 2>/dev/null
    rmdir "$lock" 2>/dev/null
}
trap cleanup EXIT
trap 'exit 0' HUP INT TERM
sd_mounted() { awk '$2 == "/external_sd" { found=1 } END { exit !found }' /proc/mounts; }
while ! sd_mounted; do
    mkdir -p /external_sd
    [ ! -b /dev/block/mmcblk1p1 ] || mount -t vfat /dev/block/mmcblk1p1 /external_sd 2>/dev/null
    sleep 1
done
boot_id=$(cat /proc/sys/kernel/random/boot_id)
dir=/external_sd/twrp_logs/boot-$boot_id
mkdir -p "$dir" || exit 1
printf '%s\n' "$dir" >/tmp/mona-recovery-logdir
printf '%s\n' "$dir" >/external_sd/twrp_logs/latest.txt
echo "logger started: $(date)" >>"$dir/logger.txt"
logcat -b all -v threadtime -f "$dir/logcat.txt" -r 2048 -n 4 2>>"$dir/logger.txt" &
logcat_pid=$!
for p in /sys/fs/pstore/*; do
    [ ! -f "$p" ] || cp "$p" "$dir/previous-$(basename "$p")"
done
count=0
while sd_mounted; do
    if [ -f /tmp/recovery.log ]; then
        cp /tmp/recovery.log "$dir/recovery.log"
        cp /tmp/recovery.log /external_sd/twrp_logs/current_recovery.log
    fi
    if [ $((count % 5)) -eq 0 ]; then
        dmesg >"$dir/dmesg.txt" 2>>"$dir/logger.txt"
        {
            date
            cat /proc/mounts
            ls -l /dev/block/mapper
            getprop ro.twrp.version
            getprop ro.boot.slot_suffix
            getprop init.svc.vendor.keymint-qti
            getprop init.svc.vendor.qseecomd
            getprop init.svc.keystore2
        } >"$dir/state.txt" 2>&1
    fi
    sync
    count=$((count + 1))
    sleep 2
done
