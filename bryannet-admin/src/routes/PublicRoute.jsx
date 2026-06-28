import {
    Navigate,
    Outlet,
} from "react-router-dom";

import {
    Box,
    CircularProgress,
} from "@mui/material";

import { useAuth } from "../context/AuthContext";

export default function PublicRoute() {

    const {
        loading,
        isAuthenticated,
    } = useAuth();

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

    if (isAuthenticated) {
        return (
            <Navigate
                to="/dashboard"
                replace
            />
        );
    }

    return <Outlet />;

}