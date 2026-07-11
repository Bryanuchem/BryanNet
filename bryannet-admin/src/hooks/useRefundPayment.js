import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    refundPayment,
} from "../api/payments";

import {

    PAYMENTS_QUERY_KEY,

    PAYMENT_SUMMARY_QUERY_KEY,

} from "./usePayments";


export function useRefundPayment() {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            refundPayment,

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