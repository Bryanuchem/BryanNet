import {
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import MainLayout from "../layouts/MainLayout";
import PublicLayout from "../layouts/PublicLayout";

import ProtectedRoute from "./ProtectedRoute";
import PublicRoute from "./PublicRoute";

import Dashboard from "../pages/Dashboard";
import Customers from "../pages/Customers";
import Devices from "../pages/Devices";
import Login from "../pages/Login";
import NotFound from "../pages/NotFound";
import Plans from "../pages/Plans";
import Subscriptions from "../pages/Subscriptions";

export default function AppRoutes() {

    return (

        <Routes>

            {/* ==========================
                Public Routes
            ========================== */}

            <Route element={<PublicRoute />}>

                <Route element={<PublicLayout />}>

                    <Route
                        path="/login"
                        element={<Login />}
                    />

                </Route>

            </Route>

            {/* ==========================
                Protected Routes
            ========================== */}

            <Route element={<ProtectedRoute />}>

                <Route element={<MainLayout />}>

                    <Route
                        path="/"
                        element={
                            <Navigate
                                to="/dashboard"
                                replace
                            />
                        }
                    />

                    <Route
                        path="/dashboard"
                        element={<Dashboard />}
                    />

                    <Route
                        path="/customers"
                        element={<Customers />}
                    />

                    <Route
                        path="/plans"
                        element={<Plans />}
                    />

                    <Route
                        path="/subscriptions"
                        element={<Subscriptions />}
                    />

                    <Route
                        path="/devices"
                        element={<Devices />}
                    />

                </Route>

            </Route>

            {/* ==========================
                404
            ========================== */}

            <Route
                path="*"
                element={<NotFound />}
            />

        </Routes>

    );

}