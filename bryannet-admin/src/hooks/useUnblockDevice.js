import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    unblockDevice,
} from "../api/devices";

export function useUnblockDevice() {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn: unblockDevice,

        onSuccess: () => {

            queryClient.invalidateQueries({
                queryKey: ["devices"],
            });

        },

    });

}