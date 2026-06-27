import DashboardIcon from "@mui/icons-material/Dashboard";
import PeopleIcon from "@mui/icons-material/People";
import Inventory2Icon from "@mui/icons-material/Inventory2";
import ReceiptLongIcon from "@mui/icons-material/ReceiptLong";
import DevicesIcon from "@mui/icons-material/Devices";

const navigation = [
    {
        label: "Dashboard",
        path: "/",
        icon: DashboardIcon,
    },
    {
        label: "Customers",
        path: "/customers",
        icon: PeopleIcon,
    },
    {
        label: "Plans",
        path: "/plans",
        icon: Inventory2Icon,
    },
    {
        label: "Subscriptions",
        path: "/subscriptions",
        icon: ReceiptLongIcon,
    },
    {
        label: "Devices",
        path: "/devices",
        icon: DevicesIcon,
    }
];

export default navigation;