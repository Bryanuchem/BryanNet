import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    replaceDevice,
} from "../api/devices";

export function useReplaceDevice() {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn: replaceDevice,

        onSuccess: () => {

            queryClient.invalidateQueries({
                queryKey: ["devices"],
            });

        },

    });

}