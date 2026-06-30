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
    },

    // =========================
    // Customers
    // =========================

    {
        section: "Customers",
        label: "Customers",
        path: "/customers",
        icon: PeopleAltRoundedIcon,
    },
    {
        section: "Customers",
        label: "Devices",
        path: "/devices",
        icon: RouterRoundedIcon,
    },

    // =========================
    // Services
    // =========================

    {
        section: "Services",
        label: "Plans",
        path: "/plans",
        icon: Inventory2RoundedIcon,
    },
    {
        section: "Services",
        label: "Subscriptions",
        path: "/subscriptions",
        icon: ReceiptLongRoundedIcon,
    },

    // =========================
    // Operations
    // =========================

    {
        section: "Operations",
        label: "Payments",
        path: "/payments",
        icon: PaymentsRoundedIcon,
    },

    // =========================
    // System
    // =========================

    {
        section: "System",
        label: "Administration",
        icon: AdminPanelSettingsRoundedIcon,

        children: [
            {
                label: "Overview",
                path: "/administration",
            },
            {
                label: "Admin Users",
                path: "/administration/users",
            },
            {
                label: "Roles & Permissions",
                path: "/administration/roles",
            },
            {
                label: "Audit Logs",
                path: "/administration/audit-logs",
            },
            {
                label: "Login Sessions",
                path: "/administration/sessions",
            },
            {
                label: "System Activity",
                path: "/administration/system-activity",
            },
        ],
    },

    {
        section: "System",
        label: settingsNavigation.title,
        icon: settingsNavigation.icon,

        children: settingsNavigation.children.map((item) => ({
            label: item.title,
            path: item.path,
        })),
    },
];

export default navigation;