# Motorola mona: unofficial LineageOS 23.2 hybrid

This publication preserves the seven original Antigravity (agy) commits and their authorship. OpenAI Codex was used to inspect, document and publish this follow-up at sammyz's direction. Original LineageOS, moto-sm8450 maintainers, Motorola, Qualcomm, AOSP and Linux contributor history/notices remain intact. This is an unofficial experimental bring-up, not an official LineageOS release.

## Source trees

- Device: moto-sm8450/android_device_motorola_mona base 2ec6bfca175e818f3aed801216a6321745a8d418; agy head 7764bfaf0755997cb6d096ec2eb2ee47e55306d9 (four commits).
- Common: moto-sm8450/android_device_motorola_sm6475-common base 5811788a3ebf1e55ed3f76db544e1fbf9ac1471d; agy head 8c8f617aa3a4798dc8ce81fc1178c3972eb90662 (three commits).
- Public forks: sammyz/android_device_motorola_mona and sammyz/android_device_motorola_sm6475-common. Branch lineage-23.2-mona-agy preserves the exact original head; lineage-23.2-mona adds publication documentation. TWRP branches remain separate.

See commits.json for the original commit messages and changes. Source bundles require the specified upstream baseline; fetch the baseline repository before importing them.

## Exact ROM artifact

File: lineage-23.2-mona-prebuilt-kernel-installable.zip
Size: 1,067,198,714 bytes
SHA256: 9040a653766873ae13c6016779844c37752a0a76d6ef8df8b40af993e4d7b1c7

Reported running version: 23.2-20261028-UNOFFICIAL-mona, Android 16, System SPL 2026-10-01, stock Motorola Android 15 vendor/boot stack from V2VAS35.29-49-1. The hybrid keeps existing stock vendor/vendor_dlkm/system_dlkm; it is not a full firmware replacement and does not repair unknown firmware on the other slot. Only the tested XT2517-1 configuration is covered.

The installer writes the active slot's boot stack and system/system_ext/product, alters super metadata, formats metadata and may write a Magisk service script to mounted Data. It uses AVB-disabled vbmeta and a root/debug-enabled init_boot. This is a destructive developer installer requiring the matching stock firmware and a verified backup. Use the tested TWRP with lptools and simg2img. Lineage Recovery is not supported by this custom shell ZIP. Do not substitute the original full unofficial OTA ZIP, which bootlooped in earlier tests under both recoveries.

Known installer limits: slot fallback silently assumes A; shell lacks fail-fast/write verification; formatting errors are ignored; /external_sd selection checks directory existence rather than a mounted filesystem. These are preserved agy source/artifact behaviors, not newly fixed or certified by publication. No new build or flashing was performed to publish this exact artifact.

## Recorded validation and limits

Agy reports clean installation to A with Data formatted and successful Android boot. Its October 29 notes report automatic 120Hz (default and peak 120.0; active/render about 120.00001), NR+LTE defaults (33,33), voice/data IN_SERVICE on AT&T, native ATEL hook service startup, and removal of dead RCS service binding. Codex independently checked the host ZIP SHA256 and original source bundles/heads during publication.

Actual new-build call/SMS delivery, cellular transfer, repeated cold boots and RCS client end-to-end activation are not established by registration/service startup alone. The ATEL service is explicitly SELinux permissive. It performs one-shot hook calls without checking their return status, resets default SMS application/display settings at every boot, and the installer also includes a Magisk service.d fallback. Earlier claims that all runtime fixes were independent of scripts must be read with these limits. APN XML is not hardcoded by these changes.

Device/common changes are recorded in their trees, but the build workspace also has build/soong and vendor/lineage changes (ELF/API-lint bypasses and build fixes). Their patches and pinned manifest are attached as provenance; this is not a claim of an otherwise pristine upstream checkout. Existing generated proprietary vendor trees and extraction inputs remain build prerequisites. Build provenance was collected after the builds; it is not a timestamped hermetic build attestation.

## Lineage Recovery source and experimental image

Lineage Recovery uses these same device/common trees, their BoardConfig/fstab/recovery directories, and LineageOS/android_bootable_recovery at acd99f7c48e0229eaedd40aa3e2adcbabe2dc283. No independent recovery device repository is needed. The manifest records additional dependencies.

lineage-23.2-mona-recovery.img: 134,217,728 bytes; SHA256 42faa40d51c2ab5eb3b38bbce40e9dffb37f33b79915c2197e4ece43d4e38a52. Header v4, Android 16 / 2026-10, kernel size zero; no bundled .ko modules. It relies on the installed boot/vendor_boot stack. This newer exact image has not been boot-tested by Codex. Earlier Lineage Recovery tests used a different image (3ae8274c...) and are not validation of this image. Volume/power navigation and no TWRP-style Data backups are expected. It contains no lptools and cannot run this hybrid ZIP's custom installer as supplied. Publish only as a separate experimental prerelease.

## Kernel source and prebuilts

The distributed hybrid uses Motorola's existing stock 6.6.50 kernel image; no new kernel source commit is needed to represent device-tree/packaging changes. Record the corresponding upstream Motorola source instead of pushing unrelated source-built 6.6.144 changes to the user's kernel branches:
https://github.com/MotorolaMobilityLLC/kernel-msm/releases/tag/MMI-V2VAS35.29-49-1
commit eff55482e5fc8c78fb5df52e2d259a0a5d80f23e (Motorola mona Android 15 source release).

This source reference identifies Motorola's matching firmware release; an exact reproducible rebuild of the factory binary has not been demonstrated. It does not identify the LineageOS 6.6.144 checkout as the source of the stock binary. Preserve Motorola/Linux licenses and source availability when redistributing the prebuilt. Supplemental source-built-kernel patches/additional files are attached only for workspace provenance; no modified 6.6.144 kernel binary is part of the hybrid installer or kernel-less recovery image.

No private phone logs, backups, credentials, raw metadata or agy conversation transcripts are published.
