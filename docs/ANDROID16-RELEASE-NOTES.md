# TWRP mona — Android 16 hybrid Data compatibility (test1)

Unofficial prerelease for the tested XT2517-1 LineageOS 23.2 hybrid: Android 16
System security patch 2026-10-01, stock Motorola Android 15 vendor patch
2025-05-01, and the matching stock 6.6.50 kernel. This is not a universal
Android 16 recovery or the native full-vendor LineageOS configuration.

**OpenAI Codex was used to make all changes in this follow-up, at sammyz's
direction.** SavedByLight's original history/notices, TeamWin, AOSP,
Qualcomm/Linux Foundation, SebaUbuntu/twrpdtgen and prior Antigravity work
remain credited. This artifact retains the previous AIDL Gatekeeper, hardware,
default-logging and CLI descriptor fixes.

## Exact tested artifact

- Version: `3.7.1_12-mona-android16-test1`.
- File: `twrp-mona-android16-test1.img` — 45,465,600 bytes.
- SHA256: `6d4bdc0a416721f1b5fee763181a3b50c6094f9e09dfda118432c83668b78770`.
- Boot header v4, kernel size zero; installed and verified on recovery_a.
- This is the exact tested image, not a rebuild made during publication prep.

## Fixes

Match recovery crypto release/patch properties to the running hybrid system,
retaining its actual stock vendor level. This resolved the observed metadata
key upgrade rejection and restored Data access. Use read-only/noload ext4 for
LineageOS System, System Ext and Product while retaining EROFS for the stock
vendor partitions; System and Data remain readable together.

## Validation

All 23 general ADB checks passed, including crypto services, DE/CE Data access,
all six logical partition reads, temporary write/read/hash checks, default
logging, sensors, expected invalid-mount handling and installed-image readback.

A real Data backup completed: 3 archives, 8 files, 4,046,501,089 bytes and 3,936
tar entries. Host copies matched fresh source SHA256 and TWRP digests; all
archive file payloads were read without extracting private contents. Android
then booted with user 0 unlocked, and a further recovery boot unlocked Data
again. TWRP's normal System mount and System build-property read also passed.

## Limits

Data backup excludes internal-storage media. Restore was not tested. Other
credentials/profiles, patch levels, firmware variants and native full-vendor
Android 16 builds require separate validation. Future ROM updates may require
updating this configuration.

Later Format Data testing exposed a stale userdata device-mapper mapping that
kept the raw device busy; formatting succeeded after the unmounted stale
mapping was removed. Automatic cleanup of that case is not fixed in this
image. Full unofficial-ROM bootloops remained in separate TWRP and Lineage
Recovery install experiments; this release does not claim to fix them.

No private logs, user backups, raw metadata or agy transcripts are included.


Published naming uses `twrp-mona-android16-test1`. The unchanged, previously tested image still reports `3.7.1_12-mona-lineage16-test1` internally; its SHA256 remains unchanged. Source now uses `mona-android16-test1` for subsequent builds. LineageOS references describe the tested ROM, not recovery branding.
