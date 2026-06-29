import api from "./axios";

/**
 * Get all internet plans.
 */
export const getPlans = async () => {
    const response = await api.get("/plans");
    return response.data;
};

/**
 * Get a single plan by ID.
 */
export const getPlan = async (planId) => {
    const response = await api.get(
        `/plans/${planId}`
    );

    return response.data;
};

/**
 * Create a new plan.
 */
export const createPlan = async (planData) => {
    const response = await api.post(
        "/plans",
        planData
    );

    return response.data;
};

/**
 * Update an existing plan.
 */
export const updatePlan = async ({
    planId,
    data,
}) => {
    const response = await api.put(
        `/plans/${planId}`,
        data
    );

    return response.data;
};

/**
 * Delete a plan.
 */
export const deletePlan = async (
    planId
) => {
    const response = await api.delete(
        `/plans/${planId}`
    );

    return response.data;
};

/**
 * Activate or deactivate a plan.
 */
export const updatePlanStatus = async ({
    planId,
    isActive,
}) => {
    const response = await api.patch(
        `/plans/${planId}/status`,
        null,
        {
            params: {
                is_active: isActive,
            },
        }
    );

    return response.data;
};