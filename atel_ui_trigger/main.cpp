/*
 * SPDX-FileCopyrightText: 2026 The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 *
 * Motorola Mona System Boot Initialization & Unblock Service
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <android/log.h>

#define LOG_TAG "atel_ui_trigger"
#define ALOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)

int main() {
    ALOGI("Starting Mona boot initialization service...");

    // 1. Send QCRIL OEM Hook SET_ATEL_UI_STATUS to unblock modem MT-SMS queue
    ALOGI("Triggering Qualcomm OEM Hook SET_ATEL_UI_STATUS (0x8001A)...");
    system("/system/bin/service call vendor.qti.hardware.radio.qcrilhook.IQtiOemHook/oemhook0 2 i32 1001 i32 17 i32 1296387921 i32 1263488840 i32 524314 i32 1 i32 1");
    system("/system/bin/service call vendor.qti.hardware.radio.qcrilhook.IQtiOemHook/oemhook1 2 i32 1002 i32 17 i32 1296387921 i32 1263488840 i32 524314 i32 1 i32 1");

    // 2. Telephony / IMS Configuration
    ALOGI("Configuring IMS MMTEL and SMS services...");
    system("/system/bin/cmd phone cc set-value -s 0 -p imssms.sms_over_ims_supported_bool true");
    system("/system/bin/cmd phone ims set-ims-service -s 0 -c org.codeaurora.ims");
    system("/system/bin/cmd phone ims enable -s 0");

    // 3. Set default SMS app to stock Messaging so incoming texts are delivered
    ALOGI("Ensuring default SMS application...");
    system("/system/bin/settings put secure sms_default_application com.android.messaging");

    // 4. Lock display refresh rate to 120Hz constant & disable auto-brightness
    ALOGI("Locking 120Hz display refresh rate...");
    system("/system/bin/settings put system min_refresh_rate 120.0");
    system("/system/bin/settings put system peak_refresh_rate 120.0");
    system("/system/bin/settings put system screen_brightness_mode 0");

    ALOGI("Mona boot initialization completed successfully.");
    return 0;
}
