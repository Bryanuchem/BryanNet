import api from "./axios";

/**
 * Get all customers.
 */
export const getCustomers = async () => {
    const response = await api.get("/customers");
    return response.data;
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
 * Delete a customer.
 */
export const deleteCustomer = async (
    customerId
) => {
    const response = await api.delete(
        `/customers/${customerId}`
    );

    return response.data;
};