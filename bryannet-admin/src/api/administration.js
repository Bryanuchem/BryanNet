import apiClient from "./client";

export async function getAdministrationOverview() {
    const response = await apiClient.get("/admin/overview");

    return response.data;
}