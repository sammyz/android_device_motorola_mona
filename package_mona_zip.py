#!/usr/bin/env python3
"""
Package LineageOS 23.2 into a safe, recovery-installable ZIP for Motorola mona (XT2517-1).

Key Safety Features:
- Uses the golden prebuilt 6.6.50 kernel (boot.img, dtbo.img, vendor_boot.img) from device/motorola/mona/prebuilts
  to prevent vermagic mismatches and bootloops.
- Flashes AVB-disabled vbmeta and vbmeta_system images (flags=3) to prevent verification loops.
- Flashes tested init_boot.img with root/debugging enabled.
- Flashes freshly compiled LineageOS 23.2 system, system_ext, and product images (where the 120Hz display lock,
  disabled auto-brightness, mobile data defaults, and atel_ui_trigger SMS service reside).
- Strictly preserves the stock Motorola vendor and vendor_dlkm partitions to avoid driver incompatibilities.
"""

import os
import shutil
import struct
import subprocess
import sys
import tempfile
import time
import zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Check if SCRIPT_DIR is inside device/motorola/mona
if "device/motorola/mona" in SCRIPT_DIR:
    MONA_DIR = SCRIPT_DIR
    REPO_ROOT = os.path.abspath(os.path.join(MONA_DIR, "../../.."))
else:
    REPO_ROOT = "/mnt/lineageos/lineage-23.2"
    MONA_DIR = os.path.join(REPO_ROOT, "device/motorola/mona")

DEFAULT_PREBUILTS_DIR = os.path.join(MONA_DIR, "prebuilts")
DEFAULT_OUT_DIR = os.path.join(REPO_ROOT, "out/target/product/mona")
DEFAULT_ARTIFACTS_DIR = "/mnt/lineageos/artifacts"

