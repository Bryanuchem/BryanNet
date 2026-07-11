import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    completePayment,
} from "../api/payments";

import {

    PAYMENTS_QUERY_KEY,

    PAYMENT_SUMMARY_QUERY_KEY,

} from "./usePayments";


export function useCompletePayment() {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            ({
                paymentReference,
                gatewayTransactionId,
            }) =>
                completePayment(
                    paymentReference,
                    gatewayTransactionId,
                ),

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