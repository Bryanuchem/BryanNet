import apiClient from "./client";

export async function getDashboardSummary() {

    const response = await apiClient.get(
        "/dashboard/summary"
    );

    return response.data;

}

export async function getRevenueOverview(
    period = "month"
) {

    const response = await apiClient.get(
        "/dashboard/revenue-overview",
        {
            params: {
                period,
            },
        }
    );

    return response.data;

}

export async function getSubscriptionBreakdown() {

    const response = await apiClient.get(
        "/dashboard/subscription-breakdown"
    );

    return response.data;

}


export async function getRecentActivity(
    limit = 10,
) {

    const response = await apiClient.get(
        "/dashboard/recent-activity",
        {
            params: {
                limit,
            },
        },
    );

    return response.data;

}