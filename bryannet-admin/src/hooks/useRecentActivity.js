import { useQuery } from "@tanstack/react-query";

import {
    getRecentActivity,
} from "../api/dashboard";

export default function useRecentActivity(
    limit = 10,
) {

    return useQuery({

        queryKey: [
            "dashboard-recent-activity",
            limit,
        ],

        queryFn: () =>
            getRecentActivity(limit),

    });

}