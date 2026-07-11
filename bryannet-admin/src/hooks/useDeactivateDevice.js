import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    deactivateDevice,
} from "../api/devices";

export function useDeactivateDevice() {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            deactivateDevice,

        onSuccess: () => {

            queryClient.invalidateQueries({

                queryKey: [
                    "devices",
                ],

            });

        },

    });

}