import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    cancelSubscription,
} from "../api/subscriptions";

export const useCancelSubscription = () => {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            cancelSubscription,

        onSuccess: () => {

            queryClient.invalidateQueries({

                queryKey: [
                    "subscriptions",
                ],

            });

        },

    });

};