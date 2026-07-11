import {
    useQuery,
} from "@tanstack/react-query";

import {
    getCustomers,
} from "../api/customers";


export const CUSTOMERS_QUERY_KEY = [
    "customers",
];


export function useCustomers({

    page = 1,

    pageSize = 25,

    search = "",

    status,

    sortBy = "created_at",

    sortOrder = "desc",

} = {}) {

    return useQuery({

        queryKey: [

            ...CUSTOMERS_QUERY_KEY,

            {

                page,

                pageSize,

                search,

                status,

                sortBy,

                sortOrder,

            },

        ],

        queryFn: () =>

            getCustomers({

                page,

                page_size: pageSize,

                search,

                status,

                sort_by: sortBy,

                sort_order: sortOrder,

            }),

        keepPreviousData: true,

    });

}