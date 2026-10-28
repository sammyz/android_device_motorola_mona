/*
 * SPDX-FileCopyrightText: 2026 The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 *
 * Motorola Mona Qualcomm QCRIL ATEL UI Status Trigger
 * Unblocks MT-SMS (Mobile Terminated SMS) in Qualcomm modem power optimization queue.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>
#include <android/binder_ibinder.h>
#include <android/binder_manager.h>
#include <android/binder_parcel.h>
#include <android/log.h>

#define LOG_TAG "atel_ui_trigger"
#define ALOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)
#define ALOGE(...) __android_log_print(ANDROID_LOG_ERROR, LOG_TAG, __VA_ARGS__)

static int trigger_atel_ui(const char* service_name, int status_val, int max_retries) {
    printf("[atel_ui_trigger] Resolving service: %s\n", service_name);
    ALOGI("Resolving service: %s (max_retries=%d)", service_name, max_retries);
    
    AIBinder* binder = NULL;
    for (int i = 0; i < max_retries; i++) {
        binder = AServiceManager_checkService(service_name);
        if (binder) break;
        if (i % 5 == 0) {
            printf("[atel_ui_trigger] Waiting for %s... (attempt %d/%d)\n", service_name, i + 1, max_retries);
            ALOGI("Waiting for %s... (attempt %d/%d)", service_name, i + 1, max_retries);
        }
        sleep(1);
    }
    
    if (!binder) {
        printf("[atel_ui_trigger] Service %s not available after %d seconds.\n", service_name, max_retries);
        ALOGE("Service %s not available after %d seconds", service_name, max_retries);
        return 1;
    }
    
    AParcel* in = NULL;
    binder_status_t status = AIBinder_prepareTransaction(binder, &in);
    if (status != STATUS_OK || !in) {
        printf("[atel_ui_trigger] AIBinder_prepareTransaction failed: %d\n", status);
        ALOGE("AIBinder_prepareTransaction failed: %d", status);
        AIBinder_decStrong(binder);
        return 2;
    }
    
    // Serial number
    int32_t serial = 1001;
    AParcel_writeInt32(in, serial);
    
    // QOEMHOOK packet:
    // Header: "QOEMHOOK" (8 bytes)
    // Request ID: 0x8001A (4 bytes, little-endian) = QCRIL_EVT_HOOK_SET_ATEL_UI_STATUS
    // Payload length: 1 (4 bytes, little-endian)
    // Payload: status_val (1 byte: 1 = UI active)
    uint8_t packet[17];
    memcpy(packet, "QOEMHOOK", 8);
    uint32_t req_id = 0x0008001a;
    uint32_t payload_len = 1;
    memcpy(packet + 8, &req_id, 4);
    memcpy(packet + 12, &payload_len, 4);
    packet[16] = (uint8_t)status_val;
    
    AParcel_writeByteArray(in, (const int8_t*)packet, sizeof(packet));
    
    AParcel* out = NULL;
    // transaction_code = 2 (FIRST_CALL_TRANSACTION + 1) = oemHookRawRequest
    printf("[atel_ui_trigger] Calling oemHookRawRequest on %s (serial=%d, req=0x%05x, val=%d)...\n",
           service_name, serial, req_id, status_val);
    ALOGI("Calling oemHookRawRequest on %s (serial=%d, req=0x%05x, val=%d)",
          service_name, serial, req_id, status_val);
          
    status = AIBinder_transact(binder, 2, &in, &out, 0);
    printf("[atel_ui_trigger] Transact returned status: %d (%s)\n",
           status, (status == STATUS_OK) ? "SUCCESS" : "FAILED");
    ALOGI("Transact returned status: %d (%s)",
          status, (status == STATUS_OK) ? "SUCCESS" : "FAILED");
          
    if (in) AParcel_delete(in);
    if (out) AParcel_delete(out);
    AIBinder_decStrong(binder);
    return (status == STATUS_OK) ? 0 : 3;
}

int main(int argc, char** argv) {
    int val = 1;
    if (argc > 1) {
        val = atoi(argv[1]);
    }
    printf("=== Motorola Mona QCRIL ATEL UI Trigger ===\n");
    ALOGI("Starting QCRIL ATEL UI trigger, val=%d", val);
    
    // Slot 0 is primary SIM; retry up to 30s during boot
    int ret0 = trigger_atel_ui("vendor.qti.hardware.radio.qcrilhook.IQtiOemHook/oemhook0", val, 30);
    // Slot 1 is secondary/eSIM; try up to 5s
    int ret1 = trigger_atel_ui("vendor.qti.hardware.radio.qcrilhook.IQtiOemHook/oemhook1", val, 5);
    
    printf("=== Complete: slot0=%d, slot1=%d ===\n", ret0, ret1);
    ALOGI("Completed: slot0=%d, slot1=%d", ret0, ret1);
    return (ret0 == 0 || ret1 == 0) ? 0 : 1;
}
