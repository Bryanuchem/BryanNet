import DashboardRoundedIcon from "@mui/icons-material/DashboardRounded";
import PeopleAltRoundedIcon from "@mui/icons-material/PeopleAltRounded";
import RouterRoundedIcon from "@mui/icons-material/RouterRounded";
import Inventory2RoundedIcon from "@mui/icons-material/Inventory2Rounded";
import ReceiptLongRoundedIcon from "@mui/icons-material/ReceiptLongRounded";
import PaymentsRoundedIcon from "@mui/icons-material/PaymentsRounded";
import SettingsRoundedIcon from "@mui/icons-material/SettingsRounded";
import AdminPanelSettingsRoundedIcon from "@mui/icons-material/AdminPanelSettingsRounded";

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
        path: "/administration",
        icon: AdminPanelSettingsRoundedIcon,
    },
    {
        section: "System",
        label: "Settings",
        path: "/settings",
        icon: SettingsRoundedIcon,
    },
];

export default navigation;