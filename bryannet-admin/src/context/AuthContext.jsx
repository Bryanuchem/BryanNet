import {
    createContext,
    useContext,
    useEffect,
    useState,
} from "react";

import authService from "../services/authService";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {

    const [admin, setAdmin] = useState(null);

    const [loading, setLoading] = useState(true);

    const [isAuthenticated, setIsAuthenticated] = useState(false);

    const login = async (username, password) => {

        const response = await authService.login({
            username,
            password,
        });

        localStorage.setItem(
            "access_token",
            response.access_token
        );

        const currentAdmin =
            await authService.getCurrentAdmin();

        setAdmin(currentAdmin);

        setIsAuthenticated(true);

        return currentAdmin;

    };

    const logout = () => {

        localStorage.removeItem(
            "access_token"
        );

        setAdmin(null);

        setIsAuthenticated(false);

    };

    useEffect(() => {

        const initialize = async () => {

            const token =
                localStorage.getItem(
                    "access_token"
                );

            if (!token) {

                setLoading(false);

                return;

            }

            try {

                const currentAdmin =
                    await authService.getCurrentAdmin();

                setAdmin(currentAdmin);

                setIsAuthenticated(true);

            }

            catch (error) {

                console.error(
                    "Session restore failed:",
                    error
                );

                localStorage.removeItem(
                    "access_token"
                );

                setAdmin(null);

                setIsAuthenticated(false);

            }

            finally {

                setLoading(false);

            }

        };

        initialize();

    }, []);

    const value = {

        admin,

        loading,

        isAuthenticated,

        login,

        logout,

    };

    return (

        <AuthContext.Provider value={value}>

            {children}

        </AuthContext.Provider>

    );

}

export function useAuth() {

    const context = useContext(
        AuthContext
    );

    if (!context) {

        throw new Error(
            "useAuth must be used inside an AuthProvider."
        );

    }

    return context;

}