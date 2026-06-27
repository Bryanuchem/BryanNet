import client from "../api/client";

export async function getHealth() {
    const response = await client.get("/health");
    return response.data;
}