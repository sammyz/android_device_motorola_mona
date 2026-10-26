# Tested recovery image

Codex was used to implement the CLI fix and prepare this publication. The chunks reconstruct the exact flashed and tested image, not a rebuild. They are on this build-only branch to keep binary artifacts out of the upstream device-tree PR.

```sh
cat builds/cli-fd-fix/image.part-* > twrp-mona-cli-fd-fix.img
echo '5d9b6900e7098a006e73dc5307b8ac045e1963c3b2e47ea43e775ca4f978260d  twrp-mona-cli-fd-fix.img' | sha256sum -c -
```

Size: 45,465,600 bytes. See [validation](../../docs/CLI-FD-FIX-VALIDATION.md). The workflow assembles and verifies the image before publishing a prerelease. This is unofficial and tested only on the documented device/firmware.
