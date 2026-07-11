import {
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import MainLayout from "../layouts/MainLayout";
import PublicLayout from "../layouts/PublicLayout";

import ProtectedRoute from "./ProtectedRoute";
import PublicRoute from "./PublicRoute";

import PermissionRoute from "../components/permissions/PermissionRoute";
import SettingsIndexRedirect from "../components/permissions/SettingsIndexRedirect";

import Unauthorized from "../pages/Unauthorized";

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

                    {/* ==========================
                        Dashboard
                    ========================== */}

                    <Route

                        path="/dashboard"

                        element={

                            <PermissionRoute

                                permission="dashboard.view"

                            >

                                <Dashboard />

                            </PermissionRoute>

                        }

                    />

                    {/* ==========================
                        Customers
                    ========================== */}

                    <Route

                        path="/customers"

                        element={

                            <PermissionRoute

                                permission="customers.view"

                            >

                                <Customers />

                            </PermissionRoute>

                        }

                    />

                    <Route

                        path="/devices"

                        element={

                            <PermissionRoute

                                permission="devices.view"

                            >

                                <Devices />

                            </PermissionRoute>

                        }

                    />

                    {/* ==========================
                        Services
                    ========================== */}

                    <Route

                        path="/plans"

                        element={

                            <PermissionRoute

                                permission="plans.view"

                            >

                                <Plans />

                            </PermissionRoute>

                        }

                    />

                    <Route

                        path="/subscriptions"

                        element={

                            <PermissionRoute

                                permission="subscriptions.view"

                            >

                                <Subscriptions />

                            </PermissionRoute>

                        }

                    />

                    {/* ==========================
                        Operations
                    ========================== */}

                    <Route

                        path="/payments"

                        element={

                            <PermissionRoute

                                permission="payments.view"

                            >

                                <Payments />

                            </PermissionRoute>

                        }

                    />

                    {/* ==========================
                        Administration
                    ========================== */}

                    <Route

                        path="/administration"

                        element={

                            <PermissionRoute

                                permission="administration.view"

                            >

                                <Overview />

                            </PermissionRoute>

                        }

                    />

                    <Route

                        path="/administration/users"

                        element={

                            <PermissionRoute

                                permission="admin_users.view"

                            >

                                <AdminUsers />

                            </PermissionRoute>

                        }

                    />

                    <Route

                        path="/administration/roles"

                        element={

                            <PermissionRoute

                                permission="roles.view"

                            >

                                <RolesPermissions />

                            </PermissionRoute>

                        }

                    />

                    <Route

                        path="/administration/audit-logs"

                        element={

                            <PermissionRoute

                                permission="audit_logs.view"

                            >

                                <AuditLogs />

                            </PermissionRoute>

                        }

                    />

                    <Route

                        path="/administration/sessions"

                        element={

                            <PermissionRoute

                                permission="login_sessions.view"

                            >

                                <LoginSessions />

                            </PermissionRoute>

                        }

                    />

                    <Route

                        path="/administration/system-activity"

                        element={

                            <PermissionRoute

                                permission="system_activity.view"

                            >

                                <SystemActivity />

                            </PermissionRoute>

                        }

                    />

                    {/* ==========================
                        Settings
                    ========================== */}

                    <Route

                        path="/settings"

                        element={

                            <PermissionRoute

                                permission="settings.view"

                            >

                                <Settings />

                            </PermissionRoute>

                        }

                    >

                        <Route

                            index

                            element={

                                <SettingsIndexRedirect />

                            }

                        />

                        <Route

                            path="general"

                            element={

                                <PermissionRoute

                                    permission="settings.general"

                                >

                                    <General />

                                </PermissionRoute>

                            }

                        />

                        <Route

                            path="authentication"

                            element={

                                <PermissionRoute

                                    permission="settings.authentication"

                                >

                                    <Authentication />

                                </PermissionRoute>

                            }

                        />

                        <Route

                            path="notifications"

                            element={

                                <PermissionRoute

                                    permission="settings.notifications"

                                >

                                    <Notifications />

                                </PermissionRoute>

                            }

                        />

                        <Route

                            path="network"

                            element={

                                <PermissionRoute

                                    permission="settings.network"

                                >

                                    <Network />

                                </PermissionRoute>

                            }

                        />

                        <Route

                            path="billing"

                            element={

                                <PermissionRoute

                                    permission="settings.billing"

                                >

                                    <Billing />

                                </PermissionRoute>

                            }

                        />

                        <Route

                            path="integrations"

                            element={

                                <PermissionRoute

                                    permission="settings.integrations"

                                >

                                    <Integrations />

                                </PermissionRoute>

                            }

                        />

                        <Route

                            path="branding"

                            element={

                                <PermissionRoute

                                    permission="settings.branding"

                                >

                                    <Branding />

                                </PermissionRoute>

                            }

                        />

                        <Route

                            path="system"

                            element={

                                <PermissionRoute

                                    permission="settings.system"

                                >

                                    <System />

                                </PermissionRoute>

                            }

                        />

                    </Route>

                    {/* ==========================
                        Unauthorized
                    ========================== */}

                    <Route

                        path="/unauthorized"

                        element={<Unauthorized />}

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