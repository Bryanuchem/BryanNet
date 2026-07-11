import {
    useMutation,
    useQueryClient,
} from "@tanstack/react-query";

import {
    renameDevice,
} from "../api/devices";

export function useRenameDevice() {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn: ({
            deviceId,
            deviceName,
        }) =>
            renameDevice(
                deviceId,
                deviceName,
            ),

        onSuccess: () => {

            queryClient.invalidateQueries({
                queryKey: ["devices"],
            });

        },

    });

}