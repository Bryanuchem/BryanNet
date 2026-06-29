import apiClient from "./client";

export const getSubscriptions = async () => {
    const response = await apiClient.get("/subscriptions/");
    return response.data;
};

export const getSubscription = async (subscriptionId) => {
    const response = await apiClient.get(
        `/subscriptions/${subscriptionId}`
    );

    return response.data;
};

export const updateSubscription = async ({
    subscriptionId,
    data,
}) => {
    const response = await apiClient.patch(
        `/subscriptions/${subscriptionId}`,
        data
    );

    return response.data;
};

export const updateSubscriptionStatus = async ({
    subscriptionId,
    status,
}) => {
    const response = await apiClient.patch(
        `/subscriptions/${subscriptionId}/status`,
        {
            status,
        }
    );

    return response.data;
};

export const renewSubscription = async (
    subscriptionId
) => {
    const response = await apiClient.post(
        `/subscriptions/${subscriptionId}/renew`
    );

    return response.data;
};

export const deleteSubscription = async (
    subscriptionId
) => {
    const response = await apiClient.delete(
        `/subscriptions/${subscriptionId}`
    );

    return response.data;
};