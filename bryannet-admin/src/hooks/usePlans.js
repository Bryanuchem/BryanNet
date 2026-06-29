import {
    useMutation,
    useQuery,
    useQueryClient,
} from "@tanstack/react-query";

import {
    createPlan,
    deletePlan,
    getPlan,
    getPlans,
    updatePlan,
} from "../api/plans";

const QUERY_KEY = ["plans"];


export const usePlans = () =>
    useQuery({
        queryKey: QUERY_KEY,
        queryFn: getPlans,
    });


export const usePlan = (
    planId
) =>
    useQuery({
        queryKey: [
            ...QUERY_KEY,
            planId,
        ],
        queryFn: () =>
            getPlan(planId),
        enabled: !!planId,
    });


export const useCreatePlan = () => {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn: createPlan,

        onSuccess: () => {

            queryClient.invalidateQueries({
                queryKey: QUERY_KEY,
            });

        },

    });

};


export const useUpdatePlan = () => {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn: updatePlan,

        onSuccess: () => {

            queryClient.invalidateQueries({
                queryKey: QUERY_KEY,
            });

        },

    });

};


export const useDeletePlan = () => {

    const queryClient = useQueryClient();

    return useMutation({

        mutationFn: deletePlan,

        onSuccess: () => {

            queryClient.invalidateQueries({
                queryKey: QUERY_KEY,
            });

        },

    });

};