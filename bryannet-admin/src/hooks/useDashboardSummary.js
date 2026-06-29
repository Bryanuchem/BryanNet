import { useQuery } from "@tanstack/react-query";

import { getDashboardSummary } from "../api/dashboard";

export default function useDashboardSummary() {
    return useQuery({
        queryKey: ["dashboard-summary"],
        queryFn: getDashboardSummary,
    });
}