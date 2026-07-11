import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    updatePlan,
} from "../api/plans";

export const useUpdatePlan = () => {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn: ({
            planId,
            planData,
        }) =>

            updatePlan(
                planId,
                planData,
            ),

        onSuccess: () => {

            queryClient.invalidateQueries({

                queryKey: ["plans"],

            });

        },

    });

};