import { useQuery } from "@tanstack/react-query";

import {
    getSubscriptionBreakdown,
} from "../api/dashboard";

export default function useSubscriptionBreakdown() {

    return useQuery({

        queryKey: [
            "dashboard-subscription-breakdown",
        ],

        queryFn: getSubscriptionBreakdown,

    });

}