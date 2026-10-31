# LineageOS Device Tree for Motorola mona (Moto G Stylus 2025, XT2517-1)

## Overview
This device tree supports building LineageOS 23.2 (Android 16 QPR2 / Baklava) for the Motorola Moto G Stylus 2025 (`mona`, `XT2517-1`, platform `parrot` / `sm6475`).

## Safe Packaging with Prebuilt Kernel (No Bootloops)
The retail firmware (`V2VAS35.29-49-1`) uses kernel **`6.6.50-android15-8-g0e20c07d648b-ab12946712-4k`**.
To prevent kernel module vermagic mismatches and bootloops with retail firmware components, the ROM installer packages the golden prebuilt 6.6.50 boot stack (`boot.img`, `dtbo.img`, `vendor_boot.img`, `init_boot.img`, `vbmeta.img`, and `vbmeta_system.img`) alongside the freshly compiled LineageOS 23.2 system, system_ext, and product images.

### How to Package the Final ZIP
From the source tree:
```bash
# Run packaging script directly
bash device/motorola/mona/package_mona_zip.sh

# Or with custom output directories:
python3 device/motorola/mona/package_mona_zip.py [out_dir] [prebuilt_dir] [artifacts_dir]
```

### What the Installer Flashes
1. **AVB Disabled VBMeta**: `vbmeta.img` and `vbmeta_system.img` with verification flags disabled (`flags=3`).
2. **Golden Kernel & Boot Stack**:
   - `boot.img` (prebuilt 6.6.50 stock kernel) -> `/dev/block/by-name/boot_a`
   - `dtbo.img` (prebuilt stock DTBO) -> `/dev/block/by-name/dtbo_a`
   - `vendor_boot.img` (prebuilt stock vendor_boot) -> `/dev/block/by-name/vendor_boot_a`
   - `init_boot.img` (tested working init_boot with root/debugging) -> `/dev/block/by-name/init_boot_a`
3. **LineageOS Dynamic Partitions**:
   - `system.img` -> `/dev/block/mapper/system_a`
   - `system_ext.img` -> `/dev/block/mapper/system_ext_a`
   - `product.img` -> `/dev/block/mapper/product_a` (contains 120Hz display lock, disabled auto-brightness, mobile data defaults, and `atel_ui_trigger` MT-SMS service)
4. **Vendor Partition Safeguard**:
   - Strictly preserves the stock retail `vendor` and `vendor_dlkm` partitions on device to ensure 100% driver and vermagic compatibility.
