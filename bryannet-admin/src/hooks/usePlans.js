import { useQuery } from "@tanstack/react-query";

import { getPlans } from "../api/plans";

export const usePlans = ({
    page = 1,
    pageSize = 25,
    search = "",
    isActive,
    sortBy = "price",
    sortOrder = "asc",
} = {}) => {

    return useQuery({

        queryKey: [

            "plans",

            {
                page,
                pageSize,
                search,
                isActive,
                sortBy,
                sortOrder,
            },

        ],

        queryFn: () =>
            getPlans({

                page,

                page_size: pageSize,

                search,

                is_active: isActive,

                sort_by: sortBy,

                sort_order: sortOrder,

            }),

        keepPreviousData: true,

    });

};