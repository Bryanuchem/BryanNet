import {
    useQuery,
} from "@tanstack/react-query";

import {

    getPayment,

    getPayments,

    getPaymentSummary,

} from "../api/payments";


export const PAYMENTS_QUERY_KEY = [
    "payments",
];

export const PAYMENT_SUMMARY_QUERY_KEY = [
    "payment-summary",
];


export function usePayments(
    filters = {},
) {

    return useQuery({

        queryKey: [

            ...PAYMENTS_QUERY_KEY,

            filters,

        ],

        queryFn: () =>
            getPayments(
                filters,
            ),

    });

}


export function usePaymentSummary() {

    return useQuery({

        queryKey:
            PAYMENT_SUMMARY_QUERY_KEY,

        queryFn:
            getPaymentSummary,

    });

}


export function usePayment(
    paymentReference,
) {

    return useQuery({

        queryKey: [

            ...PAYMENTS_QUERY_KEY,

            paymentReference,

        ],

        queryFn: () =>
            getPayment(
                paymentReference,
            ),

        enabled:
            !!paymentReference,

    });

}