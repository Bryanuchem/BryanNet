import Box from "@mui/material/Box";

import SidebarBrand from "./SidebarBrand";
import SidebarNavigation from "./SidebarNavigation";
import SidebarFooter from "./SidebarFooter";

import { SIDEBAR_WIDTH } from "../../config/layout";
import { useLayout } from "../../context/LayoutContext";

const COLLAPSED_WIDTH = 88;

export default function Sidebar() {

    const {
        sidebarCollapsed,
    } = useLayout();

    return (

        <Box
            sx={{
                width: sidebarCollapsed
                    ? COLLAPSED_WIDTH
                    : SIDEBAR_WIDTH,

                height: "100vh",

                bgcolor: "#0F172A",

                color: "#FFFFFF",

                display: "flex",

                flexDirection: "column",

                overflow: "hidden",

                borderRight: "1px solid rgba(255,255,255,0.06)",

                boxShadow: "4px 0 20px rgba(15,23,42,0.15)",

                transition: (theme) =>
                    theme.transitions.create(
                        "width",
                        {
                            duration: 250,
                        }
                    ),

                userSelect: "none",
            }}
        >

            {/* Brand */}

            <SidebarBrand />

            {/* Navigation */}

            <Box
                sx={{
                    flex: 1,
                    overflowY: "auto",
                    overflowX: "hidden",

                    "&::-webkit-scrollbar": {
                        width: 6,
                    },

                    "&::-webkit-scrollbar-thumb": {
                        backgroundColor:
                            "rgba(255,255,255,0.12)",
                        borderRadius: 10,
                    },

                    "&::-webkit-scrollbar-track": {
                        background: "transparent",
                    },
                }}
            >

                <SidebarNavigation />

            </Box>

            {/* Footer */}

            <SidebarFooter />

        </Box>

    );

}