import {
    useMutation,
    useQuery,
    useQueryClient,
} from "@tanstack/react-query";

import {
    deleteSubscription,
    getSubscription,
    getSubscriptions,
    purchaseSubscription,
    renewSubscription,
    updateSubscription,
    updateSubscriptionStatus,
} from "../api/subscriptions";

const QUERY_KEY = ["subscriptions"];


export const useSubscriptions = () =>
    useQuery({
        queryKey: QUERY_KEY,
        queryFn: getSubscriptions,
    });


export const useSubscription = (
    subscriptionId
) =>
    useQuery({
        queryKey: [
            ...QUERY_KEY,
            subscriptionId,
        ],
        queryFn: () =>
            getSubscription(subscriptionId),
        enabled: !!subscriptionId,
    });


export const usePurchaseSubscription = () => {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn: purchaseSubscription,

        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: QUERY_KEY,
            });
        },

    });

};


export const useUpdateSubscription = () => {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn: updateSubscription,

        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: QUERY_KEY,
            });
        },

    });

};


export const useUpdateSubscriptionStatus = () => {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn: updateSubscriptionStatus,

        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: QUERY_KEY,
            });
        },

    });

};


export const useRenewSubscription = () => {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn: renewSubscription,

        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: QUERY_KEY,
            });
        },

    });

};


export const useDeleteSubscription = () => {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn: deleteSubscription,

        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: QUERY_KEY,
            });
        },

    });

};