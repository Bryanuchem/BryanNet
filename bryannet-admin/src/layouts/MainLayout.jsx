import Box from "@mui/material/Box";

import { Outlet } from "react-router-dom";

import Sidebar from "../components/layout/Sidebar";
import TopBar from "../components/layout/TopBar";

import {
    SIDEBAR_WIDTH,
    TOPBAR_HEIGHT,
} from "../config/layout";

import { useLayout } from "../context/LayoutContext";

const COLLAPSED_WIDTH = 88;

export default function MainLayout() {

    const {
        sidebarCollapsed,
    } = useLayout();

    const sidebarWidth = sidebarCollapsed
        ? COLLAPSED_WIDTH
        : SIDEBAR_WIDTH;

    return (

        <Box
            sx={{
                display: "flex",
                minHeight: "100vh",
                bgcolor: "#F8FAFC",
            }}
        >

            {/* Sidebar */}

            <Box
                sx={{
                    position: "fixed",
                    top: 0,
                    left: 0,
                    bottom: 0,
                    width: sidebarWidth,
                    zIndex: 1200,
                    transition: "width .25s ease",
                }}
            >

                <Sidebar />

            </Box>

            {/* Main Content */}

            <Box
                sx={{
                    flexGrow: 1,
                    ml: `${sidebarWidth}px`,
                    transition: "margin .25s ease",
                    minHeight: "100vh",
                    display: "flex",
                    flexDirection: "column",
                }}
            >

                {/* Top Bar */}

                <Box
                    sx={{
                        position: "fixed",
                        top: 0,
                        left: `${sidebarWidth}px`,
                        right: 0,
                        zIndex: 1100,
                        transition:
                            "left .25s ease",
                    }}
                >

                    <TopBar />

                </Box>

                {/* Page */}

                <Box
                    component="main"
                    sx={{
                        flexGrow: 1,
                        mt: `${TOPBAR_HEIGHT}px`,
                        p: 4,
                        overflow: "auto",
                    }}
                >

                    <Outlet />

                </Box>

            </Box>

        </Box>

    );

}