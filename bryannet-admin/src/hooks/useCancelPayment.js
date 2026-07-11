import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    cancelPayment,
} from "../api/payments";

import {

    PAYMENTS_QUERY_KEY,

    PAYMENT_SUMMARY_QUERY_KEY,

} from "./usePayments";


export function useCancelPayment() {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            cancelPayment,

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