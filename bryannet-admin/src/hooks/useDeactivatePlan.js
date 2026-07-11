import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    deactivatePlan,
} from "../api/plans";

export const useDeactivatePlan = () => {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn: deactivatePlan,

        onSuccess: () => {

            queryClient.invalidateQueries({

                queryKey: ["plans"],

            });

        },

    });

};