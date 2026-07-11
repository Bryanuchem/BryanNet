import api from "./axios";

/**
 * Get all customers.
 */
export const getCustomers = async () => {

    const response = await api.get(
        "/customers",
    );

    return response.data.items;
};


/**
 * Register a new customer.
 */
export const registerCustomer = async (
    customerData
) => {
    const response = await api.post(
        "/customers/register",
        customerData
    );

    return response.data;
};

/**
 * Update a customer.
 */
export const updateCustomer = async (
    customerId,
    customerData
) => {
    const response = await api.put(
        `/customers/${customerId}`,
        customerData
    );

    return response.data;
};

/**
 * Activate a customer.
 */
export const activateCustomer = async (
    customerId,
) => {

    const response = await api.patch(
        `/customers/${customerId}/activate`,
    );

    return response.data;

};

/**
* Deactivate a customer.
 */
export const deactivateCustomer = async (
    customerId,
) => {

    const response = await api.patch(
        `/customers/${customerId}/deactivate`,
    );

    return response.data;

};