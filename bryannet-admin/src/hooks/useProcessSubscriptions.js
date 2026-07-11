import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    processSubscriptions,
} from "../api/subscriptions";

export const useProcessSubscriptions = () => {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            processSubscriptions,

        onSuccess: () => {

            queryClient.invalidateQueries({

                queryKey: [
                    "subscriptions",
                ],

            });

        },

    });

};