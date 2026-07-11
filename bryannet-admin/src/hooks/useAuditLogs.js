import {
    useQuery,
} from "@tanstack/react-query";

import {
    getAuditLogs,
} from "../api/auditLogs";

export function useAuditLogs(
    filters,
) {

    return useQuery({

        queryKey: [

            "audit-logs",

            filters,

        ],

        queryFn: () =>

            getAuditLogs(
                filters,
            ),

        placeholderData: (

            previousData,
        ) => previousData,

    });

}