import {
    useMutation,
    useQuery,
    useQueryClient,
} from "@tanstack/react-query";

import {
    createPayment,
    deletePayment,
    getPayment,
    getPayments,
    getPaymentStats,
    updatePayment,
} from "../api/payments";

const QUERY_KEY = ["payments"];

const SUMMARY_QUERY_KEY = [
    "payment-summary",
];


export const usePayments = (
    filters = {},
) =>
    useQuery({

        queryKey: [
            ...QUERY_KEY,
            filters,
        ],

        queryFn: () =>
            getPayments(filters),

    });


export const usePaymentStats = () =>
    useQuery({

        queryKey:
            SUMMARY_QUERY_KEY,

        queryFn:
            getPaymentStats,

    });


export const usePayment = (
    paymentId,
) =>
    useQuery({

        queryKey: [
            ...QUERY_KEY,
            paymentId,
        ],

        queryFn: () =>
            getPayment(paymentId),

        enabled: !!paymentId,

    });


export const useCreatePayment = () => {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn:
            createPayment,

        onSuccess: () => {

            queryClient.invalidateQueries({

                queryKey:
                    QUERY_KEY,

            });

            queryClient.invalidateQueries({

                queryKey:
                    SUMMARY_QUERY_KEY,

            });

        },

    });

};


export const useUpdatePayment = () => {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn:
            updatePayment,

        onSuccess: () => {

            queryClient.invalidateQueries({

                queryKey:
                    QUERY_KEY,

            });

            queryClient.invalidateQueries({

                queryKey:
                    SUMMARY_QUERY_KEY,

            });

        },

    });

};


export const useDeletePayment = () => {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn:
            deletePayment,

        onSuccess: () => {

            queryClient.invalidateQueries({

                queryKey:
                    QUERY_KEY,

            });

            queryClient.invalidateQueries({

                queryKey:
                    SUMMARY_QUERY_KEY,

            });

        },

    });

};