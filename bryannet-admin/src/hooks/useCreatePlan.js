import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    createPlan,
} from "../api/plans";

export const useCreatePlan = () => {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn: createPlan,

        onSuccess: () => {

            queryClient.invalidateQueries({

                queryKey: ["plans"],

            });

        },

    });

};