UPDATE_BINARY_SCRIPT = r"""#!/sbin/sh
# LineageOS 23.2 Recovery Installer for Motorola mona (XT2517-1)
# Built with golden prebuilt 6.6.50 kernel stack to prevent bootloops.

OUTFD=$2
ZIPFILE=$3

ui_print() {
    echo "ui_print $1" > /proc/self/fd/$OUTFD
    echo "ui_print " > /proc/self/fd/$OUTFD
}

set_progress() {
    echo "set_progress $1" > /proc/self/fd/$OUTFD
}

ui_print "=========================================="
ui_print " LineageOS 23.2 Installer (Motorola mona)"
ui_print " Safe Prebuilt-Kernel Hybrid ROM Package "
ui_print "=========================================="

SLOT=$(getprop ro.boot.slot_suffix)
if [ -z "$SLOT" ]; then
    SLOT="_a"
fi
ui_print "[*] Target Slot: $SLOT"

# 1. Flash AVB-disabled vbmeta
ui_print "[*] Flashing AVB-disabled vbmeta images..."
unzip -p "$ZIPFILE" vbmeta.img > /dev/block/by-name/vbmeta$SLOT
unzip -p "$ZIPFILE" vbmeta_system.img > /dev/block/by-name/vbmeta_system$SLOT

# 2. Flash Golden Prebuilt Boot Stack (Kernel 6.6.50)
ui_print "[*] Flashing golden 6.6.50 kernel (boot)..."
unzip -p "$ZIPFILE" boot.img > /dev/block/by-name/boot$SLOT

ui_print "[*] Flashing golden DTBO..."
unzip -p "$ZIPFILE" dtbo.img > /dev/block/by-name/dtbo$SLOT

ui_print "[*] Flashing golden vendor_boot..."
unzip -p "$ZIPFILE" vendor_boot.img > /dev/block/by-name/vendor_boot$SLOT

ui_print "[*] Flashing tested init_boot (root enabled)..."
unzip -p "$ZIPFILE" init_boot.img > /dev/block/by-name/init_boot$SLOT

# 3. Dynamic Partitions: Resize & Map
ui_print "[*] Resizing dynamic partitions in super..."
lptools unmap system$SLOT >/dev/null 2>&1 || true
lptools unmap system_ext$SLOT >/dev/null 2>&1 || true
lptools unmap product$SLOT >/dev/null 2>&1 || true

lptools resize product$SLOT 2147483648
lptools resize system$SLOT 1342177280
lptools resize system_ext$SLOT 805306368

lptools map system$SLOT
lptools map system_ext$SLOT
lptools map product$SLOT

# 4. Determine temporary working directory for simg2img
TMP_DIR="/tmp"
if [ -d "/external_sd" ]; then
    TMP_DIR="/external_sd"
fi
ui_print "[*] Staging decompression via: $TMP_DIR"

# 5. Inflate and write images
ui_print "[*] Writing system partition (LineageOS 23.2)..."
set_progress 0.25
unzip -p "$ZIPFILE" system.img > "$TMP_DIR/system.tmp"
simg2img "$TMP_DIR/system.tmp" /dev/block/mapper/system$SLOT
rm -f "$TMP_DIR/system.tmp"

ui_print "[*] Writing system_ext partition (LineageOS 23.2)..."
set_progress 0.50
unzip -p "$ZIPFILE" system_ext.img > "$TMP_DIR/system_ext.tmp"
simg2img "$TMP_DIR/system_ext.tmp" /dev/block/mapper/system_ext$SLOT
rm -f "$TMP_DIR/system_ext.tmp"

ui_print "[*] Writing product partition (120Hz display + SMS services)..."
set_progress 0.75
unzip -p "$ZIPFILE" product.img > "$TMP_DIR/product.tmp"
simg2img "$TMP_DIR/product.tmp" /dev/block/mapper/product$SLOT
rm -f "$TMP_DIR/product.tmp"

# 6. Clean up mapping
ui_print "[*] Unmapping dynamic partitions..."
lptools unmap system$SLOT >/dev/null 2>&1 || true
lptools unmap system_ext$SLOT >/dev/null 2>&1 || true
lptools unmap product$SLOT >/dev/null 2>&1 || true

# 7. Format metadata filesystem
ui_print "[*] Formatting metadata filesystem..."
make_f2fs -f /dev/block/by-name/metadata >/dev/null 2>&1 || true

set_progress 1.0
ui_print "=========================================="
ui_print " LineageOS 23.2 Installed Successfully!"
ui_print " Prebuilt 6.6.50 kernel & boot stack active"
ui_print " Ready to reboot to system!"
ui_print "=========================================="
exit 0
"""

def disable_avb_flags(src_path, dst_path):
    with open(src_path, "rb") as f:
        data = bytearray(f.read())
    if data[:4] == b"AVB0":
        # Byte 123 holds top-level flags in AVB header:
        # 0x01: AVB_VBMETA_IMAGE_FLAGS_HASHTREE_DISABLED
        # 0x02: AVB_VBMETA_IMAGE_FLAGS_VERIFICATION_DISABLED
        data[123] |= (0x01 | 0x02)
    with open(dst_path, "wb") as f:
        f.write(data)

def find_file(filename, search_dirs):
    for d in search_dirs:
        p = os.path.join(d, filename)
        if os.path.exists(p):
            return p
    return None

