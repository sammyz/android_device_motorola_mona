#
# Copyright (C) 2022 The LineageOS Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

DEVICE_PATH := device/motorola/mona

# Inherit from motorola sm6475-common
include device/motorola/sm6475-common/BoardConfigCommon.mk

# Bootloader
TARGET_BOOTLOADER_BOARD_NAME := mona

# Kernel
ifeq (,$(TARGET_PREBUILT_KERNEL))
TARGET_KERNEL_CONFIG += \
	vendor/ext_config/moto-parrot-mona.config
else
# Kernel Modules
PREBUILT_KERNEL_PATH := $(dir $(TARGET_PREBUILT_KERNEL))
BOARD_PREBUILT_DTBIMAGE_DIR := $(PREBUILT_KERNEL_PATH)/dtbs
BOARD_PREBUILT_DTBOIMAGE := $(PREBUILT_KERNEL_PATH)/dtbo.img
BOARD_SYSTEM_KERNEL_MODULES := $(wildcard $(PREBUILT_KERNEL_PATH)/system_dlkm/*.ko)
BOARD_SYSTEM_KERNEL_MODULES_LOAD := $(patsubst %,$(PREBUILT_KERNEL_PATH)/system_dlkm/%,$(shell cat $(PREBUILT_KERNEL_PATH)/system_dlkm/modules.load))
BOARD_VENDOR_KERNEL_MODULES := $(wildcard $(PREBUILT_KERNEL_PATH)/vendor_dlkm/*.ko)
BOARD_VENDOR_KERNEL_MODULES_LOAD := $(patsubst %,$(PREBUILT_KERNEL_PATH)/vendor_dlkm/%,$(shell cat $(PREBUILT_KERNEL_PATH)/vendor_dlkm/modules.load))
BOARD_VENDOR_KERNEL_MODULES_BLOCKLIST_FILE := $(PREBUILT_KERNEL_PATH)/vendor_dlkm/modules.blocklist
BOARD_VENDOR_RAMDISK_KERNEL_MODULES := $(wildcard $(PREBUILT_KERNEL_PATH)/vendor_ramdisk/*.ko)
BOARD_VENDOR_RAMDISK_KERNEL_MODULES_LOAD := $(patsubst %,$(PREBUILT_KERNEL_PATH)/vendor_ramdisk/%,$(shell cat $(PREBUILT_KERNEL_PATH)/vendor_ramdisk/modules.load))
BOARD_VENDOR_RAMDISK_RECOVERY_KERNEL_MODULES_LOAD  := $(patsubst %,$(PREBUILT_KERNEL_PATH)/vendor_ramdisk/%,$(shell cat $(PREBUILT_KERNEL_PATH)/vendor_ramdisk/modules.load.recovery))
BOARD_VENDOR_RAMDISK_KERNEL_MODULES_BLOCKLIST_FILE := $(PREBUILT_KERNEL_PATH)/vendor_ramdisk/modules.blocklist
endif

# Partitions
BOARD_MOT_DP_GROUP_SIZE := 9038725120 # ( BOARD_SUPER_PARTITION_SIZE - 4MB )
BOARD_SUPER_PARTITION_SIZE := 9042919424

# Properties
TARGET_PRODUCT_PROP += $(DEVICE_PATH)/product.prop
TARGET_SYSTEM_EXT_PROP += $(DEVICE_PATH)/system_ext.prop
TARGET_VENDOR_PROP += $(DEVICE_PATH)/vendor.prop

# Recovery
TARGET_RECOVERY_UI_MARGIN_HEIGHT := 90

# Security
BOOT_SECURITY_PATCH := 2026-03-01
VENDOR_SECURITY_PATCH := $(BOOT_SECURITY_PATCH)

# Verified Boot
BOARD_AVB_ROLLBACK_INDEX := 14
BOARD_AVB_VBMETA_SYSTEM_ROLLBACK_INDEX := 14

# inherit from the proprietary version
include vendor/motorola/mona/BoardConfigVendor.mk
