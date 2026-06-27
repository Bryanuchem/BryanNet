import Box from "@mui/material/Box";

import SidebarBrand from "./SidebarBrand";
import SidebarNavigation from "./SidebarNavigation";
import SidebarFooter from "./SidebarFooter";
import { SIDEBAR_WIDTH } from "../../config/layout";

function Sidebar() {
    return (
        <Box
            sx={{
                width: SIDEBAR_WIDTH,
                height: "100vh",
                bgcolor: "#1E293B",
                color: "white",
                display: "flex",
                flexDirection: "column",
            }}
        >
            <SidebarBrand />

            <SidebarNavigation />

            <SidebarFooter />
        </Box>
    );
}

export default Sidebar;