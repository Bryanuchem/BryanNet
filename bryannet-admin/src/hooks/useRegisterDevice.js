import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    registerDevice,
} from "../api/devices";

export function useRegisterDevice() {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            registerDevice,

        onSuccess: () => {

            queryClient.invalidateQueries({

                queryKey: [
                    "devices",
                ],

            });

        },

    });

}