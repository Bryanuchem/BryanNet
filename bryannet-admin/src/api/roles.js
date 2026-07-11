import apiClient from "./client";

// ==========================================================
// Query Methods
// ==========================================================

export async function getRoles() {

    const response = await apiClient.get(

        "/roles",

    );

    return response.data;

}

export async function getActiveRoles() {

    const response = await apiClient.get(

        "/roles/active",

    );

    return response.data;

}

export async function getRole(

    roleId,

) {

    const response = await apiClient.get(

        `/roles/${roleId}`,

    );

    return response.data;

}


// ==========================================================
// Business Commands
// ==========================================================

export async function createRole(

    data,

) {

    const response = await apiClient.post(

        "/roles",

        data,

    );

    return response.data;

}

export async function updateRole(

    roleId,

    data,

) {

    const response = await apiClient.put(

        `/roles/${roleId}`,

        data,

    );

    return response.data;

}

export async function updateRoleActivation(

    roleId,

    isActive,

) {

    const response = await apiClient.patch(

        `/roles/${roleId}/activation`,

        {

            is_active: isActive,

        },

    );

    return response.data;

}

export async function duplicateRole(

    roleId,

) {

    const response = await apiClient.post(

        `/roles/${roleId}/duplicate`,

    );

    return response.data;

}

export async function deleteRole(

    roleId,

) {

    const response = await apiClient.delete(

        `/roles/${roleId}`,

    );

    return response.data;

}