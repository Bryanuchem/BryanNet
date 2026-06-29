import apiClient from "./client";

export async function getPayments(
    filters = {},
) {

    const response = await apiClient.get(
        "/payments",
        {
            params: filters,
        },
    );

    return response.data;

}

export async function getPaymentStats() {

    const response = await apiClient.get(
        "/payments/summary",
    );

    return response.data;

}

export async function getPayment(
    paymentId,
) {

    const response = await apiClient.get(
        `/payments/${paymentId}`,
    );

    return response.data;

}

export async function createPayment(
    paymentData,
) {

    const response = await apiClient.post(
        "/payments",
        paymentData,
    );

    return response.data;

}

export async function updatePayment({

    paymentId,

    data,

}) {

    const response = await apiClient.put(
        `/payments/${paymentId}`,
        data,
    );

    return response.data;

}

export async function deletePayment(
    paymentId,
) {

    const response = await apiClient.delete(
        `/payments/${paymentId}`,
    );

    return response.data;

}