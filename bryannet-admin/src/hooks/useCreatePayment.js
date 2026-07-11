import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    createPayment,
} from "../api/payments";

import {

    PAYMENTS_QUERY_KEY,

    PAYMENT_SUMMARY_QUERY_KEY,

} from "./usePayments";


export function useCreatePayment() {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            createPayment,

        onSuccess: () => {

            queryClient.invalidateQueries({

                queryKey:
                    PAYMENTS_QUERY_KEY,

            });

            queryClient.invalidateQueries({

                queryKey:
                    PAYMENT_SUMMARY_QUERY_KEY,

            });

        },

    });

}