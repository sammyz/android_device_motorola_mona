# Hardware validation and fix mapping

Test device: Motorola XT2517-1 (mona), Android 15 V2VAS35.29-49-1.
TWRP: 3.7.1_12-mona-local-verified-layout. These results describe the earlier
hardware-tested build; the publication adds documentation/license comments.

| Symptom | Fix | Verification |
| --- | --- | --- |
| Wrong inherited kernel/layout | Header-v4 ramdisk-only recovery, stock partition sizes | Image header inspection and recovery partition boot |
| Touch unavailable | Matching Goodix module, dependency closure, firmware, modules.dep whitespace, quoted module list | Automatic module loading after reboot; user tested touch |
| Battery incorrectly at 100%, charging unavailable | ADSP/charger modules, modem firmware mount, ADSP start, legacy sysfs battery service | Actual capacity and Charging status; remote processor running |
| EROFS mount permission errors | Explicit read-only mount flags | Runtime mounts passed |
| Reboot returned to recovery | Separate Android v2 recovery.fstab and TWRP v1 twrp.fstab, valid misc entry | BCB command cleared; Android normal boot passed |
| microSD not detected | mmcblk1p1 primary, mmcblk0p1 alternate | FAT32 card mounted at /external_sd, about 29 GB available |
| Center time obscured by camera | 100-pixel theme offset/height correction | User confirmed clock visibility and touch |
| Invalid USB init expansion | Close truncated sys.usb.config property | Init verifier passed |

Source validation: 16 TWRP fstab entries, 268 modules, no missing dependency
files or malformed property expansions. Init scripts passed host_init_verifier.
Packaged module hashes were checked against the captured stock files.

Verified image size: 37965824 bytes; kernel size 0; ramdisk size 37957178.
SHA-256: `1c2f5c6659715b84ab7a5f1474ceb23f67bd14b15f965a84a39c2e0fb7b859fe`.
Installed bytes were read back and matched. Normal Android startup and
recovery persistence passed; Android SELinux was Enforcing.

Encrypted /data remains unsupported. RTC accuracy, USB OTG, backup/restore,
fastbootd, and OTA flashing are not claimed as fully tested.
Private phone logs, serial identifiers, recovery backups and host/VM data
are intentionally excluded from this source contribution.
