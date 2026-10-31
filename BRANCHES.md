# Repository branches

This repository contains two different device configurations. They share a phone, not a build tree.

| Branch | Purpose |
| --- | --- |
| [android-12.1](https://github.com/sammyz/android_device_motorola_mona/tree/android-12.1) | Maintained TWRP source, including merged Android 16 hybrid Data compatibility changes. The name identifies the TWRP source platform, not the Android version installed on the phone. |
| [lineage-23.2](https://github.com/sammyz/android_device_motorola_mona/tree/lineage-23.2) | LineageOS 23.2 Android 16 device tree, including the merged agy bring-up commits and publication documentation. |

Use [Releases](https://github.com/sammyz/android_device_motorola_mona/releases) for downloadable images and ROM ZIPs. Firmware requirements and limitations remain in each release's notes. LineageOS and TWRP source must not be merged into each other.

## Consolidation on 2026-10-31

PR #1 had already merged mona-android16-recovery into mona-recovery-fixes, and PR #2 had already merged lineage-23.2-mona into lineage-23.2. The default android-12.1 branch was fast-forwarded to the merged TWRP source, preserving its complete upstream and local history. Original agy commit IDs are preserved as ancestors of lineage-23.2, including head 7764bfaf0755997cb6d096ec2eb2ee47e55306d9.

Redundant source pointers mona-recovery-fixes, mona-android16-recovery, lineage-23.2-mona and lineage-23.2-mona-agy were removed only after verifying their tips are ancestors of their retained branch.

Build artifact branches were preserved as tags rather than merged into source:
- [archive/twrp-android16-builds-20261031](https://github.com/sammyz/android_device_motorola_mona/tree/archive/twrp-android16-builds-20261031): tip 2fc00b544dbaac2ae1e101c12afcdc28757b4334, including the renamed builds/android16-test1 directory and all twelve unchanged artifact files.
- [archive/twrp-android15-builds-20261031](https://github.com/sammyz/android_device_motorola_mona/tree/archive/twrp-android15-builds-20261031): tip e2627d913b1de43754f82cded3b9c56cb8da0a01, also retained by its existing release tag.

All releases and existing release tags remain. No source commits were squashed, rewritten or discarded; no binary was rebuilt or changed. Only documentation and repository refs changed. Codex performed the consolidation at sammyz's request; original contributors and agy credits remain intact.
