import apiClient from "./client";

export async function getAdministrationOverview() {

    const response = await apiClient.get(
        "/administration/overview",
    );

    return response.data;

}