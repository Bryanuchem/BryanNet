import { useQuery } from "@tanstack/react-query";

import {
    getSubscriptions,
} from "../api/subscriptions";

export const useSubscriptions = ({

    page = 1,

    pageSize = 25,

    search = "",

    customerId,

    planId,

    status,

    sortBy = "created_at",

    sortOrder = "desc",

} = {}) => {

    return useQuery({

        queryKey: [

            "subscriptions",

            {

                page,

                pageSize,

                search,

                customerId,

                planId,

                status,

                sortBy,

                sortOrder,

            },

        ],

        queryFn: () =>

            getSubscriptions({

                page,

                page_size: pageSize,

                search,

                customer_id: customerId,

                plan_id: planId,

                status,

                sort_by: sortBy,

                sort_order: sortOrder,

            }),

        keepPreviousData: true,

    });

};