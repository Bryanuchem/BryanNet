import {
    Navigate,
    Outlet,
    useLocation,
} from "react-router-dom";

import {
    Box,
    CircularProgress,
} from "@mui/material";

import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute() {

    const {
        loading,
        isAuthenticated,
    } = useAuth();

    const location = useLocation();

    if (loading) {
        return (
            <Box
                sx={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    minHeight: "100vh",
                    bgcolor: "#F8FAFC",
                }}
            >
                <CircularProgress />
            </Box>
        );
    }

    if (!isAuthenticated) {
        return (
            <Navigate
                to="/login"
                replace
                state={{
                    from: location,
                }}
            />
        );
    }

    return <Outlet />;
}