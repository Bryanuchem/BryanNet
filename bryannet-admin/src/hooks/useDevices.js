import {
    useMutation,
    useQuery,
    useQueryClient,
} from "@tanstack/react-query";

import {
    getDevices,
    registerDevice,
    removeDevice,
} from "../api/devices";

/**
 * Fetch all registered devices.
 */
export const useDevices = () => {
    return useQuery({
        queryKey: ["devices"],
        queryFn: getDevices,
    });
};

/**
 * Register a new device.
 */
export const useRegisterDevice = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: registerDevice,
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["devices"],
            });
        },
    });
};

/**
 * Remove a device.
 */
export const useRemoveDevice = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: removeDevice,
        onSuccess: () => {
            queryClient.invalidateQueries({
                queryKey: ["devices"],
            });
        },
    });
};