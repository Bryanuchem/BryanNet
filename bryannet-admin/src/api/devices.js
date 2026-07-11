import api from "./axios";

/**
 * Get all devices.
 */
export const getDevices = async () => {

    const response = await api.get(
        "/devices",
    );

    return response.data.items;

};

/**
 * Get devices belonging to a customer.
 */
export const getCustomerDevices = async (
    customerId,
) => {

    const response = await api.get(
        `/devices/customer/${customerId}`,
    );

    return response.data;

};

/**
 * Register a new device.
 */
export const registerDevice = async (
    deviceData,
) => {

    const response = await api.post(
        "/devices/register",
        deviceData,
    );

    return response.data;

};

/**
 * Activate a device.
 */
export const activateDevice = async (
    deviceId,
) => {

    const response = await api.patch(
        `/devices/${deviceId}/activate`,
    );

    return response.data;

};

/**
 * Deactivate a device.
 */
export const deactivateDevice = async (
    deviceId,
) => {

    const response = await api.patch(
        `/devices/${deviceId}/deactivate`,
    );

    return response.data;

};

/**
 * Approve a device.
 */
export const approveDevice = async (
    deviceId,
) => {

    const response = await api.patch(
        `/devices/${deviceId}/approve`,
    );

    return response.data;

};

/**
 * Block a device.
 */
export const blockDevice = async (
    deviceId,
) => {

    const response = await api.patch(
        `/devices/${deviceId}/block`,
    );

    return response.data;

};

/**
 * Unblock a device.
 */
export const unblockDevice = async (
    deviceId,
) => {

    const response = await api.patch(
        `/devices/${deviceId}/unblock`,
    );

    return response.data;

};

/**
 * Rename a device.
 */
export const renameDevice = async (
    deviceId,
    deviceName,
) => {

    const response = await api.patch(
        `/devices/${deviceId}/rename`,
        {
            device_name: deviceName,
        },
    );

    return response.data;

};

/**
 * Replace a device.
 */
export const replaceDevice = async (
    replacementData,
) => {

    const response = await api.post(
        "/devices/replace",
        replacementData,
    );

    return response.data;

};