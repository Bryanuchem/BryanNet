import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    activatePlan,
} from "../api/plans";

export const useActivatePlan = () => {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn: activatePlan,

        onSuccess: () => {

            queryClient.invalidateQueries({

                queryKey: ["plans"],

            });

        },

    });

};