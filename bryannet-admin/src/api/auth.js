import client from "../api/client";

const authService = {
    login: async (credentials) => {
        const response = await client.post(
            "/auth/login",
            credentials
        );

        return response.data;
    },

    getCurrentAdmin: async () => {
        const response = await client.get(
            "/auth/me"
        );

        return response.data;
    },
};

export default authService;