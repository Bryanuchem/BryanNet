import client from "../api/client";

export async function getCustomers() {
    const response = await client.get("/customers");
    return response.data;
}