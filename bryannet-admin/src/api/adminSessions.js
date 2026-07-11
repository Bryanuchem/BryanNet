import api from "./axios";

export async function getAdminSessions(

    filters = {},

) {

    const response = await api.get(

        "/sessions",

        {

            params: {

                search: filters.search,

                is_active: filters.isActive,

                device: filters.device,

                browser: filters.browser,

                sort_by: filters.sortBy,

                sort_order: filters.sortOrder,

                page: filters.page,

                page_size: filters.pageSize,

            },

        },

    );

    return response.data;

}

export async function getAdminSessionById(

    adminSessionId,

) {

    const response = await api.get(

        `/sessions/${adminSessionId}`,

    );

    return response.data;

}

export async function revokeAdminSession(

    adminSessionId,

) {

    const response = await api.patch(

        `/sessions/${adminSessionId}/revoke`,

    );

    return response.data;

}