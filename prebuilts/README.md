# Prebuilts for Motorola mona (XT2517-1)
This directory contains the golden 6.6.50 boot stack extracted from retail firmware \V2VAS35.29-49-1\ and tested working on physical device \ZA2234TMXP\:
- \oot.img\: Golden stock 6.6.50 kernel
- \dtbo.img\: Golden stock DTBO
- \endor_boot.img\: Golden stock vendor_boot
- \init_boot.img\: Tested root/debugging enabled init_boot
- \bmeta.img\: AVB disabled vbmeta (flags=3)
- \bmeta_system.img\: AVB disabled vbmeta_system (flags=3)

These images are packaged by \package_mona_zip.py\ / \package_mona_zip.sh\ into the recovery-installable ZIP.
