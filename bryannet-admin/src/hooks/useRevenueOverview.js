import { useQuery } from "@tanstack/react-query";

import {
    getRevenueOverview,
} from "../api/dashboard";

export default function useRevenueOverview(
    period = "month",
) {

    return useQuery({

        queryKey: [
            "dashboard-revenue-overview",
            period,
        ],

        queryFn: () =>
            getRevenueOverview(period),

    });

}