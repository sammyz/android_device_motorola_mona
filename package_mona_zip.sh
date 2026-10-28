#!/usr/bin/env bash
#
# package_mona_zip.sh
# Package LineageOS 23.2 for Motorola mona (XT2517-1) using the golden prebuilt 6.6.50 kernel
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEVICE_DIR="${SCRIPT_DIR}"
REPO_ROOT="$(cd "${DEVICE_DIR}/../../.." && pwd)"

OUT_DIR="${1:-${REPO_ROOT}/out/target/product/mona}"
PREBUILT_DIR="${2:-${DEVICE_DIR}/prebuilts}"
ARTIFACT_DIR="${3:-/mnt/lineageos/artifacts}"

echo "=== [$(date)] Packaging LineageOS mona with Prebuilt Kernel ==="
python3 "${DEVICE_DIR}/package_mona_zip.py" "${OUT_DIR}" "${PREBUILT_DIR}" "${ARTIFACT_DIR}"
echo "=== [$(date)] Packaging complete! ==="
