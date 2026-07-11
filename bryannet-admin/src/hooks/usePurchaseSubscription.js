import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    purchaseSubscription,
} from "../api/subscriptions";

export const usePurchaseSubscription = () => {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            purchaseSubscription,

        onSuccess: () => {

            queryClient.invalidateQueries({

                queryKey: [
                    "subscriptions",
                ],

            });

        },

    });

};