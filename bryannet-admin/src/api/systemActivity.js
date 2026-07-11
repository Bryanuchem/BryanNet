import api from "./axios";

export async function getSystemActivity(

    filters = {},

) {

    const response = await api.get(

        "/system-activity",

        {

            params: {

                search: filters.search,

                action: filters.action,

                result: filters.result,

                page: filters.page,

                page_size: filters.pageSize,

            },

        },

    );

    return response.data.items;

}

export async function getSystemActivityById(

    auditLogId,

) {

    const response = await api.get(

        `/system-activity/${auditLogId}`,

    );

    return response.data.items;
}