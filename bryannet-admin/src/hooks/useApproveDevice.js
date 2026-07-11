import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    approveDevice,
} from "../api/devices";

export function useApproveDevice() {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn: approveDevice,

        onSuccess: () => {

            queryClient.invalidateQueries({
                queryKey: ["devices"],
            });

        },

    });

}