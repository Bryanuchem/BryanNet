import api from "./axios";

/**
 * Get all plans.
 */
export const getPlans = async (params = {}) => {

    const response = await api.get(
        "/plans",
        {
            params,
        },
    );

    return response.data;

};

/**
 * Get a single plan.
 */
export const getPlan = async (
    planId,
) => {

    const response = await api.get(
        `/plans/${planId}`,
    );

    return response.data;

};

/**
 * Get all active plans.
 */
export const getActivePlans =
    async () => {

        const response = await api.get(
            "/plans/active",
        );

        return response.data;

    };

/**
 * Create a new plan.
 */
export const createPlan = async (
    planData,
) => {

    const response = await api.post(
        "/plans",
        planData,
    );

    return response.data;

};

/**
 * Update a plan.
 */
export const updatePlan = async (
    planId,
    planData,
) => {

    const response = await api.put(
        `/plans/${planId}`,
        planData,
    );

    return response.data;

};

/**
 * Activate a plan.
 */
export const activatePlan =
    async (planId) => {

        const response = await api.patch(
            `/plans/${planId}/activate`,
        );

        return response.data;

    };

/**
 * Deactivate a plan.
 */
export const deactivatePlan =
    async (planId) => {

        const response = await api.patch(
            `/plans/${planId}/deactivate`,
        );

        return response.data;

    };