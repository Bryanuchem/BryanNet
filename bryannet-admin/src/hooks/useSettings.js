import {

    useMutation,

    useQuery,

    useQueryClient,

} from "@tanstack/react-query";

import {

    getAuthenticationSettings,

    getBillingSettings,

    getBrandingSettings,

    getGeneralSettings,

    getIntegrationSettings,

    getNetworkSettings,

    getNotificationSettings,

    getSystemSettings,

    updateAuthenticationSettings,

    updateBillingSettings,

    updateBrandingSettings,

    updateGeneralSettings,

    updateIntegrationSettings,

    updateNetworkSettings,

    updateNotificationSettings,

    updateSystemSettings,

} from "../api/settings";

// ==========================================================
// Query Keys
// ==========================================================

export const GENERAL_SETTINGS_QUERY_KEY = [
    "settings",
    "general",
];

export const AUTHENTICATION_SETTINGS_QUERY_KEY = [
    "settings",
    "authentication",
];

export const NOTIFICATION_SETTINGS_QUERY_KEY = [
    "settings",
    "notifications",
];

export const NETWORK_SETTINGS_QUERY_KEY = [
    "settings",
    "network",
];

export const BILLING_SETTINGS_QUERY_KEY = [
    "settings",
    "billing",
];

export const INTEGRATION_SETTINGS_QUERY_KEY = [
    "settings",
    "integrations",
];

export const BRANDING_SETTINGS_QUERY_KEY = [
    "settings",
    "branding",
];

export const SYSTEM_SETTINGS_QUERY_KEY = [
    "settings",
    "system",
];

// ==========================================================
// General
// ==========================================================

export function useGeneralSettings() {

    return useQuery({

        queryKey:
            GENERAL_SETTINGS_QUERY_KEY,

        queryFn:
            getGeneralSettings,

    });

}

export function useUpdateGeneralSettings(

    options = {},

) {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            updateGeneralSettings,

        onSuccess: (

            data,

            variables,

            context,

        ) => {

            queryClient.invalidateQueries({

                queryKey:
                    GENERAL_SETTINGS_QUERY_KEY,

            });

            options.onSuccess?.(

                data,

                variables,

                context,

            );

        },

        onError: (

            error,

            variables,

            context,

        ) => {

            options.onError?.(

                error,

                variables,

                context,

            );

        },

    });

}

// ==========================================================
// Authentication
// ==========================================================

export function useAuthenticationSettings() {

    return useQuery({

        queryKey:
            AUTHENTICATION_SETTINGS_QUERY_KEY,

        queryFn:
            getAuthenticationSettings,

    });

}

export function useUpdateAuthenticationSettings(

    options = {},

) {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            updateAuthenticationSettings,

        onSuccess: (

            data,

            variables,

            context,

        ) => {

            queryClient.invalidateQueries({

                queryKey:
                    AUTHENTICATION_SETTINGS_QUERY_KEY,

            });

            options.onSuccess?.(

                data,

                variables,

                context,

            );

        },

        onError: (

            error,

            variables,

            context,

        ) => {

            options.onError?.(

                error,

                variables,

                context,

            );

        },

    });

}

// ==========================================================
// Notifications
// ==========================================================

export function useNotificationSettings() {

    return useQuery({

        queryKey:
            NOTIFICATION_SETTINGS_QUERY_KEY,

        queryFn:
            getNotificationSettings,

    });

}

export function useUpdateNotificationSettings(

    options = {},

) {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            updateNotificationSettings,

        onSuccess: (

            data,

            variables,

            context,

        ) => {

            queryClient.invalidateQueries({

                queryKey:
                    NOTIFICATION_SETTINGS_QUERY_KEY,

            });

            options.onSuccess?.(

                data,

                variables,

                context,

            );

        },

        onError: (

            error,

            variables,

            context,

        ) => {

            options.onError?.(

                error,

                variables,

                context,

            );

        },

    });

}

