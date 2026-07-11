import {
    useQuery,
} from "@tanstack/react-query";

import {
    getAdminUser,
    getAdminUsers,
} from "../api/adminUsers";

export const ADMIN_USERS_QUERY_KEY = [
    "admin-users",
];

export function useAdminUsers(
    filters = {},
) {

    return useQuery({

        queryKey: [

            ...ADMIN_USERS_QUERY_KEY,

            filters,

        ],

        queryFn: () =>
            getAdminUsers(
                filters,
            ),

        keepPreviousData: true,

    });

}

export function useAdminUser(
    adminUserId,
) {

    return useQuery({

        queryKey: [

            ...ADMIN_USERS_QUERY_KEY,

            adminUserId,

        ],

        queryFn: () =>
            getAdminUser(
                adminUserId,
            ),

        enabled:
            !!adminUserId,

    });

}