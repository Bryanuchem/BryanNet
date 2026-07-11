import apiClient from "./client";

// ==========================================================
// General Settings
// ==========================================================

export async function getGeneralSettings() {

    const response = await apiClient.get(

        "/settings/general",

    );

    return response.data;

}

export async function updateGeneralSettings(

    data,

) {

    const response = await apiClient.put(

        "/settings/general",

        data,

    );

    return response.data;

}

// ==========================================================
// Authentication Settings
// ==========================================================

export async function getAuthenticationSettings() {

    const response = await apiClient.get(

        "/settings/authentication",

    );

    return response.data;

}

export async function updateAuthenticationSettings(

    data,

) {

    const response = await apiClient.put(

        "/settings/authentication",

        data,

    );

    return response.data;

}

// ==========================================================
// Notification Settings
// ==========================================================

export async function getNotificationSettings() {

    const response = await apiClient.get(

        "/settings/notifications",

    );

    return response.data;

}

export async function updateNotificationSettings(

    data,

) {

    const response = await apiClient.put(

        "/settings/notifications",

        data,

    );

    return response.data;

}

// ==========================================================
// Network Settings
// ==========================================================

export async function getNetworkSettings() {

    const response = await apiClient.get(

        "/settings/network",

    );

    return response.data;

}

export async function updateNetworkSettings(

    data,

) {

    const response = await apiClient.put(

        "/settings/network",

        data,

    );

    return response.data;

}

// ==========================================================
// Billing Settings
// ==========================================================

export async function getBillingSettings() {

    const response = await apiClient.get(

        "/settings/billing",

    );

    return response.data;

}

export async function updateBillingSettings(

    data,

) {

    const response = await apiClient.put(

        "/settings/billing",

        data,

    );

    return response.data;

}

// ==========================================================
// Integration Settings
// ==========================================================

export async function getIntegrationSettings() {

    const response = await apiClient.get(

        "/settings/integrations",

    );

    return response.data;

}

export async function updateIntegrationSettings(

    data,

) {

    const response = await apiClient.put(

        "/settings/integrations",

        data,

    );

    return response.data;

}

// ==========================================================
// Branding Settings
// ==========================================================

export async function getBrandingSettings() {

    const response = await apiClient.get(

        "/settings/branding",

    );

    return response.data;

}

export async function updateBrandingSettings(

    data,

) {

    const response = await apiClient.put(

        "/settings/branding",

        data,

    );

    return response.data;

}

// ==========================================================
// System Settings
// ==========================================================

export async function getSystemSettings() {

    const response = await apiClient.get(

        "/settings/system",

    );

    return response.data;

}

export async function updateSystemSettings(

    data,

) {

    const response = await apiClient.put(

        "/settings/system",

        data,

    );

    return response.data;

}