// ==========================================================
// Network
// ==========================================================

export function useNetworkSettings() {

    return useQuery({

        queryKey:
            NETWORK_SETTINGS_QUERY_KEY,

        queryFn:
            getNetworkSettings,

    });

}

export function useUpdateNetworkSettings(

    options = {},

) {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            updateNetworkSettings,

        onSuccess: (

            data,

            variables,

            context,

        ) => {

            queryClient.invalidateQueries({

                queryKey:
                    NETWORK_SETTINGS_QUERY_KEY,

            });

            options.onSuccess?.(

                data,

                variables,

                context,

            );

        },

        onError: (

            error,

            variables,

            context,

        ) => {

            options.onError?.(

                error,

                variables,

                context,

            );

        },

    });

}

// ==========================================================
// Billing
// ==========================================================

export function useBillingSettings() {

    return useQuery({

        queryKey:
            BILLING_SETTINGS_QUERY_KEY,

        queryFn:
            getBillingSettings,

    });

}

export function useUpdateBillingSettings(

    options = {},

) {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            updateBillingSettings,

        onSuccess: (

            data,

            variables,

            context,

        ) => {

            queryClient.invalidateQueries({

                queryKey:
                    BILLING_SETTINGS_QUERY_KEY,

            });

            options.onSuccess?.(

                data,

                variables,

                context,

            );

        },

        onError: (

            error,

            variables,

            context,

        ) => {

            options.onError?.(

                error,

                variables,

                context,

            );

        },

    });

}

// ==========================================================
// Integrations
// ==========================================================

export function useIntegrationSettings() {

    return useQuery({

        queryKey:
            INTEGRATION_SETTINGS_QUERY_KEY,

        queryFn:
            getIntegrationSettings,

    });

}

export function useUpdateIntegrationSettings(

    options = {},

) {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            updateIntegrationSettings,

        onSuccess: (

            data,

            variables,

            context,

        ) => {

            queryClient.invalidateQueries({

                queryKey:
                    INTEGRATION_SETTINGS_QUERY_KEY,

            });

            options.onSuccess?.(

                data,

                variables,

                context,

            );

        },

        onError: (

            error,

            variables,

            context,

        ) => {

            options.onError?.(

                error,

                variables,

                context,

            );

        },

    });

}

// ==========================================================
// Branding
// ==========================================================

export function useBrandingSettings() {

    return useQuery({

        queryKey:
            BRANDING_SETTINGS_QUERY_KEY,

        queryFn:
            getBrandingSettings,

    });

}

export function useUpdateBrandingSettings(

    options = {},

) {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            updateBrandingSettings,

        onSuccess: (

            data,

            variables,

            context,

        ) => {

            queryClient.invalidateQueries({

                queryKey:
                    BRANDING_SETTINGS_QUERY_KEY,

            });

            options.onSuccess?.(

                data,

                variables,

                context,

            );

        },

        onError: (

            error,

            variables,

            context,

        ) => {

            options.onError?.(

                error,

                variables,

                context,

            );

        },

    });

}

// ==========================================================
// System
// ==========================================================

export function useSystemSettings() {

    return useQuery({

        queryKey:
            SYSTEM_SETTINGS_QUERY_KEY,

        queryFn:
            getSystemSettings,

    });

}

export function useUpdateSystemSettings(

    options = {},

) {

    const queryClient =
        useQueryClient();

    return useMutation({

        mutationFn:
            updateSystemSettings,

        onSuccess: (

            data,

            variables,

            context,

        ) => {

            queryClient.invalidateQueries({

                queryKey:
                    SYSTEM_SETTINGS_QUERY_KEY,

            });

            options.onSuccess?.(

                data,

                variables,

                context,

            );

        },

        onError: (

            error,

            variables,

            context,

        ) => {

            options.onError?.(

                error,

                variables,

                context,

            );

        },

    });

}