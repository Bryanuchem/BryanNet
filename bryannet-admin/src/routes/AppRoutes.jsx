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
import Payments from "../pages/Payments";

import Settings from "../pages/Settings";

import General from "../pages/Settings/General";
import Authentication from "../pages/Settings/Authentication";
import Notifications from "../pages/Settings/Notifications";
import Network from "../pages/Settings/Network";
import Billing from "../pages/Settings/Billing";
import Integrations from "../pages/Settings/Integrations";
import Branding from "../pages/Settings/Branding";
import System from "../pages/Settings/System";

// Administration
import Overview from "../pages/Administration/Overview";
import AdminUsers from "../pages/Administration/AdminUsers";
import RolesPermissions from "../pages/Administration/RolesPermissions";
import AuditLogs from "../pages/Administration/AuditLogs";
import LoginSessions from "../pages/Administration/LoginSessions";
import SystemActivity from "../pages/Administration/SystemActivity";

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

                    <Route
                        path="/payments"
                        element={<Payments />}
                    />

                    {/* ==========================
                        Administration
                    ========================== */}

                    <Route
                        path="/administration"
                        element={<Overview />}
                    />

                    <Route
                        path="/administration/users"
                        element={<AdminUsers />}
                    />

                    <Route
                        path="/administration/roles"
                        element={<RolesPermissions />}
                    />

                    <Route
                        path="/administration/audit-logs"
                        element={<AuditLogs />}
                    />

                    <Route
                        path="/administration/sessions"
                        element={<LoginSessions />}
                    />

                    <Route
                        path="/administration/system-activity"
                        element={<SystemActivity />}
                    />

                    {/* ==========================
                        Settings
                    ========================== */}

                    <Route
                        path="/settings"
                        element={<Settings />}
                    >
                        <Route
                            index
                            element={<Navigate to="general" replace />}
                        />

                        <Route
                            path="general"
                            element={<General />}
                        />

                        <Route
                            path="authentication"
                            element={<Authentication />}
                        />

                        <Route
                            path="notifications"
                            element={<Notifications />}
                        />

                        <Route
                            path="network"
                            element={<Network />}
                        />

                        <Route
                            path="billing"
                            element={<Billing />}
                        />

                        <Route
                            path="integrations"
                            element={<Integrations />}
                        />

                        <Route
                            path="branding"
                            element={<Branding />}
                        />

                        <Route
                            path="system"
                            element={<System />}
                        />
                    </Route>

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