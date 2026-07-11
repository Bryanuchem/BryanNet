import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    blockDevice,
} from "../api/devices";

export function useBlockDevice() {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn: blockDevice,

        onSuccess: () => {

            queryClient.invalidateQueries({
                queryKey: ["devices"],
            });

        },

    });

}