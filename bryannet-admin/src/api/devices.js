import api from "./axios";

/**
 * Get all registered devices.
 */
export const getDevices = async () => {
    const response = await api.get("/devices");

    return response.data;
};

/**
 * Get devices belonging to a customer.
 */
export const getCustomerDevices = async (
    customerId
) => {
    const response = await api.get(
        `/devices/${customerId}`
    );

    return response.data;
};

/**
 * Register a new device.
 */
export const registerDevice = async (
    deviceData
) => {
    const response = await api.post(
        "/devices/register",
        deviceData
    );

    return response.data;
};

/**
 * Remove a device.
 */
export const removeDevice = async (
    deviceId
) => {
    const response = await api.delete(
        `/devices/${deviceId}`
    );

    return response.data;
};