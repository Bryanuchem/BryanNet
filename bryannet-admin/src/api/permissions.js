import api from "./axios";

// ==========================================================
// Query Methods
// ==========================================================

export async function getPermissions() {

    const response = await api.get(

        "/permissions",

    );

    return response.data;

}

export async function getPermission(

    permissionId,

) {

    const response = await api.get(

        `/permissions/${permissionId}`,

    );

    return response.data;

}

export async function getRolePermissions(

    roleId,

) {

    const response = await api.get(

        `/roles/${roleId}/permissions`,

    );

    return response.data;

}


// ==========================================================
// Business Commands
// ==========================================================

export async function updateRolePermissions(

    roleId,

    permissionIds,

) {

    const response = await api.put(

        `/roles/${roleId}/permissions`,

        {

            permission_ids: permissionIds,

        },

    );

    return response.data;

}