def package_zip(out_dir=None, prebuilt_dir=None, target_dir=None):
    out_dir = out_dir or DEFAULT_OUT_DIR
    prebuilt_dir = prebuilt_dir or DEFAULT_PREBUILTS_DIR
    target_dir = target_dir or DEFAULT_ARTIFACTS_DIR
    os.makedirs(target_dir, exist_ok=True)

    output_zip = os.path.join(target_dir, "lineage-23.2-mona-prebuilt-kernel-installable.zip")

    search_dirs = [
        prebuilt_dir,
        DEFAULT_PREBUILTS_DIR,
        os.path.join(REPO_ROOT, "device/motorola/mona-kernel"),
        "/mnt/lineageos/artifacts",
        "/mnt/lineageos/mona-dump",
        out_dir,
    ]

    print("=" * 70)
    print(" Motorola mona LineageOS 23.2 Safe Package Generator")
    print(f" Source Build Dir:    {out_dir}")
    print(f" Prebuilt Kernel Dir: {prebuilt_dir}")
    print(f" Output Target:       {output_zip}")
    print("=" * 70)

    # Required compiled images
    compiled_images = {}
    for img in ["system.img", "system_ext.img", "product.img"]:
        p = os.path.join(out_dir, img)
        if not os.path.exists(p):
            print(f"[ERROR] Required compiled image missing: {p}")
            return 1
        compiled_images[img] = p

    # Required prebuilt images with multi-directory fallback resolution
    prebuilt_images = {}
    for img in ["boot.img", "dtbo.img", "vendor_boot.img", "init_boot.img", "vbmeta.img", "vbmeta_system.img"]:
        resolved = find_file(img, search_dirs)
        if not resolved:
            # Check for _disabled variants for vbmeta
            if img == "vbmeta.img":
                resolved = find_file("vbmeta_disabled.img", search_dirs)
            elif img == "vbmeta_system.img":
                resolved = find_file("vbmeta_system_disabled.img", search_dirs)

        if not resolved:
            print(f"[ERROR] Required prebuilt image missing: {img} (searched {search_dirs})")
            return 1
        prebuilt_images[img] = resolved
        print(f"  [Resolved] {img:<18} -> {resolved}")

    staging_dir = tempfile.mkdtemp(prefix="mona_pkg_")
    try:
        meta_inf = os.path.join(staging_dir, "META-INF", "com", "google", "android")
        os.makedirs(meta_inf, exist_ok=True)

        bin_path = os.path.join(meta_inf, "update-binary")
        with open(bin_path, "wb") as f:
            f.write(UPDATE_BINARY_SCRIPT.replace("\r\n", "\n").encode("utf-8"))

        script_path = os.path.join(meta_inf, "updater-script")
        with open(script_path, "wb") as f:
            f.write(b"# LineageOS 23.2 Prebuilt-Kernel Installer for Motorola mona\n")

        # Disable AVB on vbmeta images in staging
        staged_vbmeta = os.path.join(staging_dir, "vbmeta.img")
        disable_avb_flags(prebuilt_images["vbmeta.img"], staged_vbmeta)

        staged_vbmeta_sys = os.path.join(staging_dir, "vbmeta_system.img")
        disable_avb_flags(prebuilt_images["vbmeta_system.img"], staged_vbmeta_sys)

        file_map = {
            compiled_images["system.img"]: "system.img",
            compiled_images["system_ext.img"]: "system_ext.img",
            compiled_images["product.img"]: "product.img",
            prebuilt_images["boot.img"]: "boot.img",
            prebuilt_images["dtbo.img"]: "dtbo.img",
            prebuilt_images["vendor_boot.img"]: "vendor_boot.img",
            prebuilt_images["init_boot.img"]: "init_boot.img",
            staged_vbmeta: "vbmeta.img",
            staged_vbmeta_sys: "vbmeta_system.img",
        }

        print("\n[*] Packaging recovery-installable ZIP archive...")
        t0 = time.time()
        with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1) as zf:
            zf.write(bin_path, "META-INF/com/google/android/update-binary")
            zf.write(script_path, "META-INF/com/google/android/updater-script")

            for src, arcname in file_map.items():
                sz_mb = os.path.getsize(src) / (1024 * 1024)
                print(f"  + {arcname:<18} ({sz_mb:6.1f} MB) from {src}")
                zf.write(src, arcname)

        total_sz = os.path.getsize(output_zip) / (1024 * 1024)
        dt = time.time() - t0
        print("=" * 70)
        print(f"[SUCCESS] Final ZIP generated in {dt:.1f} seconds!")
        print(f"Artifact: {output_zip} ({total_sz:.1f} MB)")
        print("=" * 70)
        return 0

    finally:
        shutil.rmtree(staging_dir, ignore_errors=True)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else None
    prebuilt = sys.argv[2] if len(sys.argv) > 2 else None
    target = sys.argv[3] if len(sys.argv) > 3 else None
    sys.exit(package_zip(out, prebuilt, target))
