import { useQuery } from "@tanstack/react-query";

import { getAdministrationOverview } from "../api/administration";

export function useAdministrationOverview() {
    return useQuery({
        queryKey: ["administration-overview"],
        queryFn: getAdministrationOverview,
    });
}