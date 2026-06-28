import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import {
    Avatar,
    Box,
    Divider,
    IconButton,
    Menu,
    MenuItem,
    Stack,
    Typography,
} from "@mui/material";

import MenuRoundedIcon from "@mui/icons-material/MenuRounded";
import NotificationsNoneRoundedIcon from "@mui/icons-material/NotificationsNoneRounded";
import KeyboardArrowDownRoundedIcon from "@mui/icons-material/KeyboardArrowDownRounded";
import LogoutRoundedIcon from "@mui/icons-material/LogoutRounded";
import PersonRoundedIcon from "@mui/icons-material/PersonRounded";

import { TOPBAR_HEIGHT } from "../../config/layout";
import { useAuth } from "../../context/AuthContext";
import { useLayout } from "../../context/LayoutContext";

const pageTitles = {
    "/dashboard": "Dashboard",
    "/customers": "Customers",
    "/plans": "Plans",
    "/subscriptions": "Subscriptions",
    "/devices": "Devices",
    "/payments": "Payments",
    "/administration": "Administration",
    "/settings": "Settings",
};

export default function TopBar() {

    const location = useLocation();

    const navigate = useNavigate();

    const { admin, logout } = useAuth();

    const {
        toggleSidebar,
    } = useLayout();

    const [anchorEl, setAnchorEl] = useState(null);

    const open = Boolean(anchorEl);

    const pageTitle =
        pageTitles[location.pathname] ?? "BryanNet";

    const initials =
        admin?.username?.charAt(0)?.toUpperCase() ?? "A";

    const handleMenuOpen = (event) => {

        setAnchorEl(event.currentTarget);

    };

    const handleMenuClose = () => {

        setAnchorEl(null);

    };

    const handleLogout = () => {

        handleMenuClose();

        logout();

        navigate("/login", {
            replace: true,
        });

    };

    return (

        <Box
            sx={{
                height: TOPBAR_HEIGHT,
                bgcolor: "#FFFFFF",
                borderBottom: "1px solid #E2E8F0",
                px: 4,
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
            }}
        >

            {/* Left Section */}

            <Stack
                direction="row"
                spacing={2}
                alignItems="center"
            >

                <IconButton
                    onClick={toggleSidebar}
                    sx={{
                        border: "1px solid #E2E8F0",

                        "&:hover": {
                            bgcolor: "#F8FAFC",
                        },
                    }}
                >

                    <MenuRoundedIcon />

                </IconButton>

                <Box>

                    <Typography
                        variant="h5"
                        sx={{
                            fontWeight: 700,
                            color: "#0F172A",
                            lineHeight: 1.2,
                        }}
                    >
                        {pageTitle}
                    </Typography>

                    <Typography
                        sx={{
                            mt: 0.5,
                            fontSize: "0.85rem",
                            color: "#64748B",
                        }}
                    >
                        BryanNet ISP Management Platform
                    </Typography>

                </Box>

            </Stack>

            {/* Right Section */}

            <Stack
                direction="row"
                spacing={2}
                alignItems="center"
            >

                <IconButton
                    sx={{
                        border: "1px solid #E2E8F0",

                        "&:hover": {
                            bgcolor: "#F8FAFC",
                        },
                    }}
                >

                    <NotificationsNoneRoundedIcon />

                </IconButton>

                <Divider
                    orientation="vertical"
                    flexItem
                />

                <Stack
                    direction="row"
                    spacing={1.5}
                    alignItems="center"
                    onClick={handleMenuOpen}
                    sx={{
                        cursor: "pointer",
                    }}
                >

                    <Avatar
                        sx={{
                            width: 40,
                            height: 40,
                            bgcolor: "#2563EB",
                            fontWeight: 700,
                        }}
                    >
                        {initials}
                    </Avatar>

                    <Box>

                        <Typography
                            sx={{
                                fontWeight: 600,
                                color: "#0F172A",
                                lineHeight: 1.2,
                            }}
                        >
                            {admin?.username ??
                                "Administrator"}
                        </Typography>

                        <Typography
                            sx={{
                                fontSize: "0.8rem",
                                color: "#64748B",
                            }}
                        >
                            {admin?.role?.replace(
                                "_",
                                " "
                            ) ?? "SUPER ADMIN"}
                        </Typography>

                    </Box>

                    <KeyboardArrowDownRoundedIcon
                        sx={{
                            color: "#64748B",
                        }}
                    />

                </Stack>

            </Stack>

            <Menu
                anchorEl={anchorEl}
                open={open}
                onClose={handleMenuClose}
                PaperProps={{
                    elevation: 4,
                    sx: {
                        mt: 1,
                        minWidth: 220,
                        borderRadius: 3,
                    },
                }}
            >

                <MenuItem
                    disabled
                >

                    <PersonRoundedIcon
                        sx={{
                            mr: 1.5,
                        }}
                    />

                    My Profile

                </MenuItem>

                <Divider />

                <MenuItem
                    onClick={handleLogout}
                >

                    <LogoutRoundedIcon
                        sx={{
                            mr: 1.5,
                        }}
                    />

                    Logout

                </MenuItem>

            </Menu>

        </Box>

    );

}