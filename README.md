# TWRP device tree for Motorola mona

Moto G Stylus (2025), tested on **XT2517-1** with Android 15
`V2VAS35.29-49-1` and kernel
`6.6.50-android15-8-g0e20c07d648b-ab12946712-4k`.

## Credits and history

This is a fork of [SavedByLight/android_device_motorola_mona](https://github.com/SavedByLight/android_device_motorola_mona),
based on its `android-12.1` commit `6e12663c80cfd49db19dc7882c3d936e5d96b99d`.
SavedByLight's original commits, boot-control/GPT code, initialization work,
and existing file notices are retained. The original generated tree credits
The Android Open Source Project and SebaUbuntu's TWRP device tree generator
(Apache-2.0); Qualcomm/Linux Foundation notices remain in their files.

The [twrpdtgen mona tree](https://github.com/twrpdtgen/android_device_motorola_mona/tree/mona-user-15-V2VAS35V.29-49-ST2.4-6a189-release-keys)
at `0849e7941312418ebb4b8fef5e61c1a3835f16dd` was reviewed for comparison.
It was not the working-tree base and no commits from it were cherry-picked.
Codex was used to make **all changes in this contribution**, at sammyz's
direction. The resulting recovery was tested on sammyz's phone, with
sammyz confirming touch and clock visibility. TWRP itself is provided by
TeamWin and its contributors.

Stock kernel modules and touch firmware are **prebuilt binaries extracted
from the tested Motorola firmware**, not newly authored driver source.
Their provenance and hashes are in `docs/stock-prebuilts.json`; existing
binary licensing is not replaced by the device-tree source notices.
The old `prebuilt/kernel` and `prebuilt/dtb.img` remain as inherited history
but are not used by this ramdisk-only recovery configuration.

## Build

Use the [minimal TWRP AOSP manifest](https://github.com/minimal-manifest-twrp/platform_manifest_twrp_aosp)
branch `twrp-12.1`. `docs/platform-manifest.xml` pins the platform revisions
used for the verified build. From a Linux TWRP checkout, place this tree at
`device/motorola/mona`, then run:

```sh
python3 device/motorola/mona/tools/check-tree.py
export ALLOW_MISSING_DEPENDENCIES=true
source build/envsetup.sh
lunch twrp_mona-eng
mka -j4 recoveryimage
```

Output: `out/target/product/mona/recovery.img`. The stock recovery partition
is 134217728 bytes; header version is 4 and kernel size must be **zero**.
The installed stock kernel must match the bundled modules. This is not a
general compatibility claim for other firmware or model variants.

## Verified behavior and limits

See [validation and fix mapping](docs/VALIDATION.md). Touch, microSD,
charging/battery readings, cutout clearance, EROFS mounts, normal Android
reboot, and persistence of recovery were verified on the test device.

**Android 15 wrapped-key /data decryption is unsupported.** Internal-storage
mount errors remain; use microSD or ADB sideload. RTC wall-clock time may
require manual adjustment. USB initialization parses, but file transfer,
USB OTG, fastbootd, backup/restore and OTA installation have not all received
end-to-end testing. This is an unofficial recovery.

The tested image was installed to recovery_a only, after backing up both
stock recovery slots. Android booted with its original fingerprint and
SELinux Enforcing. A temporary `fastboot boot` attempt entered Android with
the installed normal ramdisk and did not test recovery; validate through
the appropriate recovery partition. No userdata formatting was performed.
