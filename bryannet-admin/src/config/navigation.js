import DashboardRoundedIcon from "@mui/icons-material/DashboardRounded";
import PeopleAltRoundedIcon from "@mui/icons-material/PeopleAltRounded";
import RouterRoundedIcon from "@mui/icons-material/RouterRounded";
import Inventory2RoundedIcon from "@mui/icons-material/Inventory2Rounded";
import ReceiptLongRoundedIcon from "@mui/icons-material/ReceiptLongRounded";
import PaymentsRoundedIcon from "@mui/icons-material/PaymentsRounded";
import AdminPanelSettingsRoundedIcon from "@mui/icons-material/AdminPanelSettingsRounded";

import settingsNavigation from "../navigation/settingsNavigation";

const navigation = [
    // =========================
    // Overview
    // =========================

    {
        section: "Overview",
        label: "Dashboard",
        path: "/dashboard",
        icon: DashboardRoundedIcon,
        permission: "dashboard.view",
    },

    // =========================
    // Customers
    // =========================

    {
        section: "Customers",
        label: "Customers",
        path: "/customers",
        icon: PeopleAltRoundedIcon,
        permission: "customers.view",
    },
    {
        section: "Customers",
        label: "Devices",
        path: "/devices",
        icon: RouterRoundedIcon,
        permission: "devices.view",
    },

    // =========================
    // Services
    // =========================

    {
        section: "Services",
        label: "Plans",
        path: "/plans",
        icon: Inventory2RoundedIcon,
        permission: "plans.view",
    },
    {
        section: "Services",
        label: "Subscriptions",
        path: "/subscriptions",
        icon: ReceiptLongRoundedIcon,
        permission: "subscriptions.view",
    },

    // =========================
    // Operations
    // =========================

    {
        section: "Operations",
        label: "Payments",
        path: "/payments",
        icon: PaymentsRoundedIcon,
        permission: "payments.view",
    },

    // =========================
    // System
    // =========================

    {
        section: "System",
        label: "Administration",
        icon: AdminPanelSettingsRoundedIcon,
        permission: "administration.view",

        children: [

            {

                label: "Overview",

                path: "/administration",

                permission: "administration.view",

            },

            {

                label: "Admin Users",

                path: "/administration/users",

                permission: "admin_users.view",

            },

            {

                label: "Roles & Permissions",

                path: "/administration/roles",

                permission: "roles.view",

            },

            {

                label: "Audit Logs",

                path: "/administration/audit-logs",

                permission: "audit_logs.view",

            },

            {

                label: "Login Sessions",

                path: "/administration/sessions",

                permission: "login_sessions.view",

            },

            {

                label: "System Activity",

                path: "/administration/system-activity",

                permission: "system_activity.view",

            },

        ],
    },

    {
        section: "System",
        label: settingsNavigation.title,
        icon: settingsNavigation.icon,

        children: settingsNavigation.children.map(

            (item) => ({

                label: item.title,

                path: item.path,

                permission: item.permission,

            }),

        ),
    },
];

export default navigation;