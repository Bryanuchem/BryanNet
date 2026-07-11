import apiClient from "./client";

// ==========================================================
// Query Methods
// ==========================================================

export async function getPayments(
    filters = {},
) {

    const response = await apiClient.get(
        "/payments",
        {
            params: {

                page: filters.page,

                page_size: filters.pageSize,

                search: filters.search,

                payment_channel:
                    filters.payment_channel,

                status:
                    filters.status,

            },
        },
    );

    return response.data;

}

export async function getPaymentSummary() {

    const response = await apiClient.get(
        "/payments/summary",
    );

    return response.data;

}

export async function getPayment(
    paymentReference,
) {

    const response = await apiClient.get(
        `/payments/${paymentReference}`,
    );

    return response.data;

}

export async function getCustomerPayments(
    customerId,
) {

    const response = await apiClient.get(
        `/payments/customer/${customerId}`,
    );

    return response.data;

}

export async function getPaymentReceipt(
    paymentReference,
) {

    const response = await apiClient.get(

        `/payments/${paymentReference}/receipt`,

        {

            responseType: "blob",

        },

    );

    return response.data;

}

// ==========================================================
// Business Commands
// ==========================================================

export async function createPayment(
    paymentData,
) {

    const response = await apiClient.post(
        "/payments",
        paymentData,
    );

    return response.data;

}

export async function completePayment(
    paymentReference,
    gatewayTransactionId = null,
) {

    const response = await apiClient.post(

        `/payments/${paymentReference}/complete`,

        null,

        {

            params: {

                gateway_transaction_id:
                    gatewayTransactionId,

            },

        },

    );

    return response.data;

}

export async function cancelPayment(
    paymentReference,
) {

    const response = await apiClient.patch(
        `/payments/${paymentReference}/cancel`,
    );

    return response.data;

}

export async function refundPayment(
    paymentReference,
) {

    const response = await apiClient.patch(
        `/payments/${paymentReference}/refund`,
    );

    return response.data;

}

export async function expirePayment(
    paymentReference,
) {

    const response = await apiClient.patch(
        `/payments/${paymentReference}/expire`,
    );

    return response.data;

}