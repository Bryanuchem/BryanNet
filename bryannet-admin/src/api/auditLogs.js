import apiClient from "./client";

// ==========================================================
// Query Methods
// ==========================================================

export async function getAuditLogs(
    filters = {},
) {

    const response = await apiClient.get(

        "/audit-logs",

        {

            params: {

                search:
                    filters.search || undefined,

                action:
                    filters.action || undefined,

                result:
                    filters.result || undefined,

                admin_id:
                    filters.admin_id || undefined,

            },

        },

    );

    return response.data;

}

export async function getAuditLog(
    auditLogId,
) {

    const response = await apiClient.get(

        `/audit-logs/${auditLogId}`,

    );

    return response.data;

}