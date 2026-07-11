import apiClient from "./client";

// ==========================================================
// Query Methods
// ==========================================================

export async function getAdminUsers(
    filters = {},
) {

    const response = await apiClient.get(
        "/admin-users",
        {
            params: filters,
        },
    );

    return response.data;

}

export async function getAdminUser(
    adminUserId,
) {

    const response = await apiClient.get(
        `/admin-users/${adminUserId}`,
    );

    return response.data;

}

// ==========================================================
// Business Commands
// ==========================================================

export async function createAdminUser(
    adminUser,
) {

    const response = await apiClient.post(
        "/admin-users",
        adminUser,
    );

    return response.data;

}

export async function updateAdminUser(
    adminUserId,
    adminUser,
) {

    const response = await apiClient.put(
        `/admin-users/${adminUserId}`,
        adminUser,
    );

    return response.data;

}

export async function updateAdminActivation(
    adminUserId,
    isActive,
) {

    const response = await apiClient.patch(
        `/admin-users/${adminUserId}/activation`,
        {
            is_active: isActive,
        },
    );

    return response.data;

}

export async function changeAdminRole(
    adminUserId,
    roleId,
) {

    const response = await apiClient.patch(
        `/admin-users/${adminUserId}/role`,
        {
            role_id: roleId,
        },
    );

    return response.data;

}

export async function changeAdminPassword(
    adminUserId,
    password,
) {

    const response = await apiClient.patch(
        `/admin-users/${adminUserId}/password`,
        {
            password,
        },
    );

    return response.data;

}