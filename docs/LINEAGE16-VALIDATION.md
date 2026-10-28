# TWRP for the installed mona LineageOS 23.2 hybrid

OpenAI Codex implemented these changes at the user's direction. Existing
SavedByLight, TeamWin, AOSP, Qualcomm and Antigravity contributions and their
notices are preserved. This is a compatibility variant for the tested current
installation, not a universal claim for all Android 16 ROMs or patch levels.

## Artifact and changes

- Version: `3.7.1_12-mona-lineage16-test1`.
- Image: `twrp-mona-lineage16-test1.img`, 45,465,600 bytes.
- SHA256: `6d4bdc0a416721f1b5fee763181a3b50c6094f9e09dfda118432c83668b78770`.
- Installed to recovery_a; active slot A.
- Match running Android release 16 and System patch level 2026-10-01, retain
  the actual stock vendor patch level 2025-05-01, and remove the obsolete boot
  patch alias. The vendor patch in the compiled Lineage Recovery differs from
  the actual installed hybrid's vendor; values were captured from Android.
- Use ext4 read-only/noload for System, System Ext and Product in all three
  fstabs. Preserved vendor partitions continue using EROFS.
- Existing key handling, AIDL Gatekeeper, touch, cutout, default logging and
  CLI close-on-exec fixes remain in place. No credentials were changed.

## Results

The build succeeded. Installed image bytes matched the artifact. The user
confirmed Data is readable, and recovery reports user 0 decrypted.

All 23 non-destructive ADB checks passed: recovery identity, boot-control read
access, advertised USB modes, crypto services, default logging, touch input
registration, battery/backlight sensors, all six logical partition mounts and
reads, DE/CE storage access, temporary write/read/hash checks on DE/CE/microSD,
expected handling of a nonexistent mount, and image/header readback.

A real Data-only backup completed on microSD. All 8 files were copied to F:
and matched fresh source SHA256 hashes. All 3 Data archives matched TWRP's
digests and were fully parsed and their regular-file payloads read without
extracting private contents. Total backup size: 4,046,501,089 bytes; 3,936 tar
entries. Originals remain on microSD. Restore was not performed.

After the backup, LineageOS booted on A with boot_completed=1 and user 0 in
RUNNING_UNLOCKED state. Recovery then booted again, reported user 0 decrypted,
and CE internal storage was accessible. TWRP's normal mount command mounted
System, and its System build-property file was readable alongside Data.

## Limits

Data backup excludes internal-storage media, including photos and Downloads.
This is not a full-device backup, and restore functionality is not claimed as
tested. No wipe, format, metadata erase, credential reset, ROM installation or
slot-B boot was performed. Future ROM/security-patch changes can require
updating the recovery crypto configuration. Private logs, user backups, raw
metadata and imported agy conversation messages must not be published.

## Local source commits

- `ae3352402cc6b706c13cc5bf244193f82a1348ee`: match the installed crypto values.
- `23b749cb58c7309dc458ca11c32bbac4319df904`: recognize ext4 hybrid partitions.

Branch: `mona-lineage16-recovery`. These changes have not been pushed.
