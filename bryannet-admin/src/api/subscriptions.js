import api from "./axios";

/**
 * Get all subscriptions.
 */
export const getSubscriptions = async (
    params = {},
) => {

    const response = await api.get(
        "/subscriptions",
        {
            params,
        },
    );

    return response.data;

};

/**
 * Get a single subscription.
 */
export const getSubscription = async (
    subscriptionId,
) => {

    const response = await api.get(
        `/subscriptions/${subscriptionId}`,
    );

    return response.data;

};

/**
 * Purchase a subscription.
 */
export const purchaseSubscription =
    async (subscriptionData) => {

        const response = await api.post(
            "/subscriptions/purchase",
            subscriptionData,
        );

        return response.data;

    };

/**
 * Cancel a subscription.
 */
export const cancelSubscription =
    async (subscriptionId) => {

        const response = await api.patch(
            `/subscriptions/${subscriptionId}/cancel`,
        );

        return response.data;

    };

/**
 * Process expired subscriptions.
 */
export const processSubscriptions =
    async () => {

        const response = await api.post(
            "/subscriptions/process",
        );

        return response.data;

    };

/**
 * Get subscriptions for a customer.
 */
export const getCustomerSubscriptions =
    async (customerId) => {

        const response = await api.get(
            `/subscriptions/customer/${customerId}`,
        );

        return response.data;

    };