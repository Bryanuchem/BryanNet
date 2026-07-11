import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    activateDevice,
} from "../api/devices";

export function useActivateDevice() {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            activateDevice,

        onSuccess: () => {

            queryClient.invalidateQueries({

                queryKey: [
                    "devices",
                ],

            });

        },

    });

}