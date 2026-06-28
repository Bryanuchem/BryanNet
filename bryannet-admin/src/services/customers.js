import client from "../api/client";

/**
 * Get all customers.
 */
export async function getCustomers() {
    const response = await client.get("/customers/");
    return response.data;
}

/**
 * Register a customer.
 */
export async function registerCustomer(
    customerData
) {
    const response = await client.post(
        "/customers/register",
        customerData
    );

    return response.data;
}

/**
 * Update customer.
 */
export async function updateCustomer(
    customerId,
    customerData
) {
    const response = await client.put(
        `/customers/${customerId}`,
        customerData
    );

    return response.data;
}

/**
 * Delete customer.
 */
export async function deleteCustomer(
    customerId
) {
    const response = await client.delete(
        `/customers/${customerId}`
    );

    return response.data;
}